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

def attack_cell(attacker, defender):
    attacker.change_border_color("black")
    #draw_line_between_cells(attacker.scene(), attacker, defender)
    attack_line = Attack(attacker, defender)
    scene = attacker.scene()
    scene.addItem(attack_line)
    attacker.attack_dmg += 1
    defender.dmg_taken += 2
    attacker.con_to.add(defender)
    defender.con_to.add(attacker)
    return None

def stop_attack(item):
    item.attacker.attack_dmg -= 1
    if item.attacker.owner != item.defender.owner:
        item.defender.dmg_taken -= 2
    else:
        item.defender.hp_supply -= 2

    item.attacker.con_to.discard(item.defender)
    item.defender.con_to.discard(item.attacker)
    scene = item.attacker.scene()
    scene.removeItem(item)

def support_cell(cell, item):
    cell.change_border_color("black")
    support_line = Attack(cell, item)
    scene = cell.scene()
    scene.addItem(support_line)
    cell.attack_dmg += 1
    item.hp_supply += 2
    cell.con_to.add(item)
    item.con_to.add(cell)
    return None

