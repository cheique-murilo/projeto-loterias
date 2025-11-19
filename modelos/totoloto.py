# modelos/totoloto.py (Refatorado)

from modelos.loteria_base import LoteriaBase
from modelos.sorteio import Sorteio

class Totoloto(LoteriaBase):
    def __init__(self):
        # 1. CHAMADA AO CONSTRUTOR PAI COM AS REGRAS OBRIGATÓRIAS
        super().__init__(
            nome="Totoloto",
            label_complementar="Chave",
            # Regras do Totoloto (5 em 49, 1 em 13)
            qtd_principais=5,
            qtd_complementares=1,
            faixa_principais=(1, 49),
            faixa_complementares=(1, 13)
        )

    # 2. IMPLEMENTAÇÃO DO MÉTODO ABSTRATO
    def validar_sorteio(self, sorteio: Sorteio) -> bool:
        """
        Valida se o sorteio obedece às regras básicas do Totoloto.
        """
        # A validação da LoteriaBase já é completa.
        return super().validar_sorteio(sorteio)