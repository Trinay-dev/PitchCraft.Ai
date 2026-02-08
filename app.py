import streamlit as st
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="PitchCraft AI", layout="centered")
st.title("PitchCraft AI")
st.caption("Intelligent Startup Pitch Generator")

# ---------------- INPUTS ----------------
idea = st.text_input("Business Idea")
customer = st.text_input("Target Customer")
price = st.number_input("Price per customer", min_value=0)
cost = st.number_input("Monthly cost", min_value=0)
customers = st.number_input("Customers (Month 1)", min_value=1)

# ---------------- GENERATE ----------------
if st.button("Generate"):

    # --------- AI REASONING (LOCAL) ---------
    problem = (
        f"{customer} customers face repeated inefficiencies related to {idea}. "
        "These inefficiencies result in wasted time, higher operational costs, "
        "and limited ability to scale effectively in competitive markets."
    )

    solution = (
        f"{idea} is purpose-built for {customer}, offering a focused and efficient "
        "solution that removes friction, improves productivity, and enables "
        "sustainable, scalable growth."
    )

    marketing = (
        f"Our go-to-market strategy targets {customer} using digital marketing, "
        "strategic partnerships, referrals, and value-driven messaging that "
        "highlights measurable return on investment."
    )

    elevator = (
        f"{idea} empowers {customer} to solve real business problems faster and "
        "at lower cost, unlocking growth and efficiency with a simple, powerful solution."
    )

    revenue = price * customers
    profit = revenue - cost

    # ---------------- DISPLAY ----------------
    st.subheader("AI Pitch Overview")

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

    # ---------------- PPT GENERATION ----------------
    prs = Presentation()

    def add_slide(title_text, body_text):
        slide = prs.slides.add_slide(prs.slide_layouts[6])

        # Title
        title_box = slide.shapes.add_textbox(
            Inches(0.75), Inches(0.6), Inches(8.5), Inches(1.2)
        )
        title_tf = title_box.text_frame
        title_tf.clear()
        title_p = title_tf.paragraphs[0]
        title_p.text = title_text
        title_p.font.size = Pt(38)
        title_p.font.bold = True
        title_p.alignment = PP_ALIGN.CENTER

        # Body
        body_box = slide.shapes.add_textbox(
            Inches(1), Inches(2.2), Inches(8), Inches(4.5)
        )
        body_tf = body_box.text_frame
        body_tf.word_wrap = True
        body_tf.clear()

        for line in body_text.split(". "):
            p = body_tf.add_paragraph()
            p.text = line.strip() + "."
            p.font.size = Pt(20)
            p.font.bold = False
            p.space_after = Pt(12)

        body_tf.paragraphs[0].level = 0

    # Slides
    add_slide(
        "PitchCraft AI",
        f"{idea} designed for {customer}. A smarter way to build and present startup ideas."
    )

    add_slide("Problem", problem)
    add_slide("Solution", solution)
    add_slide("Marketing Strategy", marketing)
    add_slide("Elevator Pitch", elevator)

    add_slide(
        "Financial Overview",
        f"Monthly Revenue is ₹{revenue:,.0f}. "
        f"Monthly Profit is ₹{profit:,.0f}. "
        "This model demonstrates strong scalability and financial viability."
    )

    ppt_file = "PitchCraft_AI_Pitch.pptx"
    prs.save(ppt_file)

    with open(ppt_file, "rb") as f:
        st.download_button(
            "Download Styled Pitch Deck (PPT)",
            f,
            file_name=ppt_file,
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
