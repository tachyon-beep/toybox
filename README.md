# Game of Life Toy

This repository demonstrates a small Python implementation of Conway's Game of Life.
The program runs entirely on the CPU and depends only on the Python standard library.
It can generate a random board or load one from a text file, then display each
generation using ASCII characters.

Usage:

```bash
python game_of_life.py WIDTH HEIGHT STEPS [--seed PROB] [--delay SECONDS]
```

Run the test suite with:

```bash
pytest
```
