# Minimal implementation of Conway's Game of Life
# This module provides a simple command-line interface to run the
# cellular automaton. The code is intentionally small and relies only
# on the Python standard library so it can run on any CPU-only machine.
#
# Design choices:
# - The board is represented as a set of coordinate tuples for live cells.
#   Sets make it cheap to test membership and iterate only over living cells.
# - The automaton wraps around edges (toroidal topology) so the board is
#   finite but has no borders.
# - A basic text-based display prints '#' for live cells and '.' for dead cells.
# - The script can randomize an initial board or load from a text file.
# - All functions are kept small for clarity, and the total code is under
#   300 lines including comments and blank lines.

import argparse
import random
import time
from typing import Set, Tuple

Coordinate = Tuple[int, int]


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Conway's Game of Life")
    parser.add_argument("width", type=int, help="board width")
    parser.add_argument("height", type=int, help="board height")
    parser.add_argument("steps", type=int, help="number of generations to run")
    parser.add_argument(
        "--seed", type=float, default=0.3,
        help="probability of a cell being alive at start (0-1)"
    )
    parser.add_argument(
        "--delay", type=float, default=0.3,
        help="seconds to wait between steps"
    )
    parser.add_argument(
        "--file", type=str, default=None,
        help="load initial configuration from text file"
    )
    return parser.parse_args()


def neighbors(x: int, y: int, w: int, h: int) -> Set[Coordinate]:
    """Return the set of neighbor coordinates wrapping around edges."""
    return {
        ((x + dx) % w, (y + dy) % h)
        for dx in (-1, 0, 1)
        for dy in (-1, 0, 1)
        if not (dx == 0 and dy == 0)
    }


def step(board: Set[Coordinate], w: int, h: int) -> Set[Coordinate]:
    """Compute the next generation from the current board."""
    new_board: Set[Coordinate] = set()
    # Count neighbors of all cells that might change: existing live cells
    # and their neighbors. The dictionary maps coordinates to live neighbor
    # count.
    counts = {}
    for cell in board:
        for n in neighbors(*cell, w, h):
            counts[n] = counts.get(n, 0) + 1
    for cell, ncount in counts.items():
        if ncount == 3 or (ncount == 2 and cell in board):
            new_board.add(cell)
    return new_board


def random_board(w: int, h: int, probability: float) -> Set[Coordinate]:
    """Generate a random board with given live-cell probability."""
    return {
        (x, y)
        for x in range(w)
        for y in range(h)
        if random.random() < probability
    }


def load_board(path: str) -> Set[Coordinate]:
    """Load a board from a text file of '#' and '.' characters."""
    board = set()
    with open(path) as f:
        lines = [line.rstrip("\n") for line in f]
    h = len(lines)
    w = max(len(line) for line in lines) if lines else 0
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            if ch == '#':
                board.add((x, y))
    return board, w, h


def display(board: Set[Coordinate], w: int, h: int) -> None:
    """Print the board to stdout."""
    for y in range(h):
        row = ''.join('#' if (x, y) in board else '.' for x in range(w))
        print(row)
    print()


def main() -> None:
    args = parse_args()
    if args.file:
        board, w, h = load_board(args.file)
    else:
        w, h = args.width, args.height
        board = random_board(w, h, args.seed)
    display(board, w, h)
    for _ in range(args.steps):
        board = step(board, w, h)
        time.sleep(args.delay)
        display(board, w, h)


if __name__ == "__main__":
    main()
