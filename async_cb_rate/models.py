from dataclasses import dataclass
from datetime import datetime


@dataclass
class Currency:
    name: str
    code: str
    price: float
    date: datetime
