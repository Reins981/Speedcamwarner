import pyttsx3

engine = pyttsx3.init()

# List available voices
voices = engine.getProperty('voices')
for i, voice in enumerate(voices):
    print(f"{i}: {voice.name} | {voice.gender} | {voice.id}")

# Select a female voice (this might vary by platform)
# Common on Windows: use a name like "Zira"
# On macOS/Linux: pick a voice with female characteristics in the ID or name

# Example: Pick the first female voice found
female_voice = None
for voice in voices:
    if "female" in voice.name.lower() or "zira" in voice.name.lower():
        female_voice = voice
        break

# If no female voice is found, just pick the first available
if female_voice:
    engine.setProperty('voice', female_voice.id)
else:
    print("No female voice found, using default.")

# Set speaking rate (optional)
engine.setProperty('rate', 160)

# Speak something
engine.say("Hello! I hope you're having a great day.")
engine.runAndWait()
