import csv
import json


def output_statistic(statistic, output_type='stdout'):
    if output_type == 'stdout':
        output_to_stdout(statistic)
    elif output_type == 'json':
        output_to_json(statistic)
    elif output_type == 'csv':
        output_to_csv(statistic)
    elif output_type == 'ods':
        output_to_ods(statistic)
    elif output_type == 'pdf':
        output_to_pdf(statistic)


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


def output_to_json(statistic):
    statistics_json = json.dumps(statistic, sort_keys=True, indent=4)
    with open('words_code_stat.json', 'w') as json_file:
        json_file.write(statistics_json)


def output_to_csv(statistic):
    with open('words_code_stat.csv', 'w') as csv_file:
        statistic_writer = csv.writer(csv_file)
        statistic_writer.writerow([statistic['word_type'], 'occurence'])
        for word, occurence in statistic['words_top']:
            statistic_writer.writerow([word, occurence])


def output_to_stdout(statistic):
    # Выводим на экран результаты
    # print('total {0} files'.format(statistic['file_count']))
    print('statistic type: {0}'.format(statistic['parse_code_type']))
    print_statistics_words_top(statistic['words_top'],
                               words_type=statistic['word_type'])


def output_to_ods(statistic):
    ''' заглушка '''
    pass


def output_to_pdf(statistic):
    ''' заглушка '''
    pass
