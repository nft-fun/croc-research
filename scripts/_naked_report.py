# Handles environment variables 
import os
from dotenv import load_dotenv
# Interacts with postgres DB 
import psycopg2
# Handles execution time logging 
import datetime
# Posts to slack 
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Begins execution time logging 
begin_time = datetime.datetime.now()
# Loads environment variables 
load_dotenv()

SLACK_TOKEN = os.getenv('SLACK_TOKEN')

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
OS_KEY = os.getenv('OS_KEY')

# Gets start index offset from an environment variable so as to not have to re-set it for each script 
offset = int(os.getenv('CROC_OFFSET'))
print(f'Offset: {offset}')

# Connects to postgres DB on AWS RDS 
con = psycopg2.connect(database="croc_glory", user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port="5432")

print("Database opened successfully")

# Queries all crocs from our zero-trait counting view, where they have 6 zero traits
cur = con.cursor()
cur.execute(f'SELECT croc from v_zero_trait_counts WHERE num_occurrences = 6') 
rows = cur.fetchall()

snipe_report = ''

# Loops for every returned record (should be 9)
for row in rows:

    print(f'Original Croc: {row[0]}')

    # Handles start index offset 
    offset_croc = row[0] - offset

    if offset_croc < 1:
        offset_croc = offset_croc + 8888
    print(f'OFFSET CROC: {offset_croc}')

    # Queries each croc from the table of stored opensea listings 
    cur.execute(f'SELECT croc_number, price, url from os_listings where croc_number = {offset_croc}') #Note this may be REALLY bad python SQL practice, but i'm the only one running it.
    listings = cur.fetchone()


    # If a listing is found, adds it to the snipe report 
    if listings is not None:
        croc = str(listings[0])
        price = listings[1]
        url = listings[2]
        print(f'\nListing for: {croc}\nPrice: {price}\nURL: {url}')

        snipe_report = f'\n\n{snipe_report}\n\nCroc: {offset_croc}\nPrice: {price} ETH\nURL: \n{url}\n'


# Closes DB connection 
con.close()

# Prints snipe report to terminal 
print(f'\n\n\n\n$$$$$$$$$$$$$$$$$$$$$$$$\n\nSNIPE REPORT{snipe_report}\n-----------------------')

# Posts snipe report to slack 
print('Posting to slack.....')
slack_message = f'________________\n\n`Naked Croc Report (Crocs with 3 non-zero traits)`\n ```{snipe_report}```\n_________________'

print(SLACK_TOKEN)
client = WebClient(token=SLACK_TOKEN)
try:
    response = client.api_call(
    api_method='chat.postMessage',
    json={
    'channel': 'snipe_reports',
    'text': slack_message
        }
        )
    assert response['message']

except SlackApiError as e:
    assert e.response['ok'] is False
    assert e.response['error']  
    print(f"Got an error: {e.response['error']}")

# Finishes and prints execution time logging 
print(datetime.datetime.now() - begin_time)
