# multinational-retail-data-centralisation

<i>You work for a multinational company that sells various goods across the globe. Currently, their sales data is spread across many different data sources making it not easily accessible or analysable by current members of the team. In an effort to become more data-driven, your organisation would like to make its sales data accessible from one centralised location. Your first goal will be to produce a system that stores the current company data in a database so that it's accessed from one centralised location and acts as a single source of truth for sales data. You will then query the database to get up-to-date metrics for the business.</i>

## Set up the environment.

This consists of getting the Git and GitHub going. 

- familiarised self with the use of command line, file operations and Git/GitHub
- created a new repository in GitHub called multinational-retail-data-centralisation
- added the URL for the remote repository where to push the local repository

## Extract and clean the data from the data sources. 

Besides the installation of PostgreSQL and Pgadmin, an SQL database is created to store the extracted data. Tools are created to extract and clean various kinds of data. 

- familiarised self with VSCode, Python programming, Pandas DataFrames, AWS, APIs and SQL

<b>Task 1</b>

- initialised the database "sales_data" in pgAdmin4

<b>Task 2</b>

- created three Python files for the code: <i>data_extraction.py</i>, <i>database_utils.py</i> and <i>data_cleaning.py</i>
    - data_extraction.py contains a class, DataExtractor, which will be used to extract data from different data sources
    - data_cleaning.py contains a class, DataCleaning, which will be used to clean data acquired with DataExtractor
    - database_utils.py contains a class, DatabaseConnector, which will be used to connect with and upload data to the database
- created file <i>main_programme.py</i> to tie together the code in the aforementioned files

<b>Task 3</b>

The historical data of users is stored in an AWS database in the cloud. First a yaml file was created to contain the credentials needed to connect to the database. These credentials are then read from the file and used to access the data in AWS. 

- in <i>database_utils.py</i>, created the method <i>read_db_creds</i>, which reads credentials yaml file
- in <i>database_utils.py</i>, created the method <i>init_db_engine</i>, to read the credentials and initialise database engine

![multinational-retail-data-centralisation](database_utils-1.png?raw=true "Read credentials from yaml file and initialise database engine.")

- in <i>data_utils.py</i>, created the method <i>list_db_tables</i>, which lists the names of database tables 
- in <i>data_extraction.py</i>, created the method <i>read_rds_tables</i>, which reads the desired database table (the users, in this case) into a Pandas DataFrame

![multinational-retail-data-centralisation](database_utils-2.png?raw=true "Find the names of database tables.")
![multinational-retail-data-centralisation](data_extraction-1.png?raw=true "Read the desired database table.")

Once the user data was read from AWS, it needed to be cleaned to get rid of faulty data, to harmonise formatting of dates and phone numbers, and to improve the style of data throughout the table.

- in <i>data_cleaning.py</i>, created the method <i>clean_user_data</i>, which cleans the table with user data
    - remove rows with n/a in them
    - remove lines where all values are nonsensical garbage
    - change various formattings of birth date and joining date into SI standard
    - correct country codes
    - change phone numbers into international formatting with a leading plus sign (+) and without leading zero (0) in the area code; also convert typically American phone number extensions into formatting of " x 1234" at the end of the phone number
    - change carriage returns in addresses into commas
    - remove duplicate rows
    - sort the data by index column

![multinational-retail-data-centralisation](data_cleaning-1.png?raw=true "Clean the user data table.")

Finally the cleaned used data needed to be stored into the database. The method to do this was later amended with other similar operations. 

- in <i>database_utils.py</i>, created the method <i>upload_to_db</i>, which writes the cleaned user data table into the <i>sales_data</i> database as table <i>dim_users</i>

![multinational-retail-data-centralisation](database_utils-3.png?raw=true "Write cleaned user data into sales_data as dim_users.")

<b>Task 4</b>

Details of the cards of the users are stored in a PDF document that is in an AWS S3 bucket. Once the data was accessed in the PDF document, it was imported with Python package tabula-py into a Pandas DataFrame combining data from several different pages of the document. 

- in <i>data_extraction.py</i>, created the method <i>retrieve_pdf_data</i>, which reads card data from a PDF file into a Pandas DataFrame

![multinational-retail-data-centralisation](data_extraction-2.png?raw=true "Read card data from a PDF file.")

The card data contained inconsistent data and erroneous values, which needed to be cleaned before storing the table into the database. 

- in <i>data_cleaning.py</i>, created the method <i>clean_card_data</i>, which cleans the table with card data
    - remove rows with null values
    - remove non-numeric characters from card number
    - swap month and year in the expiration date, if they are in the wrong order, and remove the rows with incorrect formatting
    - change various formattings of confirmed payment date into SI standard
    - remove duplicate rows

![multinational-retail-data-centralisation](data_cleaning-2.png?raw=true "Clean the card data table.")

- in <i>database_utils.py</i>, updated the method <i>upload_to_db</i> in order to write the cleaned card data into the <i>sales_data</i> database as table <i>dim_card_details</i>

![multinational-retail-data-centralisation](database_utils-4.png?raw=true "Write cleaned card data into sales_data as dim_card_details.")

<b>Task 5</b>

- in <i>data_extraction.py</i>, created the method <i>list_number_of_stores</i> to return the number of stores to extract
- in <i>data_extraction.py</i>, created another method, <i>retrieve_stores_data</i>, which extracts one store at a time from an API connect point and put them into a Pandas DataFrame

![multinational-retail-data-centralisation](data_extraction-3.png?raw=true "Return number of stores and extract their data.")

- in <i>data_cleaning.py</i>, created the method <i>clean_store_data</i>, which cleans the table with store data
    - remove unused column <i>lat</i>
    - fix the online store's locality and address as "online" and longitude and latitude as "0"
    - remove rows with all values as n/a
    - remove rows where all values are nonsensical garbage
    - fix staff numbers by omitting all non-numeric characters
    - change column type of longitude, latitude, and staff_numbers into numerical values
    . correct continent names (by removing "ee" in the beginning)
    - move column <i>latitude</i> next to column <i>longitude</i>
    - change various formattings of opening date into SI standard
    - change carriage returns in addresses into commas
    - remove duplicate rows

![multinational-retail-data-centralisation](data_cleaning-3.png?raw=true "Clean the store data table.")

- in <i>database_utils.py</i>, updated the method <i>upload_to_db</i> in order to write the cleaned store data into the <i>sales_data</i> database as table <i>dim_store_details</i>

![multinational-retail-data-centralisation](database_utils-5.png?raw=true "Write cleaned store data into sales_data as dim_store_details.")

<b>Task 6</b>

- in <i>data_extraction.py</i>, created the method <i>extract_from_s3</i> to download and extract the product data into a Pandas DataFrame

![multinational-retail-data-centralisation](data_extraction-4.png?raw=true "Download and extract product data.")

- in <i>data_cleaning.py</i>, created the method <i>convert_product_weights</i> to clean all weight values and harmonise them to be in <b>kg</b>
- in <i>data_cleaning.py</i>, created another method, <i>clean_product_data</i>, which cleans the table with product data
    - remove rows with null values
    - fix non-standard verbal date values into fully numerical ones
    - remove rows where all values are nonsensical garbage
    - remove non-numeric characters from EAN
    - change various formattings of "date_added" into SI standard
    - sort the data by index column

![multinational-retail-data-centralisation](data_cleaning-4.png?raw=true "Clean the store data table.")

- in <i>database_utils.py</i>, updated the method <i>upload_to_db</i> in order to write the cleaned product data into the <i>sales_data</i> database as table <i>dim_products</i>

![multinational-retail-data-centralisation](database_utils-6.png?raw=true "Write cleaned product data into sales_data as dim_products.")

<b>Task 7</b>

- using earlier established <i>list_db_tables</i> found the name of the table with data on product orders and <i>read_rds_tables</i> to extract this data into a Pandas DataFrame
- in <i>data_cleaning.py</i>, created the method <i>clean_orders_data</i> to clean the table with orders data
    - removed columns first_name, last_name and 1

![multinational-retail-data-centralisation](data_cleaning-5.png?raw=true "Clean the orders data table.")

- in <i>database_utils.py</i>, updated the method <i>upload_to_db</i> in order to write the orders data into the <i>sales_data</i> database as table <i>orders_table</i>

![multinational-retail-data-centralisation](database_utils-7.png?raw=true "Write cleaned orders data into sales_data as orders_table.")

<b>Task 8</b>

- in <i>data_extraction.py</i>, created the method <i>extract_json_from_s3</i>, which extracts the sales date events into a Pandas DataFrame

![multinational-retail-data-centralisation](data_extraction-5.png?raw=true "Download and extract sales date events data.")

- in <i>data_cleaning.py</i>, created the method <i>clean_sales_data</i> to clean the table with sales date events
    - remove rows with n/a in them
    - convert written month names to numbers
    - remove non-numeric charactes from year, month and day
    - remove rows where all values are nonsensical garbage
    - remove duplicate rows
    - convert the timestamp into a time data format
    - combine year, month and day into a date format date
    - rearrange columns so that they are in the order or year, month, day; also make these integers

![multinational-retail-data-centralisation](data_cleaning-6.png?raw=true "Clean the sales date events table.")

- in <i>database_utils.py</i>, updated the method <i>upload_to_db</i> in order to write the sales date events into the <i>sales_data</i> database as table <i>dim_date_times</i>

![multinational-retail-data-centralisation](database_utils-8.png?raw=true "Write cleaned sales date events into sales_data as dim_date_times.")

## Create the database schema.

Tables stored in the pgAdmin database <i>sales_data</i> are modified for a better data retrieval process further on. This involves changing the data types of columns in all tables and changing the structure and contents of tables in some rare cases. 

<b>Task 1</b>

- in <b><i>pgAdmin 4</i></b>, found the maximum length of values in columns "card_number", "store_code" and "product_code" using a command such as this:

![multinational-retail-data-centralisation](schema-1.png?raw=true "Found the maximum length of values in a column.")

- in <b><i>pgAdmin 4</i></b>, changed data types of columns in <i>orders_table</i>

![multinational-retail-data-centralisation](schema-2.png?raw=true "Data types of columns in orders_table.")

- table <i>orders_table</i> after the change

![multinational-retail-data-centralisation](orders_table.png?raw=true "orders_table")

<b>Task 2</b>

- in <b><i>pgAdmin 4</i></b>, changed data types of columns in <i>dim_users_table</i> (the commented ones were already done during table cleaning)

![multinational-retail-data-centralisation](schema-3.png?raw=true "Data types of columns in dim_users.")

- table <i>dim_users</i> after the change

![multinational-retail-data-centralisation](dim_users.png?raw=true "dim_users")

<b>Task 3</b>

- in <b><i>pgAdmin 4</i></b>, changed data types of columns in <i>dim_store_details</i> (the commented one was already done during table cleaning)

![multinational-retail-data-centralisation](schema-4.png?raw=true "Data types of columns in dim_store_details.")

- table <i>dim_store_details</i> after the change

![multinational-retail-data-centralisation](dim_store_details.png?raw=true "dim_store_details")

<b>Task 4</b>

- in <b><i>pgAdmin 4</i></b>, removed the currency symbol (£) from the column <i>product_price</i> in table <i>dim_products</i>

![multinational-retail-data-centralisation](schema-5.png?raw=true "Remove £ character from product_price in dim_products.")

- in <b><i>pgAdmin 4</i></b>, added a new column called <i>weight_class</i> into table <i>dim_products</i>

![multinational-retail-data-centralisation](schema-6.png?raw=true "Added column weight_class into dim_products.")

- in <b><i>pgAdmin 4</i></b>, populated the column <i>weight_class</i> with human-readable version of the weight in table <i>dim_products</i>

![multinational-retail-data-centralisation](schema-7.png?raw=true "Added human-readable version of weight into weight_class in dim_products.")

<b>Task 5</b>

- in <b><i>pgAdmin 4</i></b>, changed data types of columns in <i>dim_products</i> (the commented ones were already done during table cleaning)

![multinational-retail-data-centralisation](schema-8.png?raw=true "Data types of columns in dim_products.")

- in <b><i>pgAdmin 4</i></b>, created a new column called <i>still_available</i> and populated it with boolean values reflecting values in the column <i>removed</i> in table <i>dim_store_details</i>; finally deleted the column <i>removed</i>

![multinational-retail-data-centralisation](schema-9.png?raw=true "Data types of columns in dim_store_details.")

- table <i>dim_products</i> after the changes

![multinational-retail-data-centralisation](dim_products.png?raw=true "dim_products")

<b>Task 6</b>

- in <b><i>pgAdmin 4</i></b>, changed data types of columns in <i>dim_date_times</i>

![multinational-retail-data-centralisation](schema-10.png?raw=true "Data types of columns in dim_date_times.")

- table <i>dim_date_times</i> after the change

![multinational-retail-data-centralisation](dim_date_times.png?raw=true "dim_date_times")

<b>Task 7</b>

- in <b><i>pgAdmin 4</i></b>, changed data types of columns in <i>dim_catd_details</i> (the commented one was already done during table cleaning)

![multinational-retail-data-centralisation](schema-11.png?raw=true "Data types of columns in dim_card_details.")

- table <i>dim_card_details</i> after the change

![multinational-retail-data-centralisation](dim_card_details.png?raw=true "dim_card_details")

<b>Task 8</b>

The task description states that the columns in the tables that begin with "dim" should be updated with a primary key that matches the same column in the <i>orders_table</i>. This was done with the following pgAdmin 4 commands:

![multinational-retail-data-centralisation](schema-12.png?raw=true "Updating primary keys in the dim tables.")

<b>Task 9</b>

The task description states that foreign keys should be created in the <i>orders_table</i> to reference the primary keys in the other tables. This was done to four out of five tables as follows:

![multinational-retail-data-centralisation](schema-13.png?raw=true "Adding foreign keys to the orders_table.")

However, the table <i>dim_users</i> was missing one or more "user_uuid" values that were present in <i>orders_table</i>. In fact, the "user_uuid values were missing also in the raw table that had not been cleaned or modified in any way. Therefore, the following command invoked an error:

![multinational-retail-data-centralisation](schema-14.png?raw=true "Failing to add one more foreign key to the orders_table.")

The problem was solved by doing this in pgAdmin 4: 

![multinational-retail-data-centralisation](schema-15.png?raw=true "Solving the problem of a missing user_uiid and adding one more foreign key to the orders_table.")

## Querying the data.

Milestone description: <i>"Your boss is excited that you now have the schema for the database and all the sales data is in one location. Since you've done such a great job he would like you to get some up-to-date metrics from the data. The business can then start making more data-driven decisions and get a better understanding of its sales. In this milestone, you will be tasked with answering business questions and extracting the data from the database using SQL."</i>

<b>Task 1</b>

Find how many stores are in each of the countries the business operates in. 

![multinational-retail-data-centralisation](result-1.png?raw=true "Number of stores in different countries.")

<b>Task 2</b>

Find the number of stores in the seven locations with the most.

![multinational-retail-data-centralisation](result-2.png?raw=true "Number of stores in different locations.")

<b>Task 3</b>

Find the cost of sales in the six months with the most.

![multinational-retail-data-centralisation](result-3.png?raw=true "Cost of sales in different months.")

<b>Task 4</b>

As preparation for the task, another operation was done to create a new column for whether stores are in the web or offline: 

![multinational-retail-data-centralisation](schema-16.png?raw=true "Created a column for web or offshore identification.")

Find the number of sales between online (web) or offline stores.

![multinational-retail-data-centralisation](result-4.png?raw=true "Number of sales between web and offline stores.")

<b>Task 5</b>

Find the total sales and fraction of the grand total for each store type.

![multinational-retail-data-centralisation](result-5.png?raw=true "Total sales and fraction of grand total per store type.")

<b>Task 6</b>

Find the ten months with the highest sales historically.

![multinational-retail-data-centralisation](result-6.png?raw=true "The months with highest sales.")

<b>Task 7</b>

Find the number of staff in each country. 

![multinational-retail-data-centralisation](result-7.png?raw=true "Number of staff in each country.")

<b>Task 8</b>

Find  the total sales in different store types in Germany.

![multinational-retail-data-centralisation](result-8.png?raw=true "Total sales per store type in Germany.")

<b>Task 9</b>

Find the average time between sales in each year. 

![multinational-retail-data-centralisation](result-9.png?raw=true "Average time between sales per year.")
