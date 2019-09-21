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
        self.graveyard = []

        self.life = 20
        self.spacesize = 4

        self.generate_deck()
        self.generate_hand()
    
        pass

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


    def render(self, turn: bool):

        handsize = len(self.hand)

        if not handsize:
            return

        renderwidth  = (handsize * Card.width) + (self.spacesize * (handsize - 1))
        renderheight = Card.height + 2


        player_screen_buffer = ScreenTools.generate_screen_buffer(renderheight, renderwidth + 1)

        currentx = 2
        currenty = 1

        for i, card in enumerate(self.hand):
            # print(f"i: {i}")

            player_screen_buffer = ScreenTools.render_array_in_array(player_screen_buffer, card.render(), currentx, currenty)
            currentx += Card.width + self.spacesize

        # Render player health
        healthtext = "Health:  {}".format(self.life)

        if turn:
            player_screen_buffer = ScreenTools.render_text(player_screen_buffer, healthtext, 3, renderheight - 2)
        else:
            player_screen_buffer = ScreenTools.render_text(player_screen_buffer, healthtext, renderwidth - 10, 0)        

        return player_screen_buffer