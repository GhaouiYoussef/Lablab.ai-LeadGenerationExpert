import unittest
from unittest.mock import patch
import requests
import pandas as pd
from fastapi import HTTPException
import os
import sys
import os
sys.path.append(os.path.abspath('../'))
print(os.listdir())

from ibmgraniteclient import IBMGraniteClient  # Assuming the class is in ibm_granite_client.py

class TestIBMGraniteClient(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_api_key"
        self.scoring_url = "https://test.ibm.com/scoring"
        self.client = IBMGraniteClient(self.api_key, self.scoring_url)
        self.mock_token = "mocked_token"
        self.mock_predictions = {
            "predictions": [{
                "values": [["Won"], ["Lost"], ["Won"]]
            }]
        }
        self.sample_data = pd.DataFrame({
            "opportunity_id": [1, 2, 3],
            "sales_agent": ["Agent A", "Agent B", "Agent C"],
            "product": ["Product X", "Product Y", "Product Z"],
            "account": ["Account 1", "Account 2", "Account 3"]
        })

    @patch("requests.post")
    def test_get_auth_token_success(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"access_token": self.mock_token}
        
        self.client.get_auth_token()
        self.assertEqual(self.client.token, self.mock_token)

    @patch("requests.post")
    def test_get_auth_token_failure(self, mock_post):
        mock_post.side_effect = requests.exceptions.RequestException("Auth Error")
        
        with self.assertRaises(HTTPException) as context:
            self.client.get_auth_token()
        self.assertEqual(context.exception.status_code, 500)
        self.assertIn("Failed to get IBM token", context.exception.detail)

    @patch("requests.post")
    def test_call_model_success(self, mock_post):
        self.client.token = self.mock_token
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = self.mock_predictions
        
        result = self.client.call_model(self.sample_data)
        
        expected_result = [
            {"opportunity_id": 1, "sales_agent": "Agent A", "product": "Product X", "account": "Account 1", "prediction": "Won"},
            {"opportunity_id": 3, "sales_agent": "Agent C", "product": "Product Z", "account": "Account 3", "prediction": "Won"},
        ]
        
        self.assertEqual(result, expected_result)

    @patch("requests.post")
    def test_call_model_failure(self, mock_post):
        self.client.token = self.mock_token
        mock_post.side_effect = requests.exceptions.RequestException("Model Error")
        
        with self.assertRaises(HTTPException) as context:
            self.client.call_model(self.sample_data)
        self.assertEqual(context.exception.status_code, 500)
        self.assertIn("Error calling Granite model", context.exception.detail)

if __name__ == "__main__":
    unittest.main()
