# servicos/carregar_dados.py
import pandas as pd
import streamlit as st
import os

CAMINHO_ARQUIVO = "dados_loterias.xlsx"

@st.cache_data(show_spinner="Lendo Excel...")
def carregar_dados_brutos() -> pd.DataFrame:
    if not os.path.exists(CAMINHO_ARQUIVO):
        st.error(f"Arquivo {CAMINHO_ARQUIVO} não encontrado.")
        return pd.DataFrame()

    try:
        # O SEGREDO: dtype=str força tudo a ser lido como texto,
        # impedindo o Pandas de tentar adivinhar números.
        df = pd.read_excel(CAMINHO_ARQUIVO, engine='openpyxl', dtype=str)
        
        # Limpeza básica de nomes
        if 'loteria' in df.columns:
             df['loteria'] = df['loteria'].str.strip().str.title()
             
        return df

    except Exception as e:
        st.error(f"Erro fatal na leitura: {e}")
        return pd.DataFrame()