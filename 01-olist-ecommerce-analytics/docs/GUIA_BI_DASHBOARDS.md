# Guia de Integração BI: Power BI, Metabase e Dashboard Interativo

**Autor:** Victor Ramos  
**Stack Visual:** Power BI Desktop, Metabase, HTML5/Chart.js  
**Banco Fonte:** PostgreSQL 18 (Localhost:5432)  
**Schema Semântico:** `olist`  

---

## 1. Dashboard Interativo Local (Sem Instalação)

Para visualização tática imediata sem necessidade de servidores ou licenças adicionais, o projeto conta com um painel interativo responsivo embutido:

* **Arquivo:** [`docs/dashboard_interativo.html`](./dashboard_interativo.html)
* **Como visualizar:** Abra o arquivo diretamente em qualquer navegador moderno (Chrome, Edge, Firefox).
* **Funcionalidades:**
  * Filtros dinâmicos por macrorregião (Todas, Sudeste, Sul, Nordeste, Centro-Oeste, Norte).
  * Scorecards interativos de faturamento, prazo de trânsito, taxa de atraso e ROI do Gamer Shield.
  * Gráficos analíticos renderizados com Chart.js.
  * Tabela de nível tático atualizada em tempo real conforme a seleção do usuário.

---

## 2. Conexão no Power BI Desktop

### Parâmetros de Conexão:
* **Conector:** Banco de dados PostgreSQL
* **Servidor:** `localhost:5432`
* **Banco de Dados:** `postgres`
* **Modo de Conectividade:** Importação ou DirectQuery
* **Autenticação:** Usuário `postgres` e senha configurada

### Views Recomendadas para Importação:
Em vez de importar as 9 tabelas brutas, importe apenas a camada semântica já tratada:
1. `olist.vw_pedidos_detalhados` (Fatos de pedidos, clientes e produtos desnormalizados)
2. `olist.vw_alertas_gamer_shield` (Motor analítico prescritivo e cálculo de ROI)

### Medidas DAX Recomendadas:

```dax
-- 1. Faturamento Total
Faturamento Total = SUM(vw_pedidos_detalhados[valor_total_item])

-- 2. Tíquete Médio Gamer
Ticket Medio = DIVIDE([Faturamento Total], DISTINCTCOUNT(vw_pedidos_detalhados[order_id]), 0)

-- 3. Taxa de Atraso de SLA (%)
Taxa Atraso SLA = 
DIVIDE(
    CALCULATE(DISTINCTCOUNT(vw_pedidos_detalhados[order_id]), vw_pedidos_detalhados[dias_atraso] > 0),
    DISTINCTCOUNT(vw_pedidos_detalhados[order_id]),
    0
)

-- 4. Multiplicador de Retorno Gamer Shield (ROI)
ROI Gamer Shield = 
DIVIDE(
    SUM(vw_alertas_gamer_shield[receita_protegida]),
    SUM(vw_alertas_gamer_shield[custo_acao_voucher]),
    0
)
```

---

## 3. Conexão no Metabase

Para subir um ambiente open-source de BI em minutos via Docker:

```bash
docker run -d -p 3000:3000 --name metabase metabase/metabase
```

* Acesse `http://localhost:3000`
* Adicione o banco PostgreSQL:
  * **Host:** `host.docker.internal`
  * **Porta:** `5432`
  * **Nome do Banco:** `postgres`
  * **Usuário:** `postgres`
* Acesse a coleção de perguntas e selecione a view `olist.vw_alertas_gamer_shield` para gerar os cards com filtro de data e UF.
