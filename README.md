# multinational-retail-data-centralisation

You work for a multinational company that sells various goods across the globe. Currently, their sales data is spread across many different data sources making it not easily accessible or analysable by current members of the team. In an effort to become more data-driven, your organisation would like to make its sales data accessible from one centralised location. Your first goal will be to produce a system that stores the current company data in a database so that it's accessed from one centralised location and acts as a single source of truth for sales data. You will then query the database to get up-to-date metrics for the business. 

## Milestone 1: Set up the environment.

This consists of getting the Git and GitHub going. 

- prerequisites discussed the use of command line, file operations and Git/GitHub
- created a new repository in GitHub called multinational-retail-data-centralisation
- added the URL for the remote repository where to push the local repository

## Milestone 2: Extract and clean the data from the data sources. 

Besides the installation of PostgreSQL and Pgadmin, an SQL database is created to store the extracted data. Tools are created to extract and clean various kinds of data. 

- prerequisites discussed VSCode, Python programming, Pandas dataframes, AWS, APIs and SQL

<b>Task 1</b>

- initialised the database "sales_data" in pgAdmin4

<b>Task 2</b>

- created files <i>data_extraction.py</i>, <i>database_utils.py</i> and <i>data_cleaning.py</i> to store the code in
- created file <i>main_programme.py</i> to tie the code in the aforementioned files together

<b>Task 3</b>

- in <i>database_utils.py</i>, created the method <i>read_db_creds</i>, which reads credentials yaml file
- in <i>database_utils.py</i>, created the method <i>init_db_engine</i>, to read the credentials and initialise database engine

![multinational-retail-data-centralisation](database_utils-1.png?raw=true "Read credentials from yaml file and initialise database engine.")

- in <i>data_utils.py</i>, created the method <i>list_db_tables</i>, which lists the names of database tables 
- in <i>data_extraction.py</i>, created the method <i>read_rds_tables</i>, which reads the desired database table (the users, in this case) into a Pandas DataFrame

![multinational-retail-data-centralisation](database_utils-2.png?raw=true "Find the names of database tables.")
![multinational-retail-data-centralisation](data_extraction-1.png?raw=true "Read the desired database table.")

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

- in <i>database_utils.py</i>, created the method <i>upload_to_db</i>, which writes the cleaned user data table into the <i>sales_data</i> database as table <i>dim_users</i>

![multinational-retail-data-centralisation](database_utils-3.png?raw=true "Write cleaned user data into sales_data as dim_users.")

<b>Task 4</b>

- in <i>data_extraction.py</i>, created the method <i>retrieve_pdf_data</i>, which reads card data from a PDF file into a Pandas DataFrame

![multinational-retail-data-centralisation](data_extraction-2.png?raw=true "Read card data from a PDF file.")

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

- in <i>data_extraction.py</i>, created the method <i>extract_from_s3 to download and extract the product data into a Pandas DataFrame

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



## Milestone 3: Create the database schema.

## Milestone 4: Querying the data.
