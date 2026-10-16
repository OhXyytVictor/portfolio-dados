# Relatorio de Auditoria e Qualidade de Dados (Data Quality)

**Data de Execucao:** 2026-10-16 12:57:40  
**Ambiente:** PostgreSQL 18 (Localhost)  
**Schema Auditado:** `olist`  
**Taxa de Conformidade:** 100.0% (10/10 testes aprovados)

---

## 1. Resumo Executivo da Auditoria

| Metrica | Valor |
| :--- | :---: |
| **Total de Testes Executados** | 10 |
| **Testes Aprovados** | 10 |
| **Testes Reprovados** | 0 |
| **Status Geral** | CONFORME PARA PRODUCAO |

---

## 2. Detalhamento dos Testes Executados

| ID | Categoria | Descricao da Regra | Resultado Esperado | Resultado Obtido | Status |
| :---: | :--- | :--- | :---: | :---: | :---: |
| **DQ-01** | Integridade Estrutural | Nulidade em PK orders.order_id | 0 nulos | 0 nulos | **APROVADO** |
| **DQ-02** | Integridade Estrutural | Nulidade em PK customers.customer_id | 0 nulos | 0 nulos | **APROVADO** |
| **DQ-03** | Integridade Estrutural | Nulidade em PK products.product_id | 0 nulos | 0 nulos | **APROVADO** |
| **DQ-04** | Integridade Referencial | Itens de pedido sem pedido correspondente (orfãos) | 0 orfaos | 0 orfaos | **APROVADO** |
| **DQ-05** | Integridade Referencial | Itens de pedido com produto inexistente | 0 orfaos | 0 orfaos | **APROVADO** |
| **DQ-06** | Consistencia Temporal | Pedidos entregues antes da data de compra | 0 anomalias | 0 anomalias | **APROVADO** |
| **DQ-07** | Consistencia Financeira | Itens com preco menor ou igual a zero | 0 registros | 0 registros | **APROVADO** |
| **DQ-08** | Consistencia Financeira | Itens com frete negativo | 0 registros | 0 registros | **APROVADO** |
| **DQ-09** | Validacao de Dominio | Notas de avaliacao fora da escala de 1 a 5 | 0 notas invalidas | 0 notas invalidas | **APROVADO** |
| **DQ-10** | Camada Semantica / View | Registros na view Gamer Shield sem classificacao | 0 nulos | 0 nulos | **APROVADO** |

---

## 3. Diretrizes de Governanca Aplicadas
* **Chaves e Unicidade:** Garantia de zero duplicatas e zero nulos nas chaves de navegacao relacional.
* **Integridade Referencial:** Nao ha orfaos entre a tabela de itens e os cabecalhos de pedidos ou catalogo de produtos.
* **Consistencia Cronologica:** Todos os eventos logicos obedecem a linha temporal: compra -> aprovacao -> envio -> entrega.
* **Integridade Semantica:** A view prescritiva do Gamer Shield classifica 100% dos pedidos gamers sem lacunas nulas.
