from adversary import Adversary
from board import Board, Direction, Rotation, Shape
from constants import BOARD_HEIGHT, BOARD_WIDTH, PREFIX
from exceptions import UnknownInstructionException
from player import SelectedPlayer


class RemoteAdversary(Adversary):
    def choose_block(self, board):
        while True:
            try:
                command = input().strip()
            except EOFError:
                raise SystemExit

            if command.startswith(PREFIX):
                break

        command = command[len(PREFIX)+1:]

        if command == 'WON' or command == 'LOST':
            # Game ended; stop cleanly.
            raise SystemExit

        try:
            return Shape(command)
        except ValueError:
            pass

        raise UnknownInstructionException


board = Board(BOARD_WIDTH, BOARD_HEIGHT)

player = SelectedPlayer()
adversary = RemoteAdversary()

for move in board.run(player, adversary):
    if isinstance(move, Direction):
        print(f'{PREFIX} {move.value}')
    elif isinstance(move, Rotation):
        print(f'{PREFIX} {move.value}')
    elif move is None:
        print(f'{PREFIX} SKIP')
