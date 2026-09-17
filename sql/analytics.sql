.headers on
.mode column
-- Monthly revenue and MoM growth
WITH monthly AS (
 SELECT d.year,d.month,SUM(f.net_amount) revenue
 FROM fact_sales f JOIN dim_date d ON d.date_key=f.date_key
 GROUP BY d.year,d.month
), x AS (
 SELECT *,LAG(revenue) OVER(ORDER BY year,month) prev FROM monthly
)
SELECT year,month,ROUND(revenue,2) revenue,ROUND((revenue-prev)*100.0/prev,2) mom_pct FROM x;

-- Category performance
SELECT p.category,ROUND(SUM(f.net_amount),2) revenue,SUM(f.quantity) units
FROM fact_sales f JOIN dim_product p ON p.product_key=f.product_key
GROUP BY p.category ORDER BY revenue DESC;

-- Top customers
SELECT c.customer_name,c.state,ROUND(SUM(f.net_amount),2) revenue
FROM fact_sales f JOIN dim_customer c ON c.customer_key=f.customer_key
GROUP BY c.customer_key ORDER BY revenue DESC LIMIT 10;
