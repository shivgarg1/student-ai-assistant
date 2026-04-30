# app.py
import streamlit as st
import time
from assistant import get_response

# ── PAGE CONFIG ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="Student AI Assistant",
    page_icon="🎓",
    layout="centered",
)

# ── CUSTOM CSS ────────────────────────────────────────────────────────
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        * { font-family: 'Inter', sans-serif; }
        .stApp { background-color: transparent; }
        .welcome-box {
            background: linear-gradient(135deg, #4a90e2, #7b2ff7);
            border-radius: 20px;
            padding: 24px;
            text-align: center;
            color: white;
            margin-bottom: 20px;
        }
        .welcome-box h2 { font-size: 26px; margin: 0; }
        .welcome-box p  { font-size: 14px; opacity: 0.85; margin: 6px 0 0; }
        .stats-bar {
            display: flex;
            justify-content: space-around;
            background: linear-gradient(135deg, #1e1e2f, #2a2a4a);
            border-radius: 14px;
            padding: 14px;
            margin-bottom: 18px;
        }
        .stat-item { text-align: center; color: white; }
        .stat-number { font-size: 22px; font-weight: 700; color: #4a90e2; }
        .stat-label  { font-size: 11px; opacity: 0.7; margin-top: 2px; }
        .user-bubble {
            background: linear-gradient(135deg, #4a90e2, #7b2ff7);
            color: white;
            padding: 12px 18px;
            border-radius: 20px 20px 4px 20px;
            margin: 6px 0;
            max-width: 80%;
            float: right;
            clear: both;
            font-size: 15px;
            line-height: 1.5;
        }
        .bot-bubble {
            background: linear-gradient(135deg, #1e1e2f, #2a2a4a);
            color: white;
            padding: 12px 18px;
            border-radius: 20px 20px 20px 4px;
            margin: 6px 0;
            max-width: 80%;
            float: left;
            clear: both;
            font-size: 15px;
            line-height: 1.5;
        }
        .chat-row {
            display: flex;
            align-items: flex-end;
            margin: 10px 0;
            clear: both;
        }
        .chat-row.user-row { flex-direction: row-reverse; }
        .avatar {
            width: 36px; height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            flex-shrink: 0;
            margin: 0 8px;
        }
        .bot-avatar  { background: #4a90e2; }
        .user-avatar { background: #7b2ff7; }
        .loading-dots {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 12px 18px;
            background: linear-gradient(135deg, #1e1e2f, #2a2a4a);
            border-radius: 20px 20px 20px 4px;
            width: fit-content;
        }
        .dot {
            width: 8px; height: 8px;
            background: #4a90e2;
            border-radius: 50%;
            animation: bounce 1.2s infinite;
        }
        .dot:nth-child(2) { animation-delay: 0.2s; }
        .dot:nth-child(3) { animation-delay: 0.4s; }
        .stChatInput input {
            border-radius: 20px !important;
            border: 2px solid #4a90e2 !important;
        }
        /* ── Fix mic recorder button ── */
.stCustomComponentV1 {
    border-radius: 12px !important;
    border: 2px solid #4a90e2 !important;
    min-height: 50px !important;
}

iframe {
    border-radius: 12px !important;
    min-height: 55px !important;
    width: 100% !important;
}
        [data-testid="stSidebar"] { background-color: #1e1e2f; }
        [data-testid="stSidebar"] * { color: white !important; }
        [data-testid="stSidebar"] input { color: black !important; background-color: white !important; }
        [data-testid="stSidebar"] .stSelectbox div { color: black !important; }
        h1 { color: #4a90e2 !important; }
        @keyframes bounce {
            0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
            40%            { transform: scale(1.2); opacity: 1; }
        }
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
if "face_emotion"   not in st.session_state:
    st.session_state.face_emotion   = None


# ── SIDEBAR ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.markdown("---")

    assistant_name = st.text_input("🤖 Assistant Name", value="Aria")

    st.markdown("### 🎭 Personality Mode")
    personality = st.radio(
        "Choose how Aria talks to you:",
        ["😊 Friend", "💕 Companion", "🎓 Mentor", "📚 Strict Teacher"],
        index=0
    )
    descriptions = {
        "😊 Friend":         "Casual, fun, uses slang & memes 💀",
        "💕 Companion":      "Warm, sweet and emotionally supportive 🥺",
        "🎓 Mentor":         "Wise, thoughtful and inspiring 🌟",
        "📚 Strict Teacher": "Direct, no-nonsense, tough love 📖"
    }
    st.caption(descriptions[personality])
    st.session_state.personality = personality

    st.markdown("---")

    response_length = st.selectbox(
        "📏 Response Length",
        ["Short & Simple", "Medium", "Detailed"]
    )

    st.markdown("---")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages       = []
        st.session_state.total_messages = 0
        st.session_state.topics_asked   = 0
        st.session_state.mood           = "😊 Happy"
        st.rerun()

    st.markdown("---")
    st.markdown("### ⚡ Quick Prompts")
    if st.button("📚 Help me study"):
        st.session_state["quick_prompt"] = "Help me make a study plan"
    if st.button("💪 Motivate me"):
        st.session_state["quick_prompt"] = "I need some motivation right now"
    if st.button("😟 I'm stressed"):
        st.session_state["quick_prompt"] = "I'm really stressed about exams"
    if st.button("🧠 Quiz me"):
        st.session_state["quick_prompt"] = "Give me a quick quiz on any topic I study"

    st.markdown("---")
    st.caption("Built by Shiv 🚀")


# ── WELCOME BANNER ────────────────────────────────────────────────────
st.markdown(f"""
    <div class="welcome-box">
        <h2>🎓 {assistant_name} — Student AI Assistant</h2>
        <p>Powered by Llama 3 (Groq) · Personality: {personality} · Free & Fast ⚡</p>
    </div>
""", unsafe_allow_html=True)


# ── STATS BAR ─────────────────────────────────────────────────────────
st.markdown(f"""
    <div class="stats-bar">
        <div class="stat-item">
            <div class="stat-number">{st.session_state.total_messages}</div>
            <div class="stat-label">💬 Messages</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{st.session_state.topics_asked}</div>
            <div class="stat-label">📚 Topics Asked</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{st.session_state.mood}</div>
            <div class="stat-label">Current Mood</div>
        </div>
    </div>
""", unsafe_allow_html=True)


# ── SHOW MESSAGE FUNCTION ─────────────────────────────────────────────
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


# ── WELCOME MESSAGE ───────────────────────────────────────────────────
if not st.session_state.messages:
    from memory import load_memory
    mem = load_memory()
    if mem["name"]:
        welcome = f"Welcome back {mem['name']}! 👋 Great to see you again! How can I help you today?"
    else:
        welcome = f"Hey! 👋 I'm {assistant_name}. What's your name? I'll remember you! 🧠"
    show_message("bot", welcome)

# ── DISPLAY CHAT HISTORY ──────────────────────────────────────────────
for msg in st.session_state.messages:
    show_message(msg["role"], msg["content"])


# ── QUICK PROMPTS HANDLER ─────────────────────────────────────────────
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


# ── VOICE INPUT ───────────────────────────────────────────────────────
# ── VOICE INPUT SECTION ───────────────────────────────────────────────
st.markdown("---")
st.markdown("### 🎙️ Voice Input")
st.info("👇 Click the blue bar below → Speak → Click again to Stop!")

try:
    from streamlit_mic_recorder import mic_recorder

    # Browser based mic recorder
    audio = mic_recorder(
        start_prompt="🎙️ START Recording",
        stop_prompt="⏹️ STOP Recording",
        just_once=True,
        use_container_width=True,
        key="voice_recorder"
    )

    if audio and audio.get('bytes'):
        import tempfile, os
        from assistant import client
        from voice_helper import text_to_speech

        # Show audio playback so user can verify
        st.audio(audio['bytes'], format='audio/wav')

        # Save to temp file
        with tempfile.NamedTemporaryFile(
            delete=False, suffix='.wav'
        ) as tmp:
            tmp.write(audio['bytes'])
            tmp_path = tmp.name

        # Transcribe with Groq Whisper
        with st.spinner("🧠 Transcribing..."):
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
                st.error(f"Transcription error: {e}")
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)

        if spoken_text and spoken_text != ".":
            st.success(f"✅ You said: '{spoken_text}'")

            # Add to chat
            st.session_state.messages.append({
                "role": "user",
                "content": f"🎙️ {spoken_text}"
            })
            show_message("user", f"🎙️ {spoken_text}")

            # Get AI response
            with st.spinner("🧠 Thinking..."):
                reply = get_response(
                    spoken_text,
                    st.session_state.get("personality", "😊 Friend")
                )

            # Show response
            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })
            show_message("bot", reply)

            # Speak response
            st.markdown("#### 🔊 AI Voice Response")
            text_to_speech(reply)

            st.session_state.total_messages += 2
        else:
            st.warning("⚠️ Couldn't understand. Speak clearly and try again!")

except ImportError:
    st.error("⚠️ Voice module not installed. Run: pip install streamlit-mic-recorder")
except Exception as e:
    st.error(f"Voice error: {str(e)}")

# ── TEXT CHAT INPUT ───────────────────────────────────────────────────
user_input = st.chat_input(f"Message {assistant_name}...")

if user_input:
    # Detect mood
    mood_map = {
        "stressed": "😟 Stressed", "sad": "😢 Sad",
        "happy": "😊 Happy",      "excited": "🤩 Excited",
        "tired": "😴 Tired",      "confused": "😕 Confused",
    }
    for keyword, mood in mood_map.items():
        if keyword in user_input.lower():
            st.session_state.mood = mood
            break

    # Count topics
    study_keywords = ["explain", "what is", "how does", "teach", "help me", "study", "homework"]
    if any(k in user_input.lower() for k in study_keywords):
        st.session_state.topics_asked += 1

    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    show_message("user", user_input)

    # Loading dots
    loading = st.empty()
    loading.markdown("""
        <div class="chat-row">
            <div class="avatar bot-avatar">🤖</div>
            <div class="loading-dots">
                <div class="dot"></div><div class="dot"></div><div class="dot"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Build prompt
    length_map = {
        "Short & Simple": "Keep response under 3 sentences.",
        "Medium":         "Keep response concise but complete.",
        "Detailed":       "Give a thorough detailed response."
    }
    styled_input = f"{user_input}\n\n[{length_map[response_length]}]"

    # Get response
    try:
        reply = get_response(styled_input, st.session_state.personality)
    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"

    time.sleep(0.5)
    loading.empty()

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.total_messages += 2
    show_message("bot", reply)
    st.rerun()