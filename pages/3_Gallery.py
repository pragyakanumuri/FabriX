import streamlit as st
import sqlite3
import io
from PIL import Image

st.title("🖼 My Gallery")

user = st.session_state.get("user")
if user is None:
    st.warning("⚠️ Please log in to view your gallery.")
    st.stop()

conn = sqlite3.connect("fashion_app.db")

rows = conn.execute(
    "SELECT id, title, created_at, img FROM designs WHERE username=? ORDER BY created_at DESC",
    (user,)
).fetchall()

for design_id, title, ts, img_blob in rows:
    cols = st.columns([1, 3, 1])
    with cols[0]:
        st.image(Image.open(io.BytesIO(img_blob)), width=120)
    with cols[1]:
        st.markdown(f"**{title}**  \n_{ts}_")
    with cols[2]:
        if st.button("🗑 Delete", key=f"del{design_id}"):
            conn.execute("DELETE FROM designs WHERE id=?", (design_id,))
            conn.commit()
            st.experimental_rerun()
