
import os
import sys

projeto_root = os.getcwd()
sys.path.insert(0, projeto_root)

from servicos.carregar_dados import FonteDados
from servicos.estatistica import Estatistica
from servicos.curiosidade import Curiosidade
from visualizacao.graficos import Graficos

def main():
    caminho_excel = os.path.join(projeto_root, 'dados_loterias.xlsx')
    if not os.path.exists(caminho_excel):
        print(f"Erro: Arquivo {caminho_excel} não encontrado!")
        return
    print("Carregando dados do Excel...")
    fonte = FonteDados(caminho_excel)
    loterias = fonte.carregar_dados()
    print("\n=== ESTATÍSTICAS POR LOTERIA ===")
    for nome, loteria in loterias.items():
        if not loteria.sorteios:
            print(f"\n--- {nome} --- Sem dados de sorteios.")
            continue
        print(f"\n--- {nome} ({len(loteria.sorteios)} sorteios) ---")
        mais, menos = Estatistica.numeros_mais_menos_sairam(loteria, tipo='principais')
        print(f"Números mais saídos (principais): {mais}")
        print(f"Números menos saídos (principais): {menos}")
        repetidos = Estatistica.conjuntos_repetidos(loteria, tamanho=2)
        print("Conjuntos repetidos (duplas, top 5):", repetidos[:5])
        acums = Estatistica.contar_acumulacoes(loteria)
        print(f"Acumulações de jackpot: {acums}")
        insights = Curiosidade.gerar_insights(loteria)
        print("Curiosidades:", insights)
    print("\n=== ESTATÍSTICAS GLOBAIS ===")
    premios_paises = Estatistica.premios_por_pais(loterias)
    print("Premiações por país (total €):", dict(premios_paises))
    todos_divididos = {}
    for _, loteria in loterias.items():
        divididos_lot = Estatistica.jackpots_divididos(loteria)
        for v, count in divididos_lot.items():
            todos_divididos[v] = todos_divididos.get(v, 0) + count
    print("Jackpots divididos (todas loterias - nº vencedores: vezes):", dict(todos_divididos))
    print("\nGerando gráficos...")
    Graficos.grafico_evolucao_jackpot(loterias)
    Graficos.grafico_ranking_paises(premios_paises)
    Graficos.tabela_jackpots_divididos(todos_divididos)
    print("\nAnálise concluída! Verifique PNGs na raiz.")

if __name__ == "__main__":
    main()