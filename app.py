import streamlit as st
import requests
import json
from pptx import Presentation
from pptx.util import Inches, Pt

st.set_page_config(page_title="PitchCraft AI", layout="centered")

st.title("PitchCraft AI")

# ---------------- INPUTS ----------------
def call_gemini(prompt):
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(
        f"{url}?key={st.secrets['GEMINI_API_KEY']}",
        headers=headers,
        data=json.dumps(payload)
    )

    result = response.json()

    # SAFE RETURN (no crash)
    if "candidates" in result:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return "Gemini API error:\n" + json.dumps(result, indent=2)


# ---------------- GENERATE ----------------

if st.button("Generate"):

    prompt = f"""
Create a startup pitch.

Business: {idea}
Customer: {customer}

Return EXACTLY in this format:

Problem:
Solution:
Marketing:
Elevator Pitch:
"""

    ai_text = call_gemini(prompt)

    st.subheader("AI Pitch")

    st.write(ai_text)

    revenue = price * customers
    profit = revenue - cost

    st.subheader("Financial Snapshot")
    st.write("Monthly Revenue: ₹{:,.0f}".format(revenue))
    st.write("Monthly Profit: ₹{:,.0f}".format(profit))

    # ---------------- PPT ----------------

    prs = Presentation()

    slides = [
        ("Title", f"{idea} for {customer}"),
        ("Pitch", ai_text),
        ("Revenue", f"Monthly Revenue: ₹{revenue:,}"),
        ("Profit", f"Monthly Profit: ₹{profit:,}")
    ]

    for title, body in slides:
        slide = prs.slides.add_slide(prs.slide_layouts[6])

        title_box = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(8), Inches(1))
        title_tf = title_box.text_frame
        title_tf.text = title

        body_box = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(8), Inches(4.5))
        body_tf = body_box.text_frame
        body_tf.text = body

    prs.save("pitchcraft.pptx")

    with open("pitchcraft.pptx", "rb") as f:
        st.download_button("Download PPT", f, file_name="pitchcraft.pptx")


