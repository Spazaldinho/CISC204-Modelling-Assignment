from bauhaus import Encoding, proposition, constraint, And
from bauhaus.utils import count_solutions, likelihood
from cards import *
import random

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"

# Encoding that will store all of your constraints
E = Encoding()

class Hashable:
    def __hash__(self):
        return hash(str(self))

    def __eq__(self, __value: object) -> bool:
        return hash(self) == hash(__value)

    def __repr__(self):
        return str(self)

# Defines if a tile at (i, j) is occupied by anyone
@proposition(E)
class occupied(Hashable):
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j
    
    def __str__(self) -> str:
        return f"Tile is occupied at ({self.i}, {self.j})"
    
# Defines if a tile at (i, j) is occupied by red, red(i, j)
@proposition(E)
class o_red(Hashable):
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j
    
    def __str__(self) -> str:
        return f"Red tile at ({self.i}, {self.j})"
    
# Defines if a tile at (i, j) is occupied by green, green(i, j)
@proposition(E)
class o_green(Hashable):
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j
    
    def __str__(self) -> str:
        return f"Green tile at ({self.i}, {self.j})"

# Defines if a tile at (i, j) is occupied by blue, blue(i, j)
@proposition(E)
class o_blue(Hashable):
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j
    
    def __str__(self) -> str:
        return f"Blue tile at ({self.i}, {self.j})"
    
# Defines if someone has a card that can be played on this tile
@proposition(E)
class playable(Hashable):
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j
    
    def __str__(self) -> str:
        return f"At least one player can place a token at ({self.i}, {self.j})"
    
# Defines if red has a card that can be played on this tile
@proposition(E)
class playable_red(Hashable):
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j
    
    def __str__(self) -> str:
        return f"Red can place a token at ({self.i}, {self.j})"
    
# Defines if green has a card that can be played on this tile
@proposition(E)
class playable_green(Hashable):
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j
    
    def __str__(self) -> str:
        return f"Green can place a token at ({self.i}, {self.j})"
    
# Defines if blue has a card that can be played on this tile
@proposition(E)
class playable_blue(Hashable):
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j
    
    def __str__(self) -> str:
        return f"Blue can place a token at ({self.i}, {self.j})"
    


def initialize_game_state():
    occupied_list = []
    not_occupied_list = []
    red = []
    green = []
    blue = []
    red_cards = []
    green_cards = []
    blue_cards = []
    dealt_cards = []
    
    for x in range(0, 3):
        unique_pairs = set()  # Use a set to ensure uniqueness
        
        while len(unique_pairs) < 10:
            i = random.randint(0, 9)
            j = random.randint(0, 9)
            new_ij = (i, j)
            
            if new_ij not in unique_pairs:
                unique_pairs.add(new_ij)
                occupied_list.append(new_ij)
                
                if x == 0:
                    # Red tiles
                    E.add_constraint(And(occupied(i, j), o_red(i, j)))
                    red.append(new_ij)
                elif x == 1:
                    # Green tiles
                    E.add_constraint(And(occupied(i, j), o_green(i, j)))
                    green.append(new_ij)
                else:
                    # Blue tiles
                    E.add_constraint(And(occupied(i, j), o_blue(i, j)))
                    blue.append(new_ij)

    for x in range (0, 10):
        for y in range(0, 10):
            pair = (x, y)
            if not occupied_list.__contains__(pair):
                E.add_constraint(~occupied(x, y))
                not_occupied_list.append(pair)

    
    for x in range(0, 3):

        unique_pairs = set()

        while len(unique_pairs) < 7:
            i = random.randint(0, 9)
            j = random.randint(0, 9)
            pair = (i, j)

            if pair not in occupied_list and pair not in dealt_cards and pair not in unique_pairs:
                dealt_cards.append(pair)
                unique_pairs.add(pair)

                if x == 0:
                    # Red cards
                    E.add_constraint(playable(i, j) & playable_red(i, j))
                    red_cards.append(pair)
                elif x == 1:
                    # Green cards
                    E.add_constraint(playable(i, j) & playable_green(i, j))
                    green_cards.append(pair)
                else:
                    # Blue cards
                    E.add_constraint(playable(i, j) & playable_blue(i, j))
                    blue_cards.append(pair)




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
    initialize_game_state()
    print()
    return E
    
    
if __name__ == "__main__":

    # initialize_random_board(10)

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

    





# def initialize_random_board(number_of_turns_passed):
#     import random
#     ij_pairs = []
#     occupiedList = [[], [], []]
#     for w in range (0, 3):
#         for x in range (0, number_of_turns_passed+1):
#             y = random.randint(0, 9)
#             z = random.randint(0, 9)
#             pair = [y, z]
#             if ij_pairs.__contains__(pair):
#                 x -= 1
#             else:
#                 ij_pairs.append(pair)
#                 occupiedList[w].append(occupied(y, z, COLOR[w]))

#     for x in ij_pairs:
#         print(x)
#     for x in occupiedList:
#         for y in x:
#             print(y)

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
# 
#     
# REMOVED, USING THE PLAYER COLOR ENUM TO NOTE WHO IS OCCUPYING A TILE IN OCCUPIED
# # Checks if a tile at (i, j) is occupied by blue (would imply that it is occupied as well)
# # @proposition(E)
# # class blue:
# #     def __init__(self, i, j) -> None:
# #         self.i = i
# #         self.j = j
    
# #     def __str__(self) -> str:
# #         return f"(The tile at ({self.i}, {self.j}) is blue.)"

# # Indicates that the player has a sequence in a vertical line from top (i,j) to bottom (i, j+4)
# @proposition(E)
# class s_vertical:
#     def __init__(self, i, j) -> None:
#         self.i = i
#         self.j = j
    
#     def __str__(self) -> str:
#         return f"(There is a vertical sequence from ({self.i}, {self.j}) to ({self.i}, {self.j+4}).)"

# # Indicates that the player has a sequence in a horizontal line from left (i,j) to right (i+4, j)
# @proposition(E)
# class s_horizontal:
#     def __init__(self, i, j) -> None:
#         self.i = i
#         self.j = j
    
#     def __str__(self) -> str:
#         return f"(There is a horizontal sequence from ({self.i}, {self.j}) to ({self.i+4}, {self.j}).)"
    
# # Indicates that the player has a sequence in a diagonal line from bottom left (i,j) to top right (i+4, j-4)
# @proposition(E)
# class s_diagonal_up:
#     def __init__(self, i, j) -> None:
#         self.i = i
#         self.j = j
    
#     def __str__(self) -> str:
#         return f"(There is a diagonal sequence from ({self.i}, {self.j}) to ({self.i+4}, {self.j-4}).)"

# # Indicates that the player has a sequence in a diagonal line from top left (i,j) to bottom right (i+4, j+4)
# @proposition(E)
# class s_diagonal_down:
#     def __init__(self, i, j) -> None:
#         self.i = i
#         self.j = j
    
#     def __str__(self) -> str:
#         return f"(There is a diagonal sequence from ({self.i}, {self.j}) to ({self.i+4}, {self.j+4}).)"
    
# # If a player has a card corresponding to a tile at (i, j)
# @proposition(E)
# class can_occupy:
#     def __init__(self, i, j, color) -> None:
#         self.i = i
#         self.j = j
#         # Using color enum to show who is able to occupy
#         self.color = color

#     def __str__(self)  -> None:
#         return f"({self.color} can occupy the tile at ({self.i}, {self.j}).)"

# # If blue can make a sequence (has a line of 4 tiles) from top (i, j) to bottom (i, j+3)
# @proposition(E)
# class can_sequence_v:
#     def __init__(self, i, j) -> None:
#         self.i = i
#         self.j = j
    
#     def __str__(self) -> str:
#         return f"(A vertical sequence can be made around ({self.i}, {self.j}).)"

# # If blue can make a sequence (has a line of 4 tiles) from left (i, j) to right (i+3, j)
# @proposition(E)
# class can_sequence_h:
#     def __init__(self, i, j) -> None:
#         self.i = i
#         self.j = j
    
#     def __str__(self) -> str:
#         return f"(A horizontal sequence can be made around ({self.i}, {self.j}).)"
    
# # If blue can make a sequence (has a line of 4 tiles) from bottom left (i, j) to top right (i+3, j+3)
# @proposition(E)
# class can_sequence_d_up:
#     def __init__(self, i, j) -> None:
#         self.i = i
#         self.j = j
    
#     def __str__(self) -> str:
#         return f"(A diagonal sequence can be made around ({self.i}, {self.j}).)"
    
# # If blue can make a sequence (has a line of 4 tiles) from top (i, j) to bottom (i, j+3)
# @proposition(E)
# class can_sequence_d_down:
#     def __init__(self, i, j) -> None:
#         self.i = i
#         self.j = j
    
#     def __str__(self) -> str:
#         return f"(A vertical sequence can be made around ({self.i}, {self.j}).)"