# diagnostico.py
import pandas as pd
import os

ARQUIVO = "dados_loterias.xlsx"

def diagnosticar():
    print(f"--- INICIANDO DIAGNÓSTICO DE {ARQUIVO} ---")
    
    if not os.path.exists(ARQUIVO):
        print(f"ERRO: Arquivo {ARQUIVO} não encontrado!")
        return

    # Ler o Excel forçando tudo como string para ver o que realmente está lá
    try:
        df = pd.read_excel(ARQUIVO, engine='openpyxl', dtype=str)
        print(f"Arquivo lido com sucesso. Total de linhas: {len(df)}")
        print(f"Colunas encontradas: {list(df.columns)}\n")
    except Exception as e:
        print(f"ERRO FATAL ao ler Excel: {e}")
        return

    problemas = 0
    
    # Vamos verificar as primeiras 5 linhas e depois focar nas problemáticas
    print("--- AMOSTRA DAS PRIMEIRAS 3 LINHAS ---")
    print(df[['loteria', 'numeros_sorteados', 'numeros_complementares']].head(3))
    print("\n--- PROCURANDO DADOS PROBLEMÁTICOS ---")

    for i, row in df.iterrows():
        # Simulação da conversão
        complementares_raw = str(row.get('numeros_complementares', ''))
        
        # Tenta limpar como fizemos no validador
        limpo = complementares_raw.replace(" ", "").strip()
        
        # Se estiver vazio ou for "nan", é um problema
        if limpo.lower() in ['nan', '', 'none']:
            print(f"[LINHA {i+2}] PROBLEMA: Complementares vazio. Loteria: {row.get('loteria')}")
            problemas += 1
            continue
            
        # Se for Euromilhões e não tiver vírgula ou ponto (deve ter 2 números)
        if str(row.get('loteria')).strip() == "Euromilhões":
            if ',' not in limpo and '.' not in limpo:
                 # Se tiver menos de 3 caracteres (ex: "12"), pode ser erro
                 print(f"[LINHA {i+2}] ALERTA EUROMILHÕES: Valor estranho '{complementares_raw}'")

    print(f"\n--- DIAGNÓSTICO CONCLUÍDO ---")
    print(f"Total de linhas potencialmente vazias/inválidas: {problemas}")

if __name__ == "__main__":
    diagnosticar()