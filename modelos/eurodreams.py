# modelos/eurodreams.py (Refatorado)

from modelos.loteria_base import LoteriaBase
from modelos.sorteio import Sorteio

class Eurodreams(LoteriaBase):
    def __init__(self):
        # 1. CHAMADA AO CONSTRUTOR PAI COM AS REGRAS OBRIGATÓRIAS
        super().__init__(
            nome="Eurodreams",
            label_complementar="Sonho", # Nome da bola complementar
            # Regras do EuroDreams (6 em 40, 1 em 5)
            qtd_principais=6,
            qtd_complementares=1,
            faixa_principais=(1, 40),
            faixa_complementares=(1, 5)
        )

    # 2. IMPLEMENTAÇÃO DO MÉTODO ABSTRATO
    def validar_sorteio(self, sorteio: Sorteio) -> bool:
        """
        Valida se o sorteio obedece às regras básicas do EuroDreams.
        """
        # A validação da LoteriaBase já trata as regras de quantidade e faixa.
        return super().validar_sorteio(sorteio)

    

