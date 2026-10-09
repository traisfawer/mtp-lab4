"""Unit-тесты заданий средней сложности № 6, 8 и 2."""

import io
import types
import unittest
from contextlib import redirect_stdout
from itertools import islice

from filter_even import (even_numbers, filter_even, filter_even_comprehension,
                         filter_even_named, parse_numbers)
from primes import first_primes, is_prime, primes, primes_up_to
from timer_decorator import timer


class TestPrimes(unittest.TestCase):
    """Проверка генератора простых чисел."""

    def test_is_generator(self):
        """primes() возвращает генератор."""
        self.assertIsInstance(primes(), types.GeneratorType)

    def test_first_values(self):
        """Первые значения генератора — 2, 3, 5, 7, 11."""
        self.assertEqual(list(islice(primes(), 5)), [2, 3, 5, 7, 11])

    def test_primes_up_to(self):
        """Простые числа до 30 включительно."""
        self.assertEqual(list(primes_up_to(30)),
                         [2, 3, 5, 7, 11, 13, 17, 19, 23, 29])

    def test_primes_up_to_small(self):
        """До 1 простых чисел нет, граница включается."""
        self.assertEqual(list(primes_up_to(1)), [])
        self.assertEqual(list(primes_up_to(2)), [2])

    def test_hundredth_prime(self):
        """Сотое простое число — 541."""
        self.assertEqual(first_primes(100)[-1], 541)

    def test_agrees_with_is_prime(self):
        """Генератор и проверка is_prime дают одинаковый результат."""
        expected = [n for n in range(1000) if is_prime(n)]
        self.assertEqual(list(primes_up_to(999)), expected)

    def test_negative_count(self):
        """Отрицательное количество вызывает ValueError."""
        with self.assertRaises(ValueError):
            first_primes(-1)


class TestTimer(unittest.TestCase):
    """Проверка декоратора замера времени."""

    def setUp(self):
        """Создать декорированную функцию перед каждым тестом."""
        @timer
        def add(a, b=0):
            """Сложить два числа."""
            return a + b

        self.add = add

    def call_silently(self, func, *args, **kwargs):
        """Вызвать функцию, перехватив её вывод."""
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            result = func(*args, **kwargs)
        return result, buffer.getvalue()

    def test_result_unchanged(self):
        """Декоратор не меняет результат функции."""
        result, _ = self.call_silently(self.add, 2, b=3)
        self.assertEqual(result, 5)

    def test_prints_time(self):
        """Декоратор выводит имя функции и время."""
        _, output = self.call_silently(self.add, 1)
        self.assertIn("add", output)
        self.assertIn(" с", output)

    def test_metadata_preserved(self):
        """Имя и документация сохраняются через functools.wraps."""
        self.assertEqual(self.add.__name__, "add")
        self.assertEqual(self.add.__doc__, "Сложить два числа.")

    def test_statistics(self):
        """Обёртка хранит число вызовов и время последнего вызова."""
        self.assertIsNone(self.add.last_elapsed)
        self.call_silently(self.add, 1)
        self.call_silently(self.add, 2)
        self.assertEqual(self.add.calls, 2)
        self.assertGreaterEqual(self.add.last_elapsed, 0)
        self.assertGreaterEqual(self.add.total_elapsed,
                                self.add.last_elapsed)

    def test_time_measured_on_exception(self):
        """Время замеряется, даже если функция бросила исключение."""
        @timer
        def fail():
            """Всегда завершаться ошибкой."""
            raise RuntimeError("ошибка")

        with self.assertRaises(RuntimeError):
            self.call_silently(fail)
        self.assertEqual(fail.calls, 1)
        self.assertIsNotNone(fail.last_elapsed)


class TestFilterEven(unittest.TestCase):
    """Проверка фильтрации чётных чисел."""

    numbers = [1, 2, 3, 4, 5, 6, -4, 0, 15]
    expected = [2, 4, 6, -4, 0]

    def test_filter_lambda(self):
        """Функция filter с lambda оставляет только чётные числа."""
        self.assertEqual(filter_even(self.numbers), self.expected)

    def test_all_ways_agree(self):
        """Все способы фильтрации дают одинаковый результат."""
        self.assertEqual(filter_even_named(self.numbers), self.expected)
        self.assertEqual(filter_even_comprehension(self.numbers),
                         self.expected)
        self.assertEqual(list(even_numbers(self.numbers)), self.expected)

    def test_empty_and_odd(self):
        """Для пустого списка и списка нечётных — пустой результат."""
        self.assertEqual(filter_even([]), [])
        self.assertEqual(filter_even([1, 3, 5]), [])

    def test_generator_is_lazy(self):
        """Функция even_numbers возвращает генератор."""
        self.assertIsInstance(even_numbers([2]), types.GeneratorType)

    def test_parse_numbers(self):
        """Строка с числами преобразуется в список целых."""
        self.assertEqual(parse_numbers(" 1 -2  3 "), [1, -2, 3])
        with self.assertRaises(ValueError):
            parse_numbers("1 два 3")
