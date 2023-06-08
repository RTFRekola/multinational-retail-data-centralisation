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

    def __init__(self):

        # attributes
        self.nothing = []


    def read_rds_table(self, tableword, dbc):

        '''
        Read data from a database into Pandas DataFrame; choose the table by a keyword called tableword.
        '''

        engine = dbc.init_db_engine()
        table_name = dbc.list_db_tables(engine, tableword)
        df = pd.read_sql_table(table_name, engine)
        return df
    # end read_rds_table


    def retrieve_pdf_data(self):

        '''
        Extract content of a pdf file fetched from an online location.
        '''

        pdf_path = "https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf"
        pdfdf = pd.concat(tabula.read_pdf(pdf_path, pages="all", multiple_tables=False))
        return pdfdf
    # end retrieve_pdf_data


    def list_number_of_stores(self, endpointurl, header_dictionary):

        '''
        Return the number of stores to extract.
        '''

        response = requests.get(endpointurl, headers=header_dictionary)
        data = response.json()
        number_of_stores = data['number_stores']
        return number_of_stores
    # end list_number_of_stores


    def retrieve_stores_data(self, endpointurl, header_dictionary):

        '''
        Extract all the stores from the API.
        '''

        response = requests.get(endpointurl, headers=header_dictionary)
        data = response.json()
        try:
            stores_data = pd.DataFrame(data, index=[0])
        except:
            stores_data = pd.DataFrame({'index': 999, 'address': 'N/A', 'longitude': 'N/A', 'lat': 'N/A', 'locality': 'N/A', 
                                        'store_code': 'N/A', 'staff_numbers': 'N/A', 'opening_date': 'N/A', 'store_type': 'N/A', 
                                        'latitude': 'N/A', 'country_code': 'N/A', 'continent': 'N/A'}, index=[0])
        # end try
        return stores_data
    # end retrieve_stores_data


    def extract_from_s3(self, s3_address):

        '''
        Fetch a csv file from S3 and place the contents into a Pandas DataFrame. 
        '''

        the_data = pd.read_csv(s3_address)
        return the_data
    # end extract_from_s3


    def extract_from_s3_no_config(BUCKET_NAME, OBJECT_NAME, FILE_NAME):

        '''
        Fetch a csv file from S3. This version works in case of no AWS account.
        '''

        s3 = boto.client('s3', config=Config(signature_version=UNSIGNED))
        data.csv = s3.download_file(BUCKET_NAME, OBJECT_NAME, FILE_NAME)
        the_data = pd.read_csv('data.csv')
        return product_data
    # end extract_from_s3_no_config


    def extract_json_from_s3(self, s3_address):

        '''
        Fetch a json file from S3 and place the contents into a Pandas DataFrame.
        '''

        the_data = pd.read_json(s3_address)
        return the_data
    # end extract_json_from_s3
