# Portfolio de Engenharia e Análise de Dados

**Autor:** Victor Ramos  
**Formação:** Jogos Digitais / Desenvolvimento de Games  
**Contato:** [LinkedIn](https://www.linkedin.com/in/victorramosbraga) | jsvramos@live.com  
**Foco:** Engenharia de Dados, Analytics Engineering e Modelagem Relacional SQL  

---

## Sobre o Repositório

Repositório dedicado a projetos práticos de engenharia e análise de dados. Aliando a formação em desenvolvimento de jogos ao estudo de arquitetura de dados e bancos relacionais, os projetos aqui documentados cobrem o ciclo completo de dados: ingestão (ETL), modelagem relacional, otimização de consultas e inteligência de negócios.

Cada projeto é documentado em três níveis de profundidade, refletindo as três camadas organizacionais:
1. **Visão Estratégica (5 a 10 min):** Diagnóstico de negócio estruturado nos 4 C's (Contexto, Conflito, Consequência, Conclusão) e business case com ROI direcionados a diretores e acionistas.
2. **Visão Tática (15 min):** Tabelas detalhadas de categorias, métricas de frete e planos de ação trimestrais direcionados a gestores de produto e operações.
3. **Visão Operacional (Deep Dive):** Diagramas de arquitetura, modelagem DER, scripts ETL em Python e consultas SQL avançadas com Window Functions.

---

## Tecnologias e Ferramentas

| Categoria | Tecnologias |
| :--- | :--- |
| **Bancos de Dados Relacionais** | PostgreSQL, SQLite |
| **Linguagens** | SQL (Dialeto PostgreSQL), Python 3 |
| **Bibliotecas e Drivers** | SQLAlchemy, Pandas, Psycopg2 |
| **Ambientes e Ferramentas** | DBeaver Community, Visual Studio Code |
| **Controle de Versão** | Git, GitHub |

---

## Projetos

| Projeto | Descrição | Principais Tópicos | Status | Link |
| :--- | :--- | :--- | :--- | :--- |
| **01. Pipeline e Análise de E-commerce Gamer** | Estudo de caso de transações reais com foco em consoles, games e periféricos. Pipeline ETL completo em Python e modelagem no PostgreSQL. | Python ETL, PostgreSQL, RFM NTILE, Window Functions, SLA Logístico | Concluído | [Acessar Projeto](./01-olist-ecommerce-analytics/) |
| **02. Pipeline Macroeconômico e Varejo de Tecnologia** | Ingestão automatizada de dados abertos do Banco Central (API REST) e IBGE (2000 a 2026), analisando ciclos cambiais, Selic e inflação. | REST API, PostgreSQL, Time Series, Window Functions, NTILE | Concluído | [Acessar Projeto](./02-dados-publicos-brasil/) |
| **03. Modelagem Relacional e Consultas SQL** | Modelagem relacional e queries analíticas simulando varejo tradicional. | DER, DDL, DML, CTEs, Views | Concluído | [Acessar Projeto](./01-ecommerce-relational-analytics/) |

---

## Como Executar Localmente

1. Clone o repositório:
   ```bash
   git clone https://github.com/OhXyytVictor/portfolio-dados.git
   ```
2. Acesse a pasta do projeto desejado:
   ```bash
   cd portfolio-dados/01-olist-ecommerce-analytics
   ```
3. Siga as instruções do README específico de cada projeto para instalar as dependências e executar os scripts.
