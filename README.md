# E-commerce Data Warehouse

Mini Data Warehouse em **modelo estrela** para análise de vendas. O ETL em Python transforma arquivos operacionais em dimensões e tabela fato SQL.

## Modelo
`dim_customer`, `dim_product`, `dim_date`, `dim_channel` -> `fact_sales`

## Execução
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/generate_source.py
python src/load_dw.py
sqlite3 data/output/ecommerce_dw.db < sql/analytics.sql
```

## Testes
```bash
python -m unittest discover -s tests -v
```
