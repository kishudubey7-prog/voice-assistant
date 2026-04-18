import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
from groq import Groq
from dotenv import load_dotenv
import edge_tts
import asyncio
import pygame
import os
import sys
import time

# ===== LOAD API KEY =====
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ===== SETTINGS =====
DURATION = 5
SAMPLE_RATE = 16000
AUDIO_INPUT = "user_voice.wav"
AUDIO_OUTPUT = "aria_reply.mp3"
VOICE = "en-US-AriaNeural"
WHISPER_MODEL = "base"

# ===== ARIA'S PERSONALITY =====
SYSTEM_PROMPT = """
You are Aria, a warm, caring, and emotional AI friend — not a robot.
You talk casually like a close friend who genuinely cares.
Keep replies SHORT (1-2 sentences) for natural voice conversation.
Use natural expressions like "hmm", "oh!", "haha", "aww" when it fits.
Match the user's mood — cheer them up if sad, celebrate if happy.
Be playful, friendly, and sometimes a little funny.
Never use emojis or special characters (this will be spoken out loud).
"""

conversation_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

# Load Whisper model once
print("⏳ Loading Whisper model...")
whisper_model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")
print("✅ Whisper ready!\n")


# ===== 1. LISTEN =====
def listen():
    print(f"🎤 Listening... (speak now, {DURATION} seconds)")
    audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
    sd.wait()
    write(AUDIO_INPUT, SAMPLE_RATE, audio)
    segments, _ = whisper_model.transcribe(AUDIO_INPUT, beam_size=5)
    text = " ".join([seg.text for seg in segments]).strip()
    return text


# ===== 2. THINK =====
def think(user_text):
    conversation_history.append({"role": "user", "content": user_text})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=conversation_history,
        temperature=0.8,
        max_tokens=150,
    )
    reply = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": reply})
    return reply


# ===== 3. SPEAK =====
async def speak_async(text):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(AUDIO_OUTPUT)

def speak(text):
    asyncio.run(speak_async(text))
    pygame.mixer.init()
    pygame.mixer.music.load(AUDIO_OUTPUT)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    # ✅ FIX: Properly stop & unload audio so file is released
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    pygame.mixer.quit()


# ===== CLEAN EXIT HELPER =====
def clean_exit(message="Goodbye!"):
    """Properly closes everything and exits the program."""
    print(f"\n🤖 Aria: {message}")
    try:
        speak(message)
    except Exception:
        pass
    
    # Small delay so audio finishes
    time.sleep(0.5)
    
    # Force close all resources
    try:
        pygame.quit()
    except Exception:
        pass
    
    print("\n👋 Aria is now offline. See you soon!\n")
    sys.exit(0)  # ✅ FORCE EXIT


# ===== MAIN LOOP =====
def main():
    print("=" * 50)
    print("💛 ARIA VOICE ASSISTANT — Say 'goodbye' or press Ctrl+C to exit")
    print("=" * 50)
    
    greeting = "Hey there! I'm Aria. Press enter whenever you want to talk to me!"
    print(f"\n🤖 Aria: {greeting}")
    speak(greeting)
    
    while True:
        try:
            input("\n⏎ Press ENTER to speak (or type 'q' + ENTER to quit)...").strip().lower()
            
            # Optional: quit by typing 'q'
            # (uncomment next 2 lines if you want this feature)
            # if user_input == "q":
            #     clean_exit("Okay, shutting down. Bye!")
            
            user_text = listen()
            
            if not user_text or len(user_text) < 2:
                print("🤷 (didn't catch that, try again)")
                continue
            
            print(f"👤 You: {user_text}")
            
            # ✅ Better exit detection
            exit_phrases = ["goodbye", "bye aria", "bye bye", "see you later", "exit", "quit", "shut down", "turn off"]
            if any(phrase in user_text.lower() for phrase in exit_phrases):
                clean_exit("Aww, talk to you soon! Bye!")
            
            print("🧠 Thinking...")
            reply = think(user_text)
            print(f"🤖 Aria: {reply}")
            speak(reply)
            
        except KeyboardInterrupt:
            clean_exit("Shutting down. Bye!")
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
