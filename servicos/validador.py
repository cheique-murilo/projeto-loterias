# servicos/validador.py
import pandas as pd
import streamlit as st
from typing import Dict, Any, List

# --- IMPORTAÇÕES CRÍTICAS (Para evitar NameError) ---
from servicos.carregar_dados import carregar_dados_brutos 
from modelos.sorteio import Sorteio
from modelos.totoloto import Totoloto
from modelos.eurodreams import Eurodreams
from modelos.euromilhoes import Euromilhoes

def _converter_numeros(valor_bruto: Any, ordenar: bool = False) -> List[int]:
    """
    Converte o dado bruto do Excel em lista de números.
    Resolve o problema do Euromilhões virar '1.2'.
    """
    if pd.isna(valor_bruto) or str(valor_bruto).strip() == "":
        return []

    try:
        # 1. Garante que é string e limpa espaços
        texto = str(valor_bruto).strip().replace(" ", "")
        
        # 2. O TRUQUE DO PONTO: Se vier "1.2" (caso Euromilhões), vira "1,2"
        if "." in texto:
            texto = texto.replace(".", ",")
            
        # 3. O TRUQUE DO PONTO-E-VÍRGULA: Prevenção
        if ";" in texto:
            texto = texto.replace(";", ",")

        # 4. Divide e converte
        partes = texto.split(",")
        numeros = []
        for p in partes:
            if p.isdigit():
                numeros.append(int(p))
        
        return sorted(numeros) if ordenar else numeros

    except Exception:
        return []

def validar_e_popular_loterias(df: pd.DataFrame) -> Dict[str, Any]:
    # Inicializa os modelos
    loterias = {
        "Totoloto": Totoloto(),
        "Eurodreams": Eurodreams(),
        "Euromilhões": Euromilhoes(),
    }
    
    # Mapa simples para garantir que encontramos a loteria correta
    mapa = {
        "Totoloto": loterias["Totoloto"],
        "Eurodreams": loterias["Eurodreams"],
        "Euromilhoes": loterias["Euromilhões"], # Sem acento
        "Euromilhões": loterias["Euromilhões"], # Com acento
    }

    validos = 0
    
    for _, row in df.iterrows():
        # Pega o nome e remove espaços extras
        nome = str(row.get("loteria", "")).strip().title()
        
        if nome not in mapa:
            continue
            
        loto = mapa[nome]
        
        # Converte os números usando a função corrigida
        princ = _converter_numeros(row.get("numeros_sorteados"), True)
        comp = _converter_numeros(row.get("numeros_complementares"), False)
        
        if not princ or not comp:
            continue

        try:
            # Cria o Sorteio
            # Tratamento de jackpot: remove "€", "," e espaços antes de converter
            jackpot_raw = str(row.get("jackpot", "0")).replace("€", "").replace(",", "").replace(" ", "").split(".")[0]
            
            sorteio = Sorteio(
                data=pd.to_datetime(row["data"]),
                concurso=str(row["sorteio"]),
                principais=princ,
                complementares=comp,
                acumulou=str(row.get("acumulou", "")).lower() == "sim",
                jackpot=int(jackpot_raw) if jackpot_raw.isdigit() else 0,
                paises_ganhadores=str(row.get("pais", ""))
            )
            
            loto.adicionar(sorteio)
            validos += 1
            
        except Exception:
            continue

    return loterias

# --- FUNÇÃO DE FACHADA ---
def carregar_e_processar_loterias():
    df = carregar_dados_brutos()
    if df.empty:
        return {}
    return validar_e_popular_loterias(df)