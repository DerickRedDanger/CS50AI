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
        if self.cells and len(self.cells) == self.count:
            return self.cells
        else:
            return
            
        raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.cells and self.count == 0:
            return self.cells
        else:
            return
        
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
        self.ambiguous_intersection=[]

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
        function made to improve the functions efficience by making 
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
        mines_found = set()
        safes_found = set()

                
        # checking if the sentence only contains mines
        mine_check = sentence.know_mines()
        if mine_check:
            for mine in mine_check:
                mines_found.add(mine)
                counts -= 1
                cells.discard(mine)

        # checking if sentences has only safe cells
        safe_check = sentence.know_safe()
        if safe_check:
            for safe in safe_check:
                safes_found.add(safe)
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
            # if there is add the sentence to knowledge list
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
        
        The Mark function already checks the knowledge whenever
        a new safe or mine is found, so it's not nescessary to do it here
        
        instead, it will clean any empty knowledge, check for sentences made only of safe or mines
        and compare sets to find subsets checking what new knowledge can be obtained from the actions above
        """
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
            for sentence in self.knowledge.copy():
                cells = sentence[0]
                counts = sentence[1]

                # If this sentence is empty, remove it
                if not cells and counts == 0:
                    sentence.remove(sentence)
                
                # checking if this sentences only contains mines
                elif len(cells) == counts:
                    for mine in cells.copy():
                        mines_found.add(mine)
                    sentence.remove(sentence)
                
                # checking if this sentence only contains safe
                elif cells and counts == 0:
                    for safe in cells.copy():
                        safes_found.add(safe)
                    sentence.remove(sentence)
            
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
                the count of the second sentence from the first one.
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
                
                """
                Checking for intersection between sentences (cells they have in common), if one is found,
                check all other sentences and see if there are others with the same cells in common, saving them in a list.
                Then find all values possible for these cells to contain together (0 to n of cells)
                then remove this number of cells from the sentences(len(sentence[0]) - len(cell)) in the list and try removing 
                each of the possible values from the count of each sentence, looking for a impossibility 
                (having less cells then count or having count <0) each time one is found, discard that possibility and continue. 
                
                if only one possibility remains, this one is true, it's checked and added to knowledge. 
                If more then one is found, then it's ambiguous, save it in a set to be 
                explored again later when more information is avaliable.
                """
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
                                
                                inter_cell.update(in_common)
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

                                        # checking the conditions that would make this a valid value, 
                                        # but only triggering if they aren't a valid one (because of the Not and or)
                                        if not (difference_cell >= difference_count or difference_count >= 0):
                                            inter_values.remove(value)
                                            break
                                
                                # If there is only 1 possible value left, then this value is true. Check and add to knowledge.
                                if len(inter_values) == 1:
                                    new_sentence=[inter_cell,inter_values[0]]
                                    self.quick_check(new_sentence)
                                    if new_sentence[0] and new_sentence[1] >= 0:
                                        self.knowledge.append(new_sentence)

                                #---------------------------
                                # -------------- change this so the second ambiguous takes all values in a cell, not spread in many sentences----
                                # if there is more then 1 possible value, save them to be processed when more information is avaliable
                                else:
                                    for ambiguous_values in inter_values:
                                        self.ambiguous_intersection.append([inter_cell, ambiguous_values])
                            
            """
            Checking the intersections that returned ambiguous result, first trying to find other
            ambiguous intersections that are supersets of the first and checking the result. any that return a
            inequality is discarderd.

            If there are still more then one ambiguous intersection of a kind, compare it to the sentences that
            contain it and check for inequalities, Discarding any found.

            If only 1 sentence remains, that one is valid and should be checked then sent to sentences if
            there is still information after check.
            """
            # It's a bad idea to change a list/set while looping in it
            # So i will save the ones I want to discard and remove them later.
            ambiguous_to_discard=[]
            if self.ambiguous_intersection >= 2:
                for sentence1 in self.ambiguous_intersection:
                    if sentence1 not in ambiguous_to_discard:
                        ambiguous_to_explore=set()
                        ambiguous_to_explore.add(sentence1)
                        n_cell = len(sentence1[0])                    

                        for sentence2 in self.ambiguous_intersection:
                            if sentence1[0] == sentence2[0]:
                                ambiguous_to_explore.add(sentence2)

                        # creating a list with all possible values for a same cell
                        sentences_with_same_cell=[]

                        # creating a list of list with all possible values
                        superset_ambiguous=[]
                        
                        for sentence3 in self.ambiguous_intersection:
                            # if the sentence isn't already in the list of sentences to be explored and is a superset of them
                            if sentence3 not in ambiguous_to_explore and sentence3[0].issuperset(sentence1[0]):
                                # if the list is empty, add the first element that passes the if
                                if not sentences_with_same_cell:
                                    sentences_with_same_cell.append(sentence3)
                                # if it's not empty, add a element if it has the same cell as the one in the list
                                elif sentence3[0] == sentences_with_same_cell[0][0]:
                                    sentences_with_same_cell.append(sentence3)
                                # if it's not empty and is a different element, append the list to the one to be tested
                                # reset the list and start filling it again with this element.
                                else:
                                    superset_ambiguous.append(sentences_with_same_cell)
                                    sentences_with_same_cell=[]
                                    sentences_with_same_cell.append(sentence3)

                        # the for above won't append the last list, so if it exist, it's appended here
                        if sentences_with_same_cell:
                            superset_ambiguous.append(sentence3)
                        
                        if (superset_ambiguous):
                            for ambiguous in ambiguous_to_explore.copy():
                                
                                # Since we are working with possibilities, not certainties, the only way we can reject
                                # a value is if it's a impossibilities for all tests that have the same cells
                                for lists in superset_ambiguous:
                                    rejected = True
                                    for test in lists:
                                        difference_cell = len(test[0]) - n_cell
                                        difference_count = test[1] - ambiguous[1]
                                        # if it passes even one test, then we can't discard this value.
                                        if (difference_cell >= difference_count and difference_count >= 0):
                                            rejected=False
                                            break
                                    # if it fails all testes, then it can be discarded
                                    if rejected:
                                        ambiguous_to_discard.append(ambiguous)
                                        ambiguous_to_explore.discard(ambiguous)

                        if len(ambiguous_to_explore) >= 2:
                            superset_sentence=set()
                            for sentence in self.knowledge:
                                if sentence[0].issuperset(sentence1[0]):
                                    superset_sentence.add(sentence3)

                            if (superset_sentence):
                                for ambiguous in ambiguous_to_explore.copy():
                                    for test in superset_sentence:
                                        difference_cell = len(test[0]) - n_cell
                                        difference_count = test[1] - ambiguous[1]

                                        if not (difference_cell >= difference_count and difference_count >= 0):
                                            ambiguous_to_discard.append(ambiguous)
                                            ambiguous_to_explore.discard(ambiguous)
                                            break

                        if len(ambiguous_to_explore) == 1:
                            self.check(ambiguous_to_explore[0])
                            if ambiguous_to_explore[0][0] and ambiguous_to_explore[0][1] >= 0:
                                self.knowledge.append(new_sentence)

            if ambiguous_to_discard:
                for ambiguous in ambiguous_to_discard:
                    self.ambiguous_intersection.remove(ambiguous)


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
