-- ============================================================================
-- PROJETO 01: MODELAGEM RELACIONAL E CONSULTAS ANALÍTICAS DE E-COMMERCE
-- ARQUIVO: 01_schema_ddl.sql
-- DESCRIÇÃO: Criação das tabelas, chaves primárias, estrangeiras e índices.
-- SGBD: PostgreSQL (versão 14+)
-- AUTOR: Victor Ramos
-- ============================================================================

-- 1. LIMPEZA PREVENTIVA DO SCHEMA (Para permitir reexecução segura)
DROP TABLE IF EXISTS pagamentos CASCADE;
DROP TABLE IF EXISTS itens_pedido CASCADE;
DROP TABLE IF EXISTS pedidos CASCADE;
DROP TABLE IF EXISTS produtos CASCADE;
DROP TABLE IF EXISTS categorias CASCADE;
DROP TABLE IF EXISTS clientes CASCADE;

-- ============================================================================
-- 2. CRIAÇÃO DAS TABELAS (DDL)
-- ============================================================================

-- Tabela: clientes
CREATE TABLE clientes (
    cliente_id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    cidade VARCHAR(80) NOT NULL,
    estado CHAR(2) NOT NULL,
    data_cadastro DATE NOT NULL DEFAULT CURRENT_DATE
);

-- Tabela: categorias
CREATE TABLE categorias (
    categoria_id SERIAL PRIMARY KEY,
    nome_categoria VARCHAR(60) NOT NULL UNIQUE,
    descricao VARCHAR(255)
);

-- Tabela: produtos
CREATE TABLE produtos (
    produto_id SERIAL PRIMARY KEY,
    categoria_id INT NOT NULL,
    nome_produto VARCHAR(120) NOT NULL,
    preco_unitario NUMERIC(10, 2) NOT NULL CHECK (preco_unitario > 0),
    estoque_atual INT NOT NULL DEFAULT 0 CHECK (estoque_atual >= 0),
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT fk_produtos_categoria 
        FOREIGN KEY (categoria_id) 
        REFERENCES categorias(categoria_id) 
        ON DELETE RESTRICT
);

-- Tabela: pedidos
CREATE TABLE pedidos (
    pedido_id SERIAL PRIMARY KEY,
    cliente_id INT NOT NULL,
    data_pedido TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status_pedido VARCHAR(20) NOT NULL DEFAULT 'Pendente' 
        CHECK (status_pedido IN ('Pendente', 'Processando', 'Enviado', 'Entregue', 'Cancelado')),
    CONSTRAINT fk_pedidos_cliente 
        FOREIGN KEY (cliente_id) 
        REFERENCES clientes(cliente_id) 
        ON DELETE RESTRICT
);

-- Tabela: itens_pedido
CREATE TABLE itens_pedido (
    item_id SERIAL PRIMARY KEY,
    pedido_id INT NOT NULL,
    produto_id INT NOT NULL,
    quantidade INT NOT NULL CHECK (quantidade > 0),
    preco_praticado NUMERIC(10, 2) NOT NULL CHECK (preco_praticado > 0),
    CONSTRAINT fk_itens_pedido 
        FOREIGN KEY (pedido_id) 
        REFERENCES pedidos(pedido_id) 
        ON DELETE CASCADE,
    CONSTRAINT fk_itens_produto 
        FOREIGN KEY (produto_id) 
        REFERENCES produtos(produto_id) 
        ON DELETE RESTRICT
);

-- Tabela: pagamentos
CREATE TABLE pagamentos (
    pagamento_id SERIAL PRIMARY KEY,
    pedido_id INT NOT NULL,
    metodo_pagamento VARCHAR(30) NOT NULL 
        CHECK (metodo_pagamento IN ('Cartão de Crédito', 'Boleto Bancário', 'PIX')),
    valor_pago NUMERIC(10, 2) NOT NULL CHECK (valor_pago > 0),
    status_pagamento VARCHAR(20) NOT NULL DEFAULT 'Aprovado'
        CHECK (status_pagamento IN ('Pendente', 'Aprovado', 'Recusado', 'Estornado')),
    data_pagamento TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_pagamentos_pedido 
        FOREIGN KEY (pedido_id) 
        REFERENCES pedidos(pedido_id) 
        ON DELETE CASCADE
);

-- ============================================================================
-- 3. OTIMIZAÇÃO E PERFORMANCE (ÍNDICES)
-- ============================================================================

-- Índices em chaves estrangeiras para acelerar os JOINs frequentes
CREATE INDEX idx_produtos_categoria_id ON produtos(categoria_id);
CREATE INDEX idx_pedidos_cliente_id ON pedidos(cliente_id);
CREATE INDEX idx_itens_pedido_id ON itens_pedido(pedido_id);
CREATE INDEX idx_itens_produto_id ON itens_pedido(produto_id);
CREATE INDEX idx_pagamentos_pedido_id ON pagamentos(pedido_id);

-- Índices em colunas de filtro temporal e status
CREATE INDEX idx_pedidos_data_status ON pedidos(data_pedido, status_pedido);
