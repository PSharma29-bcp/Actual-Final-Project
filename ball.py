import pygame

colors = [(255,251,0), (0,47,255), (255,0,0), (152, 0, 255), (255,136,0), (36, 194, 36), (115,1,1)]
balls = []
# Yellow, Blue, Red, Purple, Orange, Green, Maroon

class Ball:
    def __init__(self, radius, x, y, color, dx, dy, type):
        self.radius = radius
        self.x = x
        self.y = y
        self.color = color
        self.dx = dx
        self.dy = dy
        self.type = type


    
    def display(self, screen):

        font = pygame.font.SysFont("Arial", 22)

        if self.type == 0:
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        elif self.type == 1:
            # Is a striped
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
            pygame.draw.rect(screen, (255,255,255), (self.x-5, self.y-10,10,20))
            for i in range(len(colors)):
                if colors[i] == self.color:
                    ball_number = i+1
                    ball_number += 9

                    ball_number = str(ball_number)
                    text_surface = font.render(ball_number, True, (0,0,0))
                    screen.blit(text_surface, (self.x-10, self.y-12))
        elif self.type == 2:
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
            pygame.draw.circle(screen, (255,255,255), (self.x, self.y), self.radius//2)
            for i in range(len(colors)):
                if colors[i] == self.color:
                    ball_number = i+1

                    ball_number = str(ball_number)
                    text_surface = font.render(ball_number, True, (0,0,0))
                    screen.blit(text_surface, (self.x-5, self.y-12))
        elif self.type == 3:
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
            pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius//4)

        elif self.type == 8:
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
            pygame.draw.circle(screen, (255,255,255), (self.x, self.y), self.radius//2)
            ball_number = "8"
            text_surface = font.render(ball_number, True, (0,0,0))
            screen.blit(text_surface, (self.x-5, self.y-12))

    def move(self, dx, dy, strength):
        self.x += dx
        self.y += dy

        # needs the strength to change how many pixels it moves each time
        # at strength 1, it moves 1 fps
        # at strength 15, is 15 fps
        # the distance changes as well as how much per second, should not 