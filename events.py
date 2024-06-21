import os
import requests
import pandas as pd
import sqlalchemy as db

API_KEY = os.environ.get('EVENTS_CLIENT_ID')
BASE_URL = "https://app.ticketmaster.com/discovery/v2/"

user = input("Enter a performer: ")

# Endpoint to get events
endpoint = f"{BASE_URL}events.json"

# Query parameters
params = {
    "countryCode": "US",
    "apikey": os.environ.get('EVENTS_CLIENT_ID'),
    "size": 5,
    "keyword": user
}

# Making the GET request
response = requests.get(endpoint, params=params)
print(f"Response status code: {response.status_code}")

# Checking if the request was successful
if response.status_code == 200:
    # Print the JSON response
    events = response.json()['_embedded']['events']

    events_list = []
    for event in events:
        events_info = {
            "name": event["name"],
            "id": event["id"],
            "url": event["dates"]["start"]["localDate"],
            "date": event["dates"]["start"].get("localTime", "N/A"),
            "venue": event["_embedded"]["venues"][0]["name"],
            "city": event["_embedded"]["venues"][0]["city"]["name"]
        }
        events_list.append(events_info)
    df = pd.DataFrame(events_list)

    # SQLite database operations
    engine = db.create_engine('sqlite:///events.db')

    # Export DataFrame to SQLite
    df.to_sql('events', con=engine, if_exists='replace', index=False)

    # Execute SQL query to fetch data
    with engine.connect() as connection:
        query_result = connection.execute(db.text("SELECT * FROM events;")).fetchall()
        print(pd.DataFrame(query_result))

else:
    print(f"Error: {response.status_code}")
