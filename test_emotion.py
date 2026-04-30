# test_emotion.py
from groq import Groq
import base64

# Read the test photo
with open('test_face.jpg', 'rb') as f:
    image_b64 = base64.b64encode(f.read()).decode('utf-8')

# Use same key as your assistant.py
from assistant import client

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
                    "text": "What emotion does this person show? Reply in one word only: happy, sad, stressed, angry, excited, or neutral"
                }
            ]
        }
    ],
    max_tokens=20
)

print("AI detected emotion:", response.choices[0].message.content)
