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
    # class constructor
    def __init__(self):

        # attributes
        self.credentials = {}
        self.engine = ""

    # methods
    def read_db_creds(self, in_file):
        self.credentials = yaml.load(open('db_creds.yaml'),Loader=yaml.Loader)
    # end read_db_creds

    def init_db_engine(self):
        creds_file = "db_creds.yaml"
        self.read_db_creds(creds_file)

        # ALL VALUES JUST WRITTEN HERE  (THIS WORKS, BUT IS NOT HOW IT SHOULD BE)
        self.engine = create_engine(f"postgresql://aicore_admin:AiCore2022@data-handling-project-readonly.cq2e8zno855e.eu-west-1.rds.amazonaws.com:5432/postgres")
        return self.engine
    # end init_db_engine

    def list_db_tables(self, engine, tableword):
        engine.connect()
        inspector = inspect(engine)
        table_names = inspector.get_table_names()
        # print("Table names = ", table_names)
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
        # store the data in your Sales_Data database in a number of tables
        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        HOST = 'localhost'
        USER = 'postgres'
        PASSWORD = 'rw42.pg,9O'
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


'''
#        print("Type of self.engine is:", type(self.engine))
#        engine = self.init_db_engine()

# Tried this for read_db_creds as well:

#        with open(in_file, "r") as f:
#            for line in f:
#                (key, value) = line.split()  # This works only if the line contains two words, key and value, separated by a space
#                self.credentials[key] = value
#            # end for
#        # end with

#        for k, v in self.credentials.items():
#            print(k, v)


# Tried these for init_db_engine as well: 

#        print("Is", self.credentials['RDS_PORT:'], "(type:", type(int(self.credentials['RDS_PORT:'])), ") a number of all digits:",  self.credentials['RDS_PORT:'].isdigit())

# THIS SHOULD WORK, BUT IT DOES NOT
#        self.engine = create_engine("postgresql://self.credentials['RDS_USER']:self.credentials['RDS_PASSWORD']@self.credentials['HOST']:int(self.credentials['RDS_PORT'])/self.credentials['RDS_DATABASE']")
#
# ERROR:
# ValueError: invalid literal for int() with 
#                           base 10: "']:int(self.credentials['RDS_PORT:'])"

# IT DOES NOT WORK EITHER IF I PUT THE PORT IN AS A NUMBER
#        self.engine = create_engine("postgresql://self.credentials['RDS_USER']:self.credentials['RDS_PASSWORD']@self.credentials['HOST']:5432/self.credentials['RDS_DATABASE']")
#
# ERROR:
# ValueError: invalid literal for int() with base 10: "']}:{5432}"
'''
