
from abc import ABC, abstractmethod
from typing import List
from .sorteio import Sorteio

class Loteria(ABC):
    def __init__(self, nome: str, numeros_principais_range: tuple, complementares_range: tuple):
        self.nome = nome
        self.numeros_principais_range = numeros_principais_range
        self.complementares_range = complementares_range
        self.sorteios: List[Sorteio] = []

    @abstractmethod
    def validar_sorteio(self, sorteio: Sorteio) -> bool:
        pass

    def adicionar_sorteio(self, sorteio: Sorteio) -> bool:
        self.sorteios.append(sorteio)  # Lê tudo
        return True

    def get_todos_numeros(self, tipo: str = 'principais') -> List[int]:
        numeros = []
        for sorteio in self.sorteios:
            if tipo == 'principais':
                numeros.extend(sorteio.numeros_sorteados)
            elif tipo == 'complementares':
                numeros.extend(sorteio.numeros_complementares)
        return numeros