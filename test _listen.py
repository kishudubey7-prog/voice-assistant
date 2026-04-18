import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
import os

# ===== SETTINGS =====
DURATION = 5              # How many seconds to record
SAMPLE_RATE = 16000       # Audio quality (16kHz is perfect for speech)
AUDIO_FILE = "my_voice.wav"
MODEL_SIZE = "base"       # Options: tiny, base, small, medium, large

# ===== STEP 1: Record from microphone =====
def record_audio():
    print(f"\n🎤 Recording for {DURATION} seconds... SPEAK NOW!")
    audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
    sd.wait()  # wait until recording is done
    write(AUDIO_FILE, SAMPLE_RATE, audio)
    print("✅ Recording saved!")

# ===== STEP 2: Convert speech to text =====
def transcribe_audio():
    print("🧠 Loading Whisper model (first time may take 1-2 min to download)...")
    model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
    
    print("📝 Transcribing your voice...")
    segments, info = model.transcribe(AUDIO_FILE, beam_size=5)
    
    print(f"\n🌍 Detected language: {info.language} (confidence: {info.language_probability:.2f})")
    print("─" * 50)
    full_text = ""
    for segment in segments:
        full_text += segment.text + " "
    print(f"📢 YOU SAID: {full_text.strip()}")
    print("─" * 50)
    return full_text.strip()

# ===== RUN =====
if __name__ == "__main__":
    record_audio()
    text = transcribe_audio()
