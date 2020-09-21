# TetrisAI

Alexey Pajitnov's Tetrisis often reffered to as classic. In this project, I have added an auto-player to the game.

The auto-player algorithm is the following genetic algorithm:
- Looks at the current and next piece, tries out all the possible moves(rotations and positions) in a cloned Tetris board
- Computes a *score* for a whole board after trying a move
- Selects the move with the highest score as its next move on the original board

The score for the board is based on four heuristics:
- Aggregate Height - sum of the height of each column
- Complete Lines - the number of complete lines in a board
- Holes - a hole is defined as an empty space such that there is at least one tile in the column above it
- Bumpiness - the variation of its column heights (sum of the absolute differences of two adjacent columns)

Each heuristic is assigned a different weight (both positive and negative), which indicates the importance of a heuristic and determined by analyzing best human-player strategies and trial.

# Setup

- Clone this repository
- Run ```python visual.py``` to view the Tkinter GUI version
- Install pygame by running ```pip install pygame``` and run ```python visual-pygame.py``` to view the PyGame version
