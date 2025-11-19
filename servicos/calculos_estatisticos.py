# servicos/calculos_estatisticos.py (Refatorado)

from typing import List, Tuple, Dict, Any, Literal, Counter as TypeCounter
from collections import Counter
from itertools import combinations
from modelos.sorteio import Sorteio

# Tipo de retorno comum para frequência (ex: [(10, 50), (1, 45)])
FrequenciaResultado = List[Tuple[int, int]]

class CalculosEstatisticos:
    """
    Classe para realizar cálculos estatísticos sobre um conjunto de Sorteios.
    É instanciada com os sorteios de uma loteria específica.
    """
    def __init__(self, sorteios: List[Sorteio]):
        # Armazenar os sorteios em ordem de data para garantir consistência nos cálculos de sequência/streak
        self.sorteios = sorted(sorteios, key=lambda s: s.data)

    # --- Métodos de Frequência ---
    
    def frequencia(self, tipo: Literal['principais', 'complementares'] = 'principais') -> TypeCounter:
        """Calcula a frequência de cada número (principal ou complementar)."""
        
        # 💡 Uso de 'getattr' mais limpo, mas a lógica de list comprehension já é concisa.
        if tipo == 'principais':
            return Counter(n for s in self.sorteios for n in s.principais)
        
        # Adiciona uma verificação de segurança, embora a tipagem limite as opções.
        if tipo == 'complementares':
            return Counter(n for s in self.sorteios for n in s.complementares)
            
        # Retorna um Counter vazio se o tipo for inválido.
        return Counter() 

    # --- Repetições / Combinações ---

    def repeticoes(self, tamanho: int = 2, limite: int = 10) -> List[Tuple[Tuple[int, ...], int]]:
        """
        Calcula as combinações de números principais que se repetem.
        Retorna as mais comuns com no mínimo 2 ocorrências.
        """
        c = Counter()
        for s in self.sorteios:
            # 💡 Melhoria de Performance: O sorteio.principais já é sorted pelo __post_init__!
            # Mas combinations(sorted(s.principais),...) é a forma mais segura.
            for combo in combinations(s.principais, tamanho):
                c[combo] += 1
                
        # Retorna as 'limite' combinações mais comuns, desde que ocorram pelo menos 2 vezes
        return [(combo, qtd) for combo, qtd in c.most_common(limite) if qtd >= 2]

    # --- Sequências Consecutivas ---
    
    def sequencias_consecutivas(self, min_tamanho: int = 3) -> List[str]:
        """
        Identifica sequências de números consecutivos (ex: 10, 11, 12) de tamanho >= min_tamanho.
        Retorna uma lista das 10 últimas ocorrências formatadas.
        """
        ocorrencias = []
        for s in self.sorteios:
            nums = s.principais # Já ordenados pelo __post_init__ do Sorteio
            i = 0
            while i < len(nums):
                inicio = i
                # Procura a sequência: se o próximo é igual ao atual + 1
                while i + 1 < len(nums) and nums[i + 1] == nums[i] + 1:
                    i += 1
                
                tamanho_seq = i - inicio + 1
                if tamanho_seq >= min_tamanho:
                    seq = " - ".join(map(str, nums[inicio:i+1]))
                    # Formato limpo e consistente
                    ocorrencias.append(f"{s.data.strftime('%d/%m/%Y')} | C. {s.concurso} | {seq}")
                i += 1
                
        return ocorrencias[-10:]

    # --- Lógica de Acumulação e Jackpots ---

    def streak_acumulacoes(self) -> int:
        """Calcula a maior sequência de sorteios que acumularam."""
        max_streak = atual = 0
        
        # Sorteios já estão ordenados no __init__
        for s in self.sorteios:
            if s.acumulou:
                atual += 1
                max_streak = max(max_streak, atual)
            else:
                atual = 0
        return max_streak

    def maior_jackpot(self) -> int:
        """Retorna o maior valor de jackpot registrado."""
        # 💡 Otimização: Uso de função nativa max() com generator expression
        return max((s.jackpot for s in self.sorteios), default=0)

    def total_acumulacoes(self) -> int:
        """Retorna o número total de sorteios que acumularam."""
        return sum(1 for s in self.sorteios if s.acumulou)

    # --- Prémios por País ---

    def premios_por_pais(self) -> Dict[str, int]:
        """
        Calcula o contador de jackpots ganhos por país (quando não acumulado).
        """
        contador = Counter()
        for s in self.sorteios:
            # Condição: Não acumulou E há um prêmio significativo
            if not s.acumulou and s.jackpot > 0: 
                # O atributo "paises_ganhadores" foi padronizado no Sorteio
                paises_raw = s.paises_ganhadores
                
                if paises_raw:
                    # Itera sobre os países (se a célula tiver 'Portugal, Espanha')
                    for pais in str(paises_raw).split(","):
                        pais = pais.strip()
                        if pais: # Garante que o país não é uma string vazia
                            # 💡 Padroniza a capitalização do país para contagem consistente
                            contador[pais.title()] += 1 
                            
        # O uso do 'dict(contador)' é opcional, mas garante o tipo de retorno
        return dict(contador.most_common())

    # --- Função de Agregação Final ---

    def todos(self) -> Dict[str, Any]:
        """Agrega todos os cálculos em um único dicionário de resultados."""
        fp = self.frequencia('principais')
        fc = self.frequencia('complementares')

        return {
            # Resumos
            'total_sorteios': len(self.sorteios),
            'total_acumulacoes': self.total_acumulacoes(),
            'max_streak_acumulacoes': self.streak_acumulacoes(),
            'maior_jackpot': self.maior_jackpot(),
            
            # Frequências
            'mais_frequentes_princ': fp.most_common(10), # Aumentei para 10
            'menos_frequentes_princ': sorted(fp.items(), key=lambda x: x[1])[:10], # Aumentei para 10
            'mais_frequentes_comp': fc.most_common(10), # Aumentei para 10
            
            # Repetições
            'duplas_repetidas': self.repeticoes(2, limite=10),
            'trios_repetidos': self.repeticoes(3, limite=10),
            'quadras_repetidas': self.repeticoes(4, limite=10),
            'sequencias_consecutivas': self.sequencias_consecutivas(),
            
            # Dados Geográficos
            'premios_por_pais': self.premios_por_pais(),
        }