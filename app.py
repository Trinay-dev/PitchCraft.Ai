import streamlit as st
import google.generativeai as genai
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE
from pptx.chart.data import CategoryChartData

# ================= GEMINI =================
import os

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("models/gemini-1.5-flash")


# ================= UI =================
st.title("PitchCraft AI")

idea = st.text_input("Business Idea")
customer = st.text_input("Target Customer")
price = st.number_input("Price per customer", min_value=0)
cost = st.number_input("Monthly cost", min_value=0)
customers = st.number_input("Customers (Month 1)", min_value=1)

# ================= GENERATE =================
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

    response = model.generate_content(prompt)
    ai_text = response.text

    parts = ai_text.split("2.")
    problem = parts[0].replace("1. Problem:", "").strip()

    rest = parts[1].split("3.")
    solution = rest[0].replace("Solution:", "").strip()

    rest2 = rest[1].split("4.")
    marketing = rest2[0].replace("Marketing:", "").strip()
    elevator = rest2[1].replace("Elevator Pitch:", "").strip()

    revenue = price * customers
    profit = revenue - cost

    prs = Presentation()

    # ---------- COVER ----------
    cover = prs.slides.add_slide(prs.slide_layouts[6])
    cover.background.fill.solid()
    cover.background.fill.fore_color.rgb = RGBColor(15, 15, 20)

    t = cover.shapes.add_textbox(Inches(2), Inches(2.5), Inches(6), Inches(1.5))
    tf = t.text_frame
    r = tf.paragraphs[0].add_run()
    r.text = "PitchCraft AI"
    r.font.size = Pt(40)
    r.font.bold = True
    r.font.color.rgb = RGBColor(255, 255, 255)

    p = tf.add_paragraph()
    p.text = f"{idea} for {customer}"
    p.font.size = Pt(18)
    p.font.color.rgb = RGBColor(180, 180, 180)

    slides = [
        ("Problem", problem),
        ("Solution", solution),
        ("Marketing", marketing),
        ("Elevator Pitch", elevator),
    ]

    for title, content in slides:

        slide = prs.slides.add_slide(prs.slide_layouts[6])
        slide.background.fill.solid()
        slide.background.fill.fore_color.rgb = RGBColor(15, 15, 20)

        title_box = slide.shapes.add_textbox(Inches(1), Inches(0.7), Inches(8), Inches(1))
        ttf = title_box.text_frame
        tr = ttf.paragraphs[0].add_run()
        tr.text = title
        tr.font.size = Pt(28)
        tr.font.bold = True
        tr.font.color.rgb = RGBColor(0, 180, 255)

        body = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(8), Inches(4.5))
        body_tf = body.text_frame
        body_tf.word_wrap = True
        body_tf.clear()

        bp = body_tf.paragraphs[0]
        run = bp.add_run()
        run.text = content
        run.font.size = Pt(18)
        run.font.color.rgb = RGBColor(230, 230, 230)

        body_tf.margin_left = Pt(10)
        body_tf.margin_right = Pt(10)
        body_tf.margin_top = Pt(10)
        body_tf.margin_bottom = Pt(10)

    # ---------- CHART ----------
    chart_slide = prs.slides.add_slide(prs.slide_layouts[6])
    chart_slide.background.fill.solid()
    chart_slide.background.fill.fore_color.rgb = RGBColor(15, 15, 20)

    chart_title = chart_slide.shapes.add_textbox(Inches(1), Inches(0.6), Inches(8), Inches(1))
    ctf = chart_title.text_frame
    cr = ctf.paragraphs[0].add_run()
    cr.text = "Financial Snapshot"
    cr.font.size = Pt(28)
    cr.font.bold = True
    cr.font.color.rgb = RGBColor(0, 180, 255)

    chart_data = CategoryChartData()
    chart_data.categories = ["Month 1"]
    chart_data.add_series("Revenue", (revenue,))
    chart_data.add_series("Profit", (profit,))

    chart_slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED,
        Inches(2), Inches(2), Inches(6), Inches(4),
        chart_data
    )

    prs.save("pitchcraft.pptx")

    st.success("PPT created: pitchcraft.pptx")



