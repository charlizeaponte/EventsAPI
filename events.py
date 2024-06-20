import requests

API_KEY = "EnyhC0nnujH5iAVj6SKOteGi0jzV6N7V"
BASE_URL = "https://app.ticketmaster.com/discovery/v2/"

user = input("enter a performer:")

# Endpoint to get events
endpoint = f"{BASE_URL}events.json"

# Query parameters
params = {
    "countryCode": "US",
    "apikey": API_KEY,
    "size": 1,  
    "keyword": user
}

# Making the GET request
response = requests.get(endpoint, params=params)
print(response.status_code)


# Checking if the request was successful
if response.status_code == 200:
    # Print the JSON response
    print(response.json())
else:
    print(f"Error: {response.status_code}")
    print(response.json())
