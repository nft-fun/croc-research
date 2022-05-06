# Handles environment variables 
import os
from dotenv import load_dotenv
# Handles postgres DB 
import psycopg2
# Handles JSON payloads
import json
# Handles execution time logging 
import datetime
# Posts to slack 
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Loads environment variables 
load_dotenv()

SLACK_TOKEN = os.getenv('SLACK_TOKEN')

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')

OS_KEY = os.getenv('OS_KEY')

# Begins execution time logging 
begin_time = datetime.datetime.now()


# Gets offset as environment variable to avoid re-setting it for each script 
offset = int(os.getenv('CROC_OFFSET'))
print(f'\n\nOffset: {offset}')

# Connect to postgres DB on AWS RDS 
con = psycopg2.connect(database="croc_glory", user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port="5432")

cur = con.cursor()

order_list = ''
full_report = ''

# Loops once for each attribute 1-9
for i in range(1,10):
    snipe_report = ''
    trait = f'a{i}'
    print(f'\n\n------BEGIN PROCESSING TRAIT - {trait}------\n')
    best_trait_crocs = ''
    second_trait_crocs = ''

    # Gets the top two rarest trait numbers for each attribute
    cur.execute(f'SELECT {trait}, count, percentage from v_{trait}_counts order by percentage ASC LIMIT 2')
    first_rows = cur.fetchall()

    # Captures the top and second attribute number, count, and percentage 
    top_trait = first_rows[0][0]
    top_trait_count = first_rows[0][1]
    top_trait_percentage = first_rows[0][2]

    second_trait = first_rows[1][0]
    second_trait_count = first_rows[1][1]
    second_trait_percentage = first_rows[1][2]

    # Prints some stuff for the humans 
    print(f'++++++++\nTop two {trait} Traits - Summary')
    print(f'\nTOP {trait} trait: {top_trait}\nCount: {top_trait_count}\nPercentage: {top_trait_percentage}%\n')
    print(f'\nSECOND {trait} trait: {second_trait}\nCount: {second_trait_count}\nPercentage: {second_trait_percentage}%\n+++++++')
    print(f'\n\n--Processing top {trait} trait crocs--\n')

    # Queries crocs that have the top trait for that attribute 
    cur.execute(f'SELECT croc, overall_rarity from v_9_trait_rarity WHERE {trait} = {top_trait} order by overall_rarity ASC')
    second_rows = cur.fetchall()

    # Loops all returned crocs
    for row in second_rows:
        # Handles the start index offset 
        offset_croc = row[0] - offset
        if offset_croc < 1:
            offset_croc = offset_croc + 8888
        print(f'OFFSET CROC: {offset_croc}')

        # Queries the croc from the table of stored opensea listings 
        cur.execute(f'SELECT croc_number, price, url from os_listings where croc_number = {offset_croc}') #Note this line may be REALLY bad python SQL practice, but I'm the only one running it.
        listings = cur.fetchone()

        # If there are listings found for that croc, it's added to the snipe report 
        if listings is not None:
            croc = str(listings[0])
            price = listings[1]
            url = listings[2]
            print(f'\nListing for: {croc}\nPrice: {price}\nURL: {url}')

            snipe_report = f'{snipe_report}\n\nCroc: {offset_croc}\nTrait: {trait} = {top_trait} (Tier 1)\nPrice: {price} ETH\nURL: \n{url}\n'


    print(f'\n\n--Processing second {trait} trait crocs--\n')

    # This loop does basically all of the same functionality as the bit above, but for the second tier trait for that given attribute instead of the top tier trait.

    cur.execute(f'SELECT croc, overall_rarity from v_9_trait_rarity WHERE {trait} = {second_trait} order by overall_rarity ASC')
    third_rows = cur.fetchall()

    for row in third_rows:
        offset_croc = row[0] - offset
        if offset_croc < 1:
            offset_croc = offset_croc + 8888
        print(f'OFFSET CROC: {offset_croc}')

        cur.execute(f'SELECT croc_number, price, url from os_listings where croc_number = {offset_croc}') #Note this may be REALLY bad python SQL practice, but I'm the only one running it.
        listings = cur.fetchone()

        if listings is not None:
            croc = str(listings[0])
            price = listings[1]
            url = listings[2]
            print(f'\nListing for: {croc}\nPrice: {price}\nURL: {url}')

            snipe_report = f'{snipe_report}\n\nCroc: {offset_croc}\nTrait: {trait} = {second_trait} (Tier 1)\nPrice: {price} ETH\nURL: \n{url}\n'


    # Adds the snipe report for this attribute to the full report which includes all attributes 
    full_report = f'{full_report}\n---{trait}---\n{snipe_report}\n'


    print(f'\n--END PROCESSING TRAIT - {trait}--\n')
    # Prints attribute snipe report to terminal 
    print(f'\n\n$-$-$-$-$-$-$-$-$-$-$-$-$-$-$-$-$-$-$-$-$-$-$-$\n\nSNIPE REPORT FOR TRAIT: {trait}  \n\n{snipe_report}\n$-$-$-$-$-$-$-$-$-$-$-$-$-$-$-$-$-$-$-$-$-$-$-$\n')


# Prints full report to terminal 
print(f'\n\n\n~~~~~~~~~~~~~~~~~~~~~~\n\nFinished processing. Full report: {full_report}')

# Closes DB connection 
con.close()

# Posts full report to slack 
print('Posting to slack.....')
slack_message = f'__________\n\n`Trait Snipe Report (Crocs with a top-2 trait)`\n ```{full_report}```\n_____________'

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
