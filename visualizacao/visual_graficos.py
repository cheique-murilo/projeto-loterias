# visualizacao/visual_graficos.py (FINAL - Apenas dados)

import pandas as pd
from typing import Optional

def preparar_dados_evolucao_jackpot(loteria) -> Optional[pd.DataFrame]:
    """
    Prepara o DataFrame com a evolução do jackpot (data e valor em milhões).
    """
    dados = [
        {"data": s.data, "jackpot_milhoes": s.jackpot / 1_000_000}
        for s in loteria.sorteios if s.jackpot > 0
    ]

    if not dados:
        return None

    return pd.DataFrame(dados).sort_values('data')
# O código Matplotlib/Streamlit foi removido.
