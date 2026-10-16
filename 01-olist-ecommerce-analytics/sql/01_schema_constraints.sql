-- ============================================================================
-- PROJETO OLIST E-COMMERCE - POSTGRESQL
-- ARQUIVO: 01_schema_constraints.sql
-- ETAPA: Criação de Chaves Primárias, Chaves Estrangeiras e Índices de Busca
-- AUTOR: Victor Ramos
-- ============================================================================

SET search_path TO olist, public;

-- 1. CHAVES PRIMÁRIAS (PRIMARY KEYS)
ALTER TABLE olist.customers 
    ADD CONSTRAINT pk_customers PRIMARY KEY (customer_id);

ALTER TABLE olist.sellers 
    ADD CONSTRAINT pk_sellers PRIMARY KEY (seller_id);

ALTER TABLE olist.products 
    ADD CONSTRAINT pk_products PRIMARY KEY (product_id);

ALTER TABLE olist.orders 
    ADD CONSTRAINT pk_orders PRIMARY KEY (order_id);

ALTER TABLE olist.order_items 
    ADD CONSTRAINT pk_order_items PRIMARY KEY (order_id, order_item_id);


-- 2. CHAVES ESTRANGEIRAS (FOREIGN KEYS)
ALTER TABLE olist.orders
    ADD CONSTRAINT fk_orders_customers 
    FOREIGN KEY (customer_id) REFERENCES olist.customers(customer_id);

ALTER TABLE olist.order_items
    ADD CONSTRAINT fk_order_items_orders 
    FOREIGN KEY (order_id) REFERENCES olist.orders(order_id) ON DELETE CASCADE;

ALTER TABLE olist.order_items
    ADD CONSTRAINT fk_order_items_products 
    FOREIGN KEY (product_id) REFERENCES olist.products(product_id);

ALTER TABLE olist.order_items
    ADD CONSTRAINT fk_order_items_sellers 
    FOREIGN KEY (seller_id) REFERENCES olist.sellers(seller_id);

ALTER TABLE olist.order_payments
    ADD CONSTRAINT fk_order_payments_orders 
    FOREIGN KEY (order_id) REFERENCES olist.orders(order_id) ON DELETE CASCADE;

ALTER TABLE olist.order_reviews
    ADD CONSTRAINT fk_order_reviews_orders 
    FOREIGN KEY (order_id) REFERENCES olist.orders(order_id) ON DELETE CASCADE;


-- 3. ÍNDICES DE PERFORMANCE (B-TREE INDEXES)
CREATE INDEX idx_orders_purchase_timestamp ON olist.orders(order_purchase_timestamp);
CREATE INDEX idx_orders_status ON olist.orders(order_status);
CREATE INDEX idx_order_items_seller ON olist.order_items(seller_id);
CREATE INDEX idx_order_items_product ON olist.order_items(product_id);
CREATE INDEX idx_order_payments_type ON olist.order_payments(payment_type);
CREATE INDEX idx_order_reviews_score ON olist.order_reviews(review_score);
CREATE INDEX idx_customers_state ON olist.customers(customer_state);
CREATE INDEX idx_sellers_state ON olist.sellers(seller_state);
