import edge_tts
import asyncio
import pygame
import os

# Step 1: What you want the assistant to say
TEXT = "Hello! I am your personal voice assistant. Nice to finally meet you!"

# Step 2: Choose a voice (this one sounds warm and friendly)
VOICE = "en-US-AriaNeural"

# Step 3: Output file name
OUTPUT_FILE = "output.mp3"

# Function that converts text to speech and saves it as mp3
async def speak():
    print("🎙️  Generating voice...")
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save(OUTPUT_FILE)
    print("✅ Voice file saved!")

# Function that plays the mp3 file
def play_audio():
    print("🔊 Playing audio...")
    pygame.mixer.init()
    pygame.mixer.music.load(OUTPUT_FILE)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()
    print("🎉 Done!")

# Run everything
if __name__ == "__main__":
    asyncio.run(speak())
    play_audio()
