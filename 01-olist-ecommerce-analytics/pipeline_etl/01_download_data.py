"""
=============================================================================
PIPELINE ETL - PROJETO OLIST E-COMMERCE
Etapa 01: Download Automatizado do Dataset da Olist
Autor: Victor Ramos
=============================================================================
"""

import os
import urllib.request
import sys

BASE_URL = "https://raw.githubusercontent.com/Ajandaghian/olist-ecommerce-etl-pipeline/main/data/raw/"

DATASETS = [
    "olist_customers_dataset.csv",
    "olist_geolocation_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_orders_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "product_category_name_translation.csv"
]

def download_file(filename, output_dir):
    url = BASE_URL + filename
    dest_path = os.path.join(output_dir, filename)

    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 0:
        print(f"  [OK] Ja existe: {filename} ({os.path.getsize(dest_path) / (1024*1024):.2f} MB)")
        return

    print(f"  [Baixando] {filename}...")
    try:
        urllib.request.urlretrieve(url, dest_path)
        size_mb = os.path.getsize(dest_path) / (1024 * 1024)
        print(f"  [Concluido] {filename} ({size_mb:.2f} MB)")
    except Exception as e:
        print(f"  [ERRO] Falha ao baixar {filename}: {e}")

def main():
    print("=" * 60)
    print("INICIANDO DOWNLOAD DOS DADOS DA OLIST (BRAZILIAN E-COMMERCE)")
    print("=" * 60)

    # Diretorio de destino (data/raw relativo ao script)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.abspath(os.path.join(current_dir, "..", "data", "raw"))
    os.makedirs(output_dir, exist_ok=True)
    print(f"Diretorio de destino: {output_dir}\n")

    for idx, filename in enumerate(DATASETS, 1):
        print(f"({idx}/{len(DATASETS)}) {filename}")
        download_file(filename, output_dir)

    print("\n" + "=" * 60)
    print("DOWNLOAD CONCLUIDO COM SUCESSO!")
    print("=" * 60)

if __name__ == "__main__":
    main()
