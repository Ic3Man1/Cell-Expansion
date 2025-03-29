from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtWidgets import QGraphicsLineItem, QApplication, QLabel, QGraphicsView
from PyQt5.QtCore import QRectF, QPointF, Qt, QLineF, pyqtSlot, QPropertyAnimation, QPoint, QTimer
from attack import Attack

def select_cell(cell, turn):
    if cell.color == turn:
        cell.change_border_color("yellow")
        return cell
    else:
        show_fading_message("Not your cell")
        return None

def unselect_cell(cell):
    cell.change_border_color("black")
    return None

def stop_attack(item):
    item.attacker.hp += int(round(item.length/2))
    item.attacker.attack_dmg -= 1
    if item.attacker.owner != item.defender.owner:
        item.defender.dmg_taken -= 2
        item.defender.hp -= int(round(item.length/2))
    else:
        item.defender.hp_supply -= 2
        item.defender.hp += int(round(item.length/2))

    item.attacker.con_to.discard(item.defender)
    item.defender.whos_con.discard(item.attacker)

    scene = item.attacker.scene()
    scene.removeItem(item)

    return item

def cut_attack(item, turn):
    if turn == "green":
        if item.attacker.owner == "player":
            item.line1_color = "red"
            item.attacker.attack_dmg -= 1
            item.defender.dmg_taken -= 2
            item.attacker.hp += int(round(item.length/2))
            item.attacker.con_to.discard(item.defender)
            item.defender.whos_con.discard(item.attacker)
            item.attacker, item.defender = item.defender, item.attacker
        else:
            item.line2_color = "red"
            item.defender.attack_dmg -= 1
            item.attacker.dmg_taken -= 2
            item.defender.con_to.discard(item.attacker)
            item.attacker.whos_con.discard(item.defender)
            item.defender.hp += int(round(item.length/2))
    else:
        if item.attacker.owner == "enemy":
            item.line1_color = "green"
            item.attacker.attack_dmg -= 1
            item.defender.dmg_taken -= 2
            item.attacker.hp += int(round(item.length/2))
            item.attacker.con_to.discard(item.defender)
            item.defender.whos_con.discard(item.attacker)
            item.attacker, item.defender = item.defender, item.attacker
        else:
            item.line2_color = "green"
            item.defender.attack_dmg -= 1
            item.attacker.dmg_taken -= 2
            item.defender.con_to.discard(item.attacker)
            item.attacker.whos_con.discard(item.defender)
            item.defender.hp += int(round(item.length/2))

def separate(attacks, item, turn):
    if item.line1_color != item.line2_color:
        cut_attack(item, turn)
    else:
        if item.line1_color == turn:
            attack = stop_attack(item)
            attacks.remove(attack)
            turn = switch_turn(turn)
        else:
            show_fading_message("You can't cut not your line")
    return turn

def merge_cells(attacker, defender):
    color = "green" if attacker.owner == "player" else "red"
    distance = calc_distance(attacker, defender)
    attacker.change_border_color("black")
    attack_line = Attack(attacker, defender, color, color)

    scene = attacker.scene()
    scene.addItem(attack_line)

    attacker.hp -= distance
    attacker.attack_dmg += 1
    if defender.owner != attacker.owner:
        defender.dmg_taken += 2
    else:
        defender.hp_supply += 2

    attacker.con_to.add(defender)
    defender.whos_con.add(attacker)

    return None, attack_line

def remerge_cells(merge, attacker, defender):
    distance = int(round(calc_distance(attacker, defender)/2))
    attacker.change_border_color("black")
    attacker.hp -= distance
    defender.hp += distance
    attacker.attack_dmg += 1
    if defender.owner != attacker.owner:
        defender.dmg_taken += 2
    else:
        defender.hp_supply += 2

    attacker.con_to.add(defender)
    defender.whos_con.add(attacker)

    color = select_color(attacker)
    merge.line2_color = color

    return None
    
def merge(attacks, selected_cell, item, turn):
    for i in attacks:
        if i.attacker == item and i.defender == selected_cell:
            if i.attacker.owner != i.defender.owner and int(round(calc_distance(selected_cell, item)/2)) < selected_cell.hp:
                cell = remerge_cells(i, selected_cell, item)
                turn = switch_turn(turn)
                return cell, turn
            else:
                show_fading_message("Mismove")
                return selected_cell, turn
    if calc_distance(selected_cell, item) < selected_cell.hp:
        cell, attack = merge_cells(selected_cell, item)
        attacks.append(attack)
        turn = switch_turn(turn)
    else:
        show_fading_message("Mismove")
        return selected_cell, turn
    return cell, turn

def calc_distance(attacker, defender):
    atk_center = attacker.boundingRect().center() + attacker.pos()
    def_center = defender.boundingRect().center() + defender.pos()
    help_line = QLineF(atk_center, def_center)

    return int(help_line.length()/20)

def select_color(attacker):
    if attacker.owner == "player":
        color = "green"
    else:
        color = "red"
    return color

def switch_turn(turn):
    if turn == "green":
        return "red"
    else:
        return "green"
    
def retrieve_cell(cell, attacks):
    for attack in attacks:
        if attack.attacker == cell and attack.defender not in cell.whos_con:
            attack.line1_color = "red" if attack.attacker.owner == "player" else "green"
            attack.line2_color = "red" if attack.attacker.owner == "player" else "green"
        elif (attack.attacker == cell or attack.defender == cell):
            cut_attack(attack, cell.color)
            attack.line1_color = "green" if attack.attacker.owner == "player" else "red"
            attack.line2_color = "green" if attack.attacker.owner == "player" else "red"

        if attack.attacker.owner == attack.defender.owner and (attack.attacker == cell or attack.defender == cell):
            attack.defender.hp_supply -= 2
            attack.defender.dmg_taken += 2
        elif (attack.attacker == cell or attack.defender == cell):
            attack.defender.hp_supply += 2
            attack.defender.dmg_taken -= 2
    cell.hp = 1
    cell.owner = "enemy" if cell.owner == "player" else "player"
    return attacks

def show_fading_message(message, duration=1500):
    label = QLabel(message)
    label.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    label.setAttribute(Qt.WA_TranslucentBackground)
    label.setStyleSheet("font-size: 22px; color: white; background-color: rgba(0, 0, 0, 180); padding: 10px;")
    label.adjustSize()
    label.show()

    screen_geometry = QApplication.instance().desktop().screenGeometry()
    label.move(screen_geometry.center() - label.rect().center())

    animation = QPropertyAnimation(label, b"windowOpacity")
    animation.setDuration(duration)
    animation.setStartValue(1)
    animation.setEndValue(0)
    animation.finished.connect(label.deleteLater)
    animation.start()

    QTimer.singleShot(duration, lambda: animation.start())