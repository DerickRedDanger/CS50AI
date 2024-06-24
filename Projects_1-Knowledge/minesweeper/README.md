# Minesweeper AI Project

The full problem description is available [CS50 AI Project 2: MineSweeper](https://cs50.harvard.edu/ai/2024/projects/1/minesweeper/).

## Introduction

Minesweeper is a puzzle game where players reveal cells on a grid, avoiding hidden mines. Clicking a mine ends the game, while safe cells show the number of adjacent mines. The goal is to create an AI capable of playing Minesweeper using the same information available to human players. The AI does not know the total number of mines on the board, as per CS50's constraints.

## Utilization

1. **Navigate to the Minesweeper folder:**
   ```bash
   cd minesweeper
   ```

2. **Install dependencies (only needed once):**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Run the game:**
   ```bash
   python runner.py
   ```

4. **Gameplay:**
   - Play Minesweeper manually or press "AI move" to let the AI make a move. Continue pressing "AI move" to let the AI play the entire game.

## Understanding

### Files

- **runner.py:** Provided by CS50, contains code for the game's graphical interface. Adjust board size and number of mines via `HEIGHT`, `WIDTH`, and `MINE` variables.
- **minesweeper.py:** Contains game logic and AI implementation.

### Classes

1. **Minesweeper:** Handles gameplay logic.
2. **Sentence:** Represents logical sentences with sets of cells and a count of mines.
3. **MinesweeperAI:** Implements the AI for playing Minesweeper.

### Minesweeper Class

Implemented by CS50, this class manages the game board, mines, and gameplay functions.

### Sentence Class

Partially implemented by CS50, this class handles logical sentences used by the AI.

#### Functions:

- **know_mines(self):** Returns a set of cells known to be mines if the count equals the number of cells.
- **know_safe(self):** Returns a set of cells known to be safe if the count is zero.
- **mark_mine(self, cell):** Marks a cell as a mine and updates the sentence.
- **mark_safe(self, cell):** Marks a cell as safe and updates the sentence.

### MinesweeperAI Class

This class implements the AI logic and tracks the game's state, moves made, known mines, known safes, and knowledge base.

#### Key Functions:

- **mark_mine(self, cell):** Marks a cell as a mine and updates sentences and intersections.
- **mark_safe(self, cell):** Marks a cell as safe and updates sentences and intersections.
- **quick_check(self, sentence):** Updates knowledge base with known mines and safes.
- **add_knowledge(self, cell, count):** Adds a new sentence based on a move and updates knowledge recursively.
- **check_knowledge(self):** Recursively checks for new information from the knowledge base.
- **checking_intersections(self):** Finds and processes intersections between sentences.
- **quick_check_ambiguous(self, ambiguous):** Updates ambiguous intersections.
- **make_safe_move(self):** Returns a known safe cell for the next move.
- **make_random_move(self):** Returns an educated guess for the next move based on probability.

## AI Logic

The AI utilizes logical inferences from known cells and counts to mark mines and safes, make moves, and update its knowledge base. It handles ambiguities and intersections to refine its decisions and improve its success rate.
```

Feel free to make any additional changes or let me know if there's anything else you'd like to include!