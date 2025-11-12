
import sys
from os.path import join, dirname, abspath
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import Dict
from collections import Counter

# Adiciona raiz ao path para imports absolutos
projeto_root = abspath(join(dirname(__file__), '..'))
sys.path.insert(0, projeto_root)

from modelos.loteria import Loteria
from servicos.estatistica import Estatistica

class Graficos:
    @staticmethod
    def grafico_evolucao_jackpot(loterias: Dict[str, Loteria], salvar: bool = True):
        fig, ax = plt.subplots(figsize=(12, 6))
        tem_dados = False
        for nome, loteria in loterias.items():
            datas = [s.data for s in loteria.sorteios if s.jackpot]
            valores = [s.jackpot for s in loteria.sorteios if s.jackpot]
            if datas and valores:
                ax.plot(datas, valores, label=nome, marker='o')
                tem_dados = True
        if not tem_dados:
            ax.text(0.5, 0.5, 'Sem dados de jackpot disponíveis', ha='center', va='center', transform=ax.transAxes)
        else:
            ax.set_title('Evolução do Jackpot por Loteria')
            ax.set_ylabel('Valor do Jackpot (€)')
            ax.legend()
            ax.tick_params(axis='x', rotation=45)
        plt.tight_layout()
        if salvar:
            plt.savefig('../jackpot_evolucao.png', dpi=300, bbox_inches='tight')
        plt.show()

    @staticmethod
    def grafico_ranking_paises(premios_paises: Dict[str, int], salvar: bool = True):
        if not premios_paises:
            print("Sem dados de premiações por país.")
            return
        df_paises = pd.DataFrame(list(premios_paises.items()), columns=['Pais', 'Total_Premiado'])
        df_paises = df_paises.sort_values('Total_Premiado', ascending=False)
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df_paises, x='Pais', y='Total_Premiado')
        plt.title('Ranking de Premiações por País')
        plt.xlabel('País')
        plt.ylabel('Total Premiado (€)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        if salvar:
            plt.savefig('../ranking_paises.png', dpi=300, bbox_inches='tight')
        plt.show()

    @staticmethod
    def tabela_jackpots_divididos(dados: Dict[int, int], salvar: bool = True):
        if not dados:
            print("Sem dados de jackpots divididos.")
            return
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.axis('tight')
        ax.axis('off')
        table_data = [[k, v] for k, v in dados.items()]
        table = ax.table(cellText=table_data,
                         colLabels=['Nº Vencedores', 'Vezes Dividido'],
                         cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.5)
        ax.set_title('Jackpots Divididos', fontsize=14)
        plt.tight_layout()
        if salvar:
            plt.savefig('../tabela_divididos.png', dpi=300, bbox_inches='tight')
        plt.show()