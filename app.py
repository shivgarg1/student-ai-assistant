# app.py
import streamlit as st
import time
from assistant import get_response

# ── PAGE CONFIG ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="Aria AI",
    page_icon="🤖",
    layout="centered",
)

# ── PWA + MOBILE META ─────────────────────────────────────────────────
st.markdown("""
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-title" content="Aria AI">
        <meta name="theme-color" content="#7b2ff7">
    </head>
""", unsafe_allow_html=True)

# ── CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');

    * { font-family: 'Space Grotesk', sans-serif !important; }

    /* ── Hide streamlit default stuff ── */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 120px !important;
    }

    /* ── Background ── */
    .stApp { background: #0a0a0f; }

    /* ── Header banner ── */
    .header-box {
        background: linear-gradient(135deg, #7b2ff7 0%, #f107a3 100%);
        border-radius: 24px;
        padding: 20px 24px;
        text-align: center;
        color: white;
        margin-bottom: 16px;
        position: relative;
        overflow: hidden;
    }
    .header-box::before {
        content: '';
        position: absolute;
        top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%);
        animation: shimmer 3s infinite;
    }
    @keyframes shimmer {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .header-box h2 {
        font-size: 24px;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .header-box p {
        font-size: 12px;
        opacity: 0.8;
        margin: 4px 0 0;
    }

    /* ── Stats bar ── */
    .stats-bar {
        display: flex;
        justify-content: space-around;
        background: #13131a;
        border: 1px solid #2a2a3a;
        border-radius: 16px;
        padding: 12px;
        margin-bottom: 16px;
    }
    .stat-item { text-align: center; }
    .stat-number {
        font-size: 20px;
        font-weight: 700;
        background: linear-gradient(135deg, #7b2ff7, #f107a3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stat-label { font-size: 10px; color: #666; margin-top: 2px; }

    /* ── Chat bubbles ── */
    .chat-row {
        display: flex;
        align-items: flex-end;
        margin: 8px 0;
        clear: both;
        animation: fadeUp 0.3s ease;
    }
    .chat-row.user-row { flex-direction: row-reverse; }

    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(10px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    .user-bubble {
        background: linear-gradient(135deg, #7b2ff7, #f107a3);
        color: white;
        padding: 12px 16px;
        border-radius: 20px 20px 4px 20px;
        max-width: 78%;
        font-size: 15px;
        line-height: 1.5;
        box-shadow: 0 4px 20px rgba(123,47,247,0.3);
    }
    .bot-bubble {
        background: #13131a;
        border: 1px solid #2a2a3a;
        color: #e0e0e0;
        padding: 12px 16px;
        border-radius: 20px 20px 20px 4px;
        max-width: 78%;
        font-size: 15px;
        line-height: 1.5;
    }
    .avatar {
        width: 32px; height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        flex-shrink: 0;
        margin: 0 8px;
    }
    .bot-avatar  { background: linear-gradient(135deg, #7b2ff7, #f107a3); }
    .user-avatar { background: #2a2a3a; }

    /* ── Loading dots ── */
    .loading-dots {
        display: flex;
        gap: 5px;
        padding: 12px 16px;
        background: #13131a;
        border: 1px solid #2a2a3a;
        border-radius: 20px 20px 20px 4px;
        width: fit-content;
    }
    .dot {
        width: 7px; height: 7px;
        background: #7b2ff7;
        border-radius: 50%;
        animation: bounce 1.2s infinite;
    }
    .dot:nth-child(2) { animation-delay: 0.2s; }
    .dot:nth-child(3) { animation-delay: 0.4s; }
    @keyframes bounce {
        0%, 80%, 100% { transform: scale(0.7); opacity: 0.4; }
        40%            { transform: scale(1.2); opacity: 1; }
    }

    /* ── Fixed bottom input bar ── */
    .fixed-bottom {
        position: fixed;
        bottom: 0; left: 0; right: 0;
        background: #0a0a0f;
        border-top: 1px solid #2a2a3a;
        padding: 12px 16px;
        z-index: 999;
        backdrop-filter: blur(10px);
    }

    /* ── Chat input styling ── */
    .stChatInput input {
        background: #13131a !important;
        border: 1px solid #2a2a3a !important;
        border-radius: 16px !important;
        color: white !important;
        font-size: 15px !important;
        padding: 12px 16px !important;
    }
    .stChatInput input:focus {
        border-color: #7b2ff7 !important;
        box-shadow: 0 0 0 2px rgba(123,47,247,0.2) !important;
    }

    /* ── Mic button ── */
    .stButton button {
        background: linear-gradient(135deg, #7b2ff7, #f107a3) !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        font-size: 18px !important;
        height: 50px !important;
        transition: transform 0.2s ease !important;
    }
    .stButton button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 4px 20px rgba(123,47,247,0.4) !important;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: #0d0d14 !important;
        border-right: 1px solid #2a2a3a !important;
    }
    [data-testid="stSidebar"] * { color: #e0e0e0 !important; }
    [data-testid="stSidebar"] input {
        background: #13131a !important;
        border: 1px solid #2a2a3a !important;
        color: white !important;
        border-radius: 10px !important;
    }
    [data-testid="stSidebar"] .stSelectbox > div {
        background: #13131a !important;
        border: 1px solid #2a2a3a !important;
        border-radius: 10px !important;
    }

    /* ── Radio buttons ── */
    [data-testid="stSidebar"] .stRadio label {
        background: #13131a;
        border: 1px solid #2a2a3a;
        border-radius: 10px;
        padding: 8px 12px;
        margin: 3px 0;
        display: block;
        cursor: pointer;
        transition: all 0.2s;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        border-color: #7b2ff7 !important;
    }

    /* ── Sidebar buttons ── */
    [data-testid="stSidebar"] .stButton button {
        background: #13131a !important;
        border: 1px solid #2a2a3a !important;
        border-radius: 10px !important;
        font-size: 13px !important;
        height: auto !important;
        padding: 8px !important;
    }
    [data-testid="stSidebar"] .stButton button:hover {
        border-color: #7b2ff7 !important;
    }

    /* ── Mobile responsive ── */
    @media (max-width: 768px) {
        .header-box h2 { font-size: 18px !important; }
        .user-bubble, .bot-bubble {
            max-width: 92% !important;
            font-size: 14px !important;
        }
        .stat-number { font-size: 16px !important; }
    }
    

    /* ── Push content above input bar ── */
    .block-container {
        padding-bottom: 140px !important;
        max-width: 760px !important;
    }
    # ── TOOLS TABS ────────────────────────────────────────────────────────
st.markdown("---")
tab1, tab2 = st.tabs(["📅 Study Plan", "🧠 Quiz"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        subject = st.text_input("📚 subject", placeholder="e.g. Physics, DSA")
        level   = st.selectbox("📊 level", ["Beginner", "Intermediate", "Advanced"])
    with col2:
        days  = st.slider("📆 days", 3, 30, 7)
        hours = st.slider("⏰ hrs/day", 1, 8, 2)
    goal = st.text_input("🎯 goal", placeholder="e.g. pass exam, get internship")

    if st.button("🧠 generate plan", use_container_width=True):
        if subject:
            with st.spinner("cooking ur plan... 👨‍🍳"):
                plan = get_response(
                    f"Create a {days}-day study plan for {subject} at {level} level, {hours} hrs/day. Goal: {goal or 'master it'}. Format day by day.",
                    st.session_state.personality
                )
            st.markdown(plan)
            st.download_button("💾 save", plan, f"plan_{subject}.txt")
        else:
            st.warning("enter a subject first 💀")

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        quiz_sub   = st.text_input("📚 topic", placeholder="e.g. Python, History")
        quiz_level = st.selectbox("📊 difficulty", ["Easy", "Medium", "Hard"], key="qlvl")
    with col2:
        num_q     = st.slider("❓ questions", 3, 10, 5)
        quiz_type = st.selectbox("📝 type", ["Multiple Choice", "True/False", "Mixed"])

    if st.button("🎯 generate quiz", use_container_width=True):
        if quiz_sub:
            with st.spinner("making ur quiz... 📝"):
                quiz = get_response(
                    f"Create a {quiz_level} {quiz_type} quiz about {quiz_sub} with {num_q} questions. Show question, options A-D, ✅ answer, explanation.",
                    st.session_state.personality
                )
            st.markdown(quiz)
            st.download_button("💾 save", quiz, f"quiz_{quiz_sub}.txt")
            st.session_state.topics_asked += 1
        else:
            st.warning("enter a topic first 💀")
</style>
""", unsafe_allow_html=True)


# ── SESSION STATE ─────────────────────────────────────────────────────
if "messages"       not in st.session_state:
    st.session_state.messages       = []
if "total_messages" not in st.session_state:
    st.session_state.total_messages = 0
if "mood"           not in st.session_state:
    st.session_state.mood           = "😊 Happy"
if "topics_asked"   not in st.session_state:
    st.session_state.topics_asked   = 0
if "personality"    not in st.session_state:
    st.session_state.personality    = "😊 Friend"


# ── SIDEBAR ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.markdown("---")

    assistant_name = st.text_input("🤖 Name", value="Aria")

    st.markdown("### 🎭 Vibe")
    personality = st.radio(
        "How should Aria talk?",
        ["😊 Friend", "💕 Companion", "🎓 Mentor", "📚 Strict Teacher"],
        index=0
    )
    descriptions = {
        "😊 Friend":         "casual, unhinged, bestie energy 💀",
        "💕 Companion":      "soft, sweet, always there 🥺",
        "🎓 Mentor":         "wise, real talk, big picture 🌟",
        "📚 Strict Teacher": "no cap, no excuses, just work 📖"
    }
    st.caption(descriptions[personality])
    st.session_state.personality = personality

    st.markdown("---")
    response_length = st.selectbox(
        "📏 Length",
        ["Short & Simple", "Medium", "Detailed"],
        index=1
    )

    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages       = []
        st.session_state.total_messages = 0
        st.session_state.topics_asked   = 0
        st.session_state.mood           = "😊 Happy"
        st.rerun()

    st.markdown("---")
    st.markdown("### ⚡ Quick")
    if st.button("📚 study help", use_container_width=True):
        st.session_state["quick_prompt"] = "Help me make a study plan"
    if st.button("💪 motivate me", use_container_width=True):
        st.session_state["quick_prompt"] = "I need some motivation rn"
    if st.button("😟 im stressed", use_container_width=True):
        st.session_state["quick_prompt"] = "im really stressed about exams"
    if st.button("🧠 quiz me", use_container_width=True):
        st.session_state["quick_prompt"] = "Give me a quick quiz on something I study"

    st.markdown("---")
    st.caption("built by shiv 🚀")


# ── SHOW MESSAGE ──────────────────────────────────────────────────────
def show_message(role, text):
    if role == "user":
        st.markdown(f"""
            <div class="chat-row user-row">
                <div class="user-bubble">{text}</div>
                <div class="avatar user-avatar">🧑</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="chat-row">
                <div class="avatar bot-avatar">🤖</div>
                <div class="bot-bubble">{text}</div>
            </div>
        """, unsafe_allow_html=True)


# ── HEADER ────────────────────────────────────────────────────────────
st.markdown(f"""
    <div class="header-box">
        <h2>🤖 {assistant_name} — ur AI bestie</h2>
        <p>powered by llama 3 · {personality} mode · always free ⚡</p>
    </div>
""", unsafe_allow_html=True)

# ── STATS ─────────────────────────────────────────────────────────────
st.markdown(f"""
    <div class="stats-bar">
        <div class="stat-item">
            <div class="stat-number">{st.session_state.total_messages}</div>
            <div class="stat-label">💬 messages</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{st.session_state.topics_asked}</div>
            <div class="stat-label">📚 topics</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{st.session_state.mood}</div>
            <div class="stat-label">current vibe</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ── WELCOME ───────────────────────────────────────────────────────────
if not st.session_state.messages:
    from memory import load_memory
    mem = load_memory()
    if mem["name"]:
        welcome = f"yooo {mem['name']}! welcome back 👋 what are we doing today bestie? 🚀"
    else:
        welcome = f"heyyy! 👋 i'm {assistant_name}, ur AI bestie. what's ur name? i'll remember u! 🧠"
    show_message("bot", welcome)

# ── CHAT HISTORY ──────────────────────────────────────────────────────
for msg in st.session_state.messages:
    show_message(msg["role"], msg["content"])

# ── QUICK PROMPTS ─────────────────────────────────────────────────────
if "quick_prompt" in st.session_state:
    quick = st.session_state.pop("quick_prompt")
    st.session_state.messages.append({"role": "user", "content": quick})
    show_message("user", quick)

    loading = st.empty()
    loading.markdown("""
        <div class="chat-row">
            <div class="avatar bot-avatar">🤖</div>
            <div class="loading-dots">
                <div class="dot"></div><div class="dot"></div><div class="dot"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    reply = get_response(quick, st.session_state.personality)
    time.sleep(0.5)
    loading.empty()

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.total_messages += 2
    st.session_state.topics_asked   += 1
    show_message("bot", reply)
    st.rerun()

# ── STUDY PLAN ────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("📅 study plan generator", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        subject  = st.text_input("📚 subject", placeholder="e.g. Physics, DSA")
        level    = st.selectbox("📊 level", ["Beginner", "Intermediate", "Advanced"])
    with col2:
        days     = st.slider("📆 days", 3, 30, 7)
        hours    = st.slider("⏰ hrs/day", 1, 8, 2)
    goal = st.text_input("🎯 goal", placeholder="e.g. pass exam, get internship")

    if st.button("🧠 generate plan"):
        if subject:
            with st.spinner("cooking ur study plan... 👨‍🍳"):
                plan = get_response(
                    f"Create a {days}-day study plan for {subject} at {level} level, {hours} hours/day. Goal: {goal or 'master the subject'}. Format day by day with topics, resources and practice.",
                    st.session_state.personality
                )
            st.markdown(plan)
            st.download_button("💾 save plan", plan, f"plan_{subject}.txt")
        else:
            st.warning("bro enter a subject first 💀")

# ── QUIZ ──────────────────────────────────────────────────────────────
with st.expander("🧠 quiz generator", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        quiz_sub   = st.text_input("📚 topic", placeholder="e.g. Python, History")
        quiz_level = st.selectbox("📊 difficulty", ["Easy", "Medium", "Hard"], key="qlvl")
    with col2:
        num_q    = st.slider("❓ questions", 3, 10, 5)
        quiz_type = st.selectbox("📝 type", ["Multiple Choice", "True/False", "Mixed"])

    if st.button("🎯 generate quiz"):
        if quiz_sub:
            with st.spinner("making ur quiz... 📝"):
                quiz = get_response(
                    f"Create a {quiz_level} {quiz_type} quiz about {quiz_sub} with {num_q} questions. For each: show question, options (A-D), correct answer with ✅, and brief explanation.",
                    st.session_state.personality
                )
            st.markdown(quiz)
            st.download_button("💾 save quiz", quiz, f"quiz_{quiz_sub}.txt")
            st.session_state.topics_asked += 1
        else:
            st.warning("enter a topic first bestie 💀")

# ── BOTTOM INPUT BAR ──────────────────────────────────────────────────
# ── BOTTOM INPUT ──────────────────────────────────────────────────────
st.markdown("---")
col_mic, col_chat = st.columns([1, 9])

with col_mic:
    mic_btn = st.button("🎙️", use_container_width=True)

with col_chat:
    user_input = st.chat_input(f"message {assistant_name}...")
# ── MIC HANDLER ───────────────────────────────────────────────────────
if mic_btn:
    from voice_helper import text_to_speech
    from assistant import client
    import sounddevice as sd
    import numpy as np
    from scipy.io.wavfile import write
    import tempfile, os

    SAMPLE_RATE = 16000
    DURATION    = 6

    rec_holder = st.empty()
    rec_holder.info("🔴 listening... speak now!")

    audio_data = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype='int16',
        device=2
    )
    sd.wait()
    rec_holder.empty()

    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
        write(tmp.name, SAMPLE_RATE, audio_data)
        tmp_path = tmp.name

    with st.spinner("transcribing... 🧠"):
        try:
            with open(tmp_path, 'rb') as f:
                transcription = client.audio.transcriptions.create(
                    model="whisper-large-v3",
                    file=f,
                    language="en"
                )
            spoken_text = transcription.text.strip()
        except Exception as e:
            spoken_text = None
            st.error(f"error: {e}")
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    if spoken_text and spoken_text != ".":
        st.success(f"u said: '{spoken_text}'")
        st.session_state.messages.append({"role": "user", "content": f"🎙️ {spoken_text}"})
        show_message("user", f"🎙️ {spoken_text}")

        with st.spinner("thinking... 💭"):
            reply = get_response(spoken_text, st.session_state.personality)

        st.session_state.messages.append({"role": "assistant", "content": reply})
        show_message("bot", reply)
        text_to_speech(reply)
        st.session_state.total_messages += 2
        st.rerun()
    else:
        st.warning("couldn't hear u bestie, try again 💀")

# ── TEXT INPUT HANDLER ────────────────────────────────────────────────
if user_input:
    mood_map = {
        "stressed": "😟 stressed", "sad": "😢 sad",
        "happy":    "😊 happy",    "excited": "🤩 excited",
        "tired":    "😴 tired",    "confused": "😕 confused",
    }
    for keyword, mood in mood_map.items():
        if keyword in user_input.lower():
            st.session_state.mood = mood
            break

    study_kw = ["explain", "what is", "how does", "teach", "help me", "study", "homework"]
    if any(k in user_input.lower() for k in study_kw):
        st.session_state.topics_asked += 1

    st.session_state.messages.append({"role": "user", "content": user_input})
    show_message("user", user_input)

    loading = st.empty()
    loading.markdown("""
        <div class="chat-row">
            <div class="avatar bot-avatar">🤖</div>
            <div class="loading-dots">
                <div class="dot"></div><div class="dot"></div><div class="dot"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    length_map = {
        "Short & Simple": "Keep response under 3 sentences.",
        "Medium":         "Keep response concise but complete.",
        "Detailed":       "Give a thorough detailed response."
    }
    styled_input = f"{user_input}\n\n[{length_map[response_length]}]"

    try:
        reply = get_response(styled_input, st.session_state.personality)
    except Exception as e:
        reply = f"⚠️ error: {str(e)}"

    time.sleep(0.5)
    loading.empty()

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.total_messages += 2
    show_message("bot", reply)
    st.rerun()