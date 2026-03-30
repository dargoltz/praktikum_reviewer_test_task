# Общие рекомендации по оформлению кода:
# - У классов и методов желательно добавить docstring
# - У полей, аргументов функций жеалтельно добавить явные типы
# - У всех функций желательно указывать тип возвращаемого значения (кроме специальных методов)
# Ваш код будет работать и без этого, но, следуя этим рекомендациям, вы сделаете код более читаемым и поддерживаемым.

# Общие ошибки:
# - Направильная работа с модулем datetime - для работы с датами модуль предоставляет отдельный тип date -
# datetime.datetime использовать в этом задании необязательно (этот тип предназначен для даты и временеми)


import datetime as dt
from dataclasses import dataclass, field


# class Record:
#     def __init__(self, amount, comment, date=''):
#         self.amount = amount
#         self.date = (
#             dt.datetime.now().date() if
#             not
#             date else dt.datetime.strptime(date, '%d.%m.%Y').date())
#         self.comment = comment

# 1. Для хранения данных лучше использовать @dataclasses.dataclass - это упростит описание класса и улучшит типизацию
# 2. В идеале для конвертации даты использовать datetime.fromisoformat, но этот метод ограничивает формат ввода -
# оставим вашу реализацию
# 3. Можно добавить значение по умолчанию для comment

# Исправленный вариант:
@dataclass
class Record:
    """Запись, хранимая калькулятором"""
    amount: float
    comment: str = ""
    date: dt.date | str = field(default_factory=dt.date.today) # разрешаем создание объекта с датой в str формате,
    # Далее мы переведем ее в формат datetime.date

    # Специальный метод дата-классов для пост-обработки объекта
    def __post_init__(self):
        # Если дата передана строкой - пробуем сконвертировать ее в dt.date
        # В случае ошибки - ставим сегодняшнюю дату
        if isinstance(self.date, str):
            try:
                self.date = dt.datetime.strptime(self.date, '%d.%m.%Y').date()
            except ValueError:
                self.date = dt.date.today()


# class Calculator:
#     def __init__(self, limit):
#         self.limit = limit
#         self.records = []
#
#     def add_record(self, record):
#         self.records.append(record)
#
#     def get_today_stats(self):
#         today_stats = 0
#         for Record in self.records:
#             if Record.date == dt.datetime.now().date():
#                 today_stats = today_stats + Record.amount
#         return today_stats
#
#     def get_week_stats(self):
#         week_stats = 0
#         today = dt.datetime.now().date()
#         for record in self.records:
#             if (
#                 (today - record.date).days < 7 and
#                 (today - record.date).days >= 0
#             ):
#                 week_stats += record.amount
#         return week_stats


# 1. Ошибка в методе get_today_stats:
# - for Record in self.records: Record ссылается на класс Record в принципе, а не на объект Record из массива records;
# - Реализацию можно упростить используя генератор списков
# 2. Условие в get_week_stats можно упростить, цикл for также заменить на генератор списков
# 3. Условие (today - record.date).days < 7 исключает день ровно неделю назад - ошибка
# 4. Рекомендация: по условию класс калькулятор не предназначен для прямого использования - можно запретить создание объектов Calculator,
# либо хотя бы указать это в описании класса.

# Исправленная вариант:
class Calculator:
    """Общий класс для калькуляторов, не предназначен для прямого использования"""

    def __init__(self, limit: float):
        self.limit: float = limit
        self.records: list[Record] = []

    def add_record(self, record: Record) -> None:
        """Добавить запись в хранилище калькулятора"""
        self.records.append(record)

    def get_today_stats(self) -> float:
        """Получить затраты из записей на сегодня"""
        # Для наглядности список сохраняется в переменную - для экономии памяти вы можете передать его прямо в sum
        today_records_amount = [r.amount for r in self.records if r.date == dt.date.today()]
        return sum(today_records_amount)

    def get_week_stats(self) -> float:
        """Получить затраты из записей за последнюю неделю"""
        today = dt.date.today()
        date_a_week_ago = today - dt.timedelta(days=6)

        # Для наглядности список сохраняется в переменную - для экономии памяти вы можете передать его прямо в sum
        # Условие date_a_week_ago <= r.date <= today выглядит более компактно и наглядно
        last_week_records_amount = [r.amount for r in self.records if date_a_week_ago <= r.date <= today]
        return sum(last_week_records_amount)


# class CaloriesCalculator(Calculator):
#     def get_calories_remained(self):  # Получает остаток калорий на сегодня
#         x = self.limit - self.get_today_stats()
#         if x > 0:
#             return f'Сегодня можно съесть что-нибудь' \
#                    f' ещё, но с общей калорийностью не более {x} кКал'
#         else:
#             return('Хватит есть!')

# 1. В случае когда лимит не превышен, нет необходимости вычислять x - преобразуем условие для проверки лимита.
# Также рекомендую называть переменные более определенно, чтобы они характеризовали то, что хранят
# 2. Комментарий к функции по сути описывает ее работу - можно оформить его в docstring
# 3. В выражении return ('Хватит есть!') лишние скобки - нет необходимости их указывать

# Исправленный вариант:
class CaloriesCalculator(Calculator):
    """Калькулятор калорий"""

    def get_calories_remained(self) -> str:
        """Возвращает остаток калорий на сегодня, если он не исчерпан/превышен"""
        today_stats = self.get_today_stats()

        if today_stats >= self.limit:
            return 'Хватит есть!'
        else:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {self.limit - today_stats} кКал'


# class CashCalculator(Calculator):
#     USD_RATE = float(60)  # Курс доллар США.
#     EURO_RATE = float(70)  # Курс Евро.
#
#     def get_today_cash_remained(self, currency,
#                                 USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
#         currency_type = currency
#         cash_remained = self.limit - self.get_today_stats()
#         if currency == 'usd':
#             cash_remained /= USD_RATE
#             currency_type = 'USD'
#         elif currency_type == 'eur':
#             cash_remained /= EURO_RATE
#             currency_type = 'Euro'
#         elif currency_type == 'rub':
#             cash_remained == 1.00
#             currency_type = 'руб'
#         if cash_remained > 0:
#             return (
#                 f'На сегодня осталось {round(cash_remained, 2)} '
#                 f'{currency_type}'
#             )
#         elif cash_remained == 0:
#             return 'Денег нет, держись'
#         elif cash_remained < 0:
#             return 'Денег нет, держись:' \
#                    ' твой долг - {0:.2f} {1}'.format(-cash_remained,
#                                                      currency_type)
#
#     def get_week_stats(self):
#         super().get_week_stats()


# 1. Конвертацию валют лучше вынести в отдельный, приватный метод
# 2. Нет необходимости переопределять get_week_stats, так как логика работы метода не меняется.
# Помимо этого в переопределении ошибка - переопределенная функция не возвращает результат выполнения
# 3. В метод get_today_cash_remained не нужно передавать USD_RATE и EURO_RATE -
# эти значения определены как константы внутри класса
# 4. Необходимо предусмотреть ситуацию, когда введен некорректный тип валюты.
# В хороших проектах используют прямые ограничения (например, перечисления из модуля enum).
# Для простоты добавим множество поддерживаемых типов валют и будем проверять по нему.
# 5. Нет необходимости выполнять currency_type = currency - currency_type гарантированно определится в каждом варианте проверки
# Помимо этого, можно сделать этап определения currency_type более явным, отделив его от остального кода 
# (например, выбирая его при помощи отдельного dict[currency, currency_type]

# Исправленная вариант:
class CashCalculator(Calculator):
    """Калькулятор бюджета"""

    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # Добавим множество поддерживаемых валют
    AVAILABLE_CURRENCIES = {"rub", "usd", "eur"}

    def get_today_cash_remained(self, currency: str) -> str:
        """
        Возвращает информацию о состоянии бюджета на сегодня в указанной валюте.
        Учитывает случаи когда лимит исчерпан или превышен
        """
        # Убедимся, что передан поддерживаемый тип валюты
        # Можно так же выбрасывать исключение, но мы просто завершим выполнение
        if currency not in self.AVAILABLE_CURRENCIES:
            return f"Валюта {currency} не поддерживается"

        today_stats = self.get_today_stats()

        # Сначала опишем случай когда лимит исчерпан, но не превышен, т.к. для него не нужно вычислять остаток/долг
        if today_stats == self.limit:
            return 'Денег нет, держись'

        # Переведем остаток в заданную валюту
        cash_remained = self._convert_cash(self.limit - today_stats, currency)

        # Переведем currency в корректный для вывода формат
        currency_type = {
            "rub": "руб.",
            "usd": "USD",
            "eur": "EUR",
        }[currency]

        # Используем cash_remained:.2f для того чтобы всегда иметь два знака после запятой
        # При использовании round(cash_remained, 2) в случае вроде round(10, 2) вернется 10, а не 10.00
        if cash_remained > 0:
            return f"На сегодня осталось {cash_remained:.2f} {currency_type}"
        else:
            return f"Денег нет, держись: твой долг - {-cash_remained:.2f} {currency_type}"

    # Этот метод не предназначен для прямого использования - обозначим это, сделав его приватным (добавив "_" перед его названием)
    def _convert_cash(self, amount: float, currency: str) -> float:
        """Переводит заданную сумму по курсу валют"""
        # Используем словарь-диспетчер - один из альтернативных вариантов конструкции if-elif-else
        # Такая реализация необязательна - вы можете использовать знакомые вам конструкции if-else, match-case
        converted_amount = {
            "rub": amount,
            "usd": amount / self.USD_RATE,
            "eur": amount / self.EURO_RATE,
        }[currency]

        # В этой реализации converted_amount также объявляется для наглядности - 
        # в целях экономии памяти можно сразу сделать return {...}[currency]
        return converted_amount
