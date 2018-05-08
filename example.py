#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from dclnt import (
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
        '--git-url',
        help='URL git-репозитория с кодом, который требуется проанализировать'
    )
    parser.add_argument(
        '--top-size', type=int, default=20,
        help='Ограничивает вывод количества слов'
    )
    parser.add_argument(
        '--word-type', choices=['verb', 'noun', 'any'],  default='verb',
        help='''Параметр позволяет задать какая часть речи нас интересует для \
формирования статистики. Возможные значения: verb (по-умолчанию), noun и any.
'''
    )
    parser.add_argument(
        '--parse-code-type',
        choices=['function', 'variable'],
        default='function',
        help='''Параметр позволяет задать, что мы будем анализировать: \
имена функций или имена переменных.
Возможные значения: function (по-умолчанию), variable.
'''
    )
    return parser.parse_args()


def get_projects_in_path(path=''):
    if not path:
        return []
    return path.split()


def get_projects(local_path=None, git_repo=None):
    projects = get_projects_in_path(local_path)
    if not git_repo.is_cloned:
        git_repo.clone_git_url()
    if git_repo.local_path:
        projects.append(git_repo.local_path)
    return projects


def print_statistics_words_top(words_top, words_type='words'):
    print('total {total} {words_type}'.format(
        total=len(words_top),
        words_type=words_type
    ))
    print('='*80)
    print('| {0:<60}|{1:^15} |'.format(words_type, 'occurence'))
    print('='*80)
    for word, occurence in words_top:
        print('| {0:<60}|{1:^15} |'.format(word, occurence))
    print('='*80)


def main(args):
    # Парсим argv
    args = parse_argv()

    git_repo = GitRepo(args.git_url)

    # Формируем список путей до анализируемых проектов
    projects = get_projects(local_path=args.path, git_repo=git_repo)
    if not projects:
        print('no projects...no statistics...')
        return 0

    # Считаем статистику
    words_top = []
    filenames = []

    for path_project in projects:
        words_top += get_top_words_in_path(
            path_project, args.top_size, word_type=args.word_type,
            parse_code_type=args.parse_code_type
        )
        filenames += get_filenames_in_path(path_project)

    # Выводим на экран результаты
    print('total {0} files'.format(len(filenames)))
    print('statistic type: {0}'.format(args.parse_code_type))
    print_statistics_words_top(words_top, words_type=args.word_type)

    # Не надо забывать чистить за собой скачанные репозитории
    git_repo.remove_local_git_repo()

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))
