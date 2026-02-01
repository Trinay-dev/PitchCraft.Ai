import streamlit as st
import requests
import json
from pptx import Presentation
from pptx.util import Inches

st.set_page_config(page_title="PitchCraft AI")

st.title("PitchCraft AI")

# ---------------- INPUTS ----------------

idea = st.text_input("Business Idea")
customer = st.text_input("Target Customer")
price = st.number_input("Price per customer", min_value=0)
cost = st.number_input("Monthly cost", min_value=0)
customers = st.number_input("Customers (Month 1)", min_value=1)

# ---------------- GEMINI REST ----------------
def call_gemini(prompt):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.0-pro:generateContent"



    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(
        f"{url}?key={st.secrets['GEMINI_API_KEY']}",
        headers=headers,
        data=json.dumps(payload)
    )

    result = response.json()

    if "candidates" in result:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return json.dumps(result, indent=2)

# ---------------- GENERATE ----------------

if st.button("Generate"):

    prompt = f"""
Create a startup pitch.

Business: {idea}
Customer: {customer}

Return EXACTLY:

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
    st.write(f"Monthly Revenue: ₹{revenue:,}")
    st.write(f"Monthly Profit: ₹{profit:,}")

    prs = Presentation()

    slides = [
        ("Title", f"{idea} for {customer}"),
        ("Pitch", ai_text),
        ("Revenue", f"₹{revenue:,}"),
        ("Profit", f"₹{profit:,}")
    ]

    for title, body in slides:
        slide = prs.slides.add_slide(prs.slide_layouts[6])

        slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(8), Inches(1)).text_frame.text = title
        slide.shapes.add_textbox(Inches(1), Inches(2), Inches(8), Inches(4)).text_frame.text = body

    prs.save("pitchcraft.pptx")

    with open("pitchcraft.pptx", "rb") as f:
        st.download_button("Download PPT", f, file_name="pitchcraft.pptx")


