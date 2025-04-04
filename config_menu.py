from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QRadioButton, QLineEdit, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
import json
import xml.etree.ElementTree as ET
from save_demo import *
from vod_window import *


class ConfigDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuration Menu")
        self.setGeometry(1440, 550, 350, 250)
        
        layout = QVBoxLayout()

        self.game_mode_label = QLabel("Select game mode:")
        layout.addWidget(self.game_mode_label)

        self.single_player_button = QRadioButton("Singleplayer")
        self.two_players_button = QRadioButton("Local Multiplayer")
        self.network_game_button = QRadioButton("Online Multiplayer")

        self.two_players_button.setChecked(True)

        layout.addWidget(self.single_player_button)
        layout.addWidget(self.two_players_button)
        layout.addWidget(self.network_game_button)

        self.ip_label = QLabel("Input IP and port:")
        layout.addWidget(self.ip_label)

        self.ip_input = QLineEdit(self)
        ip_validator = QRegExpValidator(QRegExp(r"^(\d{1,3}\.){3}\d{1,3}:\d{1,5}$"), self)
        self.ip_input.setValidator(ip_validator)
        self.ip_input.setPlaceholderText("xxx.xxx.xxx.xxx:port")
        layout.addWidget(self.ip_input)

        self.save_button = QPushButton("Save settings")
        self.load_button = QPushButton("Watch demo")
        self.save_button.clicked.connect(self.save_settings)
        self.load_button.clicked.connect(self.watch_demo)
        layout.addWidget(self.save_button)
        layout.addWidget(self.load_button)

        self.mode = self.get_game_mode()
        self.ip = ""
        
        #self.vod = PlaybackWindow()
        self.setLayout(layout)
        self.show()

    def save_settings(self):
        self.mode = self.get_game_mode()
        self.ip = self.ip_input.text()

    def watch_demo(self):
        self.vod = PlaybackWindow()
        self.vod.show()
        
    def get_game_mode(self):
        if self.single_player_button.isChecked():
            self.single_player_button.setChecked(True)
            return "Singleplayer"
        elif self.two_players_button.isChecked():
            self.two_players_button.setChecked(True)
            return "Local Multiplayer"
        elif self.network_game_button.isChecked():
            self.network_game_button.setChecked(True)
            return "Online Multiplayer"

    
   