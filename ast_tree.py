import os
import ast
import logging


def get_tree(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as attempt_handler:
            file_content = attempt_handler.read()
            return ast.parse(file_content)
    except IOError as e:
        logging.warning(
            '{0} I/O error({1}): {2}'.format(filename, e.errno, e.strerror)
        )
    except SyntaxError as e:
        logging.warning(
            '{0} SyntaxError error: {1}'.format(filename, e)
        )


def get_trees(path):
    ''' Функция формирования ast деревьев из .py файлов, расположенных
        в каталоге path
    '''
    filenames = get_filenames_in_path(path)
    return [get_tree(filename) for filename in filenames]


def get_trees_with_filenames(path):
    filenames = get_filenames_in_path(path)
    return [(filename, get_tree(filename)) for filename in filenames]


def get_trees_with_files_content(path):
    filenames = get_filenames_in_path(path)
    return [(filename, get_tree(filename)) for filename in filenames]


def get_all_names_in_tree(tree):
    ''' Получить все имена из ast дерева '''
    return [
        node.id for node in ast.walk(tree) if isinstance(node, ast.Name)
    ]


def get_names_in_ast_tree(tree, type_name='function'):
    ''' Получить список названий в дереве ast '''
    if type_name == 'function':
        names = [
            node.name.lower()
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef)
        ]
    if type_name == 'variable':
        names = [
            node.id.lower()
            for node in ast.walk(tree)
            if (isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store))
        ]
    return names if names else []


def get_filenames_in_path(path):
    ''' Получить все имена файлов с расширение .py в папке (рекурсивно) '''
    filenames = []
    for dirname, dirs, files in os.walk(path, topdown=True):
        # формируем список файлов с расширением .py в каждой папке
        filenames_current = [
            os.path.join(dirname, filename)
            for filename in files if filename.endswith('.py')
        ]
        filenames += filenames_current
    return filenames
