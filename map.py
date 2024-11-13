from settings import *

text_map = [
    'WWWWWWWWWWWW',
    'WLW...WW...W',
    'W.........WW',
    'W..WW..W..WW',
    'W..WWL.W...W',
    'W..W...W...W',
    'W..WW....L.W',
    'WWWWWWWWWWWW'
]

world_map = set()
light_map = []

for j, row in enumerate(text_map):
    for i, char in enumerate(row):
        if char == 'W':
            world_map.add((i * TILE, j * TILE))
        elif char == "L":
            light_map.append([i * TILE + 50, j * TILE])


