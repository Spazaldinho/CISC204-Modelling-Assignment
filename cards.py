SUIT = [
    'Joker',
    'diamonds',
    'hearts',
    'spades',
    'clubs'
]

VALUE = [
    'Joker', #Corner tile
    'Ace',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    '10',
    'Jack',
    'Queen',
    'King'
]

class card:
    def __init__(self, value, suit) -> None:
        self.value = value
        self.suit = suit
    def __str__(self) -> str:
        if (self.value == VALUE[0]):
            return f"This card is a {self.value}"
        else: 
            return f"This card is the {self.value} of {self.suit}"
        
DECK = [
    card(VALUE[1], SUIT[1]),  # Ace of diamonds
    card(VALUE[2], SUIT[1]),  # 2 of diamonds
    card(VALUE[3], SUIT[1]),  # 3 of diamonds
    card(VALUE[4], SUIT[1]),  # 4 of diamonds
    card(VALUE[5], SUIT[1]),  # 5 of diamonds
    card(VALUE[6], SUIT[1]),  # 6 of diamonds
    card(VALUE[7], SUIT[1]),  # 7 of diamonds
    card(VALUE[8], SUIT[1]),  # 8 of diamonds
    card(VALUE[9], SUIT[1]),  # 9 of diamonds
    card(VALUE[10], SUIT[1]),  # 10 of diamonds
    card(VALUE[11], SUIT[1]),  # Jack of diamonds
    card(VALUE[12], SUIT[1]),  # Queen of diamonds
    card(VALUE[13], SUIT[1]),  # King of diamonds
    card(VALUE[1], SUIT[2]),  # Ace of hearts
    card(VALUE[2], SUIT[2]),  # 2 of hearts
    card(VALUE[3], SUIT[2]),  # 3 of hearts
    card(VALUE[4], SUIT[2]),  # 4 of hearts
    card(VALUE[5], SUIT[2]),  # 5 of hearts
    card(VALUE[6], SUIT[2]),  # 6 of hearts
    card(VALUE[7], SUIT[2]),  # 7 of hearts
    card(VALUE[8], SUIT[2]),  # 8 of hearts
    card(VALUE[9], SUIT[2]),  # 9 of hearts
    card(VALUE[10], SUIT[2]),  # 10 of hearts
    card(VALUE[11], SUIT[2]),  # Jack of hearts
    card(VALUE[12], SUIT[2]),  # Queen of hearts
    card(VALUE[13], SUIT[2]),  # King of hearts
    card(VALUE[1], SUIT[3]),  # Ace of spades
    card(VALUE[2], SUIT[3]),  # 2 of spades
    card(VALUE[3], SUIT[3]),  # 3 of spades
    card(VALUE[4], SUIT[3]),  # 4 of spades
    card(VALUE[5], SUIT[3]),  # 5 of spades
    card(VALUE[6], SUIT[3]),  # 6 of spades
    card(VALUE[7], SUIT[3]),  # 7 of spades
    card(VALUE[8], SUIT[3]),  # 8 of spades
    card(VALUE[9], SUIT[3]),  # 9 of spades
    card(VALUE[10], SUIT[3]),  # 10 of spades
    card(VALUE[11], SUIT[3]),  # Jack of spades
    card(VALUE[12], SUIT[3]),  # Queen of spades
    card(VALUE[13], SUIT[3]),  # King of spades
    card(VALUE[1], SUIT[4]),  # Ace of clubs
    card(VALUE[2], SUIT[4]),  # 2 of clubs
    card(VALUE[3], SUIT[4]),  # 3 of clubs
    card(VALUE[4], SUIT[4]),  # 4 of clubs
    card(VALUE[5], SUIT[4]),  # 5 of clubs
    card(VALUE[6], SUIT[4]),  # 6 of clubs
    card(VALUE[7], SUIT[4]),  # 7 of clubs
    card(VALUE[8], SUIT[4]),  # 8 of clubs
    card(VALUE[9], SUIT[4]),  # 9 of clubs
    card(VALUE[10], SUIT[4]),  # 10 of clubs
    card(VALUE[11], SUIT[4]),  # Jack of clubs
    card(VALUE[12], SUIT[4]),  # Queen of clubs
    card(VALUE[13], SUIT[4]),  # King of clubs
    card(VALUE[0], SUIT[0]),    # Joker
]

class tile:
    def __init__(self, card, i, j) -> None:
        self.card = card
        self.i = i
        self.j = j
    def __str__(self) -> str:
        return f"{self.card} at ({self.i}, {self.j})"
    
TILES = [
    [
        tile(DECK[52], 0, 0),  # Joker
        tile(DECK[27], 1, 0),  # 2 of Spades
        tile(DECK[28], 2, 0),  # 3 of Spades
        tile(DECK[29], 3, 0),  # 4 of Spades
        tile(DECK[30], 4, 0),  # 5 of Spades
        tile(DECK[31], 5, 0),  # 6 of Spades
        tile(DECK[32], 6, 0),  # 7 of Spades
        tile(DECK[33], 7, 0),  # 8 of Spades
        tile(DECK[34], 8, 0),  # 9 of Spades
        tile(DECK[52], 9, 0)   # Joker
    ],
    [
        tile(DECK[15], 0, 1),  # 6 of Clubs
        tile(DECK[16], 1, 1),  # 5 of Clubs
        tile(DECK[17], 2, 1),  # 4 of Clubs
        tile(DECK[18], 3, 1),  # 3 of Clubs
        tile(DECK[19], 4, 1),  # 2 of Clubs
        tile(DECK[52], 5, 1),  # Ace of Hearts
        tile(DECK[48], 6, 1),  # King of Hearts
        tile(DECK[47], 7, 1),  # Queen of Hearts
        tile(DECK[36], 8, 1),  # 10 of Hearts
        tile(DECK[33], 9, 1)   # 10 of Spades
    ],
    [
        tile(DECK[23], 0, 2),  # 7 of Clubs
        tile(DECK[50], 1, 2),  # Ace of Spades
        tile(DECK[1], 2, 2),   # 2 of Diamonds
        tile(DECK[2], 3, 2),   # 3 of Diamonds
        tile(DECK[3], 4, 2),   # 4 of Diamonds
        tile(DECK[4], 5, 2),   # 5 of Diamonds
        tile(DECK[5], 6, 2),   # 6 of Diamonds
        tile(DECK[6], 7, 2),   # 7 of Diamonds
        tile(DECK[36], 8, 2),  # 9 of Hearts
        tile(DECK[41], 9, 2)   # Queen of Spades
    ],
    [
        tile(DECK[20], 0, 3),  # 8 of Clubs
        tile(DECK[40], 1, 3),  # King of Spades
        tile(DECK[17], 2, 3),  # 6 of Clubs
        tile(DECK[18], 3, 3),  # 5 of Clubs
        tile(DECK[19], 4, 3),  # 4 of Clubs
        tile(DECK[16], 5, 3),  # 3 of Clubs
        tile(DECK[15], 6, 3),  # 2 of Clubs
        tile(DECK[25], 7, 3),  # 8 of Diamonds
        tile(DECK[36], 8, 3),  # 8 of Hearts
        tile(DECK[40], 9, 3)   # King of Spades
    ],
    [
        tile(DECK[22], 0, 4),  # 9 of Clubs
        tile(DECK[40], 1, 4),  # Queen of Spades
        tile(DECK[15], 2, 4),  # 7 of Clubs
        tile(DECK[35], 3, 4),  # 6 of Hearts
        tile(DECK[34], 4, 4),  # 5 of Hearts
        tile(DECK[33], 5, 4),  # 4 of Hearts
        tile(DECK[32], 6, 4),  # Ace of Hearts
        tile(DECK[36], 7, 4),  # 9 of Diamonds
        tile(DECK[37], 8, 4),  # 7 of Hearts
        tile(DECK[40], 9, 4)   # Ace of Spades
    ],
    [
        tile(DECK[52], 0, 0),  # Joker
        tile(DECK[27], 1, 0),  # 2 of Spades
        tile(DECK[28], 2, 0),  # 3 of Spades
        tile(DECK[29], 3, 0),  # 4 of Spades
        tile(DECK[30], 4, 0),  # 5 of Spades
        tile(DECK[31], 5, 0),  # 6 of Spades
        tile(DECK[32], 6, 0),  # 7 of Spades
        tile(DECK[33], 7, 0),  # 8 of Spades
        tile(DECK[34], 8, 0),  # 9 of Spades
        tile(DECK[52], 9, 0)   # Joker
    ],
    [
        tile(DECK[15], 0, 1),  # 6 of Clubs
        tile(DECK[16], 1, 1),  # 5 of Clubs
        tile(DECK[17], 2, 1),  # 4 of Clubs
        tile(DECK[18], 3, 1),  # 3 of Clubs
        tile(DECK[19], 4, 1),  # 2 of Clubs
        tile(DECK[52], 5, 1),  # Ace of Hearts
        tile(DECK[48], 6, 1),  # King of Hearts
        tile(DECK[47], 7, 1),  # Queen of Hearts
        tile(DECK[36], 8, 1),  # 10 of Hearts
        tile(DECK[33], 9, 1)   # 10 of Spades
    ],
    [
        tile(DECK[23], 0, 2),  # 7 of Clubs
        tile(DECK[50], 1, 2),  # Ace of Spades
        tile(DECK[1], 2, 2),   # 2 of Diamonds
        tile(DECK[2], 3, 2),   # 3 of Diamonds
        tile(DECK[3], 4, 2),   # 4 of Diamonds
        tile(DECK[4], 5, 2),   # 5 of Diamonds
        tile(DECK[5], 6, 2),   # 6 of Diamonds
        tile(DECK[6], 7, 2),   # 7 of Diamonds
        tile(DECK[36], 8, 2),  # 9 of Hearts
        tile(DECK[41], 9, 2)   # Queen of Spades
    ],
    [
        tile(DECK[20], 0, 3),  # 8 of Clubs
        tile(DECK[40], 1, 3),  # King of Spades
        tile(DECK[17], 2, 3),  # 6 of Clubs
        tile(DECK[18], 3, 3),  # 5 of Clubs
        tile(DECK[19], 4, 3),  # 4 of Clubs
        tile(DECK[16], 5, 3),  # 3 of Clubs
        tile(DECK[15], 6, 3),  # 2 of Clubs
        tile(DECK[25], 7, 3),  # 8 of Diamonds
        tile(DECK[36], 8, 3),  # 8 of Hearts
        tile(DECK[40], 9, 3)   # King of Spades
    ],
    [
        tile(DECK[22], 0, 4),  # 9 of Clubs
        tile(DECK[40], 1, 4),  # Queen of Spades
        tile(DECK[15], 2, 4),  # 7 of Clubs
        tile(DECK[35], 3, 4),  # 6 of Hearts
        tile(DECK[34], 4, 4),  # 5 of Hearts
        tile(DECK[33], 5, 4),  # 4 of Hearts
        tile(DECK[32], 6, 4),  # Ace of Hearts
        tile(DECK[36], 7, 4),  # 9 of Diamonds
        tile(DECK[37], 8, 4),  # 7 of Hearts
        tile(DECK[40], 9, 4)   # Ace of Spades
    ],
]
    
if __name__ == "__main__":
    testCard = card(VALUE[1], SUIT[3])
    testtile = tile(testCard, 0, 0)
    print(testCard)
    print(testtile)