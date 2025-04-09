# 🧩 Grid Game Project

This repository contains a Python-based, object-oriented grid game developed as part of a programming assignment. The project explores fundamental programming concepts through a playable game that features several game modes and different ways of solving the grid.

---

## 🎮 Game Overview

  In this project, we tackle an optimization problem on a grid, where the objective is to find the optimal pairing of cells — that is, the pairing that minimizes the total score.
The game takes place on a grid of size n × m, with n ≥ 1 and m ≥ 2.
Each cell on the grid has two attributes: a color and a value.
  In a second phase, we modify the rules of the game (how to appair the cells) and adapt the algorithms within the new rules. 

Regarding the game modes, artificial players are designed so as to strategically match cells based on these attributes to achieve the lowest possible score.

**Key Features:**
- Turn-based movement system.
- Expandable rules and game logic (e.g., scoring systems, pairing rules, ...).
- 3 game modes : PVE, PVP and IA vs IA.
- Several solving algorithms.
- Pygame interface.

---

## ⚙️ How It Works

### Game Loop
The colors of the cells are coded as follows: { 0: white ('w'), 1: red ('r'), 2: blue ('b'), 3: green ('g'), 4: black ('d') }

The rules for forming cell pairs are defined as follows: A cell can only be part of one pair at a time and can only be paired with an adjacent cell. Additionally, the pairing follows a color-based rule: 
    - Green cells (3) can only pair with white (0) or other green cells.
    - Blue cells (2) and red cells (1) can pair with each other or with a white cell (0).
    - White cells can pair with any color except black.

Once the pairs are formed according to the pairing rules, the score is calculated as follows: for each pair, take the absolute difference between the values of the two cells and add it to the score. The values of unpaired cells (except for black cells) are added to this score.

### Players
- Players can be controlled by the user or act autonomously.
- Each player tries to minimize its score (sum of the values of the chosen pairs -> for each pair: value = the difference between the values of the two cells in the pair).

### Grid
- The grid is a 2D structure that represents the cells and their values
- Cells are colored in light grey once they are used!

---

## 📁 Repository Structure

```
project_root/
│
├── src/code/               # Python code
│   ├── main.py             # Entry point to launch the algorithms 
│   ├── grid.py             # Grid management (creation, display, updates)
│   ├── solver.py           # Implements all solvers (including the ones for new rules/game modes)
│   └── pygames.py          # Game interface (3 modes)
│
├── src/ input/             # Include different grids to work on
├── src/ tests/             # Tests to verify the code is working properly
│
├── report/                 # Documents
│   ├── Resultat final.pdf  # Results (with screenshots,time comparisons, ...) 
│   └── project_assignment.pdf
│
├── LICENSE
└── README.md               # Project overview (you're reading it!)
```

---

## 🚀 Getting Started

To run the game:

```bash
python pygames.py
```

You can customize parameters such as grid size, pairing rules, and display settings.

---

## 🧠 Educational Objectives

This project was designed to work on different kinds of algorithms:
- Greedy algorithm
- Ford-Fulkerson (Maximum flow algorithm)
- Maximum Weight Matching (Matching algorithm in a graph)
- Minimax (Game theory algorithm : zero-sum game)

---

## 📌 Important Note

We can implement a more naive version of the Greedy algorithm with a double for loop!

---

## 👥 Authors

Developed by Ralph NADER & Maxime HEBERT — ENSAE 1A Programming Course.
