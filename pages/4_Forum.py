import io, sqlite3
import streamlit as st
from PIL import Image

st.title("💬 Design Forum")

# 0️⃣  Make sure the user is logged in
user = st.session_state.get("user")
if user is None:
    st.warning("Please log in first.")
    st.stop()

conn = sqlite3.connect("fashion_app.db", check_same_thread=False)

# 1️⃣  NEW POST
design_options = conn.execute(
    "SELECT id, title FROM designs WHERE username=?", (user,)
).fetchall()

if design_options:
    design_dict = {f"{title} (id:{did})": did for did, title in design_options}
    sel = st.selectbox("Choose one of your designs to post", list(design_dict))
    caption = st.text_area("Caption")

    if st.button("Post"):
        conn.execute(
            "INSERT INTO posts(username, design_id, caption) VALUES (?,?,?)",
            (user, design_dict[sel], caption.strip())
        )
        conn.commit()
        st.success("Posted!")
        st.experimental_rerun()
else:
    st.info("You don’t have any saved designs yet. Create one first!")

st.divider()

# 2️⃣  FEED
rows = conn.execute("""
    SELECT p.id, d.img, p.caption, p.username, p.likes
    FROM posts AS p
    JOIN designs AS d ON p.design_id = d.id
    ORDER BY p.likes DESC, p.id DESC
""").fetchall()

for post_id, img_blob, cap, post_user, likes in rows:
    try:
        st.image(Image.open(io.BytesIO(img_blob)), width=300)
    except Exception:
        st.error("⚠️ Image corrupted or wrong format")
        continue

    st.markdown(f"**{cap}**  \n_Posted by {post_user}_")
    col_like, col_btn = st.columns([1, 1])
    col_like.markdown(f"👍 {likes}")

    if col_btn.button("Like", key=f"like{post_id}"):
        with conn:
            conn.execute("UPDATE posts SET likes = likes + 1 WHERE id=?", (post_id,))
        st.experimental_rerun()
    st.divider()
