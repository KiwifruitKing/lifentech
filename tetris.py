import curses
import random
import time

# Board dimensions
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

# Tetromino shapes (rotations)
TETROMINOS = {
    'I': [
        [(0,0), (1,0), (2,0), (3,0)],
        [(2,-1), (2,0), (2,1), (2,2)],
    ],
    'O': [
        [(1,0), (2,0), (1,1), (2,1)],
    ],
    'T': [
        [(1,0), (0,1), (1,1), (2,1)],
        [(1,0), (1,1), (2,1), (1,2)],
        [(0,1), (1,1), (2,1), (1,2)],
        [(1,0), (0,1), (1,1), (1,2)],
    ],
    'S': [
        [(1,0), (2,0), (0,1), (1,1)],
        [(1,0), (1,1), (2,1), (2,2)],
    ],
    'Z': [
        [(0,0), (1,0), (1,1), (2,1)],
        [(2,0), (1,1), (2,1), (1,2)],
    ],
    'J': [
        [(0,0), (0,1), (1,1), (2,1)],
        [(1,0), (2,0), (1,1), (1,2)],
        [(0,1), (1,1), (2,1), (2,2)],
        [(1,0), (1,1), (0,2), (1,2)],
    ],
    'L': [
        [(2,0), (0,1), (1,1), (2,1)],
        [(1,0), (1,1), (1,2), (2,2)],
        [(0,1), (1,1), (2,1), (0,2)],
        [(0,0), (1,0), (1,1), (1,2)],
    ],
}

class Tetromino:
    def __init__(self, shape):
        self.shape = shape
        self.rotation = 0
        self.x = BOARD_WIDTH // 2 - 2
        self.y = 0

    def coords(self):
        return [ (self.x + x, self.y + y) for x, y in TETROMINOS[self.shape][self.rotation] ]

    def rotate(self, board):
        next_rot = (self.rotation + 1) % len(TETROMINOS[self.shape])
        for x, y in [ (self.x + dx, self.y + dy) for dx, dy in TETROMINOS[self.shape][next_rot] ]:
            if x < 0 or x >= BOARD_WIDTH or y < 0 or y >= BOARD_HEIGHT or board[y][x]:
                return False
        self.rotation = next_rot
        return True

    def move(self, dx, dy, board):
        for x, y in [ (self.x + dx + px, self.y + dy + py) for px, py in TETROMINOS[self.shape][self.rotation] ]:
            if x < 0 or x >= BOARD_WIDTH or y < 0 or y >= BOARD_HEIGHT or board[y][x]:
                return False
        self.x += dx
        self.y += dy
        return True


def create_board():
    return [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]


def draw_board(stdscr, board, current):
    stdscr.clear()
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            if board[y][x]:
                stdscr.addstr(y, x*2, '[]')
            else:
                stdscr.addstr(y, x*2, ' .')
    for x, y in current.coords():
        if 0 <= y < BOARD_HEIGHT:
            stdscr.addstr(y, x*2, '[]')
    stdscr.refresh()


def merge_piece(board, piece):
    for x, y in piece.coords():
        if 0 <= y < BOARD_HEIGHT and 0 <= x < BOARD_WIDTH:
            board[y][x] = 1
    # Clear full lines
    new_board = [row for row in board if not all(row)]
    cleared = BOARD_HEIGHT - len(new_board)
    board[:] = [[0]*BOARD_WIDTH for _ in range(cleared)] + new_board
    return cleared


def game(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(200)

    board = create_board()
    current = Tetromino(random.choice(list(TETROMINOS.keys())))
    score = 0

    while True:
        draw_board(stdscr, board, current)
        key = stdscr.getch()
        if key == curses.KEY_LEFT:
            current.move(-1, 0, board)
        elif key == curses.KEY_RIGHT:
            current.move(1, 0, board)
        elif key == curses.KEY_UP:
            current.rotate(board)
        elif key == curses.KEY_DOWN:
            if not current.move(0, 1, board):
                merge_piece(board, current)
                score += 1
                current = Tetromino(random.choice(list(TETROMINOS.keys())))
                if not current.move(0,0,board):
                    break
        else:
            if not current.move(0, 1, board):
                merge_piece(board, current)
                score += 1
                current = Tetromino(random.choice(list(TETROMINOS.keys())))
                if not current.move(0,0,board):
                    break
        time.sleep(0.05)

    stdscr.nodelay(False)
    stdscr.addstr(BOARD_HEIGHT+1, 0, f"Game Over! Score: {score}")
    stdscr.getch()

if __name__ == '__main__':
    curses.wrapper(game)
