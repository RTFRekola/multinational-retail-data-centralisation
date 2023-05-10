import boto3
import tabula
import requests
import pandas as pd
from pandas import DataFrame
from database_utils import DatabaseConnector
from botocore import UNSIGNED
from botocore.config import Config

class DataExtractor:
    '''
    This class is used to extract data from different data sources. 
    '''
    # class constructor
    def __init__(self):

        # attributes
        self.nothing = []

    # methods
    def read_rds_table(self, tableword):
        # extract the database table to a pandas DataFrame
        dbc = DatabaseConnector()
        engine = dbc.init_db_engine()
        table_name = dbc.list_db_tables(engine, tableword)
        df = pd.read_sql_table(table_name, engine)
        return df
    # end read_rds_table

    def retrieve_pdf_data(self):
        # extract content of pdf from an online location
        pdf_path = "https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf"
        pdfdf = pd.concat(tabula.read_pdf(pdf_path, pages="all", multiple_tables=False))
        return pdfdf
    # end retrieve_pdf_data

    def list_number_of_stores(self, endpointurl, header_dictionary):
        # return the number of stores to extract
        response = requests.get(endpointurl, headers=header_dictionary)
        data = response.json()
        number_of_stores = data['number_stores']
        return number_of_stores
    # end list_number_of_stores

    def retrieve_stores_data(self, endpointurl, header_dictionary):
        # extract all the stores from the API
        response = requests.get(endpointurl, headers=header_dictionary)
        data = response.json()
        #print(data)
        #stores_data = DataFrame(data)
        try:
            stores_data = pd.DataFrame(data, index=[0])
        except:
            stores_data = pd.DataFrame({'index': 999, 'address': 'N/A', 'longitude': 'N/A', 'lat': 'N/A', 'locality': 'N/A', 
                                        'store_code': 'N/A', 'staff_numbers': 'N/A', 'opening_date': 'N/A', 'store_type': 'N/A', 
                                        'latitude': 'N/A', 'country_code': 'N/A', 'continent': 'N/A'}, index=[0])
        # end try
        return stores_data
    # end retrieve_stores_data

    def extract_from_s3_no_config(BUCKET_NAME, OBJECT_NAME, FILE_NAME):
        s3 = boto.client('s3', config=Config(signature_version=UNSIGNED))
        s3.download_file(BUCKET_NAME, OBJECT_NAME, FILE_NAME)
        return product_data
    # end extract_from_s3_no_config

    def extract_from_s3(self, s3_address):
        #aws_credentials = { "key": "***", "secret": "***", "token": "***" }
        #the_data = pd.read_csv(s3_address, storage_options=aws_credientials)
        the_data = pd.read_csv(s3_address)
        return the_data
    # end extract_from_s3

    def extract_json_from_s3(self, s3_address):
        #aws_credentials = { "key": "***", "secret": "***", "token": "***" }
        #the_data = pd.read_csv(s3_address, storage_options=aws_credientials)
        the_data = pd.read_json(s3_address)
        return the_data
    # end extract_json_from_s3


'''
# Tried these as well for retrieve_pdf_data: 

        # pdfdfs = tabula.read_pdf(pdf_path, pages="all")
        # the above line could also be like this and the line after it could
        # be omitted: 

        #pdfdf = pd.DataFrame(tabula.read_pdf(pdf_path, pages="all")[0])

        ## pdfdf = tabula.read_pdf(pdf_path, pages="all")
        ## pdfdf = pd.concat(pdfdfs)

#        df_list = []
#        for page in range(1, tabula.io.count_pages(pdf_path) + 1):
#            pdfdf = tabula.io.read_pdf(pdf_path, pages=page)[0]
#            df_list.append(pdfdf)
#        pdfdf = pd.concat(df_list, ignore_index=True)

##        df_list = tabula.read_pdf_with_template(pdf_path, multiple_tables=True)
##        pdfdf = pd.concat(df_list, ignore_index=True)

        #pdfdfs = tabula.read_pdf(pdf_path, pages="all")
        #pdfdf = pd.concat(pdfdfs, ignore_index=True)

# This apparently gives headers from first page to all pages:

        pdfdfs = tabula.read_pdf(filename, pages='all', pandas_options={'header': None})
        cols = tables[0].values.tolist()[0]
        tables[0] = tables[0].iloc[1:]
        for df in tables: df.columns = cols

'''
