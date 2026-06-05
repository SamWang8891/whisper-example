import sys
import os
import subprocess
import tempfile
import openai
from dotenv import load_dotenv

load_dotenv()

# OpenAI's audio endpoint rejects files larger than 25 MiB.
MAX_BYTES = 25 * 1024 * 1024

def compress_audio(audio_path):
    """Re-encode to 16 kHz mono ~32 kbps mp3, which Whisper handles fine."""
    fd, tmp_path = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", audio_path,
            "-ac", "1", "-ar", "16000", "-b:a", "32k",
            tmp_path,
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return tmp_path

def transcribe_to_srt(audio_path, output_path):
    client = openai.OpenAI()  # uses OPENAI_API_KEY env var

    tmp_path = None
    if os.path.getsize(audio_path) > MAX_BYTES:
        print(f"{audio_path} exceeds 25 MB, compressing for upload...")
        tmp_path = compress_audio(audio_path)
        upload_path = tmp_path
        size_mb = os.path.getsize(tmp_path) / (1024 * 1024)
        print(f"Compressed to {size_mb:.1f} MB. Uploading and transcribing...")
    else:
        upload_path = audio_path
        print("Uploading and transcribing...")

    try:
        with open(upload_path, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                response_format="srt",
            )
    finally:
        if tmp_path:
            os.remove(tmp_path)

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