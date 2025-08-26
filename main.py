import pygame
import math

class MoveableObject:
    def __init__(self, pos: pygame.Vector2, color: str, radius: int):
        self.pos = pos
        self.color = color
        self.radius = radius

class Platform(MoveableObject):
    def __init__(self, pos: pygame.Vector2, color: str, radius: int):
        super().__init__(pos, color, radius)
        self.score = 0

    def moveObject(self, isLeft: bool, dt: int):
        self.pos.x += dt * (500 if not isLeft else -500)

class Ball(MoveableObject):
    def __init__(self, pos: pygame.Vector2, color: str, radius: int, isDown: bool):
        super().__init__(pos, color, radius)
        self.isDown = isDown
        self.dx = 0
        # self.dy = -1 if isDown else 1
        self.dy = 300 if isDown else -300
    def moveObject(self, dt: int):
        # self.pos.y += dt * (300 if self.isDown else -300)
        self.pos.y += dt * self.dy
        self.pos.x += dt * self.dx

# pygame setup
pygame.init()
WIDTH = 1280
HEIGHT = 720
RADIUS = 40
PLATFORM_WIDTH = 150
PLATFORM_HEIGHT = 10
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0

player = Platform(pygame.Vector2(screen.get_width() / 2 - PLATFORM_WIDTH/2, 0), "white", RADIUS)
opponent = Platform(pygame.Vector2(screen.get_width() / 2 - PLATFORM_WIDTH/2, HEIGHT - PLATFORM_HEIGHT), "white", RADIUS)
ball = Ball(pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2), "white", RADIUS, False)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    pygame.draw.rect(screen, "white", pygame.Rect(player.pos.x, player.pos.y, PLATFORM_WIDTH, PLATFORM_HEIGHT))
    pygame.draw.rect(screen, "white", pygame.Rect(opponent.pos.x, opponent.pos.y, PLATFORM_WIDTH, PLATFORM_HEIGHT))
    pygame.draw.circle(screen, "white", ball.pos, RADIUS)

    # game logic
    if 0 + RADIUS > ball.pos.y or ball.pos.y > HEIGHT - RADIUS:
        running = False

    # player movement
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and 0 < player.pos.x:
        player.moveObject(True, dt)
    if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and WIDTH - PLATFORM_WIDTH >= player.pos.x:
        player.moveObject(False, dt)

    # ball physics
    ball.moveObject(dt)
    if (((ball.pos.y - RADIUS) <= (PLATFORM_HEIGHT+5) and player.pos.x - 0.75*RADIUS <= ball.pos.x <= player.pos.x+PLATFORM_WIDTH + 0.75*RADIUS)
        or ((ball.pos.y + RADIUS) >= (HEIGHT-PLATFORM_HEIGHT-5) and opponent.pos.x <= ball.pos.x <= opponent.pos.x+PLATFORM_WIDTH)):
        platformX = player.pos.x if ball.isDown else opponent.pos.x
        # returns a number from -75->75
        # 75/55 is ~1.3, which is 75 degrees to rads
        radsApprox = (abs(platformX - ball.pos.x)-(PLATFORM_WIDTH/2)) / 55
        ball.dx = math.sin(radsApprox) * 300 * 1 if ball.isDown else -1
        ball.dy = math.cos(radsApprox) * 300 * 1 if ball.isDown else -1
        ball.isDown = not ball.isDown

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
