# agent.py

class Agent:
    def __init__(self, x, y, speed, environment):
        self.x = x
        self.y = y
        self.speed = speed
        self.environment = environment

    def move(self, direction):
        if direction == 'up':
            self.y -= self.speed
        elif direction == 'down':
            self.y += self.speed
        elif direction == 'left':
            self.x -= self.speed
        elif direction == 'right':
            self.x += self.speed
        self.x, self.y = self.environment.limit_position(self.x, self.y)

    def get_position(self):
        return self.x, self.y
