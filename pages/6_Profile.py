import streamlit as st
import sqlite3

user = st.session_state.get("user")
if user is None:
    st.warning("⚠️ Please log in to view your profile.")
    st.stop()

st.title("👤 My Profile")
st.write(f"*Username:* {user}")

with sqlite3.connect("fashion_app.db") as conn:
    n_designs = conn.execute(
        "SELECT COUNT(*) FROM designs WHERE username=?", (user,)
    ).fetchone()[0]

st.write(f"*Total designs saved:* {n_designs}")

if st.button("Log out"):
    st.session_state.clear()
    st.experimental_rerun()
