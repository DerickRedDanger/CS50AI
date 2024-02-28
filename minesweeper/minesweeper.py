import itertools
import random
from termcolor import colored


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
            print(f"know_mines = {self.cells}")
            return self.cells
        else:
            return set()
            
        raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.cells and self.count == 0:
            print(f"know_safes = {self.cells}")
            return self.cells
        else:
            return set()
        
        raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # Removing mine cells from the sentence and
        # reducing it's count by 1 per cell removed
        if cell in self.cells.copy():
            #print(f"Sentence.mark_mine - self = {self}")
            self.cells.discard(cell)
            self.count -= 1
            return True
            #print(f"Sentence.mark_mine - new self = {self}")
        return False
        
        #raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # Removing the safe cell from the sentence, if it's there
        if cell in self.cells.copy():
            self.cells.discard(cell)
            return True
        return False
        
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

        # List of all cells in knowledge that are not known to be mines or safe
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
        #print (f"mine = {cell}")
        self.mines.add(cell)
        #print(f"mines = {self.mines}")
        if self.knowledge:
            for sentence in self.knowledge:
                if sentence.mark_mine(cell):
                    self.quick_check(sentence)

        if self.ambiguous_intersection:
            for sentence in self.ambiguous_intersection:
                print(colored(f"Ai_mark_mine_ambiguous - sentence = {sentence}"))
                if cell in sentence[0]:
                    changes=False
                    sentence[0].remove(cell)
                    #print(f"sentence[1] = {sentence[1]}")
                    index_to_delete=[]
                    for i in range (len(sentence[1])):
                        sentence[1][i] -=1
                        #print(f"sentence[1] = {sentence[1]}")
                        #print(f"count ={count}")
                        if len(sentence[0]) < sentence[1][i] or sentence[1][i] < 0:
                            index_to_delete.append(i)
                            changes=True
                    for i in reversed(index_to_delete):
                        sentence[1].pop(i)
                    if changes:
                        print(colored(f"Ai_mark_mine_ambiguous - changed - sentence = {sentence}"))
                        self.quick_check_ambiguous(sentence)
                    
        

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        if self.knowledge:
            for sentence in self.knowledge:
                if sentence.mark_safe(cell):
                    self.quick_check(sentence)

        if self.ambiguous_intersection:
            for sentence in self.ambiguous_intersection:
                changes = False
                if cell in sentence[0]:
                    sentence[0].remove(cell)
                    changes = True
                if changes:
                    self.quick_check_ambiguous(sentence)
    
    def quick_check(self,sentence):
        """
        function made to improve the functions efficience by making 
        quick checks to a sentence that was just modified, thus reducing te number  
        of times the knowledge would loop throught all sentences to check them
        """
        
        pointer_for_deletion=None

        # check if this sentence is in the knowledge already, if it's save it's value
        # so that i can be deleted in case it's emptied by the end of the check
        if sentence in self.knowledge:
            pointer_for_deletion = id(sentence)         

        # Removing safe cells from the sentence
        if len(self.safes) != 0:
            for safe in self.safes:
                #print (f"safe = {safe}")
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

        print(colored(f"sentence about to check {sentence}",'yellow'))
        # checking if the sentence only contains mines
        mine_check = sentence.known_mines()
        if mine_check:
            for mine in mine_check.copy():
                mines_found.add(mine)
                sentence.count -= 1
                sentence.cells.discard(mine)
            print(colored(f"sentence after mine_check = {sentence}",'yellow'))

        # checking if sentences has only safe cells
        safe_check = sentence.known_safes()
        if safe_check:
            for safe in safe_check.copy():
                safes_found.add(safe)
                sentence.cells.discard(safe)
            print(colored(f"sentence after safe_check = {sentence}",'yellow'))
        
        # if mines or safes were found, loop in them calling the mark function
        # checking self.knowledge and removing any of the mines/safe found
        #print(f"mines found ={mines_found}")
        if mines_found:
            print(colored(f" quick_check - Mines found = {mines_found}",'cyan'))
            for mine in mines_found:
                self.mark_mine(mine)
        #print(f"Mines now = {self.mines}")

        #print(f"safes found ={safes_found}")
        if safes_found:
            print(colored(f"quick_check - Safes found = {safes_found}",'green'))
            for safe in safes_found:
                self.mark_safe(safe)
        #print(f"safes now = {self.safes}")

        # check if the sentence not longer have cells and is part of the knowledge
        # if it's empty and part of knowledge, remove it from there
        print(f"sentence = {sentence}")
        #print(f"pointer_for_deletion = {pointer_for_deletion}")
        if not sentence.cells and pointer_for_deletion:
            for orignal_sentence in self.knowledge:
                if id(orignal_sentence) == pointer_for_deletion:
                    print(f"Modified sentence = {sentence}")
                    print(f"original sentence = {orignal_sentence}")
                    self.knowledge.remove(orignal_sentence)
                    break  # break after removing the item to avoid modifying the list during iteration

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
        print(colored(f"Cell clicked = {cell}, counts = {count}" ,'green'))

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

        sentence = Sentence(surrounding_cells,count)
        original_sentence = Sentence(surrounding_cells,count)
        # cleaning sentence of known safe/mines and checking
        # if new safe/mines could be found after it
        print(f"sentence in add moviment - before quick check = {sentence}")
        print(f"safe before the quick check = {self.safes}")
        print(f"mines before the quick check = {self.mines}")
        self.quick_check(sentence)
        print(f"sentence in add moviment - after quick check = {sentence}")
        print(f"safe after the quick check = {self.safes}")
        print(f"mines after the quick check = {self.mines}")

        # check if the sentence still have cells after the cleaning
        if sentence.cells and sentence.count >= 0:
            # if there is add the sentence to knowledge list
            self.knowledge.append(sentence)
        
        # if sentence don't have cells and counts == 0, 
        # then it's empty and was fully processed
            
        # But if it's count is < 0, it having cells or not, an error happened
        elif (not sentence.cells and sentence.count != 0) or sentence.count <= -1:
            raise NameError(f"""Error - Count == {sentence.count}. happened at sentence ={sentence}"
                            Original sentence = {original_sentence}
                            With mines = {self.mines}, safe = {self.safes} 
                            and knowledge = {self.knowledge}""")

        # keep checking knowledge till no new knowledge is found before making a move
        if len(self.knowledge) != 0:

            # N for debugging
            N = 0

            new_knowledge = True
            while new_knowledge:
                N += 1
                new_knowledge = self.check_knowledge()
                print(f"This is the {N}° time knowledge is checked")
        print(f"safes = {self.safes}, mines = {self.mines}")

        #print("knowledge = {", end=" ")
        #for sentence in self.knowledge:
        #    print(sentence,end= " ")
        #print("}", end="")
        #print('')
        
        
            
            
    def check_knowledge(self):
        """
        Checking the knowledge for developments
        
        The Mark function already checks the knowledge whenever
        a new safe or mine is found, so it's not nescessary to do it here
        
        instead, it will compare sets to find subsets checking what new knowledge
        can be obtained from the actions above, be it new sentences or checking ambiguous hypotheses
        
        If any new_knowledge is found, return true, else, return false.
        """
        new_knowledge=False

        # saving the sentences that were modified so they can be checked after the loop
        sentences_to_check=[]

        if len(self.knowledge) >= 2:
            """
            # checking for sentences whose cells contains all of another sentence's cell
            if they exist, then remove theses same cells from sentence 1 and reduce
            the count of the second sentence from the first one.

            effectively subtracting sentence 2 from sentence 1.
            """
            sentences_to_remove=[]

            print("knowledge = {", end=" ")
            for sentence in self.knowledge:
                print(sentence,end= " ")
            print("}", end="")
            print('')

            for sentence in self.knowledge.copy():
                if not sentence.cells:
                    continue

                for sentence2 in self.knowledge:

                    if sentence.cells.issuperset(sentence2.cells) and sentence.cells != sentence2.cells and sentence2.cells:
                        new_sentence_cells=set()
                        new_sentence_count=0

                        print(f"{sentence.cells} is superset {sentence2.cells}")
                        # to keep this function from creating multiple sentences by creating a subset 
                        # while still having it's original superset, it's superset will be saved and, after fully
                        # processing knowledge to reduce the loss of information, removed
                        sentences_to_remove.append(id(sentence))

                        print(colored(f"cell {sentence.cells} - cell 2 {sentence2.cells}", 'yellow'))
                        new_sentence_cells = sentence.cells.difference(sentence2.cells)
                        print(colored(f" = cell {new_sentence_cells}", 'yellow'))
                        print(colored(f"count1 = {sentence.count} - count2 = {sentence2.count}", 'yellow'))
                        new_sentence_count = sentence.count - sentence2.count
                        print(colored(f" = {new_sentence_count}", 'yellow'))
                        new_sentence=Sentence(new_sentence_cells,new_sentence_count)
                        print(colored(f" sentence to check = {new_sentence}", 'red'))
                        sentences_to_check.append(new_sentence)
                        new_knowledge=True
                        

            if sentences_to_check:
                for sentence in sentences_to_check:
                    print(colored(f" sentence before the check = {sentence}", 'blue'))
                    self.quick_check(sentence)
                    print(colored(f" sentence after the check = {sentence}", 'blue'))
                    if sentence.cells:
                        print(colored(f" sentence appended to knowledge = {sentence}", 'red'))
                        self.knowledge.append(sentence)
                        print(colored("knowledge after append",'yellow'))
                        
            
            checking_intersections=self.checking_intersections()
            ambiguous_intersection=self.checking_ambiguous_intersection()

            if sentences_to_remove:
                cleaned_knowledge=[]
                for sentence in self.knowledge:
                    if id(sentence) not in sentences_to_remove and sentence.cells:
                        cleaned_knowledge.append(sentence)
                self.knowledge = cleaned_knowledge
            
            else:
                cleaned_knowledge=[]
                for sentence in self.knowledge:
                    if sentence.cells :
                        cleaned_knowledge.append(sentence)
                self.knowledge = cleaned_knowledge
            
            # If any of theses checks return true, it means new information was found and knowledge was modified.
            # as such, the Ai should check the knowledge again, till no more information can be obtained
            if new_knowledge or checking_intersections or ambiguous_intersection:
                print("knowledge = {", end=" ")
                for sentence in self.knowledge:
                    print(sentence,end= " ")
                print("}", end="")
                print('')
                return True

    def checking_intersections(self):
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

            If any new_knowledge is found, return true, else, return false.
            """
            new_knowledge=False

            for sentence1 in self.knowledge.copy():
                
                inter_found=True
                while inter_found:
                    inter_found=False
                    for sentence2 in self.knowledge.copy():
                        if sentence2 == sentence1:
                            continue

                        in_common = sentence1.cells.intersection(sentence2.cells)
                        if len(in_common) >= 2 and in_common not in self.checked_intersection:
                            inter_found=True
                            self.checked_intersection.add(frozenset(in_common))
                            sentences_with_inter=[sentence1,sentence2]
                            intersection =[set(),[]]
                            inter_cell = intersection[0]
                            inter_values = intersection[1]
                            
                            inter_cell.update(in_common)
                            n_cell=len(inter_cell)
                            for i in range(0,n_cell+1):
                                inter_values.append(i)

                            # find all others (if any) sentences that are superset of the intersection we are testing
                            for sentence3 in self.knowledge:
                                if sentence3 not in sentences_with_inter and sentence3.cells.issuperset(inter_cell):
                                    sentences_with_inter.append(sentence3)

                            print(colored(f"Checking_intersections - sentence/counts - {inter_cell}/{inter_values}",'cyan'))
                            print(colored(f"sentences with inter",'cyan'),end=" ")
                            for sentence in sentences_with_inter:
                                print(colored(f"{sentence}",'cyan'),end=" ")
                            print('')
                            # Check each of the possible values against each of the superset sentences
                            for value in inter_values.copy():
                                for sentence in sentences_with_inter:
                                    print(f" sentence to be test = {sentence}")
                                    difference_cell = len(sentence.cells)-n_cell
                                    difference_count = sentence.count - value
                                    print(f"difference_cell = {difference_cell}")
                                    print(f"diffenrece_count = {difference_count}")
                                    # checking the conditions that would make this a valid value, 
                                    # but only triggering if they aren't a valid one (because of the Not and or)
                                    if not (difference_cell >= difference_count and difference_count >= 0):
                                        inter_values.remove(value)
                                        break
                            
                            # If there is only 1 possible value left, then this value is true. Check and add to knowledge.
                            if len(inter_values) == 1:
                                new_sentence = Sentence(inter_cell,inter_values[0])
                                print(colored(f"Only one value for count remains, new sentence = {new_sentence}",'cyan'))
                                self.quick_check(new_sentence)
                                if new_sentence.cells and new_sentence.count >= 0:
                                    print(colored(f" new sentence added to knowledge sentence ={new_sentence}",'cyan'))
                                    self.knowledge.append(new_sentence)
                                new_knowledge=True

                            else:
                                print(colored(f"more then one value for count remains, new ambiguous = {inter_cell},{inter_values}",'cyan'))
                                self.ambiguous_intersection.append([inter_cell,inter_values])
                                new_knowledge=True
            return new_knowledge
    
    def checking_ambiguous_intersection(self):
        """
        Checking the intersections that returned ambiguous result, first trying to find other
        ambiguous intersections that are supersets of the first and checking the result. any that return a
        inequality is discarderd.

        If there are still more then one ambiguous intersection of a kind, compare it to the sentences that
        contain it and check for inequalities, Discarding any found.

        If only 1 sentence remains, that one is valid and should be checked then sent to sentences if
        there is still information after check.

        Returns true if any new_knowledge was found, false otherwise.
        """
        
        # a check to see if this function managed to bring new knowledge
        new_knowledge=False

        # It's a bad idea to change a list/set while looping in it
        # So i will save the ones I want to discard and remove them later.
        ambiguous_to_discard=[]
        if len(self.ambiguous_intersection) >= 2:
            for sentence1 in self.ambiguous_intersection.copy():
                    ambiguous_to_explore=sentence1
                    n_cell = len(sentence1[0])                    

                    # creating a list sentences whose cell's are superset of the one we are testing
                    superset_ambiguous=[]
                    
                    for sentence2 in self.ambiguous_intersection:
                        # if the sentence isn't already in the list of sentences to be explored and is a superset of them
                        if sentence2[0] != ambiguous_to_explore[0] and sentence2[0].issuperset(ambiguous_to_explore[0]):
                            superset_ambiguous.append(sentence2)
                    
                    # if the list isn't empty
                    if (superset_ambiguous):
                        for ambiguous_value in ambiguous_to_explore[1].copy():
                            
                            # Since we are working with possibilities, not certainties, the only way we can
                            # reject a value is if it's a impossibilities for all tests of a superset
                            for lists in superset_ambiguous:
                                rejected = True
                                for test in lists[1]:
                                    difference_cell = len(lists[0]) - n_cell
                                    difference_count = test - ambiguous_value

                                    # if it passes even one test, then we can't discard this value.
                                    if (difference_cell >= difference_count and difference_count >= 0):
                                        rejected=False
                                        break

                                # if it fails all tests, then it can be discarded and we can skip to the next value
                                if rejected:
                                    ambiguous_to_explore[1].remove(ambiguous_value)
                                    new_knowledge=True
                                    break
                    
                    # if there are still more then one values, we will check with the sentences in knowledge
                    # for those whose cells are superset of the one we are testing
                    if len(ambiguous_to_explore[1]) > 1:
                        superset_sentence=[]
                        for sentence in self.knowledge:
                            if sentence.cells.issuperset(ambiguous_to_explore[0]):
                                superset_sentence.append(sentence)

                        if (superset_sentence):
                            for ambiguous_value in ambiguous_to_explore[1].copy():
                                for test in superset_sentence:
                                    difference_cell = len(test.cells) - n_cell
                                    difference_count = test.count - ambiguous_value

                                    if not (difference_cell >= difference_count and difference_count >= 0):
                                        ambiguous_to_explore[1].remove(ambiguous_value)
                                        new_knowledge=True
                                        break

                    if len(ambiguous_to_explore[1]) == 1:
                        new_knowledge=True
                        new_sentence = Sentence(ambiguous_to_explore[0],ambiguous_to_explore[1][0])
                        self.quick_check(new_sentence)
                        if new_sentence.cells and new_sentence.count >= 0:
                            self.knowledge.append(new_sentence)
                        ambiguous_to_discard.append(ambiguous_to_explore)

        if ambiguous_to_discard:
            new_ambiguous_intersection=[]
            for ambiguous in self.ambiguous_intersection:
                if ambiguous not in ambiguous_to_discard and ambiguous[0]:
                    new_ambiguous_intersection.append(ambiguous)
            self.ambiguous_intersection= new_ambiguous_intersection

        print("ambiguous_intersection = [", end="")
        for sentence in self.ambiguous_intersection:
            print(sentence,end= " ")
        print("]")

        return new_knowledge


    def quick_check_ambiguous(self,ambiguous):
        """
        Quickly checks if a ambiguous intersection only has one count (thus becoming a sentence),
        if it has only safes or only mines.
        if it's has become a sentence, add it to sentence and remove it from self.ambiguous.
        """

        #-----------------------
        # make changes so that ambiguous with only 1 cell and multiple valures are deleted
        #----------------------

        cells = ambiguous[0]
        count = ambiguous[1]
        pointer_for_deletion=None
        print(colored(f"quick_check_ambiguous - ambiguous = {ambiguous}",'cyan'))

        


        # check if this sentence is in the knowledge already, if it's save it's value
        # so that i can be deleted in case it's emptied by the end of the check
        if ambiguous in self.ambiguous_intersection:
            pointer_for_deletion = ambiguous
            if len(cells) == 1 and len(count) != 1:
                self.ambiguous_intersection.remove(pointer_for_deletion)
                    
        # Ai's mark_safe and mark_mine will loop and modify the sentence list, 
        # doing that inside a loop that is reading the sentence could lead to error,
        # instead, it will be saved and the mark function will be called after the loops.
        mines_found = set()
        safes_found = set()

        # check if this ambiguous only has 1 valid count
        if len(count) > 1:
            for value in count.copy():
                if value > len(cells) or value < 0:
                    count.remove(value)
        
        # if ambiguous has only 1 count, then it's a valid sentence and we can start to check it
        if len(count) == 1:
                
            # checking if the ambiguous only contains mines
            if count[0] == len(cells):
                for cell in cells.copy():
                    count[0] -= 1
                    mines_found.add(cell)
                    cells.remove(cell)

             # checking if the ambiguous only contains safe cells
            if count[0] == 0:
                for cell in cells.copy():
                    safes_found.add(cell)
                    cells.remove(cell)

            
            # if mines or safes were found, loop in them calling the mark function
            # checking self.knowledge and removing any of the mines/safe found
            if mines_found:
                print(colored(f"quick_check_ambiguous - Mines found = {mines_found}",'cyan'))
                for mine in mines_found:
                    self.mark_mine(mine)
            
            if safes_found:
                print(colored(f"quick_check_ambiguous - Safes found = {safes_found}",'green'))
                for safe in mines_found:
                    self.mark_safe(safe)

            # check if the ambiguous not longer have cells and is part of the ambiguous
            # intersection, if it's empty and part of intersection, remove it from there
            if not cells and pointer_for_deletion:
                self.ambiguous_intersection.remove(pointer_for_deletion)

            # if it still has cells and only 1 count, add it to sentences and remove from 
            # ambiguous intersection
            if cells:
                new_sentence=Sentence(cells,count[0])
                self.knowledge.append(new_sentence)
                self.ambiguous_intersection.remove(pointer_for_deletion)

        # if len(counts) > 1, then there nothing we can assume, as the sentence is still ambiguous
        # so we just leave the function
        else:
            return

        #raise NotImplementedError
    
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if len(self.mines) == 8 :
            print(colored("All mines were found!", 'red'))
            return
        for move in self.safes:
            if move not in self.moves_made:
                print (f"safe move made = {move}")
                return move
        return

        #raise NotImplementedError
    
    

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        # creating a dictionary that has each cell from both knowledge and ambiguous_intersection
        # while also having this cells value ( a representation of how much information that cell would reveal
        # when it's value is found) and the highest chance the cell has to be a mine
        if len(self.mines) == 8 :
            print(colored("All mines were found!", 'red'))
            return
        valuable_cells = {}
        for sentence in self.knowledge:
            for cell in sentence.cells:
                if cell not in valuable_cells:
                    valuable_cells[cell] = [0, 0]

                # the more elements in a sentence beside this cell, the lower it's value
                valuable_cells[cell][0] += 1/len(sentence.cells)
                chance = sentence.count / len(sentence.cells)
                # always picking the highest chance this cell has to be a mine
                if chance > valuable_cells[cell][1]:
                    valuable_cells[cell][1] = chance

        for cells, counts in self.ambiguous_intersection:

            # since we are dealing with possibilities, we are using the averange of the count
            count_averange=0
            for count in counts:
                count_averange+=count
            count_averange = count_averange/len(counts)

            for cell in cells:
                if cell not in valuable_cells:
                    valuable_cells[cell] = [0, 0]
                
                valuable_cells[cell][0] += 1/len(cells)
                chance = count_averange / len(cells)
                if chance > valuable_cells[cell][1]:
                    valuable_cells[cell][1] = chance

        # After finding the chances and value of each cell, we will find the one with the lowest chance
        # of being a mine. if there are more then one, we will add them all to a list
        most_likely_safe_cells=[]
        lowest=1
        for key,value,in valuable_cells.items():
            print(f"Key = {key}, highest Chance of being a mine = {value[1]} value = {value[0]}")
            if value[1] < lowest:
                lowest = value[1]
                most_likely_safe_cells = []
                most_likely_safe_cells.append(key)
            elif value[1] == lowest:
                most_likely_safe_cells.append(key)

        # if there are more then one safest cell, we will find the one that would be more worth of risk
        # in other words, the cell that would reveal more if we could find it's value
        highest=0
        most_valuable_cell=None
        if len(most_likely_safe_cells) > 1:
            for key in most_likely_safe_cells:
                if valuable_cells[key][0] > highest:
                    highest = valuable_cells[key][0]
                    most_valuable_cell = key
        
        # If most valuable exist, then there were more then 1 safest cell, so we return the most valuable
        if most_valuable_cell:
            print(colored(f"Educated random move = {most_valuable_cell}",'blue'))
            return most_valuable_cell
        
        # if it doesn't exist, then there is only one safest cell, we return it.
        elif most_likely_safe_cells:
            print(colored(f"Educated random move = {most_likely_safe_cells[0]}",'blue'))
            return most_likely_safe_cells[0]
        
        # if the program is unable to make a educated guess, it will randomly pick one of the cells in 
        # the board that isn't know to be safe nor mine
        else:
            random_move_options=[]
            for i in range(8):
                for j in range(8):
                    random_move_options.append((i,j))
            random_move_options=[element for element in random_move_options if element not in self.safes]
            random_move_options=[element for element in random_move_options if element not in self.mines]
            try:
                move = random.choice(random_move_options)
                print(colored(f"random move = {move}",'blue'))
                return move
            
            except:
                print(colored("All mines were found!", 'red'))
                return

        raise NotImplementedError
