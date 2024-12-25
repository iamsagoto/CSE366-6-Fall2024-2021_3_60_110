# environment.py
import random
import pygame

class Environment:
    def __init__(self, num_classes, num_students, time_slots):
        self.num_classes = num_classes
        self.num_students = num_students
        self.time_slots = time_slots
        self.population = self.generate_population(50)  # Population size set to 50

    def generate_population(self, population_size):
        population = []
        for _ in range(population_size):
            schedule = [[random.randint(0, self.num_students - 1) for _ in range(self.num_classes)] for _ in range(self.time_slots)]
            population.append(schedule)
        return population

    def visualize_schedule(self, schedule, generation, best_fitness, max_fitness):
        pygame.init()
        screen_width = 1200
        screen_height = 700
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Class Scheduling Visualization")
        
        screen.fill((200, 200, 200))
        font = pygame.font.Font(None, 30)

        grid_start_x = 200  # Adjusted to provide more space on the left
        grid_start_y = 50
        cell_width = 80
        cell_height = 50

        # Draw grid
        for row in range(len(schedule)):
            for col in range(len(schedule[row])):
                student_id = schedule[row][col]
                rect = pygame.Rect(
                    grid_start_x + col * cell_width,
                    grid_start_y + row * cell_height,
                    cell_width,
                    cell_height
                )
                color = (0, 0, 255) if random.random() < 0.2 else (150, 150, 150)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 2)
                text = font.render(f"P{student_id+1} 1h", True, (255, 255, 255))
                screen.blit(text, (rect.x + 10, rect.y + 10))

        # Draw headers
        for col in range(len(schedule[0])):
            text = font.render(f"Slot {col+1}", True, (0, 0, 0))
            screen.blit(text, (grid_start_x + col * cell_width + 10, grid_start_y - 30))

        for row in range(len(schedule)):
            text = font.render(f"Preference: {random.uniform(0.5, 1.5):.2f}", True, (0, 0, 0))
            screen.blit(text, (grid_start_x - 150, grid_start_y + row * cell_height + 10))

        # Draw metrics
        metrics_x = grid_start_x + len(schedule[0]) * cell_width + 50
        metrics_y = grid_start_y

        metrics = [
            f"Generation: {generation}",
            f"Best Fitness (Current): {best_fitness:.2f}",
            f"Max Fitness Achieved: {max_fitness:.2f}"
        ]

        for i, metric in enumerate(metrics):
            text = font.render(metric, True, (0, 0, 0))
            screen.blit(text, (metrics_x, metrics_y + i * 40))

        pygame.display.flip()
        pygame.time.wait(1000)  # Delay between generations set to 1000ms
