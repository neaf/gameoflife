def evolve(cells):
    stats = get_stats(cells)
    return stats[3] + living(stats, cells)

def get_stats(cells):
    counts = get_neighbour_counts(cells)
    return reverse_neighbour_counts(counts)

def reverse_neighbour_counts(counts):
    reversed = {}
    for cell, count in counts.items():
        cells = reversed.get(count, [])
        cells.append(cell)
        reversed[count] = cells
    return reversed

def get_neighbour_counts(cells, counts=None):
    counts = counts or {}
    for cell in cells:
        increase_neighbour_counts(cell, counts)
    return counts

def increase_neighbour_counts(cell, counts):
    neighbours = get_neighbours(cell)
    for cell in neighbours:
        increase_neighbour_count(cell, counts)

def increase_neighbour_count(cell, counts):
    counts[cell] = counts.get(cell, 0) + 1

def get_neighbours(cell):
    neighbors = []
    for delta_x in range(-1, 2):
        x = cell[0] + delta_x
        for delta_y in range(-1, 2):
            y = cell[1] + delta_y
            neighbor = (x, y)
            if not neighbor == cell:
                neighbors.append(neighbor)
    return neighbors

def list_intersection(a, b):
    return list(set(a) & set(b))

def living(stats, cells):
    return list_intersection(stats[2], cells)

