from fastapi import HTTPException
import requests
class IBMGraniteClient:
    """Handles authentication and communication with IBM Granite AI model."""

    def __init__(self, api_key: str, scoring_url: str):
        self.api_key = api_key
        self.scoring_url = scoring_url
        self.token = None

    def get_auth_token(self):
        """Fetches authentication token from IBM Cloud."""
        try:
            response = requests.post(
                "https://iam.cloud.ibm.com/identity/token",
                data={"apikey": self.api_key, "grant_type": "urn:ibm:params:oauth:grant-type:apikey"},
            )
            response.raise_for_status()
            self.token = response.json()["access_token"]
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Failed to get IBM token: {str(e)}")

    def call_model(self, records: pd.DataFrame):
        """Sends data to IBM Granite model and returns filtered 'Won' predictions."""
        if self.token is None:
            self.get_auth_token()

        try:
            payload = {
                "input_data": [{"fields": list(records.columns), "values": records.values.tolist()}]
            }

            response = requests.post(
                self.scoring_url,
                json=payload,
                headers={"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"},
            )
            response.raise_for_status()

            predictions = response.json().get("predictions", [{}])[0].get("values", [])
            
            # Filter 'Won' predictions
            return [
                {
                    "opportunity_id": records.iloc[idx]["opportunity_id"],
                    "sales_agent": records.iloc[idx]["sales_agent"],
                    "product": records.iloc[idx]["product"],
                    "account": records.iloc[idx]["account"],
                    "prediction": prediction[0],
                }
                for idx, prediction in enumerate(predictions) if prediction[0] == "Won"
            ]
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error calling Granite model: {str(e)}")

