# streamlit_app.py - VERSÃO FINAL COMPLETA
import streamlit as st
import base64
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# --- IMPORTAÇÕES DOS SERVIÇOS REFATORADOS ---
# Certifique-se de que os arquivos __init__.py existem nas pastas, mesmo que vazios
from servicos.validador import carregar_e_processar_loterias
from servicos.calculos_estatisticos import CalculosEstatisticos
from servicos.filtros import filtrar_por_data
from visualizacao.visual_tabelas import obter_dados_ultimos_sorteios
from visualizacao.visual_graficos import preparar_dados_evolucao_jackpot

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Loterias de Portugal",
    page_icon="🎰",
    layout="wide"
)

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
<style>
    /* Estilo dos Cards da Tela Inicial */
    .card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
        margin-bottom: 1rem;
    }
    .card:hover {
        transform: translateY(-5px);
    }
    .card h2 { margin-bottom: 0; color: white; text-shadow: 0 2px 4px rgba(0,0,0,0.3); }
    .card p { font-size: 1.2rem; opacity: 0.9; }

    /* Estilo das Bolas */
    .bola-base {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 2.8rem;
        height: 2.8rem;
        border-radius: 50%;
        font-weight: bold;
        font-size: 1.2rem;
        margin: 0.2rem;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    }
    
    /* Container de Sorteio */
    .sorteio-box {
        background-color: #262730;
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid #404040;
        margin-bottom: 1rem;
        text-align: center;
    }
    .sorteio-data { font-size: 0.9rem; color: #aaa; margin-bottom: 0.5rem; }
    .acumulou-tag { 
        display: inline-block; 
        background: #ff4b4b; 
        color: white; 
        padding: 2px 8px; 
        border-radius: 4px; 
        font-size: 0.8rem; 
        font-weight: bold;
        margin-left: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- FUNÇÕES AUXILIARES VISUAIS ---
def bola(n: int, tipo: str = "PRINCIPAL") -> str:
    """Gera o HTML para uma bola de loteria."""
    if tipo == "PRINCIPAL":
        estilo = "background: linear-gradient(145deg, #FFD700, #FFA500); color: #000;"
    elif tipo == "COMPLEMENTAR": # Estrelas (Euromilhões)
        estilo = "background: linear-gradient(145deg, #4CAF50, #2E8B57); color: #fff;"
    else: # Chave/Sonho (Totoloto/Eurodreams)
        estilo = "background: linear-gradient(145deg, #00BFFF, #1E90FF); color: #fff;"
        
    return f'<span class="bola-base" style="{estilo}">{n}</span>'

def img64(path):
    """Converte imagem para base64 de forma segura."""
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# --- CARREGAMENTO DE DADOS ---

    # --- 🖼️ HEADER COM LOGO JOGOS SANTA CASA ---
col_logo= st.columns(1) 
c_logo = st.container()
with c_logo:
    col_esq, col_meio, col_dir = st.columns([1, 1, 1])
    with col_meio:
            # Centraliza usando colunas
            if os.path.exists("imagens/jogossantacasa.png"):
                st.image("imagens/jogossantacasa.png", width=250)

st.header("📈 Análise das loterias de Portugal")

st.divider() # Uma linha separadora elegante

try:
    with st.spinner("Carregando e validando base de dados..."):
        loterias = carregar_e_processar_loterias()
except Exception as e:
    st.error("❌ Erro crítico ao iniciar o sistema.")
    st.exception(e)
    st.stop()

# Verifica se temos dados
total_geral = sum(l.total_sorteios for l in loterias.values())
if total_geral == 0:
    st.warning("⚠️ O sistema carregou, mas nenhum sorteio foi validado.")
    st.info("Verifique se o arquivo 'dados_loterias.xlsx' contém dados e se as colunas estão nomeadas corretamente.")
    st.stop()

# --- NAVEGAÇÃO ---
if "lot" not in st.session_state:
    # TELA INICIAL (DASHBOARD GERAL)      
    
    st.markdown("### Escolha uma loteria para analisar")
    
    cols = st.columns(3)
    opcoes = [
        ("Totoloto", "totoloto.png"), 
        ("Eurodreams", "eurodreams.png"), 
        ("Euromilhões", "euromilhoes.png")
    ]
    
    for col, (nome, img_file) in zip(cols, opcoes):
        loto = loterias.get(nome)
        if not loto: continue
        
        with col:
            # Card Visual
            img_code = img64(f"imagens/{img_file}")
            img_html = f'<img src="data:image/png;base64,{img_code}" style="height:100px; margin-bottom:10px;">' if img_code else ""
            
            st.markdown(f"""
            <div class="card">
                {img_html}
                <h2>{nome}</h2>
                <p>{loto.total_sorteios} Sorteios carregados</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Abrir análise {nome}", key=f"btn_{nome}", use_container_width=True):
                st.session_state.lot = nome
                st.rerun()

else:
    # TELA DE DETALHES DA LOTERIA
    nome_lot = st.session_state.lot
    loto_original = loterias.get(nome_lot)

    # Botão Voltar no topo
    if st.button("← Voltar ao menu principal"):
        del st.session_state.lot
        st.rerun()

    # --- BARRA LATERAL (FILTROS) ---
    st.sidebar.header(f"Filtros: {nome_lot}")
    
    if loto_original.total_sorteios > 0:
        min_date = min(s.data for s in loto_original.sorteios).date()
        max_date = max(s.data for s in loto_original.sorteios).date()
        
        d_inicio = st.sidebar.date_input("Data Inicial", min_date, min_value=min_date, max_value=max_date)
        d_fim = st.sidebar.date_input("Data Final", max_date, min_value=min_date, max_value=max_date)
        
        # Aplica filtro
        loto = filtrar_por_data(loto_original, d_inicio, d_fim)
    else:
        st.error("Sem dados para filtrar.")
        st.stop()

    # --- CÁLCULOS ESTATÍSTICOS ---
    # Instancia a classe de cálculos com os dados filtrados
    calc_sys = CalculosEstatisticos(loto.sorteios)
    stats = calc_sys.todos()

    st.markdown(f"# 🍀 Análise: {nome_lot}")
    
    # 1. MÉTRICAS PRINCIPAIS
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Sorteios no período", stats.get('total_sorteios', 0))
    k2.metric("Total acumulações", stats.get('total_acumulacoes', 0))
    k3.metric("Maior sequência acumulada", f"{stats.get('max_streak_acumulacoes', 0)} vezes")
    k4.metric("Maior jackpot", f"€ {stats.get('maior_jackpot', 0):,}")
    
    st.divider()

    # 2. GRÁFICOS E RANKING
    c_graf, c_rank = st.columns([2, 1])
    
    with c_graf:
        st.subheader("📈 Evolução do jackpot")
        
        # Gera os dados baseados no lote já filtrado (loto)
        df_jackpot = preparar_dados_evolucao_jackpot(loto)
        
        if df_jackpot is not None and not df_jackpot.empty:
            fig, ax = plt.subplots(figsize=(10, 5))
            
            # Plotagem dos dados
            ax.plot(df_jackpot['data'], df_jackpot['jackpot_milhoes'], 
                   color='#FF4B4B', linewidth=2, marker='o', markersize=5)
            
            # --- AJUSTES DO EIXO X (DATAS) ---
            
            # 1. Definir limites exatos baseados no Filtro da Sidebar
            # (Converte para datetime para o matplotlib entender)
            ax.set_xlim(pd.to_datetime(d_inicio), pd.to_datetime(d_fim))
            
            # 2. Formatação da Data (Dia/Mês/Ano curto)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))
            
            # 3. Lógica para mostrar datas
            # Se tivermos poucos dados (menos de 30), forçamos mostrar TODAS as datas dos sorteios
            if len(df_jackpot) < 30:
                ax.set_xticks(df_jackpot['data'])
            else:
                # Se forem muitos, deixa automático mas garante que não sobrepõe
                ax.xaxis.set_major_locator(mdates.AutoDateLocator())

            # 4. Rotação de 45º e alinhamento à direita (para ficar embaixo do tracinho)
            plt.xticks(rotation=45, ha='right')
            
            # --- ESTÉTICA GERAL ---
            ax.set_ylabel("Milhões (€)")
            ax.set_title(f"Período: {d_inicio.strftime('%d/%m/%Y')} a {d_fim.strftime('%d/%m/%Y')}", fontsize=10, color='gray')
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("Sem dados de jackpot para exibir neste período.")

    with c_rank:
        st.subheader("🌍 Top premiação por país")
        premios = stats.get('premios_por_pais', {})
        if premios:
            df_paises = pd.DataFrame(list(premios.items()), columns=['País', 'Qtd']).sort_values('Qtd', ascending=True)
            st.dataframe(
                df_paises, 
                column_config={"Qtd": st.column_config.ProgressColumn("Vezes", format="%d", min_value=0, max_value=int(df_paises['Qtd'].max()))},
                hide_index=True,
                use_container_width=True
            )
        else:
            st.info("Sem dados de países.")

    st.divider()

    # 3. ÚLTIMOS SORTEIOS (Visual)
    st.subheader("📅 Últimos resultados")
    dados_visuais = obter_dados_ultimos_sorteios(loto)
    
    for d in dados_visuais:
        # Gera HTML das bolas
        html_princ = "".join([bola(n, "PRINCIPAL") for n in d['principais']])
        
        # Define tipo da complementar baseada na loteria
        tipo_comp = "COMPLEMENTAR" if nome_lot == "Euromilhões" else "UNICO"
        html_comp = "".join([bola(n, tipo_comp) for n in d['complementares']])
        
        tag_acumulou = '<span class="acumulou-tag">ACUMULOU!</span>' if d['acumulou'] else ""
        
        st.markdown(f"""
        <div class="sorteio-box">
            <div class="sorteio-data">{d['data_str']} • Concurso <b>{d['concurso']}</b> {tag_acumulou}</div>
            <div>{html_princ} <span style="margin:0 15px; color:#aaa;">|</span> {html_comp}</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # 4. ESTATÍSTICAS DETALHADAS (Abas)
    tab1, tab2, tab3 = st.tabs(["🔢 Frequência de números", "🔥 Combinações", "🔗 Sequências"])
    
    with tab1:
        c_mais, c_menos = st.columns(2)
        with c_mais:
            st.write("#### Mais sorteados")
            for n, qtd in stats.get('mais_frequentes_princ', [])[:5]:
                st.markdown(f"{bola(n)} saiu **{qtd}** vezes", unsafe_allow_html=True)
        with c_menos:
            st.write("#### Menos sorteados")
            for n, qtd in stats.get('menos_frequentes_princ', [])[:5]:
                st.markdown(f"{bola(n)} saiu **{qtd}** vezes", unsafe_allow_html=True)

    with tab2:
        # 1. Adicionada a opção "Quadras" na lista
        tipo = st.radio("Tipo de combinação", ["Duplas", "Trios", "Quadras"], horizontal=True)
        
        # 2. Mapeamento da escolha para a chave de dados correta
        mapa_chaves = {
            "Duplas": "duplas_repetidas",
            "Trios": "trios_repetidos",
            "Quadras": "quadras_repetidas"
        }
        chave = mapa_chaves[tipo]
        
        combos = stats.get(chave, [])
        
        if combos:
            st.write(f"#### {tipo} que mais se repetem")
            # Mostra o Top 5
            for c_nums, qtd in combos[:5]: 
                html_combo = "".join([bola(n) for n in c_nums])
                st.markdown(f"{html_combo} → **{qtd}x**", unsafe_allow_html=True)
        else:
            st.info(f"Nenhuma repetição de {tipo} encontrada neste período.")

    with tab3:
        seqs = stats.get('sequencias_consecutivas', [])
        if seqs:
            st.write("#### Sequências (ex: 1, 2, 3)")
            for s in seqs:
                # O formato vem do calculos_estatisticos: "Data | Concurso | 1 - 2 - 3"
                if "|" in s:
                    info, nums_str = s.rsplit("|", 1)
                    nums = [int(x) for x in nums_str.replace("-", " ").split() if x.isdigit()]
                    html_seq = "".join([bola(n) for n in nums])
                    st.markdown(f"<small>{info}</small><br>{html_seq}", unsafe_allow_html=True)
                else:
                    st.write(s)
        else:
            st.info("Nenhuma sequência consecutiva relevante encontrada.")