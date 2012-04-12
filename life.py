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
        self.cells = start or []
        self.marked_to_die = []
        self.marked_to_live = []
        self.neighbor_counts = {}

    def tick(self):
        for cell in self.cells:
            self.process_cell(cell)
        self.kill_marked_cells()
        self.spawn_cells()

    def spawn_cells(self):
        pass

    def kill_marked_cells(self):
        self.cells = filter(lambda cell: cell not in self.marked_to_die, self.cells)

    def process_cell(self, cell):
        if self.should_die(cell):
            self.marked_to_die.append(cell)
        else:
            self.marked_to_live.append(cell)
        self.increase_neighbors_counts(cell)

    def increase_neighbors_counts(self, cell):
        neighbors = self.get_neighbors_coordinates(cell)
        for neighbor in neighbors:
            if not self.neighbor_counts.get(neighbor):
                self.neighbor_counts[neighbor] = 0
            self.neighbor_counts[neighbor] += 1

    def should_die(self, cell):
        if 1 < self.live_neighbors_count(cell) < 4:
            return False
        else:
            return True

    def live_neighbors_count(self, cell):
        neighbor_coords = self.get_neighbors_coordinates(cell)
        count = 0
        for cell in neighbor_coords:
            if cell in self.cells:
                count += 1
        return count

    def get_neighbors_coordinates(self, cell):
        neighbors = []
        for delta_x in range(-1, 2):
            x = cell[0] + delta_x
            for delta_y in range(-1, 2):
                y = cell[1] + delta_y
                neighbor = (x, y)
                if not neighbor == cell:
                    neighbors.append(neighbor)
        return neighbors
