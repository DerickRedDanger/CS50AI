import sys
from termcolor import colored
import copy
from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # overwriting self.domains[var] with only the elements that satisfy it's lenght
        for var in self.crossword.variables:
            self.domains[var] = {word for word in self.domains[var] if len(word) == var.length}
        
        # raise NotImplementedError

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # check if the variables overlaps
        X_overlap_Y = self.crossword.overlaps[x,y]

        # if they do, get the index in each varaible that should hold the same value.
        if X_overlap_Y:
            cellx= X_overlap_Y[0]
            celly= X_overlap_Y[1]

        # if they don't, we don't need to do anything and no changes were done.
        else:
            return False
        
        revision = False
        
        # checks for each word in X if there is a word in y that has the same letter in the
        # intersection between both. If there is, keep that word. if there isn't, remove that word.
        for word in self.domains[x].copy():
            if not any(word[cellx] == word2[celly] for word2 in self.domains[y]):
                self.domains[x].remove(word)
                # If any change was made, change revision to true
                revision = True

        # Return revision (True or False)
        return revision

        raise NotImplementedError

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        neighbors = {}

        # if arcs wasn't given, get all variables in crossword.varaibles and tuple it with it's neighbors
        if arcs == None:
            queue = []
            for x in self.crossword.variables:
                for y in self.crossword.variables:
                    if x != y:
                        if self.crossword.overlaps[x,y]:
                            queue.append((x,y))
                            neighbors.setdefault(x, set()).add(y)

            queue = queue_2s(queue)

        # if arc is given
        else:
            queue = queue_2s(arcs)

            # Check both elements of the tuple X and tuple Y to build the neighbors dict
            # used nested loops to cover both x elements in X, and both y elements in Y
            for X in arcs:
                for x in X:
                    neighbors[x] = set()
                    for Y in arcs:
                        for y in Y:
                            if x != y and self.crossword.overlaps[x,y]:
                                neighbors[x].add(y)

        # while the queue has more then 0 elements
        while queue.check():
            var = queue.dequeue()

            # Getting both elements from the tuple
            x = var[0]
            y = var[1]
            if y in neighbors[x]:
                if self.revise(x,y):
                    if len(self.domains[x]) == 0:
                        return False
                    for z in neighbors[x]:
                        if z!= y:
                            queue.enqueue((z,x))
        return True

        raise NotImplementedError

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Returns True if all var in variables are in assignments, false otherwise
        return not any(var not in assignment.keys() for var in self.crossword.variables)

        raise NotImplementedError

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        length = {}
        # getting a dictionary with each variable in assignments as key
        # and it's length as value
        for var in assignment.keys():
                length[var] = var.length

        for var1, word1 in assignment.items():
                
                # If the value has a length different then the variable's
                if len(word1) != length[var1]:
                    return False

                for var2, word2 in assignment.items():
                    if var1 != var2:
                        
                        # If two values have the same strings
                        if word1 == word2:
                            return False

                        # Checking if the keys overlaps, if they do,
                        # check if the overlaps have the same values
                        X_overlap_Y = self.crossword.overlaps[var1,var2]

                        if X_overlap_Y:
                            cellx= X_overlap_Y[0]
                            celly= X_overlap_Y[1]

                            if word1[cellx] != word2[celly]:
                                return False

        return True

        raise NotImplementedError

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        neighbors = []
        for var2 in self.crossword.variables:
            if var2 not in assignment.keys() and var != var2:
                overlap = self.crossword.overlaps[var,var2]
                if overlap:
                    # neighbors being a list of (neighbor,((index in var),(index in neighbor)))
                    neighbors.append((var2,(overlap)))

        domain_values = []
        for word in self.domains[var]:
            n = 0
            for neighbor in neighbors:
                if word in self.domains[neighbor[0]]:
                    n += 1
                for word2 in self.domains[neighbor[0]]:
                    # the 'word != word2' is to make sure it's not double couting,
                    # Since we already checked for word in this domains, so if we counted it back there
                    # we'd count it again here.
                    if word[neighbor[1][0]] != word2[neighbor[1][1]] and word != word2:
                        n += 1
            domain_values.append((word,n))

    
        sorted_domains = sorted(domain_values, key=lambda x:x[1])
        cleaned_domains = [value[0] for value in sorted_domains]

        return cleaned_domains
    
        raise NotImplementedError
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned = []
        variable = []

        unassigned = [var for var in self.crossword.variables if var not in assignment.keys()]

        for var1 in unassigned:
            n_values = len(self.domains[var1])
            n_neighbors = 0
            for var2 in unassigned:
                if var1 != var2:
                    if self.crossword.overlaps[var1,var2]:
                        n_neighbors +=1
            variable.append((var1,n_values,n_neighbors))

        sorted_variables = sorted(variable, key=lambda x: (x[1], -x[2]))
        selected_variable = sorted_variables[0][0]
        
        return selected_variable
        raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        # if all keys in assignment have a value and is consistent, return it
        if self.assignment_complete(assignment) and self.consistent(assignment):
            return assignment

        else:
            # get the variable with the smallest domain and/or highest degree
            var = self.select_unassigned_variable(assignment)

            # get it's ordered domain by the number of values it rule out
            domain = self.order_domain_values(var,assignment)

            # make a copy of the domains of all variables,
            # since revise in ac3 will modify them later
            domain_copy = copy.deepcopy(self.domains)

            for value in domain:

                # reset the domain, if it was modified
                self.domains = domain_copy

                # put that value as var's value
                assignment[var] = value

                # check if it's consistent
                if self.consistent(assignment):

                    # if it's, get all arcs
                    arcs = self.get_arcs(assignment)

                    # If there are arcs, do ac3.
                    if arcs:

                        # If it returns false, move on to the next value
                        if not self.ac3(arcs):
                            continue
                    
                    # if nothing went wrong, call backtrack recursively
                    result = self.backtrack(assignment)
                    if result is not None:
                        return result
            
                    # if no value worked, remove it from assignment[var] and return None
                    del assignment[var]
        return None

        raise NotImplementedError
    def get_arcs(self, assignment):
        """
        Gets all arcs to a assignment
        """
        arcs =[]
        Variables = set()

        for var in self.crossword.variables:
            if var not in assignment.keys():
                Variables.add(var)


        for var in Variables:
            for var2 in Variables:
                if var != var2 and self.crossword.overlaps[var,var2]:
                    arcs.append((var,var2))
        return arcs

class queue_2s():
    def __init__(self, queue=None):
        """
        A queue made by using two stacks.

        A queue can be computationally costly as the list increase in size. This happens because
        poping a element that isn't the last from a list, forces python to reorganize the whole list,
        moving the elements after that element foward.
        
        That's why I am using two stacks instead. we will keep appending elements to the first stack, keeping them in order.
        But when we need to dequeue elements, if S2 is already empty, we will pop elements from the first list and append them in the second list,
        So that the first element in the first list become the last in the second one, allowing us to simply pop them in order.
        If s2 is not empty, then we can just continue to pop it's last element, only adding elements from S1 when it's empty again.
        """
        self.s1 = []
        self.s2 = []

        # if queue already exist, appens it's elements to S1, one at time
        # this is done to make sure S1 is still a list. 
        # it might not be true if we did s1 = queue.

        if queue:
            for element in queue:
                self.s1.append(element)

    def enqueue(self,item):
        self.s1.append(item)

    def dequeue(self):

        # if both S1 and S2 are empty
        if not self.s1 and not self.s2:
            raise QueueEmptyError("Queue is empty")

        # If S2 is empty, but S1 isn't
        elif not self.s2 and self.s1:
            for _ in range(len(self.s1)):
                self.s2.append(self.s1.pop())

        return self.s2.pop()
    
    def check(self):
        # Return the number of elements in the queue
        return len(self.s1) + len(self.s2)
                
class QueueEmptyError(Exception):
    def __init__(self, message="Queue is empty"):
        super().__init__(message)

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
