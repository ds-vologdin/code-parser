import sys
import argparse

from code_parse import get_statistic
from repository import GitRepository
from output_statistic import output_statistic


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
        '--hg-url',
        help='''URL hg-репозитория с кодом, который требуется проанализировать \
(в разработке)'''
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
        choices=['function-frequency-word', 'variable-frequency-word',
                 'function-frequency'],
        default='function-frequency-word',
        help='''Параметр позволяет задать, что мы будем анализировать: \
частота употребления слов в именах функций (function-frequency-word), \
частота употребления слов в именах переменных (variable-frequency-word),\
частота употребления имён функций (function-frequency).
Возможные значения: function-frequency-word (по-умолчанию), \
variable-frequency-word, function-frequency.
'''
    )
    parser.add_argument(
        '--output',
        choices=['stdout', 'json', 'csv'],
        default='stdout',
        help='''Формат вывода.
Возможные значения:
stdout (по-умолчанию) - печать на консоль;
json - печать в json-файл;
csv - печать в csv-файл.
'''
    )
    parser.add_argument(
        '--language',
        choices=['python'],
        default='python',
        help='''Параметр позволяет задать язык, на котором написан проект.
Возможные значения: python (по-умолчанию).
'''
    )
    return parser.parse_args()


def get_projects_from_path(path=''):
    if not path:
        return []
    return path.split()


def get_projects_from_git(git_repo=None):
    if not git_repo:
        return []
    if not git_repo.is_cloned:
        git_repo.clone_url()
    if git_repo.local_path:
        return git_repo.local_path
    return []


def get_projects_from_hg(hg_repo=None):
    ''' заглушка '''
    return []


def get_projects(local_path=None, git_repo=None, hg_repo=None):
    projects = get_projects_from_path(local_path)
    git_project = get_projects_from_git(git_repo)
    if git_project:
        projects.append(git_project)
    hg_project = get_projects_from_hg(hg_repo)
    if hg_project:
        projects.append(hg_project)
    return projects


def main(args):
    # Парсим argv
    args = parse_argv()

    git_repository = GitRepository(args.git_url)

    # Формируем список путей до анализируемых проектов
    projects = get_projects(local_path=args.path, git_repo=git_repository)
    if not projects:
        print('no projects...no statistics...')
        return 0

    # Считаем статистику
    words_top = []

    for path_project in projects:
        words_top.extend(get_statistic(
            path_project, args.top_size, word_type=args.word_type,
            parse_code_type=args.parse_code_type, language=args.language
        ))

    statistic = {
        'word_type': args.word_type,
        'top_size': args.top_size,
        'parse_code_type': args.parse_code_type,
        'language': args.language,
        'words_top': words_top,
        'projects': projects,
    }
    output_statistic(statistic, output_type=args.output)

    # Не надо забывать чистить за собой скачанные репозитории
    git_repository.remove_local_repository()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
