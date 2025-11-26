<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🍀 Análise das loterias de Portugal</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            color: #333;
            margin: 0;
            padding: 20px;
            text-align: center;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .badges {
            margin: 20px 0;
        }
        .badges img {
            margin: 0 10px;
            height: 25px;
        }
        .demo-btn {
            display: inline-block;
            background-color: #4CAF50;
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 5px;
            font-size: 18px;
            margin: 20px 0;
            transition: background-color 0.3s;
        }
        .demo-btn:hover {
            background-color: #45a049;
        }
        footer {
            margin-top: 40px;
            font-size: 14px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🍀 Análise das loterias de Portugal</h1>
        
        <div class="badges">
            <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white" alt="Python">
            <img src="https://img.shields.io/badge/Streamlit-1.0%2B-orange?logo=streamlit&logoColor=white" alt="Streamlit">
            <img src="https://img.shields.io/badge/Deployed%20on-Streamlit-brightgreen?logo=streamlit&logoColor=white" alt="Streamlit">
        </div>
        
        <p>Um dashboard interativo desenvolvido em Python e Streamlit para análise estatística, visualização de tendências e histórico de sorteios das principais loterias de Portugal: Euromilhões, Totoloto e Eurodreams.</p>
        
        <h2>🚀 Acesse o Dashboard</h2>
        <a href="https://projeto-loterias.streamlit.app/" class="demo-btn" target="_blank">Abrir Análise! 📊</a>
        
        <footer>
            <p>⭐ Curtiu? Dê uma estrela no GitHub!</p>
            <p>#LoteriasPortugal #DataViz #Python</p>
        </footer>
    </div>
</body>
</html>

# 🍀 Análise das loterias de Portugal

Um dashboard interativo desenvolvido em **Python** e **Streamlit** para análise estatística, visualização de tendências e histórico de sorteios das principais loterias de Portugal: **Euromilhões**, **Totoloto** e **Eurodreams**.

        <div class="badges">
            <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white" alt="Python">
            <img src="https://img.shields.io/badge/Streamlit-1.0%2B-orange?logo=streamlit&logoColor=white" alt="Streamlit">
            <img src="https://img.shields.io/badge/Deployed%20on-Streamlit-brightgreen?logo=streamlit&logoColor=white" alt="Streamlit">
        </div>

## 📊 Funcionalidades

- **Dashboard interativo:** Visão geral com KPIs de sorteios, curiosidades, acumulações e jackpots.

- **Análise Estatística:**
  - Frequência de números (mais e menos sorteados).
  - Identificação de combinações repetidas (Duplas, Trios).
  - Detecção de sequências consecutivas.

- **Visualização de dados:**
  - Gráficos de evolução do Jackpot.
  - Ranking de países vencedores.
  - Representação visual das bolas sorteadas.

- **Filtros inteligentes:** Filtragem dinâmica por intervalo de datas e/ou sorteios.

- **Cache de dados:** Carregamento otimizado usando `st.cache_data` para alta performance.

## 🛠️ Tecnologias utilizadas

- **Frontend:** [Streamlit](https://streamlit.io/)
- **Manipulação de dados:** [Pandas](https://pandas.pydata.org/)
- **Visualização:** [Matplotlib](https://matplotlib.org/)
- **Excel engine:** OpenPyXL

## 📂 Estrutura do projeto

O projeto foi refatorado seguindo o padrão MVC (Model-View-Controller) adaptado para scripts de dados:

```text
├── 📂 modelos/             # Definição das classes (OOP)
│   ├── loteria_base.py     # Classe abstrata com regras de validação
│   ├── sorteio.py          # Dataclass imutável do Sorteio
│   ├── euromilhoes.py      # Regras específicas (5+2)
│   ├── totoloto.py         # Regras específicas (5+1)
│   └── eurodreams.py       # Regras específicas (6+1)
│
├── 📂 servicos/                  # Lógica de Negócio e I/O
│   ├── carregar_dados.py         # Leitura robusta de Excel/CSV
│   ├── validador.py              # Limpeza e Factory de objetos
│   ├── calculos_estatisticos.py  # Matemática e agregações
│   └── filtros.py                # Utilitários de filtro
│
├── 📂 visualizacao/        # Preparação de dados para UI
│   ├── visual_graficos.py  # Dados para Matplotlib
│   └── visual_tabelas.py   # Dados para tabelas HTML
│
├── 📂 imagens/             # Assets (Logos)
├── dados_loterias.xlsx     # Base de dados (Excel)
├── streamlit_app.py        # Aplicação principal (Entry Point)
└── requirements.txt        # Dependências

## **A melhorar para novas versões: aprimorar filtros e layout "mais bonito"**


