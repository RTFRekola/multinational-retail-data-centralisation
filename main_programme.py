#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Wed 12 Apr 2023 at 14:25 UT
Last modified on Tue 9 May 2023 at 20:05 UT 

@author: Rami T. F. Rekola 

Multinational Retail Data Centralisation
========================================

Additional files where the classes and methods are hiding. 
file1 = "database_utils.py"
file2 = "data_extraction.py"
file3 = "data_cleaning.py"
'''

import pandas as pd
from database_utils import DatabaseConnector
from data_extraction import DataExtractor
from data_cleaning import DataCleaning

# Instantiate the three classes with all the methods
dbc = DatabaseConnector()
dex = DataExtractor()
dac = DataCleaning()

# Initiate Pandas DataFrames
data = []
pd_table = pd.DataFrame(data)
pdf_data = pd.DataFrame(data)
store_details = pd.DataFrame(data)
clean_products = pd.DataFrame(data)
orders_df = pd.DataFrame(data)
sales_data = pd.DataFrame(data)

# Process user data -> dim_users
pd_table = dac.clean_user_data(dex.read_rds_table(dbc, "user"))
dbc.upload_to_db(pd_table, "dim_users")

# Process card data -> dim_card_details
pdf_data = dac.clean_card_data(dex.retrieve_pdf_data())
dbc.upload_to_db(pdf_data, "dim_card_details")

# Process store data -> dim_store_details
endpoint_url = "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores"
header_details = {'x-api-key': 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}
no_of_stores = dex.list_number_of_stores(endpoint_url, header_details)
e = "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/"
endpoint_url = (e + str(0))
pd_stores = dex.retrieve_stores_data(endpoint_url, header_details)
for i in range(0,no_of_stores):
    endpoint_url = (e + str(i+1))
    pd_stores_i = dex.retrieve_stores_data(endpoint_url, header_details)
    pd_stores = pd.concat([pd_stores, pd_stores_i], axis="rows")
# end for
store_details = dac.clean_store_data(pd_stores)
dbc.upload_to_db(store_details, "dim_store_details")

# Process product data -> dim_products
s3_address = "s3://data-handling-public/products.csv"
product_data = dex.extract_from_s3(s3_address)
clean_products = dac.clean_products_data(product_data)
dbc.upload_to_db(clean_products, "dim_products")

# Process the central orders table -> orders_table
orders_df = dac.clean_orders_data(dex.read_rds_table(dbc, "orders"))
dbc.upload_to_db(orders_df, "orders_table")

# Process sales data -> dim_date_times
s3_address = "https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json"
sales_data = dex.extract_json_from_s3(s3_address)
clean_sales = dac.clean_sales_data(sales_data)
dbc.upload_to_db(sales_data, "dim_date_times")

'''
End of the main programme. Thank you for running me.
'''