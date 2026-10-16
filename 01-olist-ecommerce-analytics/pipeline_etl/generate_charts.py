"""
=============================================================================
GERADOR DE GRAFICOS ANALITICOS MINIMALISTAS
Gera figuras de alta resolucao para a documentacao do projeto.
Autor: Victor Ramos
=============================================================================
"""

import os
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Estilo minimalista e sofisticado
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8

IMG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs", "img"))
os.makedirs(IMG_DIR, exist_ok=True)

conn = psycopg2.connect(host='localhost', port=5432, dbname='postgres', user='postgres', password='5336')

# -----------------------------------------------------------------------------
# 1. GRAFICO: Faturamento Mensal do Segmento Gamer / Perifericos
# -----------------------------------------------------------------------------
query_faturamento = """
SELECT 
    TO_CHAR(DATE_TRUNC('month', o.order_purchase_timestamp), 'YYYY-MM') AS ano_mes,
    ROUND(SUM(oi.price)::numeric, 2) AS receita
FROM olist.orders o
JOIN olist.order_items oi ON o.order_id = oi.order_id
JOIN olist.products p ON oi.product_id = p.product_id
WHERE p.product_category_name IN ('consoles_games', 'informatica_acessorios')
  AND o.order_status = 'delivered'
  AND o.order_purchase_timestamp >= '2017-01-01'
  AND o.order_purchase_timestamp < '2018-09-01'
GROUP BY DATE_TRUNC('month', o.order_purchase_timestamp)
ORDER BY ano_mes;
"""
df_fat = pd.read_sql(query_faturamento, conn)

fig, ax = plt.subplots(figsize=(10, 4.5), dpi=200)
fig.patch.set_facecolor('#FAFAFA')
ax.set_facecolor('#FAFAFA')

ax.plot(df_fat['ano_mes'], df_fat['receita'] / 1000, color='#1E293B', linewidth=2.2, marker='o', markersize=4, label='Receita Mensal (R$ mil)')
ax.fill_between(df_fat['ano_mes'], df_fat['receita'] / 1000, color='#3B82F6', alpha=0.1)

ax.set_title('Evolucao da Receita Mensal: Consoles, Games e Perifericos (2017 - 2018)', fontsize=12, fontweight='bold', pad=15, color='#0F172A', loc='left')
ax.set_ylabel('Faturamento (R$ mil)', fontsize=10, color='#475569')
ax.grid(axis='y', linestyle='--', alpha=0.5, color='#CBD5E1')
ax.set_axisbelow(True)
plt.xticks(rotation=45, ha='right', fontsize=8, color='#475569')
plt.yticks(fontsize=9, color='#475569')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()

fat_path = os.path.join(IMG_DIR, "01_faturamento_mensal_games.png")
plt.savefig(fat_path, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()
print(f"[OK] Gerado: {fat_path}")


# -----------------------------------------------------------------------------
# 2. GRAFICO: Impacto de Atrasos na Nota de Avaliacao
# -----------------------------------------------------------------------------
status = ['No Prazo / Antecipada\n(12,0 dias médios)', 'Com Atraso\n(33,1 dias médios)']
notas = [4.26, 2.65]
cores = ['#2563EB', '#DC2626']

fig, ax = plt.subplots(figsize=(6.5, 4.2), dpi=200)
fig.patch.set_facecolor('#FAFAFA')
ax.set_facecolor('#FAFAFA')

bars = ax.bar(status, notas, color=cores, width=0.45, edgecolor='none')

ax.set_title('Impacto do Atraso de Entrega na Satisfacao do Cliente', fontsize=11, fontweight='bold', pad=15, color='#0F172A', loc='left')
ax.set_ylabel('Nota Media de Avaliacao (1 a 5)', fontsize=9, color='#475569')
ax.set_ylim(0, 5)
ax.grid(axis='y', linestyle='--', alpha=0.5, color='#CBD5E1')
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 0.15, f'{yval:.2f} / 5.00', ha='center', va='bottom', fontsize=10, fontweight='bold', color='#0F172A')

ax.text(0.5, 3.4, '-38% de queda na avaliacao', ha='center', fontsize=9, color='#DC2626', fontweight='semibold', bbox=dict(boxstyle='round,pad=0.4', facecolor='#FEE2E2', edgecolor='#FCA5A5', alpha=0.8))

plt.tight_layout()
sat_path = os.path.join(IMG_DIR, "02_impacto_atraso_satisfacao.png")
plt.savefig(sat_path, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()
print(f"[OK] Gerado: {sat_path}")


# -----------------------------------------------------------------------------
# 3. GRAFICO: Disparidade Regional de Frete e Prazos
# -----------------------------------------------------------------------------
regioes = ['Sudeste', 'Sul', 'Nordeste', 'Norte']
dias = [8.4, 11.8, 18.2, 24.5]
fretes = [16.80, 21.40, 34.90, 42.10]

fig, ax1 = plt.subplots(figsize=(8, 4.2), dpi=200)
fig.patch.set_facecolor('#FAFAFA')
ax1.set_facecolor('#FAFAFA')

x = range(len(regioes))
width = 0.35

rects1 = ax1.bar([i - width/2 for i in x], dias, width, label='Prazo Medio (Dias)', color='#1E293B')
ax2 = ax1.twinx()
rects2 = ax2.bar([i + width/2 for i in x], fretes, width, label='Frete Medio (R$)', color='#64748B')

ax1.set_title('Disparidade Logistica: Prazo de Entrega vs Custo de Frete por Regiao', fontsize=11, fontweight='bold', pad=15, color='#0F172A', loc='left')
ax1.set_xticks(x)
ax1.set_xticklabels(regioes, fontsize=9, color='#0F172A')
ax1.set_ylabel('Dias para Entrega', color='#1E293B', fontsize=9)
ax2.set_ylabel('Valor do Frete (R$)', color='#64748B', fontsize=9)
ax1.grid(axis='y', linestyle='--', alpha=0.4, color='#CBD5E1')
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)

for r in rects1:
    h = r.get_height()
    ax1.text(r.get_x() + r.get_width()/2, h + 0.5, f'{h:.1f}d', ha='center', fontsize=8, color='#1E293B', fontweight='bold')

for r in rects2:
    h = r.get_height()
    ax2.text(r.get_x() + r.get_width()/2, h + 0.8, f'R${h:.1f}', ha='center', fontsize=8, color='#64748B', fontweight='bold')

fig.legend(loc='upper right', bbox_to_anchor=(0.9, 0.95), frameon=False, fontsize=8)
plt.tight_layout()

reg_path = os.path.join(IMG_DIR, "03_sla_regional_frete.png")
plt.savefig(reg_path, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()
print(f"[OK] Gerado: {reg_path}")

conn.close()
print("[SUCESSO] Todos os graficos gerados com sucesso!")
