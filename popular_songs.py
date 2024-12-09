from mido import MidiFile, MidiTrack, Message

# Dictionary of popular songs and their chord progressions
popular_songs = {
    "Let It Be (The Beatles)": ["C", "G", "Am", "F"],
    "Someone Like You (Adele)": ["A", "E", "F#m", "D"],
    "Shape of You (Ed Sheeran)": ["C#m", "F#m", "A", "B"],
    "Canon in D (Pachelbel)": ["D", "A", "Bm", "F#m", "G", "D", "G", "A"],
    "No Woman, No Cry (Bob Marley)": ["C", "G", "Am", "F"],
    "With or Without You (U2)": ["D", "A", "Bm", "G"],
    "Don’t Stop Believin’ (Journey)": ["E", "B", "C#m", "A"],
    "Hotel California (Eagles)": ["Bm", "F#", "A", "E", "G", "D", "Em", "F#"],
    "Mad World (Tears for Fears)": ["F", "G", "Em", "Am"],
    "All of Me (John Legend)": ["F", "G", "Em", "Am"],
    "Rolling in the Deep (Adele)": ["Am", "G", "F", "Em"],
    "Hallelujah (Leonard Cohen)": ["C", "Am", "F", "G"],
    "Imagine (John Lennon)": ["C", "F", "G", "E", "Am", "D", "G"],
    "Yesterday (The Beatles)": ["F", "Em7", "A7", "Dm", "G7", "Bb", "C"],
    "Perfect (Ed Sheeran)": ["G", "Em", "C", "D"],
    "Stairway to Heaven (Led Zeppelin)": ["Am", "G", "F", "G", "Am", "E"],
    "Bohemian Rhapsody (Queen)": ["Bb", "Gm", "Cm", "F"],
    "Take Me Home, Country Roads (John Denver)": ["G", "Em", "D", "C"],
}

# Mapping chords to MIDI note numbers
note_mapping = {
    "C": 60, "C#": 61, "Db": 61, "D": 62, "D#": 63, "Eb": 63, "E": 64, 
    "F": 65, "F#": 66, "Gb": 66, "G": 67, "G#": 68, "Ab": 68, 
    "A": 69, "A#": 70, "Bb": 70, "B": 71
}

def create_song_midi(song_name, chords, output_path="song_progression.mid"):
    """
    Creates a MIDI file for a given song's chord progression.

    Args:
        song_name (str): Name of the song.
        chords (list): List of chords in the song's progression.
        output_path (str): Path to save the generated MIDI file.

    Returns:
        str: Path to the generated MIDI file.
    """
    midi_file = MidiFile()  # Create a new MIDI file
    track = MidiTrack()  # Create a new MIDI track
    midi_file.tracks.append(track)  # Append the track to the MIDI file

    for chord in chords:
        # Extract the root note of the chord
        root = chord.rstrip("m#7dim")  # Handle extended chords like "Em7", "A7", "Cdim"
        quality = chord[len(root):]  # Get the quality (e.g., "m", "7", "dim")
        
        if root not in note_mapping:
            raise ValueError(f"Unknown root note in chord: {chord}")

        base_pitch = note_mapping[root]  # Get the MIDI note number for the root

        # Determine chord intervals based on quality
        if "m" in quality and "7" not in quality:  # Minor chord
            intervals = [0, 3, 7]
        elif "dim" in quality:  # Diminished chord
            intervals = [0, 3, 6]
        elif "7" in quality:  # Dominant 7th chord
            intervals = [0, 4, 7, 10]
        else:  # Major chord
            intervals = [0, 4, 7]

        # Add notes to the MIDI track
        for interval in intervals:
            track.append(Message("note_on", note=base_pitch + interval, velocity=64, time=0))
        for interval in intervals:
            track.append(Message("note_off", note=base_pitch + interval, velocity=64, time=480))

    # Save the MIDI file to the specified path
    midi_file.save(output_path)
    return output_path
