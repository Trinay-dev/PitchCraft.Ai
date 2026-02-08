import streamlit as st
from google import genai
from pptx import Presentation
from pptx.util import Inches

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="PitchCraft AI")
st.title("PitchCraft AI")

# ---------------- GEMINI CLIENT ----------------
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# ---------------- INPUTS ----------------
idea = st.text_input("Business Idea")
customer = st.text_input("Target Customer")
price = st.number_input("Price per customer", min_value=0)
cost = st.number_input("Monthly cost", min_value=0)
customers = st.number_input("Customers (Month 1)", min_value=1)

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

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    ai_text = response.text

    st.subheader("AI Pitch")
    st.write(ai_text)

    # ---------------- FINANCIALS ----------------
    revenue = price * customers
    profit = revenue - cost

    st.subheader("Financial Snapshot")
    st.write(f"Monthly Revenue: ₹{revenue:,}")
    st.write(f"Monthly Profit: ₹{profit:,}")

    # ---------------- PPT GENERATION ----------------
    prs = Presentation()

    slides = [
        ("Title", f"{idea} for {customer}"),
        ("Pitch", ai_text),
        ("Revenue", f"Monthly Revenue: ₹{revenue:,}"),
        ("Profit", f"Monthly Profit: ₹{profit:,}")
    ]

    for title, body in slides:
        slide = prs.slides.add_slide(prs.slide_layouts[6])

        title_box = slide.shapes.add_textbox(
            Inches(1), Inches(0.5), Inches(8), Inches(1)
        )
        title_box.text_frame.text = title

        body_box = slide.shapes.add_textbox(
            Inches(1), Inches(2), Inches(8), Inches(4)
        )
        body_box.text_frame.text = body

    prs.save("pitchcraft.pptx")

    with open("pitchcraft.pptx", "rb") as f:
        st.download_button(
            "Download PPT",
            f,
            file_name="pitchcraft.pptx"
        )
