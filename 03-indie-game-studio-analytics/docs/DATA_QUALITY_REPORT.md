# Relatorio de Auditoria de Dados: Estudio Indie de Games

**Data da Auditoria:** 2026-10-16 15:25:27  
**Schema Auditado:** `estudio_games` (PostgreSQL 18)  
**Taxa de Conformidade:** 100.0% (8/8 aprovados)

---

## Detalhamento dos Testes

| ID | Categoria | Regra Auditada | Esperado | Obtido | Status |
| :---: | :--- | :--- | :---: | :---: | :---: |
| **DQ-01** | Chaves Primarias | Nulidade em jogos.jogo_id | 0 nulos | 0 nulos | **APROVADO** |
| **DQ-02** | Chaves Primarias | Nulidade em equipe_colaboradores.colaborador_id | 0 nulos | 0 nulos | **APROVADO** |
| **DQ-03** | Chaves Primarias | Nulidade em vendas_plataforma.venda_id | 0 nulos | 0 nulos | **APROVADO** |
| **DQ-04** | Integridade Referencial | Vendas sem jogo correspondente | 0 orfaos | 0 orfaos | **APROVADO** |
| **DQ-05** | Integridade Referencial | Alocacao sem colaborador correspondente | 0 orfaos | 0 orfaos | **APROVADO** |
| **DQ-06** | Regras Financeiras | Colaboradores com salario invalido | 0 registros | 0 registros | **APROVADO** |
| **DQ-07** | Regras Financeiras | Vendas com receita liquida maior que receita bruta | 0 anomalias | 0 anomalias | **APROVADO** |
| **DQ-08** | Camada Semantica | Jogos com investimento total negativo | 0 registros | 0 registros | **APROVADO** |
