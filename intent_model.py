# intent_model.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Training data
texts = [
    "hello", "hi", "hey", "good morning",
    "i want to study", "help me with math", "explain ai", "teach me",
    "i feel sad", "i am stressed", "feeling low", "so tired",
    "bye", "goodbye", "see you", "take care"
]

labels = [
    "greeting", "greeting", "greeting", "greeting",
    "study", "study", "study", "study",
    "emotion", "emotion", "emotion", "emotion",
    "bye", "bye", "bye", "bye"
]

# Train the model
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

model = LogisticRegression()
model.fit(X, labels)

# This function is called by assistant.py
def predict_intent(user_input):
    user_vector = vectorizer.transform([user_input])
    prediction = model.predict(user_vector)
    return prediction[0]