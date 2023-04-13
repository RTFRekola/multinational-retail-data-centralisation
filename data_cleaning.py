import pandas as pd
from datetime import date

class DataCleaning:
    '''
    This class is used to clean data from each of the data sources.
    '''
    # class constructor
    def __init__(self):

        # attributes
        self.nothing = []

    # methods
#----------------------------------------------------------------------------
    def clean_user_data(self, user_data):
        # clean the user data

        def fix_date1(in_date):
            split_str = in_date.split(' ')
            if (len(split_str)==1):
                out_date = in_date
            else:
                if (split_str[1]=="January"):
                    out_month = "01"
                elif (split_str[1]=="February"):
                    out_month = "02"
                elif (split_str[1]=="March"):
                    out_month = "03"
                elif (split_str[1]=="April"):
                    out_month = "04"
                elif (split_str[1]=="May"):
                    out_month = "05"
                elif (split_str[1]=="June"):
                    out_month = "06"
                elif (split_str[1]=="July"):
                    out_month = "07"
                elif (split_str[1]=="August"):
                    out_month = "08"
                elif (split_str[1]=="September"):
                    out_month = "09"
                elif (split_str[1]=="October"):
                    out_month = "10"
                elif (split_str[1]=="November"):
                    out_month = "11"
                elif (split_str[1]=="December"):
                    out_month = "12"
                else:
                    out_month = "00"
                # end if
                out_year = split_str[0]
                out_day = split_str[2]
                out_date = str(out_year) + "-" + str(out_month) + "-" + str(out_day)
            # end if
            return out_date
        # end fix_date1

        def fix_date0(in_date):
            split_str = in_date.split(' ')
            if (47 < ord(in_date[0][0]) < 58):
                out_date = in_date
            else:
                if (split_str[0]=="January"):
                    out_month = "01"
                elif (split_str[0]=="February"):
                    out_month = "02"
                elif (split_str[0]=="March"):
                    out_month = "03"
                elif (split_str[0]=="April"):
                    out_month = "04"
                elif (split_str[0]=="May"):
                    out_month = "05"
                elif (split_str[0]=="June"):
                    out_month = "06"
                elif (split_str[0]=="July"):
                    out_month = "07"
                elif (split_str[0]=="August"):
                    out_month = "08"
                elif (split_str[0]=="September"):
                    out_month = "09"
                elif (split_str[0]=="October"):
                    out_month = "10"
                elif (split_str[0]=="November"):
                    out_month = "11"
                elif (split_str[0]=="December"):
                    out_month = "12"
                else:
                    out_month = "00"
                # end if
                out_year = split_str[1]
                out_day = split_str[2]
                out_date = str(out_year) + "-" + str(out_month) + "-" + str(out_day)
            # end if
            return out_date
        # end fix_date0

        def fix_phone(in_tel, country):
            counter = 0
            out_tel = "+"
            if (in_tel[counter:counter+1] == "+"):
                counter = counter + 1
            # end if

            if ((in_tel[counter:counter+1] == "1") and (country=="US")):
                out_tel = out_tel + "1"
                counter = counter + 1
            elif (country=="US"):
                out_tel = out_tel + "1"
            # end if

            if ((in_tel[counter:counter+2] == "44") and (country=="GB")):
                out_tel = out_tel + "44"
                counter = counter + 2
            elif (country=="GB"):
                out_tel = out_tel + "44"
            # end if

            if ((in_tel[counter:counter+2] == "49") and (country=="DE")):
                out_tel = out_tel + "49"
                counter = counter + 2
            elif (country=="DE"):
                out_tel = out_tel + "49"
            # end if

            if (in_tel[counter:counter+3] == " (0"):
                counter = counter + 3
            elif (in_tel[counter:counter+2] == "(0"):
                counter = counter + 2
            elif (in_tel[counter:counter+1] == "0"):
                counter = counter + 1
            # end if

            for ix in range (counter,len(in_tel)):
                if (47 < ord(in_tel[ix:ix+1]) < 58):
                    out_tel = out_tel + in_tel[ix:ix+1]
                elif (in_tel[ix:ix+1] == "x"):
                    out_tel = out_tel + " extension "
                # end if
            # end for
            return out_tel
        # end fix_phone


        # 1. remove rows with n/a in them
        user_data = user_data.dropna()

        # 2. remove lines with garbage 
        mask = (user_data['date_of_birth'].apply(lambda x: False if x[0].isdigit() else True) & user_data['join_date'].apply(lambda x: False if x[0].isdigit() else True) & user_data['phone_number'].apply(lambda x: False if x[-1].isdigit() else True))
        user_data = user_data.drop(user_data[mask].index)
        mask = (user_data['date_of_birth'].apply(lambda x: False if x[0].isdigit() else True) | user_data['date_of_birth'].apply(lambda x: False if x[-1].isdigit() else True))
        user_data = user_data.drop(user_data[mask].index)

        # 3. change formatting of date_of_birth and join_date into YYYY-MM-DD 
        #    and the type into a date type
        user_data['date_of_birth'] = user_data.apply(lambda row : fix_date0(row['date_of_birth']), axis = 1)
        user_data['date_of_birth'] = user_data.apply(lambda row : fix_date0(row['join_date']), axis = 1)
        user_data['date_of_birth'] = user_data.apply(lambda row : fix_date1(row['date_of_birth']), axis = 1)
        user_data['join_date'] = user_data.apply(lambda row : fix_date1(row['date_of_birth']), axis = 1)
        user_data['date_of_birth'] = pd.to_datetime(user_data['date_of_birth'], format='%Y-%m-%d').dt.date
        user_data['join_date'] = pd.to_datetime(user_data['join_date'], format='%Y-%m-%d').dt.date

        # 4. replace the 6 incorrect country codes
        user_data.replace('GGB', 'GB', inplace=True)

        # 5. verify country codes so that they are correct for the country 
        #    mentioned in the column 'country'
        ###  (apparently there are no such errors)

        # 6. change phone numbers into formatting +0012345678, where 00 is 
        #    the country code and what follows is the area code and phone
        #    number without spaces or parentheses; with 1 the leading 0 can
        #    be omitted
        user_data['phone_number'] = user_data.apply(lambda row : fix_phone(row['phone_number'], row['country_code']), axis = 1)

        # 7. change carriage returns into commas in address
        user_data = user_data.replace(r'\n',', ', regex=True)
        
        # 8. remove duplicate rows
        user_data = user_data.drop_duplicates()

        # 9. sort by the index column (not really needed, but maybe fun)
        #clean_data = user_data #.sort_values(by = 'index')
        user_data = user_data.sort_values(by='index')

        return user_data
    # end clean_user_data

#----------------------------------------------------------------------------
    def clean_card_data(self, card_data):
        # clean card data from the pdf file

        def fix_expiry(in_exp):
            qmonth = int(in_exp[:2])
            qyear = int(in_exp[-2:])
            if (qmonth>12 and qyear<13):
                qtemp = qmonth
                qmonth = qyear
                qyear = temp
            # end if
            lzero = ""
            if (int(qmonth)<10):
                lzero = "0"
            out_exp = lzero + str(qmonth) + "/" + str(qyear)
            return out_exp
        # end fix_expiry

        def fix_cardno(in_cno):
            out_cno = ""
            for i in range(0,len(in_cno)):
                if (47 < ord(in_cno[i:i+1]) < 58):
                    out_cno = out_cno + in_cno[i:i+1]
                # end if
            # end for
            return out_cno
        # end fix_cardno

        # 1. remove lines with null values
        card_data = card_data.dropna()

        # 2. remove non-numeric characters from card_number
        #card_data['card_number'] = card_data['card_number'].map(lambda x: ''.join([i for i in str(x) if i.isdigit()]))
        #card_data['card_number'] = card_data['card_number'].str.replace(r'[^0-9]+', '')
        card_data['card_number'] = card_data.apply(lambda row: fix_cardno(row['card_number']), axis=1)

        # 3. change column type of card_number into number
#        card_data[['card_number']] = card_data[['card_number']].apply(pd.to_numeric)

        # 4. remove lines where card number < 1,000,000
#        card_data = card_data.drop(card_data[card_data.card_number < 1000000].index)

        # 5. swap month/year in expiry_date, if month > 12 and year < 13
        #    (assuming they are then in the wrong order), remove lines where
        #    the formatting is not ##/##
        card_data = card_data[card_data.expiry_date.str.len() == 5]
        card_data['expiry_date'] = card_data.apply(lambda row: fix_expiry(row['expiry_date']), axis=1)

        # at this point, let's convert expiry_date into %m/%Y
#        card_data['expiry_date'] = card_data['expiry_date'].datetime.strftime('%m/%y')
#        card_data['expiry_date'] = pd.to_datetime(card_data['expiry_date']).dt.date

        # 6. change formatting of date_payment_confirmed into YYYY-MM-DD and 
        #    the type into a date type
        card_data['date_payment_confirmed'] = pd.to_datetime(card_data['date_payment_confirmed']).dt.date

        # 7. remove duplicate rows
        card_data = card_data.drop_duplicates()

        return card_data
    # end clean_card_data

#----------------------------------------------------------------------------
    def clean_store_data(self, store_data):
        # clean store data retrieve from the API

        # 1. remove column lat
        #del store_data['lat']
        
        # 2. fix row 48, index 0, so that address and locality are "online" 
        #    and longitude and latitude are "0"

        #store_data = store_data.reset_index()

        #store_data.rename(index={0:451},inplace=True)

        #store_data = store_data.sort_values(by='index')

        #store_data.iloc[48,1] = "online"
        #store_data.iloc[48,2] = "0"
        #store_data.iloc[48,3] = "online"
        #store_data.iloc[48,8] = "0"

        # 3. remove rows with n/a in them
        #store_data = store_data.dropna()

        # 4. remove lines with garbage (values in longitude OR latitude 
        # are not numbers) - including indexes 218, 406, 437 (all 'NULL') 
        #store_data = store_data[pd.to_numeric(store_data['longitude'], errors='coerce').notnull()]

        # 5. fix index 31: staff_numbers = 'J78'  (apply fix to all rows)
        #store_data['staff_numbers'] = store_data['staff_numbers'].map(lambda x: ''.join([i for i in x if i.isdigit()]))

        # 6. change column type of longitude, latitude, staff_numbers into 
        #    numbers
        #store_data[['longitude', 'latitude', 'staff_numbers']] = store_data[['longitude', 'latitude', 'staff_numbers']].apply(pd.to_numeric)

        # 7. correct continent names (remove 'ee')
        #store_data.replace('eeEurope', 'Europe', inplace=True)
        #store_data.replace('eeAmerica', 'America', inplace=True)

        # 8. move column latitude next to column longitude
        #store_data = store_data[['index', 'address', 'longitude', 'latitude', 'locality', 'store_code', 'staff_numbers', 'opening_date', 'store_type', 'country_code', 'continent']]

        # 9. change formatting of opening_date into YYYY-MM-DD and the type 
        #    into a date type
        #store_data['opening_date'] = pd.to_datetime(store_data['opening_date']).dt.date

        # 10. change carriage returns into commas in address
        #store_data = store_data.replace(r'\n',', ', regex=True)
        
        # 11. remove duplicate rows
        #store_data = store_data.drop_duplicates()

        # 12. restore n/a to row 48, the "web portal"
#        replace_with_na_all(data = store_data, condition = 'longitude' == 0)
#        replace_with_na_all(data = store_data, condition = 'latitude' == 0)
#        replace_with_na_all(data = store_data, condition = 'address' == "online")
#        replace_with_na_all(data = store_data, condition = 'locality' == "online")

        # 13. sort by the index column (not really needed, but maybe fun)
        #store_data = store_data.sort_values(by='index')

        return store_data
    # end clean_store_data

#----------------------------------------------------------------------------
    def convert_product_weights(self, prd):
        # convert product weights into kilograms

        def actual_conversion(product_weight):
            x = 0 ; y = 1
            for i in range(0,len(product_weight)):
                if (str(product_weight[i:i+3]) == " x "):
                    y = int(product_weight[:i])
                    x = i + 3
                    exit
                # end if
            # end for
            for i in range(x,len(product_weight)):
                if (47 < ord(product_weight[i:i+1]) < 58):
                    still_no = i
                else:
                    exit
                # end if
            # end for
            # print("Product weight: ", product_weight)
            prdvalue = y * float(product_weight[x:still_no+1])
            prdunit = str(product_weight[still_no+1:])
            # print("Product value and unit: ", prdvalue, " ", prdunit)
            if ((prdunit == "l") or (prdunit == "kg")):
                prdvalue = prdvalue
            elif ((prdunit == "ml") or (prdunit == "g")):
                prdvalue = prdvalue / 1000
            elif (prdunit == "oz"):
                prdvalue = prdvalue * 28.35 / 1000
            elif (prdunit == "g ."):
                prdvalue = prdvalue / 1000
            else:
                print("Anomaly! Product unit is ", prdunit)
            # end if
            product_data = prdvalue
            return product_data
        # end actual_conversion

        prd['weight'] = prd.apply(lambda row: actual_conversion(row['weight']), axis=1)
        return prd
    # end convert_product_weights

#----------------------------------------------------------------------------
    def clean_products_data(self, product_data):
        # clean the product data

        def fix_ean(in_ean):
            out_ean = ""
            for i in range(0,len(in_ean)):
                if (47 < ord(in_ean[i:i+1]) < 58):
                    out_ean = out_ean + in_ean[i:i+1]
                # end if
            # end for
            return out_ean
        # end fix_ean

        def fix_date(in_date):
            out_date = in_date
            if (in_date[0:3]=='Sep'):
                out_date = (in_date[10:14] + '-09-' + in_date[-2:])
            elif (in_date[5:8]=='Oct'):
                out_date = (in_date[0:4] + '-10-' + in_date[-2:])
            # end if
            return out_date
        # end fix_date

        # 1. remove lines with null values
        product_data = product_data.dropna()

        # 2. fix non-standard dates
        product_data['date_added'] = product_data.apply(lambda row: fix_date(row['date_added']), axis=1)

        # 3. remove lines with garbage 
        mask = (product_data['date_added'].apply(lambda x: False if x[0].isdigit() else True) & product_data['product_price'].apply(lambda x: False if x[-1].isdigit() else True) & product_data['weight'].apply(lambda x: False if x[0].isdigit() else True))
        product_data = product_data.drop(product_data[mask].index)
        mask = (product_data['date_added'].apply(lambda x: False if x[0].isdigit() else True) | product_data['date_added'].apply(lambda x: False if x[-1].isdigit() else True))
        product_data = product_data.drop(product_data[mask].index)

        # 4. remove non-numeric characters from EAN
        product_data['EAN'] = product_data.apply(lambda row: fix_ean(row['EAN']), axis=1)

        # 5. change formatting of date_added into YYYY-MM-DD and the type 
        #    into a date type
        product_data['date_added'] = pd.to_datetime(product_data['date_added']).dt.date

        # 6. fix product weights (in a separate method)
        product_data = self.convert_product_weights(product_data)

        # 7. sort by the index column (not really needed, but maybe fun)
        product_data = product_data.sort_values(by=product_data.columns[0])

        return product_data
    # end clean_products_data

#----------------------------------------------------------------------------
    def clean_orders_data(self, orders_data):
        # clean the orders table data

        # 1. remove columns first_name, last_name and 1
        del orders_data['1']
        del orders_data['first_name']
        del orders_data['last_name']

        return orders_data
    # end clean_orders_data

#----------------------------------------------------------------------------
    def clean_sales_data(self, sales_data):
        # clean the sales data

        def fix_month(in_month):
            if (in_month=="January"):
                out_month = "1"
            elif (in_month=="February"):
                out_month = "2"
            elif (in_month=="March"):
                out_month = "3"
            elif (in_month=="April"):
                out_month = "4"
            elif (in_month=="May"):
                out_month = "5"
            elif (in_month=="June"):
                out_month = "6"
            elif (in_month=="July"):
                out_month = "7"
            elif (in_month=="August"):
                out_month = "8"
            elif (in_month=="September"):
                out_month = "9"
            elif (in_month=="October"):
                out_month = "10"
            elif (in_month=="November"):
                out_month = "11"
            elif (in_month=="December"):
                out_month = "12"
            else:
                out_month = in_month
            # end if
            return out_month
        # end fix_month

        def fix_numbers(in_val):
            out_val = ""
            for i in range(0,len(in_val)):
                if (47 < ord(in_val[i:i+1]) < 58):
                    out_val = out_val + in_val[i:i+1]
                # end if
            # end for
            return out_val
        # end fix_numbers

        # 1. remove rows with n/a in them
        #sales_data['timestamp'].replace('', np.nan, inplace=True)
        sales_data[sales_data['timestamp'].str.strip().astype(bool)]
        sales_data[sales_data['year'].str.strip().astype(bool)]
        sales_data[sales_data['month'].str.strip().astype(bool)]
        sales_data[sales_data['day'].str.strip().astype(bool)]
        sales_data = sales_data.dropna()

        # 2. convert written month names to numbers
        sales_data['month'] = sales_data.apply(lambda row : fix_month(row['month']), axis = 1)

        # 3. remove non-numeric characters from month, year and day
        sales_data['month'] = sales_data.apply(lambda row: fix_numbers(row['month']), axis=1)
        sales_data['year'] = sales_data.apply(lambda row: fix_numbers(row['year']), axis=1)
        sales_data['day'] = sales_data.apply(lambda row: fix_numbers(row['day']), axis=1)

        # 4. remove lines with garbage 
        # Here we could have a process to check whether there is a 
        # ##:##:## substring in the 'timestamp' and drop all the other
        # characters. However, for the time being, let's skip this.
        try:
            mask = (sales_data['timestamp'].apply(lambda x: False if x[0].isdigit() else True) | sales_data['timestamp'].apply(lambda x: False if x[-1].isdigit() else True) | sales_data['timestamp'].apply(lambda x: False if x[1].isdigit() else True) | sales_data['timestamp'].apply(lambda x: False if x[-2].isdigit() else True))
            sales_data = sales_data.drop(sales_data[mask].index)
            mask = (sales_data['year'].apply(lambda x: False if x[0].isdigit() else True) & sales_data['year'].apply(lambda x: False if x[-1].isdigit() else True))
            sales_data = sales_data.drop(sales_data[mask].index)
            mask = (sales_data['year'].apply(lambda x: False if x>1900 else True) | sales_data['year'].apply(lambda x: False if not x=='' else True))
            sales_data = sales_data.drop(sales_data[mask].index)
        except:
            print("Could not remove all lines with garbage succssfully.")
        # end try

        # 5. remove duplicate rows
        sales_data = sales_data.drop_duplicates()

        # 6. convert timestamp into a time data format
        sales_data['timestamp'] = pd.to_datetime(sales_data['timestamp'],format= '%H:%M:%S' ).dt.time

        # 7. combine year, month and day into a date format date
        sales_data['date'] = pd.to_datetime(sales_data.year+sales_data.month+sales_data.day,format='%Y%m%d').dt.date

        # 8. whether they even need to be kept, rearrange year, month, and
        #    day columns and make them integers
        sales_data = sales_data[['date', 'timestamp', 'year', 'month', 'day', 'time_period', 'date_uuid']]
        sales_data[['year', 'month', 'day']] = sales_data[['year', 'month', 'day']].apply(pd.to_numeric)

        return sales_data
    # end clean_sales_data

#----------------------------------------------------------------------------

'''
# For testing:
        print(type(user_data))
        print(user_data.shape[0])
        print(user_data.iloc[0])

# In def clean_user_data

# 3.
        user_data = user_data.drop(user_data[(not user_data.longitude.str.isdigit()) | (not user_data.latitude.str.isdigit())].index)
# or
        user_data = user_data.drop(user_data[(user_data[not user_data.longitude.str.isdigit()]) | (user_data[not user_data.latitude.str.isdigit()])].index)
# or
        user_data = user_data.drop(user_data[(not user_data['longitude'].str.isdigit()) | (not user_data['latitude'].str.isdigit())].index)
# or
        user_data = user_data.drop(user_data[user_data[(not user_data.longitude.str.isdigit())]].index)
# or
        user_data = user_data[user_data['longitude'].apply(lambda x: type(x) in [float])]
# or
        user_data = user_data.query('longitude.str.isnumeric()')


# 4.
        user_data['staff_numbers'] = user_data.staff_numbers.str.replace(r"[a-zA-Z]",'')
# or
        user_data['staff_numbers'] = user_data['staff_numbers'].str.replace(r"[^0-9]+",'')

# 8.
        user_data = user_data.drop('lat', axis=1)

# In def clean_card_data

# 2.
        user_data = user_data[pd.to_numeric(user_data['email_address'], errors='coerce').notnull()]
        mask = (((ord(str(user_data['date_of_birth[0]'])) < 48) | (ord(str(user_data['date_of_birth[0]'])) > 57)) & ((ord(str(user_data['join_date[0]'])) < 48) | (ord(str(user_data['join_date[0]'])) > 57)) & 47 < ord(str(user_data['phone_number[-1]'])) < 58)
        mask = (((ord(user_data['date_of_birth'[0]].str) < 48) | (ord(user_data['date_of_birth'[0]].str) > 57)) & ((ord(user_data['join_date'[0]].str) < 48) | (ord(user_data['join_date'[0]].str) > 57)) & 47 < ord(user_data['phone_number'[-1]].str) < 58)

# 3. 
        #user_data = user_data.apply(lambda x: fix_date0(x) if x.name=='join_date' else x)
        #user_data = user_data.apply(lambda x: fix_date1(x) if x.name=='date_of_birth' else x)
        #user_data = user_data.apply(lambda x: fix_date1(x) if x.name=='join_date' else x)

# 5.
        card_data['length'] = card_data.expiry_date.str.len()
        card_data = card_data[card_data.length == 5]
        del card_data['length']
        # let's extract MM into a new column called 'inmo' and year to 'inyr'
        card_data['inmo'] = card_data['expiry_date'].str[:2]
        card_data['inyr'] = card_data['expiry_date'].str[3:]
        card_data[['inmo', 'inyr']] = card_data[['inmo', 'inyr']].apply(pd.to_numeric)
        mask = ((card_data['inmo'] > 12) & (card_data['inyr'] < 13))
        temp = card_data.loc[mask, 'inmo']
        card_data.loc[mask, 'inmo'] = card_data.loc[mask, 'inyr']
        card_data.loc[mask, 'inyr'] = temp
        card_data['inmo'] = card_data['inmo'].astype("string")
        card_data['inyr'] = card_data['inyr'].astype("string")
        card_data['expiry_date'] = card_data[['inmo', 'inyr']].agg('/'.join, axis=1)
        del card_data['inmo']  ;  del card_data['inyr']


# ???
        card_data['middle'] = card_data.expiry_date[2]
        card_data = card_data[card_data.middle == '/']
        del card_data['middle']
        card_data['ismonth'] = int(card_data['expiry_date'][:2])
        card_data['isyear'] = int(card_data['expiry_date'][3:])
        card_data = card_data[isinstance(card_data.ismonth, int) & isinstance(card_data.isyear, int)]
        del card_data['ismonth']  ;  del card_data['isyear']

# the previous 7 lines of code or the following 4 lines

        card_data = card_data.drop(card_data[len(card_data['expiry_date'])!=5].index)
        card_data = card_data.drop(card_data[type(card_data['expiry_date'][:2])!="int"].index)
        card_data = card_data.drop(card_data[type(card_data['expiry_date'][2:3])!="/"].index)
        card_data = card_data.drop(card_data[type(card_data['expiry_date'][3:])!="int"].index)


     CAST(NULLIF(column, ’N/A’) AS FLOAT)   
'''
