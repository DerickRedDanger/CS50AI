# Read me

The problem and it's full description is avaliable in the link: 
https://cs50.harvard.edu/ai/2024/projects/4/nim/

## Introduction:

This project aims at creating an Ai capable of teaching itself to play Nim through reinforcement training and of playing Nim against a human player.

This is done by making the Ai play against itself N times, initially picking random moves till the end of a game, then adding values (rewarding or punishing) the moves it made that led to that result. Overtime it will start to prefer movements that have higher values, since these led to wins more often, while still taking random movements with a small chance. Repeating this a large amount of time would lead the Ai to know which movement is the best option for most (if not all) scenarios.

Once the training is done, the terminal will return a game of Nim, allowing you to play against the trained Ai.

## Utilization:

* cd inside nim

* Run in the terminal: python play.py

* Wait for the Ai to finish training, it will keep printing the number of the game it's training till done.

* Once it finishes training, it will let you play a game of Nim against the trained Ai

* To play the game, wait for your turn, then choose a Pile to remove elements from and the count of elements you'd like to remove. The pile must be one of those showed and not empty, while the count can't be a value below 1 nor higher than the number of elements in the chosen pile.

* You can edit the number of times the Ai will train with itself in play.py by editing the value within train().

* You can edit the piles by going inside nim.py, go to the class Nim() and change the values inside its def __init__(self, initial=[1, 3, 5, 7]). Each number represents the number of elements in a pile, so if you wanted 5 piles with 4 elements each, you'd change it to def __init__(self, initial=[4, 4, 4, 4, 4])

## Background:

In the game Nim, we begin with some number of piles, each with some number of objects. Players take turns: on a player’s turn, the player removes any non-negative number of objects from anyone non-empty pile. Whoever removes the last object loses.

There’s some simple strategy you might imagine for this game: if there’s only one pile and three objects left in it, and it’s your turn, your best bet is to remove two of those objects, leaving your opponent with the third and final object to remove. But if there are more piles, the strategy gets considerably more complicated. In this problem, we built an AI to learn the strategy for this game through reinforcement learning. By playing against itself repeatedly and learning from experience, eventually our AI will learn which actions to take and which actions to avoid.

In particular, we’ll use Q-learning for this project. In Q-learning, we try to learn a reward value (a number) for every (state, action) pair. An action that loses the game will have a reward of -1, an action that results in the other player losing the game will have a reward of 1, and an action that results in the game continuing has an immediate reward of 0, but will also have some future reward.

The key formula for Q-learning is below. Every time we are in a state s and take an action a, we can update the Q-value Q(s, a) according to:

Q(s, a) <- Q(s, a) + alpha * (new value estimate - old value estimate)

In the above formula, alpha is the learning rate (how much we value new information compared to information we already have). The new value estimate represents the sum of the reward received for the current action and the estimate of all the future rewards that the player will receive. The old value estimate is just the existing value for Q(s, a). By applying this formula every time our AI takes a new action, over time our AI will start to learn which actions are better in any state.

How will we represent the states and actions inside a Python program? A “state” of the Nim game is just the current size of all the piles. An “action” in the Nim game will be a pair of integers (i, j), representing the action of taking j objects from pile i. So the action (3, 5) represents the action “from pile 3, take away 5 objects.” Applying that action to the state [1, 1, 3, 5] would result in the new state [1, 1, 3, 0] (the same state, but with pile 3 now empty).

## Understanding:

This project is composed of the files play.py and nim.py, the file responsible for selecting the number of times the Ai should train with itself and initializes the game.

nim.py contains all of this project's logic. It contains two classes, Nim (the game itself) and NimAi(the Ai for the game). And two function, Play (function made to play the game, can take as argument if there is a human player or not), and Train (Function that makes the Ai play against itself N times). Nim, Play and Train were implemented by Cs50, NimAi was initialized by Cs50, but it's full implementation was left to me.

In the class NimAi there are the functions Update, get_q_value, update_q_value, best_future_reward, choose_action, get_all_actions.

Update was implemented by Cs50, but all the others were implemented by me, get_all_actions was made by me to get all actions available, since it was necessary in both best_future_reward and Choose_action.

## Specification:

### get_q_value:
* Accepts as input a state and action, while returning the corresponding Q-value for that state/action pair.

* If that pair doesn't have a Q-value (wasn't explored or added to the self.q yet), returns 0

### update_q_value:
* takes a state, action and old_q (a existing Q-value), a current reward and estimate a future rewards, updating the Q-value for the state/action pair according to the Q-learning formula.

* the formula is the following:

    Q(s, a) <- old value estimate
                   + alpha * (new value estimate - old value estimate)

* Alpha is the learning rate associated to the NimAi object. Here, Alpha was set to 0.5.

### best_future_reward:

* Accepts a state input and returns the best possible reward among all available actions in that state, according to the Q-values in self.q

* For any action that isn't already in self.q, its value is assumed to be 0

* If not actions are available in this state, returns 0

### choose_action:

* accepts a state and (and optionally an epsilon flag for whether to use the epsilon-greedy algorithm), and return either the action with the highest value or a random one.

* if epsilon is false, the function will behave greedily, not exploring options and going for the one with the highest Q-value.

* if epsilon is true, it will behave according to the epsilon-greedy algorithm, choosing a random available option with a probability self.epsilon (default to 0.1) and otherwise choosing the best action available.

* If multiple actions have the same Q-value, it's chosen at random.

### get_all_action:

* Accepts a state as input and modifies self.q, adding any possible action for this state that wasn't there and initializing it to the value 0. It doesn't modify the actions that are already there.

* This is a utility function made to be used on both choose_action and best_future_reward