# Análise de Loterias Portuguesas

Projeto em Python para estatísticas de loterias (Totoloto, Eurodreams, Euromilhões).

## Como Rodar
1. Instale dependências: `pip install -r requirements.txt`
2. Coloque `dados_loterias.xlsx` na raiz.
3. Rode `python app/main.py` para stats no console e PNGs (gráficos).

## Web App
Rode `streamlit run streamlit_app.py` para versão interativa (upload Excel, exibe stats/gráficos).

## Estrutura
- `modelos/`: Classes para Sorteio e Loterias.
- `servicos/`: Leitura, stats, curiosidades.
- `visualizacao/`: Gráficos com Matplotlib.
- `app/main.py`: Execução principal.

Dependências: pandas, openpyxl, matplotlib, seaborn.