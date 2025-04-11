import socket
import threading
import json

class NetworkHandler:
    def __init__(self, is_host, ip, port, on_receive_callback):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.callback = on_receive_callback

        if is_host:
            self.sock.bind(("0.0.0.0", port))
            self.sock.listen(1)
            print("[Serwer] Oczekiwanie na połączenie...")
            self.conn, addr = self.sock.accept()
            print(f"[Serwer] Połączono z {addr}")
        else:
            self.sock.connect((ip, port))
            self.conn = self.sock
            print(f"[Klient] Połączono z serwerem {ip}:{port}")

        threading.Thread(target=self.listen, daemon=True).start()

    def listen(self):
        while True:
            try:
                data = self.conn.recv(4096).decode()
                if not data:
                    break
                parsed = json.loads(data)
                self.callback(parsed)
            except Exception as e:
                print("[Błąd odbioru]", e)
                break

    def send(self, data_dict):
        try:
            payload = json.dumps(data_dict).encode()
            self.conn.sendall(payload)
        except Exception as e:
            print("[Błąd wysyłania]", e)

    def is_connected(self):
        return self.conn is not None

def save_current_scene(cells, attacks, pos_moves, best_move, turn, time_left, mode, ip):
    scene_data = [] 
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
            "x": cell.x,
            "y": cell.y,
            "hp": cell.hp,
            "color": cell.color,
            "owner": cell.owner
        }
        cells_data.append(cell_data)

    

    attacks_data = []
    attack_data = {}
    for attack in attacks: # + pos_moves
        attack_data = {
            "type": "attack",
            "start_x": attack.attacker.x,
            "start_y": attack.attacker.y,
            "end_x": attack.defender.x,
            "end_y": attack.defender.y,
            "color1": attack.line1_color,
            "color2": attack.line2_color
        }
        attacks_data.append(attack_data)
    # best_move_data = {}
    # if best_move is not None:
    #     best_move_data = {
    #         "type": "best_move",
    #         "start_x": best_move.attacker.x,
    #         "start_y": best_move.attacker.y,
    #         "end_x": best_move.defender.x,
    #         "end_y": best_move.defender.y,
    #     }

    scene_data.append({
        "game_settings": game_settings,
        "game_state": game_state,
        "cells": cells_data,
        "attacks": attacks_data,
        #"best_move": best_move_data
    })

    return scene_data
