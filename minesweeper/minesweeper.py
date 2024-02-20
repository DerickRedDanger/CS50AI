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
            self.cells.discard(cell)
            self.count -= 1
        
        #raise NotImplementedError

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

        # List of all cells in knowledge that are not know to be mines or safe
        self.Backtracking_options=set()

        # set of all checked intersection that were processed in add_knowledge
        self.checked_intersection=set()

        # list of all checked intersection that still were ambiguous after processed in add_knowledge
        self.ambiguous_intersection=set()

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        self.Backtracking_options.discard(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        self.Backtracking_options.discard(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    
    def quick_check(self,sentence):
        """
        - student made custom function made to improve the functions efficience by making 
        quick checks to a sentence that was just modified, thus reducing te number  
        of times the knowledge would loop throught all sentences to check them
        """
        cells = sentence[0]
        counts = sentence[1]

        # Removing safe cells from the sentence
        if len(self.safes) != 0:
            for safe in self.safes:
                sentence.mark_safe(safe)

        # Removing mine cells from the sentence and
        # reducing it's count by 1 per cell removed
        if len(self.mines) != 0:
            for mine in self.mines:
                sentence.mark_mine(mine)
                    
        # Ai's mark_safe and mark_mine will loop and modify the sentence list, 
        # doing that inside a loop that is reading the sentence could lead to error,
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
        # checking self.knowledge and removing any of the mines/safe found
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

        # cleaning sentence of know safe/mines and checking
        # if new safe/mines could be found after it
        self.quick_check(sentence)

        # check if the sentence still have cells after the cleaning
        if sentence[0] and sentence[1] >= 0:
            # if there is, append it's cells to Backtracking_options
            for cell in sentence[0]:
                self.Backtracking_options.add(cell)
            # and the sentence to knowledge list
            self.knowledge.append(sentence)
        
        # if sentence don't have cells and counts == 0, 
        # then it's empty and was fully processed
            
        # But if it's count is < 0, it having cells or not, an error happened
        elif sentence[1] <= -1:
            raise NameError(f"""Error - Count == {sentence[1]}. happened at cell = {cell} with count = {count}"
                            With mines = {self.mines}, safe = {self.safes} 
                            and knowledge = {self.knowledge}""")

        """
        Checking the knowledge for developments
        """

        # add the check_knowledge funtion to below after creating it
        # ----
        # check_knowledge(self.knowledge)
        # ----

        # The Mark function already checks the knowledge whenever
        # a new safe or mine is found, so it's not nescessary to do it here
        
        # instead, we will clean any empty knowledge and compare sets to find subsets
        # checking what new knowledge can be obtained from the actions above
        if len(self.knowledge) != 0:
            # mark_safe and mark_mine will loop and modify the sentence list, 
            # doing that inside a loop that is reading the seentence could lead to error,
            # so intead, it will be saved and the mark function will be called after the loops.
            mines_found = set()
            safes_found = set()

            """
            Cleaning knowledge of sentences that are empty, contain only safe or mines
            and adding them to to the list.
            """
            for cells,counts in sentence.copy():

                # If this sentence is empty, remove it
                if not cells and counts == 0:
                    sentence.remove(cell,counts)
                
                # checking if this sentences only contains mines
                elif len(cells) == counts:
                    for mine in cells.copy():
                        mines_found.add(mine)
                    sentence.remove(cell,counts)
                
                # checking if this sentence only contains safe
                elif cells and counts == 0:
                    for safe in cells.copy():
                        safes_found.add(safe)
                    sentence.remove(cell,counts)
            
            if mines_found:
                for mine in mines_found:
                    self.mark_mine(mine)

            if safes_found:
                for safe in safes_found:
                    self.mark_safe(safe)

            # saving the sentences that were modified so they can be checked after the loop
            sentences_to_check={}

            if len(self.knowledge) >= 2:
                """
                # checking for sentences whose cells contains all of another sentence's cell
                if they exist, then remove theses same cells from sentence 1 and reduce
                the count from the second sentence from the first one.
                effectively subtracting sentence 2 from sentence 1.
                """
                for sentence in self.knowledge.copy():
                    cell = sentence[0]
                    count = sentence[1]
                    for sentence2 in self.knowledge.copy():
                        cell2 = sentence2[0]

                        if cell.issuperset(cell2):
                            count2=sentence2[1]
                            cell.difference_update(cell2)
                            count = count - count2
                            sentences_to_check.add(sentence)
                
                for sentence1 in self.knowledge.copy():
                    cell = sentence1[0]
                    count = sentence1[1]

                    
                    inter_found=True

                    while inter_found:
                        inter_found=False
                        for sentence2 in self.knowledge.copy():
                            cell2 = sentence2[0]
                            if sentence2 == sentence1:
                                continue

                            in_common = cell.intersection(cell2)
                            if in_common and in_common not in self.checked_intersection:
                                inter_found=True
                                self.checked_intersection.add(frozenset(in_common))
                                sentences_with_inter=[sentence1,sentence2]
                                intersection =[set(),set()]
                                inter_cell = intersection[0]
                                inter_values = intersection[1]
                                
                                inter_cell.add(in_common)
                                n_cell=len(inter_cell)
                                for i in range(0,n_cell+1):
                                    inter_values.add(i)

                                for sentence3 in self.knowledge:
                                    if sentence3 not in sentences_with_inter and sentence3[0].issuperset(inter_cell):
                                        sentences_with_inter.append(sentence3)

                                for value in inter_values.copy():
                                    for sentence in sentences_with_inter:

                                        difference_cell = len(sentence[0])-n_cell
                                        difference_count = sentence[1] - value


                                    if not (difference_cell >= difference_count and difference_count >= 0):
                                        inter_values.remove(value)
                                        break
                                
                                if len(inter_values) == 1:
                                    new_sentence=[inter_cell,inter_values[0]]
                                    self.quick_check(new_sentence)
                                    if new_sentence[0] and new_sentence[1] >= 0:
                                        self.knowledge.append(new_sentence)
                                else:
                                    for ambiguous_values in inter_values:
                                        self.ambiguous_intersection.append([inter_cell, ambiguous_values])
                            # still have to write a program to process self.ambiguous_intersection
        


        



        raise NotImplementedError
    
    def check_knowledge(self,knowledge):
        """
        - User implemented function to check a knowledge base. Made separated from
        add knowledge so it could be reutilized in Backtracking_technique
        """

        if len(knowledge) != 0:
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
    
    def Backtracking_technique(self):
        """
        - User implemented function that checks the avaliable knowledge and
        try to assign values to a cell in there and check if it properly
        satisfy all sentences that it's part of. If it does, this value is assumed as
        correct and changes are made in the knowledge. Else it's discarded and another
        cell is tried. 

        Considering this would lead to recursion and could take a considerable amount
        of time, this function will only be called if no safe_move is avaliable.
        """

        for test in self.Backtracking_options.copy():
            contained = set()
            for sentence in self.knowledge:
                cell = sentence[0]
                count = sentence[1]
                if test in cell:
                    contained.add(sentence)


        raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        raise NotImplementedError
