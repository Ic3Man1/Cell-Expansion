import json
import xml.etree.ElementTree as ET
from pymongo import MongoClient

def save_scene_to_json(cells, attacks, pos_moves, best_move, turn, time_left, mode, ip):

        scene_data = []

        game_settings = {
            "mode": mode,
            "ip_address": ip
        }
        scene_data.append(game_settings)

        game_state = {
            "turn": turn,
            "turn_time": time_left
        }
        scene_data.append(game_state)
        
        for cell in cells:
            cell_data = {
                "type": "cell",
                "x": cell.x(),
                "y": cell.y(),
                "hp": cell.hp,
                "color": cell.color,
                "owner": cell.owner
            }
            scene_data.append(cell_data)

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
            scene_data.append(attack_data)

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
            scene_data.append(best_move_data)

        with open("game_history.json", "a") as file:
            json.dump(scene_data, file)
            file.write("\n")

import xml.etree.ElementTree as ET

def save_scene_to_xml(cells, attacks, pos_moves, best_move, turn, time_left, mode, ip):
    root = ET.Element("game_data")

    game_settings = ET.SubElement(root, "game_settings")
    ET.SubElement(game_settings, "mode").text = mode
    ET.SubElement(game_settings, "ip_address").text = ip

    game_state = ET.SubElement(root, "game_state")
    ET.SubElement(game_state, "turn").text = turn
    ET.SubElement(game_state, "turn_time").text = str(time_left)

    for cell in cells:
        cell_data = ET.SubElement(root, "cell")
        ET.SubElement(cell_data, "x").text = str(cell.x())
        ET.SubElement(cell_data, "y").text = str(cell.y())
        ET.SubElement(cell_data, "hp").text = str(cell.hp)
        ET.SubElement(cell_data, "color").text = cell.color
        ET.SubElement(cell_data, "owner").text = cell.owner

    for attack in attacks + pos_moves:
        attack_data = ET.SubElement(root, "attack")
        ET.SubElement(attack_data, "start_x").text = str(attack.atk_center.x())
        ET.SubElement(attack_data, "start_y").text = str(attack.atk_center.y())
        ET.SubElement(attack_data, "end_x").text = str(attack.def_center.x())
        ET.SubElement(attack_data, "end_y").text = str(attack.def_center.y())
        ET.SubElement(attack_data, "color1").text = attack.line1_color
        ET.SubElement(attack_data, "color2").text = attack.line2_color

    if best_move is not None:
        best_move_data = ET.SubElement(root, "best_move")
        ET.SubElement(best_move_data, "start_x").text = str(best_move.atk_center.x())
        ET.SubElement(best_move_data, "start_y").text = str(best_move.atk_center.y())
        ET.SubElement(best_move_data, "end_x").text = str(best_move.def_center.x())
        ET.SubElement(best_move_data, "end_y").text = str(best_move.def_center.y())
        ET.SubElement(best_move_data, "color1").text = best_move.line1_color
        ET.SubElement(best_move_data, "color2").text = best_move.line2_color

    tree = ET.ElementTree(root)
    tree.write("game_history.xml")

def save_scene_to_db(cells, attacks, pos_moves, best_move, turn, time_left, mode, ip):
    client = MongoClient("mongodb+srv://<username>:<password>@cluster0.mongodb.net/test?retryWrites=true&w=majority")
    db = client["game_db"]
    collection = db["game_history"]

    scene_data = {}

    scene_data["game_settings"] = {
        "mode": mode,
        "ip_address": ip
    }

    scene_data["game_state"] = {
        "turn": turn,
        "turn_time": time_left
    }

    scene_data["cells"] = []
    for cell in cells:
        cell_data = {
            "x": cell.x(),
            "y": cell.y(),
            "hp": cell.hp,
            "color": cell.color,
            "owner": cell.owner
        }
        scene_data["cells"].append(cell_data)

    scene_data["attacks_and_moves"] = []
    for attack in attacks + pos_moves:
        attack_data = {
            "start_x": attack.atk_center.x(),
            "start_y": attack.atk_center.y(),
            "end_x": attack.def_center.x(),
            "end_y": attack.def_center.y(),
            "color1": attack.line1_color,
            "color2": attack.line2_color
        }
        scene_data["attacks_and_moves"].append(attack_data)

    if best_move is not None:
        best_move_data = {
            "start_x": best_move.atk_center.x(),
            "start_y": best_move.atk_center.y(),
            "end_x": best_move.def_center.x(),
            "end_y": best_move.def_center.y(),
            "color1": best_move.line1_color,
            "color2": best_move.line2_color
        }
        scene_data["best_move"] = best_move_data

    collection.insert_one(scene_data)