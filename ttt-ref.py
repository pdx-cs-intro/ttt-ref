# Tic-Tac-Toe Referee
# Bart Massey 2021

# Class representing player information.
class Player:
    def __init__(self, n):
        self.name = input(f"Player {n} name? ")
        if n == 0:
            self.side = "X"
        elif n == 1:
            self.side = "O"
        else:
            assert False

# The two players.
players = [Player(0), Player(1)]

# The board. Indexed by row and column,
# for example square 6 is board[1][2].
board = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
]

# Whose turn is it? 0 for first player, 1 for second.
on_move = 0

# Display the board in standard format.
def print_board():
    for row in board:
        print(''.join(row))

# Return the number of the opponent of Player n (0-based).
def opponent(n):
    if n == 0:
        return 1
    else:
        return 0

# Try to make given move on current board.  Return True if
# successful.
def make_move(move, side):
    global board

    # Check that move has the right format.
    if move not in "123456789":
        return False

    # Find the indicated position and replace it
    # with the side, if possible.
    for row in range(3):
        for col in range(3):
            if move == board[row][col]:
                board[row][col] = side
                return True

    # Couldn't find the position, so illegal move.
    return False

# Return "win", "draw" or "continue"
# depending on the current board state.
# Strategy: To check for a win, check for "lines" in the
# input that are all the given side's piece. To check for a
# draw, check if the board is full and no win.
def game_over(board, side):
    # Row wins.
    for r in range(3):
        if board[r][0] == side and board[r][1] == side and board[r][2] == side:
            return "win"
    # Column wins.
    for c in range(3):
        if board[0][c] == side and board[1][c] == side and board[2][c] == side:
            return "win"
    # Diagonal wins.
    if board[0][0] == side and board[1][1] == side and board[2][2] == side:
        return "win"
    if board[0][2] == side and board[1][1] == side and board[2][0] == side:
        return "win"

    # Not a draw.
    for r in range(3):
        for c in range(3):
            if board[r][c].isdigit():
                return "continue"

    # Must be a draw.
    return "draw"

empty_board = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
]
assert game_over(empty_board, 'X') == "continue"
assert game_over(empty_board, 'O') == "continue"

draw_board = [
    ['X', 'X', 'O'],
    ['O', 'X', 'X'],
    ['X', 'O', 'O'],
]
assert game_over(draw_board, 'X') == "draw"
assert game_over(draw_board, 'O') == "draw"

win_board = [
    ['X', '2', 'O'],
    ['O', 'X', '5'],
    ['X', 'O', 'X'],
]
assert game_over(win_board, 'X') == "win"
assert game_over(win_board, 'O') == "continue"

# Process moves until game over.
while True:
    print_board()
    current_player = players[on_move]
    name = current_player.name
    move = input(f"Your move, {name}? ").strip()
    if not make_move(move, current_player.side):
        opponent_name = players[opponent(on_move)].name
        print(f"Illegal move, {name}.")
        print(f"{opponent_name} wins!")
        break
    result = game_over(board, current_player.side)
    if result != "continue":
        print_board()
        if result == "win":
            print(f"{name} wins!")
        elif result == "draw":
            print("draw")
        else:
            assert False
        break
    on_move = opponent(on_move)
