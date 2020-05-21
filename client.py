from adversary import RandomAdversary
from board import Board, Direction, Rotation, Shape
from constants import BOARD_HEIGHT, BOARD_WIDTH, BLOCK_LIMIT, PREFIX
from exceptions import UnknownInstructionException, BlockLimitException
from player import Player

from sys import stderr
from os import getenv


class RemotePlayer(Player):
    def choose_action(self, board):
        while True:
            try:
                instruction = input().strip()
            except EOFError:
                raise UnknownInstructionException

            if instruction.startswith(PREFIX):
                break

        instruction = instruction[len(PREFIX)+1:]

        if instruction == 'SKIP':
            return None

        try:
            return Direction(instruction)
        except ValueError:
            pass

        try:
            return Rotation(instruction)
        except ValueError:
            pass

        raise UnknownInstructionException


board = Board(BOARD_WIDTH, BOARD_HEIGHT)

player = RemotePlayer()
adversary = RandomAdversary(getenv('SEED'), BLOCK_LIMIT)


score = 0
try:
    for move in board.run(player, adversary):
        if isinstance(move, Shape):
            print(f'{PREFIX} {move.value}')

        if board.score != score:
            stderr.write(f'{board.score}\n')
            score = board.score
except BlockLimitException:
    stderr.write('WON\n')
    print(f'{PREFIX} WON')
else:
    stderr.write('LOST\n')
    print(f'{PREFIX} LOST')
