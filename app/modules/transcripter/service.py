import subprocess, sys, os, json
from datetime import datetime, timedelta
from vosk import Model, KaldiRecognizer
import pprint
import argparse
from typing import Dict

# init config
SAMPLE_RATE = 16000
CHUNK_SIZE = 4000

class Transcriber():
    def __init__(self, model_path):
        self.model = Model(model_path)

    def fmt(self, data):
        data = json.loads(data)

        start = min(r["start"] for r in data.get("result", [{ "start": 0 }]))
        end = max(r["end"] for r in data.get("result", [{ "end": 0 }]))

        return {
            "start": str(timedelta(seconds=start)), 
            "end": str(timedelta(seconds=end)), 
            "text": data["text"]
        }

    def transcribe(self, filename):
        rec = KaldiRecognizer(self.model, SAMPLE_RATE)
        rec.SetWords(True)

        if not os.path.exists(filename):
            raise FileNotFoundError(filename)

        transcription = []

        ffmpeg_command = [
                "ffmpeg",
                "-nostdin",
                "-loglevel",
                "quiet",
                "-i",
                filename,
                "-ar",
                str(SAMPLE_RATE),
                "-ac",
                "1",
                "-f",
                "s16le",
                "-",
            ]

        with subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE) as process:

            start_time = datetime.now() 
            while True:
                data = process.stdout.read(4000)
                if len(data) == 0:
                    break
                
                if rec.AcceptWaveform(data):
                    transcription.append(self.fmt(rec.Result()))

            transcription.append(self.fmt(rec.FinalResult()))
            end_time = datetime.now()

            time_elapsed = end_time - start_time
            print(f"Time elapsed  {time_elapsed}")

        return {
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "elapsed_time": time_elapsed,
            "transcription": transcription,
        }

def transcribe_audio(filename: str, model_path: str):
    print(f"[transcriptor.service] filename={filename}, model={model_path}")
    transcriber = Transcriber(model_path)
    transcription = transcriber.transcribe(filename)
    # pprint.pprint(transcription.get("transcription"))

    print(f"[transcriptor.service] filename={filename}, model={model_path}")
    return {
        "status": True, 
        "filename": filename, 
        "model": model_path,
        "transcription": format_transcription(transcription.get("transcription"))
    }


def format_transcription(transcriptions: list[dict], start_index: int = 0, end_index: int = None) -> Dict:
    sliced = transcriptions[start_index:end_index]
    combined_text = ' '.join(item['text'] for item in sliced)
    
    return {
        'start': sliced[0]['start'] if sliced else None,
        'end': sliced[-1]['end'] if sliced else None,
        'text': combined_text
    }


# # vosk-model-es-0.42
# filename = "midudev1.mp3"
# model_path = "vosk-model-es-0.42"

# transcribe_audio(filename, model_path)

