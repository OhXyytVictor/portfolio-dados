-- ============================================================================
-- PROJETO OLIST E-COMMERCE - POSTGRESQL
-- ARQUIVO: 02_analytical_views.sql
-- ETAPA: Criação de Views Analíticas Consolidadas para BI / Dashboards
-- AUTOR: Victor Ramos
-- ============================================================================

SET search_path TO olist, public;

-- ============================================================================
-- 1. VIEW CONSOLIDADA DE ITENS DE PEDIDOS (CAMADA ANALÍTICA)
-- Une pedido, cliente, produto, categoria traduzida, vendedor e avaliações.
-- ============================================================================
CREATE OR REPLACE VIEW olist.vw_pedidos_detalhados AS
SELECT 
    o.order_id,
    o.customer_id,
    c.customer_unique_id,
    c.customer_city,
    c.customer_state,
    o.order_status,
    o.order_purchase_timestamp,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,
    -- Cálculo de dias para entrega real vs estimada
    ROUND(
        (EXTRACT(EPOCH FROM (o.order_delivered_customer_date - o.order_purchase_timestamp)) / 86400)::NUMERIC, 
        1
    ) AS dias_para_entrega,
    ROUND(
        (EXTRACT(EPOCH FROM (o.order_delivered_customer_date - o.order_estimated_delivery_date)) / 86400)::NUMERIC, 
        1
    ) AS dias_atraso,
    oi.order_item_id,
    oi.product_id,
    COALESCE(tr.product_category_name_english, p.product_category_name, 'Outros') AS categoria_produto,
    oi.seller_id,
    s.seller_city,
    s.seller_state,
    oi.price AS valor_item,
    oi.freight_value AS valor_frete,
    (oi.price + oi.freight_value) AS valor_total_item,
    r.review_score
FROM olist.orders o
JOIN olist.customers c ON o.customer_id = c.customer_id
JOIN olist.order_items oi ON o.order_id = oi.order_id
LEFT JOIN olist.products p ON oi.product_id = p.product_id
LEFT JOIN olist.category_name_translation tr ON p.product_category_name = tr.product_category_name
LEFT JOIN olist.sellers s ON oi.seller_id = s.seller_id
LEFT JOIN (
    -- Subquery para pegar a nota média se houver mais de um review por pedido
    SELECT order_id, ROUND(AVG(review_score), 1) AS review_score
    FROM olist.order_reviews
    GROUP BY order_id
) r ON o.order_id = r.order_id;


-- ============================================================================
-- 2. VIEW DE PERFORMANCE E SLA LOGÍSTICO POR ESTADO (DESTINO)
-- Avalia tempo médio de trânsito e pontualidade por UF de entrega.
-- ============================================================================
CREATE OR REPLACE VIEW olist.vw_sla_logistico_uf AS
SELECT 
    customer_state AS estado_destino,
    COUNT(DISTINCT order_id) AS total_pedidos_entregues,
    ROUND(AVG(dias_para_entrega)::NUMERIC, 1) AS media_dias_entrega,
    ROUND(AVG(valor_frete)::NUMERIC, 2) AS frete_medio,
    ROUND(
        (COUNT(CASE WHEN dias_atraso > 0 THEN 1 END)::NUMERIC / COUNT(DISTINCT order_id)) * 100, 
        2
    ) AS percentual_pedidos_com_atraso,
    ROUND(AVG(review_score)::NUMERIC, 2) AS media_avaliacao
FROM olist.vw_pedidos_detalhados
WHERE order_status = 'delivered' 
  AND dias_para_entrega IS NOT NULL
GROUP BY customer_state
ORDER BY percentual_pedidos_com_atraso DESC;
