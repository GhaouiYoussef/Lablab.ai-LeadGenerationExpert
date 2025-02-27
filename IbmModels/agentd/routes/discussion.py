from fastapi import APIRouter, HTTPException
from ibm_watson import generate_response
from database import discussions_collection

router = APIRouter()

def agent_interaction(WebSiteSummary: str, UserCompany: str = 'AI Consulting') -> list:
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

    return conversation

@router.get("/agents-discussion/")
async def agents_discussion(WebSiteSummary: str = None):
    """Handles a structured agent discussion and returns a summary."""
    try:
        conversation = agent_interaction(WebSiteSummary)

        summary_prompt = f"""
        You are Judge Agent analyzing the debate. You must provide an argumented final decision to either proceed or not.
        Debate:
        {conversation}
        """
        
        summary = generate_response(summary_prompt, model_id='ibm/granite-13b-instruct-v2', max_tokens=100)

        # Extract "FINAL DECISION"
        final_decision_start = summary.upper().find("FINAL DECISION:")
        summary = summary[final_decision_start:].strip() if final_decision_start != -1 else "FINAL DECISION: Unable to determine."

        # Store in MongoDB
        discussion_data = {"summary": summary, "history": conversation}
        discussions_collection.insert_one(discussion_data)

        return {"summary": summary, "history": conversation}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
