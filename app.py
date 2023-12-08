from flask import Flask, render_template
from cards import TILES
import argparse
import json
import run

parser = argparse.ArgumentParser()
parser.add_argument('--red', type=json.loads)
parser.add_argument('--blue', type=json.loads)
parser.add_argument('--green', type=json.loads)
args = parser.parse_args()

red = args.red
blue = args.blue
green = args.green

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
        print(filename)
        return filename

@app.route('/')
def index():
    # Prepare data for the template
    print(args.red)
    print(args.blue)
    print(args.green)
    board_data = []
    for i, row in enumerate(run.TILES):
        row_data = []
        for j, tile in enumerate(row):
            card_img = get_card_image_filename(tile.card)
            occupied_color = "none"
            if (i, j) in args.red:
                occupied_color = "red"
            elif (i, j) in args.green:
                occupied_color = "green"
            elif (i, j) in args.blue:
                occupied_color = "blue"
            row_data.append((card_img, occupied_color))
        board_data.append(row_data)

    return render_template('index.html', board_data=board_data)

if __name__ == '__main__':
    app.run(debug=True)