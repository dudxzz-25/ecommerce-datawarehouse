PRAGMA foreign_keys=ON;
DROP TABLE IF EXISTS fact_sales; DROP TABLE IF EXISTS dim_channel; DROP TABLE IF EXISTS dim_date; DROP TABLE IF EXISTS dim_product; DROP TABLE IF EXISTS dim_customer;
CREATE TABLE dim_customer(customer_key INTEGER PRIMARY KEY, customer_id INTEGER UNIQUE, customer_name TEXT, state TEXT);
CREATE TABLE dim_product(product_key INTEGER PRIMARY KEY, product_id INTEGER UNIQUE, product_name TEXT, category TEXT);
CREATE TABLE dim_date(date_key INTEGER PRIMARY KEY, full_date TEXT UNIQUE, year INTEGER, quarter INTEGER, month INTEGER, month_name TEXT, day INTEGER, weekday INTEGER);
CREATE TABLE dim_channel(channel_key INTEGER PRIMARY KEY, channel TEXT UNIQUE);
CREATE TABLE fact_sales(
 sale_key INTEGER PRIMARY KEY,
 sale_id INTEGER UNIQUE,
 customer_key INTEGER REFERENCES dim_customer(customer_key),
 product_key INTEGER REFERENCES dim_product(product_key),
 date_key INTEGER REFERENCES dim_date(date_key),
 channel_key INTEGER REFERENCES dim_channel(channel_key),
 quantity INTEGER, unit_price REAL, discount_pct REAL, gross_amount REAL, net_amount REAL
);
CREATE INDEX idx_fact_date ON fact_sales(date_key); CREATE INDEX idx_fact_product ON fact_sales(product_key); CREATE INDEX idx_fact_customer ON fact_sales(customer_key);
