import bcrypt

from app import db

# RELATIONSHIP TABLES
card_color_identities = db.Table(
    "cardcoloridentities",
    db.Column("card_id", db.Integer, db.ForeignKey("card.id")),
    db.Column("color_id", db.Integer, db.ForeignKey("color.id")),
)

card_colors = db.Table(
    "cardcolors",
    db.Column("card_id", db.Integer, db.ForeignKey("card.id")),
    db.Column("color_id", db.Integer, db.ForeignKey("color.id")),
)

card_color_indicator = db.Table(
    "cardcolorindicator",
    db.Column("card_id", db.Integer, db.ForeignKey("card.id")),
    db.Column("color_id", db.Integer, db.ForeignKey("color.id")),
)

card_printings = db.Table(
    "cardprintings",
    db.Column("card_id", db.Integer, db.ForeignKey("card.id")),
    db.Column("set_id", db.Integer, db.ForeignKey("set.id")),
)

card_subtypes = db.Table(
    "cardsubtypes",
    db.Column("card_id", db.Integer, db.ForeignKey("card.id")),
    db.Column("subtype_id", db.Integer, db.ForeignKey("subtype.id")),
)

card_supertypes = db.Table(
    "cardsupertypes",
    db.Column("card_id", db.Integer, db.ForeignKey("card.id")),
    db.Column("supertype_id", db.Integer, db.ForeignKey("supertype.id")),
)

card_types = db.Table(
    "cardtypes",
    db.Column("card_id", db.Integer, db.ForeignKey("card.id")),
    db.Column("ttype_id", db.Integer, db.ForeignKey("ttype.id")),
)

cards_to_mainboard = db.Table(
    "cardstomainboard",
    db.Column("card_id", db.Integer, db.ForeignKey("card.id")),
    db.Column("deck_id", db.Integer, db.ForeignKey("deck.id")),
    db.Column("quantity", db.Integer),
)

cards_to_sideboard = db.Table(
    "cardstosideboard",
    db.Column("card_id", db.Integer, db.ForeignKey("card.id")),
    db.Column("deck_id", db.Integer, db.ForeignKey("deck.id")),
    db.Column("quantity", db.Integer),
)

cards_to_feature = db.Table(
    "cardstofeature",
    db.Column("card_id", db.Integer, db.ForeignKey("card.id")),
    db.Column("deck_id", db.Integer, db.ForeignKey("deck.id")),
)

cards_to_names = db.Table(
    "cardstonames",
    db.Column("card_id", db.Integer, db.ForeignKey("card.id")),
    db.Column("name_id", db.Integer, db.ForeignKey("name.id")),
)

cards_to_variations = db.Table(
    "cardstovariations",
    db.Column("card_id", db.Integer, db.ForeignKey("card.id")),
    db.Column("variation_id", db.Integer, db.ForeignKey("card.id")),
)

cards_to_tokens = db.Table(
    "cardstotokens",
    db.Column("token_id", db.Integer, db.ForeignKey("card.id")),
    db.Column("related_id", db.Integer, db.ForeignKey("card.id")),
)

cards_to_collections = db.Table(
    "cardstocollections",
    db.Column("card_id", db.Integer, db.ForeignKey("card.id")),
    db.Column("collection_id", db.Integer, db.ForeignKey("collection.id")),
    db.Column("quantity", db.Integer),
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    collections = db.relationship("Collection", backref="owner", lazy="dynamic")

    def __repr__(self):
        return username

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password, bcrypt.gensalt(12))

    def verify_password(self, password):
        return bcrypt.checkpw(password, self.password_hash)


class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    description = db.Column(db.Text)
    comments = db.relationship("Comment")
    ratings = db.relationship("Rating")
    cards = db.relationship(
        "Card", secondary=cards_to_collections, back_populates="collections"
    )

    def __repr__(self):
        return "{} - {}".format(self.owner, self.name)


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Boolean)  # 0 = Down, 1 = Up
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    timestamp = db.Column(db.DateTime)

    # Parents
    collection_id = db.Column(db.Integer, db.ForeignKey("collection.id"))
    comment_id = db.Column(db.Integer, db.ForeignKey("comment.id"))
    deck_id = db.Column(db.Integer, db.ForeignKey("deck.id"))
    card_id = db.Column(db.Integer, db.ForeignKey("card.id"))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    timestamp = db.Column(db.DateTime)
    text = db.Column(db.Text)
    comments = db.relationship("Comment")
    ratings = db.relationship("Rating")

    # Parents
    collection_id = db.Column(db.Integer, db.ForeignKey("collection.id"))
    comment_id = db.Column(db.Integer, db.ForeignKey("comment.id"))
    deck_id = db.Column(db.Integer, db.ForeignKey("deck.id"))
    card_id = db.Column(db.Integer, db.ForeignKey("card.id"))


class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime)
    name = db.Column(db.String(64))
    description = db.Column(db.Text)
    mainboard = db.relationship(
        "Card", secondary=cards_to_mainboard, back_populates="mainboards"
    )
    sideboard = db.relationship(
        "Card", secondary=cards_to_sideboard, back_populates="sideboards"
    )
    feature_id = db.Column(db.Integer, db.ForeignKey("card.id"))
    comments = db.relationship("Comment")
    ratings = db.relationship("Rating")


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"))
    border_color = db.Column(db.String(32))
    color_identity = db.relationship("Color", secondary=card_color_identities)
    colors = db.relationship("Color", secondary=card_colors)
    color_indicator = db.relationship("Color", secondary=card_color_indicator)
    converted_mana_cost = db.Column(db.Integer)
    has_foil = db.Column(db.Boolean)
    has_non_foil = db.Column(db.Boolean)
    layout_id = db.Column(db.Integer, db.ForeignKey("layout.id"))
    layout = db.relationship("Layout")
    foreign_data = db.relationship("ForeignData")
    frame_effect_id = db.Column(db.Integer, db.ForeignKey("frameeffect.id"))
    frame_version_id = db.Column(db.Integer, db.ForeignKey("frameversion.id"))
    mana_cost = db.Column(db.String(32))
    multiverse_id = db.Column(db.Integer)
    name = db.Column(db.String(128))
    number = db.Column(db.String(6))
    original_text = db.Column(db.Text)
    original_type = db.Column(db.String(64))
    power = db.Column(db.String(32))
    printings = db.relationship("Set", secondary=card_printings, back_populates="cards")
    rarity_id = db.Column(db.Integer, db.ForeignKey("rarity.id"))
    rulings = db.relationship("Ruling")
    subtypes = db.relationship(
        "Subtype", secondary=card_subtypes, back_populates="cards"
    )
    supertypes = db.relationship(
        "Supertype", secondary=card_supertypes, back_populates="cards"
    )
    text = db.Column(db.Text)
    toughness = db.Column(db.String(32))
    ttype = db.Column(db.String(64))
    types = db.relationship("Ttype", secondary=card_types, back_populates="cards")
    uuid = db.Column(db.String(128), index=True, unique=True)
    comments = db.relationship("Comment")
    ratings = db.relationship("Rating")

    mainboards = db.relationship(
        "Deck", secondary=cards_to_mainboard, back_populates="mainboard"
    )
    sideboards = db.relationship(
        "Deck", secondary=cards_to_sideboard, back_populates="sideboard"
    )
    collections = db.relationship(
        "Collection", secondary=cards_to_collections, back_populates="cards"
    )
    featured = db.relationship("Deck", backref="feature", lazy="dynamic")

    duel_deck = db.Column(db.String(1))
    face_converted_mana_cost = db.Column(db.Float)
    flavor_text = db.Column(db.Text)

    hand = db.Column(db.String(4))
    life = db.Column(db.String(4))
    loyalty = db.Column(db.String(8))
    is_alternative = db.Column(db.Boolean)
    is_foil_only = db.Column(db.Boolean)
    is_online_only = db.Column(db.Boolean)
    is_oversized = db.Column(db.Boolean)
    is_reserved = db.Column(db.Boolean)
    is_timeshifted = db.Column(db.Boolean)
    names = db.relationship("Name", secondary=cards_to_names, back_populates="cards")
    scryfall_id = db.Column(db.String(128))
    side = db.Column(db.String(1))
    starter = db.Column(db.Boolean)

    variations = db.relationship(
        "Card",
        secondary=cards_to_variations,
        primaryjoin=(cards_to_variations.c.card_id == id),
        secondaryjoin=cards_to_variations.c.variation_id == id,
        backref=db.backref("alternates", lazy="dynamic"),
        lazy="dynamic",
    )

    watermark_id = db.Column(db.Integer, db.ForeignKey("watermark.id"))

    reverse_related = db.relationship(
        "Card",
        secondary=cards_to_tokens,
        primaryjoin=(cards_to_tokens.c.token_id == id),
        secondaryjoin=cards_to_tokens.c.related_id == id,
        backref=db.backref("tokens", lazy="dynamic"),
        lazy="dynamic",
    )

    # Legalities
    legal_1v1 = db.Column(db.String(32))
    legal_brawl = db.Column(db.String(32))
    legal_commander = db.Column(db.String(32))
    legal_duel = db.Column(db.String(32))
    legal_frontier = db.Column(db.String(32))
    legal_legacy = db.Column(db.String(32))
    legal_modern = db.Column(db.String(32))
    legal_standard = db.Column(db.String(32))
    legal_vintage = db.Column(db.String(32))
    legal_future = db.Column(db.String(32))
    legal_pauper = db.Column(db.String(32))
    legal_penny = db.Column(db.String(32))
    legal_oldschool = db.Column(db.String(32))


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    cards = db.relationship("Card", backref="artist", lazy="dynamic")


class Color(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    abbr = db.Column(db.String(1), unique=True)  # abbreviation
    symbol = db.Column(db.String(8), unique=True)


class Layout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)


class ForeignData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(64))
    multiverse_id = db.Column(db.Integer)
    name = db.Column(db.String(128))
    text = db.Column(db.Text)
    ttype = db.Column(db.String(64))
    card_id = db.Column(db.Integer, db.ForeignKey("card.id"))
    flavor_text = db.Column(db.Text)


class Rarity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    cards = db.relationship("Card", backref="rarity", lazy="dynamic")


class Ruling(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    text = db.Column(db.Text)
    card_id = db.Column(db.Integer, db.ForeignKey("card.id"))


class Subtype(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    cards = db.relationship("Card", secondary=card_subtypes, back_populates="subtypes")


class Supertype(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    cards = db.relationship(
        "Card", secondary=card_supertypes, back_populates="supertypes"
    )


class Ttype(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    cards = db.relationship("Card", secondary=card_types, back_populates="types")


class FrameEffect(db.Model):
    __tablename__ = "frameeffect"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    cards = db.relationship("Card", backref="frame_effect", lazy="dynamic")


class FrameVersion(db.Model):
    __tablename__ = "frameversion"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    cards = db.relationship("Card", backref="frame_version", lazy="dynamic")


class Name(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    cards = db.relationship("Card", secondary=cards_to_names, back_populates="names")


class Watermark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    cards = db.relationship("Card", backref="watermark", lazy="dynamic")


class SetType(db.Model):
    __tablename__ = "settype"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    sets = db.relationship("Set", backref="set_type", lazy="dynamic")


class Set(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    cards = db.relationship(
        "Card", secondary=card_printings, back_populates="printings"
    )

    base_set_size = db.Column(db.Integer)
    block = db.Column(db.String(128))
    booster_v3 = db.Column(db.Text)
    code = db.Column(db.String(8))
    code_v3 = db.Column(db.String(32))
    is_foil_only = db.Column(db.Boolean)
    is_online_only = db.Column(db.Boolean)
    meta = db.Column(db.String(64))
    mtgo_code = db.Column(db.String(32))
    release_date = db.Column(db.String(32))
    total_set_size = db.Column(db.Integer)
    set_type_id = db.Column(db.Integer, db.ForeignKey("settype.id"))


class DBInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    md5 = db.Column(db.String(128))
    completed = db.Column(db.Boolean, default=False)
