import re

from app.models import Deck, Card, Collection


def parse_paste(txt, col_type=Deck):
    # Parse text chunk for card names and card quantities
    # Returns dict of name : {qty: int}
    # Standard formatting is qty card_name
    # blank line
    # sideboard

    if col_type != Deck:
        board = None

    else:
        board = 'main'

    r_card = re.compile(r'(?P<qty>\d{1,2})\s+(?P<name>(\w|\s+)+)(\n|$)')

    results = {}
    
    for line in txt:

        # if blank line is detected, change board to side, only works if col_type is Deck
        if line == '' and board == 'main':
            board = 'side'

        match = r_card.match(line)
        if match:
            results[match.group('name')] = {
                'qty': int(match.group('qty')),
                'board':board
            }

    return results
