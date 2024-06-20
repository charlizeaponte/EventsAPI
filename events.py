import requests
import os


API_KEY = os.environ.get('EVENTS_CLIENT_ID')
BASE_URL = "https://app.ticketmaster.com/discovery/v2/"

user = input("Enter a performer: ")

# Endpoint to get events
endpoint = f"{BASE_URL}events.json"

# Query parameters
params = {
    "countryCode": "US",
    "apikey": os.environ.get('EVENTS_CLIENT_ID'),
    "size": 1,  
    "keyword": user
}

# Making the GET request
response = requests.get(endpoint, params=params)
print(f"Response status code: {response.status_code}")

# Checking if the request was successful
if response.status_code == 200:
    # Print the JSON response
    print(response.json())
else:
    print(f"Error: {response.status_code}")
    
