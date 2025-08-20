# main.py
import os
import json
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI

# ---------------------------
# Set your OpenAI API key here
# ---------------------------
OPENAI_API_KEY = "load the varible from .env"  # todo: repalce key
client = OpenAI(api_key=OPENAI_API_KEY)

# ---------------------------
# FastAPI setup
# ---------------------------
app = FastAPI(title="Cybruxer Agent Matcher")

# ---------------------------
# Company context
# ---------------------------
COMPANY_CONTEXT = """
Cybruxer is a deep-tech cybersecurity startup founded in 2023 in Tallinn, Estonia.
Mission: "To outthink cyber threats by creating AI defenders that never sleep, never forget, and always adapt."
Products: Cybruxer Sentinel, PhantomShield, ThreatForge, BlackIce API.
Culture: Hybrid, elite team of 28 engineers, data scientists, ethical hackers.
"""

AGENTS = {
    "Office Manager": "Handles office-related questions.",
    "Web Developer": "Handles technical and development questions.",
    "Head of HR": "Handles recruitment and employee-related questions.",
    "Salesperson": "Handles product, business model, and client-related questions."
}

# ---------------------------
# Request model
# ---------------------------
class AskRequest(BaseModel):
    prompt: str

# ---------------------------
# Utility functions
# ---------------------------
def log_interaction(data):
    filename = "interactions.json"
    try:
        with open(filename, "r", encoding="utf-8") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []

    history.append(data)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def ask_openai(messages):
    """Send a message list to OpenAI and get response"""
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return resp.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def triage_agents(prompt):
    """Ask a triage agent which agents should answer the question."""
    messages = [
        {"role": "system", "content": "You are a smart triage agent for Cybruxer."},
        {"role": "system", "content": COMPANY_CONTEXT},
        {"role": "user", "content": f"""Question: {prompt}
Decide which agents need to answer and in which order. 
Return only a JSON object like this:
{{ "agents": ["Head of HR", "Web Developer"], "reason": "Head of HR answers timelines, Web Developer answers role requirements" }}
"""}
    ]
    response = ask_openai(messages)

    # נסה לפרסר JSON מהתשובה
    try:
        data = json.loads(response)
        agents_involved = data.get("agents", [])
    except Exception:
        agents_involved = ["Office Manager"]  # fallback

    return agents_involved, response


def ask_agent(agent_name, prompt):
    """Ask a single agent a question"""
    messages = [
        {"role": "system", "content": f"You are {agent_name}. {AGENTS[agent_name]}"},
        {"role": "system", "content": COMPANY_CONTEXT},
        {"role": "user", "content": prompt}
    ]
    response = ask_openai(messages)
    return response

# ---------------------------
# Main endpoint
# ---------------------------
@app.post("/ask")
async def ask(request: AskRequest):
    prompt = request.prompt
    timestamp = datetime.utcnow().isoformat()

    # Step 1: Triage - find which agents are involved
    agents_involved, triage_response = triage_agents(prompt)

    conversation = []
    final_answer_parts = []

    # Step 2: Ask each agent in order
    for agent in agents_involved:
        agent_response = ask_agent(agent, prompt)
        conversation.append({"agent": agent, "message": agent_response})
        final_answer_parts.append(f"[{agent}]: {agent_response}")

    final_answer = "\n\n".join(final_answer_parts)

    # Step 3: Log
    log_interaction({
        "timestamp": timestamp,
        "user_prompt": prompt,
        "agents_involved": agents_involved,
        "conversation": conversation,
        "final_answer": final_answer
    })

    return {
        "agents_involved": agents_involved,
        "conversation": conversation,
        "final_answer": final_answer
    }
