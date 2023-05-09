WITH number_of_sales AS (
	SELECT store_type, COUNT(product_quantity) AS number_of_stores
	FROM orders_table
	LEFT JOIN dim_store_details ON dim_store_details.store_code = orders_table.store_code
	GROUP BY store_type
),
total_sales AS (
	SELECT COUNT(number_of_stores) total_sales
	FROM number_of_sales
)
SELECT store_type, total_sales, number_of_sales, ROUND(100 * number_of_stores / total_sales, 2) percentage_total
FROM number_of_sales, total_sales
ORDER BY percentage_total DESC;