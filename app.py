import streamlit as st
import whisper
import google.generativeai as genai
import os
import json

# PAGE CONFIG
st.set_page_config(
    page_title="AI Lecture Assistant",
    page_icon="📚",
    layout="wide"
)

# LOAD MODEL
@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
g_model = genai.GenerativeModel("gemini-1.5-flash")  # 🔥 faster model

# -----------------------------
# SAFE TRIM FUNCTION
# -----------------------------
def trim_text(text, max_chars=7000):
    if len(text) <= max_chars:
        return text

    cut = text[:max_chars]
    last_dot = cut.rfind(".")

    if last_dot == -1:
        return cut

    return cut[:last_dot + 1]

# SIDEBAR
with st.sidebar:
    st.header("📚 AI Lecture Assistant")
    st.write("""
    ### Features
    - 🎤 Speech to Text
    - 📌 AI Notes
    - 🎯 AI Quiz
    - 💬 AI Tutor
    """)
    st.write("---")
    st.info("Upload lecture audio to begin.")

# TITLE
st.markdown(
    "<h1 style='text-align:center;'>📚 AI Lecture Assistant</h1>",
    unsafe_allow_html=True
)

st.write("")

# FILE UPLOADER
uploaded_file = st.file_uploader(
    "Upload audio (mp3/wav)",
    type=["mp3", "wav"]
)

# SESSION INIT
for key in ["transcript", "summary", "quiz", "file_name", "chat_answer", "submitted"]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "submitted" else False

# SAFE FILE HANDLING
file_path = None

if uploaded_file is not None:

    if st.session_state.file_name != uploaded_file.name:

        st.session_state.transcript = None
        st.session_state.summary = None
        st.session_state.quiz = None
        st.session_state.chat_answer = None
        st.session_state.submitted = False
        st.session_state.file_name = uploaded_file.name

        for key in list(st.session_state.keys()):
            if key.startswith("q_"):
                del st.session_state[key]

    file_path = "temp_audio.wav"

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if os.path.getsize(file_path) == 0:
        st.error("❌ Uploaded file is empty or corrupted")
        st.stop()

    st.success("✅ File uploaded successfully!")

# QUIZ PARSER
def safe_parse_quiz(text):
    try:
        text = text.replace("```json", "").replace("```", "").strip()
        start = text.find("[")
        end = text.rfind("]") + 1

        if start == -1 or end == -1:
            return None

        return json.loads(text[start:end])

    except:
        return None

# -----------------------------
# AI FUNCTIONS (FIXED PROPERLY)
# -----------------------------

def summarize(text):
    text = trim_text(text)

    prompt = f"""
Convert this lecture into:
1. Simple Notes
2. Key Points
3. Short Summary

Keep response concise.

Lecture:
{text}
"""
    return g_model.generate_content(prompt).text


def generate_quiz(text):
    text = trim_text(text)

    prompt = f"""
Create 5 MCQs from this lecture.

Return ONLY valid JSON.

Lecture:
{text}
"""
    return g_model.generate_content(prompt).text


def ask_question(question, transcript):
    transcript = trim_text(transcript)

    prompt = f"""
You are an AI tutor.

Answer ONLY using the lecture transcript.

If not found:
"Answer not found in lecture."

Lecture:
{transcript}

Question:
{question}
"""
    return g_model.generate_content(prompt).text

# TABS
tab1, tab2, tab3, tab4 = st.tabs([
    "📝 Transcript",
    "📚 AI Notes",
    "🎯 Quiz",
    "🤖 AI Tutor"
])

# TAB 1
with tab1:
    if st.button("Generate Transcript"):
        if st.session_state.transcript is None and file_path:
            with st.spinner("🎤 Transcribing lecture..."):
                result = model.transcribe(file_path)

                # LIMIT TRANSCRIPT
                st.session_state.transcript = result["text"][:8000]

        else:
            st.info("Transcript already generated ✅")

    if st.session_state.transcript:
        st.success("✅ Transcript Generated")
        with st.expander("View Transcript"):
            st.write(st.session_state.transcript)

# TAB 2
with tab2:
    if st.button("Generate Notes"):
        if st.session_state.summary is None:
            if st.session_state.transcript:
                with st.spinner("📚 Generating AI notes..."):
                    st.session_state.summary = summarize(st.session_state.transcript)
            else:
                st.warning("Generate transcript first!")

    if st.session_state.summary:
        st.success("✅ Notes Generated")
        with st.expander("View Notes"):
            st.write(st.session_state.summary)

        st.download_button(
            "⬇ Download Notes",
            st.session_state.summary,
            file_name="lecture_notes.txt"
        )

# TAB 3
with tab3:
    if st.button("Generate Quiz"):
        if st.session_state.quiz is None:
            if st.session_state.transcript:
                with st.spinner("🎯 Generating quiz..."):
                    st.session_state.quiz = generate_quiz(st.session_state.transcript)
            else:
                st.warning("Generate transcript first!")

    if st.session_state.quiz:
        quiz_data = safe_parse_quiz(st.session_state.quiz)

        if quiz_data:
            st.write("## 🎯 Quiz")

            if not st.session_state.submitted:
                for i, q in enumerate(quiz_data):
                    st.write(f"### Q{i+1}: {q['question']}")
                    st.radio(
                        "Choose your answer",
                        q["options"],
                        index=None,
                        key=f"q_{i}_{st.session_state.file_name}"
                    )

                if st.button("📊 Submit Quiz"):
                    st.session_state.submitted = True
                    st.rerun()

            else:
                score = 0

                for i, q in enumerate(quiz_data):
                    user_ans = st.session_state.get(f"q_{i}_{st.session_state.file_name}")
                    correct_ans = q["answer"]

                    st.write(f"### Q{i+1}: {q['question']}")

                    for option in q["options"]:
                        if option == correct_ans:
                            st.success(option)
                        elif option == user_ans:
                            st.error(option)
                        else:
                            st.write(option)

                    if user_ans == correct_ans:
                        score += 1

                st.subheader(f"🏆 Final Score: {score} / {len(quiz_data)}")

                if st.button("🔄 Retry Quiz"):
                    st.session_state.submitted = False
                    for key in list(st.session_state.keys()):
                        if key.startswith("q_"):
                            del st.session_state[key]
                    st.rerun()

# TAB 4
with tab4:
    st.write("## 🤖 Ask Questions from Lecture")

    if st.session_state.transcript:
        user_question = st.text_input("Ask something about the lecture")

        if st.button("Ask AI"):
            if user_question.strip():
                with st.spinner("🤖 Thinking..."):
                    st.session_state.chat_answer = ask_question(
                        user_question,
                        st.session_state.transcript
                    )

        if st.session_state.chat_answer:
            st.success("✅ Answer Generated")
            st.write(st.session_state.chat_answer)
    else:
        st.warning("Generate transcript first!")

# RESET
st.write("---")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("🔄 Reset App", use_container_width=True):
        st.session_state.clear()

        for f in ["temp_audio.wav", "audio.mp3", "audio.wav"]:
            if os.path.exists(f):
                os.remove(f)

        st.rerun()

# FOOTER
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        text-align: center;
        padding: 10px;
        background-color: #0E1117;
        color: gray;
        font-size: 14px;
    }
    </style>

    <div class="footer">
        Built using Whisper + Gemini + Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
