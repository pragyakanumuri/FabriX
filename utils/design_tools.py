from PIL import Image
import io, base64, datetime

def pillow_from_streamlit(canvas_result):
    if canvas_result.image_data is None:
        return None
    return Image.fromarray(canvas_result.image_data.astype("uint8"))

def img_to_b64_png(img: Image.Image) -> bytes:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()