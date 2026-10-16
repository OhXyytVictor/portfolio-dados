-- ==============================================================================
-- PROJETO: Analise e Posicionamento Financeiro de Estudio Indie de Games
-- ARQUIVO: 02_views_financeiras.sql
-- AUTOR: Victor Ramos
-- OBJETIVO: Views semanticas de P&L por titulo e fluxo de caixa / burn rate mensal
-- ==============================================================================

-- 1. View de Demonstrativo de Resultados (P&L) Consolidado por Jogo
DROP VIEW IF EXISTS estudio_games.vw_pl_por_jogo CASCADE;
CREATE VIEW estudio_games.vw_pl_por_jogo AS
WITH dev_costs AS (
    SELECT 
        jogo_id,
        ROUND(SUM(custo_alocado)::NUMERIC, 2) AS custo_desenvolvimento
    FROM estudio_games.alocacao_desenvolvimento
    GROUP BY jogo_id
),
mkt_costs AS (
    SELECT 
        jogo_id,
        ROUND(SUM(valor_investido)::NUMERIC, 2) AS custo_marketing
    FROM estudio_games.despesas_marketing
    GROUP BY jogo_id
),
sales_metrics AS (
    SELECT 
        jogo_id,
        SUM(copias_vendidas) AS copias_totais_vendidas,
        ROUND(SUM(receita_bruta)::NUMERIC, 2) AS receita_bruta_total,
        ROUND(SUM(taxa_plataforma)::NUMERIC, 2) AS taxas_lojas_total,
        ROUND(SUM(receita_liquida)::NUMERIC, 2) AS receita_liquida_total
    FROM estudio_games.vendas_plataforma
    GROUP BY jogo_id
)
SELECT 
    j.jogo_id,
    j.titulo,
    j.genero,
    j.motor_grafico,
    j.status,
    COALESCE(s.copias_totais_vendidas, 0) AS copias_vendidas,
    COALESCE(d.custo_desenvolvimento, 0.00) AS custo_desenvolvimento,
    COALESCE(m.custo_marketing, 0.00) AS custo_marketing,
    (COALESCE(d.custo_desenvolvimento, 0.00) + COALESCE(m.custo_marketing, 0.00)) AS investimento_total,
    COALESCE(s.receita_bruta_total, 0.00) AS receita_bruta,
    COALESCE(s.taxas_lojas_total, 0.00) AS taxas_plataformas,
    COALESCE(s.receita_liquida_total, 0.00) AS receita_liquida,
    ROUND((COALESCE(s.receita_liquida_total, 0.00) - (COALESCE(d.custo_desenvolvimento, 0.00) + COALESCE(m.custo_marketing, 0.00)))::NUMERIC, 2) AS resultado_liquido,
    ROUND(
        (COALESCE(s.receita_liquida_total, 0.00) 
        / NULLIF(COALESCE(d.custo_desenvolvimento, 0.00) + COALESCE(m.custo_marketing, 0.00), 0))::NUMERIC, 
        2
    ) AS roi_multiplicador,
    ROUND(
        ((COALESCE(s.receita_liquida_total, 0.00) - (COALESCE(d.custo_desenvolvimento, 0.00) + COALESCE(m.custo_marketing, 0.00))) 
        / NULLIF(COALESCE(s.receita_liquida_total, 0.00), 0) * 100)::NUMERIC, 
        2
    ) AS margem_liquida_pct
FROM estudio_games.jogos j
LEFT JOIN dev_costs d ON j.jogo_id = d.jogo_id
LEFT JOIN mkt_costs m ON j.jogo_id = m.jogo_id
LEFT JOIN sales_metrics s ON j.jogo_id = s.jogo_id;

-- 2. View de Fluxo de Caixa Mensal, Burn Rate e Runway
DROP VIEW IF EXISTS estudio_games.vw_fluxo_caixa_mensal CASCADE;
CREATE VIEW estudio_games.vw_fluxo_caixa_mensal AS
WITH calendario_meses AS (
    SELECT DISTINCT ano_mes FROM estudio_games.custos_operacionais
),
folha_mes AS (
    SELECT 
        ano_mes,
        ROUND(SUM(custo_alocado)::NUMERIC, 2) AS total_folha
    FROM estudio_games.alocacao_desenvolvimento
    GROUP BY ano_mes
),
overhead_mes AS (
    SELECT 
        ano_mes,
        ROUND(SUM(valor)::NUMERIC, 2) AS total_overhead
    FROM estudio_games.custos_operacionais
    GROUP BY ano_mes
),
mkt_mes AS (
    SELECT 
        TO_CHAR(data_evento::DATE, 'YYYY-MM') AS ano_mes,
        ROUND(SUM(valor_investido)::NUMERIC, 2) AS total_marketing
    FROM estudio_games.despesas_marketing
    GROUP BY TO_CHAR(data_evento::DATE, 'YYYY-MM')
),
receita_mes AS (
    SELECT 
        ano_mes,
        ROUND(SUM(receita_liquida)::NUMERIC, 2) AS total_receita_liquida
    FROM estudio_games.vendas_plataforma
    GROUP BY ano_mes
),
consolidado AS (
    SELECT 
        c.ano_mes,
        COALESCE(r.total_receita_liquida, 0.00) AS receita_liquida,
        COALESCE(f.total_folha, 0.00) AS despesa_folha,
        COALESCE(o.total_overhead, 0.00) AS despesa_overhead,
        COALESCE(m.total_marketing, 0.00) AS despesa_marketing,
        (COALESCE(f.total_folha, 0.00) + COALESCE(o.total_overhead, 0.00) + COALESCE(m.total_marketing, 0.00)) AS burn_rate_mensal,
        (COALESCE(r.total_receita_liquida, 0.00) - (COALESCE(f.total_folha, 0.00) + COALESCE(o.total_overhead, 0.00) + COALESCE(m.total_marketing, 0.00))) AS resultado_liquido_mes
    FROM calendario_meses c
    LEFT JOIN folha_mes f ON c.ano_mes = f.ano_mes
    LEFT JOIN overhead_mes o ON c.ano_mes = o.ano_mes
    LEFT JOIN mkt_mes m ON c.ano_mes = m.ano_mes
    LEFT JOIN receita_mes r ON c.ano_mes = r.ano_mes
)
SELECT 
    ano_mes,
    receita_liquida,
    despesa_folha,
    despesa_overhead,
    despesa_marketing,
    burn_rate_mensal,
    resultado_liquido_mes,
    -- Saldo Acumulado de Caixa (Partindo de Aporte Inicial Angel de R$ 350.000,00)
    ROUND((350000.00 + SUM(resultado_liquido_mes) OVER (ORDER BY ano_mes))::NUMERIC, 2) AS saldo_caixa_projetado
FROM consolidado
ORDER BY ano_mes;
