# services/calculos_estatisticos.py
from typing import List, Tuple, Dict, Any
from collections import Counter
from itertools import combinations
from modelos.sorteio import Sorteio

class CalculosEstatisticos:
    def __init__(self, sorteios: List[Sorteio]):
        self.sorteios = sorteios

    def frequencia(self, tipo: str = 'principais') -> Counter:
        if tipo == 'principais':
            return Counter(n for s in self.sorteios for n in s.principais)
        return Counter(n for s in self.sorteios for n in s.complementares)

    def repeticoes(self, tamanho: int = 2) -> List[Tuple[Tuple[int, ...], int]]:
        c = Counter()
        for s in self.sorteios:
            for combo in combinations(sorted(s.principais), tamanho):
                c[combo] += 1
        return [(combo, qtd) for combo, qtd in c.most_common(15) if qtd >= 2]

    def sequencias_consecutivas(self):
        ocorrencias = []
        for s in self.sorteios:
            nums = sorted(s.principais)
            i = 0
            while i < len(nums):
                inicio = i
                while i + 1 < len(nums) and nums[i + 1] == nums[i] + 1:
                    i += 1
                if i - inicio + 1 >= 3:
                    seq = " - ".join(map(str, nums[inicio:i+1]))
                    ocorrencias.append(f"{s.data.strftime('%d/%m/%Y')} • {s.concurso} → {seq}")
                i += 1
        return ocorrencias[-10:]

    def streak_acumulacoes(self) -> int:
        max_streak = atual = 0
        for s in sorted(self.sorteios, key=lambda x: x.data):
            if s.acumulou:
                atual += 1
                max_streak = max(max_streak, atual)
            else:
                atual = 0
        return max_streak

    def todos(self) -> Dict[str, Any]:
        fp = self.frequencia('principais')
        fc = self.frequencia('complementares')
        return {
            'total': len(self.sorteios),
            'acumulacoes': sum(1 for s in self.sorteios if s.acumulou),
            'streak': self.streak_acumulacoes(),
            'maior_jackpot': max((s.jackpot for s in self.sorteios), default=0),
            'mais_princ': fp.most_common(15),
            'menos_princ': sorted(fp.items(), key=lambda x: x[1])[:15],
            'mais_comp': fc.most_common(10),
            'duplas': self.repeticoes(2),
            'trios': self.repeticoes(3),
            'sequencias': self.sequencias_consecutivas(),
        }
    
    def premios_por_pais(self) -> Dict[str, int]:
        """Conta quantas vezes o jackpot foi ganho em cada país (só quando não acumulou e vencedores > 0)"""
        from collections import Counter
        contador = Counter()
        for s in self.sorteios:
            if not s.acumulou and s.jackpot > 0:  # só conta quando houve vencedor
                # Simulação simples: se a coluna 'paises' não existir, vamos assumir que existe uma coluna 'paises' no Excel
                # Se não tiveres essa coluna ainda, podemos melhorar depois
                # Por agora vamos usar um placeholder lógico
                pass  # vamos preencher no carregamento
        return dict(contador.most_common())