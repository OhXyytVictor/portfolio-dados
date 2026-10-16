"""
==============================================================================
PROJETO: Analise e Posicionamento Financeiro de Estudio Indie de Games
ARQUIVO: 01_seed_studio_data.py
AUTOR: Victor Ramos
OBJETIVO: Geracao e ingestao da base relacional do estudio (24 meses de operacao)
==============================================================================
"""

import os
from datetime import datetime
import psycopg2
from sqlalchemy import create_engine, text
import pandas as pd
import numpy as np

DATABASE_URI = "postgresql://postgres:5336@localhost:5432/postgres"

def main():
    print("[INFO] Iniciando geracao de dados do Estudio Indie (Historico de 24 meses)...")
    engine = create_engine(DATABASE_URI)

    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS estudio_games;"))

    # 1. Tabela: Jogos
    jogos_data = [
        {
            "jogo_id": 1,
            "titulo": "Neon Protocol",
            "genero": "Roguelike Deckbuilder 2D",
            "motor_grafico": "Unity",
            "data_inicio_dev": "2024-11-01",
            "data_lancamento": "2025-08-15",
            "preco_base_usd": 14.99,
            "preco_base_brl": 44.90,
            "status": "Lancado"
        },
        {
            "jogo_id": 2,
            "titulo": "Aetheria: Chronicles of the Void",
            "genero": "Action RPG 3D / Metroidvania",
            "motor_grafico": "Unreal Engine 5",
            "data_inicio_dev": "2025-03-01",
            "data_lancamento": "2026-06-20",
            "preco_base_usd": 24.99,
            "preco_base_brl": 79.90,
            "status": "Lancado"
        },
        {
            "jogo_id": 3,
            "titulo": "Project Shift",
            "genero": "Tactical Roguelite 2.5D",
            "motor_grafico": "Unity",
            "data_inicio_dev": "2026-07-01",
            "data_lancamento": None,
            "preco_base_usd": 19.99,
            "preco_base_brl": 59.90,
            "status": "Em Desenvolvimento"
        }
    ]
    df_jogos = pd.DataFrame(jogos_data)
    df_jogos.to_sql("jogos", engine, schema="estudio_games", if_exists="replace", index=False)
    print(" [OK] Tabela estudio_games.jogos criada.")

    # 2. Tabela: Equipe de Colaboradores
    equipe_data = [
        {"colaborador_id": 1, "nome": "Lucas Silveira", "cargo": "Game Director / Lead Game Designer", "senioridade": "Senior", "salario_mensal": 9500.00, "data_admissao": "2024-11-01"},
        {"colaborador_id": 2, "nome": "Mariana Souza", "cargo": "Lead Programmer", "senioridade": "Senior", "salario_mensal": 10500.00, "data_admissao": "2024-11-01"},
        {"colaborador_id": 3, "nome": "Rodrigo Lima", "cargo": "Gameplay Programmer", "senioridade": "Pleno", "salario_mensal": 6800.00, "data_admissao": "2024-11-15"},
        {"colaborador_id": 4, "nome": "Camila Duarte", "cargo": "2D/3D Concept & Asset Artist", "senioridade": "Pleno", "salario_mensal": 6200.00, "data_admissao": "2024-11-01"},
        {"colaborador_id": 5, "nome": "Felipe Becker", "cargo": "Technical Artist & Animator", "senioridade": "Senior", "salario_mensal": 8800.00, "data_admissao": "2025-02-01"},
        {"colaborador_id": 6, "nome": "Beatriz Ramos", "cargo": "UI/UX & 2D Artist", "senioridade": "Junior", "salario_mensal": 4200.00, "data_admissao": "2025-01-10"},
        {"colaborador_id": 7, "nome": "Guilherme Prado", "cargo": "Sound Designer & Composer", "senioridade": "Pleno", "salario_mensal": 5500.00, "data_admissao": "2024-12-01"},
        {"colaborador_id": 8, "nome": "Juliana Mendes", "cargo": "Associate Producer & Community Manager", "senioridade": "Pleno", "salario_mensal": 5800.00, "data_admissao": "2025-04-01"},
        {"colaborador_id": 9, "nome": "Thiago Castro", "cargo": "QA Lead & Level Designer", "senioridade": "Pleno", "salario_mensal": 5000.00, "data_admissao": "2025-03-01"},
        {"colaborador_id": 10, "nome": "Andreia Fontes", "cargo": "Gameplay & Systems Programmer", "senioridade": "Junior", "salario_mensal": 4500.00, "data_admissao": "2025-08-01"}
    ]
    df_equipe = pd.DataFrame(equipe_data)
    df_equipe.to_sql("equipe_colaboradores", engine, schema="estudio_games", if_exists="replace", index=False)
    print(" [OK] Tabela estudio_games.equipe_colaboradores criada.")

    # 3. Tabela: Custos Operacionais Fixos Mensais (Novembro/2024 a Outubro/2026 - 24 meses)
    custos_fixos_lista = []
    custo_id = 1
    meses_str = pd.date_range(start="2024-11-01", end="2026-10-01", freq="MS").strftime("%Y-%m").tolist()

    for mes in meses_str:
        # Aluguel e infraestrutura física/coworking
        custos_fixos_lista.append({"custo_id": custo_id, "ano_mes": mes, "categoria": "Infraestrutura", "descricao": "Coworking e Escritorio Base", "valor": 4500.00})
        custo_id += 1
        # Licencas de software (Unity Pro, Unreal seat, JetBrains, Adobe, Jira, GitHub)
        licencas_val = 2800.00 if mes < "2025-06" else 3900.00
        custos_fixos_lista.append({"custo_id": custo_id, "ano_mes": mes, "categoria": "Software & Licencas", "descricao": "Licencas Unity, IDEs e Softwares de Arte", "valor": licencas_val})
        custo_id += 1
        # Servicos em nuvem, backup e repositorios (AWS, Perforce, Supabase)
        custos_fixos_lista.append({"custo_id": custo_id, "ano_mes": mes, "categoria": "Cloud & Servidores", "descricao": "Servidores de Build, Perforce e Backups", "valor": 1600.00})
        custo_id += 1
        # Contabilidade e Juridico
        custos_fixos_lista.append({"custo_id": custo_id, "ano_mes": mes, "categoria": "Juridico & Contabil", "descricao": "Assessoria Contabil e Juridica para Contratos", "valor": 2200.00})
        custo_id += 1
        # Hardware, devkits e reposicao
        hardware_val = 1500.00 if int(mes.split("-")[1]) % 3 == 0 else 400.00
        custos_fixos_lista.append({"custo_id": custo_id, "ano_mes": mes, "categoria": "Hardware & DevKits", "descricao": "Manutencao e Aquisicao de Equipamentos", "valor": hardware_val})
        custo_id += 1

    df_custos = pd.DataFrame(custos_fixos_lista)
    df_custos.to_sql("custos_operacionais", engine, schema="estudio_games", if_exists="replace", index=False)
    print(" [OK] Tabela estudio_games.custos_operacionais criada.")

    # 4. Tabela: Alocacao de Desenvolvimento (Horas e Folha Salarial por Jogo)
    alocacao_lista = []
    aloc_id = 1
    for mes in meses_str:
        dt_mes = datetime.strptime(mes, "%Y-%m")
        for colab in equipe_data:
            dt_adm = datetime.strptime(colab["data_admissao"], "%Y-%m-%d")
            if dt_mes < datetime(dt_adm.year, dt_adm.month, 1):
                continue

            salario = colab["salario_mensal"]

            # Regras de alocacao historica:
            # Jogo 1 (Neon Protocol): dev de nov/2024 a ago/2025.
            # Jogo 2 (Aetheria): dev de mar/2025 a jun/2026.
            # Jogo 3 (Project Shift): dev a partir de jul/2026.
            if mes < "2025-03":
                # Foco 100% no Jogo 1
                alocacao_lista.append({"alocacao_id": aloc_id, "ano_mes": mes, "colaborador_id": colab["colaborador_id"], "jogo_id": 1, "pct_dedicacao": 100.0, "custo_alocado": salario})
                aloc_id += 1
            elif "2025-03" <= mes <= "2025-08":
                # Transicao: Jogo 1 finalizando (polimento/QA) e Jogo 2 iniciando (prototipagem)
                alocacao_lista.append({"alocacao_id": aloc_id, "ano_mes": mes, "colaborador_id": colab["colaborador_id"], "jogo_id": 1, "pct_dedicacao": 40.0, "custo_alocado": salario * 0.4})
                aloc_id += 1
                alocacao_lista.append({"alocacao_id": aloc_id, "ano_mes": mes, "colaborador_id": colab["colaborador_id"], "jogo_id": 2, "pct_dedicacao": 60.0, "custo_alocado": salario * 0.6})
                aloc_id += 1
            elif "2025-09" <= mes <= "2026-06":
                # Jogo 2 em producao intensa
                alocacao_lista.append({"alocacao_id": aloc_id, "ano_mes": mes, "colaborador_id": colab["colaborador_id"], "jogo_id": 2, "pct_dedicacao": 90.0, "custo_alocado": salario * 0.9})
                aloc_id += 1
                # Manutencao/DLC leve do Jogo 1
                alocacao_lista.append({"alocacao_id": aloc_id, "ano_mes": mes, "colaborador_id": colab["colaborador_id"], "jogo_id": 1, "pct_dedicacao": 10.0, "custo_alocado": salario * 0.1})
                aloc_id += 1
            else:
                # A partir de jul/2026: Jogo 3 em desenvolvimento e suporte leve a Jogo 2
                alocacao_lista.append({"alocacao_id": aloc_id, "ano_mes": mes, "colaborador_id": colab["colaborador_id"], "jogo_id": 3, "pct_dedicacao": 85.0, "custo_alocado": salario * 0.85})
                aloc_id += 1
                alocacao_lista.append({"alocacao_id": aloc_id, "ano_mes": mes, "colaborador_id": colab["colaborador_id"], "jogo_id": 2, "pct_dedicacao": 15.0, "custo_alocado": salario * 0.15})
                aloc_id += 1

    df_aloc = pd.DataFrame(alocacao_lista)
    df_aloc.to_sql("alocacao_desenvolvimento", engine, schema="estudio_games", if_exists="replace", index=False)
    print(" [OK] Tabela estudio_games.alocacao_desenvolvimento criada.")

    # 5. Tabela: Despesas de Marketing e Divulgacao
    mkt_data = [
        # Jogo 1: Neon Protocol (Estrategia enxuta, focada em Steam Next Fest e criadores nicho)
        {"campanha_id": 1, "jogo_id": 1, "canal": "Steam Next Fest (Demo & Broadcast)", "fase": "Pre-Lancamento", "valor_investido": 12000.00, "data_evento": "2025-06-10"},
        {"campanha_id": 2, "jogo_id": 1, "canal": "Criadores de Conteudo e Youtubers de Roguelike", "fase": "Lancamento", "valor_investido": 18500.00, "data_evento": "2025-08-15"},
        {"campanha_id": 3, "jogo_id": 1, "canal": "Trailer de Lancamento e Redes Sociais", "fase": "Lancamento", "valor_investido": 8000.00, "data_evento": "2025-08-10"},
        {"campanha_id": 4, "jogo_id": 1, "canal": "Promocoes Sazonais Steam (Autumn/Winter Sales)", "fase": "Pos-Lancamento", "valor_investido": 6500.00, "data_evento": "2025-11-20"},

        # Jogo 2: Aetheria (Campanha inflada e dispersa, agencia externa, trailer cinematico caro)
        {"campanha_id": 5, "jogo_id": 2, "canal": "Agencia de PR Externa e Assessoria de Imprensa", "fase": "Pre-Lancamento", "valor_investido": 42000.00, "data_evento": "2026-01-15"},
        {"campanha_id": 6, "jogo_id": 2, "canal": "Trailer Cinematico CGI Terceirizado", "fase": "Pre-Lancamento", "valor_investido": 55000.00, "data_evento": "2026-04-10"},
        {"campanha_id": 7, "jogo_id": 2, "canal": "Campanha de Ads Pagos no Meta e Reddit", "fase": "Lancamento", "valor_investido": 38000.00, "data_evento": "2026-06-20"},
        {"campanha_id": 8, "jogo_id": 2, "canal": "Influenciadores de Variedade (Genericos)", "fase": "Lancamento", "valor_investido": 25000.00, "data_evento": "2026-06-25"},

        # Jogo 3: Project Shift (Pre-producao)
        {"campanha_id": 9, "jogo_id": 3, "canal": "Construcao de Pagina Steam e Teaser Inicial", "fase": "Pre-Lancamento", "valor_investido": 7000.00, "data_evento": "2026-09-01"}
    ]
    df_mkt = pd.DataFrame(mkt_data)
    df_mkt.to_sql("despesas_marketing", engine, schema="estudio_games", if_exists="replace", index=False)
    print(" [OK] Tabela estudio_games.despesas_marketing criada.")

    # 6. Tabela: Vendas e Receitas por Jogo e Plataforma
    vendas_lista = []
    venda_id = 1

    # Jogo 1: Lancado em 2025-08. Desempenho solido por 14 meses (ate out/2026).
    # Steam: 72% das vendas, Switch: 18%, Epic: 10%
    meses_jogo1 = pd.date_range(start="2025-08-01", end="2026-10-01", freq="MS").strftime("%Y-%m").tolist()
    # Curva de vendas: pico no mes 1 (14k copias), cauda longa estabilizada
    curva_jogo1 = [14200, 6800, 4200, 3100, 2600, 2100, 1800, 1500, 1300, 1100, 950, 850, 750, 700, 650]

    for idx, mes in enumerate(meses_jogo1):
        total_copias_mes = curva_jogo1[idx]
        # Distribuicao de plataformas
        dist = [("Steam", 0.72, 0.30), ("Nintendo Switch", 0.18, 0.30), ("Epic Games Store", 0.10, 0.12)]
        for plat, share, fee in dist:
            copias = int(total_copias_mes * share)
            # Ticket medio ponderado global em BRL (~R$ 42,00 considerando precos regionais e sales)
            preco_efetivo = 42.00 if idx < 3 else (36.00 if idx in [3, 4, 10] else 40.00)
            bruto = copias * preco_efetivo
            taxa_loja = bruto * fee
            liquido = bruto - taxa_loja
            vendas_lista.append({
                "venda_id": venda_id,
                "jogo_id": 1,
                "ano_mes": mes,
                "plataforma": plat,
                "copias_vendidas": copias,
                "preco_medio_praticado": preco_efetivo,
                "receita_bruta": round(bruto, 2),
                "taxa_plataforma": round(taxa_loja, 2),
                "receita_liquida": round(liquido, 2)
            })
            venda_id += 1

    # Jogo 2: Lancado em 2026-06. Desempenho abaixo do esperado (4 meses de vendas: jun a out/2026).
    meses_jogo2 = pd.date_range(start="2026-06-01", end="2026-10-01", freq="MS").strftime("%Y-%m").tolist()
    curva_jogo2 = [9200, 4800, 2900, 1800, 1300]

    for idx, mes in enumerate(meses_jogo2):
        total_copias_mes = curva_jogo2[idx]
        dist = [("Steam", 0.65, 0.30), ("PlayStation 5", 0.25, 0.30), ("Xbox Series", 0.10, 0.30)]
        for plat, share, fee in dist:
            copias = int(total_copias_mes * share)
            preco_efetivo = 79.90 if idx == 0 else 72.00
            bruto = copias * preco_efetivo
            taxa_loja = bruto * fee
            liquido = bruto - taxa_loja
            vendas_lista.append({
                "venda_id": venda_id,
                "jogo_id": 2,
                "ano_mes": mes,
                "plataforma": plat,
                "copias_vendidas": copias,
                "preco_medio_praticado": preco_efetivo,
                "receita_bruta": round(bruto, 2),
                "taxa_plataforma": round(taxa_loja, 2),
                "receita_liquida": round(liquido, 2)
            })
            venda_id += 1

    df_vendas = pd.DataFrame(vendas_lista)
    df_vendas.to_sql("vendas_plataforma", engine, schema="estudio_games", if_exists="replace", index=False)
    print(" [OK] Tabela estudio_games.vendas_plataforma criada.")

    print("\n[INFO] Todas as tabelas do estudo de games foram geradas e persistidas no PostgreSQL com sucesso!\n")

if __name__ == "__main__":
    main()
