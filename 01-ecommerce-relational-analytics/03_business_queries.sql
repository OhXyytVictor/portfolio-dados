-- ============================================================================
-- PROJETO 01: MODELAGEM RELACIONAL E CONSULTAS ANALÍTICAS DE E-COMMERCE
-- ARQUIVO: 03_business_queries.sql
-- DESCRIÇÃO: Consultas SQL analíticas para responder perguntas de negócio.
-- CONCEITOS: JOINs, GROUP BY, CTEs, Window Functions (LAG, DENSE_RANK, SUM OVER), Views
-- AUTOR: Victor Ramos
-- ============================================================================

-- ============================================================================
-- 1. FATURAMENTO TOTAL, QUANTIDADE DE PEDIDOS E TICKET MÉDIO POR MÊS
-- Pergunta de negócio: Qual é o desempenho mensal de vendas e o ticket médio da loja?
-- ============================================================================
SELECT 
    TO_CHAR(p.data_pedido, 'YYYY-MM') AS mes,
    COUNT(DISTINCT p.pedido_id) AS total_pedidos,
    SUM(i.quantidade * i.preco_praticado) AS faturamento_bruto,
    ROUND(
        SUM(i.quantidade * i.preco_praticado) / COUNT(DISTINCT p.pedido_id), 
        2
    ) AS ticket_medio
FROM pedidos p
JOIN itens_pedido i ON p.pedido_id = i.pedido_id
WHERE p.status_pedido != 'Cancelado'
GROUP BY TO_CHAR(p.data_pedido, 'YYYY-MM')
ORDER BY mes ASC;


-- ============================================================================
-- 2. CRESCIMENTO MÊS A MÊS (MONTH-OVER-MONTH - MoM GROWTH)
-- Pergunta de negócio: Quanto o faturamento cresceu ou caiu percentualmente em relação ao mês anterior?
-- Técnica: Common Table Expression (CTE) + Window Function LAG()
-- ============================================================================
WITH faturamento_mensal AS (
    SELECT 
        TO_CHAR(p.data_pedido, 'YYYY-MM') AS mes,
        SUM(i.quantidade * i.preco_praticado) AS faturamento
    FROM pedidos p
    JOIN itens_pedido i ON p.pedido_id = i.pedido_id
    WHERE p.status_pedido != 'Cancelado'
    GROUP BY TO_CHAR(p.data_pedido, 'YYYY-MM')
)
SELECT 
    mes,
    faturamento AS faturamento_atual,
    LAG(faturamento, 1) OVER (ORDER BY mes) AS faturamento_mes_anterior,
    ROUND(
        (faturamento - LAG(faturamento, 1) OVER (ORDER BY mes)) 
        / LAG(faturamento, 1) OVER (ORDER BY mes) * 100, 
        2
    ) AS crescimento_mom_percentual
FROM faturamento_mensal
ORDER BY mes;


-- ============================================================================
-- 3. RANKING DOS PRODUTOS MAIS VENDIDOS DENTRO DE CADA CATEGORIA
-- Pergunta de negócio: Quais são os 2 produtos líderes de faturamento por categoria?
-- Técnica: Window Function DENSE_RANK() com PARTITION BY
-- ============================================================================
WITH vendas_por_produto AS (
    SELECT 
        c.nome_categoria,
        pr.nome_produto,
        SUM(ip.quantidade) AS total_unidades_vendidas,
        SUM(ip.quantidade * ip.preco_praticado) AS receita_total,
        DENSE_RANK() OVER (
            PARTITION BY c.nome_categoria 
            ORDER BY SUM(ip.quantidade * ip.preco_praticado) DESC
        ) AS ranking_categoria
    FROM itens_pedido ip
    JOIN produtos pr ON ip.produto_id = pr.produto_id
    JOIN categorias c ON pr.categoria_id = c.categoria_id
    JOIN pedidos ped ON ip.pedido_id = ped.pedido_id
    WHERE ped.status_pedido != 'Cancelado'
    GROUP BY c.nome_categoria, pr.nome_produto
)
SELECT 
    nome_categoria,
    ranking_categoria,
    nome_produto,
    total_unidades_vendidas,
    receita_total
FROM vendas_por_produto
WHERE ranking_categoria <= 2
ORDER BY nome_categoria, ranking_categoria;


-- ============================================================================
-- 4. FATURAMENTO ACUMULADO AO LONGO DO TEMPO (RUNNING TOTAL)
-- Pergunta de negócio: Como a receita total se acumula progressivamente a cada pedido realizado?
-- Técnica: Window Function SUM() OVER (ORDER BY ...)
-- ============================================================================
SELECT 
    p.pedido_id,
    p.data_pedido,
    c.nome AS cliente,
    SUM(ip.quantidade * ip.preco_praticado) AS valor_pedido,
    SUM(SUM(ip.quantidade * ip.preco_praticado)) OVER (
        ORDER BY p.data_pedido 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS faturamento_acumulado
FROM pedidos p
JOIN clientes c ON p.cliente_id = c.cliente_id
JOIN itens_pedido ip ON p.pedido_id = ip.pedido_id
WHERE p.status_pedido != 'Cancelado'
GROUP BY p.pedido_id, p.data_pedido, c.nome
ORDER BY p.data_pedido;


-- ============================================================================
-- 5. ANÁLISE DE CLIENTES E LIFETIME VALUE (LTV)
-- Pergunta de negócio: Quem são os clientes mais valiosos e qual o ticket médio de cada um?
-- ============================================================================
SELECT 
    c.cliente_id,
    c.nome AS cliente,
    c.cidade,
    c.estado,
    COUNT(DISTINCT p.pedido_id) AS total_compras,
    SUM(ip.quantidade * ip.preco_praticado) AS ltv_total,
    ROUND(
        SUM(ip.quantidade * ip.preco_praticado) / COUNT(DISTINCT p.pedido_id), 
        2
    ) AS ticket_medio_cliente,
    MAX(p.data_pedido) AS data_ultima_compra
FROM clientes c
JOIN pedidos p ON c.cliente_id = p.cliente_id
JOIN itens_pedido ip ON p.pedido_id = ip.pedido_id
WHERE p.status_pedido != 'Cancelado'
GROUP BY c.cliente_id, c.nome, c.cidade, c.estado
ORDER BY ltv_total DESC;


-- ============================================================================
-- 6. PARTICIPAÇÃO POR FORMA DE PAGAMENTO (SHARE OF WALLET)
-- Pergunta de negócio: Qual método de pagamento movimenta maior volume financeiro?
-- ============================================================================
SELECT 
    metodo_pagamento,
    COUNT(pagamento_id) AS total_transacoes,
    SUM(valor_pago) AS volume_financeiro,
    ROUND(
        (SUM(valor_pago) / SUM(SUM(valor_pago)) OVER ()) * 100, 
        2
    ) AS percentual_participacao
FROM pagamentos
WHERE status_pagamento = 'Aprovado'
GROUP BY metodo_pagamento
ORDER BY volume_financeiro DESC;


-- ============================================================================
-- 7. CRIAÇÃO DE UMA VIEW ANALÍTICA PARA SUPORTE A BI / DASHBOARDS
-- Objetivo: Facilitar o consumo de dados sumarizados por ferramentas como Power BI ou Metabase.
-- ============================================================================
CREATE OR REPLACE VIEW vw_resumo_desempenho_mensal AS
SELECT 
    TO_CHAR(p.data_pedido, 'YYYY-MM') AS ano_mes,
    cat.nome_categoria,
    COUNT(DISTINCT p.pedido_id) AS total_pedidos,
    SUM(ip.quantidade) AS unidades_vendidas,
    SUM(ip.quantidade * ip.preco_praticado) AS faturamento_total
FROM pedidos p
JOIN itens_pedido ip ON p.pedido_id = ip.pedido_id
JOIN produtos pr ON ip.produto_id = pr.produto_id
JOIN categorias cat ON pr.categoria_id = cat.categoria_id
WHERE p.status_pedido != 'Cancelado'
GROUP BY TO_CHAR(p.data_pedido, 'YYYY-MM'), cat.nome_categoria;

-- Testando a visualização da View:
SELECT * FROM vw_resumo_desempenho_mensal ORDER BY ano_mes DESC, faturamento_total DESC;
