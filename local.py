import sys
import os
import whisper

model = "large" # Options: tiny base small medium large

def format_timestamp(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def transcribe_to_srt(audio_path, output_path, model_name=model):
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_path)

    with open(output_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(result["segments"], start=1):
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = segment["text"].strip()
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")

    print(f"SRT saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: local.py <audio_file>")
        sys.exit(1)
    audio_path = sys.argv[1]
    output_path = os.path.splitext(audio_path)[0] + ".srt"
    transcribe_to_srt(audio_path, output_path)
