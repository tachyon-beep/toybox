import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import game_of_life as gol


def board_from_strings(strings):
    board = set()
    h = len(strings)
    w = max(len(s) for s in strings)
    for y, row in enumerate(strings):
        for x, ch in enumerate(row):
            if ch == '#':
                board.add((x, y))
    return board, w, h


def strings_from_board(board, w, h):
    return [
        ''.join('#' if (x, y) in board else '.' for x in range(w))
        for y in range(h)
    ]


def test_blinker_oscillator():
    """Blinker should oscillate every step."""
    initial, w, h = board_from_strings([
        ".....",
        "..#..",
        "..#..",
        "..#..",
        ".....",
    ])
    expected, _, _ = board_from_strings([
        ".....",
        ".....",
        ".###.",
        ".....",
        ".....",
    ])
    next_gen = gol.step(initial, w, h)
    assert strings_from_board(next_gen, w, h) == strings_from_board(expected, w, h)

    # Oscillate back
    next_gen2 = gol.step(next_gen, w, h)
    assert strings_from_board(next_gen2, w, h) == strings_from_board(initial, w, h)


def test_block_still_life():
    initial, w, h = board_from_strings([
        "....",
        ".##.",
        ".##.",
        "....",
    ])
    next_gen = gol.step(initial, w, h)
    assert strings_from_board(next_gen, w, h) == strings_from_board(initial, w, h)
