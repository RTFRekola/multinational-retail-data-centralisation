'''
file1 = "database_utils.py"
file2 = "data_extraction.py"
file3 = "data_cleaning.py"
'''
import pandas as pd
from database_utils import DatabaseConnector
from data_extraction import DataExtractor
from data_cleaning import DataCleaning

DbC = DatabaseConnector()
DEx = DataExtractor()
DaC = DataCleaning()

data = []
pd_table = pd.DataFrame(data)
pdf_data = pd.DataFrame(data)
store_details = pd.DataFrame(data)
clean_products = pd.DataFrame(data)
orders_df = pd.DataFrame(data)
sales_data = pd.DataFrame(data)

pd_table = DaC.clean_user_data(DEx.read_rds_table("user"))
'''
pdf_data = DaC.clean_card_data(DEx.retrieve_pdf_data())

endpointurl = "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores"
header_details = {'x-api-key': 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}
no_of_stores = DEx.list_number_of_stores(endpointurl, header_details)
e = "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/"
endpointurl = (e + str(0))
pd_stores = DEx.retrieve_stores_data(endpointurl, header_details)
for i in range(0,no_of_stores):
    endpointurl = (e + str(i+1))
    pd_stores_i = DEx.retrieve_stores_data(endpointurl, header_details)
    pd_stores = pd.concat([pd_stores, pd_stores_i], axis="rows")
# end for
store_details = DaC.clean_store_data(pd_stores)

s3_address = "s3://data-handling-public/products.csv"
product_data = DEx.extract_from_s3(s3_address)
clean_products = DaC.clean_products_data(product_data)
#DbC.upload_to_db(clean_products)

orders_df = DaC.clean_orders_data(DEx.read_rds_table("orders"))
#DbC.upload_to_db(orders_df)

s3_address = "https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json"
sales_data = DEx.extract_json_from_s3(s3_address)
clean_sales = DaC.clean_sales_data(sales_data)
'''
DbC.upload_to_db(pd_table, pdf_data, store_details, clean_products, orders_df, sales_data)
