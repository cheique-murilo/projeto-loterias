
import sys
from os.path import join, dirname, abspath
from typing import List

# Adiciona raiz ao path para imports absolutos
projeto_root = abspath(join(dirname(__file__), '..'))
sys.path.insert(0, projeto_root)

from modelos.loteria import Loteria
from servicos.estatistica import Estatistica  # <- Mudança aqui: 'servicos.estatistica'

class Curiosidade:
    @staticmethod
    def gerar_insights(loteria: Loteria) -> List[str]:
        insights = []
        mais, _ = Estatistica.numeros_mais_menos_sairam(loteria, top_k=1)
        if mais:
            insights.append(f"O número {mais[0][0]} saiu mais vezes na {loteria.nome}: {mais[0][1]} vezes!")
        acums = Estatistica.contar_acumulacoes(loteria)
        insights.append(f"A {loteria.nome} acumulou {acums} vezes o jackpot.")
        return insights