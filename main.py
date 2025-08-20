# Example file showing a circle moving on screen
import pygame

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
        self.pos.x += dt * (300 if not isLeft else -300)

class Ball(MoveableObject):
    def __init__(self, pos: pygame.Vector2, color: str, radius: int, isDown: bool):
        super().__init__(pos, color, radius)
        self.isDown = isDown
    def moveObject(self, dt: int):
        self.pos.y += dt * (300 if self.isDown else -300)

# pygame setup
pygame.init()
WIDTH = 1280
HEIGHT = 720
RADIUS = 40
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0

player = Platform(pygame.Vector2(screen.get_width() / 2, 0), "white", RADIUS)
opponent = Platform(pygame.Vector2(screen.get_width() / 2, HEIGHT), "white", RADIUS)
ball = Ball(pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2), "white", RADIUS, False)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    pygame.draw.circle(screen, "white", player.pos, RADIUS)
    pygame.draw.circle(screen, "white", opponent.pos, RADIUS)
    pygame.draw.circle(screen, "white", ball.pos, RADIUS)

    # game logic
    if 0 + RADIUS > ball.pos.y or ball.pos.y > HEIGHT - RADIUS:
        running = False

    # player movement
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and 0 < player.pos.x:
        player.moveObject(True, dt)
    if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and WIDTH >= player.pos.x:
        player.moveObject(False, dt)

    # ball physics
    ball.moveObject(dt)
    platformPos = opponent.pos if ball.isDown else player.pos
    distance = ball.pos.distance_to(platformPos)
    if distance <= (RADIUS*2):
        ball.isDown = not ball.isDown

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
