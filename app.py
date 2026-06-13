import streamlit as st
import time
import base64
from datetime import datetime
from gemini_utils import explain_topic, summarize_notes, generate_quiz, generate_study_plan

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="StudyMind – AI Study Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg:          #F5F2EC;
    --surface:     #FEFCF8;
    --surface2:    #EDE9E0;
    --border:      #D6D0C4;
    --accent:      #1A9E8F;
    --accent-dim:  #C8EAE6;
    --accent-dark: #127A6E;
    --ink:         #1C1F1E;
    --muted:       #6B7170;
    --amber:       #D4820A;
    --red:         #C0392B;
    --font-head:   'DM Serif Display', serif;
    --font-body:   'DM Sans', sans-serif;
    --radius:      10px;
    --shadow:      0 1px 4px rgba(28,31,30,0.08);
}

html, body, [class*="css"] {
    font-family: var(--font-body);
    background-color: var(--bg) !important;
    color: var(--ink) !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 4rem !important; max-width: 1080px; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #1A9E8F !important;
    border-right: none !important;
}
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown h5,
section[data-testid="stSidebar"] .stCaption,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div {
    color: rgba(255,255,255,0.85) !important;
}
section[data-testid="stSidebar"] h5,
section[data-testid="stSidebar"] strong {
    color: #fff !important;
}
section[data-testid="stSidebar"] .stSelectbox > div > div,
section[data-testid="stSidebar"] .stNumberInput > div > div {
    background: rgba(255,255,255,0.15) !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    color: #fff !important;
}
section[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.15) !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    color: #fff !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.25) !important;
}
section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.2) !important;
}

/* ── Page header ── */
.page-header {
    display: flex;
    align-items: baseline;
    gap: 14px;
    margin-bottom: 2rem;
    padding-bottom: 1.2rem;
    border-bottom: 2px solid var(--accent);
}
.page-header h1 {
    font-family: var(--font-head);
    font-size: 2.2rem;
    font-weight: 400;
    font-style: italic;
    margin: 0;
    color: var(--ink);
    letter-spacing: -0.02em;
}
.page-header .tagline {
    font-size: 0.82rem;
    color: var(--muted);
    font-weight: 400;
    margin-top: 2px;
}
.page-header .badge {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--accent-dark);
    background: var(--accent-dim);
    border: 1px solid rgba(26,158,143,0.25);
    padding: 3px 10px;
    border-radius: 20px;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 2px;
    background: var(--surface2) !important;
    border-radius: var(--radius);
    padding: 3px;
    border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--muted) !important;
    border-radius: 8px !important;
    padding: 7px 16px !important;
    font-family: var(--font-body);
    font-size: 0.84rem;
    font-weight: 500;
    border: none !important;
    transition: all 0.2s;
}
.stTabs [aria-selected="true"] {
    background: var(--accent) !important;
    color: #fff !important;
}

/* ── Inputs ── */
.stTextArea textarea, .stTextInput input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--ink) !important;
    font-family: var(--font-body) !important;
    font-size: 0.9rem !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(26,158,143,0.14) !important;
}
.stSelectbox > div > div,
.stNumberInput > div > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--ink) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: var(--font-body) !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.55rem 1.6rem !important;
    transition: background 0.18s, transform 0.1s !important;
    letter-spacing: 0.01em;
}
.stButton > button:hover {
    background: var(--accent-dark) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }
.stButton > button[kind="secondary"] {
    background: var(--surface) !important;
    color: var(--muted) !important;
    border: 1px solid var(--border) !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: var(--accent) !important;
    color: var(--ink) !important;
}

/* ── Output box ── */
.output-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: var(--radius);
    padding: 1.5rem 1.8rem;
    margin-top: 1.2rem;
    font-size: 0.91rem;
    line-height: 1.8;
    white-space: pre-wrap;
    word-break: break-word;
    color: var(--ink);
    box-shadow: var(--shadow);
}

/* ── Section label ── */
.section-label {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--muted);
    margin-bottom: 0.35rem;
}

/* ── Upload zone ── */
.upload-zone {
    background: var(--surface);
    border: 1.5px dashed var(--border);
    border-radius: var(--radius);
    padding: 1.1rem 1.4rem;
    text-align: center;
    font-size: 0.85rem;
    color: var(--muted);
    transition: border-color 0.2s;
}
.upload-zone:hover { border-color: var(--accent); }

/* ── Source toggle ── */
.source-toggle {
    display: flex;
    gap: 8px;
    margin-bottom: 0.9rem;
}

/* ── Stat cards ── */
.stat-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem 1.3rem;
    margin-bottom: 0.5rem;
    box-shadow: var(--shadow);
}
.stat-card .stat-number {
    font-family: var(--font-head);
    font-size: 2rem;
    font-weight: 400;
    color: var(--accent);
}
.stat-card .stat-label {
    font-size: 0.78rem;
    color: var(--muted);
    margin-top: 2px;
}

/* ── History entry ── */
.history-entry {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
    font-size: 0.88rem;
    box-shadow: var(--shadow);
}

/* ── Chips ── */
.chip-row { display: flex; flex-wrap: wrap; gap: 6px; margin: 0.5rem 0 1rem; }
.chip {
    font-size: 0.72rem;
    padding: 3px 10px;
    border-radius: 20px;
    background: var(--accent-dim);
    border: 1px solid rgba(26,158,143,0.2);
    color: var(--accent-dark);
    font-weight: 500;
}

/* ── Alerts ── */
.stAlert {
    border-radius: var(--radius) !important;
    border: 1px solid var(--border) !important;
    background: var(--surface2) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: var(--surface) !important;
    border: 1.5px dashed var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 0.5rem !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--accent) !important;
}
[data-testid="stFileUploader"] label {
    color: var(--muted) !important;
    font-size: 0.85rem !important;
}

/* ── Input source pill selector ── */
.pill-row {
    display: flex;
    gap: 8px;
    margin-bottom: 1rem;
}
.pill {
    padding: 5px 16px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    cursor: pointer;
    border: 1.5px solid var(--border);
    background: var(--surface2);
    color: var(--muted);
    letter-spacing: 0.03em;
}
.pill-active {
    background: var(--accent-dim);
    border-color: var(--accent);
    color: var(--accent-dark);
}

/* ── PDF notice ── */
.pdf-notice {
    font-size: 0.78rem;
    color: var(--accent-dark);
    background: var(--accent-dim);
    border-radius: 6px;
    padding: 6px 12px;
    margin-top: 0.4rem;
    display: inline-block;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* Divider */
hr { border-color: var(--border) !important; margin: 1.4rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
for key, default in [("history", []), ("session_count", 0)]:
    if key not in st.session_state:
        st.session_state[key] = default


def save_to_history(action: str, prompt: str, output: str):
    st.session_state.history.insert(0, {
        "action": action,
        "prompt": prompt[:120] + ("…" if len(prompt) > 120 else ""),
        "output": output,
        "time": datetime.now().strftime("%H:%M · %b %d"),
    })
    st.session_state.session_count += 1
    if len(st.session_state.history) > 20:
        st.session_state.history = st.session_state.history[:20]


def extract_pdf_text(uploaded_file) -> str:
    """Extract plain text from an uploaded PDF using PyPDF2."""
    try:
        import PyPDF2, io
        reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n\n".join(pages).strip()
    except ImportError:
        try:
            import pdfplumber, io
            with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
                pages = [p.extract_text() or "" for p in pdf.pages]
            return "\n\n".join(pages).strip()
        except Exception as e:
            return f"[PDF extraction error: {e}]"
    except Exception as e:
        return f"[PDF extraction error: {e}]"


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1rem 0 1.5rem;">
        <div style="font-family:'DM Serif Display',serif; font-size:1.4rem; font-style:italic; color:#fff;">
            🧠 StudyMind
        </div>
        <div style="font-size:0.73rem; color:rgba(255,255,255,0.65); margin-top:2px; text-transform:uppercase; letter-spacing:0.07em;">
            AI Study Companion
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("##### This Session")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Generations", st.session_state.session_count)
    with c2:
        st.metric("Saved", len(st.session_state.history))

    st.markdown("---")
    st.markdown("##### Settings")
    model_label = st.selectbox("AI Model", ["Gemini Pro", "Gemini Flash"], label_visibility="collapsed")
    response_style = st.selectbox(
        "Response style",
        ["Detailed", "Concise", "Bullet points"],
        help="Controls the output verbosity sent to the model."
    )
    st.markdown("---")
    st.markdown("##### Quick tips")
    st.caption("• Be specific — 'Explain Newton's 2nd law with examples' beats 'Explain Newton'")
    st.caption("• Upload a PDF in Summarize or Quiz tabs to use your own material")
    st.caption("• Use Study Plan before exams to structure your prep")
    st.markdown("---")
    if st.button("🗑 Clear History", use_container_width=True):
        st.session_state.history = []
        st.session_state.session_count = 0
        st.rerun()

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <h1>StudyMind</h1>
    <span class="badge">AI-Powered</span>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_explain, tab_summarize, tab_quiz, tab_plan, tab_history = st.tabs([
    "💡 Explain",
    "📄 Summarize",
    "📝 Quiz",
    "📅 Study Plan",
    "🕘 History",
])

# ── Helper: render output ─────────────────────────────────────────────────────
def render_output(label: str, content: str):
    st.markdown(f"<div class='section-label'>{label}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='output-box'>{content}</div>", unsafe_allow_html=True)
    col_copy, col_dl, _ = st.columns([1, 1, 4])
    with col_copy:
        if st.button("📋 Copy", key=f"copy_{label}_{int(time.time())}"):
            st.toast("Copied to clipboard!", icon="✅")
    with col_dl:
        st.download_button(
            "⬇ Download",
            data=content,
            file_name=f"studymind_{label.replace(' ', '_').lower()}_{int(time.time())}.txt",
            mime="text/plain",
            key=f"dl_{label}_{int(time.time())}",
        )


# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 · Explain Topic
# ─────────────────────────────────────────────────────────────────────────────
with tab_explain:
    st.markdown("#### Explain a Concept")
    st.caption("Get a clear, structured explanation for any topic — from first principles to advanced nuance.")

    st.markdown('<div class="section-label">Topic</div>', unsafe_allow_html=True)
    topic_input = st.text_area(
        "topic", label_visibility="collapsed",
        height=120,
        placeholder="e.g. How does a PN junction diode work? Explain with band theory.",
        key="explain_input"
    )

    col_a, col_b = st.columns(2)
    with col_a:
        depth = st.selectbox("Depth", ["Beginner", "Intermediate", "Advanced"], key="explain_depth")
    with col_b:
        include_examples = st.toggle("Include examples", value=True, key="explain_ex")

    st.markdown(
        '<div class="chip-row">'
        '<span class="chip">Physics</span><span class="chip">Maths</span>'
        '<span class="chip">Chemistry</span><span class="chip">CS</span>'
        '<span class="chip">Biology</span><span class="chip">Economics</span>'
        '</div>',
        unsafe_allow_html=True
    )

    if st.button("Explain ✦", key="btn_explain"):
        if not topic_input.strip():
            st.warning("Enter a topic to explain.")
        else:
            prompt = topic_input
            if include_examples:
                prompt += " Include practical examples."
            prompt += f" Target audience: {depth} level."
            if response_style != "Detailed":
                prompt += f" Keep the response {response_style.lower()}."
            with st.spinner("Building explanation…"):
                output = explain_topic(prompt)
            save_to_history("Explain", topic_input, output)
            render_output("Explanation", output)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 · Summarize Notes  (with PDF upload)
# ─────────────────────────────────────────────────────────────────────────────
with tab_summarize:
    st.markdown("#### Summarize Notes")
    st.caption("Paste your notes **or** upload a PDF — get a clean, revision-ready summary.")

    # Source selector
    sum_source = st.radio(
        "Input source",
        ["✏️ Type / Paste", "📎 Upload PDF"],
        horizontal=True,
        label_visibility="collapsed",
        key="sum_source"
    )

    notes_text = ""

    if sum_source == "✏️ Type / Paste":
        st.markdown('<div class="section-label">Your notes</div>', unsafe_allow_html=True)
        notes_input = st.text_area(
            "notes", label_visibility="collapsed",
            height=220,
            placeholder="Paste your notes, textbook excerpts, or lecture content here…",
            key="summarize_input"
        )
        notes_text = notes_input
        word_count = len(notes_text.split()) if notes_text.strip() else 0
        if word_count:
            st.caption(f"📊 ~{word_count} words")

    else:  # PDF upload
        st.markdown('<div class="section-label">Upload a PDF</div>', unsafe_allow_html=True)
        sum_pdf = st.file_uploader(
            "pdf_sum", type=["pdf"], label_visibility="collapsed", key="sum_pdf_upload"
        )
        if sum_pdf:
            with st.spinner("Reading PDF…"):
                pdf_text = extract_pdf_text(sum_pdf)
            if pdf_text.startswith("[PDF extraction error"):
                st.error(pdf_text)
            else:
                notes_text = pdf_text
                wc = len(notes_text.split())
                st.markdown(
                    f'<div class="pdf-notice">✅ PDF loaded — ~{wc} words extracted from <strong>{sum_pdf.name}</strong></div>',
                    unsafe_allow_html=True
                )
        else:
            st.info("Upload a PDF file to use as input.")

    st.markdown("---")
    col_c, col_d = st.columns(2)
    with col_c:
        summary_style = st.selectbox(
            "Output format",
            ["Paragraph", "Bullet points", "Key–Value pairs"],
            key="sum_style"
        )
    with col_d:
        highlight_keywords = st.toggle("Highlight key terms", value=True, key="sum_kw")

    if st.button("Summarize ✦", key="btn_summarize"):
        if not notes_text.strip():
            st.warning("Add some text or upload a PDF first.")
        else:
            prompt = notes_text
            prompt += f"\n\nOutput format: {summary_style}."
            if highlight_keywords:
                prompt += " Mark key terms clearly."
            with st.spinner("Condensing notes…"):
                output = summarize_notes(prompt)
            label_hint = sum_pdf.name if (sum_source == "📎 Upload PDF" and sum_pdf) else notes_text[:80]
            save_to_history("Summarize", label_hint, output)
            render_output("Summary", output)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 · Quiz Generator  (with PDF upload)
# ─────────────────────────────────────────────────────────────────────────────
with tab_quiz:
    st.markdown("#### Generate a Quiz")
    st.caption("Type a topic, paste content, **or** upload a PDF to create practice questions.")

    quiz_source = st.radio(
        "Input source",
        ["✏️ Type / Paste", "📎 Upload PDF"],
        horizontal=True,
        label_visibility="collapsed",
        key="quiz_source"
    )

    quiz_content = ""

    if quiz_source == "✏️ Type / Paste":
        st.markdown('<div class="section-label">Topic or content</div>', unsafe_allow_html=True)
        quiz_input = st.text_area(
            "quiz_topic", label_visibility="collapsed",
            height=150,
            placeholder="e.g. Thermodynamics – First and Second Laws",
            key="quiz_input"
        )
        quiz_content = quiz_input

    else:  # PDF upload
        st.markdown('<div class="section-label">Upload a PDF</div>', unsafe_allow_html=True)
        quiz_pdf = st.file_uploader(
            "pdf_quiz", type=["pdf"], label_visibility="collapsed", key="quiz_pdf_upload"
        )
        if quiz_pdf:
            with st.spinner("Reading PDF…"):
                pdf_text = extract_pdf_text(quiz_pdf)
            if pdf_text.startswith("[PDF extraction error"):
                st.error(pdf_text)
            else:
                quiz_content = pdf_text
                wc = len(quiz_content.split())
                st.markdown(
                    f'<div class="pdf-notice">✅ PDF loaded — ~{wc} words extracted from <strong>{quiz_pdf.name}</strong></div>',
                    unsafe_allow_html=True
                )
        else:
            st.info("Upload a PDF file to generate questions from.")

    st.markdown("---")
    col_e, col_f, col_g = st.columns(3)
    with col_e:
        q_count = st.number_input("Questions", min_value=3, max_value=20, value=5, key="q_count")
    with col_f:
        q_type = st.selectbox("Type", ["MCQ", "True/False", "Short Answer", "Mixed"], key="q_type")
    with col_g:
        q_diff = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], index=1, key="q_diff")

    include_answers = st.toggle("Include answer key", value=True, key="quiz_ans")

    if st.button("Generate Quiz ✦", key="btn_quiz"):
        if not quiz_content.strip():
            st.warning("Enter a topic or upload a PDF first.")
        else:
            prompt = (
                f"Topic/Content:\n{quiz_content}\n\n"
                f"Generate {q_count} {q_type} questions at {q_diff} difficulty."
            )
            if include_answers:
                prompt += " Include correct answers after each question."
            else:
                prompt += " Do NOT include answers — this is a student copy."
            with st.spinner("Crafting questions…"):
                output = generate_quiz(prompt)
            label_hint = quiz_pdf.name if (quiz_source == "📎 Upload PDF" and quiz_pdf) else quiz_content[:80]
            save_to_history("Quiz", label_hint, output)
            render_output("Quiz", output)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 · Study Plan
# ─────────────────────────────────────────────────────────────────────────────
with tab_plan:
    st.markdown("#### Build a Study Plan")
    st.caption("Get a structured, day-by-day study schedule tailored to your subjects and timeline.")

    col_h, col_i = st.columns([3, 1])
    with col_h:
        st.markdown('<div class="section-label">Subjects (comma separated)</div>', unsafe_allow_html=True)
        subjects_input = st.text_input(
            "subjects", label_visibility="collapsed",
            placeholder="Maths, Physics, DBMS, Python, Chemistry",
            key="plan_subjects"
        )
    with col_i:
        st.markdown('<div class="section-label">Study days</div>', unsafe_allow_html=True)
        days_input = st.number_input(
            "days", label_visibility="collapsed",
            min_value=1, max_value=90, value=14, key="plan_days"
        )

    col_j, col_k = st.columns(2)
    with col_j:
        difficulty = st.selectbox("Overall difficulty", ["Easy", "Medium", "Hard"], index=1, key="plan_diff")
    with col_k:
        daily_hours = st.number_input("Daily study hours", min_value=1, max_value=12, value=4, key="plan_hrs")

    goals_input = st.text_input(
        "Specific goals (optional)",
        placeholder="e.g. Focus on integration, SQL joins, and recursion",
        key="plan_goals"
    )

    if st.button("Generate Plan ✦", key="btn_plan"):
        if not subjects_input.strip():
            st.warning("Enter at least one subject.")
        else:
            enriched_subjects = subjects_input
            if goals_input.strip():
                enriched_subjects += f". Goals: {goals_input}"
            enriched_subjects += f". Daily hours available: {daily_hours}."
            with st.spinner("Planning your study schedule…"):
                output = generate_study_plan(enriched_subjects, difficulty, days_input)
            save_to_history("Study Plan", subjects_input, output)
            render_output("Study Plan", output)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 5 · History
# ─────────────────────────────────────────────────────────────────────────────
with tab_history:
    st.markdown("#### Session History")
    st.caption("All generations from this session — cleared on refresh.")

    if not st.session_state.history:
        st.info("Nothing yet — your generations will appear here.")
    else:
        for i, entry in enumerate(st.session_state.history):
            with st.expander(f"**{entry['action']}** · {entry['time']} · _{entry['prompt']}_"):
                st.markdown(f"<div class='output-box'>{entry['output']}</div>", unsafe_allow_html=True)
                st.download_button(
                    "⬇ Download",
                    data=entry["output"],
                    file_name=f"studymind_{entry['action'].lower()}_{i}.txt",
                    mime="text/plain",
                    key=f"hist_dl_{i}",
                )