# streamlit_app.py
import streamlit as st
import base64
import os
from servicos.carregar_dados import carregar_todas_loterias
from servicos.calculos_estatisticos import CalculosEstatisticos
from visualizacao.visual_tabelas import ultimos_sorteios, bola
from visualizacao.visual_graficos import evolucao_jackpot, ranking_premios_pais
from typing import Dict

st.set_page_config(page_title="Loterias PT", page_icon="🎰", layout="wide")

st.markdown("""
<style>
    .titulo {font-size:5.5rem; font-weight:900; background:linear-gradient(90deg,#00BFFF,#1E90FF);
             -webkit-background-clip:text; -webkit-text-fill-color:transparent; text-align:center;}
    .card {background:linear-gradient(135deg,#667eea,#764ba2); border-radius:25px; padding:3rem;
           text-align:center; box-shadow:0 20px 40px rgba(0,0,0,0.4); transition:all 0.4s; color:white;}
    .card:hover {transform:translateY(-20px);}
    .metric {background:#f0f2f6; padding:2rem; border-radius:20px; text-align:center;}
</style>
""", unsafe_allow_html=True)

def img64(p):
    return base64.b64encode(open(p, "rb").read()).decode() if os.path.exists(p) else None

loterias = carregar_todas_loterias()

if "lot" not in st.session_state:
    logo = img64("imagens/jogossantacasa.PNG")
    if logo:
        st.image(f"data:image/png;base64,{logo}", width=150)
    st.markdown("<h1 class='titulo'>Loterias de Portugal</h1>", unsafe_allow_html=True)

    cols = st.columns(3)
    for col, (nome, img) in zip(cols, [("Totoloto","totoloto.PNG"), ("Eurodreams","eurodreams.PNG"), ("Euromilhões","euromilhoes.PNG")]):
        with col:
            b64 = img64(f"imagens/{img}")
            total = loterias[nome].total_sorteios
            st.markdown(f"""
            <div class="card">
                <h2>🍀 {nome}</h2>
                {f'<img src="data:image/png;base64,{b64}">' if b64 else ''}
                <p style="font-size:1.6rem;"><b>{total} sorteios</b></p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Abrir {nome}", key=nome):
                st.session_state.lot = nome
                st.rerun()
else:
    lot = loterias[st.session_state.lot]
    calc = CalculosEstatisticos(lot.sorteios).todos()

    st.markdown(f"<h1 style='text-align:center; color:#FFD700;'>🍀 {lot.nome}</h1>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Sorteios", calc['total'])
    c2.metric("Acumulações", calc['acumulacoes'])
    c3.metric("Streak Máximo", calc['streak'])
    c4.metric("Maior Jackpot", f"€{calc['maior_jackpot']:,}")

    evolucao_jackpot(lot)
    ultimos_sorteios(lot)

    st.markdown("### Ranking de Prémios Ganhos por País")
    premios_pais = {}
    for s in lot.sorteios:
        if not s.acumulou and s.jackpot > 0 and hasattr(s, 'paises_ganhadores'):
            for pais in str(s.paises_ganhadores).split(','):
                pais = pais.strip()
                if pais and pais != "nan":
                    premios_pais[pais] = premios_pais.get(pais, 0) + 1

    ranking_premios_pais(premios_pais)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Mais Sorteados")
        for n, q in calc['mais_princ'][:5]:
            st.markdown(f"{bola(n)} → **{q}x**", unsafe_allow_html=True)
    with col2:
        st.subheader("Duplas Quentes")
        for combo, q in calc['duplas']:
            b = " ".join(bola(n) for n in combo)
            st.markdown(f"{b} → **{q}x**", unsafe_allow_html=True)

    if calc['sequencias']:
        st.subheader("Sequências Consecutivas")
        for seq in calc['sequencias']:
            st.write(f"• {seq}")

    if st.button("← Voltar"):
        del st.session_state.lot
        st.rerun()
