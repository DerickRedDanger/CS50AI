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

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.cells and self.count == 0:
            print(f"know_safes = {self.cells}")
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # Removing mine cells from the sentence and
        # reducing it's count by 1 per cell removed
        if cell in self.cells.copy():
            self.cells.discard(cell)
            self.count -= 1
            # Return true if this sentence was modified
            return True
        # False otherwise
        return False

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # Removing the safe cell from the sentence, if it's there
        if cell in self.cells.copy():
            self.cells.discard(cell)
            # Return true if this sentence was modified
            return True
        # False otherwise
        return False


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

        # set of all checked intersection that were processed in add_knowledge
        self.checked_intersection = set()

        # list of all checked intersection that still were ambiguous after processed in add_knowledge
        self.ambiguous_intersection = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """

        # Updating all sentences in knowledge
        self.mines.add(cell)
        if self.knowledge:
            for sentence in self.knowledge:
                if sentence.mark_mine(cell):
                    # If the sentence is modified, check for new knowledge
                    self.quick_check(sentence)

        # Updating all sentences in ambiguous_intersections
        if self.ambiguous_intersection:
            for sentence in self.ambiguous_intersection:
                print(colored(f"Ai_mark_mine_ambiguous - sentence = {sentence}"))

                # If the new mine is in this cell, remove it
                if cell in sentence[0]:
                    sentence[0].remove(cell)
                    index_to_delete = []

                    # Since there is 1 less mine, the value of each possibility of count is reduced by 1
                    for i in range(len(sentence[1])):
                        sentence[1][i] -= 1

                        # If any of the possible counts turns into a impossibility, save their index for removal
                        if len(sentence[0]) < sentence[1][i] or sentence[1][i] < 0:
                            index_to_delete.append(i)

                    # Remove them in the descending order, to avoid changing the index of the elements to be removed
                    for i in reversed(index_to_delete):
                        sentence[1].pop(i)

                    # Check the ambiguous for new information
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
                if cell in sentence[0]:
                    sentence[0].remove(cell)
                    self.quick_check_ambiguous(sentence)

    def quick_check(self, sentence):
        """
        function made to improve the functions efficience by making
        quick checks to a sentence that was just modified, thus reducing te number
        of times the knowledge would loop throught all sentences to check them
        """

        pointer_for_deletion = None

        # check if this sentence is already in the knowledge, if it's, save it's id
        # so that it can be deleted in case it's emptied by the end of the check
        if sentence in self.knowledge:
            pointer_for_deletion = id(sentence)

        # Removing know safe cells from the sentence
        if len(self.safes) != 0:
            for safe in self.safes:
                sentence.mark_safe(safe)

        # Removing know mine cells from the sentence and
        # reducing it's count by 1 per cell removed
        if len(self.mines) != 0:
            for mine in self.mines:
                sentence.mark_mine(mine)

        # Ai's mark_safe and mark_mine will loop and check the sentence set,
        # doing that inside a loop that is reading the sentence could lead to error,
        # instead, it will be saved and the mark function will be called after the loops.
        mines_found = set()
        safes_found = set()

        print(colored(f"sentence about to be checked {sentence}", 'yellow'))
        # checking if the sentence only contains mines
        mine_check = sentence.known_mines()
        if mine_check:
            for mine in mine_check.copy():
                mines_found.add(mine)
                sentence.count -= 1
                sentence.cells.discard(mine)
            print(colored(f"sentence after mine_check = {sentence}", 'yellow'))

        # checking if sentences has only safe cells
        safe_check = sentence.known_safes()
        if safe_check:
            for safe in safe_check.copy():
                safes_found.add(safe)
                sentence.cells.discard(safe)
            print(colored(f"sentence after safe_check = {sentence}", 'yellow'))

        # if mines or safes were found, loop in them calling the mark function
        # checking self.knowledge and self.ambiguous, removing any of the mines/safe found
        if mines_found:
            print(colored(f" quick_check - Mines found = {mines_found}", 'cyan'))
            for mine in mines_found:
                self.mark_mine(mine)

        if safes_found:
            print(colored(f"quick_check - Safes found = {safes_found}", 'green'))
            for safe in safes_found:
                self.mark_safe(safe)

        # check if the sentence not longer have cells and is part of the knowledge
        # if it's empty and part of knowledge, remove it from there
        print(f"sentence at the end of check, before pointer deletion = {sentence}")
        if not sentence.cells and pointer_for_deletion:
            for orignal_sentence in self.knowledge:
                if id(orignal_sentence) == pointer_for_deletion:
                    print(f"Modified sentence to be deleted = {sentence}")
                    print(f"original sentence = {orignal_sentence}")
                    self.knowledge.remove(orignal_sentence)
                    break  # break after removing the item to avoid modifying the list during iteration
                    # it has no negative effect since the aim was to delete the sentence that was modified

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
        print(colored(f"Cell clicked = {cell}, counts = {count}", 'green'))

        """
        Marks the cell as safe
        """
        self.mark_safe(cell)

        """
        add a new sentence to the knowledge base
        """
        surrounding_cells = set()

        # get the surrounding cells
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignoring the cell itself
                if (i, j) == cell:
                    continue

                if 0 <= i < self.height and 0 <= j < self.width:
                    surrounding_cells.add((i, j))

        sentence = Sentence(surrounding_cells, count)
        original_sentence = Sentence(surrounding_cells, count)

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

        # But if it's cells are empty while it's count is != 0, or it's count is < 0 (having cells or not), an error happened
        elif (not sentence.cells and sentence.count != 0) or sentence.count < 0:
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

    def check_knowledge(self):
        """
        Checking the knowledge for developments

        The Mark function already checks the knowledge whenever
        a new safe or mine is found, so it's not nescessary to do it here

        instead, it will compare sets to find subsets, checking what new knowledge
        can be obtained from the actions above, be it new sentences or checking ambiguous hypotheses

        If any new_knowledge is found, return true, else, return false.
        """
        new_knowledge = False

        # saving the sentences that were modified so they can be checked after the loop
        sentences_to_check = []

        if len(self.knowledge) > 1:
            """
            # checking for sentences whose cells contains all of another sentence's cell
            if they exist, then remove theses same cells from sentence 1 and reduce
            the count of the second sentence from the first one.

            Effectively subtracting sentence 2 from sentence 1, creating a new sentence with the result
            removing the original superset sentence only at the end of the function, since they could
            still be used to find new knowledge.
            """

            # Saving the sentence's Id, not the sentence themselves, as they could be modified midway, ending up
            # having the same value as another sentence, leading do the lost of knowledge by removing wrong sentences
            sentences_to_remove = []

            # printing all sentences in knowledge for debugging purpose
            print("knowledge = {", end=" ")
            for sentence in self.knowledge:
                print(sentence, end=" ")
            print("}", end="")
            print('')

            for sentence in self.knowledge.copy():
                # if a sentence has no cells, skip
                if not sentence.cells:
                    continue

                for sentence2 in self.knowledge:
                    # if sentence 2 is a subset of sentence 1, they aren't the same sentence and sentence 2 is not empty
                    # (A empty set is a subset of all sets, thus it could lead to bugs)
                    if sentence.cells.issuperset(sentence2.cells) and sentence.cells != sentence2.cells and sentence2.cells:
                        new_sentence_cells = set()
                        new_sentence_count = 0

                        print(colored(f"{sentence.cells} is superset {sentence2.cells}", 'yellow'))
                        # to keep this function from creating multiple sentences by creating a subset
                        # while still having it's original superset, it's superset will be saved and, after fully
                        # processing knowledge to reduce the loss of information, removed
                        sentences_to_remove.append(id(sentence))

                        new_sentence_cells = sentence.cells.difference(sentence2.cells)
                        new_sentence_count = sentence.count - sentence2.count

                        new_sentence = Sentence(new_sentence_cells, new_sentence_count)
                        sentences_to_check.append(new_sentence)
                        new_knowledge = True

            # if new sentences were created throught the above, check them
            if sentences_to_check:
                for sentence in sentences_to_check:
                    print(colored(f" sentence before the check = {sentence}", 'blue'))
                    self.quick_check(sentence)
                    print(colored(f" sentence after the check = {sentence}", 'blue'))

                    if sentence.cells:
                        print(colored(f" sentence appended to knowledge = {sentence}", 'red'))
                        self.knowledge.append(sentence)
                        print(colored("knowledge after append", 'yellow'))

            # Running the checking_intersections functions, it returns True if new knowledge is found
            checking_intersections = self.checking_intersections()

            # after all knowledge is processed, clean it from any sentence marked to remove and any
            # empty sentences that might've survived.
            # since removing multiple elements from a list is generally taxing to the computer
            # we will instead create a new list without the sentences we want to remove
            if sentences_to_remove:
                cleaned_knowledge = []
                for sentence in self.knowledge:
                    if id(sentence) not in sentences_to_remove and sentence.cells:
                        cleaned_knowledge.append(sentence)
                self.knowledge = cleaned_knowledge

            else:
                cleaned_knowledge = []
                for sentence in self.knowledge:
                    if sentence.cells:
                        cleaned_knowledge.append(sentence)
                self.knowledge = cleaned_knowledge

            # If any of theses checks return true, it means new information was found and knowledge was modified.
            # as such, the Ai should check the knowledge again, only making a move after no more information can be obtained
            if new_knowledge or checking_intersections:

                # printing knowledge for debbuging reasons
                print("knowledge = {", end=" ")
                for sentence in self.knowledge:
                    print(sentence, end=" ")
                print("}", end="")
                print('')
                #

                return True

    def checking_intersections(self):
        """
        Checking for intersection between sentences (cells they have in common), if at least two cells are found,
        check all other sentences and see if there are others with the same cells in common, saving them in a list.
        Then find all values possible for these cells to contain together ( from 0 to n of cells)
        then remove this number of cells from the sentences cells(len(sentence.cells) - len(cell)) in the list and try removing
        each of the possible values from the count of each sentence, looking for a impossibility
        (having less cells then count or having count < 0) each time one is found, discard that possibility and continue.

        if only one possibility remains, this one is true, it's checked and not empty after it, it's added to knowledge.
        If more then one is found, then it's ambiguous, save it in a set to be explored again later
        when more information is avaliable.

        If any new_knowledge is found, return true, else, return false.
        """
        new_knowledge = False

        for sentence1 in self.knowledge.copy():
            # While new intersections are found
            inter_found = True
            while inter_found:
                inter_found = False
                for sentence2 in self.knowledge.copy():
                    # if the sentences are equal, skip
                    if sentence2 == sentence1:
                        continue

                    cells_in_common = sentence1.cells.intersection(sentence2.cells)
                    # if there are two or more cells in common and they weren't checked already
                    if len(cells_in_common) > 1 and cells_in_common not in self.checked_intersection:
                        inter_found = True
                        # saves all checked intersection, to avoid the creation of repetitions.
                        # To save a set inside another, the first one needs to be frozen (it becomes immutable till unfrozen)
                        self.checked_intersection.add(frozenset(cells_in_common))
                        # saves all sentences that have these cells in common, starting with the two that created it
                        sentences_with_inter = [sentence1, sentence2]
                        # instead of int, we are using a list for counts, since it will hold all possible values, not just one
                        intersection = [set(), []]
                        inter_cell = intersection[0]
                        inter_values = intersection[1]

                        inter_cell.update(cells_in_common)
                        n_cell = len(inter_cell)

                        # finding all possible values for this intersection's count (from all cells being safe to all being mines)
                        for i in range(0, n_cell+1):
                            inter_values.append(i)

                        # find all others (if any) sentences that are superset of the intersection we are testing
                        for sentence3 in self.knowledge:
                            if sentence3 not in sentences_with_inter and sentence3.cells.issuperset(inter_cell):
                                sentences_with_inter.append(sentence3)

                        # for debugging reasons
                        print(colored(f"Checking_intersections - sentence/counts - {inter_cell}/{inter_values}", 'cyan'))
                        print(colored(f"sentences with inter", 'cyan'), end=" ")
                        for sentence in sentences_with_inter:
                            print(colored(f"{sentence}", 'cyan'), end=" ")
                        print('')
                        #

                        # Check each of the possible values against each of the superset sentences
                        for value in inter_values.copy():
                            for sentence in sentences_with_inter:

                                difference_cell = len(sentence.cells)-n_cell
                                difference_count = sentence.count - value

                                # for debugging
                                print(f" sentence to be test = {sentence}")
                                print(f"difference_cell = {difference_cell}")
                                print(f"diffenrece_count = {difference_count}")
                                #

                                # checking the conditions that would make this a valid value,
                                # but only triggering if they aren't a valid one (because of the 'not' and 'and')
                                if not (difference_cell >= difference_count and difference_count >= 0):
                                    inter_values.remove(value)
                                    break  # if even one sentence returns impossible, we don't need to check the others.
                                    # So we skip to the next value

                        # If there is only 1 possible value left, then this value is true. Check and add to knowledge.
                        if len(inter_values) == 1:
                            new_sentence = Sentence(inter_cell, inter_values[0])
                            print(colored(f"Only one value for count remains, new sentence = {new_sentence}", 'cyan'))
                            self.quick_check(new_sentence)
                            if new_sentence.cells and new_sentence.count >= 0:
                                print(colored(f"new sentence added to knowledge sentence ={new_sentence}", 'cyan'))
                                self.knowledge.append(new_sentence)
                            new_knowledge = True

                        # if more then 1 value reamins, then this is a ambiguous intersection. Save it ambiguous for procressing later.
                        else:
                            print(
                                colored(f"more then one value for count remains, new ambiguous = {inter_cell},{inter_values}", 'cyan'))
                            self.ambiguous_intersection.append([inter_cell, inter_values])
                            new_knowledge = True

        # if new knowledge was foun, return true, else return false
        return new_knowledge

    def quick_check_ambiguous(self, ambiguous):
        """
        Quickly checks if a ambiguous intersection only has one count (thus becoming a sentence)
        if it became a sentence, check if it has only safes or only mines and
        if it's still have cells, add it to sentence and remove it from self.ambiguous.

        """

        cells = ambiguous[0]
        count = ambiguous[1]
        pointer_for_deletion = None
        print(colored(f"quick_check_ambiguous - ambiguous = {ambiguous}", 'cyan'))

        # check if this sentence is in the knowledge already, if it's save it's value
        # so that i can be deleted in case it's emptied by the end of the check
        if ambiguous in self.ambiguous_intersection:
            pointer_for_deletion = ambiguous

            # if this ambiguous has only one cell but more then one count (since cells are either mines or safe, it should be at max 2)
            # remove it, since we already know every cell is either 1 or 0
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
                print(colored(f"quick_check_ambiguous - Mines found = {mines_found}", 'cyan'))
                for mine in mines_found:
                    self.mark_mine(mine)

            if safes_found:
                print(colored(f"quick_check_ambiguous - Safes found = {safes_found}", 'green'))
                for safe in mines_found:
                    self.mark_safe(safe)

            # check if the ambiguous not longer have cells and is part of the ambiguous
            # intersection, if it's empty and part of intersection, remove it from there
            if not cells and pointer_for_deletion:
                self.ambiguous_intersection.remove(pointer_for_deletion)

            # if it still has cells and only 1 count, add it to sentences and remove from
            # ambiguous intersection
            if cells:
                new_sentence = Sentence(cells, count[0])
                self.knowledge.append(new_sentence)
                self.ambiguous_intersection.remove(pointer_for_deletion)

        # if len(counts) > 1, then there nothing we can assume, as the sentence is still ambiguous
        # so we just leave the function
        else:
            return

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        # didn't find a reason to make this refined nor complicated,
        # since the more information the Ai has, the better
        for move in self.safes:
            if move not in self.moves_made:
                print(f"safe move made = {move}")
                return move
        return

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        # creating a dictionary that has each cell from both knowledge and ambiguous_intersection
        # while also having this cell's value (a representation of how much information that cell would reveal
        # when it's value is found) and the highest chance the cell has to be a mine

        valuable_cells = {}
        know_cells = set()
        for sentence in self.knowledge:
            for cell in sentence.cells:
                know_cells.add(cell)
                # initializing this Key's value, if it doesn't exist in the dictionary
                if cell not in valuable_cells:
                    valuable_cells[cell] = [0, 0]

                # the more elements in a sentence beside this cell, the lower it's value
                valuable_cells[cell][0] += 1/len(sentence.cells)
                chance = sentence.count / len(sentence.cells)

                # always picking the highest chance this cell has to be a mine
                if chance > valuable_cells[cell][1]:
                    valuable_cells[cell][1] = chance

        for cells, counts in self.ambiguous_intersection:

            # since we are dealing with multiple possibilities, not one certainty, we are using the averange of the count
            count_averange = 0
            for count in counts:
                count_averange += count
            count_averange = count_averange/len(counts)

            for cell in cells:
                if cell not in valuable_cells:
                    valuable_cells[cell] = [0, 0]

                valuable_cells[cell][0] += 1/len(cells)
                chance = count_averange / len(cells)
                if chance > valuable_cells[cell][1]:
                    valuable_cells[cell][1] = chance

        # After finding the chance and value of each cell, we will find the one with the lowest chance
        # of being a mine. if there are more then one, we will add them all to a list
        most_likely_safe_cells = []
        lowest = 1
        for key, value, in valuable_cells.items():
            print(f"Key = {key}, highest Chance of being a mine = {value[1]} value = {value[0]}")
            if value[1] < lowest:
                lowest = value[1]
                most_likely_safe_cells = []
                most_likely_safe_cells.append(key)

            elif value[1] == lowest:
                most_likely_safe_cells.append(key)

        # if there are more then one safest cell, we will find the one that would be more worth of risk
        # in other words, the cell that would reveal more if we could find it's value, since there are no
        # other tie breaker avaliable, we will use random in case there is more then 1 option
        highest = 0
        most_valuable_cell = []
        if len(most_likely_safe_cells) > 1:
            for key in most_likely_safe_cells:
                if valuable_cells[key][0] > highest:
                    highest = valuable_cells[key][0]
                    most_valuable_cell = []
                    most_valuable_cell.append(key)

                elif valuable_cells[key][0] == highest:
                    most_valuable_cell.append(key)

        # Finding all unknown cells, cells that aren't present in the sentence, ambiguous, safes nor mines
        random_move_options = set()
        for i in range(self.height):
            for j in range(self.width):
                random_move_options.add((i, j))
        random_move_options = random_move_options - (self.mines | self.safes | know_cells)

        # If the safest cell exist but has a chance of 34% or higher of being a mine, there is a good probability that picking a
        # unknown cell that isn't in the knowledge is safer, since the Ai doesn't have acess to the number of mines
        # it's not possible to give a more precise approximation
        if random_move_options and most_likely_safe_cells and valuable_cells[most_likely_safe_cells[0]][1] >= 0.34:
            print(colored(f"Most likely safe cell chance of being a mine = {valuable_cells[most_likely_safe_cells[0]][1]}", 'blue'))
            move = random.choice(list(random_move_options))
            print(colored(f"random move is safer then the educated one, move = {move}", 'blue'))
            return move

        # if the chance is lower then 34% and most valuable exist, then there were more then 1 safest cell,
        # so we return the most valuable, if only one, or a random of the most valuable
        elif most_valuable_cell:
            move = random.choice(most_valuable_cell)
            print(colored(f"Educated random move = {move}", 'blue'))
            return move

        # if it doesn't exist, then there is only one safest cell and it's chance < 34%, we return it.
        elif most_likely_safe_cells:
            print(colored(f"Educated random move = {most_likely_safe_cells[0]}", 'blue'))
            return most_likely_safe_cells[0]

        # if the program is unable to make a educated guess, it will randomly pick one of the cells in
        # the board that isn't know to be safe nor mine nor is in the knowledge (otherwise it would've done a educated guess)
        else:
            try:
                move = random.choice(list(random_move_options))
                print(colored(f"random move = {move}", 'blue'))
                return move
            # if that's not possible, it means all cells on the board were found to be either safe or mine
            except:
                print(colored("All mines were found!", 'red'))
                print(colored(f"Number of mines = {len(self.mines)} Number of safes = {len(self.safes)}"))
                return
