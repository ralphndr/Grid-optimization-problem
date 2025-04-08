# 🧩 Grid Game Project – ENSAE 1A Python Assignment

This repository contains a Python-based, object-oriented grid game developed as part of an ENSAE 1A programming assignment. The project explores fundamental programming concepts through a playable game that runs in the terminal and features autonomous players, game state management, and user interaction.

---

## 🎮 Game Overview

The game is played on a **grid of configurable size**, where several **players** (real or virtual) move across the cells according to specific rules. Players may encounter objects or events on the grid, and the goal of the game varies depending on the game mode chosen.

**Key Features:**
- Customizable grid size and number of players.
- Turn-based movement system.
- Object-oriented design with modular architecture.
- Expandable rules and game logic (e.g., obstacles, scoring systems, etc.).

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
├── game/                   # Main game logic
│   ├── grid.py             # Grid management (creation, display, updates)
│   ├── player.py           # Player class and movement logic
│   ├── game.py             # Game controller and main loop
│
├── utils/                  # Helper functions and modules
│   └── config.py           # Game parameters and constants
│
├── main.py                 # Entry point to launch the game
├── requirements.txt        # Python dependencies (if any)
└── README.md               # Project overview (you're reading it!)
```

---

## 🚀 Getting Started

To run the game:

```bash
python main.py
```

You can customize parameters such as grid size, number of players, and turn limit by editing `config.py`.

---

## 🧠 Educational Objectives

This project was designed to:
- Practice object-oriented programming in Python.
- Learn to structure a modular project with multiple files and responsibilities.
- Develop algorithmic thinking through game mechanics.

---

## 📌 Notes

- This is a command-line game — no GUI is included.
- The project is structured to be easily expandable (e.g., adding items, AI logic, different win conditions).

---

## 👥 Authors

Developed by [Your Name], [Your Teammates' Names] — ENSAE 1A Programming Course.
