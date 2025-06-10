import streamlit as st
import hashlib, sqlite3, os

DB = "fashion_app.db"

def _hash(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def _get_conn():
    return sqlite3.connect(DB, check_same_thread=False)

def login_flow():
    st.sidebar.header("🔐 Login / Sign-Up")
    tab = st.sidebar.radio("", ["Login", "Sign-Up"], label_visibility="collapsed")

    if tab == "Sign-Up":
        new_user = st.sidebar.text_input("Username")
        new_pw   = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Create account"):
            with _get_conn() as conn:
                conn.execute(
                    "CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, pw TEXT)"
                )
                try:
                    conn.execute("INSERT INTO users VALUES(?,?)", (new_user, _hash(new_pw)))
                    conn.commit()
                    st.sidebar.success("Account created. Please log in.")
                except sqlite3.IntegrityError:
                    st.sidebar.error("Username already exists.")

    # --- login ---
    user = st.sidebar.text_input("Username", key="login_user")
    pw   = st.sidebar.text_input("Password", type="password", key="login_pw")
    if st.sidebar.button("Login"):
        with _get_conn() as conn:
            row = conn.execute(
                "SELECT pw FROM users WHERE username=?", (user,)
            ).fetchone()
        if row and _hash(pw) == row[0]:
            st.session_state["authenticated"] = True
            st.session_state["user"] = user
        else:
            st.sidebar.error("Invalid credentials")

    if st.session_state.get("authenticated"):
        return {"username": st.session_state["user"]}
    else:
        st.stop()          # halt all other page code until authenticated