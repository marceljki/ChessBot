from time import sleep
import random
from typing import Optional

import chess
from chessboard import display

chess_moves = [
    "e2e4",
    "e7e5",
    "g1f3",
    "b8c6",
    "f1c4",
    "g8f6",
    "d2d3",
    "f8d6",
    "c1e3",
    "d6e5"
]


# for i in chess_moves:
#     board.push_san(i)
#     display.update(board.fen(), game_board)
#     sleep(1)
# display.terminate()


def get_position_as_array(fen) -> [int]:
    # Create a mapping of FEN piece notations to numeric values
    piece_mapping = {
        'P': 1, 'N': 2, 'B': 3, 'R': 4, 'Q': 5, 'K': 6,
        'p': -1, 'n': -2, 'b': -3, 'r': -4, 'q': -5, 'k': -6
    }

    # Initialize a 1D array with 64 elements
    chessboard = [0] * 64

    # Split the FEN string to get the piece placement part
    parts = fen.split(' ')
    piece_placement = parts[0]

    # Map FEN pieces to the numeric array
    index = 0
    for char in piece_placement:
        if char == '/':
            continue  # Skip forward slashes
        elif char.isdigit():
            index += int(char)
        else:
            chessboard[index] = piece_mapping[char]
            index += 1

    return chessboard


def number_to_position(num: int):
    from_sq = number_to_square(num // 64)
    to_sq = number_to_square(num % 64)
    return from_sq + to_sq


def number_to_square(num: int) -> Optional[str]:
    if num < 0 or num > 63:
        return None

    rank = num // 8  # Calculate the rank (0 to 7)
    file = num % 8  # Calculate the file (0 to 7)

    # Convert rank and file to a chess square in algebraic notation
    square = chr(ord('a') + file) + str(rank + 1)

    return square


class ChessBoard:
    # 64 * 64 = 4096
    N_ALL_MOVES = 4096

    N_SQUARES = 64

    def __init__(self):
        self.board = chess.Board()
        self.board_display = None

    def get_all_legal_moves(self) -> list[str]:
        return [str(move) for move in self.board.legal_moves]

    def display_game(self):
        self.board_display = display.start(self.board.fen())
        temp_board = chess.Board()
        for move in self.board.move_stack:
            temp_board.push_san(str(move))
            self.board_display.update_pieces(temp_board.fen())
            sleep(1)

    def reset(self):
        self.board.reset()
        return get_position_as_array(self.board.fen())

    def step(self, action: str):
        self.board.push_san(action)
        if self.board.is_checkmate():
            print("CHECKMATE")
            return 1
        return None

    def request_move(self):
        self.board.push([i for i in self.board.legal_moves][0])


class ChessBot:

    def __init__(self):
        self.env = ChessBoard()
        self.states = self.env.N_SQUARES
        self.actions = self.env.N_ALL_MOVES

    def get_best_move(self):
        pass

    def test_run(self):
        # TODO: continue here: test the model, so that rando can give a random number between 0 and 4095
        episodes = 10
        for episode in range(1, episodes + 1):
            state = self.env.reset()
            done = False
            score = 0

            while not done:
                # env.render()
                action_number = random.randint(0, self.actions - 1)
                action = number_to_position(action_number)
                try:
                    output = self.env.step(action)
                    print("Chessbot tries " + action + " successfully")
                    sleep(0.5)
                    self.env.display_game()
                except ValueError:
                    # print("Chessbot tries " + action + " unsuccessfully")
                    continue
                if output is not None:
                    print("Checkmate!")
                    score += 10000
                    break
                self.env.request_move()
                # score += reward
            print('Episode:{} Score:{}'.format(episode, score))


chessBot = ChessBot()

chessBot.test_run()

# for i in range(4096):
#     if i % 64 == 0:
#         print()
#     print(number_to_position(i), end="")

# print(number_to_position(4095))
