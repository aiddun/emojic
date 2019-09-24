from Card import Card
import random
import ScreenTools


class Player:

    def __init__(self, name: str, config):
        self.name = name
        self.gameconfig = config

        # Could represent deck as a stack but chose not to in case I ever want to implement bottom of deck ability
        self.deck = []
        self.hand = []
        self.battlefield = []
        self.graveyard = []

        self.life = 20
        self.spacesize = 4

        self.generate_deck()
        self.generate_hand()

        self.turn = False

        self.max_mana = 1
        self.spendable_mana = 1

        pass

    def begin_turn(self):
        self.draw()

        self.max_mana += 1
        self.spendable_mana = self.max_mana

    def play(self, index):
        self.battlefield.append(self.hand[index])
        self.hand.pop(index)

    def draw(self):
        topcard = self.deck[-1]
        self.hand.append(topcard)

        self.deck.pop()

    def damage(damage_num: int):
        self.life -= damage_num

        pass

    def generate_hand(self):
        for i in range(self.gameconfig.handsize):
            self.draw()

            pass

    def generate_deck(self):
        for card in self.gameconfig.cards:
            for cardfreq in range(self.gameconfig.rarity_config[card.rarity]):
                self.deck.append(card)
                random.shuffle(self.deck)

                pass

    def render_cards(self, cards, startval=0):

        cardnum = len(cards)

        if not cardnum:
            return

        renderwidth = (cardnum * Card.width) + (self.spacesize * (cardnum - 1))
        renderheight = Card.height + 2

        player_screen_buffer = ScreenTools.generate_screen_buffer(
            renderheight, renderwidth + 1)

        currentx = 2
        currenty = 1

        handsize = len(self.hand)

        for i, card in enumerate(self.hand):
            player_screen_buffer = ScreenTools.render_array_in_array(
                player_screen_buffer, card.render(i + startval), currentx, currenty)

            if not i >= handsize - 1:
                currentx += Card.width + self.spacesize

        # Render player health

        return player_screen_buffer

    # def
    #     healthtext = "Health:  {}".format(self.life)

    #     if turn:
    #         player_screen_buffer = ScreenTools.render_text(player_screen_buffer, healthtext, renderwidth, renderheight - 2)
    #     else:
    #         player_screen_buffer = ScreenTools.render_text(player_screen_buffer, healthtext, renderwidth - 10, 0)
