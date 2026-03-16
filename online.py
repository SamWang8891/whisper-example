import sys
import os
import openai
from dotenv import load_dotenv

load_dotenv()

def transcribe_to_srt(audio_path, output_path):
    client = openai.OpenAI()  # uses OPENAI_API_KEY env var

    with open(audio_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="srt",
        )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(transcript)

    print(f"SRT saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: online.py <audio_file>")
        sys.exit(1)
    audio_path = sys.argv[1]
    output_path = os.path.splitext(audio_path)[0] + ".srt"
    transcribe_to_srt(audio_path, output_path)