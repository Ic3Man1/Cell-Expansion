from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QVBoxLayout, QPushButton
from PyQt5.QtCore import QTimer
import json

from cell import *
from attack import *

class PlaybackWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VOD")
        self.setGeometry(100, 100, 850, 675)
        self.history_data = self.load_history()
        self.current_frame = 0
        self.total_frames = len(self.history_data)
        
        self.layout = QVBoxLayout(self)
        self.scene = QGraphicsScene(0, 0, 800, 600)
        self.scene.setBackgroundBrush(QBrush(QColor(50, 50, 50)))
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
        self.cells = []
        self.attacks = []
        self.pos_moves = []

        # 1. Wczytaj stan gry i dane
        game_settings = scene_data.get("game_settings", {})
        game_state = scene_data.get("game_state", {})
        cells = scene_data.get("cells", [])
        attacks = scene_data.get("attacks", [])
        best_move = scene_data.get("best_move")

        turn = game_state.get("turn", "green")
        time_left = game_state.get("turn_time", 15)

        # 2. Wyświetl label tury
        turn_label = QGraphicsTextItem("Player's Turn: {}\nTurn ends in: {} seconds".format(
            turn.capitalize(), str(time_left)
        ))
        turn_label.setPos(0, 0)
        turn_label.setDefaultTextColor(QColor("white"))
        self.scene.addItem(turn_label)

        # 3. Wczytaj komórki
        for data in cells:
            if data.get("type") == "cell":
                cell = Cell(data["x"], data["y"], 30, data["owner"])
                cell.hp = data["hp"]
                cell.hp_points_label.setPlainText(str(cell.hp))
                cell.color = data["color"]
                cell.setBrush(QColor(cell.color))
                self.scene.addItem(cell)
                self.cells.append(cell)

        # 4. Wczytaj ataki
        for data in attacks:
            if data.get("type") == "attack":
                # attacker = QPointF(data["start_x"], data["start_y"])
                # defender = QPointF(data["end_x"], data["end_y"])
                attacker = Cell(data["start_x"], data["start_y"], 30, "player")
                defender = Cell(data["end_x"], data["end_y"], 30, "player")
                attack = Attack(attacker, defender, data["color1"], data["color2"])
                self.scene.addItem(attack)
                self.attacks.append(attack)

        # 5. Wczytaj najlepszy ruch, jeśli istniej
        # if best_move and best_move.get("type") == "best_move":
        #     attacker = Cell(data["start_x"], data["start_y"], 30, "player")
        #     defender = Cell(data["end_x"], data["end_y"], 30, "player")
        #     best = Attack(attacker, defender, best_move["color1"], best_move["color2"])
        #     self.scene.addItem(best)
        #     self.pos_moves.append(best)

        self.scene.setSceneRect(0, 0, 800, 600)
        self.scene.update()



    def load_history(self):
        with open("game_history.json", "r") as file:
            scene_data = json.load(file)
            return scene_data
   