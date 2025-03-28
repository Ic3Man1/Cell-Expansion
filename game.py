from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
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
        self.selected_cell = None
        self.create_cells()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(1000)

    def create_cells(self):
        player_cell = Cell(100, 100, 30, "player")
        player_cell1 = Cell(600, 500, 30, "player")
        enemy_cell = Cell(500, 300, 30, "enemy")
        enemy_cell1 = Cell(200, 400, 30, "enemy")
        self.scene.addItem(player_cell)
        self.scene.addItem(player_cell1)
        self.scene.addItem(enemy_cell)
        self.scene.addItem(enemy_cell1)
        self.cells.extend([player_cell, player_cell1, enemy_cell, enemy_cell1])

    def update_game(self):
        for cell in self.cells:
            cell.grow()

    def mousePressEvent(self, event):
        item = self.scene.itemAt(event.pos(), self.transform())
        if item == self.selected_cell and self.selected_cell is not None:
            self.selected_cell = unselect_cell(self.selected_cell)
        elif isinstance(item, Cell) and item.owner == "player" and self.selected_cell is None:
            self.selected_cell = select_cell(item)
        elif isinstance(item, Cell) and self.selected_cell is not None and item not in self.selected_cell.con_to:
            self.selected_cell = merge_cells(self.selected_cell, item)
        elif isinstance(item, Attack):
            stop_attack(item)

    
