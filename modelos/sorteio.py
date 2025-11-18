# modelos/sorteio.py
from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass(frozen=True)
class Sorteio:
    data: datetime
    concurso: str
    principais: List[int]
    complementares: List[int]
    acumulou: bool
    jackpot: int
