import random
from time import sleep

import chess
import numpy as np
from chessboard import display
from keras import Sequential
from keras.src.layers import Dense
from keras.src.optimizers import Adam
from typing import Optional


class ChessBot:
    N_ALL_MOVES = 4096
    N_SQUARES = 64

    def __init__(self):
        self.board = chess.Board()
        self.board_display = None
        # AI stuff
        self.model = self.build_model()
        self.learning_rate = 0.001
        self.actions = self.N_ALL_MOVES

    def play_chess(self):
        state = self.board.reset()
        done = False
        total_reward = 0

        while not done:
            action_number = random.randint(0, self.actions - 1)
            action = number_to_position(action_number)
            state, reward, done, move_was_legal = self.step(action)
            total_reward += reward
            if move_was_legal:
                print("Chessbot executes " + action)
                sleep(0.5)
                self.display_game()
            else:
                continue
            if done:
                print("Checkmate!")
                break
            self.request_move_from_opponent()

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

    def display_game(self):
        self.board_display = display.start(self.board.fen())
        temp_board = chess.Board()
        for move in self.board.move_stack:
            temp_board.push_uci(str(move))
            self.board_display.update_pieces(temp_board.fen())

    def build_model(self):
        model = Sequential()
        model.add(Dense(24, input_dim=fen_to_array(self.board.fen()), activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.N_ALL_MOVES, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        print(model.summary())
        return model


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

chessBot = ChessBot()
chessBot.play_chess()