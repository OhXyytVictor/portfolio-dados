"""
==============================================================================
PROJETO: Analise e Posicionamento Financeiro de Estudio Indie de Games
ARQUIVO: 02_data_quality_check.py
AUTOR: Victor Ramos
OBJETIVO: Suite automatizada de governanca e auditoria de qualidade de dados
==============================================================================
"""

from datetime import datetime
import psycopg2

DATABASE_URI = "postgresql://postgres:5336@localhost:5432/postgres"

def run_suite():
    print("[INFO] Iniciando testes de qualidade de dados do Estudio Indie...")
    conn = psycopg2.connect(DATABASE_URI)
    cur = conn.cursor()

    tests = []

    def test(test_id, category, desc, expected, actual, passed):
        status = "APROVADO" if passed else "REPROVADO"
        tests.append({
            "id": test_id, "categoria": category, "descricao": desc,
            "esperado": expected, "obtido": actual, "status": status
        })
        prefix = "[PASS]" if passed else "[FAIL]"
        print(f" {prefix} Teste {test_id}: {desc} -> {status} ({actual})")

    # 1. Nulidades em Chaves Primarias
    cur.execute("SELECT COUNT(*) FROM estudio_games.jogos WHERE jogo_id IS NULL;")
    n_jogos = cur.fetchone()[0]
    test("DQ-01", "Chaves Primarias", "Nulidade em jogos.jogo_id", "0 nulos", f"{n_jogos} nulos", n_jogos == 0)

    cur.execute("SELECT COUNT(*) FROM estudio_games.equipe_colaboradores WHERE colaborador_id IS NULL;")
    n_equipe = cur.fetchone()[0]
    test("DQ-02", "Chaves Primarias", "Nulidade em equipe_colaboradores.colaborador_id", "0 nulos", f"{n_equipe} nulos", n_equipe == 0)

    cur.execute("SELECT COUNT(*) FROM estudio_games.vendas_plataforma WHERE venda_id IS NULL;")
    n_vendas = cur.fetchone()[0]
    test("DQ-03", "Chaves Primarias", "Nulidade em vendas_plataforma.venda_id", "0 nulos", f"{n_vendas} nulos", n_vendas == 0)

    # 2. Integridade Referencial (Chaves Orfas)
    cur.execute("""
        SELECT COUNT(*) 
        FROM estudio_games.vendas_plataforma v 
        LEFT JOIN estudio_games.jogos j ON v.jogo_id = j.jogo_id 
        WHERE j.jogo_id IS NULL;
    """)
    orf_vendas = cur.fetchone()[0]
    test("DQ-04", "Integridade Referencial", "Vendas sem jogo correspondente", "0 orfaos", f"{orf_vendas} orfaos", orf_vendas == 0)

    cur.execute("""
        SELECT COUNT(*) 
        FROM estudio_games.alocacao_desenvolvimento a 
        LEFT JOIN estudio_games.equipe_colaboradores e ON a.colaborador_id = e.colaborador_id 
        WHERE e.colaborador_id IS NULL;
    """)
    orf_aloc = cur.fetchone()[0]
    test("DQ-05", "Integridade Referencial", "Alocacao sem colaborador correspondente", "0 orfaos", f"{orf_aloc} orfaos", orf_aloc == 0)

    # 3. Consistencia Financeira
    cur.execute("SELECT COUNT(*) FROM estudio_games.equipe_colaboradores WHERE salario_mensal <= 0;")
    sal_inv = cur.fetchone()[0]
    test("DQ-06", "Regras Financeiras", "Colaboradores com salario invalido", "0 registros", f"{sal_inv} registros", sal_inv == 0)

    cur.execute("SELECT COUNT(*) FROM estudio_games.vendas_plataforma WHERE receita_liquida > receita_bruta;")
    rec_inv = cur.fetchone()[0]
    test("DQ-07", "Regras Financeiras", "Vendas com receita liquida maior que receita bruta", "0 anomalias", f"{rec_inv} anomalias", rec_inv == 0)

    # 4. Consistencia da View P&L
    cur.execute("SELECT COUNT(*) FROM estudio_games.vw_pl_por_jogo WHERE investimento_total < 0;")
    inv_inv = cur.fetchone()[0]
    test("DQ-08", "Camada Semantica", "Jogos com investimento total negativo", "0 registros", f"{inv_inv} registros", inv_inv == 0)

    conn.close()

    total = len(tests)
    passed = sum(1 for t in tests if t["status"] == "APROVADO")
    pct = round((passed / total) * 100, 1)

    report = f"""# Relatorio de Auditoria de Dados: Estudio Indie de Games

**Data da Auditoria:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Schema Auditado:** `estudio_games` (PostgreSQL 18)  
**Taxa de Conformidade:** {pct}% ({passed}/{total} aprovados)

---

## Detalhamento dos Testes

| ID | Categoria | Regra Auditada | Esperado | Obtido | Status |
| :---: | :--- | :--- | :---: | :---: | :---: |
"""
    for t in tests:
        report += f"| **{t['id']}** | {t['categoria']} | {t['descricao']} | {t['esperado']} | {t['obtido']} | **{t['status']}** |\n"

    report_path = "03-indie-game-studio-analytics/docs/DATA_QUALITY_REPORT.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n[INFO] Relatorio de auditoria gerado em: {report_path}")

if __name__ == "__main__":
    run_suite()
