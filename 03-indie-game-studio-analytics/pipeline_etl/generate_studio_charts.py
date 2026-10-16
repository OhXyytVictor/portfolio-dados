"""
==============================================================================
PROJETO: Analise e Posicionamento Financeiro de Estudio Indie de Games
ARQUIVO: generate_studio_charts.py
AUTOR: Victor Ramos
OBJETIVO: Geracao automatizada de graficos minimalistas de storytelling
==============================================================================
"""

import os
import psycopg2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

OUTPUT_DIR = "03-indie-game-studio-analytics/docs/img"
os.makedirs(OUTPUT_DIR, exist_ok=True)

DATABASE_URI = "postgresql://postgres:5336@localhost:5432/postgres"

def set_minimal_style():
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["axes.edgecolor"] = "#cbd5e1"
    plt.rcParams["axes.linewidth"] = 0.8
    plt.rcParams["text.color"] = "#1e293b"
    plt.rcParams["axes.labelcolor"] = "#475569"
    plt.rcParams["xtick.color"] = "#64748b"
    plt.rcParams["ytick.color"] = "#64748b"
    plt.rcParams["figure.facecolor"] = "#ffffff"
    plt.rcParams["axes.facecolor"] = "#ffffff"

def generate_chart_1(conn):
    print("[INFO] Gerando Grafico 1: P&L Comparativo dos Jogos Lancados...")
    query = """
    SELECT 
        titulo,
        ROUND((investimento_total / 1000)::numeric, 1) as investimento_k,
        ROUND((receita_liquida / 1000)::numeric, 1) as receita_k,
        ROUND((resultado_liquido / 1000)::numeric, 1) as lucro_k
    FROM estudio_games.vw_pl_por_jogo
    WHERE status = 'Lancado'
    ORDER BY jogo_id;
    """
    df = pd.read_sql(query, conn)

    fig, ax = plt.subplots(figsize=(9, 4.5), dpi=200)

    x = np.arange(len(df["titulo"]))
    width = 0.25

    rects1 = ax.bar(x - width, df["investimento_k"], width, label="Investimento Total (Dev + Mkt)", color="#64748b")
    rects2 = ax.bar(x, df["receita_k"], width, label="Receita Liquida (Pos-Lojas)", color="#2563eb")
    rects3 = ax.bar(x + width, df["lucro_k"], width, label="Lucro Liquido Final", color="#10b981")

    ax.set_ylabel("Valores em Milhares de Reais (R$ K)", fontsize=10)
    ax.set_xticks(x)
    ax.set_xticklabels(["Neon Protocol (2D Roguelike)", "Aetheria (3D Action RPG)"], fontsize=10, fontweight="bold")
    ax.set_ylim(0, 1500)
    
    # Legenda horizontal no topo para evitar colisao com as barras
    ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, 1.12), ncol=3, fontsize=8.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle="--", alpha=0.3, color="#94a3b8")

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f"R$ {height:.0f}K",
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 5),
                        textcoords="offset points",
                        ha="center", va="bottom", fontsize=8.5, fontweight="bold")

    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)

    plt.title("P&L Comparativo: Escopo Focado (Neon Protocol) vs. Escopo Inflado (Aetheria)", 
              fontsize=11.5, fontweight="bold", pad=30, loc="left", color="#0f172a")

    output_path = os.path.join(OUTPUT_DIR, "01_pl_comparativo_jogos.png")
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    print(f" [PASS] Grafico 1 salvo em: {output_path}")

def generate_chart_2(conn):
    print("[INFO] Gerando Grafico 2: Evolucao do Saldo de Caixa e Vale da Morte...")
    query = """
    SELECT 
        ano_mes,
        ROUND((saldo_caixa_projetado / 1000)::numeric, 1) as saldo_k
    FROM estudio_games.vw_fluxo_caixa_mensal
    ORDER BY ano_mes;
    """
    df = pd.read_sql(query, conn)

    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=200)

    x_indices = range(len(df["ano_mes"]))
    ax.plot(x_indices, df["saldo_k"], color="#2563eb", linewidth=2.4, marker="o", markersize=4, label="Saldo de Caixa")
    ax.axhline(0, color="#ef4444", linestyle="--", linewidth=1.2, alpha=0.8, label="Linha de Insolvencia (R$ 0)")

    # Destaque do Ponto Mais Baixo de Caixa
    min_idx = df["saldo_k"].idxmin()
    min_val = df.loc[min_idx, "saldo_k"]
    min_mes = df.loc[min_idx, "ano_mes"]
    ax.scatter([min_idx], [min_val], color="#ef4444", s=70, zorder=5)
    ax.annotate(f"Ponto Mais Baixo ({min_mes})\nR$ {min_val:.1f}K (Pre-Lancamento)",
                xy=(min_idx, min_val), xytext=(min_idx - 5, min_val + 130),
                arrowprops=dict(facecolor="#ef4444", shrink=0.08, width=1.2, headwidth=6),
                fontsize=8.5, fontweight="bold", color="#dc2626")

    # Destaque do Pico de Caixa em out/2026 (R$ 660.5K)
    last_idx = len(df) - 1
    last_val = df.loc[last_idx, "saldo_k"]
    ax.annotate(f"Caixa Atual (Out/2026)\nR$ {last_val:.1f}K\nRunway: 8,3 Meses",
                xy=(last_idx, last_val), xytext=(last_idx - 4.5, last_val - 140),
                arrowprops=dict(facecolor="#2563eb", shrink=0.08, width=1.2, headwidth=6),
                fontsize=8.5, fontweight="bold", color="#1e40af")

    ax.set_ylabel("Saldo de Caixa Acumulado (R$ K)", fontsize=10)
    ax.set_xticks(x_indices[::3])
    ax.set_xticklabels(df["ano_mes"].iloc[::3], rotation=0, fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle="--", alpha=0.3, color="#94a3b8")
    ax.legend(frameon=False, loc="upper left", fontsize=9)

    plt.title("Evolucao do Saldo de Caixa do Estudio (24 Meses): O Risco de Ruptura de Caixa", 
              fontsize=11.5, fontweight="bold", pad=16, loc="left", color="#0f172a")

    output_path = os.path.join(OUTPUT_DIR, "02_evolucao_caixa_burn_rate.png")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f" [PASS] Grafico 2 salvo em: {output_path}")

def generate_chart_3(conn):
    print("[INFO] Gerando Grafico 3: Custo de Dev por Copia vs Margem Liquida...")
    query = """
    SELECT 
        titulo,
        ROUND((custo_desenvolvimento / copias_vendidas)::numeric, 2) as custo_por_copia,
        ROUND(margem_liquida_pct::numeric, 1) as margem_pct
    FROM estudio_games.vw_pl_por_jogo
    WHERE status = 'Lancado';
    """
    df = pd.read_sql(query, conn)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4), dpi=200)

    # Subplot 1: Custo por copia
    bars1 = ax1.bar(["Neon (2D)", "Aetheria (3D)"], df["custo_por_copia"], color=["#10b981", "#ef4444"], width=0.5)
    ax1.set_ylabel("Custo de Dev por Copia (R$)", fontsize=9)
    ax1.set_title("Custo de Dev por Copia Vendida", fontsize=10, fontweight="bold", color="#0f172a")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.grid(axis="y", linestyle="--", alpha=0.3)
    for b in bars1:
        h = b.get_height()
        ax1.text(b.get_x() + b.get_width()/2, h + 1, f"R$ {h:.2f}", ha="center", va="bottom", fontsize=8.5, fontweight="bold")
    ax1.set_ylim(0, 52)

    # Subplot 2: Margem liquida
    bars2 = ax2.bar(["Neon (2D)", "Aetheria (3D)"], df["margem_pct"], color=["#10b981", "#ef4444"], width=0.5)
    ax2.set_ylabel("Margem Liquida Final (%)", fontsize=9)
    ax2.set_title("Margem Liquida de Lucro", fontsize=10, fontweight="bold", color="#0f172a")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.grid(axis="y", linestyle="--", alpha=0.3)
    for b in bars2:
        h = b.get_height()
        ax2.text(b.get_x() + b.get_width()/2, h + 1.5, f"{h:.1f}%", ha="center", va="bottom", fontsize=8.5, fontweight="bold")
    ax2.set_ylim(0, 78)

    plt.suptitle("Disparidade de Eficiencia: A Armadilha de Custo do 3D vs. Rentabilidade do 2D", 
                 fontsize=11.5, fontweight="bold", y=1.03, color="#0f172a")

    output_path = os.path.join(OUTPUT_DIR, "03_custo_dev_vs_retorno_copia.png")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f" [PASS] Grafico 3 salvo em: {output_path}")

def generate_chart_4(conn):
    print("[INFO] Gerando Grafico 4: Decomposicao Detalhada de Gastos (Marketing, Salarios e Overhead)...")
    
    # 1. Marketing
    q_mkt = """
    SELECT 
        CASE 
            WHEN j.titulo LIKE '%Neon%' THEN 'Neon: ' || m.canal
            ELSE 'Aetheria: ' || m.canal
        END AS canal_label,
        m.valor_investido / 1000.0 AS valor_k,
        j.titulo
    FROM estudio_games.despesas_marketing m
    JOIN estudio_games.jogos j ON m.jogo_id = j.jogo_id
    WHERE j.status = 'Lancado'
    ORDER BY j.jogo_id ASC, m.valor_investido ASC;
    """
    df_mkt = pd.read_sql(q_mkt, conn)

    # 2. Folha
    q_folha = """
    SELECT 
        CASE 
            WHEN cargo LIKE '%Programmer%' THEN 'Engenharia / Codigo'
            WHEN cargo LIKE '%Artist%' OR cargo LIKE '%Animator%' THEN 'Arte e Animacao'
            WHEN cargo LIKE '%Director%' OR (cargo LIKE '%Designer%' AND cargo NOT LIKE '%Sound%' AND cargo NOT LIKE '%Level%') THEN 'Direcao e Game Design'
            WHEN cargo LIKE '%Producer%' OR cargo LIKE '%Community%' THEN 'Producao e Comunidade'
            ELSE 'Audio, QA e Level Design'
        END AS depto,
        SUM(salario_mensal) / 1000.0 AS folha_k,
        ROUND((SUM(salario_mensal) * 100.0 / (SELECT SUM(salario_mensal) FROM estudio_games.equipe_colaboradores))::numeric, 1) as pct
    FROM estudio_games.equipe_colaboradores
    GROUP BY 1
    ORDER BY folha_k ASC;
    """
    df_folha = pd.read_sql(q_folha, conn)

    # 3. Overhead
    q_over = """
    SELECT 
        categoria,
        SUM(valor) / 1000.0 AS total_k,
        ROUND((SUM(valor) * 100.0 / (SELECT SUM(valor) FROM estudio_games.custos_operacionais))::numeric, 1) as pct
    FROM estudio_games.custos_operacionais
    GROUP BY categoria
    ORDER BY total_k ASC;
    """
    df_over = pd.read_sql(q_over, conn)

    fig = plt.figure(figsize=(12, 9), dpi=200)
    gs = fig.add_gridspec(2, 2, height_ratios=[1.15, 1], hspace=0.42, wspace=0.55)

    # Subplot 1: Marketing (Topo inteiro)
    ax_mkt = fig.add_subplot(gs[0, :])
    colors_mkt = ["#2563eb" if "Neon" in lbl else "#ef4444" for lbl in df_mkt["canal_label"]]
    bars_mkt = ax_mkt.barh(df_mkt["canal_label"], df_mkt["valor_k"], color=colors_mkt, height=0.6)
    ax_mkt.set_xlim(0, 72)
    ax_mkt.set_xlabel("Valor Investido em Campanha (R$ K)", fontsize=9, labelpad=6)
    ax_mkt.set_title("1. Destrinchamento de Marketing: Canais Eficientes (Azul / Neon) vs. Dispersao de Alto Custo (Vermelho / Aetheria)", 
                     fontsize=10.5, fontweight="bold", loc="left", pad=10, color="#0f172a")
    ax_mkt.spines["top"].set_visible(False)
    ax_mkt.spines["right"].set_visible(False)
    ax_mkt.grid(axis="x", linestyle="--", alpha=0.3)
    for b in bars_mkt:
        w = b.get_width()
        ax_mkt.text(w + 1.2, b.get_y() + b.get_height()/2, f"R$ {w:.1f}K", 
                    va="center", ha="left", fontsize=8.5, fontweight="bold", color="#1e293b")

    # Subplot 2: Folha Salarial (Inferior Esquerdo)
    ax_folha = fig.add_subplot(gs[1, 0])
    bars_folha = ax_folha.barh(df_folha["depto"], df_folha["folha_k"], color="#3b82f6", height=0.55)
    ax_folha.set_xlim(0, 32)
    ax_folha.set_xlabel("Folha Salarial Mensal (R$ K)", fontsize=8.5, labelpad=6)
    ax_folha.set_title("2. Salarios por Departamento (R$ 66,8K/mes)", 
                       fontsize=9.5, fontweight="bold", loc="left", pad=10, color="#0f172a")
    ax_folha.spines["top"].set_visible(False)
    ax_folha.spines["right"].set_visible(False)
    ax_folha.grid(axis="x", linestyle="--", alpha=0.3)
    for b, pct in zip(bars_folha, df_folha["pct"]):
        w = b.get_width()
        ax_folha.text(w + 0.6, b.get_y() + b.get_height()/2, f"R$ {w:.1f}K ({pct}%)", 
                     va="center", ha="left", fontsize=8, fontweight="bold", color="#1e293b")

    # Subplot 3: Overhead Operacional (Inferior Direito)
    ax_over = fig.add_subplot(gs[1, 1])
    bars_over = ax_over.barh(df_over["categoria"], df_over["total_k"], color="#64748b", height=0.55)
    ax_over.set_xlim(0, 145)
    ax_over.set_xlabel("Custo Acumulado em 24 Meses (R$ K)", fontsize=8.5, labelpad=6)
    ax_over.set_title("3. Contas Fixas e Infraestrutura (Total R$ 303,5K)", 
                      fontsize=9.5, fontweight="bold", loc="left", pad=10, color="#0f172a")
    ax_over.spines["top"].set_visible(False)
    ax_over.spines["right"].set_visible(False)
    ax_over.grid(axis="x", linestyle="--", alpha=0.3)
    for b, pct in zip(bars_over, df_over["pct"]):
        w = b.get_width()
        ax_over.text(w + 2.5, b.get_y() + b.get_height()/2, f"R$ {w:.1f}K ({pct}%)", 
                    va="center", ha="left", fontsize=8, fontweight="bold", color="#1e293b")

    plt.suptitle("Decomposicao Granular dos Gastos do Estudio: Marketing, Equipe e Infraestrutura", 
                 fontsize=12, fontweight="bold", y=0.98, color="#0f172a")

    output_path = os.path.join(OUTPUT_DIR, "04_decomposicao_gastos_destrinchados.png")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    print(f" [PASS] Grafico 4 salvo em: {output_path}")

def main():
    set_minimal_style()
    conn = psycopg2.connect(DATABASE_URI)
    generate_chart_1(conn)
    generate_chart_2(conn)
    generate_chart_3(conn)
    generate_chart_4(conn)
    conn.close()
    print("[INFO] Todos os graficos analiticos do estudio foram gerados com sucesso!")

if __name__ == "__main__":
    main()

