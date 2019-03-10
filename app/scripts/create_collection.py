from app.models import Collection, Card, Deck
from app import db
from .utilities import parse_paste

def get_cards():
    print('Paste cards: ')
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break
    return lines

if __name__ == '__main__':
    not_found = []
    print('Create a new (D)eck or (C)ollection?')
    ans = input().lower()
    if ans == 'd':
        cards = parse_paste(get_cards(), Deck)
        deck = Deck(name=input('Deck Name: '))
        db.session.add(deck)
        
        for card in cards.keys():
            c = db.session.query(Card).filter(Card.name==card).first()
            if not c:
                not_found.append(card)
                continue
            if cards[card]['board'] == 'main':
                for _ in range(cards[card]['qty']):
                    deck.mainboard.append(c)
            elif cards[card]['board'] == 'side':
                for _ in range(cards[card]['qty']):
                    deck.sideboard.append(c)
                
    elif ans == 'c':
        cards = parse_paste(get_cards(), Collection)
        collection = Collection(name=input('Collection Name: '))
        db.session.add(collection)

        for card in cards.keys():
            c = db.session.query(Card).filter(Card.name==card).first()
            if not c:
                not_found.append(card)
                continue
            for _ in range(cards[card]['qty']):
                collection.cards.append(c)
                    
    else:
        print('Invalid response.')
    
    db.session.commit()
    print('Unable to find the following cards:\n{}'.format('\n'.join(set(not_found))))
        

    
    
