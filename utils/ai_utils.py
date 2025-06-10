import openai, streamlit as st, os

openai.api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", ""))

def ai_suggest(prompt: str, n=1):
    """
    Call GPT-4o designer coach with a short prompt and return text completions.
    """
    if not openai.api_key:
        return ["(No API key configured)"]
    res = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful fashion-design assistant."},
            {"role": "user", "content": prompt}
        ],
        n=n
    )
    return [choice.message.content.strip() for choice in res.choices]