-- ==============================================================================
-- PROJETO: Analise e Posicionamento Financeiro de Estudio Indie de Games
-- ARQUIVO: 01_schema_constraints.sql
-- AUTOR: Victor Ramos
-- OBJETIVO: Definicao de integridade referencial, chaves e indices de performance
-- ==============================================================================

-- 1. Chaves Primarias
ALTER TABLE estudio_games.jogos 
    ADD CONSTRAINT pk_jogos PRIMARY KEY (jogo_id);

ALTER TABLE estudio_games.equipe_colaboradores 
    ADD CONSTRAINT pk_equipe PRIMARY KEY (colaborador_id);

ALTER TABLE estudio_games.custos_operacionais 
    ADD CONSTRAINT pk_custos_operacionais PRIMARY KEY (custo_id);

ALTER TABLE estudio_games.alocacao_desenvolvimento 
    ADD CONSTRAINT pk_alocacao_desenvolvimento PRIMARY KEY (alocacao_id);

ALTER TABLE estudio_games.despesas_marketing 
    ADD CONSTRAINT pk_despesas_marketing PRIMARY KEY (campanha_id);

ALTER TABLE estudio_games.vendas_plataforma 
    ADD CONSTRAINT pk_vendas_plataforma PRIMARY KEY (venda_id);

-- 2. Chaves Estrangeiras (Integridade Referencial)
ALTER TABLE estudio_games.alocacao_desenvolvimento
    ADD CONSTRAINT fk_alocacao_jogo 
    FOREIGN KEY (jogo_id) REFERENCES estudio_games.jogos(jogo_id) ON DELETE CASCADE,
    ADD CONSTRAINT fk_alocacao_colaborador 
    FOREIGN KEY (colaborador_id) REFERENCES estudio_games.equipe_colaboradores(colaborador_id) ON DELETE RESTRICT;

ALTER TABLE estudio_games.despesas_marketing
    ADD CONSTRAINT fk_marketing_jogo 
    FOREIGN KEY (jogo_id) REFERENCES estudio_games.jogos(jogo_id) ON DELETE CASCADE;

ALTER TABLE estudio_games.vendas_plataforma
    ADD CONSTRAINT fk_vendas_jogo 
    FOREIGN KEY (jogo_id) REFERENCES estudio_games.jogos(jogo_id) ON DELETE CASCADE;

-- 3. Indices de Performance (B-Tree)
CREATE INDEX idx_alocacao_jogo ON estudio_games.alocacao_desenvolvimento(jogo_id);
CREATE INDEX idx_alocacao_mes ON estudio_games.alocacao_desenvolvimento(ano_mes);
CREATE INDEX idx_marketing_jogo ON estudio_games.despesas_marketing(jogo_id);
CREATE INDEX idx_vendas_jogo ON estudio_games.vendas_plataforma(jogo_id);
CREATE INDEX idx_vendas_mes ON estudio_games.vendas_plataforma(ano_mes);
CREATE INDEX idx_custos_mes ON estudio_games.custos_operacionais(ano_mes);
