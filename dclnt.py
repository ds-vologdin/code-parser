import ast
import os
import collections

from nltk import pos_tag


def flat(not_flat_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return [item for sublist in not_flat_list for item in sublist]


def is_verb(word):
    ''' Проверка на глагол '''
    if not word:
        return False
    pos_info = pos_tag([word])
    return pos_info[0][1] == 'VB'


def get_filenames_in_path(path, max_count_files=500):
    ''' Получить все имена файлов с расширение .py в папке (рекурсивно)
    max_count_files - ограничение на количества файлов
    '''
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

        # Проверяем набрали ли мы уже нужное количество файлов
        if len(filenames) >= max_count_files:
            # Обрезаем список до нужного количества элементов
            filenames = filenames[0:max_count_files]
            break
    return filenames


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
        except SyntaxError as e:
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


def get_verbs_from_function_name(function_name):
    ''' Получить глаголы из названия функции '''
    return [word for word in function_name.split('_') if is_verb(word)]


def split_snake_case_name_to_words(name):
    ''' Разбить имя на слова '''
    if not name:
        return []
    return [n for n in name.split('_') if n]


def get_all_words_in_path(path):
    ''' Получить все слова используемые в текстовых файлах каталога path
    '''
    trees = [t for t in get_trees(path) if t]
    # Получаем список всех имён в дереве ast
    names = flat([get_all_names_in_tree(t) for t in trees])
    # Исключаем магические функции
    names = [
        f for f in names if not (f.startswith('__') and f.endswith('__'))
    ]
    return flat([split_snake_case_name_to_words(name) for name in names])


def get_functions_names_in_tree(tree):
    ''' Получить список функций в дереве ast '''
    if not tree:
        return []
    return [node.name.lower()
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef)]


def get_top_verbs_in_path(path, top_size=10):
    ''' Получить ТОП используемых глаголов в каталоге path '''
    # Формируем список ast деревьев
    trees = [t for t in get_trees(path) if t]

    # Формируем список всех функций
    functions_names = flat(
        [get_functions_names_in_tree(t) for t in trees]
    )

    # Удаляем магический функции
    functions_names = [
        name for name in functions_names
        if not (name.startswith('__') and name.endswith('__'))
    ]

    # Формируем список глаголов, содержащихся в названиях функций
    verbs = flat([
        get_verbs_from_function_name(function_name)
        for function_name in functions_names
    ])
    return collections.Counter(verbs).most_common(top_size)


def get_top_functions_names_in_path(path, top_size=10):
    ''' Получить ТОП используемых имён функций в каталоге path'''
    # Получаем список ast деревьев
    trees = get_trees(path)
    # Формируем список имён в ast деревьях
    names = [
        f for f in flat(
            [get_functions_names_in_tree(t) for t in trees if t]
        ) if not (f.startswith('__') and f.endswith('__'))
    ]
    return collections.Counter(names).most_common(top_size)
