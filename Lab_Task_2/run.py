import pygame
import sys
from agent import Agent
from environment import Environment

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
GRID_SIZE = 40
STATUS_WIDTH = 200
BACKGROUND_COLOR = (255, 255, 255)
BARRIER_COLOR = (0, 0, 0)       # Barrier color is black
TASK_COLOR = (255, 0, 0)        # Task color is red
TEXT_COLOR = (0, 0, 0)
BUTTON_COLOR = (0, 200, 0)
BUTTON_HOVER_COLOR = (0, 255, 0)
BUTTON_TEXT_COLOR = (255, 255, 255)
MOVEMENT_DELAY = 200  # Milliseconds between movements

def main():
    pygame.init()

    # Set up display with an additional status panel
    screen = pygame.display.set_mode((WINDOW_WIDTH + STATUS_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pygame AI Grid Simulation")

    # Clock to control frame rate
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    # Initialize environment and agent
    environment = Environment(WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, num_tasks=3, num_barriers=10)
    environment.current_mode = "UCS"  # Default search mode
    agent = Agent(environment, GRID_SIZE)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(agent)

    # Start button and mode toggle button
    button_width, button_height = 100, 50
    start_button_x = WINDOW_WIDTH + (STATUS_WIDTH - button_width) // 2
    start_button_y = WINDOW_HEIGHT // 2 - button_height
    toggle_button_y = start_button_y + button_height + 20
    start_button_rect = pygame.Rect(start_button_x, start_button_y, button_width, button_height)
    toggle_button_rect = pygame.Rect(start_button_x, toggle_button_y, button_width, button_height)

    # Variables for simulation
    simulation_started = False
    last_move_time = pygame.time.get_ticks()

    # Main loop
    running = True
    while running:
        clock.tick(60)  # Limit to 60 FPS

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not simulation_started and start_button_rect.collidepoint(event.pos):
                    simulation_started = True
                elif toggle_button_rect.collidepoint(event.pos):
                    # Toggle between UCS and A*
                    environment.current_mode = "A*" if environment.current_mode == "UCS" else "UCS"

        # Clear the screen
        screen.fill(BACKGROUND_COLOR)

        # Draw grid and barriers
        for x in range(environment.columns):
            for y in range(environment.rows):
                rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(screen, (200, 200, 200), rect, 1)  # Draw grid lines

        # Draw barriers
        for (bx, by) in environment.barrier_locations:
            barrier_rect = pygame.Rect(bx * GRID_SIZE, by * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, BARRIER_COLOR, barrier_rect)

        # Draw tasks with numbers
        for (tx, ty), task_number in environment.task_locations.items():
            task_rect = pygame.Rect(tx * GRID_SIZE, ty * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, TASK_COLOR, task_rect)
            task_num_surface = font.render(str(task_number), True, (255, 255, 255))
            task_num_rect = task_num_surface.get_rect(center=task_rect.center)
            screen.blit(task_num_surface, task_num_rect)

        # Draw agent
        all_sprites.draw(screen)

        # Status panel
        status_x = WINDOW_WIDTH + 10
        mode_text = f"Mode: {environment.current_mode}"
        task_status_text = f"Tasks Completed: {agent.task_completed}"
        position_text = f"Position: {agent.position}"
        total_cost_text = f"Total Cost: {agent.cumulative_cost_ucs if environment.current_mode == 'UCS' else agent.cumulative_cost_astar}"
        screen.blit(font.render(mode_text, True, TEXT_COLOR), (status_x, 20))
        screen.blit(font.render(task_status_text, True, TEXT_COLOR), (status_x, 50))
        screen.blit(font.render(position_text, True, TEXT_COLOR), (status_x, 80))
        screen.blit(font.render(total_cost_text, True, TEXT_COLOR), (status_x, 110))

        # Completed task details
        task_y_offset = 150
        for i, (task_number, cost) in enumerate(agent.completed_tasks):
            task_text = f"Task {task_number}: Cost {cost}"
            screen.blit(font.render(task_text, True, TEXT_COLOR), (status_x, task_y_offset + i * 30))

        # Draw buttons
        if not simulation_started:
            pygame.draw.rect(screen, BUTTON_COLOR, start_button_rect)
            start_text = font.render("Start", True, BUTTON_TEXT_COLOR)
            screen.blit(start_text, start_text.get_rect(center=start_button_rect.center))

        pygame.draw.rect(screen, BUTTON_COLOR, toggle_button_rect)
        toggle_text = font.render(f"Toggle ({environment.current_mode})", True, BUTTON_TEXT_COLOR)
        screen.blit(toggle_text, toggle_text.get_rect(center=toggle_button_rect.center))

        # Simulation movement
        if simulation_started:
            current_time = pygame.time.get_ticks()
            if current_time - last_move_time > MOVEMENT_DELAY:
                if not agent.moving and environment.task_locations:
                    # Find next task based on selected mode
                    if environment.current_mode == "UCS":
                        agent.find_path_to_task_ucs()
                    elif environment.current_mode == "A*":
                        agent.find_path_to_task_astar()
                elif agent.moving:
                    agent.move()
                last_move_time = current_time

        # Draw the status panel separator
        pygame.draw.line(screen, (0, 0, 0), (WINDOW_WIDTH, 0), (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
