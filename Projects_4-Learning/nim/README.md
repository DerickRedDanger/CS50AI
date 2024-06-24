# Nim Project

## Problem Description
The full problem description is available at the following link: [CS50 AI Project 4 - Nim](https://cs50.harvard.edu/ai/2024/projects/4/nim/)

## Introduction

This project aims to create an AI capable of teaching itself to play Nim through reinforcement learning and to play Nim against a human player.

The AI plays against itself multiple times, initially making random moves until the end of a game, then adjusting its strategies by rewarding or punishing the moves based on the game outcome. Over time, it will prefer moves with higher values, which lead to wins more often, while still occasionally making random moves. Repeating this process many times allows the AI to learn the best moves for most (if not all) scenarios.

Once the training is complete, the terminal will return a game of Nim, allowing you to play against the trained AI.

## Utilization

1. Navigate to the `nim` directory:
   ```bash
   cd nim
   ```
2. Run the following command in the terminal:
   ```bash
   python play.py
   ```
3. Wait for the AI to finish training. It will print the number of the game it's training on until done.
4. Once training is complete, you can play a game of Nim against the trained AI.
5. To play the game, wait for your turn, then choose a pile to remove elements from and the count of elements you'd like to remove. The pile must be one of those shown and not empty, while the count can't be below 1 or higher than the number of elements in the chosen pile.
6. You can adjust the number of training games in `play.py` by editing the value within the `train()` function.
7. You can modify the piles by editing the `nim.py` file. Go to the `Nim` class and change the values inside its `__init__(self, initial=[1, 3, 5, 7])` method. Each number represents the number of elements in a pile. For example, to create 5 piles with 4 elements each, change it to `__init__(self, initial=[4, 4, 4, 4, 4])`.

## Background

In the game of Nim, players take turns removing any non-negative number of objects from any one non-empty pile. The player forced to remove the last object loses.

While simple strategies exist for single-pile scenarios, multi-pile strategies are more complex. This project builds an AI that learns Nim strategies through reinforcement learning. By playing against itself repeatedly and learning from experience, the AI will eventually learn which actions to take and which to avoid.

The project uses Q-learning, a reinforcement learning technique where we try to learn a reward value for every (state, action) pair. Actions leading to a win have a reward of 1, actions leading to a loss have a reward of -1, and actions that keep the game going have an immediate reward of 0, but include future rewards.

The key formula for Q-learning is:
```
Q(s, a) <- Q(s, a) + alpha * (new value estimate - old value estimate)
```
where `alpha` is the learning rate. The new value estimate represents the sum of the reward for the current action and the future rewards. The old value estimate is the existing value for `Q(s, a)`. By applying this formula each time the AI takes a new action, the AI learns the best actions for any state.

## Understanding

This project includes the files `play.py` and `nim.py`.

- `play.py` is responsible for determining the number of training games and initializing the game.
- `nim.py` contains the logic for the game and the AI. It includes two classes: `Nim` (the game) and `NimAI` (the AI), and two functions: `play` (plays the game, with an option for a human player) and `train` (trains the AI by making it play against itself).

In the `NimAI` class, there are several functions:
- `update`: Provided by CS50
- `get_q_value`, `update_q_value`, `best_future_reward`, `choose_action`, `get_all_actions`: Implemented by me

## Specification

### `get_q_value`
- Accepts a state and action as input and returns the corresponding Q-value.
- If the state/action pair doesn't have a Q-value, returns 0.

### `update_q_value`
- Takes a state, action, old Q-value, current reward, and future reward estimate. Updates the Q-value using the Q-learning formula.
- Formula:
  ```
  Q(s, a) <- old value estimate + alpha * (new value estimate - old value estimate)
  ```
- `Alpha` is set to 0.5.

### `best_future_reward`
- Accepts a state as input and returns the best possible reward among all available actions in that state, according to the Q-values.
- If an action isn't in the Q-values, assumes its value is 0.
- If no actions are available, returns 0.

### `choose_action`
- Accepts a state and an optional epsilon flag for using the epsilon-greedy algorithm. Returns either the highest-value action or a random action.
- If `epsilon` is `False`, behaves greedily, choosing the highest Q-value action.
- If `epsilon` is `True`, chooses a random action with probability `self.epsilon` (default 0.1) and the best action otherwise.
- If multiple actions have the same Q-value, one is chosen at random.

### `get_all_actions`
- Accepts a state as input and modifies the Q-values, adding any possible actions for the state and initializing them to 0.
- Utility function used in `choose_action` and `best_future_reward`.
```

Feel free to make any additional changes or let me know if there's anything else you'd like to include!