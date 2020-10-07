#!/usr/bin/env python
# coding: utf-8
import findspark
findspark.init()

import math
from pyspark.sql import Row
import re
from pyspark.sql import SQLContext
import pycountry
from pyspark.sql import SparkSession
from pyspark.sql.types import ArrayType, StructField, StructType, StringType, IntegerType,FloatType
from pyspark.sql.functions import lit
from streetaddress import StreetAddressFormatter, StreetAddressParser
import os




def check_country(country: str) -> str:
    '''
    Changes the country name in order to be properly mapped .
    Unrecognised country are mapped to other
    '''
    if len(country) == 2:
        result = pycountry.countries.get(alpha_2=country)
    elif len(country) == 3:
        result = pycountry.countries.get(alpha_3=country)
    else:
        result = pycountry.countries.get(name=country.replace("The ",""))
    if result is None:
        return "Other"
    else:
        return result.name
    
def get_street_standard(address: str) -> str:
    '''
    extract the street name from the adress .
   '''
    addr_parser = StreetAddressParser()
    addr = addr_parser.parse(address) 
    street = f"{re.sub(r'[^A-Za-z0-9 ]+', '', addr.get('street_name'))} {addr.get('street_type')}"
    return street

def rowwise_function_tripadvisor(row):
    # convert row to dict:
    row_dict = row.asDict()
    # Add a new key in the dictionary with the new column name and value. 
    row_dict['country'] = check_country(row_dict['country'])
    row_dict['address'] = row_dict['address'].replace(row_dict['country'],'').strip(',') 
    if row_dict['country'] in ['Germany', 'Netherlands']:
        regex = '([A-ZÄÖÜ][a-zäöüß]+(([.] )|( )|([-])))+[1-9][0-9]{0,3}[a-z]?'
        regex_search = re.search(regex, row_dict.get('street',row_dict['address']), re.IGNORECASE)
        if regex_search:
            row_dict['street'] = regex_search.group(0)
        else:
            row_dict['street'] = ''
    else:
        row_dict['street'] = get_street_standard(row_dict.get('street',row_dict['address']))
    # convert dict to row:
    row_dict['id'] = f"{row_dict['name']}-{row_dict['street']}-{row_dict['country']}"
    newrow = Row(**row_dict)
    # return new row
    return newrow

def rowwise_function_ubereats(row):
    '''
    preprocess row of the data frame.
    Futher transformation can be added (feature from string to array), but I will limit myself to api needs
    '''
    # convert row to dict:
    row_dict = row.asDict()
    # Add a new key in the dictionary with the new column name and value. 
    row_dict['country'] = check_country(row_dict['country'])
    row_dict['address'] = row_dict['address'].replace(row_dict['country'],'').strip(',') 
    if row_dict['country'] in ['Germany', 'Netherlands']:
        regex = '([A-ZÄÖÜ][a-zäöüß]+(([.] )|( )|([-])))+[1-9][0-9]{0,3}[a-z]?'
        regex_search = re.search(regex, row_dict.get('street',row_dict['address']), re.IGNORECASE)
        if regex_search:
            row_dict['street'] = regex_search.group(0)
        else:
            row_dict['street'] = ''
    else:
        row_dict['street'] = get_street_standard(row_dict.get('street',row_dict['address']))
    # convert dict to row:
    row_dict['id'] = f"{row_dict['name']}-{row_dict['street']}-{row_dict['country']}"
    try:
        row_dict['reviews_nr'] = float(row_dict['reviews_nr'])
    except ValueError:
        row_dict['reviews_nr'] = None

    newrow = Row(**row_dict)
    # return new row
    return newrow

def rowwise_function_menu(row):
    # convert row to dict:
    row_dict = row.asDict()
    # Add a new key in the dictionary with the new column name and value. 
    # convert dict to row:
    try:
        row_dict['volume'] = float(row_dict['volume'])
    except ValueError:
        row_dict['volume'] = None
    
    newrow = Row(**row_dict)
    # return new row
    return newrow

if __name__=="__main__":
    appName = "Dashmode"
    master = "local"

    # Create Spark session
    spark = SparkSession.builder.appName(appName).master(master).getOrCreate()

    # Create a schema for the dataframe ubereat_outlet
    schema = StructType([
        StructField('id_outlet', StringType(), True),
        StructField('country', StringType(), True),
        StructField('name', StringType(), True),
        StructField('address', StringType(), True),
        StructField('reviews_nr', StringType(), True),
    ])


    # Create a schema for the dataframe tripadvisor_outlet
    schema_outlet = StructType([
        StructField('address', StringType(), True),
        StructField('city', StringType(), True),
        StructField('country', StringType(), True),
        StructField('cuisines', StringType(), True),
        StructField('features', StringType(), True),
        StructField('id_outlet', StringType(), True),
        StructField('lat', FloatType(), True),
        StructField('lon', FloatType(), True),
        StructField('menu', StringType(), True),
        StructField('name', StringType(), True),
        StructField('opening_hours', StringType(), True),
        StructField('phone', StringType(), True),
        StructField('postal_code', StringType(), True),
        StructField('price_level', StringType(), True),
        StructField('price_range', StringType(), True),
        StructField('rating', FloatType(), True),
        StructField('region', StringType(), True),
        StructField('reviews_nr', FloatType(), True),
        StructField('special_diets', StringType(), True),
        StructField('street', StringType(), True),
        StructField('tags', StringType(), True),
        StructField('url', StringType(), True),
        StructField('website', StringType(), True),
    ])

    # Create a schema for the dataframe ubereats menu
    schema_menu = StructType([
        StructField('id_outlet', StringType(), True),
        StructField('name', StringType(), True),
        StructField('brand', StringType(), True),
        StructField('price', FloatType(), True),
        StructField('volume', StringType(), True),
    ])


    # Create data frame for uberts eats
    json_file_path = 'ubereats_outlet.json'
    df_outlet_ue = spark.read.json(json_file_path, schema, multiLine=True)
    # print(df.schema)
    df_outlet_ue = df_outlet_ue.withColumn('source', lit('ubereats'))
    # convert uberts dataframe to RDD
    df_outlet_ue_rdd = df_outlet_ue.rdd
    # apply our function to RDD
    df_outlet_ue_rdd_new = df_outlet_ue_rdd.map(lambda row: rowwise_function_ubereats(row))
    # Convert RDD Back to DataFrame
    df_outlet_ue_new = df_outlet_ue_rdd_new.toDF()
    df_outlet_ue_new = df_outlet_ue_new.dropDuplicates(['id'])
    # df_outlet_ue_new = df_outlet_ue_new.drop('country')


    # Create data frame for trip advisor
    json_file_path = 'tripadvisor_outlet.json'
    df_outlet = spark.read.json(json_file_path, schema_outlet, multiLine=True)
    df_outlet = df_outlet.withColumn('source', lit('tripadvisor'))
    # convert trip advisor dataframe to RDD
    df_outlet_rdd = df_outlet.rdd
    # apply our function to RDD
    df_outlet_rdd_new = df_outlet_rdd.map(lambda row: rowwise_function_tripadvisor(row))
    # Convert RDD Back to DataFrame
    df_outlet_new = df_outlet_rdd_new.toDF()
    df_outlet_new = df_outlet_new.dropDuplicates(['id'])
    # df_outlet_new.show(2)
    # df_outlet_ue_new = df_outlet_ue_new.drop('country')


    # Join dataframe 
    outlet = df_outlet_new.join(df_outlet_ue_new, on=['id','id_outlet', 'country', 'name', 'address', 'reviews_nr', 'street','source'], how='outer')
    outlet = outlet.dropDuplicates(['id'])

    # outlet = outlet.replace("NaN",None)



    # Create data frame for ubereats menu
    json_file_path = 'ubereats_menu.json'
    df_menu = spark.read.json(json_file_path, schema_menu, multiLine=True)
    # print(df.schema)
    df_menu = df_menu.withColumn('source', lit('ubereats'))
    df_menu_rdd = df_menu.rdd
    # apply our function to RDD
    df_menu_rdd_new = df_menu_rdd.map(lambda row: rowwise_function_menu(row))
    # Convert RDD Back to DataFrame
    df_menu_new = df_menu_rdd_new.toDF()
    # get outlet id
    menu = df_menu_new.join(outlet[['id_outlet','id']], on=['id_outlet'], how='left_outer')


    # Add data to postgresql

    # outlet_url = 'postgresql://localhost:5432/app_db'
    outlet_url = os.environ['PG_JDBC_URL']
    properties = {
        "driver": "org.postgresql.Driver",
        "user": os.environ['PG_JDBC_USER'],
        "password": os.environ['PG_JDBC_PASS']
    }



    outlet.write.jdbc(
    url=outlet_url, table='outlet', properties=properties, mode='append'
    )

    menu.write.jdbc(
    url=outlet_url, table='menu', properties=properties, mode='append'
    )



    # a.	GET outlets who sell certain brands (Optional - try not to use an exact match on the brand. E.g. a brand of 'Coca’ should bring up Coca-Cola.);
    # foreign key and ´%like%
                                            
    # b.	GET a list of outlets that have a presence in one specific source (defined in the API call); 
    # easy
    # c.	GET menu items above a certain price threshold (defined in the API call);
                                            
    # d.	POST a new outlet.

