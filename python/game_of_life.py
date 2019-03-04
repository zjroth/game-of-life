# ========================================================================
# Imports
# ========================================================================

# This is for creating a randomized board (which really only exists for the
# purposes of the demo in demo.py)
import random

# ========================================================================
# A two-dimensional array class
# ========================================================================
#
# A simple array class just for the heck of it.  We could obviously just use nested
# lists or numpy arrays.

class Array2D:
    def __init__(self, num_rows, num_cols, eltype):
        """Create a two-dimensional array.  The parameter `eltype` specifies the data
        type of the elements of the array (e.g., `int`, `bool`, `float`)."""
        array = [[eltype(0) for j in range(num_cols)]
                 for i in range(num_rows)]

        # Store the array and its dimensions in the object.
        self.data = array
        self.eltype = eltype
        self.dims = (num_rows, num_cols)

    def validindex(self, key):
        """Determine whether the given index is valid."""
        # We need to make sure that exactly two indices have been provided.
        correct_len = (len(key) == 2)
        row_valid = (0 <= key[0] < self.dims[0])
        col_valid = (0 <= key[1] < self.dims[1])

        return correct_len and row_valid and col_valid

    def __getitem__(self, key):
        """Get the element at the specified index."""
        # Make sure that the index is valid.
        assert self.validindex(key), "Invalid index into `Array2D`."

        # Return the requested element.
        return self.data[key[0]][key[1]]

    def __setitem__(self, key, value):
        """Set the element at the specified index to the specified value."""
        # Make sure that the index is valid.
        assert self.validindex(key), "Invalid index into `Array2D`."

        # Make sure that the value is of the correct type.
        assert self.eltype == type(value), \
            "Provided element of type `{0}` instead of type `{1}`.".format(
                type(value), self.eltype)

        # Set the element to the given value.
        self.data[key[0]][key[1]] = value

    def sum(self):
        """Sum up all of the entries in the array."""
        return sum(sum(r) for r in self.data)

# ========================================================================
# Conway's Game of Life
# ========================================================================
#
# A python implementation of Conway's Game of Life.  See
# https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life for more information.
#
# Here are the basic rules:
# - Any live cell with fewer than two live neighbors dies, as if by underpopulation.
# - Any live cell with two or three live neighbors lives on to the next generation.
# - Any live cell with more than three live neighbors dies, as if by overpopulation.
# - Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.

# The main code for Conway's Game of Life.
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
        board = Array2D(num_rows, num_cols, eltype = bool)

        # Store the board and its dimensions in the object.
        # TODO: It'd be bad if someone modified these.  Can they be made private?
        self.board = board
        self.cols = num_cols
        self.rows = num_rows

        # Store some variables related to indexing.
        self.on_torus = True if on_torus else False

    def randomize_board(self, prob_alive = 0.25):
        """Set the board to a random state with each entry having `prob_alive` chance of
        being alive."""

        assert 0 < prob_alive < 1, \
            "The parameter `prob_alive` must be strictly between zero and one."

        # Set each entry randomly.
        for i in range(num_rows):
            for j in range(num_cols):
                self.board[i, j] = (random.random() < prob_alive)

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
        return self.board[row, col]

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
        board_new = Array2D(self.rows, self.cols, eltype = bool)

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
                    board_new[row, col] = (2 <= num_neighbors <= 3)
                else:
                    board_new[row, col] = (num_neighbors == 3)

        # Update the board.
        self.board = board_new

    def has_life(self):
        """Determine whether any cells are alive on the current board."""
        num_alive = self.board.sum()
        return num_alive > 0
