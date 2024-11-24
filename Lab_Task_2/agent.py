import pygame
from collections import deque
import heapq

class Agent(pygame.sprite.Sprite):
    def __init__(self, environment, grid_size):
        super().__init__()
        self.image = pygame.Surface((grid_size, grid_size))
        self.image.fill((0, 0, 255))  # Agent color is blue
        self.rect = self.image.get_rect()
        self.grid_size = grid_size
        self.environment = environment
        self.position = [0, 0]  # Starting at the top-left corner of the grid
        self.rect.topleft = (0, 0)
        self.task_completed = 0
        self.completed_tasks = []  # To store (task_number, cost) for completed tasks
        self.path = []  # List of positions to follow
        self.moving = False  # Flag to indicate if the agent is moving
        self.cumulative_cost_ucs = 0  # Tracks total cost for UCS
        self.cumulative_cost_astar = 0  # Tracks total cost for A*

    def move(self):
        """Move the agent along the path."""
        if self.path:
            next_position = self.path.pop(0)
            self.position = list(next_position)
            self.rect.topleft = (self.position[0] * self.grid_size, self.position[1] * self.grid_size)
            self.check_task_completion()
        else:
            self.moving = False  # Stop moving when path is exhausted

    def check_task_completion(self):
        """Check if the agent has reached a task location."""
        position_tuple = tuple(self.position)
        if position_tuple in self.environment.task_locations:
            task_number = self.environment.task_locations.pop(position_tuple)
            self.task_completed += 1
            cost = self.cumulative_cost_ucs if self.environment.current_mode == "UCS" else self.cumulative_cost_astar
            self.completed_tasks.append((task_number, cost))  # Record task number and its cost
            self.path = []  # Clear the path after completing the task

    def find_path_to_task_ucs(self):
        """Find the shortest path to a task using Uniform Cost Search (UCS)."""
        if not self.environment.task_locations:
            self.moving = False  # Stop moving if no tasks remain
            return
        nearest_task = min(self.environment.task_locations.keys(), key=lambda t: self.ucs(tuple(self.position), t)[1])
        path, cost = self.ucs(tuple(self.position), nearest_task)
        if path:
            self.path = path[1:]  # Exclude the current position
            self.moving = True
            self.cumulative_cost_ucs += cost

    def find_path_to_task_astar(self):
        """Find the shortest path to a task using A* Search."""
        if not self.environment.task_locations:
            self.moving = False  # Stop moving if no tasks remain
            return
        nearest_task = min(self.environment.task_locations.keys(), key=lambda t: self.astar(tuple(self.position), t)[1])
        path, cost = self.astar(tuple(self.position), nearest_task)
        if path:
            self.path = path[1:]  # Exclude the current position
            self.moving = True
            self.cumulative_cost_astar += cost

    def ucs(self, start, goal):
        """Uniform Cost Search to find the shortest path."""
        frontier = [(0, start)]
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            current_cost, current = heapq.heappop(frontier)

            if current == goal:
                break

            for neighbor in self.get_neighbors(current):
                new_cost = cost_so_far[current] + 1  # Each move costs 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost
                    heapq.heappush(frontier, (priority, neighbor))
                    came_from[neighbor] = current

        path = self.reconstruct_path(came_from, start, goal)
        return path, cost_so_far.get(goal, float('inf'))

    def astar(self, start, goal):
        """A* Search to find the shortest path."""
        frontier = [(0, start)]
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            current_cost, current = heapq.heappop(frontier)

            if current == goal:
                break

            for neighbor in self.get_neighbors(current):
                new_cost = cost_so_far[current] + 1  # Each move costs 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + self.heuristic(neighbor, goal)
                    heapq.heappush(frontier, (priority, neighbor))
                    came_from[neighbor] = current

        path = self.reconstruct_path(came_from, start, goal)
        return path, cost_so_far.get(goal, float('inf'))

    def get_neighbors(self, position):
        """Get valid neighboring positions on the grid."""
        x, y = position
        neighbors = [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
        return [
            (nx, ny)
            for nx, ny in neighbors
            if self.environment.is_within_bounds(nx, ny) and not self.environment.is_barrier(nx, ny)
        ]

    def heuristic(self, position, goal):
        """Heuristic function for A* (Manhattan distance)."""
        x1, y1 = position
        x2, y2 = goal
        return abs(x1 - x2) + abs(y1 - y2)

    def reconstruct_path(self, came_from, start, goal):
        """Reconstruct the path from start to goal."""
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from.get(current)
            if current is None:
                return []  # No valid path
        path.append(start)
        path.reverse()
        return path
