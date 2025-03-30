import math
from game_logic import calc_distance

def suggest_best_move(cells, turn):
    best_score = -math.inf
    best_move = None

    for attacker in cells:
        if attacker.color != turn:
            continue

        for target in cells:
            if target == attacker or target in attacker.con_to:
                continue

            distance = calc_distance(attacker, target)
            if distance > attacker.hp:
                continue

            if target.color != turn:
                score = target.hp - distance
            else:
                score = -target.hp - distance

            if score > best_score:
                best_score = score
                best_move = (attacker, target)

    return best_move