-- ============================================================================
-- PROJETO 01: MODELAGEM RELACIONAL E CONSULTAS ANALÍTICAS DE E-COMMERCE
-- ARQUIVO: 02_seed_data.sql
-- DESCRIÇÃO: Inserção de dados de exemplo consistentes e realistas.
-- SGBD: PostgreSQL (versão 14+)
-- AUTOR: Victor Ramos
-- ============================================================================

-- 1. CATEGORIAS
INSERT INTO categorias (nome_categoria, descricao) VALUES
('Eletrônicos', 'Smartphones, notebooks, fones de ouvido e acessórios eletrônicos'),
('Informática', 'Hardware, monitores, teclados mecânicos e periféricos para PC'),
('Móveis & Decoração', 'Cadeiras ergonômicas, mesas de escritório e estantes'),
('Livros', 'Livros técnicos de computação, dados, negócios e literatura');

-- 2. PRODUTOS
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

-- 3. CLIENTES
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

-- 4. PEDIDOS (Distribuídos em meses para permitir análise temporal MoM)
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

-- 5. ITENS DOS PEDIDOS
INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_praticado) VALUES
-- Pedido 1 (Ana Clara)
(1, 1, 1, 4299.00), -- Smartphone
(1, 10, 1, 69.90),  -- Livro Storytelling
-- Pedido 2 (Bruno Souza)
(2, 4, 1, 2199.00), -- Monitor
(2, 5, 1, 389.90),  -- Teclado
-- Pedido 3 (Camila)
(3, 8, 1, 1250.00), -- Cadeira
-- Pedido 4 (Diego)
(4, 2, 2, 799.00),  -- 2 Fones
-- Pedido 5 (Ana Clara)
(5, 7, 2, 450.00),  -- 2 SSDs
(5, 6, 1, 189.90),  -- 1 Mouse
-- Pedido 6 (Eliana - Cancelado)
(6, 1, 1, 4299.00),
-- Pedido 7 (Felipe)
(7, 9, 1, 1950.00), -- Mesa Regulável
(7, 8, 1, 1250.00), -- Cadeira
-- Pedido 8 (Gabriela)
(8, 3, 1, 499.00),  -- Smartwatch
-- Pedido 9 (Bruno Souza)
(9, 7, 1, 450.00),  -- SSD
(9, 11, 1, 89.90),  -- Livro SQL
-- Pedido 10 (Henrique)
(10, 2, 1, 799.00), -- Fone
(10, 3, 1, 499.00), -- Smartwatch
-- Pedido 11 (Camila)
(11, 4, 1, 2199.00), -- Monitor
-- Pedido 12 (Isabela)
(12, 10, 1, 69.90),
(12, 11, 1, 89.90),
(12, 12, 1, 95.00),
-- Pedido 13 (João Victor)
(13, 5, 1, 389.90),
(13, 6, 1, 189.90),
-- Pedido 14 (Ana Clara)
(14, 9, 1, 1950.00),
-- Pedido 15 (Diego)
(15, 1, 1, 4299.00);

-- 6. PAGAMENTOS
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
