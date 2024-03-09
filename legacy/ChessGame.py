from time import sleep
import random
from typing import Optional
import numpy as np
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

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
            temp_board.push_uci(str(move))
            self.board_display.update_pieces(temp_board.fen())

    def reset(self):
        self.board.reset()
        return get_position_as_array(self.board.fen())

    def step(self, action: str):
        move_is_legal = True
        reward = 0
        if self.board.is_checkmate():
            print("ChessNet has lost by checkmate")
            reward += -10_000
            return None, reward, True
        try:
            self.board.push_uci(action)
            reward += 1
        except ValueError:
            reward += -100
            move_is_legal = False

        is_checkmate = self.board.is_checkmate()
        if is_checkmate:
            reward += 10_000
        state = self.board.fen
        return state, reward, is_checkmate, move_is_legal

    def request_move_from_opponent(self):
        self.board.push([i for i in self.board.legal_moves][0])


class ChessBot:

    def __init__(self):
        self.env = ChessBoard()
        self.states = self.env.N_SQUARES
        self.actions = self.env.N_ALL_MOVES

    def get_best_move(self):
        pass

    def test_run(self):
        episodes = 10
        for episode in range(1, episodes + 1):
            state = self.env.reset()
            done = False
            total_reward = 0

            while not done:
                # env.render()
                action_number = random.randint(0, self.actions - 1)
                action = number_to_position(action_number)
                state, reward, done, move_was_legal = self.env.step(action)
                total_reward += reward
                if move_was_legal:
                    print("Chessbot executes " + action)
                    sleep(0.5)
                    self.env.display_game()
                else:
                    continue
                if done:
                    print("Checkmate!")
                    break
                self.env.request_move_from_opponent()
                total_reward += reward
            print('Episode:{} Score:{}'.format(episode, total_reward))


class ChessNet:

    def __init__(self):
        self.model = self._build_model()
        self.chess_board = ChessBoard()
        self.board = self.chess_board.board
        self.learning_rate = 0.001

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(24, input_dim=fen_to_array(self.board.fen()), activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(ChessBoard.N_ALL_MOVES, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        print(model.summary())
        return model


def fen_to_array(fen):
    # Converts FEN notation to a numpy array suitable for input to a neural network

    # Mapping of piece characters to integers
    piece_to_int = {'p': 1, 'r': 2, 'n': 3, 'b': 4, 'q': 5, 'k': 6,
                    'P': 7, 'R': 8, 'N': 9, 'B': 10, 'Q': 11, 'K': 12}

    # Initialize an empty board array
    board_array = np.zeros((8, 8, 12), dtype=np.int8)

    # Split FEN string into its components
    fen_parts = fen.split(' ')

    # Parse the piece placement part of FEN
    row_strs = fen_parts[0].split('/')
    for i, row_str in enumerate(row_strs):
        j = 0
        for char in row_str:
            if char.isdigit():
                j += int(char)
            else:
                board_array[i, j, piece_to_int[char] - 1] = 1
                j += 1

    return board_array
