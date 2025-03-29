from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsTextItem, QGraphicsRectItem
from PyQt5.QtCore import QTimer, QPointF
from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtWidgets import QGraphicsLineItem
from cell import Cell
from game_logic import *
from attack import Attack

class Game(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(0, 0, 800, 600)
        self.scene.setBackgroundBrush(QBrush(QColor(50, 50, 50)))
        self.setScene(self.scene)
        
        self.cells = []
        self.attacks = []
        self.selected_cell = None
        self.create_cells()

        self.last_turn = "green"
        self.turn = "green"
        self.time_left = 15

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
    
    def change_turn(self):
        if self.turn == "green":
            self.turn = "red"
        else:
            self.turn = "green"
        self.time_left = 15
        self.update_turn_display()

    def create_cells(self):
        player_cell = Cell(100, 100, 30, "player")
        player_cell1 = Cell(600, 500, 30, "player")
        enemy_cell = Cell(500, 300, 30, "enemy")
        enemy_cell1 = Cell(200, 400, 30, "enemy")
        self.scene.addItem(player_cell)
        self.scene.addItem(player_cell1)
        self.scene.addItem(enemy_cell)
        self.scene.addItem(enemy_cell1)
        self.cells.extend([player_cell1, enemy_cell, enemy_cell1, player_cell])

    def update_game(self):
        for cell in self.cells:
            if cell.hp <= 0:
                new_owner = "enemy" if cell.owner == "player" else "player"
                cell.owner = new_owner
                cell.update()
            cell.grow()
        if self.last_turn != self.turn:
            self.time_left = 15
            self.turn_timer.start(15000)
            self.last_turn = self.turn
            self.update_turn_display()
        else:
            self.time_left -= 1
        

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

    
