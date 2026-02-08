import streamlit as st
from pptx import Presentation
from pptx.util import Inches, Pt

# ---------------- APP TITLE ----------------
st.set_page_config(page_title="PitchCraft AI", layout="centered")
st.title("PitchCraft AI")
st.caption("Intelligent Startup Pitch Generator")

# ---------------- USER INPUTS ----------------
idea = st.text_input("Business Idea")
customer = st.text_input("Target Customer")
price = st.number_input("Price per customer", min_value=0)
cost = st.number_input("Monthly cost", min_value=0)
customers = st.number_input("Customers (Month 1)", min_value=1)

# ---------------- GENERATE ----------------
if st.button("Generate"):

    # ---------- AI REASONING (LOCAL, NO API) ----------
    problem = (
        f"{customer} customers often face inefficiencies related to {idea}, "
        "leading to wasted time, higher costs, and slower growth."
    )

    solution = (
        f"{idea} is designed specifically for {customer}, helping them "
        "solve these challenges efficiently while enabling scalable growth."
    )

    marketing = (
        f"We will reach {customer} through digital marketing, partnerships, "
        "and referral-driven growth focused on measurable ROI."
    )

    elevator = (
        f"{idea} helps {customer} reduce friction, save money, and grow faster "
        "using a simple and effective solution."
    )

    # ---------- FINANCIALS ----------
    revenue = price * customers
    profit = revenue - cost

    # ---------- DISPLAY IN APP ----------
    st.subheader("AI Pitch")

    st.markdown("### Problem")
    st.write(problem)

    st.markdown("### Solution")
    st.write(solution)

    st.markdown("### Marketing Strategy")
    st.write(marketing)

    st.markdown("### Elevator Pitch")
    st.write(elevator)

    st.subheader("Financial Snapshot")
    st.write(f"Monthly Revenue: ₹{revenue:,.0f}")
    st.write(f"Monthly Profit: ₹{profit:,.0f}")

    # ---------- CREATE PPT ----------
    prs = Presentation()

    slides_content = [
        ("PitchCraft AI", f"{idea} for {customer}"),
        ("Problem", problem),
        ("Solution", solution),
        ("Marketing Strategy", marketing),
        ("Elevator Pitch", elevator),
        ("Financials", f"Revenue: ₹{revenue:,.0f}\nProfit: ₹{profit:,.0f}")
    ]

    for title, content in slides_content:
        slide = prs.slides.add_slide(prs.slide_layouts[6])

        title_box = slide.shapes.add_textbox(
            Inches(1), Inches(0.8), Inches(8), Inches(1)
        )
        title_tf = title_box.text_frame
        title_tf.text = title
        title_tf.paragraphs[0].font.size = Pt(36)
        title_tf.paragraphs[0].font.bold = True

        body_box = slide.shapes.add_textbox(
            Inches(1), Inches(2), Inches(8), Inches(4.5)
        )
        body_tf = body_box.text_frame
        body_tf.text = content
        body_tf.paragraphs[0].font.size = Pt(20)

    ppt_filename = "PitchCraft_AI_Pitch.pptx"
    prs.save(ppt_filename)

    with open(ppt_filename, "rb") as file:
        st.download_button(
            label="Download Pitch Deck (PPT)",
            data=file,
            file_name=ppt_filename,
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
