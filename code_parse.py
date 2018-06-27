import collections
from nltk import pos_tag

from ast_tree import get_trees, get_all_names_in_tree, get_names_in_ast_tree


def flatten_list(not_flat_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return [item for sublist in not_flat_list for item in sublist]


def is_verb(word):
    ''' Проверка на глагол '''
    if not word:
        return False
    pos_info = pos_tag([word])
    # VB	verb, base form	take
    # VBD	verb, past tense	took
    # VBG	verb, gerund/present participle	taking
    # VBN	verb, past participle	taken
    # VBP	verb, sing. present, non-3d	take
    # VBZ	verb, 3rd person sing. present	takes
    return pos_info[0][1] in ('VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ')


def is_noun(word):
    ''' Проверка является ли word существительным '''
    if not word:
        return False
    pos_info = pos_tag([word])
    return pos_info[0][1] == 'NN'


def get_words_from_name(name, word_type='verb'):
    words = []
    if word_type == 'verb':
        words = [word for word in name.split('_') if is_verb(word)]
    elif word_type == 'noun':
        words = [word for word in name.split('_') if is_noun(word)]
    elif word_type == 'any':
        words = [word for word in name.split('_')]
    return words


def split_snake_case_name_to_words(name):
    ''' Разбить имя на слова '''
    if not name:
        return []
    return [n for n in name.split('_') if n]


def get_all_words_in_path(path):
    ''' Получить все слова используемые в текстовых файлах каталога path '''
    trees = [t for t in get_trees(path) if t]
    names = flatten_list([get_all_names_in_tree(t) for t in trees])
    # Исключаем магические функции
    names = [
        f for f in names if not (f.startswith('__') and f.endswith('__'))
    ]
    return flatten_list(
        [split_snake_case_name_to_words(name) for name in names]
    )


def get_functions_names_in_tree(tree):
    ''' Получить список функций в дереве ast '''
    return get_names_in_ast_tree(tree, type_name='function')


def get_top_verbs_in_path(path, top_size=10):
    ''' Получить ТОП используемых глаголов в каталоге path '''
    return get_top_words_in_path(path, top_size, word_type='verb')


def get_top_words_in_path_python(path, top_size=10, word_type='verb',
                                 parse_code_type='function'):
    trees = [t for t in get_trees(path) if t]
    names_in_code = flatten_list(
        [get_names_in_ast_tree(t, type_name=parse_code_type) for t in trees]
    )
    # Удаляем магию
    names_in_code = [
        name for name in names_in_code
        if not (name.startswith('__') and name.endswith('__'))
    ]
    words = flatten_list([
        get_words_from_name(name, word_type=word_type)
        for name in names_in_code
    ])
    return collections.Counter(words).most_common(top_size)


def get_top_words_in_path(path, top_size=10, word_type='verb',
                          parse_code_type='function', language='python'):
    ''' Получить ТОП используемых глаголов в каталоге path
    parse_code_type - function или variable '''
    if language == 'python':
        return get_top_words_in_path_python(path, top_size, word_type,
                                            parse_code_type)


def get_top_functions_names_in_path_python(path, top_size=10):
    ''' Получить ТОП используемых имён функций в каталоге path'''
    trees = get_trees(path)
    names = [
        f for f in flatten_list(
            [get_functions_names_in_tree(t) for t in trees if t]
        ) if not (f.startswith('__') and f.endswith('__'))
    ]
    return collections.Counter(names).most_common(top_size)


def get_top_functions_names_in_path(path, top_size=10, language='python'):
    ''' Получить ТОП используемых имён функций в каталоге path'''
    if language == 'python':
        return get_top_functions_names_in_path_python(path, top_size=10)


def get_statistic(path, top_size=10, word_type='verb',
                  parse_code_type='function-frequency-word',
                  language='python'):
    if parse_code_type == 'function-frequency-word':
        return get_top_words_in_path(
            path=path, top_size=top_size, word_type=word_type,
            parse_code_type='function', language=language
        )
    elif parse_code_type == 'variable-frequency-word':
        return get_top_words_in_path(
            path=path, top_size=top_size, word_type=word_type,
            parse_code_type='variable', language=language
        )
    elif parse_code_type == 'function-frequency':
        return get_top_functions_names_in_path(path, top_size, language)
