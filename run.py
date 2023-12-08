from bauhaus import Encoding, proposition, constraint, And
from bauhaus.utils import count_solutions, likelihood
from cards import *
import random
import subprocess
import sys
import json

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
    
occupied_list = []
not_occupied_list = []
red = []
green = []
blue = []
red_cards = []
green_cards = []
blue_cards = []
dealt_cards = []
blue_unified = []
red_unified = []
green_unified = []


def initialize_game_state():
    
    
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

blueE = Encoding()

@proposition(blueE)
class blue_horizontal(Hashable):
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j
    
    def __str__(self) -> str:
        return f"Blue can win with tiles at ({self.i}, {self.j}), ({self.i + 1}, {self.j}), ({self.i + 2}, {self.j}), ({self.i + 3}, {self.j})."
    
@proposition(blueE)
class no_blue_horizontal(Hashable):    
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j

    def __str__(self) -> str:
        return f"Blue can't win with a horizontal sequence starting at ({self.i}, {self.j})."
    
@proposition(blueE)
class blue_vertical(Hashable):
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j
    
    def __str__(self) -> str:
        return f"Blue can win with tiles at ({self.i}, {self.j}), ({self.i}, {self.j + 1}), ({self.i}, {self.j + 1}), ({self.i}, {self.j + 3})."
    
@proposition(blueE)
class no_blue_vertical(Hashable):    
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j

    def __str__(self) -> str:
        return f"Blue can't win with a horizontal sequence starting at ({self.i}, {self.j})."

@proposition(blueE)
class blue_diagonal(Hashable):
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j
    
    def __str__(self) -> str:
        return f"blue can win with a diagonal sequence going up, starting at ({self.i}, {self.j}))."
    
@proposition(blueE)
class no_blue_diagonal_up(Hashable):    
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j

    def __str__(self) -> str:
        return f"blue can't win with a diagonal sequence starting at ({self.i}, {self.j})."
    
@proposition(blueE)
class no_blue_diagonal_down(Hashable):    
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j
    def __str__(self) -> str:
        return f"blue can't win with a diagonal sequence going down, starting at ({self.i}, {self.j})."

def check_blue_win():

    for y in range(0, 10):
        for x in range (0, 7):
            p1 = (x, y)
            p2 = (x + 1, y)
            p3 = (x + 2, y)
            p4 = (x + 3, y)
            if p1 in blue_unified and p2 in blue_unified and p3 in blue_unified and p4 in blue_unified:
                blueE.add_constraint(blue_horizontal(x, y))
                flag = 1
                print("Blue can win!")
            else:
                blueE.add_constraint(no_blue_horizontal(x, y))

    for y in range(0, 7):
        for x in range (0, 10):
            p1 = (x, y)
            p2 = (x, y + 1)
            p3 = (x, y + 2)
            p4 = (x, y + 3)
            if p1 in blue_unified and p2 in blue_unified and p3 in blue_unified and p4 in blue_unified:
                blueE.add_constraint(blue_vertical(x, y))
                flag = 1
                print("Blue can win!")
            else:
                blueE.add_constraint(no_blue_vertical(x, y))

    for y in range(0, 7):
        for x in range(0, 7):
            p1 = (x, y)
            p2 = (x + 1, y + 1)
            p3 = (x + 2, y + 2)
            p4 = (x + 3, y + 3)
            if p1 in blue_unified and p2 in blue_unified and p3 in blue_unified and p4 in blue_unified:
                blueE.add_constraint(blue_diagonal(x, y))
                flag = 1
                print("blue can win!")
            else:
                blueE.add_constraint(no_blue_diagonal_down(x, y))

    for y in range(4, 10):
        for x in range(0, 7):
            p1 = (x, y)
            p2 = (x + 1, y - 1)
            p3 = (x + 2, y - 2)
            p4 = (x + 3, y - 3)
            if p1 in blue_unified and p2 in blue_unified and p3 in blue_unified and p4 in blue_unified:
                blueE.add_constraint(blue_diagonal(x, y))
                flag = 1
                print("blue can win!")
            else:
                blueE.add_constraint(no_blue_diagonal_up(x, y))





redE = Encoding()

@proposition(redE)
class red_horizontal(Hashable):
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j
    
    def __str__(self) -> str:
        return f"red can win with tiles at ({self.i}, {self.j}), ({self.i + 1}, {self.j}), ({self.i + 2}, {self.j}), ({self.i + 3}, {self.j})."
    
@proposition(redE)
class no_red_horizontal(Hashable):    
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j

    def __str__(self) -> str:
        return f"red can't win with a horizontal sequence starting at ({self.i}, {self.j})."
    
@proposition(redE)
class red_vertical(Hashable):
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j
    
    def __str__(self) -> str:
        return f"red can win with tiles at ({self.i}, {self.j}), ({self.i}, {self.j + 1}), ({self.i}, {self.j + 1}), ({self.i}, {self.j + 3})."
    
@proposition(redE)
class no_red_vertical(Hashable):    
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j

    def __str__(self) -> str:
        return f"red can't win with a horizontal sequence starting at ({self.i}, {self.j})."
    
@proposition(redE)
class red_diagonal(Hashable):
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j
    
    def __str__(self) -> str:
        return f"red can win with a diagonal sequence going up, starting at ({self.i}, {self.j}))."
    
@proposition(redE)
class no_red_diagonal_up(Hashable):    
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j

    def __str__(self) -> str:
        return f"red can't win with a diagonal sequence starting at ({self.i}, {self.j})."
    
@proposition(redE)
class no_red_diagonal_down(Hashable):    
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j
    def __str__(self) -> str:
        return f"red can't win with a diagonal sequence going down, starting at ({self.i}, {self.j})."

def check_red_win():

    for y in range(0, 10):
        for x in range (0, 7):
            p1 = (x, y)
            p2 = (x + 1, y)
            p3 = (x + 2, y)
            p4 = (x + 3, y)
            if p1 in red_unified and p2 in red_unified and p3 in red_unified and p4 in red_unified:
                redE.add_constraint(red_horizontal(x, y))
                flag = 1
                print("red can win!")
            else:
                redE.add_constraint(no_red_horizontal(x, y))

    for y in range(0, 7):
        for x in range (0, 10):
            p1 = (x, y)
            p2 = (x, y + 1)
            p3 = (x, y + 2)
            p4 = (x, y + 3)
            if p1 in red_unified and p2 in red_unified and p3 in red_unified and p4 in red_unified:
                redE.add_constraint(red_vertical(x, y))
                flag = 1
                print("red can win!")
            else:
                redE.add_constraint(no_red_vertical(x, y))

    for y in range(0, 7):
        for x in range(0, 7):
            p1 = (x, y)
            p2 = (x + 1, y + 1)
            p3 = (x + 2, y + 2)
            p4 = (x + 3, y + 3)
            if p1 in red_unified and p2 in red_unified and p3 in red_unified and p4 in red_unified:
                redE.add_constraint(red_diagonal(x, y))
                flag = 1
                print("red can win!")
            else:
                redE.add_constraint(no_red_diagonal_down(x, y))

    for y in range(4, 10):
        for x in range(0, 7):
            p1 = (x, y)
            p2 = (x + 1, y - 1)
            p3 = (x + 2, y - 2)
            p4 = (x + 3, y - 3)
            if p1 in red_unified and p2 in red_unified and p3 in red_unified and p4 in red_unified:
                redE.add_constraint(red_diagonal(x, y))
                flag = 1
                print("red can win!")
            else:
                redE.add_constraint(no_red_diagonal_up(x, y))




greenE = Encoding()

@proposition(greenE)
class green_horizontal(Hashable):
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j
    
    def __str__(self) -> str:
        return f"green can win with tiles at ({self.i}, {self.j}), ({self.i + 1}, {self.j}), ({self.i + 2}, {self.j}), ({self.i + 3}, {self.j})."
    
@proposition(greenE)
class no_green_horizontal(Hashable):    
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j

    def __str__(self) -> str:
        return f"green can't win with a horizontal sequence starting at ({self.i}, {self.j})."
    
@proposition(greenE)
class green_vertical(Hashable):
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j
    
    def __str__(self) -> str:
        return f"green can win with tiles at ({self.i}, {self.j}), ({self.i}, {self.j + 1}), ({self.i}, {self.j + 1}), ({self.i}, {self.j + 3})."
    
@proposition(greenE)
class no_green_vertical(Hashable):    
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j

    def __str__(self) -> str:
        return f"green can't win with a horizontal sequence starting at ({self.i}, {self.j})."
    
@proposition(greenE)
class green_diagonal(Hashable):
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j
    
    def __str__(self) -> str:
        return f"green can win with a diagonal sequence going up, starting at ({self.i}, {self.j}))."
    
@proposition(greenE)
class no_green_diagonal_up(Hashable):    
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j

    def __str__(self) -> str:
        return f"green can't win with a diagonal sequence starting at ({self.i}, {self.j})."
    
@proposition(greenE)
class no_green_diagonal_down(Hashable):    
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j

    def __str__(self) -> str:
        return f"green can't win with a diagonal sequence going down, starting at ({self.i}, {self.j})."

def check_green_win():

    for y in range(0, 10):
        for x in range (0, 7):
            p1 = (x, y)
            p2 = (x + 1, y)
            p3 = (x + 2, y)
            p4 = (x + 3, y)
            if p1 in green_unified and p2 in green_unified and p3 in green_unified and p4 in green_unified:
                greenE.add_constraint(green_horizontal(x, y))
                flag = 1
                print("green can win!")
            else:
                greenE.add_constraint(no_green_horizontal(x, y))

    for y in range(0, 7):
        for x in range(0, 7):
            p1 = (x, y)
            p2 = (x + 1, y + 1)
            p3 = (x + 2, y + 2)
            p4 = (x + 3, y + 3)
            if p1 in green_unified and p2 in green_unified and p3 in green_unified and p4 in green_unified:
                greenE.add_constraint(green_diagonal(x, y))
                flag = 1
                print("green can win!")
            else:
                greenE.add_constraint(no_green_diagonal_down(x, y))

    for y in range(4, 10):
        for x in range(0, 7):
            p1 = (x, y)
            p2 = (x + 1, y - 1)
            p3 = (x + 2, y - 2)
            p4 = (x + 3, y - 3)
            if p1 in green_unified and p2 in green_unified and p3 in green_unified and p4 in green_unified:
                greenE.add_constraint(green_diagonal(x, y))
                flag = 1
                print("green can win!")
            else:
                greenE.add_constraint(no_green_diagonal_up(x, y))

    for y in range(0, 7):
        for x in range (0, 10):
            p1 = (x, y)
            p2 = (x, y + 1)
            p3 = (x, y + 2)
            p4 = (x, y + 3)
            if p1 in green_unified and p2 in green_unified and p3 in green_unified and p4 in green_unified:
                greenE.add_constraint(green_vertical(x, y))
                flag = 1
                print("green can win!")
            else:
                greenE.add_constraint(no_green_vertical(x, y))


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
    
def blue_win():
    check_blue_win()
    return blueE

def red_win():
    check_red_win()
    return redE

def green_win():
    check_green_win()
    return greenE


if __name__ == "__main__":

    T = example_theory()
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % T.satisfiable())
    print("# Solutions: %d" % count_solutions(T))
    print("   Solution: %s" % T.solve())

    #These loops create a shared list of where each team has tiles and where they can also place tiles
    for x in range (0, 10):
        blue_unified.append(blue[x])
        red_unified.append(red[x])
        green_unified.append(green[x])
    for x in range (0, 7):
        blue_unified.append(blue_cards[x])
        red_unified.append(red_cards[x])
        green_unified.append(green_cards[x])
    
    

    B = blue_win()
    # Don't compile until you're finished adding all your constraints!
    B = B.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % B.satisfiable())
    print("# Solutions: %d" % count_solutions(B))
    print("   Solution: %s" % B.solve())

    R = red_win()
    # Don't compile until you're finished adding all your constraints!
    R = R.compile()
    print("\nSatisfiable: %s" % R.satisfiable())
    print("# Solutions: %d" % count_solutions(R))
    print("   Solution: %s" % R.solve())

    G = green_win()
    # Don't compile until you're finished adding all your constraints!
    G = G.compile()
    print("\nSatisfiable: %s" % G.satisfiable())
    print("# Solutions: %d" % count_solutions(G))
    print("   Solution: %s" % G.solve())

    


    red_json = json.dumps(red)
    blue_json = json.dumps(blue)
    green_json = json.dumps(green)
    red_cards_json = json.dumps(red_cards)
    blue_cards_json = json.dumps(blue_cards)
    green_cards_json = json.dumps(green_cards)
    subprocess.run([sys.executable, 'app.py', '--red', red_json, '--blue', blue_json, '--green', green_json, '--red_cards', red_cards_json, '--blue_cards', blue_cards_json, '--green_cards', green_cards_json])