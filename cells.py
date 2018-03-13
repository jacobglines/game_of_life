class Cell:
    def __init__(self, living):
        self.living = living

    def __str__(self):
        return '0' if self.living else 'x'