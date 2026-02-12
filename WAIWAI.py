import subprocess
import requests
import sounddevice as sd
import numpy as np
import keyboard
import wavio
import json
import re
import sys
import warnings
import whisper
import os
import atexit
import signal


# ======================
# Privacy: Temp Files
# ======================
TEMP_FILES = [
    "temp.wav",
    "response.wav",
]


def cleanup_files():
    print("\n[🧹] Cleaning up temporary files...")
    for file in TEMP_FILES:
        try:
            if os.path.exists(file):
                os.remove(file)
                print(f"[✓] Deleted: {file}")
        except Exception as e:
            print(f"[!] Failed to delete {file}: {e}")


atexit.register(cleanup_files)


def handle_exit(sig, frame):
    print("\n[✖] Exit signal received.")
    cleanup_files()
    sys.exit(0)


signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)


# ======================
# System Health Checks
# ======================
def check_whisper():
    try:
        whisper.load_model("base")
        return True
    except Exception:
        return False


def check_ollama():
    try:
        res = requests.get("http://localhost:11434/api/tags", timeout=2)
        return res.status_code == 200
    except requests.exceptions.RequestException:
        return False


def check_voicevox():
    try:
        res = requests.get("http://localhost:50021/speakers", timeout=2)
        return res.status_code == 200
    except requests.exceptions.RequestException:
        return False


# ======================
# Terminal UI
# ======================
def show_banner():
    print("=" * 50)
    print("=== WAIWAI Japanese Speaking Tutor System ===")

    whisper_ok = check_whisper()
    ollama_ok = check_ollama()
    voicevox_ok = check_voicevox()

    print("System Status:")
    print(f"- Whisper Model   : {'Loaded' if whisper_ok else 'FAILED'} (base)")
    print(f"- Ollama Server   : {'Running' if ollama_ok else 'OFFLINE'} (localhost:11434)")
    print(f"- VoiceVox Engine : {'Active' if voicevox_ok else 'OFFLINE'} (localhost:50021)")

    if not (whisper_ok and ollama_ok and voicevox_ok):
        print("\n[!] One or more services are not ready.")
        print("[!] Please fix the issue and restart the program.")
    else:
        print("\nAll systems operational.")

    print("\nPress [SPACE] to start/stop recording")
    print("Press [ESC] to exit program")
    print("> Ready for Japanese conversation...")
    print("=" * 50 + "\n")

    return whisper_ok and ollama_ok and voicevox_ok


# ======================
# Audio Recording
# ======================
def record_audio(filename="temp.wav", samplerate=16000):
    print("[🎙️] Waiting for voice input...")
    while True:
        if keyboard.is_pressed("space"):
            print("[🎙️] Recording... (press SPACE again to stop)")
            frames = []

            def callback(indata, frames_count, time, status):
                frames.append(indata.copy())

            with sd.InputStream(samplerate=samplerate, channels=1, callback=callback):
                keyboard.wait("space")

            print("[🎙️] Recording stopped.")
            audio_data = np.concatenate(frames, axis=0)
            wavio.write(filename, audio_data, samplerate, sampwidth=2)
            print(f"[💾] Audio saved as: {filename}\n")
            break

        if keyboard.is_pressed("esc"):
            print("\n[✖] Program terminated by user.")
            cleanup_files()
            sys.exit()


# ======================
# Whisper Transcription
# ======================
warnings.filterwarnings("ignore", message="pkg_resources is deprecated")


def transcribe_with_whisper():
    print("[🧠] Transcribing audio with Whisper...")
    model = whisper.load_model("base")
    result = model.transcribe("temp.wav")
    return result["text"]


# ======================
# Ollama LLM Query
# ======================
def query_llm(text):
    print("[💬] WaiWai is thinking...", end="", flush=True)

    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "gemma3:4b",
        "system": (
            "You are an AI Japanese language tutor named わいわい (WAIWAI)."
            "You help users practice Japanese conversation."
            "Always use polite Japanese (です・ます form)."
            "Maximum 6 to 7 Japanese sentences."
            "Each sentence format:"
            "[Japanese] / [Romaji] (English translation)."
            "Do not add explanations outside the format."
            
           "Example response format (MUST follow exactly, and also make sure EACH SENTENCES HAVE SEPARATED like this):"
           "こんにちは！ / Konnichiwa! (Hello!)"
           "今日は日本語を勉強しましょう。 / Kyō wa Nihongo o benkyō shimashō. (Let’s study Japanese today.)"
           "今どんなことを話したいですか？ / Ima donna koto o hanashitai desu ka? (What would you like to talk about?)"
        ),
        "prompt": text,
        "stream": True
    }        

    with requests.post(url, json=payload, stream=True) as res:
        response_text = ""
        for line in res.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    if "response" in data:
                        response_text += data["response"]
                except json.JSONDecodeError:
                    continue

    print(" done.\n")
    return response_text.strip() if response_text else "No response from model."


# ======================
# Japanese Text Extraction
# ======================
def extract_japanese_sentences(text):
    sentences = re.findall(r"[ぁ-んァ-ン一-龯ー、。！？「」『』]+", text)
    return [s.strip() for s in sentences if len(s.strip()) > 2]


# ======================
# VoiceVox TTS
# ======================
def speak_with_voicevox(text, speaker=66):
    print("[🔊] Speaking response...")
    params = {"text": text, "speaker": speaker}

    audio_query = requests.post(
        "http://localhost:50021/audio_query",
        params=params
    )

    synthesis = requests.post(
        "http://localhost:50021/synthesis",
        params=params,
        data=audio_query.text
    )

    with open("response.wav", "wb") as f:
        f.write(synthesis.content)

    subprocess.run(["start", "response.wav"], shell=True)
    print()


# ======================
# Main Loop
# ======================
def main():
    system_ready = show_banner()

    if not system_ready:
        print("System not ready. Exiting...")
        sys.exit()

    while True:
        record_audio()

        user_text = transcribe_with_whisper()
        print("👤 User:")
        print(user_text + "\n")

        reply = query_llm(user_text)

        print("🤖 WaiWai:")
        print(reply + "\n")

        jp_sentences = extract_japanese_sentences(reply)
        final_text = " ".join(jp_sentences)

        speak_with_voicevox(final_text)

if __name__ == "__main__":
    main()