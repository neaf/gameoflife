from unittest import TestCase
import mock
from life import StateParser, GameOfLife


class StateParserTest(TestCase):
    def test_input_parse(self):
        input = "1,1 1,4 44,54 124,54"
        expected = [(1,1), (1,4), (44,54), (124,54)]
        parser = StateParser(input)
        self.assertEqual(parser.get_list(), expected)


class GameOfLifeTest(TestCase):
    def setUp(self):
        self.game = GameOfLife()

    def test_tick_fires_process_cell_on_each_cell(self):
        self.game.cells = [(1,1), (1,4), (44,54), (124,54)]
        self.game.process_cell = mock.Mock()
        self.game.tick()
        calls = [mock.call(cell) for cell in self.game.cells]
        self.game.process_cell.assert_has_calls(calls)

    def test_process_cell_marks_to_die_if_has_no_neighbors(self):
        self.game.cells = [(1,1)]
        self.game.process_cell((1,1))
        self.assertIn((1,1), self.game.cells_to_die)
