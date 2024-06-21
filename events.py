import os
import requests
import pandas as pd
import sqlalchemy as db

# Retrieve API_KEY from environment variables
API_KEY = os.environ.get('EVENTS_CLIENT_ID')

# Base URL for Ticketmaster API
BASE_URL = "https://app.ticketmaster.com/discovery/v2/"

# Prompt user to enter performer name
user = input("Enter a performer: ")

# Endpoint to get events
endpoint = f"{BASE_URL}events.json"

# Query parameters for API request
params = {
    "countryCode": "US",
    "apikey": API_KEY,
    "size": 5,
    "keyword": user
}

# Making the GET request
response = requests.get(endpoint, params=params)
print(f"Response status code: {response.status_code}")

# Checking if the request was successful
if response.status_code == 200:
    # Extracting events data from JSON response
    events = response.json()['_embedded']['events']

    events_list = []
    for event in events:
        # Extracting relevant event information
        events_info = {
            "name": event["name"],
            "id": event["id"],
            "url": event["dates"]["start"]["localDate"],
            "date": event["dates"]["start"].get("localTime", "N/A"),
            "venue": event["_embedded"]["venues"][0]["name"],
            "city": event["_embedded"]["venues"][0]["city"]["name"]
        }
        events_list.append(events_info)

    # Creating a DataFrame from events list
    df = pd.DataFrame(events_list)

    # SQLite database operations
    engine = db.create_engine('sqlite:///events.db')

    # Export DataFrame to SQLite database
    df.to_sql('events', con=engine, if_exists='replace', index=False)

    # Execute SQL query to fetch data and print results
    with engine.connect() as connection:
        query = "SELECT * FROM events;"
        query_result = connection.execute(db.text(query)).fetchall()
        print(pd.DataFrame(query_result))

else:
    # Handling unsuccessful API request
    print(f"Error: {response.status_code}")
