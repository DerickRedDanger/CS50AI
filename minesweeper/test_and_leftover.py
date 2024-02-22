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
            cells = sentence.cells
            counts = sentence.count

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

       