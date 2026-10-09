"""Задание средней сложности № 6: генератор простых чисел.

Бесконечный генератор выдаёт простые числа по одному и хранит только
уже найденные простые числа, поэтому следующее значение вычисляется
лениво, в момент запроса.
"""

from itertools import islice, takewhile


def is_prime(number):
    """Проверить, является ли число простым."""
    if number < 2:
        return False
    if number < 4:
        return True
    if number % 2 == 0:
        return False
    divisor = 3
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 2
    return True


def primes():
    """Бесконечно выдавать простые числа: 2, 3, 5, 7, 11, ..."""
    found = []
    candidate = 2
    while True:
        if all(candidate % p for p in takewhile(
                lambda p: p * p <= candidate, found)):
            found.append(candidate)
            yield candidate
        candidate += 1 if candidate == 2 else 2


def primes_up_to(limit):
    """Выдать все простые числа, не превышающие limit."""
    return takewhile(lambda p: p <= limit, primes())


def first_primes(count):
    """Вернуть список из count первых простых чисел."""
    if count < 0:
        raise ValueError("Количество не может быть отрицательным")
    return list(islice(primes(), count))


def main():
    """Продемонстрировать работу генератора простых чисел."""
    generator = primes()
    print("Первые три значения через next():",
          next(generator), next(generator), next(generator))

    print("Первые 15 простых чисел:", first_primes(15))
    print("Простые числа до 50:", list(primes_up_to(50)))

    twins = [(p, p + 2) for p in primes_up_to(100) if is_prime(p + 2)]
    print("Простые числа-близнецы до 100:", twins)

    total = sum(p for p in primes_up_to(1000))
    print("Сумма простых чисел до 1000 (генераторное выражение):", total)

    try:
        raw = input("Введите N, чтобы получить простые числа "
                    "до N: ").strip()
    except EOFError:
        print()
        print("Ввод не получен, интерактивная часть пропущена")
        return
    if raw.isdigit():
        print(f"Простые числа до {raw}:", list(primes_up_to(int(raw))))
    else:
        print("Нужно ввести целое неотрицательное число")


if __name__ == "__main__":
    main()
