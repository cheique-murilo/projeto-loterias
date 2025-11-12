
import sys
from os.path import join, dirname, abspath
from typing import List

# Adiciona raiz ao path
projeto_root = abspath(join(dirname(__file__), '..'))
sys.path.insert(0, projeto_root)

from modelos.loteria import Loteria
from servicos.estatistica import Estatistica  # <- Fix: Import absoluto

class Curiosidade:
    @staticmethod
    def gerar_insights(loteria: Loteria) -> List[str]:
        insights = []
        mais, _ = Estatistica.numeros_mais_menos_sairam(loteria, top_k=1)
        if mais:
            insights.append(f"O número {mais[0][0]} saiu mais vezes na {loteria.nome}: {mais[0][1]} vezes!")
        acums = Estatistica.contar_acumulacoes(loteria)
        insights.append(f"A {loteria.nome} acumulou {acums} vezes o jackpot.")
        
        # Vezes divididas vs única aposta
        divididos = Estatistica.jackpots_divididos(loteria)
        unica_aposta = divididos.get(1, 0)
        multi_apostas = sum(divididos.get(v, 0) for v in divididos if v > 1)
        total_jackpots = unica_aposta + multi_apostas
        if total_jackpots > 0:
            insights.append(f"Jackpots: {unica_aposta} vezes para 1 aposta, {multi_apostas} vezes divididos")
        
        # Streak máximo de acumulações
        streak_max = Estatistica.streak_max_acumulacoes(loteria)
        insights.append(f"O máximo streak de acumulações foi de {streak_max} sorteios consecutivos.")

        return insights