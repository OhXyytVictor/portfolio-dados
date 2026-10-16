-- ==============================================================================
-- PROJETO: Pipeline e Analise de E-commerce Gamer
-- ARQUIVO: 04_prescriptive_gamer_shield.sql
-- AUTOR: Victor Ramos
-- OBJETIVO: View analitica prescritiva para o motor Gamer Shield (Camada de Sabedoria)
-- ==============================================================================

-- 1. Criacao da View Prescritiva do Gamer Shield
DROP VIEW IF EXISTS olist.vw_alertas_gamer_shield CASCADE;
CREATE VIEW olist.vw_alertas_gamer_shield AS
WITH pedidos_consolidados AS (
    SELECT 
        o.order_id,
        c.customer_unique_id,
        c.customer_city,
        c.customer_state,
        CASE 
            WHEN c.customer_state IN ('SP', 'RJ', 'MG', 'ES') THEN 'Sudeste'
            WHEN c.customer_state IN ('PR', 'SC', 'RS') THEN 'Sul'
            WHEN c.customer_state IN ('BA', 'PE', 'CE', 'MA', 'PB', 'RN', 'AL', 'SE', 'PI') THEN 'Nordeste'
            WHEN c.customer_state IN ('AM', 'PA', 'RO', 'AC', 'TO', 'AP', 'RR') THEN 'Norte'
            ELSE 'Centro-Oeste'
        END AS regiao_macro,
        p.product_category_name AS categoria,
        o.order_purchase_timestamp AS data_compra,
        o.order_delivered_carrier_date AS data_despacho,
        o.order_estimated_delivery_date AS data_estimada,
        o.order_delivered_customer_date AS data_entrega_real,
        oi.price AS preco_item,
        oi.freight_value AS valor_frete,
        ROUND((oi.price + oi.freight_value)::NUMERIC, 2) AS valor_total_pedido,
        -- Calculo de SLA em dias
        ROUND(EXTRACT(EPOCH FROM (o.order_delivered_customer_date - o.order_purchase_timestamp)) / 86400, 1) AS dias_transito_total,
        ROUND(EXTRACT(EPOCH FROM (o.order_delivered_customer_date - o.order_estimated_delivery_date)) / 86400, 1) AS dias_desvio_sla
    FROM olist.orders o
    JOIN olist.customers c ON o.customer_id = c.customer_id
    JOIN olist.order_items oi ON o.order_id = oi.order_id
    JOIN olist.products p ON oi.product_id = p.product_id
    WHERE p.product_category_name IN ('consoles_games', 'informatica_acessorios')
      AND o.order_status = 'delivered'
      AND o.order_delivered_customer_date IS NOT NULL
)
SELECT 
    order_id,
    customer_unique_id,
    customer_state,
    regiao_macro,
    categoria,
    data_compra,
    data_estimada,
    data_entrega_real,
    valor_total_pedido,
    valor_frete,
    dias_transito_total,
    dias_desvio_sla,
    -- Classificacao Prescritiva de Risco
    CASE 
        WHEN dias_desvio_sla > 0 THEN 'Risco Critico / Atrasado'
        WHEN dias_desvio_sla BETWEEN -2.0 AND 0 THEN 'Alerta Amarelo (Margem Estreita 48h)'
        ELSE 'Operacao Regular (No Prazo)'
    END AS status_gamer_shield,
    -- Acao Prescritiva Recomendada
    CASE 
        WHEN dias_desvio_sla > 0 THEN 'Disparo Proativo WhatsApp + Voucher R$ 30,00'
        WHEN dias_desvio_sla BETWEEN -2.0 AND 0 THEN 'Notificacao de Rastreamento Reforcada'
        ELSE 'Fluxo Padrao Sem Intervencao'
    END AS acao_prescritiva,
    -- Impacto Financeiro da Acao
    CASE 
        WHEN dias_desvio_sla > 0 THEN 30.00
        ELSE 0.00
    END AS custo_acao_voucher,
    CASE 
        WHEN dias_desvio_sla > 0 THEN valor_total_pedido
        ELSE 0.00
    END AS receita_protegida
FROM pedidos_consolidados;

-- 2. Consulta de Diagnostico de Impacto da Sabedoria Prescritiva
-- Consolida o volume de pedidos, custo do programa e receita protegida por regiao
SELECT 
    regiao_macro,
    COUNT(DISTINCT order_id) AS total_pedidos,
    SUM(CASE WHEN status_gamer_shield = 'Risco Critico / Atrasado' THEN 1 ELSE 0 END) AS pedidos_acionados_gamer_shield,
    ROUND(
        SUM(CASE WHEN status_gamer_shield = 'Risco Critico / Atrasado' THEN 1 ELSE 0 END)::NUMERIC 
        / COUNT(DISTINCT order_id) * 100, 
        2
    ) AS taxa_acionamento_pct,
    ROUND(SUM(custo_acao_voucher)::NUMERIC, 2) AS custo_total_vouchers,
    ROUND(SUM(receita_protegida)::NUMERIC, 2) AS receita_total_salvaguardada,
    ROUND(
        SUM(receita_protegida)::NUMERIC / NULLIF(SUM(custo_acao_voucher), 0), 
        2
    ) AS multiplicador_protecao_por_real
FROM olist.vw_alertas_gamer_shield
GROUP BY regiao_macro
ORDER BY pedidos_acionados_gamer_shield DESC;
