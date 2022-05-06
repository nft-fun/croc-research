# Handles environment variables
import os
from dotenv import load_dotenv
# Connects with postgres DB 
import psycopg2
# Logs time 
import datetime
# Posts messages to slack 
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Begins logging
begin_time = datetime.datetime.now()

# Loads environment variables 
load_dotenv()

SLACK_TOKEN = os.getenv('SLACK_TOKEN')

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
OS_KEY = os.getenv('OS_KEY')

# Gets the start index offset, defined as an environment variable so as to only have to update once and be used by all scripts
offset = int(os.getenv('CROC_OFFSET'))
print(f'Offset: {offset}')

# Connects to postgres DB on AWS RDS
con = psycopg2.connect(database="croc_glory", user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port="5432")

print("Database opened successfully")

# Gets the top 200 rows in our rarity ranking SQL view
cur = con.cursor()
cur.execute(f'SELECT CROC, overall_rarity from v_9_trait_rarity order by overall_rarity ASC LIMIT 200') 
rows = cur.fetchall()

# Preps some values that will be continually updated in the following loop
snipe_report = ''
rank_count = 0

# Loops through each item retrieved from the SQL query
for row in rows:
    rank_count = rank_count + 1

    print(f'\n\n-------Rank: {rank_count}-------')
    print(f'Original Croc: {row[0]}')
    print(f'Rarity: {row[1]}')

    # Handles the offset 
    offset_croc = row[0] - offset

    if offset_croc < 1:
        offset_croc = offset_croc + 8888
    print(f'OFFSET CROC: {offset_croc}')

    # Tries to find the offset croc in the stored opensea listings table
    cur.execute(f'SELECT croc_number, price, url from os_listings where croc_number = {offset_croc}') #Note this line may be REALLY bad python SQL practice, but I'm the only one running it.
    listings = cur.fetchone()

    # If the query above finds anything that croc is both in our top 200 rarity and has an opensea listing 
    if listings is not None:
        croc = str(listings[0])
        price = listings[1]
        url = listings[2]
        print(f'\nListing for: {croc}\nPrice: {price}\nURL: {url}')

        # Add that croc to the 'snipe report' summary that will happen at the end
        snipe_report = f'{snipe_report}\n\nCroc: {offset_croc}\nRank: {rank_count}\nRarity: {row[1]}\nPrice: {price} ETH\nURL: \n{url}\n'


# Close the DB connection
con.close()

# Print the snipe report to terminal
print(f'\n\n\n\n$$$$$$$$$$$$$$$$$$$$$$$$\n\nSNIPE REPORT{snipe_report}\n-----------------------')

# Post the snipe report to slack 
print('Posting to slack.....')
slack_message = f'________________\n\n`Overall Rarity Snipe Report (From top 200)`\n ```{snipe_report}```\n______________________'

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

# finish time logging 
print(datetime.datetime.now() - begin_time)
