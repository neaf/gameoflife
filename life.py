class StateParser(object):
    def __init__(self, input):
        self.input = input

    def get_list(self):
        list = []
        point_strings = self.input.split(" ")
        for point in point_strings:
            coordinates = point.split(",")
            x = int(coordinates[0])
            y = int(coordinates[1])
            list.append((x, y))
        return list

class GameOfLife(object):
    def __init__(self, start=None):
        if not start: start = []
        self.cells = start
        self.cells_to_die = []

    def tick(self):
        for cell in self.cells:
            self.process_cell(cell)

    def process_cell(self, cell):
        self.cells_to_die.append(cell)
