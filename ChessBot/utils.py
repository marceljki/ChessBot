from typing import Optional


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
