from unittest import TestCase
import mock
from gameoflife import GameOfLife

class GameOfLifeTest(TestCase):
    def setUp(self):
        self.game = GameOfLife()

    def assertCellMarkedToLive(self, cell):
        self.assertIn(cell, self.game.marked_to_live)
        self.assertNotIn(cell, self.game.marked_to_die)

    def assertCellMarkedToDie(self, cell):
        self.assertIn(cell, self.game.marked_to_die)
        self.assertNotIn(cell, self.game.marked_to_live)

    @mock.patch.object(GameOfLife, 'set_initial')
    def test_new_sets_initial_containers(self, set_initial):
        game = GameOfLife()
        set_initial.assert_called_once_with()

    def test_set_initial(self):
        self.assertEqual(self.game.marked_to_live, [])
        self.assertEqual(self.game.marked_to_die, [])
        self.assertEqual(self.game.neighbor_counts, {})

    def test_tick_fires_process_cell_on_each_cell(self):
        self.game.cells = [(1,1), (1,4), (44,54), (124,54)]
        self.game.process_cell = mock.Mock()
        calls = [mock.call(cell) for cell in self.game.cells]
        self.game.tick()
        self.game.process_cell.assert_has_calls(calls)

    def test_tick_makes_marked_cells_die(self):
        self.game.kill_marked_cells = mock.Mock()
        self.game.tick()
        self.game.kill_marked_cells.assert_called_once_with()

    def test_tick_spawns_correct_cells(self):
        self.game.spawn_cells= mock.Mock()
        self.game.tick()
        self.game.spawn_cells.assert_called_once_with()

    def test_tick_sets_initial(self):
        self.game.set_initial = mock.Mock()
        self.game.tick()
        self.game.set_initial.assert_called_once_with()

    def test_process_cell_increase_neighbor_counters(self):
        cell = (1, 1)
        self.game.cells = [cell]
        self.game.increase_neighbors_counts = mock.Mock(return_value=True)
        self.game.process_cell(cell)
        self.game.increase_neighbors_counts.assert_called_once_with(cell)

    def test_increase_neighbor_counts(self):
        self.game.neighbor_counts = {
            (0, 1): 1,
            (1, 1): 1,
            (2, 2): 0,
        }
        self.game.increase_neighbors_counts((2, 1))
        expected = {
            (0, 1): 1,
            (1, 1): 2,
            (2, 2): 1,
        }
        self.assertDictContainsSubset(expected, self.game.neighbor_counts)

    def test_process_cell_marks_to_die_if_should_die(self):
        cell = (1, 1)
        self.game.cells = [cell]
        self.game.should_die = mock.Mock(return_value=True)
        self.game.process_cell(cell)
        self.assertCellMarkedToDie(cell)

    def test_should_die_true_if_lone(self):
        cell = (1, 1)
        self.game.cells = [cell]
        self.assertTrue(self.game.should_die(cell))

    def test_should_die(self):
        cell = (1, 1)
        samples = {
            True: (0, 1, 4, 5, 6, 7, 8),
            False: (2, 3),
        }

        self.game.live_neighbors_count = mock.Mock()
        for expected, counts in samples.items():
            for c in counts:
                self.game.live_neighbors_count.return_value = c
                self.assertEqual(expected, self.game.should_die(cell))

    def test_should_die_true_if_one_neighbor(self):
        cell = (1, 1)
        self.game.cells = [cell, (2, 2), (50, 30)]
        self.game.should_die(cell)
        self.assertTrue(self.game.should_die(cell))

    def test_should_die_false_if_2_neighbors(self):
        cell = (1, 1)
        self.game.cells = [cell, (1, 2), (2, 2), (50, 30)]
        self.assertFalse(self.game.should_die(cell))

    def test_live_neighbors_count(self):
        cell = (1, 1)
        samples = {
            (cell,): 0,
            (cell, (2, 2), (50, 30)): 1,
            (cell, (2, 2), (0, 0), (50, 30)): 2,
            (cell, (0, 0), (0, 1), (2, 1), (2, 2), (1, 0), (50, 30)): 5,
        }
        for sample, expected in samples.items():
            self.game.cells = sample
            result = self.game.live_neighbors_count(cell)
            self.assertEqual(result, expected)

    def test_get_neighbors_coordinates(self):
        result = self.game.get_neighbors_coordinates((1, 1))
        expected = [
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 0),
            (1, 2),
            (2, 0),
            (2, 1),
            (2, 2),
        ]
        self.assertEqual(result, expected)

    def test_kill_marked_cells(self):
        self.game.cells = [(1, 1), (1, 2), (2, 2), (50, 30)]
        self.game.marked_to_die = [(1, 1), (2, 2)]

        self.game.kill_marked_cells()

        expected = [(1, 2), (50, 30)]
        self.assertItemsEqual(self.game.cells, expected)

    def test_spawn_cells(self):
        self.game.populate_marked_to_live = mock.Mock()
        self.game.give_birth = mock.Mock()
        self.game.spawn_cells()
        self.game.populate_marked_to_live.assert_called_once_with()
        self.game.give_birth.assert_called_once_with()

    def test_populate_marked_to_live(self):
        self.game.neighbor_counts = {
            (1, 1): 2,
            (1, 3): 3,
            (0, 2): 1,
            (4, 5): 8,
            (3, 12): 3,
        }
        self.game.populate_marked_to_live()
        expected = [(1,3), (3,12)]
        self.assertItemsEqual(self.game.marked_to_live, expected)

    def test_give_birth(self):
        self.game.cells = [(1, 1), (1, 2), (2, 2), (50, 30)]
        self.game.marked_to_live = [(2, 1), (4, 2)]
        expected = self.game.cells + self.game.marked_to_live

        self.game.give_birth()

        self.assertItemsEqual(self.game.cells, expected)
