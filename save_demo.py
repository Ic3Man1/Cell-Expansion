import json
import os
import xml.etree.ElementTree as ET
from pymongo import MongoClient

def save_scene_to_json(cells, attacks, pos_moves, best_move, turn, time_left, mode, ip):
    try:
        with open("game_history.json", "r") as file:
            scene_data = json.load(file) 
    except FileNotFoundError:
        scene_data = []  

    game_settings = {
        "mode": mode,
        "ip_address": ip
    }

    game_state = {
        "turn": turn,
        "turn_time": time_left
    }
    
    for cell in cells:
        cell_data = {
            "type": "cell",
            "x": cell.x(),
            "y": cell.y(),
            "hp": cell.hp,
            "color": cell.color,
            "owner": cell.owner
        }
    attack_data = {}
    for attack in attacks + pos_moves:
        attack_data = {
            "type": "attack",
            "start_x": attack.atk_center.x(),
            "start_y": attack.atk_center.y(),
            "end_x": attack.def_center.x(),
            "end_y": attack.def_center.y(),
            "color1": attack.line1_color,
            "color2": attack.line2_color
        }

    best_move_data = None
    if best_move is not None:
        best_move_data = {
            "type": "attack",
            "start_x": attack.atk_center.x(),
            "start_y": attack.atk_center.y(),
            "end_x": attack.def_center.x(),
            "end_y": attack.def_center.y(),
            "color1": attack.line1_color,
            "color2": attack.line2_color
        }

    scene_data.append({
        "game_settings": game_settings,
        "game_state": game_state,
        "cells": cell_data,
        "attacks": attack_data,
        "best_move": best_move_data
    })

    with open("game_history.json", "w") as file:
        json.dump(scene_data, file, indent=4)
        file.write("\n")

def save_scene_to_xml(cells, attacks, pos_moves, best_move, turn, time_left, mode, ip):
    if os.path.exists("game_history.xml"):
        tree = ET.parse("game_history.xml")
        root = tree.getroot()
    else:
        root = ET.Element("game_history")
        tree = ET.ElementTree(root)

    scene = ET.SubElement(root, "scene")

    game_settings = ET.SubElement(scene, "game_settings")
    ET.SubElement(game_settings, "mode").text = mode
    ET.SubElement(game_settings, "ip_address").text = ip

    game_state = ET.SubElement(scene, "game_state")
    ET.SubElement(game_state, "turn").text = turn
    ET.SubElement(game_state, "turn_time").text = str(time_left)

    cells_el = ET.SubElement(scene, "cells")
    for cell in cells:
        cell_data = ET.SubElement(cells_el, "cell")
        ET.SubElement(cell_data, "x").text = str(cell.x())
        ET.SubElement(cell_data, "y").text = str(cell.y())
        ET.SubElement(cell_data, "hp").text = str(cell.hp)
        ET.SubElement(cell_data, "color").text = cell.color
        ET.SubElement(cell_data, "owner").text = cell.owner

    attacks_el = ET.SubElement(scene, "attacks")
    for attack in attacks + pos_moves:
        attack_data = ET.SubElement(attacks_el, "attack")
        ET.SubElement(attack_data, "start_x").text = str(attack.atk_center.x())
        ET.SubElement(attack_data, "start_y").text = str(attack.atk_center.y())
        ET.SubElement(attack_data, "end_x").text = str(attack.def_center.x())
        ET.SubElement(attack_data, "end_y").text = str(attack.def_center.y())
        ET.SubElement(attack_data, "color1").text = attack.line1_color
        ET.SubElement(attack_data, "color2").text = attack.line2_color

    if best_move is not None:
        best_move_el = ET.SubElement(scene, "best_move")
        ET.SubElement(best_move_el, "start_x").text = str(best_move.atk_center.x())
        ET.SubElement(best_move_el, "start_y").text = str(best_move.atk_center.y())
        ET.SubElement(best_move_el, "end_x").text = str(best_move.def_center.x())
        ET.SubElement(best_move_el, "end_y").text = str(best_move.def_center.y())
        ET.SubElement(best_move_el, "color1").text = best_move.line1_color
        ET.SubElement(best_move_el, "color2").text = best_move.line2_color

    indent(root)
    tree.write("game_history.xml", encoding="utf-8", xml_declaration=True)


def save_scene_to_db(cells, attacks, pos_moves, best_move, turn, time_left, mode, ip):
    client = MongoClient("mongodb://localhost:27017/") 
    db = client["cell_expansion"]
    collection = db["game_history"]

    game_settings = {
        "mode": mode,
        "ip_address": ip
    }

    game_state = {
        "turn": turn,
        "turn_time": time_left
    }

    cells_data = []
    for cell in cells:
        cell_data = {
            "type": "cell",
            "x": cell.x(),
            "y": cell.y(),
            "hp": cell.hp,
            "color": cell.color,
            "owner": cell.owner
        }
        cells_data.append(cell_data)

    attacks_data = []
    for attack in attacks + pos_moves:
        attack_data = {
            "type": "attack",
            "start_x": attack.atk_center.x(),
            "start_y": attack.atk_center.y(),
            "end_x": attack.def_center.x(),
            "end_y": attack.def_center.y(),
            "color1": attack.line1_color,
            "color2": attack.line2_color
        }
        attacks_data.append(attack_data)

    best_move_data = None
    if best_move is not None:
        best_move_data = {
            "type": "attack",
            "start_x": best_move.atk_center.x(),
            "start_y": best_move.atk_center.y(),
            "end_x": best_move.def_center.x(),
            "end_y": best_move.def_center.y(),
            "color1": best_move.line1_color,
            "color2": best_move.line2_color
        }

    scene_document = {
        "game_settings": game_settings,
        "game_state": game_state,
        "cells": cells_data,
        "attacks": attacks_data,
        "best_move": best_move_data
    }

    try:
        collection.insert_one(scene_document)
    except Exception as e:
        print(f"Błąd zapisu do bazy: {e}")

def indent(elem, level=0):
    i = "\n" + level * "    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        for child in elem:
            indent(child, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
