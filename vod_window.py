from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import QTimer
import json

from cell import *
from attack import *

class PlaybackWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VOD")
        self.setGeometry(100, 100, 850, 750)
        self.history_data = self.load_history()
        self.current_frame = 0
        self.total_frames = len(self.history_data)
        self.speed = 1000
        self.help_layout = QHBoxLayout()
        self.layout = QVBoxLayout(self)
        self.scene = QGraphicsScene(0, 0, 800, 600)
        self.scene.setBackgroundBrush(QBrush(QColor(50, 50, 50)))
        self.view = QGraphicsView(self.scene)
        self.layout.addWidget(self.view)

        self.start_button = QPushButton("Start Playback", self)
        self.start_button.clicked.connect(self.start_playback)
        self.layout.addWidget(self.start_button)

        self.x05_button = QPushButton("Speed x0.5", self)
        self.x05_button.clicked.connect(self.halve_speed)
        self.help_layout.addWidget(self.x05_button)
        
        self.reset_speed_button = QPushButton("Reset Speed", self)
        self.reset_speed_button.clicked.connect(self.reset_speed)
        self.help_layout.addWidget(self.reset_speed_button)

        self.x2_button = QPushButton("Speed x2", self)
        self.x2_button.clicked.connect(self.double_speed)
        self.help_layout.addWidget(self.x2_button)

        self.layout.addLayout(self.help_layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_frame)

    def double_speed(self):
        self.speed = max(self.speed // 2, 125)
        self.timer.setInterval(self.speed)

    def halve_speed(self):
        self.speed = min(self.speed * 2, 8000)
        self.timer.setInterval(self.speed)

    def reset_speed(self):
        self.speed = 1000
        self.timer.setInterval(self.speed)

    def start_playback(self):
        self.current_frame = 0
        self.timer.start(self.speed)  
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
        self.cells = []
        self.attacks = []
        self.pos_moves = []

        game_settings = scene_data.get("game_settings", {})
        game_state = scene_data.get("game_state", {})
        cells = scene_data.get("cells", [])
        attacks = scene_data.get("attacks", [])
        best_move = scene_data.get("best_move")

        turn = game_state.get("turn", "green")
        time_left = game_state.get("turn_time", 15)

        turn_label = QGraphicsTextItem("Player's Turn: {}\nTurn ends in: {} seconds".format(
            turn.capitalize(), str(time_left)
        ))
        turn_label.setPos(0, 0)
        turn_label.setDefaultTextColor(QColor("white"))
        self.scene.addItem(turn_label)

        for data in cells:
            if data.get("type") == "cell":
                cell = Cell(data["x"], data["y"], 30, data["owner"])
                cell.hp = data["hp"]
                cell.hp_points_label.setPlainText(str(cell.hp))
                cell.color = data["color"]
                cell.setBrush(QColor(cell.color))
                self.scene.addItem(cell)
                self.cells.append(cell)

        for data in attacks:
            if data.get("type") == "attack":
                attacker = Cell(data["start_x"], data["start_y"], 30, "player")
                defender = Cell(data["end_x"], data["end_y"], 30, "player")
                attack = Attack(attacker, defender, data["color1"], data["color2"])
                self.scene.addItem(attack)
                self.attacks.append(attack)

        if best_move:
            attacker = Cell(best_move["start_x"], best_move["start_y"], 30, "player")
            defender = Cell(best_move["end_x"], best_move["end_y"], 30, "player")
            best = Attack(attacker, defender, "orange", "orange")
            self.scene.addItem(best)
            self.pos_moves.append(best)

        self.scene.setSceneRect(0, 0, 800, 600)
        self.scene.update()

    def load_history(self):
        with open("game_history.json", "r") as file:
            scene_data = json.load(file)
            return scene_data
   