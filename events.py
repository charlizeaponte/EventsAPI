import os
import requests
import pandas as pd
from sqlalchemy import create_engine, text  # Import text from sqlalchemy.sql


def events():
    API_KEY = os.environ.get('EVENTS_CLIENT_ID')
    BASE_URL = "https://app.ticketmaster.com/discovery/v2/"
    user = input("Enter a performer: ")
    endpoint = f"{BASE_URL}events.json"
    params = {
        "countryCode": "US",
        "apikey": API_KEY,
        "size": 5,
        "keyword": user
    }

    response = requests.get(endpoint, params=params)
    print(f"Response status code: {response.status_code}")

    if response.status_code == 200:
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
        engine = create_engine('sqlite:///events.db')
        df.to_sql('events', con=engine, if_exists='replace', index=False)

        with engine.connect() as connection:
            query = "SELECT * FROM events;"
            query_result = connection.execute(text(query)).fetchall()
            print(pd.DataFrame(query_result))

    else:
        print(f"Error: {response.status_code}")


events()
