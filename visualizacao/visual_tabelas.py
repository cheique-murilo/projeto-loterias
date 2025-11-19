# visualizacao/visual_tabelas.py (FINAL - Apenas dados)

from typing import List

def obter_dados_ultimos_sorteios(loteria) -> List[dict]:
    """
    Prepara os dados dos últimos 5 sorteios para renderização,
    retornando uma lista de dicionários.
    """
    ultimos = loteria.sorteios[-5:] 

    dados_formatados = []
    for s in ultimos:
        dados_formatados.append({
            "data": s.data, 
            "data_str": s.data.strftime('%d/%m/%Y'),
            "concurso": s.concurso,
            "principais": s.principais,
            "complementares": s.complementares,
            "acumulou": s.acumulou,
            "label_complementar": loteria.label_complementar,
            "nome_loteria": loteria.nome
        })
        
    return list(reversed(dados_formatados))
# A função 'bola' e o código Streamlit/HTML foram removidos.