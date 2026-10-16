-- ============================================================================
-- PROJETO OLIST E-COMMERCE - POSTGRESQL
-- ARQUIVO: 03_business_analytics_kpis.sql
-- ETAPA: Consultas Analíticas Avançadas de Negócio
-- CONCEITOS: CTEs, Window Functions (LAG, NTILE, SUM OVER), Agregações e KPIs
-- AUTOR: Victor Ramos
-- ============================================================================

SET search_path TO olist, public;

-- ============================================================================
-- 1. CRESCIMENTO DE FATURAMENTO MÊS A MÊS (MoM % GROWTH)
-- Pergunta: Qual o histórico de receita mensal e a taxa de crescimento da Olist?
-- Técnica: CTE + Window Function LAG()
-- ============================================================================
WITH faturamento_mensal AS (
    SELECT 
        TO_CHAR(DATE_TRUNC('month', order_purchase_timestamp), 'YYYY-MM') AS ano_mes,
        COUNT(DISTINCT order_id) AS total_pedidos,
        ROUND(SUM(valor_item)::NUMERIC, 2) AS receita_produtos,
        ROUND(SUM(valor_total_item)::NUMERIC, 2) AS receita_total
    FROM olist.vw_pedidos_detalhados
    WHERE order_status = 'delivered'
    GROUP BY DATE_TRUNC('month', order_purchase_timestamp)
)
SELECT 
    ano_mes,
    total_pedidos,
    receita_total,
    LAG(receita_total, 1) OVER (ORDER BY ano_mes) AS receita_mes_anterior,
    ROUND(
        (receita_total - LAG(receita_total, 1) OVER (ORDER BY ano_mes)) 
        / LAG(receita_total, 1) OVER (ORDER BY ano_mes) * 100, 
        2
    ) AS crescimento_mom_percentual
FROM faturamento_mensal
ORDER BY ano_mes;


-- ============================================================================
-- 2. TOP 10 CATEGORIAS E PARTICIPAÇÃO NO FATURAMENTO TOTAL (% SHARE)
-- Pergunta: Quais categorias concentram o faturamento e qual a % de representatividade?
-- Técnica: Agrupamento + Window Function SUM() OVER ()
-- ============================================================================
WITH vendas_categorias AS (
    SELECT 
        categoria_produto,
        COUNT(DISTINCT order_id) AS total_pedidos,
        SUM(valor_item) AS receita_categoria
    FROM olist.vw_pedidos_detalhados
    WHERE order_status = 'delivered'
    GROUP BY categoria_produto
)
SELECT 
    categoria_produto,
    total_pedidos,
    ROUND(receita_categoria::NUMERIC, 2) AS faturamento,
    ROUND(
        (receita_categoria / SUM(receita_categoria) OVER ()) * 100, 
        2
    ) AS percentual_participacao_total
FROM vendas_categorias
ORDER BY faturamento DESC
LIMIT 10;


-- ============================================================================
-- 3. IMPACTO DE ATRASO LOGÍSTICO NA SATISFAÇÃO DO CLIENTE (REVIEW SCORE)
-- Pergunta: Quanto a nota de avaliação cai quando o pedido atrasa?
-- ============================================================================
SELECT 
    CASE 
        WHEN dias_atraso > 0 THEN 'Entrega com Atraso'
        ELSE 'Entrega no Prazo ou Antecipada'
    END AS status_logistico,
    COUNT(DISTINCT order_id) AS total_pedidos,
    ROUND(AVG(dias_para_entrega), 1) AS media_dias_transporte,
    ROUND(AVG(review_score), 2) AS nota_media_satisfacao,
    ROUND(
        (COUNT(CASE WHEN review_score = 5 THEN 1 END)::NUMERIC / COUNT(*)) * 100, 
        1
    ) AS percentual_nota_maxima,
    ROUND(
        (COUNT(CASE WHEN review_score = 1 THEN 1 END)::NUMERIC / COUNT(*)) * 100, 
        1
    ) AS percentual_nota_minima
FROM olist.vw_pedidos_detalhados
WHERE order_status = 'delivered' 
  AND review_score IS NOT NULL
GROUP BY 
    CASE 
        WHEN dias_atraso > 0 THEN 'Entrega com Atraso'
        ELSE 'Entrega no Prazo ou Antecipada'
    END;


-- ============================================================================
-- 4. SEGMENTAÇÃO RFM SIMPLIFICADA (RECÊNCIA, FREQUÊNCIA E VALOR MONETÁRIO)
-- Pergunta: Quem são nossos clientes mais fiéis e rentáveis (Clientes VIP)?
-- Técnica: CTEs + NTILE(4) para cálculo de quartis
-- ============================================================================
WITH metricas_cliente AS (
    SELECT 
        customer_unique_id,
        -- Recência: Dias desde a última compra até o fim do dataset (Outubro/2018)
        ROUND(
            EXTRACT(EPOCH FROM (DATE '2018-10-17' - MAX(order_purchase_timestamp))) / 86400
        ) AS recencia_dias,
        COUNT(DISTINCT order_id) AS frequencia_compras,
        SUM(valor_total_item) AS valor_monetario
    FROM olist.vw_pedidos_detalhados
    WHERE order_status = 'delivered'
    GROUP BY customer_unique_id
),
quartis_rfm AS (
    SELECT 
        customer_unique_id,
        recencia_dias,
        frequencia_compras,
        valor_monetario,
        -- R score invertido: quanto menos dias, melhor a nota
        NTILE(4) OVER (ORDER BY recencia_dias DESC) AS r_score,
        NTILE(4) OVER (ORDER BY frequencia_compras ASC) AS f_score,
        NTILE(4) OVER (ORDER BY valor_monetario ASC) AS m_score
    FROM metricas_cliente
)
SELECT 
    customer_unique_id,
    recencia_dias,
    frequencia_compras,
    ROUND(valor_monetario::NUMERIC, 2) AS valor_monetario,
    (r_score + f_score + m_score) AS pontuacao_total_rfm,
    CASE 
        WHEN (r_score + f_score + m_score) >= 10 THEN 'Cliente VIP / Ouro'
        WHEN (r_score + f_score + m_score) BETWEEN 7 AND 9 THEN 'Cliente Potencial'
        WHEN r_score <= 2 THEN 'Cliente em Risco / Churn'
        ELSE 'Cliente Ocasional'
    END AS segmento_cliente
FROM quartis_rfm
ORDER BY pontuacao_total_rfm DESC, valor_monetario DESC
LIMIT 50;


-- ============================================================================
-- 5. TOP 10 VENDEDORES MAIS PRODUTIVOS COM AVALIAÇÃO CONSISTENTE
-- Pergunta: Quais vendedores geram maior receita mantendo alta satisfação?
-- ============================================================================
SELECT 
    seller_id,
    seller_city,
    seller_state,
    COUNT(DISTINCT order_id) AS pedidos_atendidos,
    ROUND(SUM(valor_item)::NUMERIC, 2) AS faturamento_gerado,
    ROUND(AVG(review_score), 2) AS nota_media_vendedor
FROM olist.vw_pedidos_detalhados
WHERE order_status = 'delivered'
GROUP BY seller_id, seller_city, seller_state
HAVING COUNT(DISTINCT order_id) >= 50
ORDER BY faturamento_gerado DESC
LIMIT 10;
