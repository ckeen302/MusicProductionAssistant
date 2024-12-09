import sys
import os
import pygame
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QFileDialog,
    QVBoxLayout, QWidget, QComboBox, QFrame, QStatusBar
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from chord_generation import generate_random_chords, create_midi, keys_and_chords
from audio_conversion import convert_mp3_to_wav, convert_wav_to_mp3
from popular_songs import popular_songs, create_song_midi


class MusicProductionAssistant(QMainWindow):
    def __init__(self):
        """
        Initializes the Music Production Assistant application.
        """
        super().__init__()
        self.setWindowTitle("Music Production Assistant")  # Application title
        self.setGeometry(200, 100, 900, 700)

        # Initialize variables
        self.generated_progression = []  # Stores the generated chord progression
        self.midi_path = None  # Path to the generated or loaded MIDI file

        # Setup the user interface
        self.initUI()

    def initUI(self):
        """
        Sets up the user interface, including layout, widgets, and styling.
        """
        # Apply retro neon styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            QPushButton {
                background-color: #2e2e2e;
                color: #00ff00;
                border: 2px solid #00ff00;
                border-radius: 8px;
                font-family: 'Courier New', monospace;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
            }
            QLabel {
                color: #00ff00;
                font-family: 'Courier New', monospace;
                font-size: 16px;
            }
            QComboBox {
                background-color: #2e2e2e;
                color: #00ff00;
                border: 2px solid #00ff00;
                border-radius: 5px;
                padding: 4px;
                font-family: 'Courier New', monospace;
                font-size: 14px;
            }
        """)

        # Set central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)

        # Title Label
        title_label = QLabel("🎵 Music Production Assistant 🎶")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #00ff00;")
        main_layout.addWidget(title_label)

        # Section: Chord Progression by Key
        key_frame = QFrame()  # Frame for the dropdown
        key_layout = QVBoxLayout(key_frame)
        key_label = QLabel("Generate Chord Progression by Key:")
        self.key_selector = QComboBox()  # Dropdown menu for selecting keys
        self.key_selector.addItems(keys_and_chords.keys())  # Populate dropdown with available keys
        key_layout.addWidget(key_label)
        key_layout.addWidget(self.key_selector)
        main_layout.addWidget(key_frame)

        # Buttons for chord progression generation and control
        self.generate_button = QPushButton("Generate Progression")
        self.generate_button.clicked.connect(self.generate_progression)  # Connect to generation method
        main_layout.addWidget(self.generate_button)

        self.play_button = QPushButton("Play Progression")
        self.play_button.clicked.connect(self.play_generated_progression)  # Connect to playback method
        main_layout.addWidget(self.play_button)

        self.download_button = QPushButton("Download MIDI")
        self.download_button.clicked.connect(self.download_generated_progression)  # Connect to download method
        main_layout.addWidget(self.download_button)

        # Section: Popular Songs
        song_frame = QFrame()
        song_layout = QVBoxLayout(song_frame)
        song_label = QLabel("Select a Popular Song:")
        self.song_selector = QComboBox()
        self.song_selector.addItems(popular_songs.keys())  # Populate with popular songs
        song_layout.addWidget(song_label)
        song_layout.addWidget(self.song_selector)
        main_layout.addWidget(song_frame)

        self.play_song_button = QPushButton("Play Song Progression")
        self.play_song_button.clicked.connect(self.play_song_progression)
        main_layout.addWidget(self.play_song_button)

        self.download_song_button = QPushButton("Download Song MIDI")
        self.download_song_button.clicked.connect(self.download_song_midi)
        main_layout.addWidget(self.download_song_button)

        # Section: Audio Conversion
        conversion_frame = QFrame()
        conversion_layout = QVBoxLayout(conversion_frame)
        convert_label = QLabel("Audio Conversion Tools:")
        convert_label.setAlignment(Qt.AlignLeft)
        conversion_layout.addWidget(convert_label)

        self.convert_mp3_button = QPushButton("Convert MP3 to WAV")
        self.convert_mp3_button.clicked.connect(self.convert_mp3_to_wav_file)
        conversion_layout.addWidget(self.convert_mp3_button)

        self.convert_wav_button = QPushButton("Convert WAV to MP3")
        self.convert_wav_button.clicked.connect(self.convert_wav_to_mp3_file)
        conversion_layout.addWidget(self.convert_wav_button)
        main_layout.addWidget(conversion_frame)

        # Result Label
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 14px; color: #00ff00; margin: 10px 0;")
        main_layout.addWidget(self.result_label)

        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def generate_progression(self):
        """
        Generates a random chord progression based on the selected key.
        Updates the result label with the generated progression.
        """
        key = self.key_selector.currentText()  # Get the selected key
        self.generated_progression = generate_random_chords(key)  # Generate chords for the key
        self.result_label.setText(f"Generated Progression: {' -> '.join(self.generated_progression)}")
        self.status_bar.showMessage("Chord progression generated.", 3000)

    def play_generated_progression(self):
        """
        Creates and plays the MIDI file for the generated chord progression.
        Updates the result label to indicate playback.
        """
        if not self.generated_progression:
            self.result_label.setText("No progression generated!")
            self.status_bar.showMessage("No progression to play.", 3000)
            return

        self.midi_path = create_midi(self.generated_progression)  # Create MIDI file from progression
        pygame.mixer.init()
        pygame.mixer.music.load(self.midi_path)  # Load the MIDI file for playback
        pygame.mixer.music.play()
        self.result_label.setText("Playing Generated Progression")
        self.status_bar.showMessage("Playing chord progression.", 3000)

    def download_generated_progression(self):
        """
        Allows the user to save the generated chord progression as a MIDI file.
        Updates the result label with the save status.
        """
        if not self.midi_path or not os.path.exists(self.midi_path):
            self.result_label.setText("No progression available to download!")
            self.status_bar.showMessage("No MIDI file available to download.", 3000)
            return

        save_path, _ = QFileDialog.getSaveFileName(self, "Save MIDI File", self.midi_path, "MIDI Files (*.mid)")
        if save_path:
            os.rename(self.midi_path, save_path)  # Move the MIDI file to the specified location
            self.result_label.setText(f"MIDI saved as: {save_path}")
            self.status_bar.showMessage("MIDI file saved.", 3000)
        else:
            self.result_label.setText("MIDI download canceled.")
            self.status_bar.showMessage("MIDI download canceled.", 3000)

    def play_song_progression(self):
        """
        Plays the chord progression for the selected popular song.
        """
        song_name = self.song_selector.currentText()  # Get the selected song name
        chords = popular_songs[song_name]  # Get the chord progression for the song
        self.midi_path = create_song_midi(song_name, chords)  # Create the MIDI file
        pygame.mixer.init()
        pygame.mixer.music.load(self.midi_path)
        pygame.mixer.music.play()
        self.result_label.setText(f"Playing: {song_name}")
        self.status_bar.showMessage(f"Playing {song_name} chord progression.", 3000)

    def download_song_midi(self):
        """
        Allows the user to save the MIDI file for the selected popular song.
        """
        if not self.midi_path or not os.path.exists(self.midi_path):
            self.result_label.setText("No song progression available to download!")
            self.status_bar.showMessage("No MIDI file available to download.", 3000)
            return

        save_path, _ = QFileDialog.getSaveFileName(self, "Save MIDI File", self.midi_path, "MIDI Files (*.mid)")
        if save_path:
            os.rename(self.midi_path, save_path)  # Move the MIDI file to the specified location
            self.result_label.setText(f"MIDI saved as: {save_path}")
            self.status_bar.showMessage(f"MIDI file saved for {self.song_selector.currentText()}.", 3000)
        else:
            self.result_label.setText("MIDI download canceled.")
            self.status_bar.showMessage("MIDI download canceled.", 3000)

    def convert_mp3_to_wav_file(self):
        """
        Converts an MP3 file to WAV format and updates the result label.
        """
        file_dialog = QFileDialog.getOpenFileName(self, "Select MP3 File", "", "Audio Files (*.mp3)")
        if file_dialog[0]:
            filepath = file_dialog[0]
            result = convert_mp3_to_wav(filepath)  # Call the audio conversion function
            self.result_label.setText(result)
            self.status_bar.showMessage("MP3 converted to WAV.", 3000)

    def convert_wav_to_mp3_file(self):
        """
        Converts a WAV file to MP3 format and updates the result label.
        """
        file_dialog = QFileDialog.getOpenFileName(self, "Select WAV File", "", "Audio Files (*.wav)")
        if file_dialog[0]:
            filepath = file_dialog[0]
            result = convert_wav_to_mp3(filepath)  # Call the audio conversion function
            self.result_label.setText(result)
            self.status_bar.showMessage("WAV converted to MP3.", 3000)

    def closeEvent(self, event):
        """
        Cleans up temporary files and quits pygame when the application is closed.
        """
        if self.midi_path and os.path.exists(self.midi_path):  # Remove temporary MIDI file if it exists
            os.remove(self.midi_path)
        if pygame.mixer.get_init():  # Quit pygame mixer
            pygame.mixer.quit()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MusicProductionAssistant()
    window.show()
    sys.exit(app.exec_())
