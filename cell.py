from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem
from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtCore import QRectF

class Cell(QGraphicsEllipseItem):
    def __init__(self, x, y, radius, owner):
        super().__init__(QRectF(x, y, radius * 2, radius * 2))
        self.color = "green" if owner == "player" else "red"
        self.setBrush(QBrush(QColor(self.color)))
        self.owner = owner
        self.hp = 10
        self.setZValue(1)
        self.con_to = set()

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
            self.setBrush(QBrush(QColor("green")))
        else:
            self.setBrush(QBrush(QColor("red")))
        self.dmg_taken, self.hp_supply = self.hp_supply, self.dmg_taken
