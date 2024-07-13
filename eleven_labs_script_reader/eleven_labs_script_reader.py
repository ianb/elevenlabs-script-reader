from elevenlabs import Voice, VoiceSettings, save
from elevenlabs.client import ElevenLabs
from bs4 import BeautifulSoup
from pydub import AudioSegment
import toml
import sys
import os
import hashlib
import re

def parse_script(script):
    # Parse the script using BeautifulSoup
    soup = BeautifulSoup(script, 'html.parser')

    # Initialize an empty list to store the parsed content
    parsed_content = []

    # Extract background-sound tags
    for tag in soup.find_all(['background-sound', 'dialog', 'narrator']):
        if tag.name == 'background-sound':
          parsed_content.append({
              "type": "background-sound",
              "content": tag.get_text(strip=True)
          })
        elif tag.name == 'dialog':
          parsed_content.append({
              "type": "dialog",
              "name": tag.get('character', '').strip(),
              "content": tag.get_text(strip=True)
          })
        elif tag.name == 'narrator':
          parsed_content.append({
              "type": "narrator",
              "content": tag.get_text(strip=True)
          })
    return parsed_content

def parse_voices(voices_file):
    with open(voices_file, 'r') as f:
        voices_data = toml.load(f)
    return voices_data

def merge_voice_info(parsed_content, voices_data):
    for entry in parsed_content:
        if entry['type'] == 'background-sound':
            continue

        character_name = entry['name'] if entry['type'] == 'dialog' else 'narrator'

        if character_name not in voices_data:
            print(f"Error: Missing voice information for '{character_name}' (from {entry})")
            sys.exit(1)

        entry['voice'] = voices_data[character_name]

    return parsed_content

# Function to generate a hash from character name and text
def generate_hash(character_name, text):
    hash_input = f"{character_name}|{text}"
    return hashlib.md5(hash_input.encode()).hexdigest()

# Function to check if the audio file exists in the cache and generate if not
def get_or_generate_audio(client, entry, cache_dir):
    character_name = entry['name'] if entry['type'] == 'dialog' else 'narrator'
    text = entry['content']
    filename_slug = slugify(text[:10])
    hash_value = generate_hash(character_name, text)
    filename = f"{character_name}-{filename_slug}-{hash_value}.mp3"
    file_path = os.path.join(cache_dir, filename)

    if not os.path.exists(file_path):
        print(f"Generating audio for {character_name}: {text[:10]}...")
        voice_settings = entry['voice']
        audio = client.generate(
            text=text,
            voice=Voice(
                voice_id=voice_settings['voice_id'],
                settings=VoiceSettings(
                    stability=voice_settings.get('stability', 0.75),
                    similarity_boost=voice_settings.get('similarity_boost', 0.75),
                    style=voice_settings.get('style', 0.0),
                    use_speaker_boost=voice_settings.get('use_speaker_boost', True)
                )
            )
        )
        save(audio, file_path)
    else:
        print(f"Using cached audio for {character_name}: {text[:10]}")

    return file_path

# Main function to process the script and generate audio files
def process_script(script, voices_file, api_key, cache_dir):
    parsed_content = parse_script(script)
    voices_data = parse_voices(voices_file)
    merged_content = merge_voice_info(parsed_content, voices_data)

    client = ElevenLabs(api_key=api_key)
    os.makedirs(cache_dir, exist_ok=True)

    filenames = []
    for entry in merged_content:
        if entry['type'] != 'background-sound':
            filenames.append(get_or_generate_audio(client, entry, cache_dir))

    return filenames

# Function to concatenate audio files into one MP3
def concatenate_audio_files(filenames, output_filename):
    combined_audio = AudioSegment.empty()
    for filename in filenames:
        audio = AudioSegment.from_mp3(filename)
        combined_audio += audio
    combined_audio.export(output_filename, format="mp3")

def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Remove characters that
    aren't alphanumerics, underscores, or hyphens. Convert to lowercase.
    Also strip leading and trailing whitespace, and replace spaces with hyphens.
    """
    value = str(value)
    if allow_unicode:
        value = re.sub(r'[^\w\s-]', '', value).strip().lower()
        value = re.sub(r'[-\s]+', '-', value)
    else:
        value = re.sub(r'[^\w\s-]', '', value).strip().lower()
        value = re.sub(r'[-\s]+', '-', value)
    return value
