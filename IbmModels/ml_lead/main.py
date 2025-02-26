from fastapi import FastAPI, File, UploadFile, HTTPException
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
import io
from dotenv import load_dotenv
import os
from ibmgraniteclient import IBMGraniteClient
# Load environment variables
load_dotenv()

# IBM Cloud credentials and scoring URL
API_KEY = os.getenv("API_KEY")
SCORING_URL = 'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/ml_genlead21/predictions?version=2021-05-01'

# FastAPI app instance
app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://leads-gen-ai.vercel.app"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Instantiate IBM client
ibm_client = IBMGraniteClient(api_key=API_KEY, scoring_url=SCORING_URL)


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """Handles CSV file upload, processes data, and returns 'Won' predictions."""
    try:
        # Read and process CSV file
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8"))).dropna()

        # Get predictions from IBM Granite model
        predictions = ibm_client.call_model(df)

        return {"predictions": predictions}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
