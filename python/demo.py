# ========================================================================
# Imports
# ========================================================================

# The GUI toolkit
import tkinter as tk

# Conway's Game of Life (our code)
exec(open("game_of_life.py").read())

# ========================================================================
# Prompt the user for board characteristics.
# ========================================================================
#
# Before creating the GUI below, as the user for a board size and whether the
# board/world should be a torus.

# Function to prompt until we get an answer we like.
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

# Function to determine whether a string represents a positive integer.
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

# Function to determine whether a string represents a yes/no response.
def parse_yes_no(string, default = 'n'):
    """Parse 'yes'/'y' and 'no'/'n' as bools (True and False, respectively)."""
    if string == '':
        string = default

    if string == 'yes' or string == 'y':
        return (True, True)
    elif string == 'n' or string == 'n':
        return (True, False)
    else:
        return (False, None)

# Get a board size from the user.
default_size = 30
str_prompt = "Specify a number of {0} for the board (default " \
             + str(default_size) +  "): "
fcn_parse = lambda string: (True, default_size) if string == '' else parse_positive_int(string)

num_rows = my_prompt(str_prompt.format('rows'), fcn_parse)
num_cols = my_prompt(str_prompt.format('columns'), fcn_parse)

# Should we play on a torus?
fcn_parse_torus = lambda string: (True, False) if string == '' else parse_yes_no(string)
on_torus = my_prompt("Make the board a torus (a la Pac-Man)? y/[n]: ", parse_yes_no)

# Initialize a random game.
game = GameOfLife(num_rows, num_cols, on_torus = on_torus)
game.randomize_board()

# ========================================================================
# A simple GUI demo
# ========================================================================
#
# Draw the board we created above, and update it every 250 milliseconds as long
# as there is life on the board.  No additional interaction is supported.

# Create a canvas for drawing to.
master = tk.Tk()
master.title("Conway's Game of Life")
w = tk.Canvas(master, width = 10 * num_cols, height = 10 * num_rows)
w.pack()

# Create the rectangles with which we'll draw the game.
rects = Array2D(game.rows, game.cols, eltype = int)

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
