import pygame
import pymunk
import pymunk.pygame_util

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Ball Escape Maze')
clock = pygame.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Physics setup
space = pymunk.Space()
space.gravity = (0, 900)

# Platform setup
def create_platform(x, y, width, height):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (x + width / 2, y + height / 2)
    shape = pymunk.Poly.create_box(body, (width, height))
    shape.elasticity = 0.8
    space.add(body, shape)

# Beautiful Maze Design
create_platform(50, 550, 700, 20)
create_platform(50, 450, 150, 20)
create_platform(250, 450, 200, 20)
create_platform(500, 450, 250, 20)
create_platform(50, 350, 200, 20)
create_platform(400, 350, 300, 20)
create_platform(50, 250, 150, 20)
create_platform(300, 250, 250, 20)
create_platform(600, 250, 150, 20)
create_platform(50, 150, 100, 20)
create_platform(250, 150, 300, 20)
create_platform(600, 150, 150, 20)

# Ball setup
def create_ball():
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 20))
    body.position = (70, 520)
    shape = pymunk.Circle(body, 20)
    shape.elasticity = 0.5
    space.add(body, shape)
    return body

ball = create_ball()

# Exit door
exit_rect = pygame.Rect(750, 50, 50, 100)

# Game Over and Win Functions
def game_over():
    font = pygame.font.SysFont(None, 60)
    text = font.render('Game Over!', True, (255, 0, 0))
    screen.blit(text, (300, 250))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    exit()

def game_win():
    font = pygame.font.SysFont(None, 60)
    text = font.render('You Win!', True, (0, 255, 0))
    screen.blit(text, (300, 250))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    exit()

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        ball.apply_impulse_at_local_point((0, -50))
    if keys[pygame.K_LEFT]:
        ball.apply_impulse_at_local_point((-10, 0))
    if keys[pygame.K_RIGHT]:
        ball.apply_impulse_at_local_point((10, 0))

    # Ball falling check
    if ball.position.y > 600:
        game_over()

    # Win check
    if exit_rect.collidepoint(ball.position.x, ball.position.y):
        game_win()

    # Drawing
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 255, 0), exit_rect)
    space.debug_draw(draw_options)
    
    # Step the simulation
    space.step(1 / 60.0)
    pygame.display.flip()
    clock.tick(60)
