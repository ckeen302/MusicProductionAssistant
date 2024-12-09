from mido import MidiFile, MidiTrack, Message
import random

# Dictionary of keys and chords
# Each key maps to its associated diatonic chords.
keys_and_chords = {
    # Major keys
    "C Major": ["C", "Dm", "Em", "F", "G", "Am", "Bdim"],
    "G Major": ["G", "Am", "Bm", "C", "D", "Em", "F#dim"],
    "D Major": ["D", "Em", "F#m", "G", "A", "Bm", "C#dim"],
    "A Major": ["A", "Bm", "C#m", "D", "E", "F#m", "G#dim"],
    "E Major": ["E", "F#m", "G#m", "A", "B", "C#m", "D#dim"],
    "B Major": ["B", "C#m", "D#m", "E", "F#", "G#m", "A#dim"],
    "F# Major": ["F#", "G#m", "A#m", "B", "C#", "D#m", "E#dim"],
    "C# Major": ["C#", "D#m", "E#m", "F#", "G#", "A#m", "B#dim"],
    "F Major": ["F", "Gm", "Am", "Bb", "C", "Dm", "Edim"],
    "Bb Major": ["Bb", "Cm", "Dm", "Eb", "F", "Gm", "Adim"],
    "Eb Major": ["Eb", "Fm", "Gm", "Ab", "Bb", "Cm", "Ddim"],
    "Ab Major": ["Ab", "Bbm", "Cm", "Db", "Eb", "Fm", "Gdim"],
    # Minor keys
    "A Minor": ["Am", "Bdim", "C", "Dm", "Em", "F", "G"],
    "E Minor": ["Em", "F#dim", "G", "Am", "Bm", "C", "D"],
    "B Minor": ["Bm", "C#dim", "D", "Em", "F#m", "G", "A"],
    "F# Minor": ["F#m", "G#dim", "A", "Bm", "C#m", "D", "E"],
    "C# Minor": ["C#m", "D#dim", "E", "F#m", "G#m", "A", "B"],
    "G# Minor": ["G#m", "A#dim", "B", "C#m", "D#m", "E", "F#"],
    "D# Minor": ["D#m", "E#dim", "F#", "G#m", "A#m", "B", "C#"],
    "A# Minor": ["A#m", "B#dim", "C#", "D#m", "E#m", "F#", "G#"],
    "D Minor": ["Dm", "Edim", "F", "Gm", "Am", "Bb", "C"],
    "G Minor": ["Gm", "Adim", "Bb", "Cm", "Dm", "Eb", "F"],
    "C Minor": ["Cm", "Ddim", "Eb", "Fm", "Gm", "Ab", "Bb"],
    "F Minor": ["Fm", "Gdim", "Ab", "Bbm", "Cm", "Db", "Eb"],
}


def generate_random_chords(key):
    """
    Generates a random chord progression in the specified key.

    Args:
        key (str): The musical key to generate chords for.
    
    Returns:
        list: A list of chords in the generated progression.

    Raises:
        ValueError: If the key is not valid.
    """
    # Get the chords for the given key
    chords = keys_and_chords.get(key, [])
    
    # If the key is invalid, raise an error
    if not chords:
        raise ValueError(f"Invalid key: {key}")
    
    # Randomly select 4 chords from the key
    return random.sample(chords, k=4)


def create_midi(chords, output_path="random_progression.mid"):
    """
    Creates a MIDI file from the given chord progression.

    Args:
        chords (list): A list of chords to include in the MIDI file.
        output_path (str): The output file path for the MIDI file.

    Returns:
        str: The output file path of the created MIDI file.
    
    Raises:
        ValueError: If a chord's root note is invalid.
    """
    # Create a new MIDI file and add a track
    midi_file = MidiFile()
    track = MidiTrack()
    midi_file.tracks.append(track)

    # Map chords to MIDI note numbers
    note_mapping = {
        "C": 60, "C#": 61, "D": 62, "D#": 63, "E": 64, "F": 65,
        "F#": 66, "G": 67, "G#": 68, "A": 69, "A#": 70, "B": 71,
        "Bb": 70, "Db": 61, "Eb": 63, "Gb": 66, "Ab": 68, "E#": 65, "B#": 72
    }

    for chord in chords:
        # Identify chord root and quality
        if chord.endswith("dim"):  # Diminished chord
            root = chord[:-3]
            quality = "dim"
        elif chord.endswith("m"):  # Minor chord
            root = chord[:-1]
            quality = "m"
        else:  # Major chord
            root = chord
            quality = "maj"

        # Ensure the chord root is valid
        if root not in note_mapping:
            raise ValueError(f"Invalid chord root '{root}' in chord '{chord}'")

        # Get the base pitch for the chord root
        base_pitch = note_mapping[root]

        # Determine the intervals for the chord
        intervals = [0, 3, 6] if quality == "dim" else [0, 3, 7] if quality == "m" else [0, 4, 7]

        # Add notes to the MIDI file for the chord
        for interval in intervals:
            track.append(Message("note_on", note=base_pitch + interval, velocity=64, time=0))
        for interval in intervals:
            track.append(Message("note_off", note=base_pitch + interval, velocity=64, time=480))

    # Save the MIDI file to the specified output path
    midi_file.save(output_path)
    return output_path
