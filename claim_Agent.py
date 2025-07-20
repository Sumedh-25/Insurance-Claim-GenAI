# claim_agent.py

import openai
import json
import os

# Set your OpenAI API key (use environment variables in production)
api_key = os.getenv("OPENAI_API_KEY")

# Load static policy info (for FAQs or rule-based support)
def load_policy_knowledge():
    with open("data/policy_info.json", "r") as file:
        return json.load(file)

# Generate a GPT-4 based response to user queries
def respond_to_user(query, chat_history=None):
    system_prompt = (
        "You are an intelligent Insurance Claim Assistant. "
        "You help users file claims, answer insurance questions, and check claim status. "
        "Always provide clear, step-by-step, and actionable solutions to any problem the user describes. "
        "If you do not know the answer, suggest practical next steps or where the user can get help. "
        "Be helpful, polite, and clear."
    )

    messages = [{"role": "system", "content": system_prompt}]
    if chat_history:
        messages.extend(chat_history)
    messages.append({"role": "user", "content": query})

    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.5,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Sorry, I couldn't process your request due to an internal error: {str(e)}. Please check your API key and internet connection, or try again later."

# Simulate collecting claim filing information
def collect_claim_info():
    return {
        "required_fields": [
            "Full Name",
            "Policy Number",
            "Date of Incident",
            "Type of Claim (Health, Vehicle, Property, etc.)",
            "Description of Incident",
            "Amount Claimed"
        ],
        "instructions": "Please fill out the above details to initiate your claim."
    }

# Simulate claim tracking
def track_claim(claim_id):
    # In real-world: Query a database or API
    dummy_status = {
        "C12345": "Under Review",
        "C67890": "Approved - Payment Processing",
        "C00001": "Rejected - Incomplete Documents"
    }
    return dummy_status.get(claim_id, "No claim found with this ID.")

