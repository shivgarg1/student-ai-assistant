# face_emotion.py
import cv2
import time
import base64
import numpy as np
from groq import Groq

st.secrets.get("GROQ_API_KEY")


def capture_face():
    """Captures photo from Mac webcam and returns it."""
    try:
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            return None

        # Warm up camera properly
        for _ in range(10):
            cap.read()

        time.sleep(0.5)
        ret, frame = cap.read()
        cap.release()

        if not ret or frame is None:
            return None

        return frame

    except Exception as e:
        print(f"Capture error: {e}")
        return None


def frame_to_base64(frame):
    """Convert OpenCV frame to base64 string for API."""
    _, buffer = cv2.imencode('.jpg', frame)
    return base64.b64encode(buffer).decode('utf-8')


def detect_emotion_with_ai(frame):
    """You are an expert emotion detector.
    Look very carefully at this person's facial expression.
    Check their:
    - Eyes (wide = excited/surprised, droopy = sad/tired)
    - Mouth (smile = happy, frown = sad, tight = stressed)
    - Eyebrows (raised = surprised, furrowed = angry/stressed)
    - Overall face tension

    Based on what you see, pick the BEST matching emotion.
    Reply with ONLY one word, no punctuation:
    happy
    sad
    stressed
    angry
    excited
    neutral

    One word only."""
    try:
        # Convert frame to base64
        image_b64 = frame_to_base64(frame)

        # Send to Groq vision model
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_b64}"
                            }
                        },
                        {
                            "type": "text",
                            "text": """Look at this person's face carefully.
Detect their emotion from their facial expression.
Reply with ONLY one word from this list:
happy, sad, stressed, angry, excited, neutral

Just one word. Nothing else."""
                        }
                    ]
                }
            ],
            max_tokens=10
        )

        emotion_raw = response.choices[0].message.content.strip().lower()

        # Map to our emoji labels
        emotion_map = {
            "happy":    "😊 happy",
            "sad":      "😢 sad",
            "angry":    "😠 angry",
            "stressed": "😟 stressed",
            "excited":  "🤩 excited",
            "neutral":  "😐 neutral"
        }

        return emotion_map.get(emotion_raw, "😐 neutral")

    except Exception as e:
        print(f"AI emotion error: {e}")
        return "😐 neutral"


def capture_and_detect():
    """
    Main function — captures face + detects emotion with AI.
    Returns emotion label and frame for display.
    """
    # Capture frame
    frame = capture_face()

    if frame is None:
        return "😐 neutral", None

    # Detect emotion using AI
    emotion = detect_emotion_with_ai(frame)

    # Draw emotion on frame
    cv2.putText(
        frame,
        emotion,
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1, (0, 255, 0), 2
    )

    # Convert to RGB for Streamlit
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    return emotion, frame_rgb


def get_emotion_ai_instruction(emotion):
    """Returns AI instruction based on detected face emotion."""
    instructions = {
        "😊 happy":    "Student looks HAPPY. Be fun and enthusiastic! Match their energy!",
        "😢 sad":      "Student looks SAD. Be very gentle and supportive. Acknowledge feelings first.",
        "😠 angry":    "Student looks ANGRY. Stay extremely calm and patient.",
        "😟 stressed": "Student looks STRESSED. Be reassuring and calming. Take it slow.",
        "🤩 excited":  "Student looks EXCITED. Match their enthusiasm and energy!",
        "😐 neutral":  "Student looks calm and neutral. Respond naturally and helpfully."
    }
    return instructions.get(emotion, "Respond helpfully.")