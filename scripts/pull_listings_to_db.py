# For getting sensitive creds from a .env file instead of storing them in the main script
import os
from dotenv import load_dotenv
# For making HTTP calls to opensea API 
import requests
# For connecting to the postgresql database 
import psycopg2
# For handing JSON payloads
import json
# For adding a 1 second delay to avoid getting slapped by opensea's api throttling
import time
# To log how long this takes
import datetime
# To manipulate arrays
import numpy

load_dotenv()

# This gets DB Creds and opensea keyan environment variable from a file named .env. It relies on the os and dotenv bits above.

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')

OS_KEY = os.getenv('OS_KEY')

# Sets the opensea https headers to be used later
headers = {'X-API-KEY': OS_KEY, 'Accept': 'application/json'}

# Starts the time logging. Takes about 8 minutes to run through the whole creco collection
begin_time = datetime.datetime.now()

# Connects to postgres DB on AWS RDS
con = psycopg2.connect(database="croc_glory", user=DB_USER,
                       password=DB_PASSWORD, host=DB_HOST, port="5432")
# Creates a 'cursor' to act on the DB 
cur = con.cursor()


loop_count = 0
# 320 loops x 25 per batch covers 8000, assumption is the treasury is not selling any above that
for i in range (320):
    # If running this from the beginning rather than picking up part way through (you might run a partial set using ...in range (55,320) on the line above when opensea's api fails inexplicibly) this will nuke all of the existing records from the DB and populate fresh
    if i == 0:
        cur.execute("TRUNCATE os_listings")

    print(f'\n\n--{i}--')

    # Creates an array to target each batch of 25
    a=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
    # a=[1,2,3]
    ar = numpy.array(a)
    # Adds the loop count*25 to that base array 
    ar = ar + i*25
    print(ar)
    # Opensea's (undocumented) parameter format for this array is STUPID. E.g. 8&token_ids=69&token_ids=70&token_ids=71 But this handles it
    b='&token_ids='. join(str(x) for x in ar)

    # print(b)

    # Sleeps for a second because Opensea's API has restrictions
    time.sleep(1)
    # Calls for non-english-auction sell listings within a 25 token ID batch at a time.
    url=f'https://api.opensea.io/wyvern/v1/orders?token_ids={b}&asset_contract_address=0x2CA113E1aA37d83662A1D3F84e209f7068700fa6&side=1&is_english=false'
    print(url)
    r = requests.get(url, headers=headers)
    jsonResponse = r.json()
    print(r.status_code)
    # print(jsonResponse)

    # If there are orders returned this will add each to the DB 
    if jsonResponse['orders']:
        # Loops once per NFT with orders 
        for o in range(len(jsonResponse['orders'])):
            # Preps the variables that will be pushed into the DB 
            token = jsonResponse['orders'][o]['asset']['token_id']
            price = int(float(jsonResponse['orders'][o]['current_price']))
            price = price / 1000000000000000000
            url = f'https://opensea.io/assets/0x2ca113e1aa37d83662a1d3f84e209f7068700fa6/{token}'

            print(f'\nOrder for: {token}')
            print(f'Price: {price} ETH')

            # Creates the line item in the DB 
            cur.execute("""INSERT INTO os_listings (croc_number, price, url) VALUES (%s, %s, %s);""",(token,price,url))
            con.commit()


# Closes the DB connection
con.close()

print('\n\n--Done---\n\nRuntime:')
# Finishes the time logging 
print(datetime.datetime.now() - begin_time)







