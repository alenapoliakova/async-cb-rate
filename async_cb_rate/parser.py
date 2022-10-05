import re
import aiohttp
import warnings

from typing import Generator

from bs4 import BeautifulSoup
from bs4.builder import XMLParsedAsHTMLWarning

from datetime import datetime

from async_cb_rate.models import Currency
from async_cb_rate.errors import NoValidDateError, CurrencyRateNotFoundError

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

compiled_letters_pattern = re.compile(r"[а-яА-я]+")
compiled_price_pattern = re.compile(r"\d+.\d+$")


async def _parse_cb(date: datetime) -> Generator[Currency, None, None]:
    if date > datetime.now():
        raise NoValidDateError("The date hasn't arrived yet")
    url = f"https://cbr.ru/scripts/XML_daily.asp?date_req={date.day:02}/{date.month:02}/{date.year}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.text()

    soup = BeautifulSoup(data, "lxml")

    for tag in soup.select("valute"):
        text = tag.text

        code = text[3:6]
        name = " ".join(compiled_letters_pattern.findall(text))
        price = float(compiled_price_pattern.findall(text)[0].replace(",", "."))

        yield Currency(name=name, code=code, price=price, date=date)


async def get_codes(date: datetime = datetime.now()) -> list[str]:
    """Парсинг кодов курса валют ЦБ. Возвращает список доступных для парсинга кодов в заданный день.
    Parameters:
        date (datetime):
            Дата, за которую нужно найти коды валют. По умолчанию - сегодняшний день.
    Returns:
        codes (list[str]):
            Список из доступных кодов для парсинга валют.
    """
    codes = []

    async for currency in _parse_cb(date):
        codes.append(currency.code)

    return codes


async def get_rate(code: str, date: datetime = datetime.now()) -> Currency:
    """Парсинг курса ЦБ, возвращает объект Currency, содержащий стоимость валюты в заданный день.
    Parameters:
        code (str):
            Код валюты. Получить все коды можно в get_codes().
        date (datetime):
            Дата курса.
    Returns:
        currency_object (Currency):
            Объект валюты (или вызовется ошибка `CurrencyRateNotFoundError`, если валюта не была найдена).
    """
    async for currency in _parse_cb(date):
        if currency.code == code:
            return currency

    raise CurrencyRateNotFoundError("Given currency code not found. Get all codes by calling get_codes()")


async def get_all_rates(date: datetime = datetime.now()) -> list[Currency]:
    """Парсинг курса ЦБ, возвращает список из объектов Currency на заданный день.
    Parameters:
        date (datetime):
            Дата курса.
    ReturnsL
        currencies (list[Currency]):
            Список из объектов валют.
    """
    currencies = []

    async for currency in _parse_cb(date):
        currencies.append(currency)

    return currencies
