# Advent of code

This repo contains my solutions to the advent of code puzzles.

**Purpose:**

I started solving the AoC puzzles mainly for fun.

I try to keep solutions as I submitted them at the time. Thus, I do not edit past solutions (even if I would find
another algorithm and/or write the code differently nowadays).

**Years:**
- 2021: 18/50 stars (First time doing the AoC).
- 2022: 38/50 stars.
- 2023: 50/50 stars. 6310<sup>th</sup> to solve all 50 puzzles.


## Getting started

### Installation

Create virtual env:
```
python3 -m venv .venv
```

Activate it:
```
source .venv/bin/activate
```

Install all dependencies (NB: I try to use as few as possible):
```
python3 -m pip install -r requirements.txt
```

_NB: to install an individual package without adding it in the `requirements.txt` file_
```
python3 -m pip install <package>
```

### Fetch data from private repo with `git submodule`

The creator and maintainers of the Advent of Code ask participants [to
_not_ share their puzzle inputs publicly](https://www.reddit.com/r/adventofcode/wiki/faqs/copyright/inputs/).
Thus, I use `git submodule` to keep my puzzle inputs under version control in a private repo.

To fetch the data after cloning the repo, do:
```
git submodule init
git submodule update
```

### Solve puzzles

To solve the puzzles for any day, execute:
```
python3 2023/day01.py
```

