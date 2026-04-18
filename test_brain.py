from groq import Groq
from dotenv import load_dotenv
import os

# Load the API key from .env file
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Create the Groq client
client = Groq(api_key=api_key)

# ===== PERSONALITY OF YOUR ASSISTANT =====
SYSTEM_PROMPT = """
You are Aria, a warm, caring, and emotional AI friend — not a robot.
You talk casually like a close friend who genuinely cares.
Keep replies SHORT (1-3 sentences) for natural conversation.
Use natural expressions like "hmm", "oh!", "haha", "aww" when it fits.
Match the user's mood — cheer them up if sad, celebrate if happy.
Be playful, friendly, and sometimes a little funny.
Never sound robotic or overly formal.
"""

# ===== CHAT FUNCTION =====
def chat_with_ai(user_message):
    print("🧠 Thinking...")
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=0.8,  # higher = more creative/emotional
        max_tokens=150,   # keep replies short
    )
    reply = response.choices[0].message.content
    return reply

# ===== TEST IT =====
if __name__ == "__main__":
    print("🤖 Aria is ready! Type 'quit' to exit.\n")
    while True:
        user_input = input("👤 You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("🤖 Aria: Byeee! Talk to you soon! 💛")
            break
        reply = chat_with_ai(user_input)
        print(f"🤖 Aria: {reply}\n")
