# Handles environment variables
import os
from dotenv import load_dotenv
# Connects with postgres DB 
import psycopg2
# Handles time logging
import datetime
# Posts to slack 
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
# Begins time logging 
begin_time = datetime.datetime.now()

load_dotenv()

SLACK_TOKEN = os.getenv('SLACK_TOKEN')

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
OS_KEY = os.getenv('OS_KEY')

# Gets starting index offset from an environment variable so as to not have to re-set it for each script 
offset = int(os.getenv('CROC_OFFSET'))
print(f'Offset: {offset}')

# Connects to the postgres DB 
con = psycopg2.connect(database="croc_glory", user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port="5432")

print("Database opened successfully")

# Gets all crocs from our view tracking unqiue traits
cur = con.cursor()
cur.execute(f'SELECT croc from v_croc_with_singular_count_of_trait LIMIT 100') 
rows = cur.fetchall()

snipe_report = ''

# Loops through each returned item 
for row in rows:

    print(f'Original Croc: {row[0]}')

    # Handles starting index offset 
    offset_croc = row[0] - offset

    if offset_croc < 1:
        offset_croc = offset_croc + 8888
    print(f'OFFSET CROC: {offset_croc}')

    # Queries offset croc number from opensea listing DB table to see if it is for sale 
    cur.execute(f'SELECT croc_number, price, url from os_listings where croc_number = {offset_croc}') #Note this may be REALLY bad python SQL practice, but i'm the only one running it.
    listings = cur.fetchone()

    # If a listing is found, it adds that croc to the snipe report 
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
slack_message = f'________________\n\n`1-of1 Trait Report (Crocs with a unique trait)`\n ```{snipe_report}```\n________________'

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

# Finishes time logging 
print(datetime.datetime.now() - begin_time)
