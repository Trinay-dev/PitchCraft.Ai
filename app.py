import streamlit as st
import requests
import json
from pptx import Presentation
from pptx.util import Inches

# ---------------- UI ----------------
st.title("PitchCraft AI")

idea = st.text_input("Business Idea")
customer = st.text_input("Target Customer")
price = st.number_input("Price per customer", min_value=0)
cost = st.number_input("Monthly cost", min_value=0)
customers = st.number_input("Customers (Month 1)", min_value=1)

# ---------------- GEMINI CALL ----------------
def call_gemini(prompt):
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        params={"key": st.secrets["GEMINI_API_KEY"]},
        data=json.dumps(payload),
        timeout=30
    )

    result = response.json()

    if "candidates" in result:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return "AI Error:\n" + json.dumps(result, indent=2)

# ---------------- GENERATE ----------------
if st.button("Generate"):
    prompt = f"""
Create a startup pitch.

Business: {idea}
Customer: {customer}

Return EXACTLY in this format:

1. Problem:
2. Solution:
3. Marketing:
4. Elevator Pitch:
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
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "PitchCraft AI"
    slide.placeholders[1].text = ai_text

    prs.save("pitchcraft.pptx")

    with open("pitchcraft.pptx", "rb") as f:
        st.download_button("Download PPT", f, file_name="pitchcraft.pptx")
