"""Задание повышенной сложности № 4: фильтрация данных из файла.

Файл журнала обрабатывается цепочкой генераторов: строки читаются
по одной, разбираются в записи и фильтруются по уровню, дате, модулю
и тексту. Ни на одном шаге файл не загружается в память целиком,
поэтому так можно обрабатывать журналы любого размера.
"""

import os
from collections import Counter, namedtuple
from datetime import date

LogRecord = namedtuple(
    "LogRecord", ["day", "time", "level", "module", "message"])

LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")

DEFAULT_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "data", "server.log")


def read_lines(path, encoding="utf-8"):
    """Лениво читать непустые строки файла, пропуская комментарии."""
    with open(path, encoding=encoding) as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):
                yield line


def parse_line(line):
    """Разобрать строку журнала в LogRecord или вернуть None."""
    parts = line.split(" ", 3)
    if len(parts) < 4 or parts[2] not in LEVELS:
        return None
    module, separator, message = parts[3].partition(": ")
    if not separator:
        return None
    try:
        day = date.fromisoformat(parts[0])
    except ValueError:
        return None
    return LogRecord(day, parts[1], parts[2], module, message)


def parse_records(lines):
    """Преобразовать строки в записи, отбрасывая повреждённые строки."""
    for line in lines:
        record = parse_line(line)
        if record is not None:
            yield record


def filter_min_level(records, min_level):
    """Оставить записи с уровнем не ниже min_level."""
    threshold = LEVELS.index(min_level)
    return (r for r in records if LEVELS.index(r.level) >= threshold)


def filter_period(records, start=None, end=None):
    """Оставить записи за период [start; end] (границы необязательны)."""
    for record in records:
        if start is not None and record.day < start:
            continue
        if end is not None and record.day > end:
            continue
        yield record


def filter_module(records, *modules):
    """Оставить записи указанных модулей."""
    return (r for r in records if r.module in modules)


def grep(records, text):
    """Оставить записи, в сообщении которых встречается text."""
    text = text.lower()
    return (r for r in records if text in r.message.lower())


def load_records(path=DEFAULT_LOG):
    """Создать генератор записей журнала из файла."""
    return parse_records(read_lines(path))


def format_record(record):
    """Отформатировать запись журнала для вывода."""
    return (f"{record.day} {record.time} {record.level:<8} "
            f"{record.module:<6} {record.message}")


def main():
    """Продемонстрировать фильтрацию журнала цепочкой генераторов."""
    print("Ошибки и критические события (ERROR и выше):")
    for record in filter_min_level(load_records(), "ERROR"):
        print("  ", format_record(record))

    print("\nПредупреждения и ошибки модуля db за 02.10–03.10:")
    records = load_records()
    records = filter_period(records, date(2026, 10, 2), date(2026, 10, 3))
    records = filter_module(records, "db")
    records = filter_min_level(records, "WARNING")
    for record in records:
        print("  ", format_record(record))

    print("\nЗаписи, где упоминаются заказы (orders):")
    for record in grep(load_records(), "orders"):
        print("  ", format_record(record))

    stats = Counter(r.level for r in load_records())
    print("\nКоличество записей по уровням:", dict(stats))
    total_lines = sum(1 for _ in read_lines(DEFAULT_LOG))
    parsed = sum(stats.values())
    print(f"Разобрано {parsed} из {total_lines} строк, "
          f"повреждённых строк: {total_lines - parsed}")


if __name__ == "__main__":
    main()
