<h1 align=center> WAIWAI </h1>
<p align="center"> <i>Your personal Japanese conversation tutor, running 100% locally!</i> </p>
<p align="center"> 
<p align="center">
  <a href="https://docs.google.com/document/d/1MTFCYoW7yhwXDfWpgVE0lIhTGQqQ33ID/edit">
    <img src="https://img.shields.io/badge/Paper-GDocs-blue.svg">
  </a>
  <a href="https://github.com/openai/whisper">
    <img src="https://img.shields.io/badge/STT-Whisper-orange.svg">
  </a>
  <a href="https://ollama.com/library/gemma3">
    <img src="https://img.shields.io/badge/LLM-Gemma3%3A4B-orange.svg">
  </a>
  <a href="https://voicevox.hiroshiba.jp/">
    <img src="https://img.shields.io/badge/TTS-VOICEVOX-orange.svg">
  </a>
  <a href="https://github.com/aLeapz/waiwai">
    <img src="https://img.shields.io/badge/Status-Proof%20of%20Concept-brightgreen.svg">
  </a>
</p>


# The system integrates:
- 🎙 OpenAI Whisper (Speech-to-Text)
- 🧠 Ollama (Gemma 3 4B LLM)
- 🔊 VoiceVox (Japanese Text-to-Speech via Docker)
- 🖥 Terminal-based UI
- 🔐 Automatic temporary file cleanup (privacy-focused)
-----------------------------------------------------------------------------
# Demo Video:
[![Demo WAIWAI](https://img.youtube.com/vi/dY4P1IYFA0M/maxresdefault.jpg)](https://www.youtube.com/watch?v=dY4P1IYFA0M)
- Click the image above to watch the demo
    - PS: go to 12:01 if you don't want to hear me yap, YES i yap for 12 minutes
-----------------------------------------------------------------------------
# 🖥️ System Requirements
## Minimum Hardware (Tested)
- CPU	Intel Core i3-10105F (or equivalent)	4 cores, 8 threads
- GPU	NVIDIA GTX 1650 4GB	Required for Gemma 3:4B
- RAM	16GB DDR4	(already minimum)
- Storage	20GB free space	For models + dependencies
- Audio	Microphone (USB recommended)	16kHz sampling rate
## Software Requirements
- Windows	10/11	Tested on Windows only
- Python	3.9.9	| 3.11+ may have compatibility issues
- CUDA	11.6	Must match PyTorch version
- Docker	24.0+	For VoiceVox Engine
- Ollama	Latest	For running Gemma 3:4B
-----------------------------------------------------------------------------
# 🔧 Installation
## Step 1: Install Whisper 
https://github.com/openai/whisper
just follow along this video https://www.youtube.com/watch?v=ABFqbY_rmEk
## Step 2: Install Docker Desktop
Download from:
https://www.docker.com/products/docker-desktop/
and enable WSL2 integration if on Windows
### VoiceVox Engine (Docker)
Pull & Run CPU Version
```bash
docker pull voicevox/voicevox_engine:cpu-latest
docker run --rm -it -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:cpu-latest
```
Pull & Run GPU Version
```bash
docker pull voicevox/voicevox_engine:nvidia-latest
docker run --rm --gpus all -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:nvidia-latest
```
### Keep Docker Running
- Docker container should stay running in a separate terminal
- Keep it open while using WAIWAI
- Press Ctrl+C to stop after you're done
## Step 3: Install Ollama
Download from:
https://ollama.com/download
### Pull Gemma 3:4B Model
```bash 
ollama pull gemma3:4b
```
Wait for download (~3.3GB)
## Step 4: Clone Repository
```bash
git clone https://github.com/aLeapz/waiwai.git
```
go to waiwai directory 
```bash
cd waiwai
```
## Step 5: Install Python Dependencies
```bash
pip install -r requirements.txt
```
-----------------------------------------------------------------------------

# 🚀 Quick Start
## 1. Start All Services
### 1 - Run Ollama:
```bash
ollama serve
```
Should show: Listening on 127.0.0.1:11434
### 2 - Run Docker Desktop then Run VoiceVox:
- CPU
```bash
docker run --rm -it -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:cpu-latest
```
- GPU
```bash
docker run --rm --gpus all -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:nvidia-latest
```
Should show: Starting server on 0.0.0.0:50021
### 3- Run WAIWAI.py
## 2. Start Conversing!

```bash
==================================================
=== WAIWAI Japanese Tutor System ===
System Status:
- Whisper Model   : Loaded (base)
- Ollama Server   : Running (localhost:11434)
- VoiceVox Engine : Active (localhost:50021)

All systems operational.

Press [SPACE] to start/stop recording
Press [ESC] to exit program
> Ready for Japanese conversation...
==================================================
```
-----------------------------------------------------------------------------
# 🎮 How to Use
- SPACE:	Start recording → Speak → Press SPACE again to stop
- ESC:	Exit program (auto-cleanup)
- Ctrl+C:	Force exit (auto-cleanup)
-----------------------------------------------------------------------------
# Conversation Flow
- Press SPACE → "Recording..." appears
- Speak Japanese (e.g., "こんにちは")
- Press SPACE again → Recording stops
- Wait 15-20 seconds → WAIWAI processes
- Hear response → WAIWAI speaks back!
- Repeat → Continue conversation
-----------------------------------------------------------------------------
# 🧠 How It Works
System Architecture
- <img src="https://drive.google.com/uc?export=view&id=1RPlhcluAkt7mvUgqUSqKr0BQI7vw0iJZ" width="400">
-----------------------------------------------------------------------------
# Automatic File Cleanup
python
TEMP_FILES = [
    "temp.wav",     # Your voice recording
    "response.wav", # AI voice response
]
## Cleanup Triggers
- ✅ Normal exit - Program closes normally
- ✅ Ctrl+C - User interrupts
- ✅ ESC key - User exits
- ✅ System shutdown - SIGTERM handled
No files left behind. Ever.
-----------------------------------------------------------------------------
# 🔒 Privacy & Security
Your Data Stays With You.
- ✅ No cloud - Everything runs locally.
- ✅ No tracking - No analytics, no telemetry.
- ✅ No retention - Files deleted automatically
-----------------------------------------------------------------------------
# 🐛 Troubleshooting
## Common Issues & Solutions
❌ "Ollama server is OFFLINE"
### Solution:
restart Ollama from system tray.
or 
Start Ollama service.
```bash
ollama serve
```
---
❌ "VoiceVox Engine is OFFLINE"
### Solution:
- Make sure Docker is running
- If not running, start docker and start the container again
  - CPU
    ```bash
    docker run --rm -it -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:cpu-latest
    ```
  - GPU
    ```bash
    docker run --rm --gpus all -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:nvidia-latest
    ```
---
❌ "Whisper is FAILED"
### Solution:
- try to reinstall whisper
---
❌ "Program crashes on startup"
### Solution:
- Verify Python version: python --version (must be below version 3.11.x)
- Check requirements.txt installation
- Check all troubleshooting above
-----------------------------------------------------------------------------
# License
## This is just a project for proof of concept on my paper, everyone can use this project as it is or change the code or whatever, i don't mind it as long as you use it by following each terms of service
-----------------------------------------------------------------------------
# Credits
- **Whisper** by OpenAI
- **Gemma3** by Google
- **VoiceVox:** Mochiko (cv Asuha Yomogi)
- **Nama & NIM:** Muhammad Alif Rido (230401010006)
