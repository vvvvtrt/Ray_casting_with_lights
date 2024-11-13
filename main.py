import pygame
from settings import *
from player import Player
import math
from map import world_map, light_map
from ray_casting import ray_casting
from pygame.locals import *
import Pygame_Lights

pygame.init()
sc = pygame.display.set_mode((WIDTH + 300, HEIGHT))
pygame.display.set_caption("DOOM RTX")
clock = pygame.time.Clock()
player = Player()

direction_flags = [True for _ in range(len(light_map))]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    player.movement()
    sc.fill(BLACK)
    sc.fill((255, 255, 255))
    pygame.draw.rect(sc, WHITE, (0, 0, WIDTH, HALF_HEIGHT))



    light_size = 85

    # Create multiple lights with the same size
    lights = [
        Pygame_Lights.LIGHT(light_size, Pygame_Lights.pixel_shader(light_size, (233, 107, 106), 1, False)),
        Pygame_Lights.LIGHT(light_size, Pygame_Lights.pixel_shader(light_size, (171, 209, 232), 1, False)),
        Pygame_Lights.LIGHT(light_size, Pygame_Lights.pixel_shader(light_size, (130, 48, 102), 1, False))
    ]

    # Define positions and movement directions for each light

    light_positions = [(WIDTH + i[0] // scale_map, i[1] // scale_map) for i in light_map]

    squares = []
    for x,y in world_map:
        squares.append(pygame.draw.rect(sc, DARKGRAY, (WIDTH + x // scale_map, y // scale_map, TILE // scale_map, TILE // scale_map)   ))

    lights_display = pygame.Surface((sc.get_size()))
    lights_display.blit(Pygame_Lights.global_light(sc.get_size(), 25), (0, 0))

    # Update light positions and apply them
    for i, light in enumerate(lights):
        light.main(squares, lights_display, *light_positions[i])

    sc.blit(lights_display, (0, 0), special_flags=BLEND_RGBA_MULT)

    pygame.draw.rect(sc, DARKGRAY, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

    ray_casting(sc, player.pos, player.angle)
    pygame.draw.circle(sc, GREEN, (WIDTH + int(player.x) // scale_map, int(player.y) // scale_map), 6)

    for i in range(len(light_map)):
        if direction_flags[i]:
            light_map[i][1] += 2
        else:
            light_map[i][1] -= 2

        if light_map[i][1] < 100:
            direction_flags[i] = True
        elif light_map[i][1] > 600:
            direction_flags[i] = False


    # pygame.draw.line(sc, GREEN, player.pos, (player.x // scale_map + WIDTH * math.cos(player.angle) // scale_map,
    #                                           player.y // scale_map + WIDTH * math.sin(player.angle) // scale_map), 2)

    pygame.display.flip()
    clock.tick(FPS)
    # print(clock.get_fps())