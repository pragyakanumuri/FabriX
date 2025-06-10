import streamlit as st
import os
from PIL import Image

st.title("👚 Create Apparel Design")

user = st.session_state.get("user")
if user is None:
    st.warning("⚠️ Please log in first to create a design.")
    st.stop()  # Stop here if not logged in

# ────────────── Apparel types and subtypes ──────────────
apparel_options = {
    "T-Shirt": ["Oversized", "Fit", "Athletic"],
    "Dress": ["Maxi", "Mini", "Bodycon"],
    "Hoodie": ["Zipper", "Pullover"],
    "Skirt": ["Pencil", "Pleated"],
    "Shirt": ["Formal", "Casual"],
    "Blazer": ["Single-breasted", "Double-breasted"],
    "Jacket": ["Bomber", "Denim", "Puffer"],
    "Pant": ["Chinos", "Joggers", "Formal"],
    "Jeans": ["Skinny", "Straight", "Bootcut"],
    "Frock": ["Party", "Casual"],
    "Kurti": ["A-Line", "Straight Cut"],
    "Kurta": ["Pathani", "Angrakha"],
    "Shorts": ["Denim", "Cargo"],
    "Tote Bag": ["Canvas", "Leather"],
    "Hat": ["Beanie", "Bucket"],
    "Belt": ["Leather", "Fabric"]
}

apparel = st.selectbox("Choose apparel type", list(apparel_options.keys()))
subtype = st.selectbox(f"Choose {apparel} style", apparel_options[apparel])

# ────────────── Fabric options ──────────────
fabric_options = [
    "Cotton", "Silk", "Denim", "Linen", "Wool",
    "Polyester", "Rayon", "Velvet", "Chiffon", "Georgette"
]
fabric = st.selectbox("Choose fabric", fabric_options)

# ────────────── Design title ──────────────
title = st.text_input("Design title")

# ────────────── Size selection ──────────────
sizes = ["XS", "S", "M", "L", "XL", "XXL"]
size = st.selectbox("Select size", sizes)

# ────────────── Price range slider ──────────────
price = st.slider("Select price range (₹)", 500, 5000, (1000, 3000), step=100)

# ────────────── Front/Back toggle ──────────────
if "view_side" not in st.session_state:
    st.session_state.view_side = "front"

col1, col2 = st.columns(2)
with col1:
    if st.button("Front"):
        st.session_state.view_side = "front"
with col2:
    if st.button("Back"):
        st.session_state.view_side = "back"

# ────────────── Show template if exists ──────────────
template_dir = "assets/apparel_templates"
side_suffix = "_front" if st.session_state.view_side == "front" else "_back"
filename = f"{apparel.lower().replace(' ', '_')}_{subtype.lower().replace(' ', '_')}{side_suffix}.png"
template_file = os.path.join(template_dir, filename)

if os.path.isfile(template_file):
    st.image(template_file, width=300, caption=f"{apparel} ({subtype}) - {st.session_state.view_side.capitalize()} View")
else:
    st.warning(f"No template found for {apparel} - {subtype} ({st.session_state.view_side} view).")

# ────────────── Optional size chart ──────────────
if st.checkbox("📏 Show size chart"):
    st.markdown("### 📐 Size Chart (in inches)")
    st.table({
        "Size": ["XS", "S", "M", "L", "XL", "XXL"],
        "Chest": [32, 34, 36, 38, 40, 42],
        "Waist": [24, 26, 28, 30, 32, 34],
        "Length": [25, 26, 27, 28, 29, 30]
    })
