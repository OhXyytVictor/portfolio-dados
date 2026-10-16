-- ==============================================================================
-- PROJETO: Analise e Posicionamento Financeiro de Estudio Indie de Games
-- ARQUIVO: 03_analise_posicionamento_estrategico.sql
-- AUTOR: Victor Ramos
-- OBJETIVO: Consultas analiticas de posicionamento de mercado e simulacao de ROI
-- ==============================================================================

-- 1. Comparativo de Eficiencia de Desenvolvimento: Motor Grafico e Complexidade
-- Revela a armadilha do escopo 3D vs a alta rentabilidade de sistemas 2D/rejogaveis
SELECT 
    j.titulo,
    j.genero,
    j.motor_grafico,
    j.status,
    p.custo_desenvolvimento,
    p.custo_marketing,
    p.investimento_total,
    p.copias_vendidas,
    p.receita_liquida,
    p.resultado_liquido,
    p.roi_multiplicador,
    p.margem_liquida_pct,
    -- Custo de Desenvolvimento por Copia Vendida
    ROUND((p.custo_desenvolvimento / NULLIF(p.copias_vendidas, 0))::NUMERIC, 2) AS custo_dev_por_copia,
    -- Receita Liquida Gerada por Real de Desenvolvimento Investido
    ROUND((p.receita_liquida / NULLIF(p.custo_desenvolvimento, 0))::NUMERIC, 2) AS retorno_por_real_dev
FROM estudio_games.vw_pl_por_jogo p
JOIN estudio_games.jogos j ON p.jogo_id = j.jogo_id
WHERE j.status = 'Lancado';

-- 2. Eficiencia de Canais de Divulgacao e Marketing
-- Analisa o custo por campanha e o perfil de alocacao (Nicho Organico vs Agencias/CGI)
SELECT 
    j.titulo,
    m.canal,
    m.fase,
    m.valor_investido,
    ROUND(
        (m.valor_investido / SUM(m.valor_investido) OVER (PARTITION BY m.jogo_id) * 100)::NUMERIC, 
        2
    ) AS pct_orcamento_mkt_jogo
FROM estudio_games.despesas_marketing m
JOIN estudio_games.jogos j ON m.jogo_id = j.jogo_id
ORDER BY j.jogo_id, m.valor_investido DESC;

-- 3. Analise de Runway e Sobrevivencia Operacional do Estudio
-- Avalia o saldo de caixa em outubro/2026, burn rate fixo e meses de sobrevida
WITH metricas_finais AS (
    SELECT 
        ano_mes,
        burn_rate_mensal,
        receita_liquida,
        saldo_caixa_projetado
    FROM estudio_games.vw_fluxo_caixa_mensal
    WHERE ano_mes = '2026-10'
)
SELECT 
    ano_mes,
    saldo_caixa_projetado AS caixa_disponivel_atual,
    burn_rate_mensal AS despesa_mensal_atual,
    receita_liquida AS receita_residual_atual,
    (burn_rate_mensal - receita_liquida) AS queima_liquida_mensal_projetada,
    -- Runway em meses caso a receita residual zere completamente
    ROUND((saldo_caixa_projetado / NULLIF(burn_rate_mensal, 0))::NUMERIC, 1) AS runway_meses_caixa_puro,
    -- Runway em meses considerando a queima liquida atual
    ROUND((saldo_caixa_projetado / NULLIF(burn_rate_mensal - receita_liquida, 0))::NUMERIC, 1) AS runway_meses_operacao_atual
FROM metricas_finais;
