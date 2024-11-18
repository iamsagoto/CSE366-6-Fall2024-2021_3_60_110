# environment.py

class Environment:
    def __init__(self, width, height):
        """
        Initialize environment dimensions.
        """
        self.width = width
        self.height = height

    def limit_position(self, x, y):
        """
        Ensures that the agent wraps around when it goes out of bounds.
        """
        # Wrap around horizontally
        if x < 0:
            x = self.width
        elif x > self.width:
            x = 0

        # Wrap around vertically
        if y < 0:
            y = self.height
        elif y > self.height:
            y = 0

        return x, y
