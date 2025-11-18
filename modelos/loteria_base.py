# modelos/loteria_base.py
from typing import List
from .sorteio import Sorteio

class LoteriaBase:
    def __init__(self, nome: str, label_complementar: str):
        self.nome = nome
        self.label_complementar = label_complementar
        self.sorteios: List[Sorteio] = []

    def adicionar(self, sorteio: Sorteio):
        self.sorteios.append(sorteio)
        self.sorteios.sort(key=lambda x: x.data)

    @property
    def total_sorteios(self) -> int:
        return len(self.sorteios)

    @property
    def ultimos_5(self):
        return self.sorteios[-5:] if self.sorteios else []

    @property
    def acumulações(self) -> int:
        return sum(1 for s in self.sorteios if s.acumulou)

    @property
    def maior_jackpot(self) -> int:
        return max((s.jackpot for s in self.sorteios), default=0)