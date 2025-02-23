from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from pymongo import MongoClient
from dotenv import load_dotenv
import os

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

@app.get("/api/agents-discussion")
async def agents_discussion():
    try:
        conversation = []
        
        # **Structured Prompt for Agents**
        structure_prompt = """
        You are Agent {agent_number}. You are having a structured debate about whether we should consider working with this client.
        Your goal is to convince the other agent of your position. 
        You must present strong arguments, counter the other agent's points, and lead the discussion toward a logical conclusion.
        Here is the conversation so far:
        {history}
        Now, respond with your next argument. Only provide one argument, not the entire conversation following this format:
        Agent {agent_number}: "Your argument here" EOA.
        """

        # Start with Agent 1 presenting the case FOR
        agent_1_prompt = structure_prompt.format(agent_number="1", history="(No prior discussion)")
        agent_1_response = generate_response(agent_1_prompt).replace('Agent 1: "Your argument here" EOA', '').strip()
        print('agent_1_response:', agent_1_response)
        conversation.append({"agent": "Agent 1", "message": agent_1_response})

        # Agent 2 counters the argument
        agent_2_prompt = structure_prompt.format(agent_number="2", history=agent_1_response)
        agent_2_response = generate_response(agent_2_prompt)
        print('agent_2_response:', agent_2_response)
        conversation.append({"agent": "Agent 2", "message": agent_2_response})

        # Agent 1 rebuts
        agent_1_prompt_2 = structure_prompt.format(agent_number="1", history=agent_1_response + " " + agent_2_response)
        agent_1_response_2 = generate_response(agent_1_prompt_2)
        print('agent_1_response_2:', agent_1_response_2)
        conversation.append({"agent": "Agent 1", "message": agent_1_response_2})

        # Agent 2 gives a final response and reaches a conclusion
        agent_2_prompt_2 = structure_prompt.format(agent_number="2", history=agent_1_response_2 + " " + agent_2_response)
        agent_2_response_2 = generate_response(agent_2_prompt_2)
        print('agent_2_response_2:', agent_2_response_2)
        conversation.append({"agent": "Agent 2", "message": agent_2_response_2})

        # Generate a summary
        summary_prompt = """
        You are Judge Agent analyzing the debate. Provide a summary of this discussion and a final decision about whether we should consider working with this client.
        Start your response with 'FINAL DECISION: ...' and explain why you reached this conclusion.
        Here is the conversation so far:
        """ + " ".join([m["message"] for m in conversation])

        summary = generate_response(summary_prompt, max_tokens=300*4)
        idx = 0
        while idx != -1: 
            idx = summary.upper().find('FINAL DECISION')
            print('idx:', idx)
            if idx == -1:
                break
            summary = summary[idx + 14:].strip()
            print('summary:', summary)

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
