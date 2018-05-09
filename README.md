# code_parse

Библиотека позволяет оценить на сколько часто используются в проектах те или иные лексические конструкции.

Умеет работать с глаголами и существительными, разбирать как названия функции так и названия переменных.

## Установка
Установка из git:
```
git clone https://github.com/ds-vologdin/dcInt.git
```

## Как использовать
Пример использования библиотеки представлен в words_code_statistic.py

```
from code_parse import get_top_words_in_path


words_top = get_top_words_in_path(
    path='/home/developer/code/', top_size=50, word_type='verb',
    parse_code_type='function'
)
```
top_size - максимальное количество выводимых в отчёт слов
word_type - часть речи, которая нас интересует.
Возможные значения: verb, noun, any.
parse_code_type - говорит нам, что анализировать.
Возможные значения function (анализируем названия функции) и variable (анализируем названия переменных).



## words_code_statistic.py
Поставляется в составе библиотеки code_parse.
Приложение для формирования статистики по частоте употребления в коде различных слов.  Умеет работать с git-репозиториями и локальными проектами.  Выводит результат выполнения на консоль, csv-файл, json-файл.

### Пример использования words_code_statistic.py
```
python3 words_code_statistic.py --git-url https://github.com/django/django.git
--word-type noun --parse-code-type variable --output json
```
JSON-отчет будет записан в words_code_stat.json

Информацию о возможных аргументах можно посмотреть в хелпе.

```
python3 words_code_statistic.py -h
usage: words_code_statistic.py [-h] [--path PATH] [--git-url GIT_URL]
                               [--top-size TOP_SIZE]
                               [--word-type {verb,noun,any}]
                               [--parse-code-type {function,variable}]
                               [--output {stdout,json,csv}]

Приложение для проведения лексического анализа программного кода

optional arguments:
  -h, --help            show this help message and exit
  --path PATH           Пути к каталогам, где требуется провести анализ кода.
                        Можно указать несколько катологов в кавычках:
                        '/home/bill/coding/ /home/alisa/coding/'
  --git-url GIT_URL     URL git-репозитория с кодом, который требуется
                        проанализировать
  --top-size TOP_SIZE   Ограничивает вывод количества слов
  --word-type {verb,noun,any}
                        Параметр позволяет задать какая часть речи нас
                        интересует для формирования статистики. Возможные
                        значения: verb (по-умолчанию), noun и any.
  --parse-code-type {function,variable}
                        Параметр позволяет задать, что мы будем анализировать:
                        имена функций или имена переменных. Возможные
                        значения: function (по-умолчанию), variable.
  --output {stdout,json,csv}
                        Формат вывода. Возможные значения: stdout (по-
                        умолчанию) - печать на консоль; json - печать в json-
                        файл; csv - печать в csv-файл.
```
