import json
from Card import Card


class Config:

    handsize = 3

    rarity_config = {
        "Low": 3,
        "Medium": 2,
        "Rare": 1,
    }

    def __init__(self):
        self.cards = []
        self.load_cards()

        pass

    def load_cards(self):
        with open('cards.json', 'r') as cards:
            card_dict = json.load(cards)

        for c in card_dict:
            props = c.values()
            self.cards.append(Card(*props))

        pass
