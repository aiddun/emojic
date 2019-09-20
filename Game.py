from Config import Config
from Screen import Screen
from Player import Player
from Card   import Card

import json

class Game:

    def __init__(self):
        
        self.turn = 0

        self.Screen = Screen()
        self.Screen.splash_screen()

        self.config = Config()

        playerlist = self.player_select()

        self.Screen.clearscreen()
        self.Screen.clearbuffer()
        player1view = playerlist[0].render(True)
        self.Screen.render_array(player1view, 0, Card.height + 1)
        player2view = playerlist[0].render(False)
        self.Screen.render_array(player2view, self.Screen.width - len(player2view[0]) - 1 - 5, 0)

        # self.Screen.render_array(playerlist[1].render(True))
        self.Screen.render()

        self.Screen.fancy_input()

        pass


    def load_cards(self):
        with open('cards.json', 'r') as cards:
            card_dict = json.load(cards)

        for c in card_dict:
            props = c.values
            self.cards.append(Card(*props))


    def player_select(self):
        self.Screen.clearscreen()

        self.Screen.render_center_text("Player 1: what is your name?")
        self.Screen.render()

        player1_name = self.Screen.fancy_input()

        self.Screen.render_center_text("Player 2: what is your name?")
        self.Screen.render()

        player2_name = self.Screen.fancy_input()

        return [
            Player(player1_name, self.config), 
            Player(player2_name, self.config)
            ]





    def battle(self, attacking_card_player, attacking_card_index, defending_player, defending_card_index):
        # Assuming no encapsulation
        attacking_card = attacking_card_index.deck[attacking_card_index]
        defending_card = defending_card_index.deck[defending_card_index]

        # Haste
        if attacking_card.turnplayed == self.turn:
            if attacking_card.ability == "Haste":
                battle_standard(attacking_card_index, attacking_card_index, defending_player, defending_card_index)

                return True


        if "First strike" == attacking_card.ability:
            #  First strike assumes that the attacking card will attack 
            defending_card.damage()

            if not defending_card.alive:
                return True

        elif "Flying" == attacking_card.ability:
            
            if "Flying" == defending_card.ability:
                battle_standard(attacking_card_index, attacking_card_index, defending_player, defending_card_index)



        # Defender can't attack

        else:
            battle_standard(attacking_card_index, attacking_card_index, defending_player, defending_card_index)
    

    # def battle_standard(self, attacking_player, attacking_card_index, defending_player, defending_card_index):





