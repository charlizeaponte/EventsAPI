import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
from sqlalchemy import create_engine, text
import pandas as pd
import requests
import os

from events import events

class TestEventsFunction(unittest.TestCase):

    @patch('builtins.input', return_value='Drake')
    @patch('requests.get')
    @patch('sqlalchemy.create_engine')
    def test_events_success(self, mock_engine, mock_get, mock_input):
        # Mock API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "_embedded": {
                "events": [
                    {
                        "name": "Drake Milligan",
                        "id": "vv17fZbFGkSfc6OY",
                        "dates": {"start": {"localDate": "2024-07-13", "localTime": "20:45:00"}},
                        "_embedded": {"venues": [{"name": "8 Seconds Saloon", "city": {"name": "Indianapolis"}}]}
                    },
                    {
                        "name": "Drake White",
                        "id": "vvG1YZb56-yV2i",
                        "dates": {"start": {"localDate": "2024-09-07", "localTime": "20:00:00"}},
                        "_embedded": {"venues": [{"name": "Tannahill's Tavern and Music Hall", "city": {"name": "Fort Worth"}}]}
                    },
                    {
                        "name": "Drake White",
                        "id": "G5dIZb1Uyu3EA",
                        "dates": {"start": {"localDate": "2024-08-08", "localTime": "18:30:00"}},
                        "_embedded": {"venues": [{"name": "Scoot Inn", "city": {"name": "Austin"}}]}
                    },
                    {
                        "name": "Drake Milligan",
                        "id": "vv1kv8vO0_GAuB-z-",
                        "dates": {"start": {"localDate": "2024-10-05", "localTime": "20:00:00"}},
                        "_embedded": {"venues": [{"name": "Lori's Road House", "city": {"name": "West Chester Township"}}]}
                    },
                    {
                        "name": "Drake Milligan",
                        "id": "G5viZbu19U-Yj",
                        "dates": {"start": {"localDate": "2024-09-25", "localTime": "19:30:00"}},
                        "_embedded": {"venues": [{"name": "Duling Hall", "city": {"name": "Jackson"}}]}
                    }
                ]
            }
        }
        mock_get.return_value = mock_response

        # Mock SQLAlchemy engine and connection
        mock_conn = MagicMock()
        mock_engine.return_value.connect.return_value.__enter__.return_value = mock_conn
        mock_conn.execute.return_value.fetchall.return_value = [
            {"name": "Drake Milligan", "id": "vv17fZbFGkSfc6OY", "url": "N/A", "date": "2024-07-13 20:45:00", "venue": "8 Seconds Saloon", "city": "Indianapolis"},
            {"name": "Drake White", "id": "vvG1YZb56-yV2i", "url": "N/A", "date": "2024-09-07 20:00:00", "venue": "Tannahill's Tavern and Music Hall", "city": "Fort Worth"},
            {"name": "Drake White", "id": "G5dIZb1Uyu3EA", "url": "N/A", "date": "2024-08-08 18:30:00", "venue": "Scoot Inn", "city": "Austin"},
            {"name": "Drake Milligan", "id": "vv1kv8vO0_GAuB-z-", "url": "N/A", "date": "2024-10-05 20:00:00", "venue": "Lori's Road House", "city": "West Chester Township"},
            {"name": "Drake Milligan", "id": "G5viZbu19U-Yj", "url": "N/A", "date": "2024-09-25 19:30:00", "venue": "Duling Hall", "city": "Jackson"}
        ]

        # Capture stdout to check printed output
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            events()

            # Verify printed output
            output = mock_stdout.getvalue().strip()
            expected_output = """
                 name                 id         url               date                              venue                   city
    0  Drake Milligan   vv17fZbFGkSfc6OY         2024-07-13 20:45:00                   8 Seconds Saloon           Indianapolis
    1     Drake White     vvG1YZb56-yV2i          2024-09-07 20:00:00  Tannahill's Tavern and Music Hall             Fort Worth
    2     Drake White      G5dIZb1Uyu3EA         2024-08-08 18:30:00                          Scoot Inn                 Austin
    3  Drake Milligan  vv1kv8vO0_GAuB-z-          2024-10-05 20:00:00                  Lori's Road House  West Chester Township
    4  Drake Milligan      G5viZbu19U-Yj          2024-09-25 19:30:00                        Duling Hall                Jackson
                """
            # Compare stripped versions to ignore whitespace differences
            self.assertIn(expected_output.strip(), output.strip())

            # Debug prints
            print("Expected Output:")
            print(expected_output.strip())
            print("\nActual Output:")
            print(output.strip())

    @patch('builtins.input', return_value='Drake')
    @patch('requests.get')
    @patch('sqlalchemy.create_engine')
    def test_events_error(self, mock_engine, mock_get, mock_input):
        # Mock API response with error status code
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Capture stdout to check printed output
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            events()

            # Verify error message
            output = mock_stdout.getvalue().strip()
            self.assertIn("Error: 404", output)

if __name__ == '__main__':
    unittest.main()

