"""Задание повышенной сложности № 10: собственная функция reduce.

my_reduce повторяет поведение functools.reduce: сворачивает
последовательность в одно значение, последовательно применяя функцию
двух аргументов к накопленному результату и очередному элементу.
Дополнительно реализованы рекурсивная версия и функция accumulate,
возвращающая генератор промежуточных результатов.
"""

import functools
import operator

_MISSING = object()


def my_reduce(function, iterable, initial=_MISSING):
    """Свернуть iterable функцией function двух аргументов.

    my_reduce(f, [a, b, c], init) == f(f(f(init, a), b), c).
    Если initial не задан, начальным значением становится первый
    элемент. Для пустой последовательности без initial возбуждается
    TypeError, как и в functools.reduce.
    """
    iterator = iter(iterable)
    if initial is _MISSING:
        try:
            accumulator = next(iterator)
        except StopIteration:
            raise TypeError(
                "my_reduce() of empty iterable with no initial value"
            ) from None
    else:
        accumulator = initial
    for element in iterator:
        accumulator = function(accumulator, element)
    return accumulator


def my_reduce_recursive(function, sequence, initial=_MISSING):
    """Рекурсивная версия my_reduce для последовательностей (list, tuple)."""
    if initial is _MISSING:
        if not sequence:
            raise TypeError("my_reduce_recursive() of empty sequence "
                            "with no initial value")
        return my_reduce_recursive(function, sequence[1:], sequence[0])
    if not sequence:
        return initial
    return my_reduce_recursive(function, sequence[1:],
                               function(initial, sequence[0]))


def accumulate(function, iterable, initial=_MISSING):
    """Лениво выдавать все промежуточные результаты свёртки."""
    iterator = iter(iterable)
    if initial is _MISSING:
        try:
            accumulator = next(iterator)
        except StopIteration:
            return
    else:
        accumulator = initial
    yield accumulator
    for element in iterator:
        accumulator = function(accumulator, element)
        yield accumulator


def compose(*functions):
    """Собрать композицию функций с помощью my_reduce: f(g(h(x)))."""
    return my_reduce(lambda f, g: lambda x: f(g(x)), functions,
                     lambda x: x)


def main():
    """Продемонстрировать работу собственной реализации reduce."""
    numbers = [3, 1, 4, 1, 5, 9, 2, 6]
    print("Список:", numbers)
    print("Сумма:", my_reduce(operator.add, numbers))
    print("Произведение:", my_reduce(lambda x, y: x * y, numbers))
    print("Максимум:", my_reduce(lambda x, y: x if x > y else y, numbers))
    print("Факториал 10:", my_reduce(operator.mul, range(1, 11), 1))
    print("Склейка строк:", my_reduce(lambda s, w: s + "-" + w,
                                      ["map", "filter", "reduce"]))
    print("Сплющивание списков:",
          my_reduce(operator.add, [[1, 2], [3], [4, 5, 6]], []))
    print("Подсчёт слов:",
          my_reduce(lambda d, w: {**d, w: d.get(w, 0) + 1},
                    "a b a c b a".split(), {}))
    print("Рекурсивная версия, сумма:",
          my_reduce_recursive(operator.add, numbers))
    print("Промежуточные суммы:", list(accumulate(operator.add, numbers)))

    increment_then_double = compose(lambda x: x * 2, lambda x: x + 1)
    print("compose(x*2, x+1)(5) =", increment_then_double(5))

    same = my_reduce(operator.add, numbers) == functools.reduce(
        operator.add, numbers)
    print("Совпадает с functools.reduce:", same)

    try:
        my_reduce(operator.add, [])
    except TypeError as error:
        print("Пустой список без начального значения:", error)


if __name__ == "__main__":
    main()
