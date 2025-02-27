import requests
from config import API_KEY, IBM_AUTH_URL, IBM_API_URL

def get_ibm_access_token():
    """Fetches an access token from IBM Watson."""
    response = requests.post(
        IBM_AUTH_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"grant_type": "urn:ibm:params:oauth:grant-type:apikey", "apikey": API_KEY},
    )
    
    if response.status_code == 200:
        return response.json().get("access_token")
    
    raise Exception(f"Error getting access token: {response.text}")

# Get an IBM access token at startup
ACCESS_TOKEN = get_ibm_access_token()

def generate_response(prompt: str, model_id="ibm/granite-3-8b-instruct", max_tokens=300):
    """Generates a response using IBM Watson API."""
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }

    body = {
        "input": prompt,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": max_tokens,
            "min_new_tokens": 0,
            "repetition_penalty": 1
        },
        "model_id": model_id,
        "project_id": "7f1f5582-3e1f-4330-a539-e2d20b58041e"
    }

    response = requests.post(IBM_API_URL, headers=headers, json=body)

    if response.status_code == 200:
        try:
            return response.json()["results"][0]["generated_text"]
        except (KeyError, IndexError):
            return "Error: Unexpected response format from IBM API"
    
    return f"Error: IBM API returned {response.status_code} - {response.text}"
