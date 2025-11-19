# modelos/loteria_base.py (Corrigido)

from __future__ import annotations 
from typing import List, Tuple
from abc import ABC, abstractmethod
from .sorteio import Sorteio

class LoteriaBase(ABC):
    def __init__(
        self, 
        nome: str, 
        label_complementar: str,
        qtd_principais: int,
        qtd_complementares: int,
        faixa_principais: Tuple[int, int],
        faixa_complementares: Tuple[int, int]
    ):
        self.nome = nome
        self.label_complementar = label_complementar
        self._sorteios: List[Sorteio] = []
        
        self.qtd_principais = qtd_principais
        self.qtd_complementares = qtd_complementares
        self.faixa_principais = faixa_principais
        self.faixa_complementares = faixa_complementares

    def adicionar(self, sorteio: Sorteio):
        # Chama o método que estávamos a corrigir
        if not self.validar_sorteio(sorteio):
            print(f"Aviso: Sorteio {sorteio.concurso} não é válido para {self.nome} e foi descartado.")
            return

        self._sorteios.append(sorteio)
        self._sorteios.sort(key=lambda x: x.data)

    @property
    def sorteios(self) -> List[Sorteio]:
        return self._sorteios

    @property
    def total_sorteios(self) -> int:
        return len(self._sorteios)

    @property
    def ultimos_5(self) -> List[Sorteio]:
        return self._sorteios[-5:] if self._sorteios else []
        
    @abstractmethod
    def validar_sorteio(self, sorteio: Sorteio) -> bool:
        """
        Implementação base da validação de regras de Qtd, Faixa e Duplicatas.
        """
        # CORREÇÃO CRÍTICA: Usar 'principais' e 'complementares'
        qtd_p = len(sorteio.principais)
        qtd_c = len(sorteio.complementares)
        
        # 1. Validação de Quantidade
        if qtd_p != self.qtd_principais or qtd_c != self.qtd_complementares:
            return False

        # 2. Validação de Faixa
        min_p, max_p = self.faixa_principais
        min_c, max_c = self.faixa_complementares

        # CORREÇÃO: Iterar sobre os atributos corretos
        if not all(min_p <= n <= max_p for n in sorteio.principais): return False
        if not all(min_c <= n <= max_c for n in sorteio.complementares): return False

        # 3. Validação de Duplicatas
        if len(set(sorteio.principais)) != qtd_p: return False
        if len(set(sorteio.complementares)) != qtd_c: return False

        return True