class Cell:
    def __init__(self, living):
        self.living = living

    def __repr__(self):
        return '0' if self.living else '-'