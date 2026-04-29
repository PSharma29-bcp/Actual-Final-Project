import sys
import pygame
import random
import os
import math
os.environ['SDL_AUDIODRIVER'] = 'dsp'

from ball import Ball

# Screen Dimensions
WIDTH = 800
HEIGHT = 400

# Constants
TABLE_WIDTH = 600
TABLE_HEIGHT = 300
BALL_RADIUS = 12
HOLE_RADIUS = 15

FPS = 30 # Frames per second (used with clock)

# RGB Values of screen objects
BG_COLOR = (0,0,0)
WOOD_COLOR = (179, 104, 5)
TABLE_COLOR = (0,255,0)
HOLE_COLOR = (74,74,74)
STICK_COLOR = (242, 164, 80)

# Yellow, Blue, Red, Purple, Orange, Green, Maroon
YELLOW = (255,251,0)
BLUE = (0,47,255)
RED = (255,0,0)
PURPLE = (152, 0, 255)
ORANGE = (255,136,0)
GREEN = (36, 194, 36)
MAROON = (115,1,1)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

pygame.display.set_caption("Pool")

def main(): # The game loop
    running = True
    turn = 1
    clicks = 0

    # Last parameter for balls is the type, so 0 for hole, 1 for striped, 2 for solid, 
    # 3 for cue, and 8 for 8-ball
    # Striped balls and their placement
    yellow_striped = Ball(BALL_RADIUS, 348, 200, YELLOW, 0, 0, 1)
    blue_striped = Ball(BALL_RADIUS, 304, 176, BLUE, 0, 0, 1)
    red_striped = Ball(BALL_RADIUS, 326, 188, RED, 0, 0, 1)
    purple_striped = Ball(BALL_RADIUS, 260, 152, PURPLE, 0, 0, 1)
    orange_striped = Ball(BALL_RADIUS, 260, 176, ORANGE, 0, 0, 1)
    green_striped = Ball(BALL_RADIUS, 260, 200, GREEN, 0, 0, 1)
    maroon_striped = Ball(BALL_RADIUS, 282, 164, MAROON, 0,0,1)

    # Solid balls and their placement
    yellow_solid = Ball(BALL_RADIUS, 282, 188, YELLOW, 0, 0, 2)
    blue_solid = Ball(BALL_RADIUS, 282, 212, BLUE, 0, 0, 2)
    red_solid = Ball(BALL_RADIUS, 282, 236, RED, 0, 0, 2)
    purple_solid = Ball(BALL_RADIUS, 326, 212, PURPLE, 0, 0, 2)
    orange_solid = Ball(BALL_RADIUS, 304, 200, ORANGE, 0, 0, 2)
    green_solid = Ball(BALL_RADIUS, 304, 224, GREEN, 0, 0, 2)       
    maroon_solid = Ball(BALL_RADIUS, 260, 224, MAROON, 0,0,2)

    # Where the 8-ball is placed
    eight_ball = Ball(BALL_RADIUS, 260, 248, (0,0,0), 0,0,8)

    # Where the cue ball is placed
    cue_ball = Ball(BALL_RADIUS, 448, 200, (255,255,255), 0,0,3)

    while running:
        screen.fill(BG_COLOR)
        
        table_perimeter = pygame.draw.rect(screen, WOOD_COLOR, (50,50,TABLE_WIDTH, TABLE_HEIGHT))
        table_cloth = pygame.draw.rect(screen, TABLE_COLOR, (70,70,TABLE_WIDTH-40,TABLE_HEIGHT-40))
        top_left_hole = Ball(HOLE_RADIUS, 75, 75, HOLE_COLOR, 0, 0, 0)
        top_left_hole.display(screen)
        top_right_hole = Ball(HOLE_RADIUS, 625, 75, HOLE_COLOR, 0, 0, 0)
        top_right_hole.display(screen)
        bottom_left_hole = Ball(HOLE_RADIUS, 75, 325, HOLE_COLOR, 0, 0, 0)
        bottom_left_hole.display(screen)
        bottom_right_hole = Ball(HOLE_RADIUS, 625, 325, HOLE_COLOR, 0, 0, 0)
        bottom_right_hole.display(screen)

        yellow_striped.display(screen)
        blue_striped.display(screen)
        red_striped.display(screen)
        purple_striped.display(screen)
        orange_striped.display(screen)
        green_striped.display(screen)
        maroon_striped.display(screen)

        yellow_solid.display(screen)
        blue_solid.display(screen)
        red_solid.display(screen)
        purple_solid.display(screen)
        orange_solid.display(screen)
        green_solid.display(screen)
        maroon_solid.display(screen)

        eight_ball.display(screen)
        cue_ball.display(screen)


        mx, my = pygame.mouse.get_pos()
        distance_x = mx - cue_ball.x
        distance_y = my - cue_ball.y

        distance_squared = distance_x * distance_x + distance_y * distance_y

        if distance_squared <= 0:
            total_distance = 1
        else:
            total_distance = math.sqrt(distance_squared)

        distance_x = distance_x / total_distance
        distance_y = distance_y / total_distance

        starting_x = cue_ball.x + distance_x * 20
        starting_y = cue_ball.y + distance_y * 20

        stick_length = 120
        ending_x = starting_x + distance_x * stick_length
        ending_y = starting_y + distance_y * stick_length

        cue_stick = pygame.draw.line(screen, STICK_COLOR, (starting_x, starting_y),
                                    (ending_x, ending_y), width = 10)
        # Cue stick is moved by the mouse's position and angle to the cue ball
        run = ending_x - starting_x
        rise = ending_y - starting_y






        # The menu for controlling the cue stick
        stick_strength_menu = pygame.draw.rect(screen, (255,255,255), (5,50,35, TABLE_HEIGHT))
        if 20 * clicks > 300:
            clicks = 15
        elif clicks < 0:
            clicks = 0
        else:
            stick_strength_bar = pygame.draw.rect(screen, (255, 0, 0), (5,50,35, (20*clicks)))
        font = pygame.font.SysFont("Arial", 22)
        text_surface = font.render(("MIN"), True, (255,255,255))
        screen.blit(text_surface, (5,20))
        text_surface = font.render(("MAX"), True, (255,255,255))
        screen.blit(text_surface, (5,350))
        # Bar will be controlled by up and down arrow keys




        pygame.display.update()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    clicks += 1

                if event.key == pygame.K_DOWN:
                    clicks -= 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(clicks):
                    cue_ball.move(-run, -rise, clicks/6)
            if event.type == pygame.MOUSEBUTTONUP:
                pass

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    pass
                    
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    pass


if __name__ == "__main__":
    main()
    pygame.quit()






