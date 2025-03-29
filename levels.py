from cell import Cell    

def level1(scene, cells):
    player_cell = Cell(100, 100, 30, "player")

    enemy_cell = Cell(500, 300, 30, "enemy")

    scene.addItem(player_cell)
    scene.addItem(enemy_cell)

    cells.extend([enemy_cell, player_cell])

def level2(scene, cells):
    player_cell = Cell(100, 100, 30, "player")
    player_cell1 = Cell(600, 500, 30, "player")

    enemy_cell = Cell(500, 300, 30, "enemy")
    enemy_cell1 = Cell(200, 400, 30, "enemy")

    scene.addItem(player_cell)
    scene.addItem(player_cell1)
    scene.addItem(enemy_cell)
    scene.addItem(enemy_cell1)

    cells.extend([player_cell1, enemy_cell, enemy_cell1, player_cell])

def level3(scene, cells):
    player_cell1 = Cell(50, 550 - 40, 30, "player")  
    player_cell2 = Cell(200, 200, 30, "player")
    player_cell3 = Cell(750 - 60, 50, 30, "player")  

    enemy_cell1 = Cell(600, 550 - 40, 30, "enemy")  
    enemy_cell2 = Cell(750 - 60, 300, 30, "enemy")  
    enemy_cell3 = Cell(400, 100, 30, "enemy")

    scene.addItem(player_cell1)
    scene.addItem(player_cell2)
    scene.addItem(player_cell3)
    scene.addItem(enemy_cell1)
    scene.addItem(enemy_cell2)
    scene.addItem(enemy_cell3)

    cells.extend([player_cell1, player_cell2, player_cell3, enemy_cell1, enemy_cell2, enemy_cell3])
