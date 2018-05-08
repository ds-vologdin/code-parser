# dcInt

Библиотека позволяет оценить на сколько часто используются в проектах те или иные лексические конструкции.

## Установка
```
git clone https://github.com/ds-vologdin/dcInt.git
```

## Как использовать
Пример использования
```
python3 words_code_statistic.py --git-url https://github.com/django/django.git --word-type noun --parse-code-type variable --output json
```
JSON-отчет будет записан в words_code_stat.json

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
