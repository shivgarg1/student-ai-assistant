# emotion_model.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Training data
texts = [
    "i am happy", "feeling great", "this is awesome", "i am good",
    "i am sad", "feeling low", "very upset", "i feel bad",
    "i am stressed", "too much pressure", "i am tired", "so overwhelmed",
    "i am excited", "so thrilled", "cant wait", "feeling energetic"
]

labels = [
    "happy", "happy", "happy", "happy",
    "sad", "sad", "sad", "sad",
    "stressed", "stressed", "stressed", "stressed",
    "excited", "excited", "excited", "excited"
]

# Train the model
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

model = LogisticRegression()
model.fit(X, labels)

# This function is called by assistant.py
def predict_emotion(user_input):
    user_vector = vectorizer.transform([user_input])
    prediction = model.predict(user_vector)
    return prediction[0]