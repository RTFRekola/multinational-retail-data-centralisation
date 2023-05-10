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
- initialised the database "sales_data" in pgAdmin4
- created files <i>data_extraction.py</i>, <i>database_utils.py</i> and <i>data_cleaning.py</i> to store the code in
- created file <i>main_programme.py</i> to tie the code in the aforementioned files together

- in <i>database_utils.py</i>, created a method (<i>read_db_creds</i>), which reads credentials yaml file
- in <i>database_utils.py</i>, created a method init_db_engine, to read the credentials and initialise database engine

![multinational-retail-data-centralisation](database_utils-1.png?raw=true "Read credentials from yaml file and initialise database engine.")

## Milestone 3: Create the database schema.

## Milestone 4: Querying the data.
