import streamlit as st
import sqlite3
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
from utils.design_tools import pillow_from_streamlit, img_to_b64_png
from utils.db import init_db

st.title("🎨 Draw Your Design")

user = st.session_state.get("user")
if user is None:
    st.warning("⚠️ Please log in to use the drawing canvas.")
    st.stop()  # Stop here if no user logged in

# Sidebar controls
stroke_width = st.sidebar.slider("Brush size", 1, 50, 10)
stroke_color = st.sidebar.color_picker("Brush color", "#000000")
bg_color     = st.sidebar.color_picker("Background", "#ffffff")
realtime     = st.sidebar.checkbox("Update in realtime", True)

# Drawing canvas
canvas_result = st_canvas(
    fill_color="rgba(0,0,0,0)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=500,
    width=400,
    drawing_mode="freedraw",
    update_streamlit=realtime,
    key="canvas",
)

# Save button
if st.button("✅ Save to Gallery"):
    img = pillow_from_streamlit(canvas_result)
    if img is None:
        st.error("No drawing found to save!")
    else:
        png_bytes = img_to_b64_png(img)
        with sqlite3.connect("fashion_app.db") as conn:
            conn.execute(
                "INSERT INTO designs(username, title, apparel_type, img) VALUES (?, ?, ?, ?)",
                (
                    user,
                    st.session_state.get("title", "Untitled"),
                    "custom",
                    png_bytes,
                ),
            )
            conn.commit()
        st.success("Saved! View it in Gallery.")
