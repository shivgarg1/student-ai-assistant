# voice_helper.py
import os
import tempfile
import time
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from groq import Groq
from gtts import gTTS
import streamlit as st

# Use same Groq client
import streamlit as st
import os
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Recording settings
SAMPLE_RATE = 16000   # 16kHz — best for Whisper
DURATION    = 6       # seconds to record


def record_audio():
    """
    Records audio from mic using sounddevice.
    Returns path to saved WAV file.
    """
    try:
        st.info("🎙️ Recording for 6 seconds... Speak now!")

        # Record audio
        audio_data = sd.rec(
            int(DURATION * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype='int16',
            device=2  # MacBook Pro Microphone
        )

        # Wait for recording to finish
        sd.wait()

        # Save to temp WAV file
        tmp = tempfile.NamedTemporaryFile(
            delete=False,
            suffix='.wav'
        )
        write(tmp.name, SAMPLE_RATE, audio_data)
        return tmp.name

    except Exception as e:
        print(f"Recording error: {e}")
        return None


def speech_to_text():
    """
    Records mic → sends to Groq Whisper API → returns text.
    Groq Whisper is extremely accurate and free!
    """
    # Record audio first
    audio_path = record_audio()

    if not audio_path:
        return None

    try:
        # Send to Groq Whisper API
        with open(audio_path, 'rb') as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-large-v3",  # Most accurate Whisper model
                file=audio_file,
                language="en"              # Change to "hi" for Hindi!
            )

        # Clean up temp file
        os.unlink(audio_path)

        return transcription.text

    except Exception as e:
        print(f"Whisper API error: {e}")
        if os.path.exists(audio_path):
            os.unlink(audio_path)
        return None


def text_to_speech(text):
    """
    Converts text to speech.
    Shows audio player in Streamlit — click play to hear!
    """
    try:
        # Remove emojis
        clean_text = text.encode('ascii', 'ignore').decode('ascii').strip()

        if not clean_text:
            return

        # Generate speech
        tts = gTTS(text=clean_text, lang='en', slow=False)

        # Save to temp file
        tmp = tempfile.NamedTemporaryFile(
            delete=False,
            suffix='.mp3'
        )
        tts.save(tmp.name)

        # Read bytes
        with open(tmp.name, 'rb') as f:
            audio_bytes = f.read()

        # Show player in Streamlit
        st.markdown("🔊 **AI Voice Response:**")
        st.audio(audio_bytes, format='audio/mp3')

        # Clean up
        os.unlink(tmp.name)

    except Exception as e:
        print(f"TTS error: {e}")