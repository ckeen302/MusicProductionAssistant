from pydub import AudioSegment


def convert_mp3_to_wav(filepath):
    """
    Converts an MP3 file to WAV format.
    :param filepath: Path to the MP3 file.
    :return: Success or error message.
    """
    try:
        output_path = filepath.replace(".mp3", ".wav")
        audio = AudioSegment.from_file(filepath, format="mp3")
        audio.export(output_path, format="wav")
        return f"Converted to WAV: {output_path}"
    except Exception as e:
        return f"Error converting MP3 to WAV: {e}"


def convert_wav_to_mp3(filepath):
    """
    Converts a WAV file to MP3 format.
    :param filepath: Path to the WAV file.
    :return: Success or error message.
    """
    try:
        output_path = filepath.replace(".wav", ".mp3")
        audio = AudioSegment.from_file(filepath, format="wav")
        audio.export(output_path, format="mp3")
        return f"Converted to MP3: {output_path}"
    except Exception as e:
        return f"Error converting WAV to MP3: {e}"
