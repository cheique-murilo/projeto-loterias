# visualizacao/visual_graficos.py
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
from modelos.loteria_base import LoteriaBase
from typing import Dict

def evolucao_jackpot(loteria: LoteriaBase):
    # Agora recebe SÓ a loteria selecionada
    dados = []
    for s in loteria.sorteios:
        if s.jackpot > 0:
            dados.append({"data": s.data, "jackpot": s.jackpot / 1_000_000})

    if not dados:
        st.info("Nenhum jackpot registrado para esta loteria.")
        return

    df = pd.DataFrame(dados).sort_values('data')

    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(df['data'], df['jackpot'], marker='o', linewidth=3, markersize=6, color='#FF6B6B')
    ax.set_title(f"Evolução do Jackpot – {loteria.nome}", fontsize=20, pad=20)
    ax.set_ylabel("Jackpot (milhões €)", fontsize=14)
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

def ranking_premios_pais(premios_por_pais: Dict[str, int]):
    if not premios_por_pais:
        st.info("Ainda não há dados de prémios ganhos por país (ou a coluna 'paises_ganhadores' está vazia).")
        return

    paises = list(premios_por_pais.keys())
    contagens = list(premios_por_pais.values())

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(paises, contagens, color='#00BFFF', edgecolor='navy')
    ax.set_title("Ranking de Prémios Ganhos por País", fontsize=18, pad=20)
    ax.set_xlabel("Número de Vezes que o Jackpot Foi Ganho")
    ax.invert_yaxis()

    # Destacar Portugal se estiver no top
    for i, bar in enumerate(bars):
        if paises[i] == "Portugal":
            bar.set_color('#FF6B6B')

    # Números nas barras
    for i, v in enumerate(contagens):
        ax.text(v + 0.1, i, str(v), color='black', va='center', fontweight='bold')

    plt.tight_layout()
    st.pyplot(fig)