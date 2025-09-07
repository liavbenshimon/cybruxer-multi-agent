# Cybruxer Multi-Agent API

## Overview

**Cybruxer Multi-Agent** is an intelligent API service designed for Cybruxer, a deep-tech cybersecurity startup founded in 2023 in Tallinn, Estonia. The project leverages OpenAI's GPT models and FastAPI to create a multi-agent system that can answer questions by routing them to the most relevant virtual "agent" based on company context.

## Mission

> "To outthink cyber threats by creating AI defenders that never sleep, never forget, and always adapt."

## Products

- **Cybruxer Sentinel**
- **PhantomShield**
- **ThreatForge**
- **BlackIce API**

## Team & Culture

- Hybrid, elite team of 28 engineers, data scientists, and ethical hackers.

---

## How It Works

1. **User Prompt:** The user sends a question to the `/ask` endpoint.
2. **Triage Agent:** The system uses a triage agent (powered by OpenAI) to decide which company agents should answer the question.
3. **Agent Responses:** Each relevant agent (Office Manager, Web Developer, Head of HR, Salesperson) answers the question in turn.
4. **Logging:** All interactions are logged in `interactions.json` for traceability.
5. **Final Answer:** The API returns a structured response with all agent answers.

---

## Agents

- **Office Manager:** Handles office-related questions.
- **Web Developer:** Handles technical and development questions.
- **Head of HR:** Handles recruitment and employee-related questions.
- **Salesperson:** Handles product, business model, and client-related questions.

---

## API Usage

### Endpoint

- `POST /ask`
  - **Body:** `{ "prompt": "Your question here" }`
  - **Response:**
    - `agents_involved`: List of agents who answered
    - `conversation`: Each agent's answer
    - `final_answer`: Combined answer

### Example

```json
{
  "prompt": "Can we hire a ReactJS developer for the new product launch?"
}
```

**Response:**

```json
{
  "agents_involved": ["Head of HR"],
  "conversation": [
    {
      "agent": "Head of HR",
      "message": "Yes, hiring a ReactJS developer for your new product launch would be a great idea..."
    }
  ],
  "final_answer": "Yes, hiring a ReactJS developer for your new product launch would be a great idea..."
}
```

---

## Technology Stack

- **Python**
- **FastAPI**
- **OpenAI GPT-4o-mini**
- **Pydantic**
- **JSON for logging**
- **Requirements:** See `requirements.txt` for all dependencies.

---

## Setup

1. **Clone the repository**
2. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```
3. **Set your OpenAI API key**
   - Add your key to an `.env` file or set it in `main.py`.
4. **Run the API**
   ```
   uvicorn main:app --reload
   ```

---

## Logging

All interactions are saved in `interactions.json` for audit and review.

---

## Example Interactions

- **Office questions:** "Where is the coffee in the office?"
- **Tech questions:** "What is ReactJS?"
- **HR questions:** "Can we hire a ReactJS developer for the new product launch?"

---

## Contributing

Feel free to open issues or submit pull requests to improve the multi-agent system or add new agents.

---

## License

This project is for educational and demonstration purposes.

---
