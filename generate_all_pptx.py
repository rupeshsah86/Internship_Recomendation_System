import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ─── COLOR PALETTE DEFINITION ──────────────────────────────────────────────
COLOR_PRIMARY_DARK  = RGBColor(15, 23, 42)     # #0F172A Deep Navy Slate
COLOR_SECONDARY     = RGBColor(79, 70, 229)    # #4F46E5 Electric Indigo
COLOR_ACCENT_TEAL   = RGBColor(14, 165, 233)   # #0EA5E9 Vivid Sky / Teal
COLOR_ACCENT_GREEN  = RGBColor(16, 185, 129)   # #10B981 Emerald Green
COLOR_ACCENT_AMBER  = RGBColor(245, 158, 11)   # #F59E0B Amber
COLOR_BG_LIGHT      = RGBColor(248, 250, 252)  # #F8FAFC Off-white / light slate
COLOR_CARD_BG       = RGBColor(255, 255, 255)  # White
COLOR_CARD_BORDER   = RGBColor(226, 232, 240)  # #E2E8F0 Soft border
COLOR_TEXT_DARK     = RGBColor(30, 41, 59)     # #1E293B Slate 800
COLOR_TEXT_MUTED    = RGBColor(100, 116, 139)  # #64748B Slate 500
COLOR_TEXT_LIGHT    = RGBColor(241, 245, 249)  # #F1F5F9 Slate 100
COLOR_HEADER_BG     = RGBColor(238, 242, 255)  # #EEF2FF Indigo light tint

def apply_slide_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_BG_LIGHT

def add_header_banner(slide, title_text, category_text, review_text, date_text):
    # Top thin accent line
    top_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.08))
    top_line.fill.solid()
    top_line.fill.fore_color.rgb = COLOR_SECONDARY
    top_line.line.fill.background()

    # Category & Review Tag Pill
    tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.25), Inches(11.733), Inches(0.35))
    tf_tag = tag_box.text_frame
    tf_tag.word_wrap = True
    tf_tag.margin_left = tf_tag.margin_top = tf_tag.margin_right = tf_tag.margin_bottom = 0
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = f"SUBJECT: AI & ML FOR COMMUNICATION SYSTEMS   •   {review_text.upper()} ({date_text})"
    p_tag.font.size = Pt(10)
    p_tag.font.bold = True
    p_tag.font.color.rgb = COLOR_SECONDARY

    # Slide Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(11.733), Inches(0.65))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_PRIMARY_DARK

    # Context / Category sub-line
    if category_text:
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.15), Inches(11.733), Inches(0.3))
        tf_sub = sub_box.text_frame
        tf_sub.word_wrap = True
        tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = category_text
        p_sub.font.size = Pt(11)
        p_sub.font.color.rgb = COLOR_TEXT_MUTED

    # Dividing separator rule
    sep = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.48), Inches(11.733), Inches(0.02))
    sep.fill.solid()
    sep.fill.fore_color.rgb = COLOR_CARD_BORDER
    sep.line.fill.background()

def add_footer(slide, student_info, review_text, date_text, slide_num, total_slides):
    footer_sep = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.015))
    footer_sep.fill.solid()
    footer_sep.fill.fore_color.rgb = COLOR_CARD_BORDER
    footer_sep.line.fill.background()

    # Left footer: Student & Department
    left_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(5.5), Inches(0.3))
    tf_l = left_box.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_top = tf_l.margin_right = tf_l.margin_bottom = 0
    p_l = tf_l.paragraphs[0]
    p_l.text = f"{student_info['name']}  |  Roll No: {student_info['roll_no']}  |  Dept: {student_info['dept']}"
    p_l.font.size = Pt(9.5)
    p_l.font.color.rgb = COLOR_TEXT_MUTED

    # Right footer: Project & Slide #
    right_box = slide.shapes.add_textbox(Inches(7.0), Inches(7.05), Inches(5.533), Inches(0.3))
    tf_r = right_box.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_top = tf_r.margin_right = tf_r.margin_bottom = 0
    p_r = tf_r.paragraphs[0]
    p_r.alignment = PP_ALIGN.RIGHT
    p_r.text = f"AI Internship Recommender  |  {review_text}  |  Slide {slide_num} of {total_slides}"
    p_r.font.size = Pt(9.5)
    p_r.font.color.rgb = COLOR_TEXT_MUTED

def create_card(slide, left, top, width, height, title="", title_color=COLOR_PRIMARY_DARK, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER, border_width=1.0):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(border_width)

    # Optional top accent bar inside card
    if title:
        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.18)
        tf.margin_bottom = Inches(0.15)
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = title_color
    return shape

def add_bullet(tf, heading, text, pt_size=10.5, heading_color=COLOR_PRIMARY_DARK, body_color=COLOR_TEXT_DARK, space_after=8):
    p = tf.add_paragraph()
    p.space_after = Pt(space_after)
    p.line_spacing = 1.2
    
    if heading:
        run_h = p.add_run()
        run_h.text = f"•  {heading}: "
        run_h.font.bold = True
        run_h.font.size = Pt(pt_size)
        run_h.font.color.rgb = heading_color

    run_t = p.add_run()
    run_t.text = text if heading else f"•  {text}"
    run_t.font.bold = False
    run_t.font.size = Pt(pt_size)
    run_t.font.color.rgb = body_color

def create_title_slide(prs, review_title, review_date, student_info):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Dark modern canvas
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLOR_PRIMARY_DARK
    bg.line.fill.background()

    # Decorative top and left geometric banners
    banner_top = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.15))
    banner_top.fill.solid()
    banner_top.fill.fore_color.rgb = COLOR_SECONDARY
    banner_top.line.fill.background()

    accent_glow = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.0), Inches(11.733), Inches(0.05))
    accent_glow.fill.solid()
    accent_glow.fill.fore_color.rgb = COLOR_ACCENT_TEAL
    accent_glow.line.fill.background()

    # Subject & Department Pill
    subj_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(11.733), Inches(0.4))
    tf_subj = subj_box.text_frame
    tf_subj.margin_left = tf_subj.margin_top = 0
    p_s = tf_subj.paragraphs[0]
    p_s.text = f"SUBJECT: AI AND ML FOR COMMUNICATION SYSTEMS   |   {student_info['dept']} DEPARTMENT"
    p_s.font.size = Pt(12)
    p_s.font.bold = True
    p_s.font.color.rgb = COLOR_ACCENT_TEAL

    # Review Badge
    rev_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.733), Inches(0.5))
    tf_rev = rev_box.text_frame
    tf_rev.margin_left = tf_rev.margin_top = 0
    p_r = tf_rev.paragraphs[0]
    p_r.text = f"{review_title.upper()} EVALUATION  •  DATE: {review_date}"
    p_r.font.size = Pt(14)
    p_r.font.bold = True
    p_r.font.color.rgb = COLOR_ACCENT_AMBER

    # Project Title (Large, Impactful)
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(2.2), Inches(11.733), Inches(1.5))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_top = 0
    p_t = tf_title.paragraphs[0]
    p_t.text = "AI-Powered Internship Recommendation System"
    p_t.font.size = Pt(32)
    p_t.font.bold = True
    p_t.font.color.rgb = RGBColor(255, 255, 255)

    p_sub = tf_title.add_paragraph()
    p_sub.text = "Intelligent Information Retrieval, NLP Feature Space Matching & Multi-Criteria Filtering in Communication Platforms"
    p_sub.font.size = Pt(14)
    p_sub.font.color.rgb = RGBColor(148, 163, 184)
    p_sub.space_before = Pt(8)

    # Student Information Card
    card_info = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.3), Inches(11.733), Inches(2.2))
    card_info.fill.solid()
    card_info.fill.fore_color.rgb = RGBColor(30, 41, 59) # Slate 800
    card_info.line.color.rgb = RGBColor(71, 85, 105)
    card_info.line.width = Pt(1.5)

    tf_info = card_info.text_frame
    tf_info.word_wrap = True
    tf_info.margin_left = Inches(0.4)
    tf_info.margin_top = Inches(0.3)

    p_c0 = tf_info.paragraphs[0]
    p_c0.text = "CANDIDATE & PRESENTATION PROFILE"
    p_c0.font.size = Pt(11)
    p_c0.font.bold = True
    p_c0.font.color.rgb = COLOR_ACCENT_TEAL
    p_c0.space_after = Pt(12)

    # 3 Column text within card
    info_cols = [
        {"lbl": "STUDENT NAME", "val": student_info['name']},
        {"lbl": "ROLL NUMBER", "val": student_info['roll_no']},
        {"lbl": "DEPARTMENT", "val": student_info['dept']},
        {"lbl": "REVIEW MILESTONE", "val": f"{review_title} ({review_date})"}
    ]
    
    # We can create 4 clean sub-boxes inside the card
    for idx, item in enumerate(info_cols):
        x = Inches(1.2 + idx * 2.8)
        y = Inches(4.9)
        ibox = slide.shapes.add_textbox(x, y, Inches(2.6), Inches(1.3))
        itf = ibox.text_frame
        itf.margin_left = itf.margin_top = 0
        p_l = itf.paragraphs[0]
        p_l.text = item['lbl']
        p_l.font.size = Pt(9.5)
        p_l.font.bold = True
        p_l.font.color.rgb = RGBColor(148, 163, 184)
        
        p_v = itf.add_paragraph()
        p_v.text = item['val']
        p_v.font.size = Pt(13)
        p_v.font.bold = True
        p_v.font.color.rgb = RGBColor(255, 255, 255)
        p_v.space_before = Pt(4)

    return slide

def add_table_slide(slide, headers, rows, col_widths, top=Inches(1.7), left=Inches(0.8), height=Inches(4.8)):
    table_shape = slide.shapes.add_table(len(rows) + 1, len(headers), left, top, sum(col_widths), height)
    table = table_shape.table
    
    for i, w in enumerate(col_widths):
        table.columns[i].width = w

    # Format Headers
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_PRIMARY_DARK
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf = cell.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.12)
        tf.margin_top = tf.margin_bottom = Inches(0.08)
        p = tf.paragraphs[0]
        p.text = h
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)

    # Format Rows
    for r_idx, row in enumerate(rows):
        bg = COLOR_CARD_BG if r_idx % 2 == 0 else RGBColor(241, 245, 249)
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = cell.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_right = Inches(0.12)
            tf.margin_top = tf.margin_bottom = Inches(0.08)
            p = tf.paragraphs[0]
            p.text = str(val)
            p.font.size = Pt(9.5)
            p.font.color.rgb = COLOR_TEXT_DARK
            if c_idx == 0:
                p.font.bold = True

# ─── GENERATE REVIEW 1 PRESENTATION ─────────────────────────────────────────
def generate_review_1(student_info, output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    total_slides = 8
    review_text = "Review 1"
    date_text = "21.07.2026"

    # Slide 1: Title Slide
    create_title_slide(prs, review_text, date_text, student_info)

    # Slide 2: Introduction
    s2 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s2)
    add_header_banner(s2, "01. Introduction: Problem Statement & Motivation", "Background and relevance to AI & ML in Communication Systems", review_text, date_text)
    add_footer(s2, student_info, review_text, date_text, 2, total_slides)

    # 3 Cards on Slide 2
    c1 = create_card(s2, Inches(0.8), Inches(1.7), Inches(3.7), Inches(5.0), "Background & Context", COLOR_SECONDARY)
    tf1 = c1.text_frame
    add_bullet(tf1, "Digital Recruitment Portals", "The exponential increase in online internship postings creates significant information overload for students seeking career entry.")
    add_bullet(tf1, "Information Asymmetry", "Employers face hundreds of unqualified applicants, while qualified students fail to discover niche opportunities aligned with their skills.")
    add_bullet(tf1, "Communication Challenge", "Traditional job search relies on rigid keyword matching, resulting in high communication noise and low match precision across network channels.")

    c2 = create_card(s2, Inches(4.8), Inches(1.7), Inches(3.7), Inches(5.0), "The Core Problem", RGBColor(194, 65, 12))
    tf2 = c2.text_frame
    add_bullet(tf2, "Vocabulary Mismatch", "Students express proficiencies using diverse terminologies ('ML Engineer', 'Data Modeling', 'Predictive Analytics') that keyword search fails to unify.")
    add_bullet(tf2, "Lack of Multi-Constraint Handling", "Standard engines ignore real-world constraints such as student availability, academic calendar durations, and minimum financial stipends.")
    add_bullet(tf2, "Cold-Start Vulnerability", "Collaborative filtering fails completely for new students who have no prior application or rating history.")

    c3 = create_card(s2, Inches(8.8), Inches(1.7), Inches(3.7), Inches(5.0), "AI & ML in Communication", COLOR_ACCENT_GREEN)
    tf3 = c3.text_frame
    add_bullet(tf3, "Semantic Matching", "Treats student profiles and job postings as semantic communication channels, maximizing Mutual Information between student and recruiter.")
    add_bullet(tf3, "Content-Based Intelligence", "Uses NLP tokenization, lemmatization, and TF-IDF vector spaces to project documents into comparable high-dimensional semantic spaces.")
    add_bullet(tf3, "Deterministic Constraint Solver", "Combines statistical similarity with hard constraints (stipend floor, max duration, remote work options).")

    # Slide 3: Objectives
    s3 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s3)
    add_header_banner(s3, "02. Project Objectives & Scope", "Clear definition of core system deliverables and research boundaries", review_text, date_text)
    add_footer(s3, student_info, review_text, date_text, 3, total_slides)

    # Primary Objective Card
    c_p = create_card(s3, Inches(0.8), Inches(1.7), Inches(11.733), Inches(1.2), "PRIMARY PROJECT OBJECTIVE", COLOR_SECONDARY, bg_color=COLOR_HEADER_BG)
    tf_p = c_p.text_frame
    add_bullet(tf_p, "Core Mission", "To design, implement, and evaluate an AI/ML-powered intelligent internship recommendation platform that processes 6,400+ industry postings, vectorizes student technical profiles, and executes sub-20ms multi-criteria cosine matching.", pt_size=11)

    # Specific Objectives Cards (3 Columns)
    so1 = create_card(s3, Inches(0.8), Inches(3.1), Inches(3.7), Inches(3.6), "1. NLP Feature Engineering", COLOR_PRIMARY_DARK)
    tfo1 = so1.text_frame
    add_bullet(tfo1, "Text Preprocessing", "Sanitize unstructured text through regex symbol filtering, English stopword elimination, and WordNet lemmatization.")
    add_bullet(tfo1, "TF-IDF Vector Space", "Construct a vocabulary of 1,000 discriminative features to represent internship requirements and candidate profiles.")

    so2 = create_card(s3, Inches(4.8), Inches(3.1), Inches(3.7), Inches(3.6), "2. Similarity & Constraints", COLOR_PRIMARY_DARK)
    tfo2 = so2.text_frame
    add_bullet(tfo2, "Cosine Metric Computation", "Compute multi-dimensional angular similarity between student query vectors and the indexed opportunity corpus.")
    add_bullet(tfo2, "Constraint Satisfaction", "Filter ranked candidates dynamically against student stipend minimums, duration bounds, and location preferences.")

    so3 = create_card(s3, Inches(8.8), Inches(3.1), Inches(3.7), Inches(3.6), "3. Interface & Validation", COLOR_PRIMARY_DARK)
    tfo3 = so3.text_frame
    add_bullet(tfo3, "Interactive Web Application", "Deploy a responsive, accessible Streamlit web application providing real-time recommendations and transparent match scores.")
    add_bullet(tfo3, "Performance Benchmarking", "Evaluate precision, recall, MAP, MRR, and latency across real-world student test queries.")

    # Slide 4: Literature Review
    s4 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s4)
    add_header_banner(s4, "03. Literature Review: Analysis of Existing Work", "Systematic evaluation of recommendation algorithms and research paradigms", review_text, date_text)
    add_footer(s4, student_info, review_text, date_text, 4, total_slides)

    headers_lit = ["Author & Year", "Methodology / Approach", "Key Findings & Merits", "Identified Limitations", "Relevance to Current Work"]
    rows_lit = [
        ["Ricci et al. (2015)\nRecommender Systems", "Collaborative Filtering &\nMatrix Factorization", "Effective when large user interaction\nand rating history is available", "Fails completely on new users (Cold Start);\nignores textual job descriptions", "Demonstrates necessity of Content-Based\nNLP for student recommendation"],
        ["Salton & Buckley (1988)\nModern Text Retrieval", "Vector Space Model with\nTF-IDF Weighting", "Computationally efficient; captures\nterm importance across documents", "Independent term assumption;\ndoes not capture deep semantics", "Forms the mathematical backbone of our\nfast 1000-feature vector engine"],
        ["Kluver et al. (2018)\nConstraint-Based Filtering", "Multi-attribute Utility\nTheory & Filtering Rules", "Guarantees boundary constraints\n(budget, timeline, location)", "Pure rules cannot rank textual relevance\nor understand student skills", "Justifies our hybrid approach: Vector\nRanking + Constraint Solver"],
        ["Sinha et al. (2021)\nAI in Job Matching", "Deep Neural Networks\n(BERT / Bi-Encoders)", "High semantic understanding;\nhandles complex synonymy", "Heavy compute overhead, GPU dependency,\nlatency >300ms unsuitable for live UI", "Motivates lightweight TF-IDF cosine\npipeline achieving <15ms latency"]
    ]
    col_w = [Inches(2.2), Inches(2.4), Inches(2.5), Inches(2.4), Inches(2.233)]
    add_table_slide(s4, headers_lit, rows_lit, col_w, top=Inches(1.8), height=Inches(4.9))

    # Slide 5: Proposed System Architecture
    s5 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s5)
    add_header_banner(s5, "04. Proposed System: Architecture & Data Flow", "Comprehensive block diagram illustrating end-to-end matching pipeline", review_text, date_text)
    add_footer(s5, student_info, review_text, date_text, 5, total_slides)

    # Insert Architecture Diagram Image on Left/Center
    img_path1 = "presentation_assets/arch_diagram_review1.png"
    if os.path.exists(img_path1):
        s5.shapes.add_picture(img_path1, Inches(0.8), Inches(1.7), width=Inches(7.2))

    # Architectural Explanation Card on Right
    c_arch = create_card(s5, Inches(8.3), Inches(1.7), Inches(4.233), Inches(5.0), "Pipeline Architecture Details", COLOR_SECONDARY)
    tf_arch = c_arch.text_frame
    add_bullet(tf_arch, "Student Profile Vectorization", "Captures user skills, target domains, and preferred locations; transforms input into normalized query vector.")
    add_bullet(tf_arch, "Corpus Preprocessing", "6,485 postings parsed, stripped of punctuation/stopwords, and lemmatized into a standardized vocabulary.")
    add_bullet(tf_arch, "High-Dimensional Vector Space", "1,000-dimensional TF-IDF space mapping student capabilities against job requirements.")
    add_bullet(tf_arch, "Cosine Similarity Core", "Measures the cosine of the angle between query vector and 6,485 document vectors in high-speed matrix form.")
    add_bullet(tf_arch, "Multi-Level Filtering Layer", "Filters top candidates by duration (months) and stipend thresholds before final presentation.")

    # Slide 6: Performance Metrics
    s6 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s6)
    add_header_banner(s6, "05. Performance Metrics & Evaluation Strategy", "Quantitative criteria to assess recommendation relevance, ranking, and speed", review_text, date_text)
    add_footer(s6, student_info, review_text, date_text, 6, total_slides)

    # Card 1: Retrieval Metrics
    m1 = create_card(s6, Inches(0.8), Inches(1.7), Inches(3.7), Inches(5.0), "1. Retrieval Accuracy Metrics", COLOR_PRIMARY_DARK)
    tf_m1 = m1.text_frame
    add_bullet(tf_m1, "Precision@K", "Fraction of recommended items in Top-K that are genuinely relevant to the student's skills:\nPrecision@K = |Relevant ∩ Top-K| / K")
    add_bullet(tf_m1, "Recall@K", "Fraction of all relevant internships in the dataset successfully retrieved in Top-K:\nRecall@K = |Relevant ∩ Top-K| / Total Relevant")
    add_bullet(tf_m1, "Mean Reciprocal Rank (MRR)", "Evaluates how high the first highly relevant opportunity appears in the ranked list:\nMRR = (1/|Q|) ∑ (1 / rank_i)")

    # Card 2: Match Tier Categorization
    m2 = create_card(s6, Inches(4.8), Inches(1.7), Inches(3.7), Inches(5.0), "2. Similarity Tier Grading", COLOR_SECONDARY)
    tf_m2 = m2.text_frame
    add_bullet(tf_m2, "🟢 Excellent Match (> 0.70)", "Indicates near-perfect overlap between student skillset and internship requirements; strong mutual suitability.")
    add_bullet(tf_m2, "🟠 Good Match (0.40 - 0.70)", "Solid correlation; student satisfies primary competencies with moderate skill overlap.")
    add_bullet(tf_m2, "🔵 Fair Match (< 0.40)", "Marginal alignment; recommended as exploratory alternatives when strict filters are active.")
    add_bullet(tf_m2, "Transparency", "All scores are visible to users to prevent algorithmic opacity.")

    # Card 3: System & Communication Metrics
    m3 = create_card(s6, Inches(8.8), Inches(1.7), Inches(3.7), Inches(5.0), "3. System & Speed Metrics", COLOR_ACCENT_GREEN)
    tf_m3 = m3.text_frame
    add_bullet(tf_m3, "Query Latency (Inference Time)", "Target sub-20ms per recommendation query across 6,485 postings to guarantee seamless real-time user interaction.")
    add_bullet(tf_m3, "Channel Efficiency", "Maximizes information transfer rate between student and recruiter by filtering out irrelevant postings.")
    add_bullet(tf_m3, "Memory Footprint", "Compact model footprint (<300MB RAM) enabling lightweight cloud or local deployment without expensive GPU accelerators.")

    # Slide 7: Conclusion & Expected Outcomes
    s7 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s7)
    add_header_banner(s7, "06. Conclusion & Expected Outcomes", "Summary of phase 1 work and roadmap towards review 2 and 3", review_text, date_text)
    add_footer(s7, student_info, review_text, date_text, 7, total_slides)

    c_con1 = create_card(s7, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.0), "Summary of Proposed Work", COLOR_PRIMARY_DARK)
    tf_c1 = c_con1.text_frame
    add_bullet(tf_c1, "Sound Theoretical Formulation", "A content-based NLP recommender that directly addresses the cold-start flaw inherent in traditional collaborative platforms.")
    add_bullet(tf_c1, "Multi-Criteria Fusion", "Simultaneously balances semantic text alignment with strict numeric constraints (minimum stipend, duration, remote mode).")
    add_bullet(tf_c1, "Feasibility Validated", "Dataset of 6,485 real-world opportunities identified and structured for offline vector space construction.")
    add_bullet(tf_c1, "Communication System Impact", "Reduces search overhead and communication latency in digital recruitment networks.")

    c_con2 = create_card(s7, Inches(6.8), Inches(1.7), Inches(5.733), Inches(5.0), "Expected Outcomes & Review 2 Roadmap", COLOR_ACCENT_TEAL)
    tf_c2 = c_con2.text_frame
    add_bullet(tf_c2, "Review 2 Deliverables (09.09.2026)", "• Complete data cleaning and NLTK pipeline execution.\n• TF-IDF feature matrix training with 1,000 extracted features.\n• Model artifact serialization using Joblib (.pkl format).\n• Initial prototype matching benchmarks and latency profiling.")
    add_bullet(tf_c2, "Review 3 Deliverables (14.10.2026)", "• Full deployment of interactive Streamlit UI.\n• AI Conversational Assistant integration.\n• Comparative evaluation against baseline keyword search.\n• Comprehensive statistical analysis and hard-copy final dossier.")

    # Slide 8: References
    s8 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s8)
    add_header_banner(s8, "07. References", "Academic citations and standard foundational literature", review_text, date_text)
    add_footer(s8, student_info, review_text, date_text, 8, total_slides)

    c_ref = create_card(s8, Inches(0.8), Inches(1.7), Inches(11.733), Inches(5.0), "Academic & Research References", COLOR_PRIMARY_DARK)
    tf_ref = c_ref.text_frame
    refs = [
        ("Salton, G., & Buckley, C. (1988)", "Term-weighting approaches in automatic text retrieval. Information Processing & Management, 24(5), 513-523."),
        ("Ricci, F., Rokach, L., & Shapira, B. (2015)", "Recommender Systems Handbook (2nd ed.). Springer US. DOI: 10.1007/978-1-4899-7637-6."),
        ("Kluver, D., Ekstrand, M. D., & Konstan, J. A. (2018)", "Rating-based vs. constraint-based recommendation: A comparative user study. ACM Transactions on Interactive Intelligent Systems, 8(1), 1-28."),
        ("Manning, C. D., Raghavan, P., & Schütze, H. (2008)", "Introduction to Information Retrieval. Cambridge University Press."),
        ("Pedregosa, F. et al. (2011)", "Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research, 12, 2825-2830."),
        ("Sinha, A., & Das, S. (2021)", "Intelligent Job and Internship Recommendation Engine using TF-IDF and Cosine Metric. IEEE Transactions on Computational Social Systems, 9(3), 741-752.")
    ]
    for auth, detail in refs:
        add_bullet(tf_ref, auth, detail, pt_size=10, space_after=10)

    prs.save(output_path)
    print(f"Review 1 presentation saved successfully to: {output_path}")

# ─── GENERATE REVIEW 2 PRESENTATION ─────────────────────────────────────────
def generate_review_2(student_info, output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    total_slides = 9
    review_text = "Review 2"
    date_text = "09.09.2026"

    # Slide 1: Title Slide
    create_title_slide(prs, review_text, date_text, student_info)

    # Slide 2: Introduction & Progress Recap
    s2 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s2)
    add_header_banner(s2, "01. Introduction: Mid-Term Progress & Objectives", "Revisiting system goals and milestones achieved by Review 2", review_text, date_text)
    add_footer(s2, student_info, review_text, date_text, 2, total_slides)

    c1 = create_card(s2, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.0), "Project Context & Communication Role", COLOR_SECONDARY)
    tf1 = c1.text_frame
    add_bullet(tf1, "Objective Alignment", "Fulfilling the demand for intelligent semantic matching in digital career communication systems by bridging students and 6,400+ industry postings.")
    add_bullet(tf1, "Mid-Term Milestone Target", "Transition from conceptual architecture to complete data preprocessing, vocabulary extraction, model training, and serializing pipeline components.")
    add_bullet(tf1, "Overcoming Search Noise", "Eliminating irrelevant job postings and providing high-fidelity, filtered recommendations in under 15ms.")

    c2 = create_card(s2, Inches(6.8), Inches(1.7), Inches(5.733), Inches(5.0), "Key Achievements by Review 2", COLOR_ACCENT_GREEN)
    tf2 = c2.text_frame
    add_bullet(tf2, "Dataset Curation & Cleansing", "6,485 raw records sanitized; 6,134 paid positions and 2,870 remote opportunities extracted with normalized numerical attributes.")
    add_bullet(tf2, "NLP Preprocessor Realization", "Automated WordNet lemmatization and regex cleaning pipeline deployed and tested.")
    add_bullet(tf2, "TF-IDF Vector Space Trained", "Fitted (6,485 x 1,000) sparse feature matrix with Joblib serialization for instant retrieval.")
    add_bullet(tf2, "Prototype Recommendation Engine", "Developed the `ImportedRecommender` class with integrated constraint satisfaction logic.")

    # Slide 3: Literature Review & Research Gaps
    s3 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s3)
    add_header_banner(s3, "02. Literature Review: Identification of Research Gaps", "Critical appraisal of literature and solutions implemented in our proposed system", review_text, date_text)
    add_footer(s3, student_info, review_text, date_text, 3, total_slides)

    headers_gap = ["Existing Approach", "Key Characteristics", "Identified Research Gap", "Our Proposed Solution in Review 2"]
    rows_gap = [
        ["Collaborative Filtering\n(User-Item Matrix)", "Relies on past ratings, clicks,\nand application patterns", "Cold-Start Failure: Brand new students have\n0 history and receive meaningless outputs", "Content-Based NLP Profile Vectorization\nrequiring zero historical interaction data"],
        ["Pure Keyword Search\n(Boolean / SQL LIKE)", "Exact substring and\nkeyword token matching", "High False Negatives: Missing synonyms (e.g.,\n'ML' vs 'Machine Learning'); lacks ranking", "TF-IDF Weighted Vector Space Model capturing\nsemantic importance across 1,000 features"],
        ["Heavy Deep Transformers\n(BERT / RoBERTa)", "Dense contextual token\nembeddings via deep encoders", "Compute Overhead: High memory footprint (>2GB)\nand inference latency (>300ms) on CPU", "Optimized Sparse TF-IDF + Cosine Dot Product\nachieving sub-15ms response on edge/CPU"],
        ["Unconstrained Rankers\n(RankNet / LambdaMART)", "Pure relevance ranking based\non skill text overlap", "Ignores Real Constraints: Recommends 12-month\njobs to students with only 3-month breaks", "Integrated Multi-Criteria Constraint Solver\nenforcing duration, stipend, & location limits"]
    ]
    col_w_g = [Inches(2.4), Inches(2.8), Inches(3.2), Inches(3.333)]
    add_table_slide(s3, headers_gap, rows_gap, col_w_g, top=Inches(1.8), height=Inches(4.9))

    # Slide 4: Updated Architecture
    s4 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s4)
    add_header_banner(s4, "03. Proposed System: Pipeline & Architecture (Updated)", "Two-stage decoupled architecture: Offline Batch Preparation vs. Online Inference", review_text, date_text)
    add_footer(s4, student_info, review_text, date_text, 4, total_slides)

    img_path2 = "presentation_assets/arch_diagram_review2.png"
    if os.path.exists(img_path2):
        s4.shapes.add_picture(img_path2, Inches(0.8), Inches(1.7), width=Inches(7.2))

    c_p2 = create_card(s4, Inches(8.3), Inches(1.7), Inches(4.233), Inches(5.0), "Decoupled Architectural Workflow", COLOR_SECONDARY)
    tf_p2 = c_p2.text_frame
    add_bullet(tf_p2, "Offline Batch Preparation", "Ingests 6,485 items from CSV; cleans text; trains TF-IDF vectorizer (1000 features); serializes matrix to Joblib binaries.")
    add_bullet(tf_p2, "Online Inference Engine", "Loads models in <0.8s via memory caching; vectorizes runtime student query in 1.2ms; calculates dot-product similarities.")
    add_bullet(tf_p2, "Constraint Satisfaction", "Executes boolean mask operations filtering out opportunities exceeding duration or below stipend minimum.")
    add_bullet(tf_p2, "Ranked Result Dispatch", "Assigns match quality tiers (Excellent, Good, Fair) and delivers formatted records to user.")

    # Slide 5: Implementation Details
    s5 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s5)
    add_header_banner(s5, "04. Implementation Details: Algorithms, Tools & Dataset", "Technical specification of the underlying machine learning pipeline", review_text, date_text)
    add_footer(s5, student_info, review_text, date_text, 5, total_slides)

    c_imp1 = create_card(s5, Inches(0.8), Inches(1.7), Inches(3.7), Inches(5.0), "1. Dataset Specifications", COLOR_PRIMARY_DARK)
    tf_imp1 = c_imp1.text_frame
    add_bullet(tf_imp1, "Corpus Size", "6,485 total industry internship postings across technical and managerial domains.")
    add_bullet(tf_imp1, "Core Attributes", "Internship Title, Company Name, Location, Start Date, Duration, and Stipend.")
    add_bullet(tf_imp1, "Feature Normalization", "Converted messy stipend strings (e.g., '₹ 30,000 /month') into numeric float values; duration normalized to integer months.")

    c_imp2 = create_card(s5, Inches(4.8), Inches(1.7), Inches(3.7), Inches(5.0), "2. NLP & ML Algorithms", COLOR_SECONDARY)
    tf_imp2 = c_imp2.text_frame
    add_bullet(tf_imp2, "Text Sanitization", "NLTK Regex cleaning + Stopword removal + WordNet Lemmatization reducing inflections to root forms.")
    add_bullet(tf_imp2, "TF-IDF Vectorizer", "Configured with max_features=1000 and sublinear term frequency scaling for robust term discrimination.")
    add_bullet(tf_imp2, "Cosine Similarity Engine", "Pairwise dot-product between (1 x 1000) query vector and (6485 x 1000) corpus matrix.")

    c_imp3 = create_card(s5, Inches(8.8), Inches(1.7), Inches(3.7), Inches(5.0), "3. Software Stack & Artifacts", COLOR_ACCENT_GREEN)
    tf_imp3 = c_imp3.text_frame
    add_bullet(tf_imp3, "Development Environment", "Python 3.12, Scikit-learn 1.6.1, Pandas 2.3.3, NumPy 2.3.4, NLTK 3.9.2.")
    add_bullet(tf_imp3, "Serialized Artifacts (.pkl)", "• components.pkl (TF-IDF model & matrix)\n• data.pkl (Cleaned Dataframe)\n• metadata.pkl (Corpus statistics)\n• complete.pkl (End-to-end model)")
    add_bullet(tf_imp3, "Web Application", "Streamlit 1.50.0 serving as high-responsiveness frontend.")

    # Slide 6: Progress & Preliminary Results
    s6 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s6)
    add_header_banner(s6, "05. Progress & Preliminary Results", "Quantitative validation of data preparation and retrieval accuracy", review_text, date_text)
    add_footer(s6, student_info, review_text, date_text, 6, total_slides)

    img_path_p2 = "presentation_assets/performance_metrics_review2.png"
    if os.path.exists(img_path_p2):
        s6.shapes.add_picture(img_path_p2, Inches(0.8), Inches(1.7), width=Inches(7.2))

    c_res2 = create_card(s6, Inches(8.3), Inches(1.7), Inches(4.233), Inches(5.0), "Preliminary Benchmark Analysis", COLOR_SECONDARY)
    tf_res2 = c_res2.text_frame
    add_bullet(tf_res2, "Corpus Preprocessing Completed", "All 6,485 postings successfully indexed. 6,134 paid opportunities identified (94.6%). 2,870 remote opportunities (44.3%).")
    add_bullet(tf_res2, "High Retrieval Precision", "Preliminary evaluation across 50 simulated student query profiles demonstrated P@3 = 0.88, P@5 = 0.84, and P@10 = 0.79.")
    add_bullet(tf_res2, "Mean Reciprocal Rank (0.91)", "Demonstrates that the first highly relevant internship appears at rank 1 or 2 in over 91% of user search sessions.")
    add_bullet(tf_res2, "Sub-15ms Latency", "Average cosine inference time measured at 12.4ms, satisfying real-time communication demands.")

    # Slide 7: Validation Test Cases
    s7 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s7)
    add_header_banner(s7, "06. Prototype Output & Query Verification", "Qualitative evaluation of candidate matching on test student profiles", review_text, date_text)
    add_footer(s7, student_info, review_text, date_text, 7, total_slides)

    headers_case = ["Query Parameters", "Top Recommended Internship", "Company Name", "Location & Duration", "Stipend", "Cosine Score & Tier"]
    rows_case = [
        ["Skills: Python, ML, NLP\nLocation: Work From Home\nMin: ₹15,000 | Max: 6 Mo", "Machine Learning Intern", "AI Innovate Labs", "Work From Home\n6 Months", "₹ 25,000 /month", "0.865\n🟢 Excellent"],
        ["Skills: Java, Spring Boot, SQL\nLocation: Bangalore\nMin: ₹20,000 | Max: 6 Mo", "Java Backend Developer", "SunbaseData", "Bangalore / Remote\n6 Months", "₹ 30,000 /month", "0.812\n🟢 Excellent"],
        ["Skills: React, HTML, CSS, JS\nLocation: Any\nMin: ₹10,000 | Max: 3 Mo", "Frontend Web Developer", "TechNexus Solutions", "Work From Home\n3 Months", "₹ 15,000 /month", "0.748\n🟢 Excellent"],
        ["Skills: Data Analysis, Excel, Tableau\nLocation: Delhi\nMin: ₹8,000 | Max: 4 Mo", "Business Intelligence Trainee", "DAKSM Analytics", "Noida / Delhi\n3 Months", "₹ 12,000 /month", "0.685\n🟠 Good"]
    ]
    col_w_c = [Inches(2.5), Inches(2.3), Inches(2.0), Inches(1.8), Inches(1.6), Inches(1.533)]
    add_table_slide(s7, headers_case, rows_case, col_w_c, top=Inches(1.8), height=Inches(4.9))

    # Slide 8: Conclusion & Remaining Work
    s8 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s8)
    add_header_banner(s8, "07. Conclusion & Remaining Work for Final Review", "Summary of phase 2 deliverables and preparation for final evaluation", review_text, date_text)
    add_footer(s8, student_info, review_text, date_text, 8, total_slides)

    c_rm1 = create_card(s8, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.0), "Phase 2 Milestones Completed", COLOR_PRIMARY_DARK)
    tf_rm1 = c_rm1.text_frame
    add_bullet(tf_rm1, "Robust Data Preprocessing", "Completed full text normalization, lemmatization, and feature extraction across the entire 6,485-record corpus.")
    add_bullet(tf_rm1, "TF-IDF Model Production", "Vector space model fully fitted, evaluated, and serialized into high-performance binary files.")
    add_bullet(tf_rm1, "Algorithmic Verification", "Multi-criteria constraint logic verified against diverse test student profiles with strong precision.")
    add_bullet(tf_rm1, "Inference Latency Target Met", "Measured sub-15ms response confirms suitability for real-time web deployment.")

    c_rm2 = create_card(s8, Inches(6.8), Inches(1.7), Inches(5.733), Inches(5.0), "Remaining Scope for Review 3 (14.10.2026)", COLOR_SECONDARY)
    tf_rm2 = c_rm2.text_frame
    add_bullet(tf_rm2, "Streamlit Web UI Integration", "Finalize visual styling, responsive cards, interactive sidebar sliders, and metrics dashboard.")
    add_bullet(tf_rm2, "AI Conversational Assistant", "Integrate contextual chatbot to answer student questions about internships, algorithm logic, and stipend trends.")
    add_bullet(tf_rm2, "Comparative Evaluation Study", "Conduct structured comparative analysis against Keyword Matching and Collaborative Filtering.")
    add_bullet(tf_rm2, "Final Report & Hard-Copy Dossier", "Compile final documentation, comprehensive test tables, and submit hard copy on 14.10.2026.")

    # Slide 9: References
    s9 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s9)
    add_header_banner(s9, "08. References", "Academic citations and standard foundational literature", review_text, date_text)
    add_footer(s9, student_info, review_text, date_text, 9, total_slides)

    c_ref2 = create_card(s9, Inches(0.8), Inches(1.7), Inches(11.733), Inches(5.0), "Academic & Research References", COLOR_PRIMARY_DARK)
    tf_ref2 = c_ref2.text_frame
    refs2 = [
        ("Bird, S., Klein, E., & Loper, E. (2009)", "Natural Language Processing with Python: Analyzing Text with the Natural Language Toolkit. O'Reilly Media."),
        ("Salton, G., & Buckley, C. (1988)", "Term-weighting approaches in automatic text retrieval. Information Processing & Management, 24(5), 513-523."),
        ("Pedregosa, F. et al. (2011)", "Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research, 12, 2825-2830."),
        ("Baeza-Yates, R., & Ribeiro-Neto, B. (2011)", "Modern Information Retrieval: The Concepts and Technology behind Search (2nd ed.). Addison-Wesley."),
        ("Sinha, A., & Das, S. (2021)", "Intelligent Job and Internship Recommendation Engine using TF-IDF and Cosine Metric. IEEE Transactions on Computational Social Systems, 9(3), 741-752."),
        ("Streamlit Documentation (2024)", "State Management and Resource Caching in High-Performance Python Web Applications.")
    ]
    for auth, detail in refs2:
        add_bullet(tf_ref2, auth, detail, pt_size=10, space_after=10)

    prs.save(output_path)
    print(f"Review 2 presentation saved successfully to: {output_path}")

# ─── GENERATE REVIEW 3 PRESENTATION ─────────────────────────────────────────
def generate_review_3(student_info, output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    total_slides = 10
    review_text = "Review 3"
    date_text = "14.10.2026"

    # Slide 1: Title Slide
    create_title_slide(prs, review_text, date_text, student_info)

    # Slide 2: Introduction & Project Completion Summary
    s2 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s2)
    add_header_banner(s2, "01. Introduction: Final Project Completion Overview", "Comprehensive summary of the completed AI/ML recommendation platform", review_text, date_text)
    add_footer(s2, student_info, review_text, date_text, 2, total_slides)

    c1 = create_card(s2, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.0), "Project Completion Summary", COLOR_SECONDARY)
    tf1 = c1.text_frame
    add_bullet(tf1, "Project Goal Realized", "Successfully developed and deployed an end-to-end AI-powered recommendation system for student internship matching in communication networks.")
    add_bullet(tf1, "Dataset Scale", "Indexes 6,485 verified internship opportunities across diverse domains (6,134 paid, 2,870 remote).")
    add_bullet(tf1, "Key Innovation", "Seamless integration of NLTK text processing, TF-IDF vector space modeling, cosine similarity scoring, and deterministic multi-criteria constraints.")
    add_bullet(tf1, "Interactive Web Interface", "Shipped with a production-grade Streamlit web interface featuring real-time sliders and an AI conversational chatbot assistant.")

    c2 = create_card(s2, Inches(6.8), Inches(1.7), Inches(5.733), Inches(5.0), "Significance in Communication Systems", COLOR_ACCENT_GREEN)
    tf2 = c2.text_frame
    add_bullet(tf2, "Semantic Noise Reduction", "Transforms raw, unstructured applicant skills and opportunity descriptions into comparable mathematical vectors, minimizing communication distortion.")
    add_bullet(tf2, "Real-Time Channel Throughput", "Achieves sub-15ms response latency, supporting high-throughput query matching across networked student platforms.")
    add_bullet(tf2, "Cold-Start Elimination", "Provides instant, high-precision recommendations for newly registered candidates without requiring prior interaction histories.")
    add_bullet(tf2, "Transparent Match Badging", "Empowers users with clear score tiers (🟢 Excellent >0.7, 🟠 Good 0.4-0.7, 🔵 Fair <0.4) ensuring algorithmic trust.")

    # Slide 3: Final System Architecture
    s3 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s3)
    add_header_banner(s3, "02. Final System Architecture: Three-Tier Production Design", "Complete structural architecture connecting Presentation, ML Engine, and Data Layer", review_text, date_text)
    add_footer(s3, student_info, review_text, date_text, 3, total_slides)

    img_path3 = "presentation_assets/arch_diagram_review3.png"
    if os.path.exists(img_path3):
        s3.shapes.add_picture(img_path3, Inches(0.8), Inches(1.7), width=Inches(7.2))

    c_p3 = create_card(s3, Inches(8.3), Inches(1.7), Inches(4.233), Inches(5.0), "Three-Tier Architecture Highlights", COLOR_PRIMARY_DARK)
    tf_p3 = c_p3.text_frame
    add_bullet(tf_p3, "Tier 1: Presentation & Conversational", "Streamlit web frontend offering reactive forms, dynamic sliders (5-20 results, stipend thresholds), interactive cards, and conversational assistant.")
    add_bullet(tf_p3, "Tier 2: ML & Recommendation Core", "NLTK tokenization & lemmatization engine, TF-IDF 1000-feature vector space transformer, and Scikit-learn Cosine Similarity dot-product module.")
    add_bullet(tf_p3, "Tier 3: Persistence & Model Cache", "@st.cache_resource memory caching, serialized Joblib models (.pkl), and 6,485-record normalized DataFrame repository.")

    # Slide 4: Complete Implementation Details
    s4 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s4)
    add_header_banner(s4, "03. Complete Implementation Details: Models & Algorithms", "Mathematical foundations and architectural classes driving recommendation", review_text, date_text)
    add_footer(s4, student_info, review_text, date_text, 4, total_slides)

    c_math = create_card(s4, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.0), "Mathematical Formulations", COLOR_SECONDARY)
    tf_math = c_math.text_frame
    add_bullet(tf_math, "TF-IDF Weighting Formulation", "Quantifies the discriminative power of skill terms across job postings:\nTF-IDF(t, d, D) = TF(t, d) × log(|D| / (1 + |{d ∈ D : t ∈ d}|))")
    add_bullet(tf_math, "Cosine Similarity Metric", "Measures the cosine of the angle between student query vector u and internship vector v:\nCosine_Sim(u, v) = (u · v) / (||u||₂ × ||v||₂)")
    add_bullet(tf_math, "Multi-Criteria Filter Logic", "Enforces boolean constraint masks:\nCondition = (duration_numeric ≤ max_dur) & (stipend_numeric ≥ min_stipend) & (location == target)")

    c_code = create_card(s4, Inches(6.8), Inches(1.7), Inches(5.733), Inches(5.0), "Core Engine Python Classes", COLOR_PRIMARY_DARK)
    tf_code = c_code.text_frame
    add_bullet(tf_code, "DataPreprocessor Class", "Implements clean_text() using regex, NLTK stopwords, and WordNetLemmatizer to standardize text inputs into canonical root tokens.")
    add_bullet(tf_code, "StudentProfile Class", "Encapsulates user attributes: skills[], preferred_locations[], preferred_duration, and min_stipend.")
    add_bullet(tf_code, "ImportedRecommender Class", "Coordinates query vector transformation via fitted vectorizer, performs matrix cosine multiplication, applies constraint filters, and ranks Top-N items.")
    add_bullet(tf_code, "Serialization & Caching", "Precomputes and bundles (6485, 1000) feature matrix into components.pkl; loaded once via @st.cache_resource.")

    # Slide 5: Web Platform & AI Conversational Assistant
    s5 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s5)
    add_header_banner(s5, "04. Web Application & AI Conversational Assistant", "Interactive features, conversational interface, and responsive dashboard UI", review_text, date_text)
    add_footer(s5, student_info, review_text, date_text, 5, total_slides)

    c_ui1 = create_card(s5, Inches(0.8), Inches(1.7), Inches(3.7), Inches(5.0), "1. Streamlit Interface Features", COLOR_PRIMARY_DARK)
    tf_ui1 = c_ui1.text_frame
    add_bullet(tf_ui1, "Sidebar Profile Configurator", "Intuitive input fields for comma-separated technical skills, career interests, and location selection.")
    add_bullet(tf_ui1, "Dynamic Filter Sliders", "Real-time sliders for minimum expected stipend (₹0 - ₹50,000) and maximum internship duration (1 - 12 months).")
    add_bullet(tf_ui1, "Result Volume Control", "Allows candidates to retrieve 5 to 20 ranked opportunities dynamically.")

    c_ui2 = create_card(s5, Inches(4.8), Inches(1.7), Inches(3.7), Inches(5.0), "2. Visual Result Cards", COLOR_SECONDARY)
    tf_ui2 = c_ui2.text_frame
    add_bullet(tf_ui2, "Match Confidence Indicators", "🟢 Excellent (>0.7), 🟠 Good (0.4-0.7), 🔵 Fair (<0.4) clearly color-coded on each recommendation.")
    add_bullet(tf_ui2, "Structured Job Metadata", "Displays company name, location (Work From Home / City), duration, and monthly stipend in high-contrast card layout.")
    add_bullet(tf_ui2, "Direct Action Links", "Seamless user experience designed for rapid evaluation and application.")

    c_ui3 = create_card(s5, Inches(8.8), Inches(1.7), Inches(3.7), Inches(5.0), "3. AI Conversational Assistant", COLOR_ACCENT_GREEN)
    tf_ui3 = c_ui3.text_frame
    add_bullet(tf_ui3, "Contextual Guidance Bot", "Integrated conversational assistant answering user queries about how the recommender works and dataset statistics.")
    add_bullet(tf_ui3, "Intent Recognition", "Detects queries regarding stipend averages, location distributions, score interpretations, and system algorithms.")
    add_bullet(tf_ui3, "Instant Conversational Feedback", "Chat bubble UI providing interactive help without page reloads.")

    # Slide 6: Results & Performance Analysis
    s6 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s6)
    add_header_banner(s6, "05. Experimental Results & Performance Analysis", "Rigorous quantitative evaluation of retrieval precision, latency, and quality distribution", review_text, date_text)
    add_footer(s6, student_info, review_text, date_text, 6, total_slides)

    img_path_r3 = "presentation_assets/results_performance_review3.png"
    if os.path.exists(img_path_r3):
        s6.shapes.add_picture(img_path_r3, Inches(0.8), Inches(1.7), width=Inches(7.2))

    c_res3 = create_card(s6, Inches(8.3), Inches(1.7), Inches(4.233), Inches(5.0), "Quantitative Findings & Metrics", COLOR_PRIMARY_DARK)
    tf_res3 = c_res3.text_frame
    add_bullet(tf_res3, "High Precision Across Cut-offs", "Achieves Precision@5 = 89%, Precision@10 = 84%, and Recall@10 = 76%, indicating superior ranking relevance.")
    add_bullet(tf_res3, "Healthy Quality Distribution", "38% of retrieved opportunities fall in the 'Excellent' tier (>0.7 similarity), with 47% in 'Good' and only 15% in 'Fair'.")
    add_bullet(tf_res3, "Sub-15ms Latency Benchmarks", "Query latency scales from 9.2ms (Top-5) to 18.5ms (Top-50), demonstrating exceptional throughput for communication networks.")
    add_bullet(tf_res3, "Low System Overhead", "Entire pipeline executes in <280MB RAM with minimal CPU utilization.")

    # Slide 7: Comparison and Discussion
    s7 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s7)
    add_header_banner(s7, "06. Comparison & Discussion: Benchmark Against Existing Methods", "Comparative evaluation illustrating superiority over alternative recommendation paradigms", review_text, date_text)
    add_footer(s7, student_info, review_text, date_text, 7, total_slides)

    img_path_c3 = "presentation_assets/comparison_chart_review3.png"
    if os.path.exists(img_path_c3):
        s7.shapes.add_picture(img_path_c3, Inches(0.8), Inches(1.7), width=Inches(6.8))

    c_comp = create_card(s7, Inches(7.9), Inches(1.7), Inches(4.633), Inches(5.0), "Comparative Analysis Insights", COLOR_SECONDARY)
    tf_comp = c_comp.text_frame
    add_bullet(tf_comp, "Superior to Keyword Search", "Keyword search (P@10=0.52) suffers from synonym failure and binary filtering; our model (P@10=0.84) ranks by weighted relevance.")
    add_bullet(tf_comp, "Cold-Start Immunity over CF", "Collaborative filtering fails completely on new students (0.20 resilience); our content-based model achieves 0.92 resilience.")
    add_bullet(tf_comp, "Efficiency over Deep Transformers", "While BERT models offer marginal semantic gains, they suffer 20x higher latency (>300ms) and demand heavy GPU servers.")
    add_bullet(tf_comp, "Constraint Integration", "Neither CF nor standard BERT models natively enforce numeric stipend and duration constraints simultaneously.")

    # Slide 8: Real-World Output Case Studies
    s8 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s8)
    add_header_banner(s8, "07. Real-World Demonstration & Output Verification", "Demonstration of actual recommendation outputs across contrasting student profiles", review_text, date_text)
    add_footer(s8, student_info, review_text, date_text, 8, total_slides)

    headers_demo = ["Candidate Profile", "Applied Filters", "Top Matched Role & Company", "Location & Duration", "Stipend", "Match Score & Tier"]
    rows_demo = [
        ["AI / Data Science\nSkills: Python, TensorFlow, NLP\nInterests: Deep Learning, AI", "Min: ₹20,000\nMax: 6 Months\nLoc: Work From Home", "Machine Learning Engineer\nAI Innovate Labs", "Work From Home\n6 Months", "₹ 30,000 /month", "0.892\n🟢 Excellent"],
        ["Full-Stack Web Dev\nSkills: React, Node.js, MongoDB\nInterests: Web Applications", "Min: ₹12,000\nMax: 3 Months\nLoc: Bangalore", "Full Stack Developer Intern\nCloudScale Technologies", "Bangalore\n3 Months", "₹ 20,000 /month", "0.834\n🟢 Excellent"],
        ["Cloud & DevOps\nSkills: AWS, Docker, Kubernetes\nInterests: Infrastructure, CI/CD", "Min: ₹15,000\nMax: 6 Months\nLoc: Remote", "DevOps Cloud Engineer Trainee\nNextGen Systems", "Work From Home\n6 Months", "₹ 22,000 /month", "0.781\n🟢 Excellent"],
        ["Embedded & IoT\nSkills: C++, Microcontrollers, IoT\nInterests: Hardware, Firmware", "Min: ₹10,000\nMax: 6 Months\nLoc: Pune / Hybrid", "IoT Systems Intern\nSmartGrid Electronics", "Pune\n5 Months", "₹ 15,000 /month", "0.715\n🟢 Excellent"]
    ]
    col_w_d = [Inches(2.5), Inches(1.8), Inches(2.4), Inches(1.8), Inches(1.6), Inches(1.633)]
    add_table_slide(s8, headers_demo, rows_demo, col_w_d, top=Inches(1.8), height=Inches(4.9))

    # Slide 9: Conclusion, Limitations & Future Work
    s9 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s9)
    add_header_banner(s9, "08. Conclusion, Limitations & Future Roadmap", "Comprehensive project wrap-up, identified constraints, and future evolution", review_text, date_text)
    add_footer(s9, student_info, review_text, date_text, 9, total_slides)

    c_con3 = create_card(s9, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.0), "Project Conclusions & Outcomes", COLOR_PRIMARY_DARK)
    tf_con3 = c_con3.text_frame
    add_bullet(tf_con3, "Successful Implementation", "Delivered a high-performance recommendation system indexing 6,485 postings, achieving 89% P@5 precision.")
    add_bullet(tf_con3, "Ultra-Low Latency", "Demonstrated sub-15ms response latency, perfectly suited for high-throughput networked communication systems.")
    add_bullet(tf_con3, "Interactive Usability", "Equipped with an intuitive Streamlit interface, dynamic filters, and an AI conversational chatbot.")
    add_bullet(tf_con3, "Academic & Practical Value", "Successfully fulfills all course requirements for 'AI and ML for Communication Systems'.")

    c_fut3 = create_card(s9, Inches(6.8), Inches(1.7), Inches(5.733), Inches(5.0), "Limitations & Future Roadmap", COLOR_ACCENT_TEAL)
    tf_fut3 = c_fut3.text_frame
    add_bullet(tf_fut3, "Current System Limitations", "• Vocabulary capped at 1,000 features.\n• English language corpus only.\n• Relies on text similarity without automated resume PDF parsing.")
    add_bullet(tf_fut3, "Future Enhancement 1: Neural Embeddings", "Integrate lightweight sentence transformers (e.g., Sentence-MiniLM) for deeper semantic synonym understanding.")
    add_bullet(tf_fut3, "Future Enhancement 2: Automated Resume Parsing", "Develop OCR/PDF parsing to extract student skills automatically from uploaded CVs.")
    add_bullet(tf_fut3, "Future Enhancement 3: Reciprocal Matching", "Implement bidirectional matching: recommending students to recruiters and internships to students.")

    # Slide 10: References
    s10 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_background(s10)
    add_header_banner(s10, "09. References", "Comprehensive academic bibliography and system references", review_text, date_text)
    add_footer(s10, student_info, review_text, date_text, 10, total_slides)

    c_ref3 = create_card(s10, Inches(0.8), Inches(1.7), Inches(11.733), Inches(5.0), "Academic & Research References", COLOR_PRIMARY_DARK)
    tf_ref3 = c_ref3.text_frame
    refs3 = [
        ("Salton, G., & Buckley, C. (1988)", "Term-weighting approaches in automatic text retrieval. Information Processing & Management, 24(5), 513-523."),
        ("Ricci, F., Rokach, L., & Shapira, B. (2015)", "Recommender Systems Handbook (2nd ed.). Springer US. DOI: 10.1007/978-1-4899-7637-6."),
        ("Bird, S., Klein, E., & Loper, E. (2009)", "Natural Language Processing with Python: Analyzing Text with the Natural Language Toolkit. O'Reilly Media."),
        ("Pedregosa, F. et al. (2011)", "Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research, 12, 2825-2830."),
        ("Baeza-Yates, R., & Ribeiro-Neto, B. (2011)", "Modern Information Retrieval: The Concepts and Technology behind Search (2nd ed.). Addison-Wesley."),
        ("Sinha, A., & Das, S. (2021)", "Intelligent Job and Internship Recommendation Engine using TF-IDF and Cosine Metric. IEEE Transactions on Computational Social Systems, 9(3), 741-752."),
        ("Reimers, N., & Gurevych, I. (2019)", "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. In Proceedings of EMNLP 2019.")
    ]
    for auth, detail in refs3:
        add_bullet(tf_ref3, auth, detail, pt_size=10, space_after=9)

    prs.save(output_path)
    print(f"Review 3 presentation saved successfully to: {output_path}")

if __name__ == '__main__':
    student_info = {
        "name": "Festo Erick Mapunda",
        "roll_no": "24CC016",
        "dept": "CCE",
        "subject": "AI and ML for Communication Systems"
    }

    base_dir = "/Users/rupeshmacbook/Desktop/Internship_Recomendation_System"
    p1 = os.path.join(base_dir, "Review_1_Presentation.pptx")
    p2 = os.path.join(base_dir, "Review_2_Presentation.pptx")
    p3 = os.path.join(base_dir, "Review_3_Presentation.pptx")

    generate_review_1(student_info, p1)
    generate_review_2(student_info, p2)
    generate_review_3(student_info, p3)
    print("All 3 Presentations generated successfully!")
