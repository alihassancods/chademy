from django.shortcuts import render
import subprocess
import os
import assemblyai as aai
import dotenv
# Create your views here.


def transcribe(video_path, audio_path):
    try:
        subprocess.run([
            'ffmpeg', '-y', '-i', video_path, '-vn', '-c:a',
            'libmp3lame', '-f', 'mp3', audio_path
        ], check=True, capture_output=True, text=True)
    except Exception as e:
        return "Error converting video to audio"

    # Transcribe audio with AssemblyAI
    dotenv.load_dotenv()
    aai.settings.api_key = os.getenv("ASSEMBLY_API_KEY")
    transcriber = aai.Transcriber()
    try:
        transcript_obj = transcriber.transcribe(audio_path)
        transcript_text = transcript_obj.text
        return transcript_text
    except Exception as e:
        return "Error"
