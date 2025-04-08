# 🧩 Grid Game Project

This repository contains a Python-based, object-oriented grid game developed as part of an ENSAE 1A programming assignment. The project explores fundamental programming concepts through a playable game that features several game modes and different ways of solving the grid.

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
1. The game starts with a grid and a set of players.
2. Each player takes turns making a move based on the game rules.
3. The game continues until an end condition is met (e.g., maximum rounds, victory condition, etc.).

### Players
- Players can be controlled by the user or act autonomously.
- Each player has a position and possibly a strategy.

### Grid
- The grid is a 2D structure that holds player positions and other objects (if any).
- It handles boundaries, player interactions, and visual representation.

---

## 📁 Repository Structure

```
project_root/
│
├── src/                    # Python code
│   ├── main.py             # Entry point to launch the algorithms 
│   ├── grid.py             # Grid management (creation, display, updates)
│   ├── solver.py           # Implements all solvers (including the ones for new rules/game modes)
│   └── pygames.py          # Game interface (3 modes)
│
├── report/                 # Documents
│   ├── Resultat final.pdf  # Results
│   └── project_assignment.pdf
│
├── requirements.txt        # Python dependencies (if any)
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

This project was designed to work on diferent kind of algorithms:
- Greedy algorithm
- Ford-Fulkerson (Maximum flow algorithm)
- Maximum Weight Matching (Matching algorithm in a graph)
- Minimax (Game theory algorithm : zero-sum game)

---

## 📌 Important Note

We can implement a more naive version of the Greedy algorithm with a double for loop!

---

## 👥 Authors

Developed by Ralph NADER & Maxime Hebert — ENSAE 1A Programming Course.
