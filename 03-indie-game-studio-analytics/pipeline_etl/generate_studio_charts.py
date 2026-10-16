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
    ax.legend(frameon=False, loc="upper right", fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle="--", alpha=0.3, color="#94a3b8")

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f"R$ {height:.0f}K",
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 4),
                        textcoords="offset points",
                        ha="center", va="bottom", fontsize=8.5, fontweight="bold")

    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)

    plt.title("P&L Comparativo: Escopo Focado (Neon Protocol) vs. Escopo Inflado (Aetheria)", 
              fontsize=11.5, fontweight="bold", pad=16, loc="left", color="#0f172a")

    output_path = os.path.join(OUTPUT_DIR, "01_pl_comparativo_jogos.png")
    plt.tight_layout()
    plt.savefig(output_path)
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

    # Destaque do Vale da Morte em maio/2026 (-R$ 38.4K)
    min_idx = df["saldo_k"].idxmin()
    min_val = df.loc[min_idx, "saldo_k"]
    ax.scatter([min_idx], [min_val], color="#ef4444", s=70, zorder=5)
    ax.annotate(f"Vale da Morte (Mai/2026)\nR$ {min_val:.1f}K (Insolvencia Iminente)",
                xy=(min_idx, min_val), xytext=(min_idx - 5, min_val + 120),
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

def main():
    set_minimal_style()
    conn = psycopg2.connect(DATABASE_URI)
    generate_chart_1(conn)
    generate_chart_2(conn)
    generate_chart_3(conn)
    conn.close()
    print("[INFO] Todos os graficos analiticos do estudio foram gerados com sucesso!")

if __name__ == "__main__":
    main()
