# voice_helper.py
import os
import tempfile
import base64
import streamlit as st
from gtts import gTTS


def text_to_speech(text):
    """
    Converts text to speech.
    Uses JavaScript trick to force autoplay in browser.
    """
    try:
        # Clean text — remove emojis
        clean_text = text.encode('ascii', 'ignore').decode('ascii').strip()

        if not clean_text:
            return

        # Generate speech
        tts = gTTS(text=clean_text, lang='en', slow=False)

        # Save to temp file
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        tts.save(tmp.name)

        # Read bytes
        with open(tmp.name, 'rb') as f:
            audio_bytes = f.read()

        # Convert to base64
        audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')

        # JavaScript trick to force autoplay
        # Works in Chrome, Safari, Firefox!
        autoplay_html = f"""
            <script>
                var audio = new Audio("data:audio/mp3;base64,{audio_b64}");
                audio.play().then(() => {{
                    console.log("Playing audio");
                }}).catch((e) => {{
                    console.log("Autoplay blocked:", e);
                }});
            </script>
            <audio controls>
                <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
            </audio>
            <p style="color: #4a90e2; font-size: 13px;">
                🔊 Click ▶️ to hear AI response
            </p>
        """
        st.markdown(autoplay_html, unsafe_allow_html=True)

        # Clean up
        os.unlink(tmp.name)

    except Exception as e:
        st.warning(f"Voice output error: {str(e)}")