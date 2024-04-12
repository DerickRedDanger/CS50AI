The problem and it's full description is avaliable in the link: 
https://cs50.harvard.edu/ai/2024/projects/1/minesweeper/

Obs: Given how long the original specification is and all the modifications, aditional variables and functions I made in this program. I did not write the original specifications(what each function should do) in this README, and instead wrote the specification for my complete program (what each function do). If'd you like to read the original specification, please check the link above.

## Introduction:

Minesweeper is a puzzle game that consists of a grid of cells, where some of the cells contain hidden “mines.” Clicking on a cell that contains a mine detonates the mine, and causes the user to lose the game. Clicking on a “safe” cell (i.e., a cell that does not contain a mine) reveals a number that indicates how many neighboring cells – where a neighbor is a cell that is one square to the left, right, up, down, or diagonal from the given cell – contain a mine.

My task is to create a Ai that is capable of playing Minesweeper.

The Ai will have access to the information a player usually has. That is, how many cells are in the board, their positions, all cells that were already clicked, if a cell they clicked was a mine or not, and the amount of mines in it's neighboring cells. One possible difference is that this Ai will not have access to the total amount of mines in a board. This was set by Cs50 since they didn't add that value to the Ai's arguments and they also set we shouldn't change the already present functions.

The Ai will have to use these informations to figure out which cells are safe and which are mine, marking the latter. As the Ai will have to make random or educated guesses at the start and some points during the game, it's not expected for it to win every time.

## Utilization:

* cd inside minesweeper folder.

* Run in the terminal: pip3 install -r requirements.txt (You only need to do this once.)

* run in the terminal: python runner.py

* Play minesweeper normaly or press AI move to let the AI make a move for you. (It can play the whole game, from start to finish, on it's own, but you need to keep pressing it to let it make it's move.)

## Understanding:

There are two main files in this project.

Runner.py was implemented by Cs50 and contains all the the code to run the graphical interface of the game.(It's possible to easily edit the size of the board and the number of mine by editing Runner.Py variables HEIGHT, WIDTH and MINE. Their standard value is 8.)

minesweeper.py contains all of the logic of the game itself and for the AI to play the game.

Inside minesweeper, there are three classes defined. Minesweeper, which handles the gameplay. Sentence, which represents a logical sentence containing both a set of cells and count. MinesweeperAi, which handles inferring which moves to make based on knowledge.

The Minesweeper class was fully implemented by Cs50, notice that each cell is a pair (i,j), where I is the row number and J is the column, each raging from 0 to width - 1.

The Sentence class was partially implemented by Cs50. Each Sentence has a set of cells and a count of how many of theses cells are mines. This class also contains the functions know_mines and know_safes for determining if any of the cells in a sentence are know to be mines or safe. it also contains functions mark_mines and mark_safe to update a sentence in response to new information.

MinesweeperAi class will implement an Ai that can play Minesweeper. The Ai class keep tracks of a number of values. Self.moves_made contains a set of all cells already clicked on. self.mines contain a set of all cells know to be mines. self.safes contains a set of all cells known to be safe. And self.knowledge contains a list of all sentences that the Ai know to be true.

## Specification:
The description and explanation of each class in minesweeper.py and it's functions.

### Minesweeper(height,width,mines):

Implemented by Cs50, contains the game's representation. the game's board with it's safe cells, mine cells, and the functions that show if a cell is a mine (is_mine(self.cell):), the count of how many neightboring cells are mines (nearby_mines(self,cell):), the variable that hold which cells were flagged as mines (self.mines_found) and a function that returns if all mines were flagged (won(self):)


### Sentence(cells,count):

Initialized by Cs50, while it's functions were made by me. Is the class of the logical statement used by the Ai. it's made of a set of cells and a count of how many mines are present in it. A description of it's functions:

* know_mines(self): return a set of all cells in a self.cells know to be mines. Else returns a empty set. Only works if the number of cells in a sentence is the same as the count, since this is the only way to guaranteed that there are only mines here.

* know_safe(self): works just like know mines, but returns a set of safe cells and only works when count == 0.

* mark_mines(self,cell): Check if Cell(mine) are present in self.cells. if it's, remove it from cells, reduce self.count by one and returns True. Return False if no modification was made(if cell isn't present in self.cell). This return is made to allow the program to know if a sentence was modified, so it can be checked.

* mark_safe(self,cell): works just like mark_mines, taking a cell, checking if it's in self.cell and removing if it's. returning true if was, false if not. only real difference is it doesn't affect the self.count.


### MinesweeperAI(height,width):

Has the following variables:

* self.height and self.width: takes the height and width of the game's board

* self.moves_made: A variable that holds a of all cell clicked.

* self.knowledge: Is a list that holds all sentences know to the Ai. this list increases when new sentences are found (throught making moves, or by the logic that explores and compares sentences) and removed when all cells are removed from a sentence ( All mines and safes in a sentence are found).

* self.checked_intersection: a set with all intersections already checked. made to avoid recursive creation of the same intersection. (better explained in the function check_knowledge(self))

* self.ambiguous_intersection: a list with all ambiguous intersections, in other words, a set of cell and a list of possible count for that set of cells. Theses are the intersections found in check_knowledge, but that still have ambiguous counts (and thus, not turned into a sentence and added to knowledge).

#### Mark_mine(cell):

Adds a cell to self.mine, then check all sentence in knowledge and runs sentence.mark_mine(cell), removing that mine from it's cell, if it was there.

It also removes that mine from all intersection in ambiguous_intersection. Then check the intersections that were modified to remove counts that became impossibilities. if only 1 count remains, creates a new sentence with theses cells and single count while deletes this intersection.

#### Mark_safe(cell):

Works just like Mark_mine, but with safe cells instead.

#### Quick_check(sentence):

Function made to check a sentence that was modified. calling self.safe and self.mines to remove all know minesa and safe. Then calling sentence.know_mines and sentence.know_safes to get all mines and safe present in this sentence. then calling self.mark_mines and self.mark_safe on these mines and safe to add them to self.know_mine and self.know_safe. If the sentence was in self.knowledge and no longer has cells (all were removed through know_mine and know_safe), remove it from there.

#### add_knowledge(cell,count):

Called after Minesweeper.board return to us the count and neighboring cells of a move. This function add the move to self.moves_made and mark that cell as safe (if it was a mine, it wouldn't trigger this function), it also find the cells neighboring that move, creating a new sentence with the cells and count. Checking that sentence, cleaning it of all know mines and cell, checking if new safe/mines can be found from it and,if there are still cells in it after that, adds it to knowledge.

This function then call the check_knowledge function to check the knowledge for new information. Recursively calling Check_knowledge again and again utill it returns false(utill it can no longer find new information).

#### check_knowledge():

Checks the knowledge for developtments, recursively. This is done by two different means, first by comparing the cells of each sentence against each trying to find a superset (when one sentence has all the cells of the other sentence in it), If it find it, it will remove the cells from the subset from the superset and reduce it's count by the value of the Sub's count. Effectively reducing the subset sentence from the superset.

As an example, let's take the following sentences:
    [{(0,1),(0,2),(0,3),(1,1)},2]
    [{(0,3),(1,1)},1]

    the first sentence is a superset of the second, so we reduce the second from the first, creating the third sentence below:
    [{(0,1),(0,2)},1]

The superset sentence is them marked to be removed at the end of check_knowledge (since it's possible that this sentence is the superset of yet another sentece), while the new sentence goes throught quick_check() and, if not empty, added to knowledge.

The second method is to check for intersections, which is done by calling the function Checking_intersections() that is expalined below.

After running checking_intersections, it will remove all superset to avoid the recursive creation of repetitive new sentences, while also removing all sentences with empty cells from knowledge.

If any new sentence was created of checking_intersection return true, this sente will return true, causing add_knowledge() to call this sentence again to check for further developtments

#### Checking_intersections():

This function check knowledge's sentences for intersections (cells in common between two or more sentences, but only does this if they have 2 or more cells in common), while also saving a set of theses cells to ensure it will not repeately recreate it.

Then find the maximal and minimal count these cells could have (since each cell can be either a mine or a safe, it means the minimun and maximun value 0 and Nº cells), then test theses values in their original sentence by reducing the number of cell they contained and reducing their counts by the theorical values. An example of this is showed below

Let's consider that our knowledge have the following two sentences:
    [{(1,2),(2,3),(4,5)},2]
    [{(1,2),(4,5),(4,7)},1]
They have two cells in common, so their theorical count would be 0,1 and 2.
    [{(1,2),(4,5)},[0,1,2]]
Removing them from original sentence, would give us:
    [{(2,3)},2]
    [{(4,7)},1]
for theses sentences to be true, their count need to be either 0 or 1. so removing the theorical counts form them, in order, we'd get:
    [{(2,3)},[2*,1,0]]
    [{(4,7)},[1,0,-1*]]
The values with a * means they are impossible for that situation. And since the cells we got belong to both sentences at same time, they also need to satisfy both sentences at once. from that we can find out that the cells {(1,2),(4,5)} must have a count of 1. This would lead us to the following results.
    [{(2,3)},1]
    [{(4,7)},0]
    [{(1,2),(4,5)},1]
This allows us to know that the cell(2,3) is a mine, cell (4,7) is safe and that there is a mine in either cell (1,2) or (4,5).

the original sentences are then quick_checked and cleaned, while the third new sentence is also quick_checked and, if it still have cells after it, added to self.knowledge.

However, there are cases where our intersections still have 2 or more possible values. On theses cases, they are saved in the list self.ambiguous_intersection. The mark_mine/safe is called also affect theses functions, removing cells and reducing the count(when removing mines). If a intersection is modified they will go throught the quick_check_ambiguous function (described below, works similar to quick_check, but for intersections) then checked for impossibility ( 0> count or count> n° cells), deleting them. If only one possibility remains, this intersection is now true and is added to sentence, however if only 1 cell remains while this sentence has more then 1 possible count, this intersection is discarded (since we already know that every cell is either safe or mine)

If any intersection is created, whether it becomes a new sentence or an ambiguous intersection, this function will return True, else it will return false.

#### quick_check_ambiguous(ambiguous):

Checks if a ambiguous intersection's counts are still valid, removing the invalid ones ( 0> count or count> n° cells). If only one count remains, a sentence is created with this ambiguous and quick checked, while this ambiguous is deleted.

If only one cell remains, but more then one count, then this ambiguous will be deleted (since we already know that each cell can be either a mine or safe)

If more then one cell and count remains, then nothing happens to this ambiguous.

#### make_safe_move():
Returns a safe cell that is not a move that was already made, if no safe move is know, returns None. Didn't find a reason to make this refined or complicated. Meanwhile picking the right cells might make the game a bit faster, we often end up exploring all safe options before making a riskier move, so it shouldn't make a big difference in the end.

#### Make_random_move():
Is only called when it's impossible to make a safe move. Should return a random cell from those that weren't choose already, nor those that are know to be mines. But instead, I made it return a educated guess.

It check all sentences in self.knowledge and ambiguous in self.ambiguous_intersection, getting each cell, putting them in a dictionary and finding both their highest chance of being a mine and their value (how much information we'd be able to get should we know this cells value, based on all sentences and ambiguous).

After that we'd check which cells have the lowest odd of being a mine. If there is only one cell, that would be our safest_cell, if there is more then one, then we'd save them in a list and pick the one with the highest value as our most_valuable_cell. If our most_valuable_cell chance of being a mine is 33% or lower, this will be our "random move". If we only have one safest_cell and it's chance of being a mine is 33% or lower, then this will be our move. But if the lowest chance of being a mine is 34% or higher, then we will instead make a random choice of the cells that aren't safe, mine nor in any sentence/ambigous, since the chance of that random unknow cell being a mine is (likely) lower then 33%. If there isn't any unknow cells (all are already in safe or mines or in sentence/ambiguous), then it will pick the most valuable cell, else the safested one. Since Our Ai doesn't have access to total number of mines in a board, I didn't find it possible to refine this percentage further.

