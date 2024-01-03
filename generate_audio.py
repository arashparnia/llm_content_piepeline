import json
from pydub import AudioSegment
import torch
from TTS.api import TTS
from tqdm import tqdm
import os

def convert_to_mp3(input_file, output_file):
    audio = AudioSegment.from_wav(input_file)
    audio.export(output_file, format="mp3")

def tts_synthesize(tts, text, output_path):
    tts.tts_to_file(text=text, speaker="Ana Florence", language="en", file_path=output_path)

def process_stories(json_file, mp3_folder="mp3"):
    # Create the mp3 folder if it doesn't exist
    if not os.path.exists(mp3_folder):
        os.makedirs(mp3_folder)

    # Load JSON file
    with open(json_file, 'r') as file:
        stories = json.load(file)

    # Initialize TTS model
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts_model = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

    # Process each story
    for story in tqdm(stories):
        mp3_file_path = os.path.join(mp3_folder, f"{story['moderation']['moderation_id']}.mp3")

        # Check if the MP3 file already exists
        if not os.path.isfile(mp3_file_path):
            wav_file_path = f"{story['moderation']['moderation_id']}.wav"

            # Generate WAV file using TTS
            tts_synthesize(tts_model, story['content'], wav_file_path)

            # Convert WAV to MP3
            convert_to_mp3(wav_file_path, mp3_file_path)

# Call the function with the path to your JSON file
process_stories("../../mojo/children_stories_final_moderated.json")
