-- ============================================================================
-- PORTFÓLIO DE DADOS - PROJETO 01: E-COMMERCE ANALYTICS
-- AUTOR: Victor Ramos
-- SCRIPT UNIFICADO: DDL + SEED + CONSULTAS PRONTAS
-- ============================================================================

-- ============================================================================
-- PASSO 1: CRIAÇÃO DO SCHEMA E TABELAS (DDL)
-- ============================================================================

DROP VIEW IF EXISTS vw_resumo_desempenho_mensal CASCADE;
DROP TABLE IF EXISTS pagamentos CASCADE;
DROP TABLE IF EXISTS itens_pedido CASCADE;
DROP TABLE IF EXISTS pedidos CASCADE;
DROP TABLE IF EXISTS produtos CASCADE;
DROP TABLE IF EXISTS categorias CASCADE;
DROP TABLE IF EXISTS clientes CASCADE;

CREATE TABLE clientes (
    cliente_id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    cidade VARCHAR(80) NOT NULL,
    estado CHAR(2) NOT NULL,
    data_cadastro DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE categorias (
    categoria_id SERIAL PRIMARY KEY,
    nome_categoria VARCHAR(60) NOT NULL UNIQUE,
    descricao VARCHAR(255)
);

CREATE TABLE produtos (
    produto_id SERIAL PRIMARY KEY,
    categoria_id INT NOT NULL REFERENCES categorias(categoria_id) ON DELETE RESTRICT,
    nome_produto VARCHAR(120) NOT NULL,
    preco_unitario NUMERIC(10, 2) NOT NULL CHECK (preco_unitario > 0),
    estoque_atual INT NOT NULL DEFAULT 0 CHECK (estoque_atual >= 0),
    ativo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE pedidos (
    pedido_id SERIAL PRIMARY KEY,
    cliente_id INT NOT NULL REFERENCES clientes(cliente_id) ON DELETE RESTRICT,
    data_pedido TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status_pedido VARCHAR(20) NOT NULL DEFAULT 'Pendente' 
        CHECK (status_pedido IN ('Pendente', 'Processando', 'Enviado', 'Entregue', 'Cancelado'))
);

CREATE TABLE itens_pedido (
    item_id SERIAL PRIMARY KEY,
    pedido_id INT NOT NULL REFERENCES pedidos(pedido_id) ON DELETE CASCADE,
    produto_id INT NOT NULL REFERENCES produtos(produto_id) ON DELETE RESTRICT,
    quantidade INT NOT NULL CHECK (quantidade > 0),
    preco_praticado NUMERIC(10, 2) NOT NULL CHECK (preco_praticado > 0)
);

CREATE TABLE pagamentos (
    pagamento_id SERIAL PRIMARY KEY,
    pedido_id INT NOT NULL REFERENCES pedidos(pedido_id) ON DELETE CASCADE,
    metodo_pagamento VARCHAR(30) NOT NULL 
        CHECK (metodo_pagamento IN ('Cartão de Crédito', 'Boleto Bancário', 'PIX')),
    valor_pago NUMERIC(10, 2) NOT NULL CHECK (valor_pago > 0),
    status_pagamento VARCHAR(20) NOT NULL DEFAULT 'Aprovado'
        CHECK (status_pagamento IN ('Pendente', 'Aprovado', 'Recusado', 'Estornado')),
    data_pagamento TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_produtos_categoria ON produtos(categoria_id);
CREATE INDEX idx_pedidos_cliente ON pedidos(cliente_id);
CREATE INDEX idx_pedidos_data ON pedidos(data_pedido);


-- ============================================================================
-- PASSO 2: INSERÇÃO DOS DADOS REALISTAS (DML / SEED)
-- ============================================================================

INSERT INTO categorias (nome_categoria, descricao) VALUES
('Eletrônicos', 'Smartphones, notebooks e fones bluetooth'),
('Informática', 'Hardware, monitores e teclados mecânicos'),
('Móveis & Decoração', 'Cadeiras ergonômicas e mesas reguláveis'),
('Livros', 'Livros técnicos de dados e negócios');

INSERT INTO produtos (categoria_id, nome_produto, preco_unitario, estoque_atual, ativo) VALUES
(1, 'Smartphone Galaxy Ultra', 4299.00, 25, TRUE),
(1, 'Fone Bluetooth Noise Cancelling', 799.00, 60, TRUE),
(1, 'Smartwatch Fitness Tracker', 499.00, 40, TRUE),
(2, 'Monitor Ultrawide 34 Polegadas', 2199.00, 15, TRUE),
(2, 'Teclado Mecânico RGB Switch Brown', 389.90, 80, TRUE),
(2, 'Mouse Ergonômico Vertical', 189.90, 100, TRUE),
(2, 'SSD NVMe 1TB Gen4', 450.00, 120, TRUE),
(3, 'Cadeira de Escritório Ergonômica', 1250.00, 30, TRUE),
(3, 'Mesa Regulável com Ajuste Elétrico', 1950.00, 10, TRUE),
(4, 'Livro: Storytelling com Dados', 69.90, 50, TRUE),
(4, 'Livro: SQL para Análise de Dados', 89.90, 45, TRUE),
(4, 'Livro: Data Science para Negócios', 95.00, 35, TRUE);

INSERT INTO clientes (nome, email, cidade, estado, data_cadastro) VALUES
('Ana Clara Silveira', 'ana.silveira@email.com', 'São Paulo', 'SP', '2023-01-15'),
('Bruno Eduardo Souza', 'bruno.souza@email.com', 'Rio de Janeiro', 'RJ', '2023-02-10'),
('Camila Rodrigues', 'camila.rodrigues@email.com', 'Belo Horizonte', 'MG', '2023-03-05'),
('Diego Fernandes Lima', 'diego.lima@email.com', 'Curitiba', 'PR', '2023-03-22'),
('Eliana Moreira Costa', 'eliana.costa@email.com', 'Porto Alegre', 'RS', '2023-04-18'),
('Felipe Augusto Castro', 'felipe.castro@email.com', 'Campinas', 'SP', '2023-05-12'),
('Gabriela Mendes', 'gabriela.mendes@email.com', 'Salvador', 'BA', '2023-06-01'),
('Henrique Rocha', 'henrique.rocha@email.com', 'Recife', 'PE', '2023-07-14'),
('Isabela Pires', 'isabela.pires@email.com', 'Brasília', 'DF', '2023-08-20'),
('João Victor Martins', 'joao.martins@email.com', 'Florianópolis', 'SC', '2023-09-02');

INSERT INTO pedidos (cliente_id, data_pedido, status_pedido) VALUES
(1, '2024-01-10 14:30:00', 'Entregue'),
(2, '2024-01-15 11:20:00', 'Entregue'),
(3, '2024-01-22 18:45:00', 'Entregue'),
(4, '2024-02-05 09:15:00', 'Entregue'),
(1, '2024-02-14 16:00:00', 'Entregue'),
(5, '2024-02-20 20:10:00', 'Cancelado'),
(6, '2024-03-02 10:05:00', 'Entregue'),
(7, '2024-03-11 13:40:00', 'Entregue'),
(2, '2024-03-25 15:50:00', 'Entregue'),
(8, '2024-04-04 17:15:00', 'Entregue'),
(3, '2024-04-18 12:30:00', 'Entregue'),
(9, '2024-04-29 19:25:00', 'Entregue'),
(10, '2024-05-08 08:50:00', 'Entregue'),
(1, '2024-05-15 21:00:00', 'Entregue'),
(4, '2024-05-27 14:10:00', 'Processando');

INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_praticado) VALUES
(1, 1, 1, 4299.00), (1, 10, 1, 69.90),
(2, 4, 1, 2199.00), (2, 5, 1, 389.90),
(3, 8, 1, 1250.00),
(4, 2, 2, 799.00),
(5, 7, 2, 450.00), (5, 6, 1, 189.90),
(6, 1, 1, 4299.00),
(7, 9, 1, 1950.00), (7, 8, 1, 1250.00),
(8, 3, 1, 499.00),
(9, 7, 1, 450.00), (9, 11, 1, 89.90),
(10, 2, 1, 799.00), (10, 3, 1, 499.00),
(11, 4, 1, 2199.00),
(12, 10, 1, 69.90), (12, 11, 1, 89.90), (12, 12, 1, 95.00),
(13, 5, 1, 389.90), (13, 6, 1, 189.90),
(14, 9, 1, 1950.00),
(15, 1, 1, 4299.00);

INSERT INTO pagamentos (pedido_id, metodo_pagamento, valor_pago, status_pagamento) VALUES
(1, 'Cartão de Crédito', 4368.90, 'Aprovado'),
(2, 'PIX', 2588.90, 'Aprovado'),
(3, 'Cartão de Crédito', 1250.00, 'Aprovado'),
(4, 'Boleto Bancário', 1598.00, 'Aprovado'),
(5, 'PIX', 1089.90, 'Aprovado'),
(6, 'Cartão de Crédito', 4299.00, 'Recusado'),
(7, 'Cartão de Crédito', 3200.00, 'Aprovado'),
(8, 'PIX', 499.00, 'Aprovado'),
(9, 'PIX', 539.90, 'Aprovado'),
(10, 'Cartão de Crédito', 1298.00, 'Aprovado'),
(11, 'Cartão de Crédito', 2199.00, 'Aprovado'),
(12, 'Boleto Bancário', 254.80, 'Aprovado'),
(13, 'PIX', 579.80, 'Aprovado'),
(14, 'PIX', 1950.00, 'Aprovado'),
(15, 'Cartão de Crédito', 4299.00, 'Pendente');


-- ============================================================================
-- PASSO 3: CONSULTAS ANALÍTICAS DE NEGÓCIO (EXECUTE CADA UMA COM CTRL+ENTER)
-- ============================================================================

-- [CONSULTA 1] FATURAMENTO TOTAL E TICKET MÉDIO POR MÊS:
SELECT 
    TO_CHAR(p.data_pedido, 'YYYY-MM') AS mes,
    COUNT(DISTINCT p.pedido_id) AS total_pedidos,
    SUM(i.quantidade * i.preco_praticado) AS faturamento_bruto,
    ROUND(SUM(i.quantidade * i.preco_praticado) / COUNT(DISTINCT p.pedido_id), 2) AS ticket_medio
FROM pedidos p
JOIN itens_pedido i ON p.pedido_id = i.pedido_id
WHERE p.status_pedido != 'Cancelado'
GROUP BY TO_CHAR(p.data_pedido, 'YYYY-MM')
ORDER BY mes ASC;


-- [CONSULTA 2] CRESCIMENTO MÊS A MÊS (MoM %) USANDO WINDOW FUNCTION LAG():
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
    ROUND((faturamento - LAG(faturamento, 1) OVER (ORDER BY mes)) / LAG(faturamento, 1) OVER (ORDER BY mes) * 100, 2) AS crescimento_mom_percentual
FROM faturamento_mensal
ORDER BY mes;


-- [CONSULTA 3] TOP 2 PRODUTOS LÍDERES DE VENDAS POR CATEGORIA (DENSE_RANK):
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
SELECT * FROM vendas_por_produto WHERE ranking_categoria <= 2 ORDER BY nome_categoria, ranking_categoria;


-- [CONSULTA 4] ANÁLISE DE CLIENTES E LIFETIME VALUE (LTV):
SELECT 
    c.cliente_id,
    c.nome AS cliente,
    c.cidade,
    c.estado,
    COUNT(DISTINCT p.pedido_id) AS total_compras,
    SUM(ip.quantidade * ip.preco_praticado) AS ltv_total,
    ROUND(SUM(ip.quantidade * ip.preco_praticado) / COUNT(DISTINCT p.pedido_id), 2) AS ticket_medio_cliente
FROM clientes c
JOIN pedidos p ON c.cliente_id = p.cliente_id
JOIN itens_pedido ip ON p.pedido_id = ip.pedido_id
WHERE p.status_pedido != 'Cancelado'
GROUP BY c.cliente_id, c.nome, c.cidade, c.estado
ORDER BY ltv_total DESC;
