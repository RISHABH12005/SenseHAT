from sense_hat import SenseHat
from time import sleep
import keyboard  # For keyboard input

sense = SenseHat()

X_COLOR = [255, 0, 0]
O_COLOR = [0, 0, 255]
EMPTY_COLOR = [0, 0, 0]
CURSOR_COLOR = [0, 255, 0]
GRID_COLOR = [255, 255, 255]  # White grid color

board = [[None for _ in range(3)] for _ in range(3)]
current_player = "X"
cursor_x, cursor_y = 0, 0

def draw_board():
    sense.clear()
    # Draw grid lines
    for i in range(1, 3):
        # Horizontal lines
        for x in range(8):
            sense.set_pixel(x, i * 3 - 1, GRID_COLOR)
        # Vertical lines
        for y in range(8):
            sense.set_pixel(i * 3 - 1, y, GRID_COLOR)
    
    # Draw X and O markers
    for y in range(3):
        for x in range(3):
            pixel_x = x * 3
            pixel_y = y * 3
            if board[y][x] == "X":
                sense.set_pixel(pixel_x, pixel_y, X_COLOR)
                sense.set_pixel(pixel_x + 1, pixel_y, X_COLOR)
                sense.set_pixel(pixel_x, pixel_y + 1, X_COLOR)
                sense.set_pixel(pixel_x + 1, pixel_y + 1, X_COLOR)
            elif board[y][x] == "O":
                sense.set_pixel(pixel_x, pixel_y, O_COLOR)
                sense.set_pixel(pixel_x + 1, pixel_y, O_COLOR)
                sense.set_pixel(pixel_x, pixel_y + 1, O_COLOR)
                sense.set_pixel(pixel_x + 1, pixel_y + 1, O_COLOR)

    # Draw cursor
    cursor_pixel_x = cursor_x * 3
    cursor_pixel_y = cursor_y * 3
    sense.set_pixel(cursor_pixel_x, cursor_pixel_y, CURSOR_COLOR)
    sense.set_pixel(cursor_pixel_x + 1, cursor_pixel_y, CURSOR_COLOR)
    sense.set_pixel(cursor_pixel_x, cursor_pixel_y + 1, CURSOR_COLOR)
    sense.set_pixel(cursor_pixel_x + 1, cursor_pixel_y + 1, CURSOR_COLOR)

def check_winner():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0]:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i]:
            return board[0][i]
    
    if board[0][0] == board[1][1] == board[2][2] and board[0][0]:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2]:
        return board[0][2]
    
    if all(all(cell for cell in row) for row in board):
        return "Draw"
    
    return None

def move_cursor(dx, dy):
    global cursor_x, cursor_y
    cursor_x = (cursor_x + dx) % 3
    cursor_y = (cursor_y + dy) % 3
    draw_board()

def place_marker():
    global current_player
    if board[cursor_y][cursor_x] is None:
        board[cursor_y][cursor_x] = current_player
        winner = check_winner()
        if winner:
            sense.show_message(f"{winner} wins!" if winner != "Draw" else "Draw!")
            reset_game()
        else:
            current_player = "O" if current_player == "X" else "X"
        draw_board()

def reset_game():
    global board, current_player, cursor_x, cursor_y
    board = [[None for _ in range(3)] for _ in range(3)]
    current_player = "X"
    cursor_x, cursor_y = 0, 0
    draw_board()

draw_board()

while True:
    if keyboard.is_pressed('up'):
        move_cursor(0, -1)
        sleep(0.2)
    elif keyboard.is_pressed('down'):
        move_cursor(0, 1)
        sleep(0.2)
    elif keyboard.is_pressed('left'):
        move_cursor(-1, 0)
        sleep(0.2)
    elif keyboard.is_pressed('right'):
        move_cursor(1, 0)
        sleep(0.2)
    elif keyboard.is_pressed('enter'):  # Use Enter key to place marker
        place_marker()
        sleep(0.2)
