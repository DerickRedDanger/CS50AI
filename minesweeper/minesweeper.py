import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """

        raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # Removing mine cells from the sentence and
        # reducing it's count by 1 per cell removed
        if cell in self.cells:
            self.cells.discard(mine)
            self.count -= 1
        raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # Removing the safe cell from the sentence, if it's there
        if cell in self.cells:
            self.cells.discard(cell)
        
        #raise NotImplementedError


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    
    def quick_check(self,cells,counts):
        """
        # student made custom function made to improve the functions efficience by making 
        quick checks to a sentence that was just modified, thus reducing te number  
        of times the knowledge would loop throught all sentences to check them
        """

        # Removing safe cells from the sentence
        if len(self.safes) != 0:
            for safe in self.safes:
                if safe in cells:
                    cells.discard(safe)

        # Removing mine cells from the sentence and
        # reducing it's count by 1 per cell removed
        if len(self.mines) != 0:
            for mine in self.mines:
                if mine in cells:
                    cells.discard(mine)
                    counts -= 1

        # checking what new knowledge can be obtained from the actions above
                    
            # mark_safe and mark_mine will loop and modify the sentence list, 
            # doing that inside a loop that is reading the seentence could lead to error,
            # instead, it will be saved and the mark function will be called after the loops.
        mines_found = []
        safes_found = []

                
        # checking if the sentence only contains mines
        if len(cells) == counts:
            for mine in cells.copy():
                mines_found.append(mine)
                counts -= 1
                cells.discard(mine)

        # checking if sentences has only safe cells
        elif cells and counts == 0:
            for safe in cells.copy():
                safes_found.append(safe)
                cells.discard(safe)
        
        # if mines or safes were found, loop in them calling the mark function
        if mines_found:
            for mine in mines_found:
                self.mark_mine(mine)
        
        if safes_found:
            for safe in mines_found:
                self.mark_safe(safe)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # TODO
        """
        Marks the cell to the set of moves_made
        """
        self.moves_made.add(cell)

        """
        Marks the cell as safe
        """
        self.mark_safe(cell)

        """
        add a new sentence to the knowledge base
        """
        surrounding_cells=set()

        # get the surrounding cells
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignoring the cell itself
                if (i, j) == cell:
                    continue

                if 0 <= i < self.height and 0 <= j < self.width:
                    surrounding_cells.add((i,j))

        sentence = [surrounding_cells,count]

        # append the new sentence to the knowledge list
        self.knowledge.append(sentence)

        """
        Checking the knowledge for developments
        """
        # Removing safe cells from the sentences
        if len(self.safes) != 0 and len(self.knowledge) != 0:
            for safe in self.safes:
                for cells, counts in sentence:
                    if safe in cells:
                        cells.discard(safe)

        # Removing mine cells from the sentence and
        # reducing it's count by the number of cell removed
        if len(self.mines) != 0 and len(self.knowledge) != 0:
            for mine in self.mines:
                for cells, counts in sentence:
                    if mine in cells:
                        cells.discard(mine)
                        counts -= 1

        # checking what new knowledge can be obtained from the actions above
        if len(self.knowledge) != 0:
            # mark_safe and mark_mine will loop and modify the sentence list, 
            # doing that inside a loop that is reading the seentence could lead to error,
            # so intead, it will be saved and the mark function will be called after the loops.
            mines_found = []
            safes_found = []

            for cells,counts in sentence.copy():
                if not cells and counts == 0:
                    sentence.remove(cell,counts)

                #elif (not cells and counts != 0):
                #    raise NameError("Found a empty cells with count != 0")

                #elif (cells and counts < 0):
                #    raise NameError("Found a non empty cells with counts < 0")
                
                # checking for sentences that only contains mines
                elif len(cells) == counts:
                    for mine in cells.copy():
                        mines_found.append(mine)
                    sentence.remove(cell,counts)
                
                # checking for sentences that have cells but counts == 0
                elif cells and counts == 0:
                    for safe in cells.copy():
                        safes_found.append(safe)
                    sentence.remove(cell,counts)

                        
        


        



        raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        raise NotImplementedError
