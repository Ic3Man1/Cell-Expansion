from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsTextItem
from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtCore import QRectF, QPointF
from cell import Cell

class Attack(QGraphicsLineItem):
    def __init__(self, atk_cell, def_cell):
        super().__init__()

        self.atk_center = atk_cell.boundingRect().center() + atk_cell.pos()
        self.def_center = def_cell.boundingRect().center() + def_cell.pos()
        self.mid = QPointF((self.atk_center.x() + self.def_center.x()) / 2, (self.atk_center.y() + self.def_center.y()) / 2)

        self.attacker = atk_cell
        self.defender = def_cell

        self.scene = atk_cell.scene()
        self.setLine(self.atk_center.x(), self.atk_center.y(), self.def_center.x(), self.def_center.y())

    def boundingRect(self):
        return QRectF(self.atk_center, self.def_center).normalized()

    def paint(self, painter, option, widget):
        pen = QPen(QColor("green"))
        pen.setWidth(5)
        painter.setPen(pen)

        painter.drawLine(self.atk_center, self.mid)

        pen = QPen(QColor("red"))
        pen.setWidth(5)
        painter.setPen(pen)

        painter.drawLine(self.mid, self.def_center)
