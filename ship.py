class Ship:
    def __init__(self, size):
        self.size = size
        self.hits = 0
        self.coordinates = []
        self.orientation = 0

    def is_sunk(self):
        return self.hits == self.size