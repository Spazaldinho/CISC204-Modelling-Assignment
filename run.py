from bauhaus import Encoding, proposition, constraint, Not
from bauhaus.utils import count_solutions, likelihood
from cards import *
from players import COLOR

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"

# Encoding that will store all of your constraints
E = Encoding()

# Checks if a tile at (i, j) is occupied by anyone
@proposition(E)
class occupied:
    def __init__(self, i, j, color) -> None:
        self.i = i
        self.j = j
        # ADDED TO SPECIFY WHO HAS THE TILE
        self.color = color
    
    def __str__(self) -> str:
        return f"{self.color} tile at ({self.i}, {self.j})"
    
    def __hash__(self):
        return hash(str(self.color))
    
    def __eq__(self, __value: object) -> True:
        if type(self) != type(object):
            return False
        return hash(self) == hash(__value)

# REMOVED, USING THE PLAYER COLOR ENUM TO NOTE WHO IS OCCUPYING A TILE IN OCCUPIED
# Checks if a tile at (i, j) is occupied by blue (would imply that it is occupied as well)
# @proposition(E)
# class blue:
#     def __init__(self, i, j) -> None:
#         self.i = i
#         self.j = j
    
#     def __str__(self) -> str:
#         return f"(The tile at ({self.i}, {self.j}) is blue.)"

# Indicates that the player has a sequence in a vertical line from top (i,j) to bottom (i, j+4)
@proposition(E)
class s_vertical:
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j
    
    def __str__(self) -> str:
        return f"(There is a vertical sequence from ({self.i}, {self.j}) to ({self.i}, {self.j+4}).)"

# Indicates that the player has a sequence in a horizontal line from left (i,j) to right (i+4, j)
@proposition(E)
class s_horizontal:
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j
    
    def __str__(self) -> str:
        return f"(There is a horizontal sequence from ({self.i}, {self.j}) to ({self.i+4}, {self.j}).)"
    
# Indicates that the player has a sequence in a diagonal line from bottom left (i,j) to top right (i+4, j-4)
@proposition(E)
class s_diagonal_up:
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j
    
    def __str__(self) -> str:
        return f"(There is a diagonal sequence from ({self.i}, {self.j}) to ({self.i+4}, {self.j-4}).)"

# Indicates that the player has a sequence in a diagonal line from top left (i,j) to bottom right (i+4, j+4)
@proposition(E)
class s_diagonal_down:
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j
    
    def __str__(self) -> str:
        return f"(There is a diagonal sequence from ({self.i}, {self.j}) to ({self.i+4}, {self.j+4}).)"
    
# If a player has a card corresponding to a tile at (i, j)
@proposition(E)
class can_occupy:
    def __init__(self, i, j, color) -> None:
        self.i = i
        self.j = j
        # Using color enum to show who is able to occupy
        self.color = color

    def __str__(self)  -> None:
        return f"({self.color} can occupy the tile at ({self.i}, {self.j}).)"

# If blue can make a sequence (has a line of 4 tiles) from top (i, j) to bottom (i, j+3)
@proposition(E)
class can_sequence_v:
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j
    
    def __str__(self) -> str:
        return f"(A vertical sequence can be made around ({self.i}, {self.j}).)"

# If blue can make a sequence (has a line of 4 tiles) from left (i, j) to right (i+3, j)
@proposition(E)
class can_sequence_h:
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j
    
    def __str__(self) -> str:
        return f"(A horizontal sequence can be made around ({self.i}, {self.j}).)"
    
# If blue can make a sequence (has a line of 4 tiles) from bottom left (i, j) to top right (i+3, j+3)
@proposition(E)
class can_sequence_d_up:
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j
    
    def __str__(self) -> str:
        return f"(A diagonal sequence can be made around ({self.i}, {self.j}).)"
    
# If blue can make a sequence (has a line of 4 tiles) from top (i, j) to bottom (i, j+3)
@proposition(E)
class can_sequence_d_down:
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j
    
    def __str__(self) -> str:
        return f"(A vertical sequence can be made around ({self.i}, {self.j}).)"

# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():
    # At most 2 sequences, the number of s_vertical + s_horizontal + s_diagonal_up + s_diagonal_down 

    # The size of the board is 10x10, each tile has coordinates (i,j). Top left tile is (0,0) and bottom right is (9,9)

    # Sequences of the same kind can't overlap with each other, they will only be one sequence (any proposition starting with s_ is a sequence)

    # Sequences and can sequence only consider blue
    print()


def initialize_random_board(number_of_turns_passed):
    import random
    ij_pairs = []
    occupiedList = [[], [], []]
    for w in range (0, 3):
        for x in range (0, number_of_turns_passed+1):
            y = random.randint(0, 9)
            z = random.randint(0, 9)
            pair = [y, z]
            if ij_pairs.__contains__(pair):
                x -= 1
            else:
                ij_pairs.append(pair)
                occupiedList[w].append(occupied(y, z, COLOR[w]))

    for x in ij_pairs:
        print(x)
    for x in occupiedList:
        for y in x:
            print(y)

# def board_state(board):
#     # Board size
#     height = 10
#     width = 10
#     sequence_length = 5

#     # Check vertical
#     for i in range(0, 10):
#         for j in range(0, height-(sequence_length-1)):
#             if (board[i][j] == occupied(0,0, COLOR[2])):
                

#     # Check horizontal
#     # Check diagonal_up
#     # Check diagonal_down
    
    
if __name__ == "__main__":

    initialize_random_board(10)

    T = example_theory()
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % T.satisfiable())
    print("# Solutions: %d" % count_solutions(T))
    print("   Solution: %s" % T.solve())

    # print("\nVariable likelihoods:")
    # for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
    #     # Ensure that you only send these functions NNF formulas
    #     # Literals are compiled to NNF here
    #     print(" %s: %.2f" % (vn, likelihood(T, v)))
    print()

    
