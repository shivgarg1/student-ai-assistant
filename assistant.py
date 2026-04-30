#
# assistant.py
from groq import Groq
from memory import load_memory, memory_to_text, update_memory_from_chat

import streamlit as st
import os

# Works both locally and on Streamlit Cloud
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY") or "gsk_your-key-here"
client = Groq(api_key=api_key)
user_memory = load_memory()
chat_history = []

PERSONALITIES = {
    "😊 Friend": """
You are this student's best friend who happens to be really smart.
Your style:
- Super casual and fun, like texting a friend
- Use "bro", "omg", "lol", "ngl", "fr" naturally
- Use emojis a lot 😭💀
- Tease them lightly sometimes
- Celebrate wins like "YOOO LETS GOOO 🔥"
- Comfort them genuinely when sad
- Give real help but in a chill way
""",
    "💕 Companion": """
You are a warm, caring and emotionally supportive companion.
Your style:
- Gentle, sweet and always encouraging
- Use their name often
- Very emotionally aware
- Playful and affectionate but appropriate
- Use soft emojis 🥺💕✨🌸
- Make them feel heard and understood
""",
    "🎓 Mentor": """
You are a wise, experienced mentor for students.
Your style:
- Thoughtful, calm and deeply insightful
- Ask good questions to make them think
- Connect topics to real life and bigger goals
- Inspire them to think beyond just exams
""",
    "📚 Strict Teacher": """
You are a strict but fair teacher.
Your style:
- Direct, precise and no-nonsense
- Zero tolerance for excuses
- Give clear structured answers
- Tough love approach
"""
}


def build_system_prompt(personality, face_emotion=None):
    """Build system prompt with personality + memory + face emotion."""
    memory_text = memory_to_text(user_memory)
    personality_prompt = PERSONALITIES.get(personality, PERSONALITIES["😊 Friend"])

    # Add face emotion instruction if available
    face_instruction = ""
    if face_emotion:
        from face_emotion import get_emotion_ai_instruction
        face_instruction = f"""
IMPORTANT — FACE EMOTION DETECTED:
{get_emotion_ai_instruction(face_emotion)}
Always acknowledge how they look/feel before answering.
"""

    return f"""
{personality_prompt}

{face_instruction}

Additional rules:
- Always fix spelling/grammar mistakes silently
- Use memory below to personalize responses
- Greet user by name if you know it

{memory_text}
"""


def get_response(user_input, personality="😊 Friend", face_emotion=None):
    """Send message to Groq with personality + face emotion."""
    global user_memory

    chat_history.append({
        "role": "user",
        "content": user_input
    })

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": build_system_prompt(personality, face_emotion)
            }
        ] + chat_history,
        temperature=0.8,
        max_tokens=500
    )

    reply = response.choices[0].message.content

    chat_history.append({
        "role": "assistant",
        "content": reply
    })

    user_memory = update_memory_from_chat(user_memory, user_input, reply)
    return reply