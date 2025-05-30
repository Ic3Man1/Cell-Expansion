from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem
from PyQt5.QtGui import QBrush, QColor, QPen, QPixmap
from PyQt5.QtCore import QRectF
import resources_rc

class Cell(QGraphicsEllipseItem):
    def __init__(self, x, y, radius, owner):
        super().__init__(QRectF(x, y, radius * 2, radius * 2))
        self.x = x
        self.y = y
        self.color = "green" if owner == "player" else "red"
        if owner == "player":
            pixmap = QPixmap(":/green_cell") 
        else:
            pixmap = QPixmap(":/red_cell")
        self.setBrush(QBrush(pixmap))
        self.owner = owner
        self.hp = 10
        self.setZValue(1)
        self.con_to = set()
        self.whos_con = set()

        self.dmg_taken = 0
        self.hp_supply = 0
        self.attack_dmg = 0

        self.pen = QPen(QColor("black")) 
        self.pen.setWidth(3)
        self.setPen(self.pen)  

        self.hp_points_label = QGraphicsTextItem(str(self.hp), self)
        self.hp_points_label.setPos(self.boundingRect().center() - self.hp_points_label.boundingRect().center())
        self.hp_points_label.setDefaultTextColor(QColor("black"))

    def grow(self):
        if self.owner:
            self.hp = self.hp + 1 + self.hp_supply - self.dmg_taken - self.attack_dmg
            self.hp_points_label.setPlainText(str(self.hp))

    def change_border_color(self, color):
        self.pen.setColor(QColor(color))
        self.setPen(self.pen)

    def update(self):
        if self.owner == "player":
            self.color = "green"
            self.setBrush(QBrush(QPixmap(":/green_cell")))
        else:
            self.color = "red"
            self.setBrush(QBrush(QPixmap(":/red_cell")))
