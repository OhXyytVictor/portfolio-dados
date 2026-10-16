"""
=============================================================================
GERADOR DE GRAFICOS COM STORYTELLING E DESIGN MINIMALISTA (PADRAO ALURA)
Aplica tecnicas de decluttering, cores com intencionalidade, titulos ativos
e eixos simplificados (K) para comunicacao executiva.
Autor: Victor Ramos
=============================================================================
"""

import os
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# -----------------------------------------------------------------------------
# Configuracoes Globais de Estilo e Consistencia Institucional
# -----------------------------------------------------------------------------
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'DejaVu Sans']
plt.rcParams['text.color'] = '#0F172A'
plt.rcParams['axes.labelcolor'] = '#475569'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'

COR_FUNDO = '#FFFFFF'
COR_TEXTO_TITULO = '#0F172A'
COR_TEXTO_SUBTITULO = '#475569'
COR_NEUTRA_PRINCIPAL = '#334155'  # Slate escuro institucional
COR_NEUTRA_SECUNDARIA = '#94A3B8' # Slate claro para contexto
COR_DESTAQUE_ALERTA = '#DC2626'   # Vermelho intencional para gargalos
COR_DESTAQUE_SUCESSO = '#2563EB'  # Azul sobrio institucional

IMG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs", "img"))
os.makedirs(IMG_DIR, exist_ok=True)

conn = psycopg2.connect(host='localhost', port=5432, dbname='postgres', user='postgres', password='5336')

# -----------------------------------------------------------------------------
# GRAFICO 1: Evolucao da Receita com Titulo Ativo e Destaque no Pico
# Storytelling: Menos e mais, eixos com 'K', chamada direta no ponto maximo
# -----------------------------------------------------------------------------
query_fat = """
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
df_fat = pd.read_sql(query_fat, conn)

fig, ax = plt.subplots(figsize=(10, 4.2), dpi=200)
fig.patch.set_facecolor(COR_FUNDO)
ax.set_facecolor(COR_FUNDO)

# Linha principal com cor institucional
ax.plot(df_fat['ano_mes'], df_fat['receita'], color=COR_NEUTRA_PRINCIPAL, linewidth=2.4, zorder=3)

# Identificacao automatica do pico de receita
idx_max = df_fat['receita'].idxmax()
pico_mes = df_fat.loc[idx_max, 'ano_mes']
pico_val = df_fat.loc[idx_max, 'receita']

# Ponto de destaque no pico
ax.scatter([pico_mes], [pico_val], color=COR_DESTAQUE_SUCESSO, s=60, zorder=4)

# Anotacao direta no pico (evitando que o leitor precise cruzar eixos)
ax.annotate(
    f'Pico Historico: R$ {pico_val/1000:.1f}K\n(Mai/2018)',
    xy=(pico_mes, pico_val),
    xytext=(15, 8),
    textcoords='offset points',
    fontsize=9,
    fontweight='bold',
    color=COR_DESTAQUE_SUCESSO,
    arrowprops=dict(arrowstyle='->', color=COR_DESTAQUE_SUCESSO, lw=1.2)
)

# Titulo orientativo (vende a mensagem imediatamente)
ax.set_title('Receita mensal atinge maturidade em 2018, estabilizando acima de R$ 80K',
             fontsize=12, fontweight='bold', pad=22, color=COR_TEXTO_TITULO, loc='left')
plt.suptitle('Consoles, Games e Perifericos de Informatica (Base Olist 2017-2018)',
             fontsize=9, color=COR_TEXTO_SUBTITULO, x=0.125, y=0.96, ha='left')

# Formatacao limpa dos eixos: sem zeros excessivos, usando sufixo K
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'R$ {int(y/1000)}K' if y > 0 else '0'))
ax.set_ylabel('')

# Remocao de ruidos visuais (decluttering)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#E2E8F0')
ax.spines['bottom'].set_color('#E2E8F0')
ax.grid(axis='y', linestyle=':', color='#E2E8F0', alpha=0.8, zorder=1)

# Reduzir labels do eixo X para evitar poluicao visual
plt.xticks(rotation=45, ha='right', fontsize=8.5)
plt.yticks(fontsize=8.5)
plt.tight_layout()

fat_path = os.path.join(IMG_DIR, "01_faturamento_mensal_games.png")
plt.savefig(fat_path, facecolor=COR_FUNDO, edgecolor='none', bbox_inches='tight')
plt.close()
print(f"[OK] Grafico 1 refinado: {fat_path}")


# -----------------------------------------------------------------------------
# GRAFICO 2: Impacto do Atraso na Satisfacao com Contraste Estrategico
# Storytelling: Cor neutra para o resultado normal, vermelho apenas para o problema
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.8, 4.0), dpi=200)
fig.patch.set_facecolor(COR_FUNDO)
ax.set_facecolor(COR_FUNDO)

categorias_entrega = ['No Prazo ou Antecipada\n(Media: 12,0 dias)', 'Com Atraso\n(Media: 33,1 dias)']
notas_avaliacao = [4.26, 2.65]
# Uso intencional de cores: neutro no normal, alerta no atraso
cores_barras = [COR_NEUTRA_PRINCIPAL, COR_DESTAQUE_ALERTA]

barras = ax.bar(categorias_entrega, notas_avaliacao, color=cores_barras, width=0.42, zorder=3)

# Titulo com conclusao clara
ax.set_title('Atrasos na entrega derrubam a satisfacao do cliente em 38%',
             fontsize=11.5, fontweight='bold', pad=22, color=COR_TEXTO_TITULO, loc='left')
plt.suptitle('Nota media de avaliacao de 1 a 5 estrelas em compras de consoles e games',
             fontsize=8.5, color=COR_TEXTO_SUBTITULO, x=0.125, y=0.96, ha='left')

# Rotulos diretos acima das barras (dispensa eixo Y)
for bar in barras:
    altura = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        altura + 0.12,
        f'{altura:.2f} / 5,00',
        ha='center',
        va='bottom',
        fontsize=10.5,
        fontweight='bold',
        color=COR_TEXTO_TITULO
    )

# Destaque da variacao percentual
ax.annotate(
    '-1,61 pontos\n(-38%)',
    xy=(0.5, 3.2),
    ha='center',
    fontsize=9,
    fontweight='bold',
    color=COR_DESTAQUE_ALERTA,
    bbox=dict(boxstyle='round,pad=0.5', facecolor='#FEF2F2', edgecolor='#FECACA', lw=1)
)

ax.set_ylim(0, 5.0)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_color('#E2E8F0')
ax.get_yaxis().set_visible(False) # Sem eixo Y poluindo
ax.tick_params(bottom=False)
plt.xticks(fontsize=9)
plt.tight_layout()

sat_path = os.path.join(IMG_DIR, "02_impacto_atraso_satisfacao.png")
plt.savefig(sat_path, facecolor=COR_FUNDO, edgecolor='none', bbox_inches='tight')
plt.close()
print(f"[OK] Grafico 2 refinado: {sat_path}")


# -----------------------------------------------------------------------------
# GRAFICO 3: Disparidade Regional de Frete com Cores por Desempenho
# Storytelling: Destacar regioes criticas (Norte/Nordeste) vs Sudeste
# -----------------------------------------------------------------------------
regioes = ['Sudeste', 'Sul', 'Nordeste', 'Norte']
prazos = [8.4, 11.8, 18.2, 24.5]
fretes = [16.80, 21.40, 34.90, 42.10]
# Cores: Sudeste/Sul neutros; Nordeste/Norte com atencao crescente
cores_regioes = [COR_NEUTRA_PRINCIPAL, COR_NEUTRA_PRINCIPAL, '#F97316', COR_DESTAQUE_ALERTA]

fig, (ax_dias, ax_frete) = plt.subplots(1, 2, figsize=(9.5, 3.8), dpi=200, sharey=True)
fig.patch.set_facecolor(COR_FUNDO)

# Grafico A: Dias medios
ax_dias.set_facecolor(COR_FUNDO)
barras_d = ax_dias.barh(regioes, prazos, color=cores_regioes, height=0.5, zorder=3)
ax_dias.set_title('Prazo Medio de Entrega (Dias)', fontsize=10, fontweight='bold', pad=12, loc='left')
ax_dias.spines['top'].set_visible(False)
ax_dias.spines['right'].set_visible(False)
ax_dias.spines['bottom'].set_visible(False)
ax_dias.spines['left'].set_color('#CBD5E1')
ax_dias.get_xaxis().set_visible(False)

for b in barras_d:
    w = b.get_width()
    ax_dias.text(w + 0.6, b.get_y() + b.get_height()/2, f'{w:.1f} dias', va='center', fontsize=8.5, fontweight='bold', color='#1E293B')

# Grafico B: Frete medio
ax_frete.set_facecolor(COR_FUNDO)
barras_f = ax_frete.barh(regioes, fretes, color=cores_regioes, height=0.5, zorder=3)
ax_frete.set_title('Custo Medio do Frete (R$)', fontsize=10, fontweight='bold', pad=12, loc='left')
ax_frete.spines['top'].set_visible(False)
ax_frete.spines['right'].set_visible(False)
ax_frete.spines['bottom'].set_visible(False)
ax_frete.spines['left'].set_visible(False)
ax_frete.get_xaxis().set_visible(False)
ax_frete.tick_params(left=False)

for b in barras_f:
    w = b.get_width()
    ax_frete.text(w + 1.0, b.get_y() + b.get_height()/2, f'R$ {w:.2f}', va='center', fontsize=8.5, fontweight='bold', color='#1E293B')

plt.suptitle('Disparidade Logistica: Norte e Nordeste pagam ate 2,5x mais de frete com o triplo do prazo',
             fontsize=11.5, fontweight='bold', x=0.08, y=1.03, ha='left', color=COR_TEXTO_TITULO)

plt.tight_layout()
reg_path = os.path.join(IMG_DIR, "03_sla_regional_frete.png")
plt.savefig(reg_path, facecolor=COR_FUNDO, edgecolor='none', bbox_inches='tight')
plt.close()
print(f"[OK] Grafico 3 refinado: {reg_path}")

conn.close()
print("\n[CONCLUIDO] Graficos refinados com tecnicas visuais de storytelling!")
