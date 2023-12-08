from flask import Flask, render_template
from cards import TILES
import argparse
import json
import run

parser = argparse.ArgumentParser()
parser.add_argument('--red', type=json.loads)
parser.add_argument('--blue', type=json.loads)
parser.add_argument('--green', type=json.loads)
parser.add_argument('--red_cards', type=json.loads)
parser.add_argument('--blue_cards', type=json.loads)
parser.add_argument('--green_cards', type=json.loads)
args = parser.parse_args()

red = args.red
blue = args.blue
green = args.green

red_cards = args.red_cards
blue_cards = args.blue_cards
green_cards = args.green_cards

app = Flask(__name__)

def get_card_image_filename(card):
    card_str = str(card)  # Get the string representation of the card
    if "joker" in card_str.lower():
        return 'red_joker.png'  # Assuming joker image is named 'red_joker.png'
    else:
        # Extract value and suit from the card string
        parts = card_str.split(' ')
        value = parts[4] if parts[4] != 'a' else 'ace'  # Convert 'a' to 'ace'
        suit = parts[-1]
        if suit.endswith('s'):
            suit = suit[:-1]  # Remove trailing 's' from suit

        if value in ["king", "queen", "jack"]:
            value += '2'  # Add '2' at the end for King, Queen, and Jack
        
        filename = f"{value}_of_{suit}s.png"  # Construct filename
        return filename

@app.route('/')
def index():
    # Prepare data for the template
    board_data = []
    red_card_positions = set((x, y) for x, y in red_cards)
    blue_card_positions = set((x, y) for x, y in blue_cards)
    green_card_positions = set((x, y) for x, y in green_cards)

    for i, row in enumerate(TILES):
        row_data = []
        for j, tile in enumerate(row):
            card_img = get_card_image_filename(tile.card)
            occupied_color = None

            if [i, j] in red:
                occupied_color = "red"
            elif [i, j] in blue:
                occupied_color = "blue"
            elif [i, j] in green:
                occupied_color = "green"

            can_play = ""
            if (i, j) in red_card_positions:
                can_play = "can-play-red"
            elif (i, j) in blue_card_positions:
                can_play = "can-play-blue"
            elif (i, j) in green_card_positions:
                can_play = "can-play-green"

            row_data.append((card_img, occupied_color, can_play))
        board_data.append(row_data)

    return render_template('index.html', board_data=board_data)

if __name__ == '__main__':
    app.run(debug=True)