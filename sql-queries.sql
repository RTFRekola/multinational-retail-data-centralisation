SELECT product_code
       , length(product_code)
FROM orders_table
GROUP BY product_code
ORDER BY length(product_code) desc
LIMIT 1;

------------------------------------------------------------

ALTER TABLE orders_table
	ALTER COLUMN date_uuid TYPE UUID USING date_uuid::uuid;

ALTER TABLE orders_table
	ALTER COLUMN user_uuid TYPE UUID USING user_uuid::uuid;

ALTER TABLE orders_table
	ALTER COLUMN card_number TYPE varchar(19);

ALTER TABLE orders_table
	ALTER COLUMN store_code TYPE varchar(12);

ALTER TABLE orders_table
	ALTER COLUMN product_code TYPE varchar(11);

ALTER TABLE orders_table
	ALTER COLUMN product_quantity TYPE smallint;

------------------------------------------------------------

ALTER TABLE dim_users
	ALTER COLUMN first_name TYPE varchar(255);

ALTER TABLE dim_users
	ALTER COLUMN last_name TYPE varchar(255);

-- ALTER TABLE dim_users
-- 	ALTER COLUMN date_of_birth TYPE date;

ALTER TABLE dim_users
	ALTER COLUMN country_code TYPE varchar(2);

ALTER TABLE dim_users
	ALTER COLUMN user_uuid TYPE UUID USING user_uuid::uuid;

-- ALTER TABLE dim_users
-- 	ALTER COLUMN join_date TYPE date;

------------------------------------------------------------

ALTER TABLE dim_store_details
	ALTER COLUMN longitude TYPE float;

ALTER TABLE dim_store_details
	ALTER COLUMN latitude TYPE float;

ALTER TABLE dim_store_details
	ALTER COLUMN locality TYPE varchar(255);

ALTER TABLE dim_store_details
	ALTER COLUMN store_code TYPE varchar(12);

ALTER TABLE dim_store_details
	ALTER COLUMN staff_numbers TYPE smallint;

-- ALTER TABLE dim_store_details
-- 	ALTER COLUMN opening_date TYPE date;

ALTER TABLE dim_store_details ALTER COLUMN store_type DROP NOT NULL;

ALTER TABLE dim_store_details
	ALTER COLUMN store_type TYPE varchar(255) nullable;

ALTER TABLE dim_store_details
	ALTER COLUMN country_code TYPE varchar(2);

ALTER TABLE dim_store_details
	ALTER COLUMN continent TYPE varchar(255);

------------------------------------------------------------

ALTER TABLE dim_products ALTER COLUMN product_price TYPE float USING (REPLACE(product_price, '£', '')::numeric);

ALTER TABLE dim_products
ADD COLUMN weight_class varchar(14);

UPDATE dim_products
SET weight_class = 'Light'
WHERE weight < 2

UPDATE dim_products
SET weight_class = 'Mid_Sized'
WHERE weight >= 2 AND weight < 40

UPDATE dim_products
SET weight_class = 'Heavy'
WHERE weight >= 40 AND weight < 140

UPDATE dim_products
SET weight_class = 'Truck_Required'
WHERE weight >= 140

------------------------------------------------------------

-- ALTER TABLE dim_products
--    ALTER COLUMN product_price TYPE float;

-- ALTER TABLE dim_products
--    ALTER COLUMN weight TYPE float;

ALTER TABLE dim_products
    ALTER COLUMN "EAN" TYPE varchar(17);

ALTER TABLE dim_products
    ALTER COLUMN product_code TYPE varchar(11);

-- ALTER TABLE dim_products
--    ALTER COLUMN date_added TYPE date;

ALTER TABLE dim_products
    ALTER COLUMN uuid TYPE UUID USING uuid::uuid;

-- ALTER TABLE dim_products
--    ALTER COLUMN weight_class TYPE varchar(14);

------------------------------------------------------------

ALTER TABLE dim_products
ADD COLUMN still_available boolean;

UPDATE dim_products
SET still_available = true
WHERE removed = 'Still_avaliable';

UPDATE dim_products
SET still_available = false
WHERE removed = 'Removed';

ALTER TABLE dim_products
    DROP COLUMN removed;

------------------------------------------------------------

ALTER TABLE dim_date_times
    ALTER COLUMN year TYPE varchar(4);

ALTER TABLE dim_date_times
    ALTER COLUMN month TYPE varchar(2);

ALTER TABLE dim_date_times
    ALTER COLUMN day TYPE varchar(2);

ALTER TABLE dim_date_times
    ALTER COLUMN time_period TYPE varchar(10);

ALTER TABLE dim_date_times
	ALTER COLUMN date_uuid TYPE UUID USING date_uuid::uuid;

------------------------------------------------------------

ALTER TABLE dim_card_details
    ALTER COLUMN card_number TYPE varchar(19);

ALTER TABLE dim_card_details
    ALTER COLUMN expiry_date TYPE varchar(5);

-- ALTER TABLE dim_card_details
--    ALTER COLUMN date_payment_confirmed date;

------------------------------------------------------------

ALTER TABLE dim_card_details ADD PRIMARY KEY (card_number);

ALTER TABLE dim_date_times ADD PRIMARY KEY (date_uuid);

ALTER TABLE dim_products ADD PRIMARY KEY (product_code);

ALTER TABLE dim_store_details ADD PRIMARY KEY (store_code);

ALTER TABLE dim_users ADD PRIMARY KEY (user_uuid);

------------------------------------------------------------

ALTER TABLE orders_table ADD FOREIGN KEY(date_uuid) REFERENCES dim_date_times(date_uuid);

ALTER TABLE orders_table ADD FOREIGN KEY(card_number) REFERENCES dim_card_details(card_number);

ALTER TABLE orders_table ADD FOREIGN KEY(product_code) REFERENCES dim_products(product_code);

ALTER TABLE orders_table ADD FOREIGN KEY(store_code) REFERENCES dim_store_details(store_code);

DELETE FROM orders_table
WHERE user_uuid NOT IN (SELECT user_uuid FROM dim_users);
ALTER TABLE orders_table 
ADD CONSTRAINT fk_orders_table_user_uuid
FOREIGN KEY (user_uuid)
REFERENCES dim_users(user_uuid);

------------------------------------------------------------
------------------------------------------------------------
------------------------------------------------------------

SELECT country_code, COUNT(country_code) AS total_no_stores
FROM dim_store_details
GROUP BY country_code
ORDER BY total_no_stores DESC;

------------------------------------------------------------

SELECT locality, COUNT(locality) AS total_no_stores
FROM dim_store_details
GROUP BY locality
HAVING COUNT(locality) > 9
ORDER BY total_no_stores DESC;

------------------------------------------------------------

SELECT ROUND(SUM(product_quantity * product_price)::Decimal, 2) AS total_sales, month
FROM orders_table
LEFT JOIN dim_date_times ON dim_date_times.date_uuid = orders_table.date_uuid
LEFT JOIN dim_products ON dim_products.product_code = orders_table.product_code
GROUP BY month
ORDER BY total_sales DESC
LIMIT 6;

------------------------------------------------------------

ALTER TABLE dim_store_details
ADD COLUMN location VARCHAR(17);

UPDATE dim_store_details
SET location = 'Web'
WHERE store_type = 'Web Portal';

UPDATE dim_store_details
SET location = 'Offline'
WHERE store_type = 'Local' OR store_type = 'Super Store' OR store_type = 'Outlet' OR store_type = 'Mall Kiosk';

----

SELECT COUNT(product_quantity) AS numbers_of_sales, SUM(product_quantity) AS product_quantity_count, location
FROM orders_table
LEFT JOIN dim_store_details ON dim_store_details.store_code = orders_table.store_code
GROUP BY location
ORDER BY location DESC;

------------------------------------------------------------

WITH cte1 AS (
	SELECT store_type, ROUND(SUM(product_quantity * product_price)::Decimal,  2) AS total_sales
	FROM dim_store_details
	LEFT JOIN orders_table ON orders_table.store_code = dim_store_details.store_code
	LEFT JOIN dim_products ON dim_products.product_code = orders_table.product_code
	GROUP BY store_type
	ORDER BY total_sales DESC
), 
cte2 AS (
	SELECT SUM(total_sales) AS total_total_sales
	FROM cte1
)
SELECT store_type, total_sales, ROUND((100 * total_sales / total_total_sales)::Decimal, 2) percentage_total
FROM cte1, cte2
ORDER BY percentage_total DESC;

------------------------------------------------------------

SELECT ROUND(SUM(product_quantity * product_price)::Decimal,  2) AS total_sales, year, month
FROM orders_table
LEFT JOIN dim_date_times ON dim_date_times.date_uuid = orders_table.date_uuid
LEFT JOIN dim_products ON dim_products.product_code = orders_table.product_code
GROUP BY year, month
ORDER BY total_sales DESC
LIMIT 9;

------------------------------------------------------------

SELECT SUM(staff_numbers) AS total_staff_numbers, country_code
FROM dim_store_details
GROUP BY country_code
ORDER BY total_staff_numbers DESC;

------------------------------------------------------------

WITH cte1 AS (
	SELECT store_type, ROUND(SUM(product_quantity * product_price)::Decimal,  2) AS total_sales, country_code
	FROM dim_store_details
	LEFT JOIN orders_table ON orders_table.store_code = dim_store_details.store_code
	LEFT JOIN dim_products ON dim_products.product_code = orders_table.product_code
	GROUP BY store_type, country_code
	HAVING country_code = 'DE'
	ORDER BY total_sales ASC
)
SELECT total_sales, store_type, country_code
FROM cte1
ORDER BY total_sales ASC;

------------------------------------------------------------

WITH cte1 AS (
	SELECT TO_TIMESTAMP(year || '-' || month || '-' || day || ' ' || timestamp, 'YYYY-MM-DD HH24:MI:SS') AS datetime, year
	FROM dim_date_times
),
cte2 AS (
	SELECT year, datetime, 
	LEAD(datetime, 1) OVER (
		ORDER BY datetime DESC
	) AS time_difference
	FROM cte1
)
SELECT year, AVG(cte2.datetime - time_difference) AS actual_time_taken
FROM cte2
GROUP BY year
ORDER BY actual_time_taken DESC;
