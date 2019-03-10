import requests
import json
from tqdm import tqdm
import colorama

from app import db
from app.models import *


def process_card(card, db):
    c = db.session.query(Card).filter(Card.uuid == card['uuid']).first()
    if c:
        if hasattr(c, 'name'):
            # Already exists and processed, skip it
            return
    else:
        c = Card(uuid=card['uuid'])
    
    # Artist
    if 'artist' in card.keys():
        artist = db.session.query(Artist).filter(Artist.name == card['artist']).first()
        if not artist:
            artist = Artist(name=card['artist'])
            db.session.add(artist)
        c.artist = artist

    # Border Color
    if 'borderColor' in card.keys():
        c.border_color = card['borderColor']

    # Color Identity
    if 'colorIdentity' in card.keys():
        for color in card['colorIdentity']:
            color = db.session.query(Color).filter(Color.abbr == color).first()
            c.color_identity.append(color)
    
    # Color Indicator
    if 'colorIndicator' in card.keys():
        for color in card['colorIndicator']:
            color = db.session.query(Color).filter(Color.abbr == color).first()
            c.color_indicator.append(color)

    # Colors
    if 'colors' in card.keys():
        for color in card['colors']:
            color = db.session.query(Color).filter(Color.abbr == color).first()
            c.colors.append(color)
    
    # Converted Mana Cost
    if 'convertedManaCost' in card.keys():
        c.converted_mana_cost = card['convertedManaCost']

    # DuelDeck
    if 'duelDeck' in card.keys():
        c.duel_deck = card['duelDeck']
    
    # faceConvertedManaCost
    if 'faceConvertedManaCost' in card.keys():
        c.face_converted_mana_cost = card['faceConvertedManaCost']

    # flavorText
    if 'flavorText' in card.keys():
        c.flavor_text = card['flavorText']

    # Foreign Data
    if 'foreignData' in card.keys():
        for foda in card['foreignData']:
            fd = ForeignData(
                language = foda['language'],
                name = foda['name'],
            )
            if 'flavorText' in foda.keys():
                fd.flavor_text = foda['flavorText']
            if 'text' in foda.keys():
                fd.text = foda['text']
            if 'multiverseId' in foda.keys():
                fd.multiverse_id = foda['multiverseId']
            if 'type' in foda.keys():
                fd.ttype = foda['type']
            db.session.add(fd)
            c.foreign_data.append(fd)

    # frameEffect
    if 'frameEffect' in card.keys():
        fe = db.session.query(FrameEffect).filter(FrameEffect.name==card['frameEffect']).first()
        if not fe:
            fe = FrameEffect(name=card['frameEffect'])
            db.session.add(fe)
        c.frame_effect = fe

    # frameVersion
    if 'frameVersion' in card.keys():
        fv = db.session.query(FrameVersion).filter(FrameVersion.name==card['frameVersion']).first()
        if not fv:
            fv = FrameVersion(name=card['frameVersion'])
            db.session.add(fv)
        c.frame_verson = fv
    
    # hand
    if 'hand' in card.keys():
        c.hand = card['hand']

    # hasFoil
    if 'hasFoil' in card.keys():
        c.has_foil = card['hasFoil']

    # hasNonFoil
    if 'hasNonFoil' in card.keys():
        c.has_non_foil = card['hasNonFoil']
        
    # isAlternative
    if 'isAlternative' in card.keys():
        c.is_alternative = card['isAlternative']

    # isFoilOnly
    if 'isFoilOnly' in card.keys():
        c.is_foil_only = card['isFoilOnly']

    # isOnlineOnly
    if 'isOnlineOnly' in card.keys():
        c.is_online_only = card['isOnlineOnly']

    # isOversized
    if 'isOversized' in card.keys():
        c.is_oversized = card['isOversized']

    # isReserved
    if 'isReserved' in card.keys():
        c.is_reserved = card['isReserved']

    # isTimeshifted
    if 'isTimeshifted' in card.keys():
        c.is_timeshifted = card['isTimeshifted']

    # layout
    if 'layout' in card.keys():
        layout = db.session.query(Layout).filter(Layout.name==card['layout']).first()
        if not layout:
            layout = Layout(name=card['layout'])
            db.session.add(layout)
        c.layout = layout
        
    # legalities
    if 'legalities' in card.keys():
        if '1v1' in card['legalities']:
            c.legal_1v1 = card['legalities']['1v1']
        if 'brawl' in card['legalities']:
            c.legal_brawl = card['legalities']['brawl']
        if 'commander' in card['legalities']:
            c.legal_commander = card['legalities']['commander']
        if 'duel' in card['legalities']:
            c.legal_duel = card['legalities']['duel']
        if 'frontier' in card['legalities']:
            c.legal_frontier = card['legalities']['frontier']
        if 'legacy' in card['legalities']:
            c.legal_legacy = card['legalities']['legacy']
        if 'modern' in card['legalities']:
            c.legal_modern = card['legalities']['modern']
        if 'standard' in card['legalities']:
            c.legal_standard = card['legalities']['standard']
        if 'vintage' in card['legalities']:
            c.legal_vintage = card['legalities']['vintage']
        if 'future' in card['legalities']:
            c.legal_future = card['legalities']['future']
        if 'pauper' in card['legalities']:
            c.legal_pauper = card['legalities']['pauper']
        if 'penny' in card['legalities']:
            c.legal_penny = card['legalities']['penny']
        if 'oldschool' in card['legalities']:
            c.legal_oldschool = card['legalities']['oldschool']
            
    # life
    if 'life' in card.keys():
        c.life = card['life']

    # loyalty
    if 'loyalty' in card.keys():
        c.loyalty = card['loyalty']

    # manaCost
    if 'manaCost' in card.keys():
        c.mana_cost = card['manaCost']

    # multiverseId
    if 'multiverseId' in card.keys():
        c.multiverse_id = card['multiverseId']

    # name
    if 'name' in card.keys():
        c.name = card['name']

    # names
    if 'names' in card.keys():
        for name in card['names']:     
            n = db.session.query(Name).filter(Name.name==name).first()
            if not n:
                n = Name(name=name)
                db.session.add(n)
            c.names.append(n)

    # number
    if 'number' in card.keys():
        c.number = card['number']

    # originalText
    if 'originalText' in card.keys():
        c.original_text = card['originalText']

    #originalType
    if 'originalType' in card.keys():
        c.original_type = card['originalType']

    #printings
    if 'printings' in card.keys():
        for code in card['printings']:
            sset = db.session.query(Set).filter(Set.code==code).first()
            if not sset:
                sset = Set(code=code)
                db.session.add(sset)
            c.printings.append(sset)

    #power
    if 'power' in card.keys():
        c.power = card['power']

    #rarity
    if 'rarity' in card.keys():
        r = db.session.query(Rarity).filter(Rarity.name==card['rarity']).first()
        c.rarity = r

    #rulings
    if 'rulings' in card.keys():
        for ruling in card['rulings']:
            r = Ruling(
                date = ruling['date'],
                text = ruling['text'],
            )
            db.session.add(r)
            c.rulings.append(r)

    #scryfallId
    if 'scryfallId' in card.keys():
        c.scryfall_id = card['scryfallId']

    #side
    if 'side' in card.keys():
        c.side = card['side']

    #starter
    if 'starter' in card.keys():
        c.starter = card['starter']

    #subtypes
    if 'subtypes' in card.keys():
        for subtype in card['subtypes']:
            subt = db.session.query(Subtype).filter(Subtype.name==subtype).first()
            if not subt:
                subt = Subtype(name=subtype)
                db.session.add(subt)
            c.subtypes.append(subt)

    #supertypes
    if 'supertypes' in card.keys():
        for supertype in card['supertypes']:
            supt = db.session.query(Supertype).filter(Supertype.name==supertype).first()
            if not supt:
                supt = Supertype(name=supertype)
                db.session.add(supt)
            c.supertypes.append(supt)

    #text
    if 'text' in card.keys():
        c.text = card['text']

    #toughness
    if 'toughness' in card.keys():
        c.toughness = card['toughness']

    #type
    if 'type' in card.keys():
        c.ttype = card['type']

    #types
    if 'types' in card.keys():
        for ttype in card['types']:
            ttyp = db.session.query(Ttype).filter(Ttype.name==ttype).first()
            if not ttyp:
                ttyp = Ttype(name=ttype)
                db.session.add(ttyp)
            c.types.append(ttyp)

    #variations
    if 'variations' in card.keys():
        for variation in card['variations']:
            # look up uuid
            v = db.session.query(Card).filter(Card.uuid == variation).first()
            if not v:
                v = Card(uuid=variation)
                db.session.add(v)
            c.variations.append(v)


    #watermark
    if 'watermark' in card.keys():
        watermark = db.session.query(Watermark).filter(Watermark.name==card['watermark']).first()
        if not watermark:
            watermark = Watermark(name=card['watermark'])
            db.session.add(watermark)
        c.watermark = watermark

    # Save
    db.session.commit()

def process_token(card, db, sset):
    c = db.session.query(Card).filter(Card.uuid == card['uuid']).first()
    if c:
        if hasattr(c, 'name'):
            # Already exists and processed, skip it
            return
    else:
        # make card (this shouldn't happen)
        process_card(card, db)
        c = db.session.query(Card).filter(Card.uuid == card['uuid']).first()

    #reverseRelated
    if 'reverseRelated' in card.keys():
        for related in card['reverseRelated']:
            r = db.session.query(Card).filter(Card.name==related).all()
            related_cards = [card for cards in r if sset in cards.printings]
            for i in related_cards:
                c.reverse_related.append(i)
    
    #save
    db.session.commit()

if __name__ == '__main__':
    colorama.init()

    # Get JSON from MTGJSON

    # standard for testing
    #results = requests.get('https://mtgjson.com/json/M19.json')
    #if results.status_code == 200:
    #    data = json.loads(results.text)

with open('AllSets.json', encoding='utf-8') as f:
    loads = json.load(f)

    # Set up colors and rarity
    colors = {'W':'White', 'B':'Black', 'R':'Red', 'U':'Blue', 'G':'Green', 'C':'Colorless'}
    rarities = ['mythic', 'rare', 'uncommon', 'common', 'basic']
    for color in colors.keys():
        find_color = db.session.query(Color).filter(Color.abbr == color).first()
        if not find_color:
            color = Color(abbr=color, name=colors[color])
            db.session.add(color)
    for rarity in rarities:
        find_rarity = db.session.query(Rarity).filter(Rarity.name == rarity).first()
        if not find_rarity:
            rarity = Rarity(name=rarity)
            db.session.add(rarity)
    db.session.commit()

    pbar_sets = tqdm(total=len(loads.keys()), position=0, desc='Sets')
    for d in loads.keys():
        pbar_sets.update(1)
        data = loads[d]
        # Create set if it doesn't exist
        s = db.session.query(Set).filter(Set.name == data['name']).first()
        if not s:
            s = db.session.query(Set).filter(Set.code == data['code']).first()
            if not s:
                s = Set(name=data['name'])
                db.session.add(s)
            # Not guaranteed to have anything else, so will use 'if x in data.keys()'
            if 'baseSetSize' in data.keys():
                s.base_set_size =  data['baseSetSize']
            if 'block' in data.keys():
                s.block = data['block']
            if 'boosterV3' in data.keys():
                # This is a list, compressing with json.dumps
                s.booster_v3 = json.dumps(data['boosterV3'])
            if 'code' in data.keys():
                s.code = data['code']
            if 'codeV3' in data.keys():
                # This is a dict, compressing with json.dumps
                s.code_v3 = data['codeV3']
            if 'isFoilOnly' in data.keys():
                s.is_foil_only = data['isFoilOnly']
            if 'isOnlineOnly' in data.keys():
                s.is_online_only = data['isOnlineOnly']
            if 'meta' in data.keys():  
                s.meta =  json.dumps(data['meta'])
            if 'mtgoCode' in data.keys():
                s.mtgo_code = data['mtgoCode']
            if 'releaseDate' in data.keys():  
                s.release_date = data['releaseDate']
            if 'totalSetSize' in data.keys():
                s.total_set_size = data['totalSetSize']
            if 'type' in data.keys():
                set_type = db.session.query(SetType).filter(SetType.name == data['type']).first()
                if not set_type:
                    t = SetType(name=data['type'])
                    db.session.add(t)
                s.set_type = set_type

        
        # Start importing cards, UUID is the only unique identifier here
        cards = data['cards']
        pbar_cards = tqdm(total=len(cards), position=1, desc=data['name']+' Cards')
        for card in cards:
            pbar_cards.update(1)
            process_card(card, db)
        
        # TOKENS
        tokens = data['tokens']
        pbar_tokens = tqdm(total=len(tokens), position=1, desc=data['name']+' Tokens')
        for card in tokens:
            pbar_cards.update(1)
            # Tokens have same traits as card, but not all of them
            process_card(card, db)
            # Run separately to get related cards
            process_token(card, db, s)

        # save
        db.session.commit()