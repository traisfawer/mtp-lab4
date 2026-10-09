# Лабораторная работа № 4. Функциональное программирование на Python

**Ефимов Денис Борисович, группа 220042-11, вариант 6, лабораторная №4**

Дисциплина «Методы и технологии программирования» (часть 1).

## Задания варианта 6

Средней сложности:
- № 6 — генератор простых чисел — `primes.py`;
- № 8 — декоратор замера времени работы функции — `timer_decorator.py`;
- № 2 — отфильтровать чётные числа из списка — `filter_even.py`.

Повышенной сложности:
- № 4 — фильтрация данных из файла через генератор — `file_filter.py`
  (журнал `data/server.log`);
- № 10 — собственная реализация reduce — `my_reduce.py`.

## Что используется

- функции высшего порядка и `lambda` — `filter`, `map`, `my_reduce`, `compose`;
- генераторы (`yield`) и генераторные выражения — `primes`, `read_lines`,
  `parse_records`, фильтры журнала, `accumulate`;
- декораторы с `functools.wraps` — `timer`;
- модули `functools`, `itertools`, `operator`.

## Запуск

```
pip install -r requirements.txt

python primes.py
python timer_decorator.py
python filter_even.py
python file_filter.py
python my_reduce.py
```

## Тесты

```
python -m pytest -v
```

или средствами стандартной библиотеки:

```
python -m unittest discover -s tests -t .
```

Проверка стиля: `python -m flake8 .`
