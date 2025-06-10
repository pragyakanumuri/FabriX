import streamlit as st
import openai
from openai.error import RateLimitError

# Set your OpenAI API key — make sure you have it in secrets or env variable
# openai.api_key = st.secrets["openai_api_key"]

def ai_suggest(prompt, n):
    try:
        res = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            n=n
        )
        return [choice['message']['content'] for choice in res['choices']]
    except RateLimitError:
        return ["Rate limit exceeded. Please try again later or check your API usage."]

st.title("🤖 AI Design Assistant")

user = st.session_state.get("user")
if user is None:
    st.warning("⚠️ Please log in to use the AI assistant.")
    st.stop()

prompt = st.text_area("Describe the style or garment you’d like ideas for")
n = st.slider("How many suggestions?", 1, 5, 3)

if st.button("Generate"):
    if not prompt.strip():
        st.error("Please enter a description to generate ideas.")
    else:
        with st.spinner("Thinking..."):
            ideas = ai_suggest(prompt, n)
        for i, text in enumerate(ideas, 1):
            st.markdown(f"*Idea {i}*: {text}")
