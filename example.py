#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getopt
import collections
from dclnt import (
    get_top_verbs_in_path,
    get_top_functions_names_in_path,
    get_all_words_in_path,
    get_filenames_in_path,
)
from gitrepo import GitRepo


def usage():
    print("usage: python3 {0} OPTIONS".format(sys.argv[0]))
    print("OPTIONS")
    helpText = '''--top-size=XXX По умолчанию top-size=20
--path=PATH - папки, в которых требуется провести лексический анализ.
Несколько папок можно указать в кавычках через запятую:
--path='~/coding/django, ~/coding/flask'
По умолчанию
path='./django, ./flask, ./pyramid, ./reddit, ./requests, ./sqlalchemy'
--git-url=git_url - url проекта на github (или в другом git репозитории)
--help
'''
    print(helpText)


def parse_argv():
    # Смотрим переданные параметры и инициируем переменные
    try:
        opts, args = getopt.getopt(
            sys.argv[1:], '', ['top-size=', 'path=', 'git-url=', 'help'])
    except getopt.GetoptError as err:
        print("parameter error: ", err)
        usage()
        return None

    options = {}
    for o, a in opts:
        if o == '--top-size':
            try:
                options['top-size'] = int(a)
            except:
                print('top_size must be a number')
                usage()
                return None
        elif o == '--path':
            options['path'] = a
        elif o == '--git-url':
            options['git_url'] = a
        elif o == '--help':
            usage()
            return 1
        else:
            print('unhandled option: {0}'.format(o))
            usage()
            return None
    return options


def main(args):
    # Парсим argv
    options = parse_argv()

    top_size = options.get('top-size', 20)
    path = options.get('path', '')
    git_url = options.get('git_url', '')

    # Формируем список путей до анализируемых проектов
    projects = []
    if path:
        projects = path.replace(' ', '').split(',')
    # path_repo = clone_git_url(git_url)
    git_repo = GitRepo(git_url)
    git_repo.clone_git_url()
    if git_repo.local_path:
        projects.append(git_repo.local_path)

    if not projects:
        print('no projects...no statistics...')
        return 0

    # Считаем статистику
    verbs = []
    functions_names = []
    words = []
    filenames = []

    for path_project in projects:
        verbs += get_top_verbs_in_path(path_project, top_size)
        functions_names += get_top_functions_names_in_path(
            path_project, top_size
        )
        words += get_all_words_in_path(path_project)
        filenames += get_filenames_in_path(path_project)

    # Выводим на экран результаты
    print('total {0} files'.format(len(filenames)))
    print('-'*80)

    print('total {0} verbs, {1} unique'.format(len(verbs), len(set(verbs))))
    for word, occurence in verbs:
        print(word, occurence)

    print('-'*80)
    print('total {0} functions names, {0} unique'.format(
          len(functions_names), len(set(functions_names))))
    for word, occurence in functions_names:
        print(word, occurence)

    print('-'*80)
    print('total {0} words, {1} unique'.format(len(words), len(set(words))))
    for word, occurence in collections.Counter(words).most_common(top_size):
        print(word, occurence)

    # Не надо забывать чистить за собой скаченные репозитории
    git_repo.remove_local_git_repo()

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))
