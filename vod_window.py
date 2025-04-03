from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QVBoxLayout, QPushButton
from PyQt5.QtCore import QTimer
import json

from cell import *
from attack import *

class PlaybackWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VOD")
        self.setGeometry(100, 100, 800, 600)
        #self.fix_json_format()
        self.history_data = self.load_history()
        self.current_frame = 0
        self.total_frames = len(self.history_data)
        
        self.layout = QVBoxLayout(self)
        self.scene = QGraphicsScene(0, 0, 800, 600)
        self.view = QGraphicsView(self.scene)
        self.layout.addWidget(self.view)

        self.start_button = QPushButton("Start Playback", self)
        self.start_button.clicked.connect(self.start_playback)
        self.layout.addWidget(self.start_button)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_frame)

    def start_playback(self):
        self.current_frame = 0
        self.timer.start(1000)  
        self.start_button.setDisabled(True)  

    def next_frame(self):
        if self.current_frame < self.total_frames:
            self.load_scene(self.history_data[self.current_frame])
            self.current_frame += 1
        else:
            self.timer.stop()
            self.start_button.setDisabled(False)

    def load_scene(self, scene_data):

        self.scene.clear()

        for data in scene_data:
            if "turn" in data:
                turn = data[turn]
                time_left = data.get("turn_time", 15)
            turn_label = QGraphicsTextItem("Player's Turn: {}\nTurn ends in: {} seconds".format(
            turn.capitalize(),
            str(time_left)
            ))
            turn_label.setPos(0, 0)
            turn_label.setDefaultTextColor(QColor("white"))
            self.scene.addItem(turn_label)

            if data["type"] == "cell":
                cell = Cell(data["x"], data["y"], 30, data["owner"])
                cell.hp = data["hp"]
                cell.color = data["color"]
                self.scene.addItem(cell)

            if data["type"] == "attack":
                attack = Attack(QPointF(data["start_x"], data["start_y"]),
                                QPointF(data["end_x"], data["end_y"]),
                                data["color1"], data["color2"])
                self.scene.addItem(attack)

        self.scene.update()

    def load_history(self):
        with open("game_history.json", "r") as file:
            data = json.load(file)
            return data
   