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

card_legalities = db.Table(
    "cardlegalities",
    db.Column("card_id", db.Integer, db.ForeignKey("card.id")),
    db.Column("legality_id", db.Integer, db.ForeignKey("legality.id")),
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
)

cards_to_sideboard = db.Table(
    "cardstosideboard",
    db.Column("card_id", db.Integer, db.ForeignKey("card.id")),
    db.Column("deck_id", db.Integer, db.ForeignKey("deck.id")),
)

cards_to_feature = db.Table(
    "cardstofeature",
    db.Column("card_id", db.Integer, db.ForeignKey("card.id")),
    db.Column("deck_id", db.Integer, db.ForeignKey("deck.id")),
)

cards_to_frame_effects = db.Table(
    "cardstoframeeffects",
    db.Column("card_id", db.Integer, db.ForeignKey("card.id")),
    db.Column("frameeffect_id", db.Integer, db.ForeignKey("frameeffect.id")),
)

cards_to_frame_versions = db.Table(
    "cardstoframeversions",
    db.Column("card_id", db.Integer, db.ForeignKey("card.id")),
    db.Column("frameversion_id", db.Integer, db.ForeignKey("frameversion.id")),
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
    frame_version_id = db.Column(db.Integer, db.ForeignKey("frameversion.id"))
    frame_effect_id = db.Column(db.Integer, db.ForeignKey("frameeffect.id"))
    legalities = db.relationship(
        "Legality", secondary=card_legalities, back_populates="cards"
    )
    mana_cost = db.Column(db.String(10))
    multiverse_id = db.Column(db.Integer)
    name = db.Column(db.String(128))
    number = db.Column(db.String(6))
    original_text = db.Column(db.Text)
    original_type = db.Column(db.String(64))
    power = db.Column(db.String(32))
    printings = db.relationship(
        "Printing", secondary=card_printings, back_populates="cards"
    )
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
        "Deck", secondary=cards_to_mainboard, back_populates="cards"
    )
    sideboards = db.relationship(
        "Deck", secondary=cards_to_sideboard, back_populates="cards"
    )
    featured = db.relationship("Deck", backref="feature", lazy="dynamic")

    dueldeck = db.Column(db.String(1))
    face_converted_mana_cost = db.Column(db.Float)
    flavor_text = db.Column(db.Text)

    hand = db.Column(db.String(4))
    life = db.Column(db.String(4))
    loyalty = db.Column(db.String(4))
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
    multiverseid = db.Column(db.Integer)
    name = db.Column(db.String(128))
    text = db.Column(db.Text)
    ttype = db.Column(db.String(64))
    card_id = db.Column(db.Integer, db.ForeignKey("card.id"))


class Legality(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    cards = db.relationship(
        "Card", secondary=card_legalities, back_populates="legalities"
    )


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
    cards = db.relationship("Card", secondary=card_types, back_populates="ttypes")


class FrameEffect(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    cards = db.relationship(
        "Card", secondary=cards_to_frame_effects, back_populates="frame_effect"
    )


class FrameVersion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    cards = db.relationship(
        "Card", secondary=cards_to_frame_versions, back_populates="frame_version"
    )


class Name(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    cards = db.relationship("Card", secondary=cards_to_names, back_populates="names")


class Watermark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    cards = db.relationship("Card", backref="watermark", lazy="dynamic")


class SetType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    sets = db.relationship("Set", backref="set_type", lazy="dynamic")


class Set(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    abbr = db.Column(db.String(3), unique=True)  # abbreviation
    cards = db.relationship(
        "Card", secondary=card_printings, back_populates="printings"
    )

    base_set_size = db.Column(db.Integer)
    block = name = db.Column(db.String(128))
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
