from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtWidgets import QGraphicsLineItem
from attack import Attack


# def draw_line_between_cells(scene, cell1, cell2):
#     cell1_center = cell1.boundingRect().center() + cell1.pos()
#     cell2_center = cell2.boundingRect().center() + cell2.pos()
#     mid = QPointF((cell1_center.x() + cell2_center.x()) / 2, (cell1_center.y() + cell2_center.y()) / 2)

#     line1 = QGraphicsLineItem(cell1_center.x(), cell1_center.y(), mid.x(), mid.y())
#     line_pen = QPen(QColor("green"))
#     line_pen.setWidth(5)
#     line1.setPen(line_pen)
    
#     line2 = QGraphicsLineItem(mid.x(), mid.y(), cell2_center.x(), cell2_center.y())
#     line_pen = QPen(QColor("green"))
#     line_pen.setWidth(5)
#     line2.setPen(line_pen)

#     scene.addItem(line1)
#     scene.addItem(line2)

def select_cell(cell):
    cell.change_border_color("yellow")
    return cell

def unselect_cell(cell):
    cell.change_border_color("black")
    return None

def attack_cell(selected_cell, item):
    selected_cell.change_border_color("black")
    #draw_line_between_cells(selected_cell.scene(), selected_cell, item)
    attack_line = Attack(selected_cell, item)
    scene = selected_cell.scene()
    scene.addItem(attack_line)
    selected_cell.attack_dmg += 1
    item.dmg_taken += 2
    selected_cell.con_to.add(item)
    return None

def stop_attack():
    pass
