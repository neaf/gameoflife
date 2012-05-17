import mock
from gameoflife import evolve, get_stats, living, get_neighbour_counts, increase_neighbour_counts, get_neighbours, increase_neighbour_count, reverse_neighbour_counts, list_intersection

@mock.patch('gameoflife.living')
@mock.patch('gameoflife.get_stats')
def test_evolve(get_stats, living):
    cells = mock.Mock()
    zero = mock.Mock()
    get_stats.return_value = {
        0: zero,
        3: 2
    }
    living.return_value = 3
    result = evolve(cells)
    get_stats.assert_called_once_with(cells)
    living.assert_colled_once_with(get_stats.return_value, cells)
    assert result == 5

@mock.patch('gameoflife.reverse_neighbour_counts')
@mock.patch('gameoflife.get_neighbour_counts')
def test_get_stats(get_neighbour_counts, reverse_neighbour_counts):
    cells = mock.Mock()
    result = get_stats(cells)
    get_neighbour_counts.assert_called_once_with(cells)
    reverse_neighbour_counts.assert_called_once_with(get_neighbour_counts.return_value)
    assert result == reverse_neighbour_counts.return_value

@mock.patch('gameoflife.list_intersection')
def test_living(list_intersection):
    stats = {
        2: mock.Mock()
    }
    cells = mock.Mock()
    result = living(stats, cells)
    list_intersection.assert_called_once_with(stats[2], cells)
    assert result == list_intersection.return_value

@mock.patch('gameoflife.increase_neighbour_counts')
def test_get_neighbour_counts(increase_neighbour_counts):
    cells = (mock.Mock(), mock.Mock())
    counts = mock.Mock()
    result = get_neighbour_counts(cells, counts=counts)
    calls = [mock.call(cell, counts) for cell in cells]
    increase_neighbour_counts.assert_has_calls(calls)
    assert result == counts

@mock.patch('gameoflife.increase_neighbour_count')
@mock.patch('gameoflife.get_neighbours')
def test_increase_neighbour_counts(get_neighbours, increase_neighbour_count):
    cell = mock.Mock()
    neighbours = (mock.Mock(), mock.Mock())
    get_neighbours.return_value = neighbours
    counts = mock.Mock()

    increase_neighbour_counts(cell, counts)

    calls = [mock.call(cell, counts) for cell in neighbours]
    increase_neighbour_count.assert_has_calls(calls)

def test_get_neighbours():
    result = get_neighbours((2,4))
    expected = [
        (1, 3), (2, 3), (3, 3),
        (1, 4),         (3, 4),
        (1, 5), (2, 5), (3, 5)
    ]
    assert set(result) == set(expected)

def test_increase_neighbour_count_when_empty():
    cell = mock.Mock()
    counts = {}
    increase_neighbour_count(cell, counts)
    assert counts[cell] == 1

def test_increase_neighbour_count_when_already_existing():
    cell = mock.Mock()
    counts = {cell: 3}
    increase_neighbour_count(cell, counts)
    assert counts[cell] == 4

def test_reverse_neighbour_counts():
    ones = [mock.Mock() for _ in range(2)]
    twos = [mock.Mock() for _ in range(2)]
    counts = {}
    for one in ones:
        counts[one] = 1
    for two in twos:
        counts[two] = 2
    result = reverse_neighbour_counts(counts)
    assert set(result[1]) == set(ones)
    assert set(result[2]) == set(twos)

def test_list_intersection():
    a = [1, 2]
    b = [2, 3]

    result = list_intersection(a, b)
    assert result == [2]
