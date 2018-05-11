import os
import ast


def get_trees(path, with_filenames=False, with_file_content=False):
    ''' Функция формирования ast деревьев из .py файлов, расположенных
        в каталоге path
    '''
    # Получаем список файлов в каталоге
    filenames = get_filenames_in_path(path)
    # Собираем список ast деревьев
    trees = []
    for filename in filenames:
        with open(filename, 'r', encoding='utf-8') as attempt_handler:
            try:
                main_file_content = attempt_handler.read()
            except:
                continue
        try:
            tree = ast.parse(main_file_content)
        except SyntaxError:
            # print(e) - мы за чистые функции
            tree = None
        if with_filenames:
            if with_file_content:
                trees.append((filename, main_file_content, tree))
            else:
                trees.append((filename, tree))
        else:
            trees.append(tree)
    return trees


def get_all_names_in_tree(tree):
    ''' Получить все имена из ast дерева '''
    if not tree:
        return []
    return [
        node.id for node in ast.walk(tree) if isinstance(node, ast.Name)
    ]


def get_names_in_ast_tree(tree, type_name='function'):
    ''' Получить список названий в дереве ast '''
    if not tree:
        return []
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
    if not path:
        return []
    filenames = []
    for dirname, dirs, files in os.walk(path, topdown=True):
        # формируем список файлов с расширением .py в каждой папке
        filenames_current = [
            os.path.join(dirname, filename)
            for filename in files if filename.endswith('.py')
        ]
        # Накапливаем результат
        filenames += filenames_current
    return filenames
