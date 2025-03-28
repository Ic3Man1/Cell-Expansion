from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtWidgets import QGraphicsLineItem
from attack import Attack

def select_cell(cell):
    cell.change_border_color("yellow")
    return cell

def unselect_cell(cell):
    cell.change_border_color("black")
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

def merge_cells(attacker, defender):
    attacker.change_border_color("black")
    attack_line = Attack(attacker, defender)
    scene = attacker.scene()
    scene.addItem(attack_line)
    attacker.attack_dmg += 1
    if defender.owner != attacker.owner:
        defender.dmg_taken += 2
    else:
        defender.hp_supply += 2
    attacker.con_to.add(defender)
    defender.con_to.add(attacker)
    return None

