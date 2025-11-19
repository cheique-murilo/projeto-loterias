# modelos/euromilhoes.py (Refatorado)

from modelos.loteria_base import LoteriaBase
from modelos.sorteio import Sorteio

class Euromilhoes(LoteriaBase):
    def __init__(self):
        # 1. CHAMADA AO CONSTRUTOR PAI COM AS REGRAS OBRIGATÓRIAS
        super().__init__(
            nome="Euromilhões",
            label_complementar="Estrelas",
            # Regras do Euromilhões (5 em 50, 2 em 12)
            qtd_principais=5,
            qtd_complementares=2,
            faixa_principais=(1, 50),
            faixa_complementares=(1, 12)
        )

    # 2. IMPLEMENTAÇÃO DO MÉTODO ABSTRATO (OBRIGATÓRIO)
    def validar_sorteio(self, sorteio: Sorteio) -> bool:
        """
        Valida se o sorteio obedece às regras básicas do Euromilhões
        (quantidade, faixa de números e duplicatas).
        """
        # A validação básica na LoteriaBase já é suficiente
        return super().validar_sorteio(sorteio)




