import yaml
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from sklearn.datasets import load_iris

class DatabaseConnector:
    '''
    This class is used to connect with and upload data to the database. 
    '''

    def __init__(self):

        # attributes
        self.credentials = {}
        self.engine = ""


    def read_db_creds(self, in_file):

        '''
        Load credentials from a yaml file.
        '''

        self.credentials = yaml.load(open('db_creds.yaml'),Loader=yaml.Loader)
    # end read_db_creds


    def init_db_engine(self):

        '''
        Initiate engine to read data from AWS.
        '''

        creds_file = "db_creds.yaml"
        self.read_db_creds(creds_file)

        # ALL VALUES JUST WRITTEN HERE  (THIS WORKS, BUT IS NOT HOW IT SHOULD BE)
        self.engine = create_engine(f"postgresql://aicore_admin:AiCore2022@data-handling-project-readonly.cq2e8zno855e.eu-west-1.rds.amazonaws.com:5432/postgres")
        return self.engine
    # end init_db_engine


    def list_db_tables(self, engine, tableword):

        '''
        In preparation for extracting a table, find the name of the table based on a keyword (tableword) that should appear in the table name.
        '''

        engine.connect()
        inspector = inspect(engine)
        table_names = inspector.get_table_names()
        for i in range(0,len(table_names)):
            if tableword in table_names[i]:
                table_name = table_names[i]
                break
            else:
                table_name = table_names[0]
            # end if
        # end for
        return table_name
    # end list_db_tables


    def upload_to_db(self, pd_table, pdf_data, store_data, product_data, orders_data, sales_data):

        '''
        Store the data in Sales_Data database in a number of tables.
        '''

        with open('db_password.pw') as pwf:
            password_in = pwf.readline()
            db_password = password_in.strip()
        # end with
        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        HOST = 'localhost'
        USER = 'postgres'
        PASSWORD = db_password
        DATABASE = 'Sales_Data'
        PORT = 5432
        local_engine = create_engine(f"{DATABASE_TYPE}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
        Session = sessionmaker(bind=local_engine)
        with Session() as session:
            df = pd_table
            df.to_sql("dim_users", con=local_engine, if_exists='replace', index=False)
            pdfdf = pdf_data
            pdfdf.to_sql("dim_card_details", con=local_engine, if_exists='replace', index=False)
            sedf = store_data
            sedf.to_sql("dim_store_details", con=local_engine, if_exists='replace', index=False)
            podf = product_data
            podf.to_sql("dim_products", con=local_engine, if_exists='replace', index=False)
            ordf = orders_data
            ordf.to_sql("orders_table", con=local_engine, if_exists='replace', index=False)
            sadf = sales_data
            sadf.to_sql("dim_date_times", con=local_engine, if_exists='replace', index=False)
    # end upload_to_db
