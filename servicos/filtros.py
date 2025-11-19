# services/filtros.py
from typing import List
from modelos.sorteio import Sorteio

class LoteriaFiltrada:
    """View leve e modular para sorteios filtrados – sem gambiarra"""
    def __init__(self, nome: str, label_complementar: str, sorteios: List[Sorteio]):
        self.nome = nome
        self.label_complementar = label_complementar
        self.sorteios = sorteios

def filtrar_por_data(loteria, inicio, fim):
    """Retorna uma LoteriaFiltrada com os sorteios no intervalo"""
    from datetime import datetime
    inicio_dt = datetime.combine(inicio, datetime.min.time())
    fim_dt = datetime.combine(fim, datetime.max.time())
    filtrados = [s for s in loteria.sorteios if inicio_dt <= s.data <= fim_dt]
    return LoteriaFiltrada(loteria.nome, loteria.label_complementar, filtrados)

