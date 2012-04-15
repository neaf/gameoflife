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
        self.set_initial()

    def set_initial(self):
        self.marked_to_die = []
        self.marked_to_live = []
        self.neighbor_counts = {}

    def tick(self):
        self.draw()
        for cell in self.cells:
            self.process_cell(cell)
        self.kill_marked_cells()
        self.spawn_cells()
        self.set_initial()

    def spawn_cells(self):
        self.populate_marked_to_live()
        self.give_birth()

    def populate_marked_to_live(self):
        for cell, count in self.neighbor_counts.items():
            if count == 3:
                self.marked_to_live.append(cell)

    def give_birth(self):
        self.cells = set(self.cells + self.marked_to_live)

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
            current = self.neighbor_counts.get(neighbor, 0)
            self.neighbor_counts[neighbor] = current + 1


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

    def draw(self):
        rows = []
        for x in range(-60, 60):
            row = []
            for y in range(-60, 60):
                if (y, x) in self.cells:
                    row.append('##')
                else:
                    row.append('  ')
            rows.append(''.join(row))
        print '\n'.join(rows)

if __name__ == "__main__":
    from time import sleep

    start = [(1,1), (1,2), (3,2), (2,4), (1,5), (1,6), (1,7)]

    while True:
        game = GameOfLife(start=start)
        game.tick()
        start = game.cells
        sleep(0.03)

