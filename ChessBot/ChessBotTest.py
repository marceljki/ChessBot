import unittest

from legacy import ChessGame


class MyTestCase(unittest.TestCase):
    def test_single_converts(self):
        position = ChessGame.number_to_position(0)
        self.assertEqual("a1a1", position)
        position = ChessGame.number_to_position(1)
        self.assertEqual("a1b1", position)
        position = ChessGame.number_to_position(2)
        self.assertEqual("a1c1", position)
        position = ChessGame.number_to_position(7)
        self.assertEqual("a1h1", position)
        position = ChessGame.number_to_position(15)
        self.assertEqual("a1h2", position)
        position = ChessGame.number_to_position(23)
        self.assertEqual("a1h3", position)

    def test_every_pos_is_given(self):
        all_expected_moves = set()
        for a in 'abcdefgh':
            for b in range(1, 9):
                for c in 'abcdefgh':
                    for d in range(1, 9):
                        all_expected_moves.add(a + str(b) + c + str(d))
        print(len(all_expected_moves))
        all_actual_moves = set()
        for i in range(4096):
            all_actual_moves.add(ChessGame.number_to_position(i))
        self.assertEqual(len(all_actual_moves), len(all_expected_moves))
        self.assertEqual(all_actual_moves, all_expected_moves)

    def test_piece_movement(self):
        chessbot = ChessGame.ChessBot()
        chessbot.env.step("b1c3")


if __name__ == '__main__':
    unittest.main()
