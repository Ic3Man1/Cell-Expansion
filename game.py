from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsTextItem, QGraphicsRectItem
from PyQt5.QtCore import QTimer, QPointF
from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtWidgets import QGraphicsLineItem, QPushButton, QHBoxLayout, QVBoxLayout
from cell import Cell
from game_logic import *
from attack import Attack
from levels import *
from buttonstyles import *
from logger import *
from helper import suggest_best_move
from config_menu import *
from save_demo import *
from network_handler import NetworkHandler, save_current_scene

class Game(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(0, 0, 800, 600)
        self.setWindowTitle('Game')
        self.scene.setBackgroundBrush(QBrush(QColor(50, 50, 50)))
        self.setScene(self.scene)
        self.network = None
        
        self.cells = []
        self.attacks = []
        self.pos_moves = []
        self.selected_cell = None
        self.best_move = None

        self.last_turn = "green"
        self.turn = "green"
        self.time_left = 15

        self.game_won = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.timeout.connect(self.update_turn_display)
        self.timer.start(1000)

        self.turn_timer = QTimer()
        self.turn_timer.timeout.connect(self.change_turn)
        self.turn_timer.start(15000)
        
        self.turn_background = QGraphicsRectItem(0, 0, 130, 35)
        self.scene.addItem(self.turn_background)
        self.turn_label = QGraphicsTextItem("Player's Turn: {}\nTurn ends in: {} seconds".format(
            self.turn.capitalize(),
            str(self.time_left)
        ))
        self.turn_label.setPos(0, 0)
        self.scene.addItem(self.turn_label)
        self.update_turn_display() 

        self.create_cells(level1)
        self.init_ui()
        self.log_window = LogWindow()
        self.logger = setup_logger()
        self.init_logger()
        set_logger(self.logger)
        self.congig_menu = ConfigDialog()
        
    def init_logger(self):
        text_handler = logging.StreamHandler(stream=sys.stdout)
        text_handler.setFormatter(logging.Formatter('%(message)s'))
        text_handler.emit = lambda record: self.log_window.log_message(text_handler.format(record))
        self.logger.addHandler(text_handler)
        self.logger.info("Logger initialized.")
        self.logger.info("Game started")
        

    def init_ui(self):
        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        main_layout.addStretch(1)

        possible_move_button = QPushButton('Show possible moves', self)
        possible_move_button.pressed.connect(self.show_possible_moves)
        possible_move_button.released.connect(self.hide_possible_moves)
        possible_move_button.setStyleSheet(possible_moves_style)
        button_layout.addWidget(possible_move_button)

        best_move_button = QPushButton('Show best move', self)
        best_move_button.pressed.connect(self.show_best_move)
        best_move_button.released.connect(self.hide_best_move)
        best_move_button.setStyleSheet(best_move_style)
        button_layout.addWidget(best_move_button)

        level1_button = QPushButton('Level 1', self)
        level1_button.clicked.connect(lambda: self.create_cells(level1))
        level1_button.clicked.connect(lambda: self.logger.info(str(self.turn.capitalize()) + " player changed level to 1"))
        level1_button.setStyleSheet(level_style)
        button_layout.addWidget(level1_button)

        level2_button = QPushButton('Level 2', self)
        level2_button.clicked.connect(lambda: self.create_cells(level2))
        level2_button.clicked.connect(lambda: self.logger.info(str(self.turn.capitalize()) + " player changed level to 2"))
        level2_button.setStyleSheet(level_style)
        button_layout.addWidget(level2_button)

        level3_button = QPushButton('Level 3', self)
        level3_button.clicked.connect(lambda: self.create_cells(level3))
        level3_button.clicked.connect(lambda: self.logger.info(str(self.turn.capitalize()) + " player changed level to 3"))
        level3_button.setStyleSheet(level_style)
        button_layout.addWidget(level3_button)
         
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
    
    def show_possible_moves(self):
        for cell in self.cells:
            for another_cell in self.cells:
                if cell != another_cell and cell.color == self.turn and another_cell not in cell.con_to:
                    if cell in another_cell.con_to:
                        if int(round(calc_distance(cell, another_cell)/2)) < cell.hp:
                            pos_move = Attack(cell, another_cell, "yellow", "yellow")
                            self.scene.addItem(pos_move)
                            self.pos_moves.append(pos_move)
                    else:
                        if calc_distance(cell, another_cell) < cell.hp:
                            pos_move = Attack(cell, another_cell, "yellow", "yellow")
                            self.scene.addItem(pos_move)
                            self.pos_moves.append(pos_move)
        self.logger.info(str(self.turn.capitalize()) + " player displayed possible moves")
        self.scene.update()
      
    def hide_possible_moves(self):
        for pos_mov in self.pos_moves:
            self.scene.removeItem(pos_mov)
        del self.pos_moves[:]

    def show_best_move(self):
        result = suggest_best_move(self.cells, self.turn)
        if not result:
            self.logger.info("No best move")
            return

        attacker, defender = result
        line = Attack(attacker, defender, "orange", "orange")
        self.scene.addItem(line)
        self.best_move = line
        self.logger.info(str(self.turn.capitalize()) + " player displayed best move")

    def hide_best_move(self):
        if self.best_move is None:
            return
        self.scene.removeItem(self.best_move)
        self.best_move = None

    def change_turn(self):
        if self.turn == "green":
            self.turn = "red"
        else:
            self.turn = "green"
        self.time_left = 15
        self.update_turn_display()

    def chcek_win(self):
        color = self.cells[0].color
        for cell in self.cells:
            if cell.color != color:
                return False, color
        return True, color

    def create_cells(self, level):
        for i in self.cells + self.attacks:
            self.scene.removeItem(i)
        del self.cells[:]
        del self.attacks[:]
        level(self.scene, self.cells)
        self.reset_timer()
        self.game_won = False
        self.scene.update()

    def update_game(self):
        self.save_game()
        if self.congig_menu.mode == "Online Multiplayer":
            if not (self.network and self.network.is_connected()):
                self.network = NetworkHandler(
                    is_host=(self.congig_menu.ip.strip() == ""),
                    ip=self.congig_menu.ip.strip(),
                    port=12345,
                    on_receive_callback=self.receive_scene
                )
            #print("Jest polaczenie B)")
        else:
            self.network = None
        if self.congig_menu.mode == "Singleplayer":
            self.turn = "green"
        else:
            if self.last_turn != self.turn:
                self.reset_timer()
            else:
                self.time_left -= 1
        if not self.game_won:
            win, color = self.chcek_win()
            if win:
                show_fading_message((str(color) + " has won"), 5000)
                self.logger.info(str(self.turn.capitalize()) + " player has won a game")
                self.game_won = True
        for cell in self.cells:
            if cell.hp <= 0:
                self.attacks = retrieve_cell(cell, self.attacks)
                self.logger.info(str(self.turn.capitalize()) + " player has captured an enemy cell")
                cell.update()
                self.scene.update()
            cell.grow()
        
    def reset_timer(self):
        self.time_left = 15
        self.turn_timer.start(15000)
        self.last_turn = self.turn
        self.update_turn_display()

    def update_turn_display(self):
        if self.turn == "green":
            self.turn_background.setBrush(QBrush(QColor("white")))  
            self.turn_label.setDefaultTextColor(QColor("green"))
        else:
            self.turn_background.setBrush(QBrush(QColor("black")))
            self.turn_label.setDefaultTextColor(QColor("red"))
        
        self.turn_label.setPlainText("Player's Turn: {}\nTurn ends in: {} seconds".format(
            self.turn.capitalize(),
            str(self.time_left)
        ))
            
    def mousePressEvent(self, event):
        item = self.scene.itemAt(event.pos(), self.transform())
        if item == self.selected_cell and self.selected_cell is not None:
            self.selected_cell = unselect_cell(self.selected_cell)
            self.logger.info(str(self.turn.capitalize()) + " player has unmarked the cell")
        elif isinstance(item, Cell) and self.selected_cell is None:
            self.selected_cell = select_cell(item, self.turn)
        elif isinstance(item, Cell) and self.selected_cell is not None and item not in self.selected_cell.con_to:
            self.last_turn = self.turn
            self.selected_cell, self.turn = merge(self.attacks, self.selected_cell, item, self.turn)
            self.update_turn_display()
            self.scene.update()
        elif isinstance(item, Attack):
            self.last_turn = self.turn
            self.turn = separate(self.attacks, item, self.turn)
            self.update_turn_display()
            self.scene.update()
        if self.network:
                    scene = save_current_scene(
                        self.cells, self.attacks,
                        self.turn, self.time_left,
                        self.congig_menu.mode, self.congig_menu.ip
                    )
                    self.network.send({"type": "scene", "data": scene})

    def save_game(self):
        save_scene_to_json(self.cells, self.attacks, self.pos_moves, self.best_move, self.turn, self.time_left, self.congig_menu.mode, self.congig_menu.ip)
        save_scene_to_xml(self.cells, self.attacks, self.pos_moves, self.best_move, self.turn, self.time_left, self.congig_menu.mode, self.congig_menu.ip)
        #save_current_scene(self.cells, self.attacks, self.pos_moves, self.best_move, self.turn, self.time_left, self.congig_menu.mode, self.congig_menu.ip)
        #save_scene_to_db(self.cells, self.attacks, self.pos_moves, self.best_move, self.turn, self.time_left, self.congig_menu.mode, self.congig_menu.ip)

    def receive_scene(self, data):
        if data.get("type") != "scene":
            return
        scene_data = data.get("data")
        if scene_data:
            print("[DEBUG] Otrzymano scenę od przeciwnika")
            QTimer.singleShot(0, lambda: self.load_scene(scene_data))
            QTimer.singleShot(0, lambda: self.ensure_timers())

    def load_scene(self, scene_data):
        print("[DEBUG] Ładuję scenę...")

        self.scene.clear()
        self.cells = []
        self.attacks = []
        self.pos_moves = []

        game_state = scene_data.get("game_state", {})
        self.turn = game_state.get("turn", "green")
        self.time_left = game_state.get("turn_time", 15)
        self.update_turn_display()

        for data in scene_data.get("cells", []):
            if data.get("type") == "cell":
                cell = Cell(data["x"], data["y"], 30, data["owner"])
                cell.hp = data["hp"]
                cell.color = data["color"]
                cell.setBrush(QColor(cell.color))
                cell.hp_points_label.setPlainText(str(cell.hp))
                self.scene.addItem(cell)
                self.cells.append(cell)

        for data in scene_data.get("attacks", []):
            if data.get("type") == "attack":
                attacker = self.find_cell_near(data["start_x"], data["start_y"])
                defender = self.find_cell_near(data["end_x"], data["end_y"])
                if attacker and defender:
                    attack = Attack(attacker, defender, data["color1"], data["color2"])
                    self.scene.addItem(attack)
                    self.attacks.append(attack)

        self.scene.setSceneRect(0, 0, 800, 600)
        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        self.view.viewport().update()
        self.scene.update()

    def ensure_timers(self):
        if not self.timer.isActive():
            self.timer.start(1000)
        if not self.turn_timer.isActive():
            self.turn_timer.start(15000)