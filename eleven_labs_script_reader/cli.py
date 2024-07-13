"""Console script for eleven_labs_script_reader."""
from dotenv import load_dotenv
import sys
import os
import click
from .eleven_labs_script_reader import process_script, concatenate_audio_files

load_dotenv()

@click.command()
@click.argument('scripts', nargs=-1, type=click.Path(exists=True))
@click.option('--voices-file', default='voices.toml', type=click.Path(exists=True), help='Path to the voices.toml file.')
@click.option('--cache-dir', default='cache', type=click.Path(), help='Directory for cached audio files.')
@click.option('--api-key', default=lambda: os.environ.get('ELEVENLABS_API_KEY', ''), help='ElevenLabs API key, defaults to ELEVENLABS_API_KEY environment variable.')
def main(scripts, voices_file, cache_dir, api_key):
    """Console script for eleven_labs_script_reader."""
    if not scripts:
        click.echo("No script files provided. Please specify one or more script files.")
        sys.exit(1)

    for script_path in scripts:
        script_filename = os.path.basename(script_path)
        script_name, _ = os.path.splitext(script_filename)
        output_filename = f"{script_name}.mp3"

        with open(script_path, 'r') as script_file:
            script_content = script_file.read()

        click.echo(f"Processing {script_filename}...")

        # Process the script and generate audio files
        filenames = process_script(script_content, voices_file, api_key, cache_dir)

        # Concatenate the audio files into one MP3
        concatenate_audio_files(filenames, output_filename)

        click.echo(f"Combined audio saved as {output_filename}")

    return 0

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
