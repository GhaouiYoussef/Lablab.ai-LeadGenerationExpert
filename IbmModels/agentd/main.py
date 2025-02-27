from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import uvicorn

# Load environment variables
load_dotenv()

# IBM Watson API setup
API_KEY = os.getenv("API_KEY")
url = "https://iam.cloud.ibm.com/identity/token"
headers = {"Content-Type": "application/x-www-form-urlencoded"}
data = {
    "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
    "apikey": API_KEY,
}

response = requests.post(url, headers=headers, data=data)
if response.status_code == 200:
    token_info = response.json()
    ACCESS_TOKEN = token_info["access_token"]
else:
    raise Exception(f"Error getting access token: {response.text}")

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["test"]
discussions_collection = db["discussions"]

# FastAPI app setup
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_URL = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {ACCESS_TOKEN}",
}

# Function to generate a response using IBM Watson
def generate_response(prompt, model_id="ibm/granite-3-8b-instruct", max_tokens=300):
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
    response = requests.post(API_URL, headers=HEADERS, json=body)
    if response.status_code == 200:
        try:
            return response.json()["results"][0]["generated_text"]
        except (KeyError, IndexError):
            return "Error: Unexpected response format from IBM API"
    else:
        return f"Error: IBM API returned {response.status_code} - {response.text}"

# In main.py
@app.get("/api/agents-discussion")
async def agents_discussion(WebSiteSummary: str = None, UserCompany: str = 'AI Consulting'):  # Add parameter
    try:
        
        """Handles a structured competitive debate between two agents—one for and one against working with the client."""
    
        conversation = []
        history = "(No prior discussion)"

        # Define agent roles
        agent_roles = {
            1: "Argue why we SHOULD work with this client.",
            2: "Argue why we SHOULD NOT work with this client."
        }

        structure_prompt = """
        You are Agent {agent_number}, a strategic advisor for our {UserCompany} company. 
        Our AI model has predicted this client as 'winnable,' but we need to verify this through structured debate.
        
        Your role: {AgentRole}
        
        Below is a summary of the client from their website:
        {WebSiteSummary}
        
        Consider the client's potential risks, strategic fit, and business opportunities.
        Respond with your next argument. Provide only one argument for Agent {agent_number}, and do not generate the response for the other agent.
        
        Here is the conversation so far:
        {History}
        """

        for i in range(4):  # Alternate between Pro Agent (1) and Against Agent (2)
            agent_number = (i % 2) + 1
            agent_prompt = structure_prompt.format(
                agent_number=agent_number,
                UserCompany=UserCompany,
                AgentRole=agent_roles[agent_number],
                WebSiteSummary=WebSiteSummary or "No summary available",
                History=history
            )
            
            response = generate_response(agent_prompt)
            conversation.append({"agent": f"Agent {agent_number}", "message": response})
            history += " " + response  # Update history for context

            if agent_number == 1:
                print('\033[91m' + 'Pro Agent:', response + '\033[0m')
            else:
                print('\033[92m' + 'Against Agent:', response + '\033[0m')

        # Generate a summary
        summary_prompt = f"""
            You are Senior Strategic Advisor Agent analyzing the debate of two junior Agents. You must provide an argumented final decision in 150 word max, to either proceed or not with this client.
            The debate:""" + "\n".join([f"{m['agent']}: {m['message']}" for m in conversation])

        # Generate the summary
        summary = generate_response(summary_prompt, max_tokens=500)  # Increase max_tokens if needed
        print('summary:', summary)
        
        # Extract the "FINAL DECISION" section
        final_decision_start = summary.upper().find("FINAL DECISION:")
        if final_decision_start != -1:
            summary = summary[final_decision_start:].strip()
        else:
            summary = summary + "FINAL DECISION: Unable to determine a clear decision from the discussion."

        print('summary:', summary)

        # Store in MongoDB
        discussion_data = {
            "summary": summary,
            "history": conversation
        }
        discussions_collection.insert_one(discussion_data)

        return {"summary": summary, "history": conversation}

    except Exception as e:
        return {"error": str(e)}

@app.get("/api/get-discussions")
async def get_discussions():
    try:
        discussions = list(discussions_collection.find({}, {"_id": 0}))
        return {"discussions": discussions}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)