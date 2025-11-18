# services/carregar_dados.py
import pandas as pd
import streamlit as st
from modelos import Totoloto, Eurodreams, Euromilhoes, Sorteio

@st.cache_data(show_spinner="Carregando dados...")
def carregar_todas_loterias():
    df = pd.read_excel("dados_loterias.xlsx")

    loterias = {
        "Totoloto": Totoloto(),
        "Eurodreams": Eurodreams(),
        "Euromilhões": Euromilhoes(),
    }

    for _, row in df.iterrows():
        nome_raw = str(row["loteria"]).strip().lower()

        if "totoloto" in nome_raw:
            lot = loterias["Totoloto"]
        elif "eurodreams" in nome_raw:
            lot = loterias["Eurodreams"]
        elif "euromilh" in nome_raw:
            lot = loterias["Euromilhões"]
        else:
            continue

        try:
            principais = sorted(int(x) for x in str(row["numeros_sorteados"]).replace(" ", "").split(",") if x.isdigit())
            complementares = [int(x) for x in str(row["numeros_complementares"]).replace(" ", "").split(",") if x.isdigit()] or [0]

            if not principais:
                continue

            sorteio = Sorteio(
                data=pd.to_datetime(row["data"]),
                concurso=str(row["sorteio"]),
                principais=principais,
                complementares=sorted(complementares),
                acumulou=str(row.get("acumulou", "")).lower() == "sim",
                jackpot=int(row["jackpot"]) if pd.notna(row.get("jackpot")) else 0,
            )
            lot.adicionar(sorteio)
        except:
            continue

    total = sum(lot.total_sorteios for lot in loterias.values())
    st.success(f"Carregados {total} sorteios!")
    return loterias