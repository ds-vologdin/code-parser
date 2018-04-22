import os
import collections
from dclnt import (get_top_verbs_in_path,
                   get_top_functions_names_in_path,
                   get_all_words_in_path)


def main():
    top_size = 500
    verbs = []
    functions_names = []
    words = []
    projects = [
        'django',
        'flask',
        'pyramid',
        'reddit',
        'requests',
        'sqlalchemy',
    ]

    for project in projects:
        path = os.path.join('.', project)
        verbs += get_top_verbs_in_path(path, top_size)
        functions_names += get_top_functions_names_in_path(path, top_size)
        words += get_all_words_in_path(path)

    print('total %s verbs, %s unique' % (len(verbs), len(set(verbs))))
    for word, occurence in verbs:
        print(word, occurence)

    print('-'*80)
    print('total %s functions names, %s unique' %
          (len(functions_names), len(set(functions_names))))
    for word, occurence in functions_names:
        print(word, occurence)

    print('-'*80)
    print('total %s words, %s unique' % (len(words), len(set(words))))
    for word, occurence in collections.Counter(words).most_common(top_size):
        print(word, occurence)

if __name__ == "__main__":
    main()
