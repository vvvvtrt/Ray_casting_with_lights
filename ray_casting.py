import pygame
import math
from settings import *
from map import world_map, light_map

def is_visible_from_light(x, y, lx, ly):
    angle_to_wall = math.atan2(y - ly, x - lx)
    sin_a = math.sin(angle_to_wall)
    cos_a = math.cos(angle_to_wall)
    eps = 2

    for depth in range(1, int(math.sqrt((x - lx) ** 2 + (y - ly) ** 2))):
        check_x = lx + depth * cos_a
        check_y = ly + depth * sin_a

        # Если на пути есть стена, то путь блокирован
        if (check_x // TILE * TILE, check_y // TILE * TILE) in world_map and abs(check_x - x) > eps and abs(check_y - y) > eps:
            return False
    return True

def ray_casting(sc, player_pos, player_angle):
    cur_angle = player_angle - HALF_FOV
    xo, yo = player_pos

    for ray in range(NUM_RAYS):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)

        for depth in range(1, MAX_DEPTH):
            x = xo + depth * cos_a
            y = yo + depth * sin_a


            wall_pos = (x // TILE * TILE, y // TILE * TILE)
            if wall_pos in world_map:
                depth *= math.cos(player_angle - cur_angle)
                proj_height = min(PROJ_COEFF / (depth + 0.0001), HEIGHT)

                final_color = list(base_color)

                for i, (lx, ly) in enumerate(light_map):
                    lr, lg, lb = light_colors[i]

                    if is_visible_from_light(x, y, lx, ly):
                        light_distance = math.sqrt((x - lx) ** 2 + (y - ly) ** 2)
                        light_intensity = max(0, 255 - int(light_distance * 1.5)) / 255

                        final_color[0] += lr * light_intensity
                        final_color[1] += lg * light_intensity
                        final_color[2] += lb * light_intensity

                final_color = tuple(min(255, int(c)) for c in final_color)

                pygame.draw.rect(sc, final_color, (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))
                break

        cur_angle += DELTA_ANGLE
