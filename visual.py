from threading import Condition, Thread
from time import sleep
from tkinter import Tk, Canvas, Frame, BOTH, TclError

from adversary import RandomAdversary
from arguments import parser
from board import Board, Direction, Rotation
from constants import BOARD_HEIGHT, BOARD_WIDTH, DEFAULT_SEED, INTERVAL
from player import SelectedPlayer, Player

DRAW_INTERVAL = 100


class Visual(Frame):
    board = None
    canvas = None

    CELL_SIZE = 20

    def __init__(self, board):
        super().__init__()

        self.board = board

        self.master.geometry(
            f'{(BOARD_WIDTH+6)*self.CELL_SIZE}x' +
            f'{BOARD_HEIGHT*self.CELL_SIZE}'
        )

        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=1)

        self.after(DRAW_INTERVAL, self.draw)

        self.focus_set()
        self.bind("<Escape>", self.quit)

    def quit(self, event):
        raise SystemExit

    def draw_cell(self, x, y, color):
        self.canvas.create_rectangle(
            x * self.CELL_SIZE,
            y * self.CELL_SIZE,
            (x+1) * self.CELL_SIZE,
            (y+1) * self.CELL_SIZE,
            fill=color,
            outline=color,
        )

    def draw(self):
        with self.board.lock:
            self.canvas.delete('all')

            if self.board.falling is not None:
                for (x, y) in self.board.falling:
                    self.draw_cell(x, y, self.board.falling.color)

            if self.board.next is not None:
                for (x, y) in self.board.next:
                    self.draw_cell(
                        x + self.board.width + 2,
                        y + 1,
                        self.board.next.color
                    )

            for (x, y) in self.board:
                self.draw_cell(x, y, self.board.cellcolor[x, y])

            x = self.board.width * self.CELL_SIZE + 1
            y = self.board.height * self.CELL_SIZE
            self.canvas.create_line(x, 0, x, y, fill='black')

            self.master.title(f'Score: {self.board.score}')

            self.after(DRAW_INTERVAL, self.draw)


class UserPlayer(Player):
    has_move = None
    target = None
    next_move = None

    def __init__(self, target):
        self.has_move = Condition()
        self.target = target

        target.focus_set()
        target.bind("<Up>", self.key)
        target.bind("<Right>", self.key)
        target.bind("<Down>", self.key)
        target.bind("<Left>", self.key)
        target.bind("<space>", self.key)
        target.bind("z", self.key)
        target.bind("x", self.key)

        target.after(INTERVAL, self.drop)

    def key(self, event):
        with self.has_move:
            if event.keysym == 'Up':
                self.next_move = Rotation.Clockwise
            elif event.keysym == 'Right':
                self.next_move = Direction.Right
            elif event.keysym == 'Down':
                self.next_move = Direction.Down
            elif event.keysym == 'Left':
                self.next_move = Direction.Left
            elif event.keysym == 'space':
                self.next_move = Direction.Drop
            elif event.keysym == 'z':
                self.next_move = Rotation.Clockwise
            elif event.keysym == 'x':
                self.next_move = Rotation.Anticlockwise
            else:
                return

            self.has_move.notify()

    def drop(self):
        with self.has_move:
            self.next_move = None
            self.has_move.notify()

        self.target.after(INTERVAL, self.drop)

    def choose_action(self, board):
        with self.has_move:
            self.has_move.wait()
            try:
                return self.next_move
            finally:
                self.next_move = None


def run():
    root = Tk()

    # Try making window a dialog if the system allows it.
    try:
        root.attributes('-type', 'dialog')
    except TclError:
        pass

    args = parser.parse_args()
    if args.manual:
        player = UserPlayer(root)
    else:
        player = SelectedPlayer()

    adversary = RandomAdversary(DEFAULT_SEED)
    board = Board(BOARD_WIDTH, BOARD_HEIGHT)

    def runner():
        for move in board.run(player, adversary):
            # When not playing manually, allow some time to see the move.
            if not args.manual:
                sleep(0.01)

    Visual(board)

    background = Thread(target=runner)
    background.daemon = True
    background.start()

    root.mainloop()

    raise SystemExit


if __name__ == '__main__':
    run()
