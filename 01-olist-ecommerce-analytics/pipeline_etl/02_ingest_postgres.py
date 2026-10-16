"""
=============================================================================
PIPELINE ETL - PROJETO OLIST E-COMMERCE
Etapa 02: Ingestao Estruturada de Dados no PostgreSQL (Schema 'olist')
Autor: Victor Ramos
=============================================================================
"""

import os
import sys
import getpass
import time
import pandas as pd
from sqlalchemy import create_engine, text

# Configuracoes de Conexao
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")

# Mapeamento dos Arquivos para Tabelas e Colunas de Data
FILES_MAP = {
    "product_category_name_translation.csv": {
        "table": "category_name_translation",
        "dates": []
    },
    "olist_customers_dataset.csv": {
        "table": "customers",
        "dates": []
    },
    "olist_sellers_dataset.csv": {
        "table": "sellers",
        "dates": []
    },
    "olist_products_dataset.csv": {
        "table": "products",
        "dates": []
    },
    "olist_orders_dataset.csv": {
        "table": "orders",
        "dates": [
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date"
        ]
    },
    "olist_order_items_dataset.csv": {
        "table": "order_items",
        "dates": ["shipping_limit_date"]
    },
    "olist_order_payments_dataset.csv": {
        "table": "order_payments",
        "dates": []
    },
    "olist_order_reviews_dataset.csv": {
        "table": "order_reviews",
        "dates": ["review_creation_date", "review_answer_timestamp"]
    },
    "olist_geolocation_dataset.csv": {
        "table": "geolocation",
        "dates": []
    }
}

def get_db_engine(password):
    url = f"postgresql+psycopg2://{DB_USER}:{password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(url, pool_pre_ping=True)

def ingest_dataset(engine, raw_dir):
    print("\n" + "=" * 65)
    print("INICIANDO INGESTAO DE DADOS NO POSTGRESQL (SCHEMA: olist)")
    print("=" * 65)

    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS olist;"))
        print("[OK] Schema 'olist' verificado/criado com sucesso.\n")

    total_start = time.time()

    for idx, (filename, info) in enumerate(FILES_MAP.items(), 1):
        filepath = os.path.join(raw_dir, filename)
        table_name = info["table"]
        date_cols = info["dates"]

        if not os.path.exists(filepath):
            print(f"[{idx}/{len(FILES_MAP)}] AVISO: Arquivo nao encontrado: {filename} (Pulando)")
            continue

        start_t = time.time()
        print(f"[{idx}/{len(FILES_MAP)}] Processando: {filename} -> olist.{table_name}")

        # Leitura do CSV com deteccao de datas
        df = pd.read_csv(filepath, parse_dates=date_cols if date_cols else False, low_memory=False)

        # Carga no PostgreSQL
        # Usamos chunksize para garantir estabilidade mesmo em bases grandes (ex: geolocation com 1 milhao de linhas)
        chunk_size = 20000 if table_name == "geolocation" else 10000
        df.to_sql(
            name=table_name,
            con=engine,
            schema="olist",
            if_exists="replace",
            index=False,
            chunksize=chunk_size,
            method="multi"
        )

        elapsed = time.time() - start_t
        print(f"       -> {len(df):,} linhas inseridas com sucesso em {elapsed:.2f}s.")

    total_elapsed = time.time() - total_start
    print("\n" + "=" * 65)
    print(f"INGESTAO COMPLETA FINALIZADA EM {total_elapsed:.2f} SEGUNDOS!")
    print("=" * 65)

def main():
    raw_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "raw"))

    # Verifica senha por variavel de ambiente, parametro ou solicita
    password = os.getenv("POSTGRES_PASSWORD")
    if not password and len(sys.argv) > 1:
        password = sys.argv[1]
    
    if not password:
        password = input("Digite a senha do PostgreSQL (usuario postgres): ").strip()

    try:
        engine = get_db_engine(password)
        # Teste rapido de conexao
        with engine.connect() as conn:
            conn.execute(text("SELECT 1;"))
            print("[OK] Conexao com PostgreSQL validada com sucesso!")
        
        ingest_dataset(engine, raw_dir)

    except Exception as e:
        print(f"\n[ERRO DE CONEXAO OU CARGA]: {e}")
        print("Verifique se o PostgreSQL esta rodando e se a senha digitada esta correta.")

if __name__ == "__main__":
    main()
