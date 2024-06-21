# EVENTSAPI

This project uses a performer name that the user enters to retrieve event data from the Ticketmaster API. After retrieving the event details, it stores them in a SQLite database and shows the information.

## Setup Instructions

### Prerequisites

- Python 3.6 or higher

### Libraries to Install

Use the following command to install the required libraries:

```bash
pip install requests pandas sqlalchemy
```
### Environment Variables

Add your Ticketmaster API key to the environment variable EVENTS_CLIENT_ID. To accomplish this, add the following line to your Windows environment variables (environment variables.vbs) or Linux/macOS.bash_profile:

```bash
export EVENTS_CLIENT_ID=your_ticketmaster_api_key
```
Replace your_ticketmaster_api_key with your actual API key.

### How to Run the Code

1. Either save the code locally or clone the repository.
2. Make sure you have installed all the necessary libraries.
3. As mentioned above, set the environment variable EVENTS_CLIENT_ID.
4. Utilizing the following command in terminal, run the code:
```bash
python3 events.py
```

### OVERVIEW ON HOW THE PROJECT WORKS

1. **Import Libraries**: Requests, OS, Pandas, and SQLAlchemy are among the libraries that are imported by the code.

2.  **API Key and Base URL**: It sets the API's base URL and retrieves the Ticketmaster API key from environment variables.

3. **User Input**: Requests the name of the performer.

4. Building the endpoint and query parameters for the API request is known as endpoint and query parameters construction. The API key, country code, size (number of results), and user-supplied keyword (performer name) are among the query parameters.

5. **API Request**: Submits a GET request with the given parameters to the Ticketmaster API.

6. **Handling the Response**: Verifies whether the request (status code 200) was successful. If it is successful, event details are extracted by parsing the JSON response. It prints an error message if it fails.

7. **Information Processing**: extracts pertinent data from the JSON response, including the event name, ID, URL, date, time, location, and city. Saves the information that was extracted into a pandas DataFrame.

8. **Database Management**: produces a database engine called SQLite. Replaces any existing tables in the SQLite database (events.db) with the DataFrame when it is stored there. Prints every record that is retrieved from the events table by running a database query.

9. **Error Handling**: An error message containing the status code is printed if the API request is unsuccessful.

