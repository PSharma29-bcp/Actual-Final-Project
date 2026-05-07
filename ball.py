import pygame
import math

colors = [(255,251,0), (0,47,255), (255,0,0), (152, 0, 255), (255,136,0), (36, 194, 36), (115,1,1)]
outs = []
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

    def reset(self):
        self.x = 448
        self.y = 200
        self.dx = 0
        self.dy = 0

    def out(self):
        outs.append((self.type, self.color))
        self.x = ((len(outs) + 1) * 10)
        self.y = 10
        self.dx = 0
        self.dy
    
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

    def shoot(self, dx, dy,strength):
        self.dx = dx * strength
        self.dy = dy * strength

    def move(self):
        self.x += self.dx
        self.y += self.dy

        self.dx *= 0.995
        self.dy *= 0.995

        if abs(self.dx) < 0.05:
            self.dx = 0
        if abs(self.dy) < 0.05:
            self.dy = 0

        if self.in_hole(75,75) and self.type == 3:
            self.reset()
        if self.in_hole(625,75) and self.type == 3:
            self.reset()
        if self.in_hole(75,325) and self.type == 3:
            self.reset()
        if self.in_hole(625,325) and self.type == 3:
            self.reset()

        if self.in_hole(75,75) and (self.type == 1 or self.type == 2 or self.type == 8):
            self.out()
        if self.in_hole(625,75) and (self.type == 1 or self.type == 2 or self.type == 8):
            self.out()
        if self.in_hole(75,325) and (self.type == 1 or self.type == 2 or self.type == 8):
            self.out()
        if self.in_hole(625,325) and (self.type == 1 or self.type == 2 or self.type == 8):
            self.out()

        if self.y < 70 + self.radius:
            self.y = 70 + self.radius
            self.dy *= -1
        if self.y > 330 - self.radius:
            self.y = 330 - self.radius
            self.dy *= -1
        if self.x < 70 + self.radius:
            self.x = 70 + self.radius
            self.dx *= -1
        if self.x > 630 - self.radius:
            self.x = 630 - self.radius
            self.dx *= -1

        # needs the strength to change how many pixels it moves each time
        # at strength 1, it moves 1 fps
        # at strength 15, is 15 fps
        # the distance changes as well as how much per second, should not stay same

    def in_hole(self, hole_x, hole_y):
        distance = math.sqrt((self.x - hole_x)**2 + (self.y - hole_y)**2)
        return distance < 15 # 15 is hole radius
    
    def collide(self, other):
        dx = other.x - self.x
        dy = other.y - self.y

        distance = math.sqrt(dx**2 + dy**2)

        if distance == 0:
            return
        
        if distance < self.radius + other.radius:
            nx = dx/distance
            ny = dy/distance

            overlap = (self.radius + other.radius) - distance

            self.x -= nx * overlap/2
            self.y -= ny * overlap/2
            other.x += nx * overlap/2
            other.y += ny * overlap/2

            dvx = self.dx - other.dx
            dvy = self.dy - other.dy

            dot = dvx * nx + dvy * ny

            # will only collide if balls are moving
            if dot > 0:
                return
            
            impulse = dot
            
            self.dx -= impulse * nx
            self.dy -= impulse * ny
            other.dx += impulse * nx
            other.dy += impulse * ny

            other.dx *= 0.99
            other.dy *= 0.99

