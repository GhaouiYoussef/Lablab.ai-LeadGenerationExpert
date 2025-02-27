
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("IBM_API_KEY")
ACCESS_TOKEN = None

def get_ibm_token():
    """Retrieve IBM Watson API Access Token."""
    global ACCESS_TOKEN
    if not ACCESS_TOKEN:
        url = "https://iam.cloud.ibm.com/identity/token"
        response = requests.post(url, headers={"Content-Type": "application/x-www-form-urlencoded"}, 
                                 data={"grant_type": "urn:ibm:params:oauth:grant-type:apikey", "apikey": API_KEY})
        if response.status_code == 200:
            ACCESS_TOKEN = response.json()["access_token"]
        else:
            raise Exception(f"Error getting IBM Watson token: {response.text}")

    return ACCESS_TOKEN

def summarize_text(text, model_id="ibm/granite-3-2b-instruct", max_tokens=300):
    """Summarize the extracted text using IBM Watson."""
    token = get_ibm_token()
    url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
    
    body = {
        "input": f"Summarize this scraped content to give a overview of the company in 350 word:\n\n{text}",
        "parameters": {"decoding_method": "greedy", "max_new_tokens": max_tokens},
        "model_id": model_id,
        "project_id": "7f1f5582-3e1f-4330-a539-e2d20b58041e"
    }
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    
    response = requests.post(url, headers=headers, json=body)
    return response.json().get("results", [{}])[0].get("generated_text", "Error: Unable to summarize.")
