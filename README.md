# async-cb-rate
Асинхронная библиотека для парсинга курса валют с сайта ЦБ РФ.

### Библиотеку можно использовать для:
- мониторинга за курсом валют
- построения графиков изменения курса

### Установка c pip
```shell
pip install async-cb-rate
```

### Краткий обзор функциональности
- Библиотека позволяет получить курс валюты на любой день. По умолчанию курс ищется на сегодняшний день.
- Функции возвращают объекты `Currency`, с которыми удобно далее работать.
```python
import asyncio

from async_cb_rate.parser import get_rate, get_codes, get_all_rates


async def main():
    usd_rate = await get_rate("USD")
    print(f"USD rate for today={usd_rate.price}₽")  # USD rate for today=55.2987₽

    euro_rate = await get_rate("EUR")  # EUR rate for today=52.7379₽
    print(f"EUR rate for today={euro_rate.price}₽")

    codes = await get_codes()
    print(f"Available codes: {codes}") # ['AUD', 'AZN', 'GBP', 'AMD', 'BYN', 'BGN', 'BRL', 'HUF', 'HKD', 'DKK', 'USD', 
    # 'EUR', 'INR', 'KZT', 'CAD', 'KGS', 'CNY', 'MDL', 'NOK', 'PLN', 'RON', 'XDR', 'SGD', 'TJS', 'TRY', 'TMT', 'UZS', 
    # 'UAH', 'CZK', 'SEK', 'CHF', 'ZAR', 'KRW', 'JPY']

    all_rates = await get_all_rates()
    print(f"All rates for today: {all_rates}")  # [Currency(name='Австралийский доллар', code='AUD', price=35.9552, 
    # date=datetime.datetime(2022, 10, 3, 23, 45, 29, 145779)), ...]


asyncio.run(main())
```

### Доступные асинхронные функции библиотеки:
- **get_codes(date)** - получить все доступные коды валют на определённую дату:  
`codes = await get_codes()  # Коды валют`
- **get_rate(code, date)** - получить курс определённой валюты по её коду на определённую дату:  
`usd_rate = await get_rate("USD")  # Курс доллара на сегодня`
- **get_all_rates(date)** - получить курс всех доступных валют от ЦБ на определённую дату:  
`all_rates = await get_all_rates()  # Все курсы валют на сегодня`  
! По умолчанию поле date - это сегодня.

### Ошибки, которые можно получить при работе с библиотекой:
- `NoValidDateError` - функция была вызвана с датой, которая ещё не наступила.
- `CurrencyRateNotFoundError` - курс для данного кода валюты не найден.
