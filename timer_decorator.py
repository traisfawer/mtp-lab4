"""Задание средней сложности № 8: декоратор замера времени работы функции.

Декоратор timer оборачивает функцию, измеряет время её выполнения
через time.perf_counter, выводит результат и сохраняет последнее
измерение в атрибуте обёртки last_elapsed.
"""

import time
from functools import wraps


def timer(func):
    """Измерять и выводить время выполнения декорируемой функции."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            wrapper.last_elapsed = elapsed
            wrapper.calls += 1
            wrapper.total_elapsed += elapsed
            print(f"[timer] {func.__name__} выполнена за {elapsed:.6f} с")

    wrapper.last_elapsed = None
    wrapper.calls = 0
    wrapper.total_elapsed = 0.0
    return wrapper


@timer
def sum_of_squares(n):
    """Посчитать сумму квадратов чисел от 1 до n через map."""
    return sum(map(lambda x: x * x, range(1, n + 1)))


@timer
def slow_add(a, b, delay=0.2):
    """Сложить два числа с искусственной задержкой."""
    time.sleep(delay)
    return a + b


@timer
def sort_numbers(numbers):
    """Вернуть отсортированную копию списка."""
    return sorted(numbers)


def main():
    """Продемонстрировать работу декоратора timer."""
    print("Сумма квадратов до 1 000 000:", sum_of_squares(1_000_000))
    print("slow_add(2, 3):", slow_add(2, 3))
    print("slow_add(10, 20, delay=0.5):", slow_add(10, 20, delay=0.5))
    print("Отсортировано:", sort_numbers([5, 3, 9, 1, 7])[:5])

    print("Имя функции сохранено через wraps:", slow_add.__name__)
    print("Документация сохранена:", slow_add.__doc__)
    print(f"slow_add вызвана {slow_add.calls} раза, суммарно "
          f"{slow_add.total_elapsed:.3f} с, последний вызов "
          f"{slow_add.last_elapsed:.3f} с")


if __name__ == "__main__":
    main()
