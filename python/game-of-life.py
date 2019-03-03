
# ========================================================================
# Conway's Game of Life
# ========================================================================

# A python implementation of Conway's Game of Life.  See
# https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life for more information.
#
# Here are the basic rules:
# - Any live cell with fewer than two live neighbors dies, as if by underpopulation.
# - Any live cell with two or three live neighbors lives on to the next generation.
# - Any live cell with more than three live neighbors dies, as if by overpopulation.
# - Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.

# We'll need some randomness.
import random

class GameOfLife:
    """A board/world on which Conway's Game of Life will be played/lived.  Each such
    board should contain the following variables:
    - `board`: the current state of the game
    - `rows`: the number of rows in the board
    - `cols`: the number of columns in the board
    - `on_torus`: if `True`, play pac-man style (left/right, top/bottom adjacent)
    """

    def __init__(self, num_rows, num_cols, on_torus = False):
        """Create a new board on which to play the Game of Life."""
        # Create the board.
        board = GameOfLife.create_empty_board(num_rows, num_cols)

        # Store the board and its dimensions in the object.
        # TODO: It'd be bad if someone modified these.  Can they be made private?
        self.rows = num_rows
        self.cols = num_cols
        self.board = board

        # Store some variables related to indexing.
        self.on_torus = True if on_torus else False

    @staticmethod
    def create_empty_board(num_rows, num_cols):
        """Create an empty board for the Game of Life."""
        return [[False for j in range(num_cols)]
                 for i in range(num_rows)]

    def randomize_board(self, prob_alive = 0.25):
        """Set the board to a random state with each entry having `prob_alive` chance of
        being alive."""

        assert 0 < prob_alive < 1, \
            "The parameter `prob_alive` must be strictly between zero and one."

        # Set each entry randomly.
        self.board = [[random.random() < prob_alive for j in range(num_cols)]
                      for i in range(num_rows)]

    def row_inbounds(self, row):
        """Determine whether the given row is valid."""
        return True if self.on_torus else (0 <= row < self.rows)

    def col_inbounds(self, col):
        """Determine whether the given col is valid."""
        return True if self.on_torus else (0 <= col < self.cols)

    def __getitem__(self, key):
        """Access the current state of a given cell of the game using two indices."""

        # We need to make sure that exactly two indices have been provided.
        assert len(key) == 2, \
            "Exactly two indices are required to index a `GameOfLife` board."
        row, col = key

        if self.on_torus:
            # Any index is valid on a torus.  Just wrap the indices.
            row %= self.rows
            col %= self.cols
        else:
            # In a regular (i.e., non-torus) world, we need to make sure we
            # don't go out of bounds.
            assert self.row_inbounds(row), "Row index out of bounds"
            assert self.col_inbounds(col), "Column index out of bounds"

        # Return the requested item.
        return self.board[row][col]

    def count_neighbors(self, row, col):
        """Count how many neighbors a given cell has."""

        # Regardless of board indexing (which depends on whether we're living on
        # a torus), we'll only allow counting of the neighbors of an entry
        # specified with it's canonical/natural coordinates.
        assert 0 <= row < self.rows, "Row index out of bounds"
        assert 0 <= col < self.cols, "Column index out of bounds"

        # Create lists of row and column indices for the neighbors.
        offsets = range(-1, 2)
        row_indices = [row + x for x in offsets]
        col_indices = [col + x for x in offsets]

        # Remove indices that don't fall within the bounds of the board, which
        # only exist if we're not living on a torus.
        if not self.on_torus:
            row_indices = [r for r in row_indices if self.row_inbounds(r)]
            col_indices = [c for c in col_indices if self.col_inbounds(c)]

        # Count the number of neighbors.  (We're counting the current entry,
        # too, and will adjust later.)
        num_neighbors = 0

        for r in row_indices:
            for c in col_indices:
                num_neighbors += self[r, c]

        # We over-counted.  Subtract the value of the current element.
        num_neighbors -= self[row, col]

        # Return the count.
        return num_neighbors

    def update(self):
        """Update the current board state."""

        # Create an empty board.  We'll fill it, then replace the current board.
        #
        # NOTE: Maybe I should create a new `GameOfLife` object here.  There
        # would be some overhead, bu tit might be more convenient.
        board_new = GameOfLife.create_empty_board(self.rows, self.cols)

        # Update each board element one at a time...
        for row in range(self.rows):
            for col in range(self.cols):
                # Count the number of neighbors of the current entry.
                num_neighbors = self.count_neighbors(row, col)

                # This is the basic game logic.  By initializing everything to
                # false in the new board (i.e., everything is dead), we only
                # need to specify where life occurs (or, rather, might occur) in
                # the new board.
                if self[row, col]:
                    board_new[row][col] = (2 <= num_neighbors <= 3)
                else:
                    board_new[row][col] = (num_neighbors == 3)

        # Update the board.
        self.board = board_new

    def has_life(self):
        num_alive = sum(map(sum, self.board))
        return num_alive > 0

# ========================================================================
# Code to prompt the user for a board size
# ========================================================================

def my_prompt(msg, fcn_parse):
    """Prompt a user for input.  Proceed with the prompt until the provided function
    returns true for the given input.  Function should return a tuple
    `(is_parsable, value)` indicating whether the input was parsable and the
    value of the parsed input (which is ignored if `is_parsable` is `False`)."""
    is_parsable = False

    while not is_parsable:
        str_input = input(msg)
        is_parsable, value = fcn_parse(str_input)

    return value

def parse_positive_int(string):
    """Try to parse a string as a positive.  Return tuple `(True, num)` if `string`
    represents a positive integer `num`.  Return `(False, None)` otherwise."""
    try:
        num = int(string)
        is_positive_int = (num > 0)
    except Error():
        num = None
        is_positive_int = False

    return is_positive_int, num

# Get a board size from the user.
default_size = 30
str_prompt = "Specify a number of {0} for the board (default {0}): ".format(default_size)
fcn_parse = lambda string: (True, default_size) if string == '' else parse_positive_int(string)

num_rows = my_prompt(str_prompt.format('rows'), fcn_parse)
num_cols = my_prompt(str_prompt.format('columns'), fcn_parse)

# Initialize a random game.
game = GameOfLife(num_rows, num_cols, on_torus = True)
game.randomize_board()

# ========================================================================
# A simple tkinter interface
# ========================================================================

# Load the toolkit for drawing.
import tkinter as tk

# Create a canvas for drawing to.
master = tk.Tk()
master.title("Conway's Game of Life")
w = tk.Canvas(master, width = 10 * num_cols, height = 10 * num_rows)
w.pack()

# Create the rectangles with which we'll draw the game.
import numpy as np
rects = np.zeros((game.rows, game.cols), dtype = int)

for i in range(game.rows):
    for j in range(game.cols):
        x = 10 * j
        y = 10 * i
        rects[i, j] = w.create_rectangle(x, y, x + 10, y + 10)

# A function to draw the board.
def draw_board(canv, rects, game, clr_alive = 'black', clr_dead = 'white'):
    for i in range(game.rows):
        for j in range(game.cols):
            color = clr_alive if game[i, j] else clr_dead
            canv.itemconfig(rects[i, j], fill = color)

# Draw the board every 200 milliseconds.
def update_board():
    global after_id
    game.update()
    draw_board(w, rects, game)

    if game.has_life():
        after_id = master.after(200, update_board)

after_id = master.after(200, update_board)

# Destroy things when the window is closed.
def quit_game():
    global after_id
    master.after_cancel(after_id)
    after_id = None
    master.destroy()

master.protocol("WM_DELETE_WINDOW", quit_game)

# Run the main GUI loop.
tk.mainloop()
