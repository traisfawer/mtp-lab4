"""Unit-тесты заданий повышенной сложности № 4 и 10."""

import functools
import operator
import os
import tempfile
import types
import unittest
from datetime import date

from file_filter import (filter_min_level, filter_module, filter_period, grep,
                         load_records, parse_line, read_lines)
from my_reduce import accumulate, compose, my_reduce, my_reduce_recursive

SAMPLE_LOG = """# комментарий
2026-10-01 08:00:01 INFO server: сервер запущен

2026-10-01 09:30:00 ERROR db: потеряно соединение
битая строка
2026-10-02 11:45:12 WARNING api: медленный запрос /orders
2026-10-03 14:00:00 CRITICAL db: нет места на диске
2026-13-40 10:00:00 INFO db: неверная дата
"""


class TestFileFilter(unittest.TestCase):
    """Проверка фильтрации журнала цепочкой генераторов."""

    def setUp(self):
        """Создать временный файл журнала."""
        handle, self.path = tempfile.mkstemp(suffix=".log")
        with os.fdopen(handle, "w", encoding="utf-8") as file:
            file.write(SAMPLE_LOG)

    def tearDown(self):
        """Удалить временный файл."""
        os.remove(self.path)

    def test_read_lines_skips_empty_and_comments(self):
        """Пустые строки и комментарии пропускаются."""
        lines = list(read_lines(self.path))
        self.assertEqual(len(lines), 6)
        self.assertTrue(lines[0].startswith("2026-10-01"))

    def test_generators(self):
        """Функции чтения и фильтрации возвращают генераторы."""
        self.assertIsInstance(read_lines(self.path), types.GeneratorType)
        records = load_records(self.path)
        self.assertIsInstance(records, types.GeneratorType)
        self.assertIsInstance(filter_min_level(records, "INFO"),
                              types.GeneratorType)

    def test_parse_line(self):
        """Корректная строка разбирается на поля."""
        record = parse_line("2026-10-01 09:30:00 ERROR db: нет связи")
        self.assertEqual(record.day, date(2026, 10, 1))
        self.assertEqual(record.level, "ERROR")
        self.assertEqual(record.module, "db")
        self.assertEqual(record.message, "нет связи")

    def test_bad_lines_dropped(self):
        """Повреждённые строки и неверные даты отбрасываются."""
        self.assertIsNone(parse_line("битая строка"))
        self.assertIsNone(parse_line("2026-13-40 10:00:00 INFO db: x"))
        self.assertEqual(len(list(load_records(self.path))), 4)

    def test_filter_min_level(self):
        """Остаются записи уровня ERROR и выше."""
        levels = [r.level for r in
                  filter_min_level(load_records(self.path), "ERROR")]
        self.assertEqual(levels, ["ERROR", "CRITICAL"])

    def test_filter_period(self):
        """Фильтрация по периоду включает границы."""
        records = filter_period(load_records(self.path),
                                date(2026, 10, 2), date(2026, 10, 3))
        self.assertEqual([r.day.day for r in records], [2, 3])
        records = filter_period(load_records(self.path),
                                end=date(2026, 10, 1))
        self.assertEqual(len(list(records)), 2)

    def test_chain(self):
        """Фильтры объединяются в цепочку."""
        records = filter_module(load_records(self.path), "db")
        records = filter_min_level(records, "CRITICAL")
        self.assertEqual([r.message for r in records],
                         ["нет места на диске"])

    def test_grep(self):
        """Поиск по тексту не зависит от регистра."""
        records = list(grep(load_records(self.path), "ORDERS"))
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].module, "api")

    def test_default_log(self):
        """Файл журнала из каталога data читается и разбирается."""
        self.assertGreater(len(list(load_records())), 0)


class TestMyReduce(unittest.TestCase):
    """Проверка собственной реализации reduce."""

    cases = [
        (operator.add, [1, 2, 3, 4]),
        (operator.mul, [1, 2, 3, 4, 5]),
        (lambda a, b: a if a > b else b, [3, 9, 2, 7]),
        (lambda s, w: s + w, ["a", "b", "c"]),
    ]

    def test_matches_functools(self):
        """Результат совпадает с functools.reduce."""
        for function, data in self.cases:
            with self.subTest(data=data):
                self.assertEqual(my_reduce(function, data),
                                 functools.reduce(function, data))
                self.assertEqual(my_reduce(function, data, data[0]),
                                 functools.reduce(function, data, data[0]))

    def test_initial(self):
        """Начальное значение используется первым."""
        self.assertEqual(my_reduce(operator.sub, [1, 2], 10), 7)
        self.assertEqual(my_reduce(operator.add, [], 5), 5)

    def test_single_element(self):
        """Для одного элемента функция не вызывается."""
        self.assertEqual(my_reduce(None, [42]), 42)

    def test_empty_without_initial(self):
        """Пустая последовательность без initial — TypeError."""
        with self.assertRaises(TypeError):
            my_reduce(operator.add, [])
        with self.assertRaises(TypeError):
            my_reduce_recursive(operator.add, [])

    def test_iterator_and_generator(self):
        """Работает с итераторами и генераторами."""
        self.assertEqual(my_reduce(operator.add, (x for x in range(5))), 10)
        self.assertEqual(my_reduce(operator.mul, range(1, 6), 1), 120)

    def test_order_of_application(self):
        """Свёртка выполняется слева направо."""
        result = my_reduce(lambda acc, x: f"({acc}{x})", "abc", "")
        self.assertEqual(result, "(((a)b)c)")

    def test_recursive(self):
        """Рекурсивная версия совпадает с итеративной."""
        for function, data in self.cases:
            with self.subTest(data=data):
                self.assertEqual(my_reduce_recursive(function, data),
                                 my_reduce(function, data))

    def test_accumulate(self):
        """Функция accumulate выдаёт промежуточные результаты."""
        self.assertEqual(list(accumulate(operator.add, [1, 2, 3])),
                         [1, 3, 6])
        self.assertEqual(list(accumulate(operator.add, [1, 2], 10)),
                         [10, 11, 13])
        self.assertEqual(list(accumulate(operator.add, [])), [])

    def test_compose(self):
        """Композиция применяет функции справа налево."""
        func = compose(lambda x: x * 2, lambda x: x + 1)
        self.assertEqual(func(5), 12)
        self.assertEqual(compose()(7), 7)
