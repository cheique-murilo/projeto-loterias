
import sys
from os.path import join, dirname, abspath
from collections import Counter
from typing import Dict, List, Tuple
from itertools import combinations

# Adiciona raiz ao path
projeto_root = abspath(join(dirname(__file__), '..'))
sys.path.insert(0, projeto_root)

from modelos.loteria import Loteria

class Estatistica:
    @staticmethod
    def numeros_mais_menos_sairam(loteria: Loteria, tipo: str = 'principais', top_k: int = 5) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
        numeros = loteria.get_todos_numeros(tipo)
        contagem = Counter(numeros)
        mais = contagem.most_common(top_k)
        menos = sorted(contagem.items(), key=lambda x: x[1])[:top_k]
        return mais, menos

    @staticmethod
    def conjuntos_repetidos(loteria: Loteria, tamanho: int = 2, min_ocorrencias: int = 2) -> List[Tuple[Tuple[int, ...], int]]:
        """Encontra duplas (tamanho=2), trios (3), etc. que se repetem."""
        todos_conjuntos = []
        for sorteio in loteria.sorteios:
            nums = tuple(sorted(sorteio.numeros_sorteados))  # Apenas principais, em ordem
            todos_conjuntos.extend(combinations(nums, tamanho))
        contagem = Counter(todos_conjuntos)
        repetidos = [(conj, count) for conj, count in contagem.items() if count >= min_ocorrencias]
        return sorted(repetidos, key=lambda x: x[1], reverse=True)[:10]  # Top 10

    @staticmethod
    def contar_acumulacoes(loteria: Loteria) -> int:
        return sum(1 for s in loteria.sorteios if s.acumulou)

    @staticmethod
    def jackpots_divididos(loteria: Loteria) -> Dict[int, int]:
        """Conta vezes que jackpot foi dividido por número de vencedores."""
        contagem = Counter()
        for s in loteria.sorteios:
            if s.jackpot and not s.acumulou and s.vencedores > 1:
                contagem[s.vencedores] += 1
        return dict(contagem)

    @staticmethod
    def premios_por_pais(loterias: Dict[str, Loteria]) -> Dict[str, int]:
        """Soma prêmios por país (apenas jackpots não acumulados)."""
        total_paises = Counter()
        for loteria in loterias.values():
            for s in loteria.sorteios:
                if s.premio:
                    for pais in s.paises:
                        total_paises[pais] += s.premio
        return dict(total_paises)
    
    @staticmethod
    def streak_max_acumulacoes(loteria: Loteria) -> int:  # <- Novo método
        if not loteria.sorteios:
            return 0
        max_streak = 0
        current_streak = 0
        for s in sorted(loteria.sorteios, key=lambda x: x.data):
            if s.acumulou:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0
        return max_streak