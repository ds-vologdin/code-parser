#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import collections
from dclnt import (
    get_top_verbs_in_path,
    get_top_functions_names_in_path,
    get_all_words_in_path,
    get_filenames_in_path,
)
from gitrepo import GitRepo


def parse_argv_with_argparse():
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


def main(args):
    # Парсим argv
    args = parse_argv_with_argparse()

    top_size = args.top_size
    path = args.path
    git_url = args.git_url

    # Формируем список путей до анализируемых проектов
    projects = []
    if path:
        projects = path.split()
    # path_repo = clone_git_url(git_url)
    if git_url:
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
    # TODO: надо подумать, возможно лучше вынести удаление "временного
    # каталога" в деструктор класса
    if git_url:
        git_repo.remove_local_git_repo()

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))
