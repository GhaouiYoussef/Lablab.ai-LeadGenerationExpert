from fastapi import FastAPI, File, UploadFile, HTTPException
import requests
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
import io
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# IBM Cloud credentials and scoring URL
API_KEY = os.getenv("API_KEY")
SCORING_URL = 'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/ml_genlead21/predictions?version=2021-05-01'

app = FastAPI()
# Enable CORS for specific origins (adjust as necessary)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow only the front-end domain
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Function to get IBM Cloud authentication token
def get_ibm_token():
    try:
        response = requests.post(
            "https://iam.cloud.ibm.com/identity/token",
            data={"apikey": API_KEY, "grant_type": "urn:ibm:params:oauth:grant-type:apikey"},
        )
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()["access_token"]
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to get IBM token: {str(e)}")

# Function to send data to IBM Granite model
def call_granite_model(token, records):
    try:
        fields = list(records.columns)
        values = records.values.tolist()

        payload = {
            "input_data": [{"fields": fields, "values": values}]
        }

        response = requests.post(
            SCORING_URL,
            json=payload,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        )
        response.raise_for_status()  # Raises an HTTPError for bad responses

        predictions = response.json()["predictions"][0]["values"]
        
        # Loop through the predictions and filter only those that match 'Won'
        won_predictions = []
        for idx, prediction in enumerate(predictions):
            if prediction[0] == 'Won':
                # Retrieve the corresponding columns (opportunity_id, sales_agent, product, account)
                won_predictions.append({
                    "opportunity_id": records.iloc[idx]["opportunity_id"],
                    "sales_agent": records.iloc[idx]["sales_agent"],
                    "product": records.iloc[idx]["product"],
                    "account": records.iloc[idx]["account"],
                    "prediction": prediction[0]
                })

        return won_predictions
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error calling Granite model: {str(e)}")

# API to handle file uploads and predictions
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Read the CSV file into a DataFrame
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8"))).dropna()

        # Get IBM Cloud authentication token
        token = get_ibm_token()

        # Call the Granite model for prediction
        won_predictions = call_granite_model(token, df)

        # Return the 'Won' predictions
        return {"predictions": won_predictions}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
