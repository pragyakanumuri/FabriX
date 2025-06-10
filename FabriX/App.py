import streamlit as st
from utils.auth import login_flow
from utils.db   import init_db
from streamlit_drawable_canvas import st_canvas


st.set_page_config(page_title="Fashion Design Studio", layout="wide")
init_db()                                # ensure DB & tables exist
user = login_flow()                      # simple username/password auth

# Streamlit will automatically show pages/*.py as navigation tabs
st.sidebar.success(f"Logged in as *{user['username']}*")