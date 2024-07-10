import sys
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6 import uic
from Stopwatch import Stopwatch
from gpiozero import Button

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        uic.loadUi("ShowPrompter.ui", self)

        self.current_song_index = 0
        self.previous_song = ""
        self.next_song = ""
        self.set_list = []

        self.showFullScreen()
        self.setup_interface()

        # Set stopwatch timer and label
        self.stopwatch_label.stopwatch_timer = QTimer()
        self.stopwatch = Stopwatch(self.stopwatch_label, 0)
        self.stopwatch_label.stopwatch_timer.timeout.connect(self.stopwatch.display)
        self.stopwatch_label.stopwatch_timer.start(10)

        self.settings = {}
        self.load_settings()


    ''' Load program settings '''
    def load_settings(self):
        # Read settings
        file = open("Config/settings.txt", "r")
        for line in file:
            self.settings[line.split()[0]] = int(line.split()[1])

        # GPIO setup
        if self.settings["has_GPIO_configured"]:
            self.left_button = Button(3, hold_time=0.05)
            self.left_button.when_pressed = self.on_previous_song
            self.right_button = Button(4, hold_time=0.05)
            self.right_button.when_pressed = self.on_next_song


    ''' Initial interface setup. Reads set list, applies labels and lyrics '''
    def setup_interface(self):
        # Read set list
        file = open("Config/setList.txt", "r")
        for line in file:
            self.set_list.append(line)

        # Setup interface
        self.set_song_labels()
        self.set_lyrics_pixmap()


    ''' Update song label in relation to "current song" '''
    def set_song_labels(self):
        if self.current_song_index < len(self.set_list) - 1:
            self.previous_song = self.set_list[self.current_song_index-1] if self.current_song_index != 0 else ""
            self.next_song = self.set_list[self.current_song_index+1] if self.current_song_index < len(self.set_list) - 1 else ""
            self.lb_previous_song.setText(self.previous_song)
            self.lb_next_song.setText(self.next_song)


    ''' Set lyrics pixmap '''
    def set_lyrics_pixmap(self):
        # Load the image and display in label
        self.pix = QPixmap("ShowMedia/{:02d}.JPG".format(self.current_song_index))
        scaled_pixmap = self.pix.scaled(self.lyrics_image.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.lyrics_image.setPixmap(scaled_pixmap)


    ''' Execute all tasks releated to "previous song" operation '''
    def on_previous_song(self):
        if self.current_song_index > 0:
            self.current_song_index -= 1
            self.set_song_labels()
            self.set_lyrics_pixmap()


    ''' Execute all tasks releated to "next song" operation '''
    def on_next_song(self):
        if self.current_song_index < len(self.set_list) - 1:
            self.current_song_index += 1
            self.set_song_labels()
            self.set_lyrics_pixmap()


    '''Key presses logic '''
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Left:
            self.on_previous_song()
        elif event.key() == Qt.Key.Key_Right:
            self.on_next_song()
        elif event.key() == Qt.Key.Key_Escape:
            self.close()


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
