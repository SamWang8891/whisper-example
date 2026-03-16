# Whisper Example

Example usage of OpenAI whisper, online and local.

## Files
- local.py -> Run locally
- online.py -> Run using OpenAI API (cost $)

## Usage
1. Init python env using uv
2. Copy .env.example to .env and put in your API key if you want to use online mode.
3. uv run <local.py or online.py> <file.mp3>
4. Wait for it to complete. It generates .srt file.
