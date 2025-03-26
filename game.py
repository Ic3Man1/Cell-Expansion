from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtWidgets import QGraphicsLineItem
from cell import Cell

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
        enemy_cell = Cell(500, 300, 30, "enemy")
        self.scene.addItem(player_cell)
        self.scene.addItem(enemy_cell)
        self.cells.extend([player_cell, enemy_cell])

    def update_game(self):
        for cell in self.cells:
            cell.grow()

    def mousePressEvent(self, event):
        item = self.scene.itemAt(event.pos(), self.transform())
        if item == self.selected_cell:
            self.selected_cell.change_border_color("black")
            self.selected_cell = None
        elif isinstance(item, Cell) and item.owner == "player":
            self.selected_cell = item
            self.selected_cell.change_border_color("yellow")
        elif isinstance(item, Cell) and item.owner == "enemy" and self.selected_cell is not None:
            self.selected_cell.change_border_color("black")
            self.draw_line_between_cells(item, self.selected_cell)
            self.selected_cell = None

    def draw_line_between_cells(self, cell1, cell2):
        cell1_center = cell1.boundingRect().center() + cell1.pos()
        cell2_center = cell2.boundingRect().center() + cell2.pos()

        line = QGraphicsLineItem(cell1_center.x(), cell1_center.y(), cell2_center.x(), cell2_center.y())
        line_pen = QPen(QColor("black"))
        line_pen.setWidth(5)
        line.setPen(line_pen)

        self.scene.addItem(line)
            
