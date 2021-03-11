# Tic-Tac-Toe Referee / Player
# Bart Massey 2021

# Computer chooses randomly from equivalent moves.
import random

# Class representing player information.
class Player:
    def __init__(self, n, name, human):
        if n == 0:
            self.side = "X"
        elif n == 1:
            self.side = "O"
        else:
            assert False
        self.name = name
        self.human = human

# Set up the game.
players = []
for n in range(2):
    name = input(f"Player {n} name (empty for computer)? ")
    if name == "":
        name = ["Alpha", "Beta"][n]
        players.append(Player(n, name, False))
    else:
        players.append(Player(n, name, True))

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
# successful. Modifies board.
def make_move(board, move, side):
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

# Select a computer move. Returns result/move tuple: None
# for finished position else move character; -1 for a losing
# position, 0 for a drawn position, 1 for a winning
# position. Always returns with board unmodified.

# Strategy: Try each legal move and see how the game
# continues from there. Prefer a move which forces opponent
# to lose, else a move which forces a draw.

# XXX This is fairly deep and tricky recursive code.
def computer_move(board, n):
    # XXX Need to compute side from player number.
    side = "XO"[n]
    opp_side = "XO"[opponent(n)]

    # Check for finished position. XXX Want to know whether
    # *opponent* just won.
    result = game_over(board, opp_side)
    if result != "continue":
        if result == "win":
            return (-1, None)
        elif result == "draw":
            return (0, None)
        else:
            # Opponent could not have made you win.
            assert False

    # Find legal moves by position.
    # moves is list of row/column tuples.
    moves = []
    for r in range(3):
        for c in range(3):
            if board[r][c].isdigit():
                moves.append((r, c))
    
    # Find results of moves.
    # results is list of winning, drawn, losing moves
    # for this side.
    results = [[],[],[]]
    for (r, c) in moves:
        # Remember previous contents of board.
        digit = board[r][c]
        # Make the move.
        assert make_move(board, digit, side)
        # Find out the result of playing from there.
        opp_result, _ = computer_move(board, opponent(n))
        # Remember the result.
        results[opp_result + 1].append(digit)
        # Undo the move to put the board back.
        board[r][c] = digit
    
    # Pick a random move in order of preference.
    for result_type in range(3):
        possibilities = results[result_type]
        if possibilities != []:
            move = random.choice(possibilities)
            return (1 - result_type, move)

    # Should always have a move.
    assert False
        
# Unit tests for computer_move().
test_board = [
    ['X', 'X', 'O'],
    ['4', 'O', '6'],
    ['X', 'O', '9'],
]
result = computer_move(test_board, 0)
assert result == (1, '4')
test_board = [
    ['X', 'X', 'O'],
    ['4', 'X', '6'],
    ['X', 'O', 'O'],
]
result = computer_move(test_board, 1)
assert result == (1, '6')

# Process moves until game over.
while True:
    # Set up for moving.
    print_board()
    print()
    current_player = players[on_move]
    name = current_player.name

    # Get and make a move.
    if current_player.human:
        move = input(f"Your move, {name}? ").strip()
        if not make_move(board, move, current_player.side):
            opponent_name = players[opponent(on_move)].name
            print(f"Illegal move, {name}.")
            print(f"{opponent_name} wins!")
            break
    else:
        _, move = computer_move(board, on_move)
        assert make_move(board, move, current_player.side)

    # Check for done.
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

    # Change sides.
    on_move = opponent(on_move)
