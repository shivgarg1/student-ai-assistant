# memory.py
# Handles saving and loading long term memory

import json
import os

# Memory file location — saves on your Mac permanently
MEMORY_FILE = "user_memory.json"


def load_memory():
    """Load saved memory from file."""
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    # Default empty memory
    return {
        "name":     None,
        "grade":    None,
        "subjects": [],
        "goals":    [],
        "mood_history": [],
        "facts":    []
    }


def save_memory(memory):
    """Save memory to file permanently."""
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)


def memory_to_text(memory):
    """
    Convert memory dict into a text summary
    that gets injected into AI's system prompt.
    """
    if not any([memory["name"], memory["subjects"], memory["facts"]]):
        return "No memory of this user yet."

    lines = ["Here is what you remember about this student:"]

    if memory["name"]:
        lines.append(f"- Name: {memory['name']}")
    if memory["grade"]:
        lines.append(f"- Grade/Class: {memory['grade']}")
    if memory["subjects"]:
        lines.append(f"- Subjects they study: {', '.join(memory['subjects'])}")
    if memory["goals"]:
        lines.append(f"- Their goals: {', '.join(memory['goals'])}")
    if memory["facts"]:
        lines.append(f"- Other facts: {', '.join(memory['facts'])}")
    if memory["mood_history"]:
        last_mood = memory["mood_history"][-1]
        lines.append(f"- Last known mood: {last_mood}")

    return "\n".join(lines)


def update_memory_from_chat(memory, user_input, ai_response):
    """
    Scans conversation for important facts and saves them.
    Simple keyword based extraction.
    """
    text = user_input.lower()

    # Extract name
    for phrase in ["my name is", "i am ", "call me "]:
        if phrase in text:
            part = text.split(phrase)[-1].strip()
            name = part.split()[0].capitalize()
            if len(name) > 1:
                memory["name"] = name

    # Extract grade
    for phrase in ["i study in", "i'm in", "i am in", "grade ", "class "]:
        if phrase in text:
            part = text.split(phrase)[-1].strip()
            grade = part.split()[0]
            memory["grade"] = grade

    # Extract subjects
    subjects = [
        "math", "physics", "chemistry", "biology",
        "history", "english", "science", "computer",
        "economics", "geography", "hindi", "french"
    ]
    for subject in subjects:
        if subject in text and subject not in memory["subjects"]:
            memory["subjects"].append(subject)

    # Extract goals
    for phrase in ["i want to", "my goal is", "i wish to", "i dream of"]:
        if phrase in text:
            part = text.split(phrase)[-1].strip()
            goal = part.split(".")[0][:60]  # max 60 chars
            if goal and goal not in memory["goals"]:
                memory["goals"].append(goal)

    # Save mood
    mood_words = {
        "stressed": "😟 stressed",
        "sad":      "😢 sad",
        "happy":    "😊 happy",
        "excited":  "🤩 excited",
        "tired":    "😴 tired",
        "anxious":  "😰 anxious"
    }
    for word, mood in mood_words.items():
        if word in text:
            memory["mood_history"].append(mood)
            # Keep only last 5 moods
            memory["mood_history"] = memory["mood_history"][-5:]

    # Save updated memory
    save_memory(memory)
    return memory