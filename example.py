#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import collections
from dclnt import (
    get_top_functions_names_in_path,
    get_all_words_in_path,
    get_filenames_in_path,
    get_top_words_in_path,
)
from gitrepo import GitRepo


def parse_argv():
    description_programm = '''Приложение для проведения лексического анализа \
программного кода'''
    parser = argparse.ArgumentParser(description=description_programm)
    parser.add_argument(
        '--path',
        help='''Пути к каталогам, где требуется провести анализ кода.
Можно указать несколько катологов в кавычках:
    '/home/bill/coding/ /home/alisa/coding/' '''
    )
    parser.add_argument(
        "--git-url",
        help="URL git-репозитория с кодом, который требуется проанализировать"
    )
    parser.add_argument(
        "--top-size", type=int, default=20,
        help="Ограничивает вывод количества слов"
    )
    return parser.parse_args()


def get_projects_in_path(path=''):
    if not path:
        return []
    return path.split()


def main(args):
    # Парсим argv
    args = parse_argv()

    top_size = args.top_size
    path = args.path
    git_url = args.git_url

    # Формируем список путей до анализируемых проектов
    projects = get_projects_in_path(path)

    # path_repo = clone_git_url(git_url)
    if git_url:
        git_repo = GitRepo(git_url)
        path_git = git_repo.clone_git_url()
        if path_git:
            projects.append(path_git)

    if not projects:
        print('no projects...no statistics...')
        return 0

    # Считаем статистику
    verbs_top = []
    nouns_top = []
    words_top = []
    functions_names = []
    words = []
    filenames = []

    for path_project in projects:
        words_top += get_top_words_in_path(
            path_project, top_size, word_type='any'
        )
        verbs_top += get_top_words_in_path(
            path_project, top_size, word_type='verb'
        )
        nouns_top += get_top_words_in_path(
            path_project, top_size, word_type='noun'
        )
        functions_names += get_top_functions_names_in_path(
            path_project, top_size
        )
        words += get_all_words_in_path(path_project)
        filenames += get_filenames_in_path(path_project)

    # Выводим на экран результаты
    print('total {0} files'.format(len(filenames)))

    print('-'*80)
    print('total {0} words, {1} unique'.format(
        len(words_top), len(set(words_top))
    ))
    for word, occurence in words_top:
        print(word, occurence)

    print('-'*80)
    print('total {0} verbs, {1} unique'.format(
        len(verbs_top), len(set(verbs_top))
    ))
    for word, occurence in verbs_top:
        print(word, occurence)

    print('-'*80)
    print('total {0} nouns, {1} unique'.format(
        len(nouns_top), len(set(nouns_top))
    ))
    for word, occurence in nouns_top:
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

    # Не надо забывать чистить за собой скачанные репозитории
    if git_url:
        git_repo.remove_local_git_repo()

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))
