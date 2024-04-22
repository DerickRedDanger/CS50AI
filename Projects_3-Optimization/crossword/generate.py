import sys

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

        for var in self.crossword.variables:
            for word in self.domains[var].copy():
                if len(word) != var.length:
                    self.domains[var].remove(word)


        # raise NotImplementedError

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        X_overlap_Y = self.crossword.overlaps[x,y]
        Y_overlap_X = self.crossword.overlaps[y,x]

        if X_overlap_Y:
            cellx= X_overlap_Y[0]
            celly= X_overlap_Y[1]

        elif Y_overlap_X:
            celly= Y_overlap_X[0]
            cellx= Y_overlap_X[1]

        else:
            return False
        
        revision = False
        
        # checks for each word in X if there is a word in y that has the same letter in the
        # intersection between both. If there is, keep that word. if there isn't, remove that word.
        for word in self.domains[x].copy():
            if not any(word(cellx) == word2(celly) for word2 in self.domains[y]):
                self.domains[x].remove(word)
                revision = True
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
                        if self.crossword.overlaps(x,y):
                            queue.append((x,y))
                            neighbors.setdefault(x, set()).add(y)

            queue = queue_2s(queue)

        else:
            queue = queue_2s(arcs)

            for X in arcs:
                for Y in arcs:
                    x=X[0]
                    y=Y[0]
                    if x != y:
                        if self.crossword.overlaps(x,y):
                            neighbors.setdefault(x, set()).add(y)

        # while the queue has more then 0 elements
        while queue.check():
            value = queue.dequeue()
            x = value[0]
            y = value[1]
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

        # Returns False if any value is none, True otherwise
        return not any(value is None for value in assignment.values())

        raise NotImplementedError

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        # checked = set()

        for key1, value1 in assignment.items():
            if value1 != None:
                # If the value has a length different then the variable's
                if len(value1) != self.crossword.variables[key1].length:
                    return False

                for key2, value2 in assignment.items():
                    if value2 != None:
                        # If two values have the same strings
                        if value1 == value2:
                            return False
                        
                        # Checking if the keys overlaps, if they do,
                        # check if the overlaps have the same values
                        X_overlap_Y = self.crossword.overlaps[key1,key2]
                        Y_overlap_X = self.crossword.overlaps[key2,key1]

                        if X_overlap_Y:
                            cellx= X_overlap_Y[0]
                            celly= X_overlap_Y[1]

                        elif Y_overlap_X:
                            celly= Y_overlap_X[0]
                            cellx= Y_overlap_X[1]
                        
                        if cellx:
                            if value1[cellx] != value2[celly]:
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
        neighbors =[]
        for options, words in assignment.items():
            if words == None and options != var:
                overlap = self.crossword.overlaps[var,options]
                if overlap:
                    # neighbors being a list of (neighbor,((index in var),(index in neighbor)))
                    neighbors.append((options,(overlap)))

        domain_values = []
        for word in self.domains[var]:
            n = 0
            for neighbor in neighbors:
                if word in self.domains[neighbor[0]]:
                    n += 1
                for word2 in self.domains[neighbor[0]]:
                    # the and is to make sure it's not double couting
                    if word[neighbor[1][0]] != word2[neighbor[1][1]] and word != word2:
                        n += 1
            domain_values.append((word,n))

    
        sorted_domains = sorted(domain_values, key=lambda x:x[1])

        return sorted_domains
    
        raise NotImplementedError
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        variable =[]
        for options, words in assignment.items():
            if words == None:
                n_values = len(self.domains[options])
                n_neighbors = 0
                for options2, words2 in assignment.items():
                    if words2 == None and options2 != options:
                        if self.crossword.overlaps[options,options2]:
                            n_neighbors +=1
                variable.append((options,n_values,n_neighbors))

        sorted_variables = sorted(variable, key=lambda x: (x[1], -x[2]))
        return sorted_variables[0][0]
        raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        raise NotImplementedError

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
        if not queue:
            self.s1 = []
        else:
            for element in queue:
                self.s1.append(element)

        self.s2 = []

    def enqueue(self,item):

        self.s1.append(item)

    def dequeue(self):
        if not self.s1 and not self.s2:
            raise QueueEmptyError("Queue is empty")

        elif not self.s2 and self.s1:
            for _ in range(len(self.s1)):
                self.s2.append(self.s1.pop())
    
        return self.s2.pop()
    
    

    def check(self):
        return len(self.s1) + len(self.s2)
                
class QueueEmptyError(Exception):
        pass

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
