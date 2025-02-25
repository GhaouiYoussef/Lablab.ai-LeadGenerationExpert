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
async def agents_discussion(WebSiteSummary: str = None):  # Add parameter
    try:
        conversation = []
        
        # Modified structure prompt
        structure_prompt = """
        You are Agent {agent_number}. Engage in a structured debate about whether we should consider working with this client.
        Your objective is to present compelling arguments, counter the other agent's points, and guide the discussion toward a logical conclusion.
        Below is a summary of the client from their website:
        {WebSiteSummary}
        Respond with your next argument. Provide only one argument for Agent {agent_number}, and do not generate the response for the other agent. Follow this format:
        Agent {agent_number}: "Your argument here" EOA.
        Here is the conversation so far:
        {History}
        """

        # Agent 1's first response
        agent_1_prompt = structure_prompt.format(
            agent_number="1", 
            WebSiteSummary=WebSiteSummary or "No summary available",
            History="(No prior discussion)"
        )
        agent_1_response = generate_response(agent_1_prompt).replace('Agent 1: "Your argument here" EOA', '').strip()
        print('\033[91m' + 'agent_1_response:', agent_1_response + '\033[0m')
        conversation.append({"agent": "Agent 1", "message": agent_1_response})
        history = agent_1_response
        # print('history:', history)
        # Agent 2's response
        agent_2_prompt = structure_prompt.format(
            agent_number="2", 
            WebSiteSummary=WebSiteSummary or "No summary available",
            History=history
        )
        agent_2_response = generate_response(agent_2_prompt)
        print('\033[92m' + 'agent_2_response:', agent_2_response + '\033[0m')
        conversation.append({"agent": "Agent 2", "message": agent_2_response})
        history += " " + agent_2_response
        # print('history:', history)

        # Agent 1's rebuttal
        agent_1_prompt_2 = structure_prompt.format(
            agent_number="1", 
            WebSiteSummary=WebSiteSummary or "No summary available",
            History=history
        )
        agent_1_response_2 = generate_response(agent_1_prompt_2)
        print('\033[91m' + 'agent_1_response_2:', agent_1_response_2 + '\033[0m')
        conversation.append({"agent": "Agent 1", "message": agent_1_response_2})
        history += " " + agent_1_response_2
        # print('history:', history)

        # Agent 2's final response
        agent_2_prompt_2 = structure_prompt.format(
            agent_number="2", 
            WebSiteSummary=WebSiteSummary or "No summary available",
            History=history
        )
        agent_2_response_2 = generate_response(agent_2_prompt_2)
        print('\033[92m' + 'agent_2_response_2:', agent_2_response_2 + '\033[0m')
        conversation.append({"agent": "Agent 2", "message": agent_2_response_2})

        # Generate a summary
        summary_prompt = """
        You are Judge Agent analyzing the debate. Your task is to summarize the key arguments made by both agents and provide a final decision about whether we should consider working with this client.

        Follow these steps:
        1. Summarize the main points made by Agent 1 and Agent 2.
        2. Evaluate the strengths and weaknesses of each argument.
        3. Provide a final decision starting with "FINAL DECISION: ..." and explain your reasoning.

        Here is the conversation so far:
        """ + "\n".join([f"{m['agent']}: {m['message']}" for m in conversation])

        # Generate the summary
        summary = generate_response(summary_prompt, max_tokens=500)  # Increase max_tokens if needed

        # Extract the "FINAL DECISION" section
        final_decision_start = summary.upper().find("FINAL DECISION:")
        if final_decision_start != -1:
            summary = summary[final_decision_start:].strip()
        else:
            summary = "FINAL DECISION: Unable to determine a clear decision from the discussion."

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
