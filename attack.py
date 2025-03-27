from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsTextItem
from PyQt5.QtGui import QBrush, QColor, QPen, QPainterPath, QPainterPathStroker
from PyQt5.QtCore import QRectF, QPointF, Qt
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

        self.pen = QPen(Qt.red, 10)  
        self.pen.setCapStyle(Qt.RoundCap)
        self.setPen(self.pen)

    def paint(self, painter, option, widget):
        pen = QPen(QColor("green"))
        pen.setWidth(10)
        painter.setPen(pen)

        painter.drawLine(self.atk_center, self.mid)

        pen = QPen(QColor("green"))
        pen.setWidth(10)
        painter.setPen(pen)

        painter.drawLine(self.mid, self.def_center)

    def shape(self):
        path = QPainterPath()
        path.moveTo(self.line().p1())
        path.lineTo(self.line().p2())

        stroker = QPainterPathStroker()
        stroker.setWidth(self.pen.widthF())  
        stroker.setCapStyle(self.pen.capStyle())
        return stroker.createStroke(path)
