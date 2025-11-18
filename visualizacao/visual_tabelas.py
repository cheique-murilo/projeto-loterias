# visualizacao/visual_tabelas.py
import streamlit as st

def bola(n: int, estrela: bool = False):
    cor = "background: linear-gradient(45deg, #4CAF50, #8BC34A); color: white" if estrela else "background: linear-gradient(45deg, #FFD700, #FFA500); color: black"
    return f'<span style="font-size:2.3rem; font-weight:bold; padding:0.6rem 1.2rem; margin:0.4rem; border-radius:50px; display:inline-block; {cor}">{n}</span>'

def ultimos_sorteios(loteria):
    st.subheader("🎯 Últimos 5 Sorteios")
    for s in loteria.ultimos_5:
        bolas = " ".join(bola(n) for n in s.principais)
        
        # Correção aqui: reconhece o complementar correto
        if len(s.complementares) == 1 and s.complementares[0] != 0:
            comp = s.complementares[0]
            comp_html = bola(comp, estrela=True)
        elif len(s.complementares) == 2:  # Euromilhões tem 2 estrelas
            comp_html = " ".join(bola(n, estrela=True) for n in s.complementares)
        else:
            comp_html = "-"

        st.markdown(f"""
        <div style="background:#1e1e1e; color:white; padding:2rem; border-radius:20px; text-align:center; margin:1rem 0;">
            <h3>{s.data.strftime('%d/%m/%Y')} • Concurso {s.concurso}</h3>
            {bolas}<br><br>
            <b>{loteria.label_complementar}:</b> {comp_html}
            {' ➜ <span style="color:#FF4444; font-size:1.8rem;">ACUMULOU!</span>' if s.acumulou else ''}
        </div>
        """, unsafe_allow_html=True)