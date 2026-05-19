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
HOLE_RADIUS = 20

FPS = 120 # Frames per second (used with clock)

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

def balls_stopped(balls):
    for ball in balls:
        if ball.dx != 0 or ball.dy != 0:
            return False
        
    return True

def main(): # The game loop
    running = True

    game_state = "START"
    winner = None

    turn = 1
    clicks = 0
    player1_type = None
    player2_type = None
    current_player = 1
    turn_continues = False
    assignment_done = False
    turn_switched = False

    shot_in_progress = False
    pocketed_this_shot = []

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

    balls = [yellow_striped, blue_striped, red_striped, purple_striped, orange_striped, green_striped,
            maroon_striped, yellow_solid, blue_solid, red_solid, purple_solid, orange_solid, green_solid,
            maroon_solid, eight_ball, cue_ball]
    outs = []

    while running:
        
        screen.fill(BG_COLOR)

        font_big = pygame.font.SysFont("Arial", 40)
        font_small = pygame.font.SysFont("Arial", 20)

        

        if game_state == "START":
            title = font_big.render("POOL GAME", True, (255,255,255))
            prompt = font_small.render("Click to Start", True, (200,200,200))

            screen.blit(title, (WIDTH//2 - 100, HEIGHT//2 - 40))
            screen.blit(prompt, (WIDTH//2 - 70, HEIGHT//2 + 10))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    game_state = "PLAYING"

            continue
        
        if game_state == "PLAYING":
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

            for ball in balls:
                ball.move()

            for i in range(len(balls)):
                for j in range(i+1, len(balls)):
                    balls[i].collide(balls[j])

            for ball in balls:
                ball.display(screen)

            for ball in balls:
                if ball.pocketed and ball not in outs:
                    outs.append(ball)
                    pocketed_this_turn.append(ball)



            mx, my = pygame.mouse.get_pos()

            dir_x = mx - cue_ball.x
            dir_y = my - cue_ball.y

            distance_squared = dir_x * dir_x + dir_y * dir_y

            if distance_squared <= 0:
                total_distance = 1
            else:
                total_distance = math.sqrt(distance_squared)

            dir_x = dir_x / total_distance
            dir_y = dir_y / total_distance


            if cue_ball.dx == 0 or cue_ball.dy == 0 or cue_ball.dx != 0 or cue_ball.dy != 0:
                starting_x = cue_ball.x + dir_x * 20
                starting_y = cue_ball.y + dir_y * 20

                stick_length = 120
                ending_x = starting_x + dir_x * stick_length
                ending_y = starting_y + dir_y * stick_length

                cue_stick = pygame.draw.line(screen, STICK_COLOR, (starting_x, starting_y),
                                            (ending_x, ending_y), width = 10)
                # Cue stick is moved by the mouse's position and angle to the cue ball

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

                #rect(surface, color, rect, width=0, border_radius=0, border_top_left_radius=-1, 
                # border_top_right_radius=-1, border_bottom_left_radius=-1, 
                # border_bottom_right_radius=-1) -> Rect
                out_ball_holder = pygame.draw.rect(screen, (255, 255, 0), (50,5,600,40), 5, 25)

            starting_x = 85
            starting_y = 25
            spacing = 35

            for i, ball in enumerate(outs):
                ball_x = starting_x + i * spacing
                ball.y = starting_y
                ball.dx = 0
                ball.dy = 0
                ball.display(screen)

            # Displaying the players and their types
            font = pygame.font.SysFont("Arial", 16)

            def type_color(t):
                if t == 1:
                    return (255, 220, 80)   # stripes
                if t == 2:
                    return (80, 255, 120)   # solids
                return (180, 180, 180)     # unassigned

            # Player 1 text
            p1_text = "Player 1: "
            if player1_type == 1:
                p1_text += "Stripes"
            elif player1_type == 2:
                p1_text += "Solids"
            else:
                p1_text += "Unassigned"

            # Player 2 text
            p2_text = "Player 2: "
            if player2_type == 1:
                p2_text += "Stripes"
            elif player2_type == 2:
                p2_text += "Solids"
            else:
                p2_text += "Unassigned"

            turn_text = f"Current Turn: Player {current_player}"

            # draw text
            screen.blit(font.render(p1_text, True, type_color(player1_type)), (660, 40))
            screen.blit(font.render(p2_text, True, type_color(player2_type)), (660, 70))
            screen.blit(font.render(turn_text, True, (255,255,0)), (660, 100))

            # little indicator dots (optional but nice)
            pygame.draw.circle(screen, type_color(player1_type), (650, 47), 5)
            pygame.draw.circle(screen, type_color(player2_type), (650, 77), 5)


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
                if cue_ball.dx == 0 or cue_ball.dy == 0 or cue_ball.dx != 0 or cue_ball.dy != 0:
                    cue_ball.shoot(-dir_x, -dir_y, clicks)

                shot_in_progress = True
                turn_switched = False
                pocketed_this_turn = []


                
            if event.type == pygame.MOUSEBUTTONUP:
                pass

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    pass
                    
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    pass
        

        if shot_in_progress and balls_stopped(balls):
            shot_in_progress = False

            pocketed_this_shot = pocketed_this_turn

            print("SHOT RESULT TYPES:", [b.type for b in pocketed_this_turn])
            print("ASSIGNED FLAG:", assignment_done)
            print("PLAYER1:", player1_type, "PLAYER2:", player2_type)

            if not assignment_done:
                for ball in pocketed_this_shot:
                    if ball.type in [1,2]:
                        if current_player == 1:
                            player1_type = ball.type
                            player2_type = 2 if ball.type == 1 else 1
                            # simple win condition: 8-ball pocketed
                            for ball in outs:
                                if ball.type == 8:
                                    winner = current_player
                                    game_state = "END"
                        else:
                            player2_type = ball.type
                            player1_type = 2 if ball.type == 1 else 1

                        assignment_done = True
                        print("ASSIGNED SUCCESS:", player1_type, player2_type)
                        break
            
            # Determine if player keeps turn
            keep_turn = False
            
            for ball in pocketed_this_shot:
                if current_player == 1 and ball.type == player1_type:
                    keep_turn = True

                if current_player == 2 and ball.type == player2_type:
                    keep_turn = True

            if not keep_turn:
                current_player = 2 if current_player == 1 else 1

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()






