"""Задание средней сложности № 2: отфильтровать чётные числа из списка.

Основной способ — встроенная функция filter с lambda-выражением.
Для сравнения показаны списковое включение и генераторное выражение.
"""


def is_even(number):
    """Проверить, что число чётное."""
    return number % 2 == 0


def filter_even(numbers):
    """Вернуть список чётных чисел с помощью filter и lambda."""
    return list(filter(lambda x: x % 2 == 0, numbers))


def filter_even_named(numbers):
    """Вернуть список чётных чисел, передав в filter именованную функцию."""
    return list(filter(is_even, numbers))


def filter_even_comprehension(numbers):
    """Вернуть список чётных чисел через списковое включение."""
    return [x for x in numbers if x % 2 == 0]


def even_numbers(numbers):
    """Лениво выдавать чётные числа (генераторное выражение)."""
    return (x for x in numbers if x % 2 == 0)


def parse_numbers(text):
    """Преобразовать строку с целыми числами через пробел в список."""
    return list(map(int, text.split()))


def main():
    """Продемонстрировать фильтрацию чётных чисел."""
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, -4, 0, 15, 22]
    print("Исходный список:", numbers)
    print("filter + lambda:", filter_even(numbers))
    print("filter + функция:", filter_even_named(numbers))
    print("Списковое включение:", filter_even_comprehension(numbers))
    print("Генераторное выражение:", list(even_numbers(numbers)))

    squares_of_even = list(map(lambda x: x ** 2, filter(is_even, numbers)))
    print("Квадраты чётных чисел (filter + map):", squares_of_even)

    try:
        raw = input("Введите целые числа через пробел: ")
    except EOFError:
        print()
        print("Ввод не получен, интерактивная часть пропущена")
        return
    try:
        user_numbers = parse_numbers(raw)
    except ValueError:
        print("Ошибка: нужно вводить только целые числа")
        return
    print("Чётные числа:", filter_even(user_numbers))


if __name__ == "__main__":
    main()
