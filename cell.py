from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem
from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtCore import QRectF

class Cell(QGraphicsEllipseItem):
    def __init__(self, x, y, radius, owner):
        super().__init__(QRectF(x, y, radius * 2, radius * 2))
        self.setBrush(QBrush(QColor("green" if owner == "player" else "red")))
        self.owner = owner
        self.units = 10
        self.position = self.pos()
        self.setZValue(1)

        self.pen = QPen(QColor("black"))  # Początkowy kolor obwódki
        self.pen.setWidth(3)
        self.setPen(self.pen)  # Ustawiamy pióro na komórce

        self.health_points = QGraphicsTextItem(str(self.units), self)
        self.health_points.setPos(self.boundingRect().center() - self.health_points.boundingRect().center())
        self.health_points.setDefaultTextColor(QColor("black"))

    def grow(self):
        if self.owner:
            self.units += 1
            self.health_points.setPlainText(str(self.units))

    def change_border_color(self, color):
        self.pen.setColor(QColor(color))
        self.setPen(self.pen)
