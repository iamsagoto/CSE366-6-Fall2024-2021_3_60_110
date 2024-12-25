

import pygame
from agent import Agent
from environment import Environment

pygame.init()

WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Simulation")

WHITE = (255, 255, 255)
AQUA = (0, 0, 255)
BLACK = (0,0,0)

font = pygame.font.Font(None, 36)

env = Environment(WIDTH, HEIGHT)
agent = Agent(x=WIDTH // 2, y=HEIGHT // 2, speed=5, environment=env)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        agent.move('up')
    if keys[pygame.K_DOWN]:
        agent.move('down')
    if keys[pygame.K_LEFT]:
        agent.move('left')
    if keys[pygame.K_RIGHT]:
        agent.move('right')

    window.fill(WHITE)


    agent_pos = agent.get_position()
    square_size = 20  


    top_left_x = agent_pos[0] - square_size // 2
    top_left_y = agent_pos[1] - square_size // 2


    pygame.draw.rect(window, AQUA, (top_left_x, top_left_y, square_size, square_size))

    position_text = font.render(f"Position: {agent_pos}", True, BLACK)
    window.blit(position_text, (10, 10))

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()
