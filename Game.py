from Config import Config
from Screen import Screen
from Player import Player
from Card import Card

import json
import random
import time


class Game:

    def __init__(self):

        self.Screen = Screen()
        self.config = Config()
        self.playerlist = None

        self.turn = 0
        self.game_ended = False

        pass

    def play(self):
        self.playerlist = self.player_select()

        # Not using f-strings for compatibility
        firstplayerindex = random.randint(0, 1)
        self.Screen.display_prompt("{name} (Player {num}) goes first".format(
            name=self.playerlist[firstplayerindex].name, num=firstplayerindex))

        turn_index = firstplayerindex

        while not self.game_ended:

            self.playerlist[turn_index].turn = True
            self.playerlist[turn_index ^ 1].turn = False

            loopcompleted = False
            looperror = False

            while not loopcompleted:

                self.Screen.display_player_screen(self.playerlist, looperror)
                command_input = self.Screen.fancy_input()

                if not command_input:
                    looperror = True
                    continue

                splitargs = command_input.lower().split()
                firstarg = splitargs[0]

                if firstarg == "help":
                    commandinput = self.Screen.display_help()
                    continue

                elif firstarg == "play":
                    if len(splitargs) != 2:
                        looperror = True
                        continue
                    else:
                        index = splitargs[1]
                        self.playerlist[turn_index].play(int(index))
                        loopcompleted = True
                        continue

                elif firstarg == "quit":
                    self.Screen.clearscreen()
                    print("Thank you for playing emojic.")
                    exit()

                # else if firstarg == "attack":

            self.Screen.display_player_screen(self.playerlist)

            # Invert index (0 -> 1, 1 -> 0) with xor (1)
            turn_index = turn_index ^ 1

    def command_help(self, turn_index, error=False):

        pass

    def tick(self):
        for playernum, player in enumerate(self.playerlist):
            if player.life <= 0:
                # Line assumes two players
                self.lose(playernum)
                return False

            # Can't draw
            if len(player.deck) == 0 and player.turn:
                self.lose(playernum)
                return False

            for i, card in enumerate(player.deck):
                if not card.alive:
                    self.playerlist[playernum].graveyard.append(card)
                    self.playerlist[playernum].deck.pop(i)

            return True

    def load_cards(self):
        with open('cards.json', 'r') as cards:
            card_dict = json.load(cards)

        for c in card_dict:
            props = c.values
            self.cards.append(Card(*props))

    def player_select(self):
        self.Screen.clearscreen()
        self.Screen.clearbuffer()

        self.Screen.render_center_text("Player 1: what is your name?")
        self.Screen.refresh()

        player1_name = self.Screen.fancy_input()

        self.Screen.render_center_text("Player 2: what is your name?")
        self.Screen.refresh()

        player2_name = self.Screen.fancy_input()

        return [
            Player(player1_name, self.config),
            Player(player2_name, self.config)
        ]

    def battle(self, att_player_index, att_card_index, def_player_index, def_card_index):
        # Returns true if attack was successful

        # Can't refence specific card because
        att_player = self.playerlist[att_player_index]
        def_player = self.playerlist[def_player_index]

        attacking_deck = self.playerlist[att_player_index].deck
        defending_deck = self.playerlist[def_player_index].deck

        if attacking_deck[att_card_index].tapped:
            return False

        # Haste
        if attacking_deck.turnplayed == self.turn:
            if attacking_deck[att_card_index].ability == "Haste":
                defending_deck[def_card_index].damage(
                    attacking_deck[att_card_index])
                attacking_deck[att_card_index].damage(
                    defending_deck[def_card_index])

                return True
            else:
                # Can't attack turn it's played
                return False

        if "First strike" == attacking_deck[att_card_index].ability:
            #  First strike assumes that the attacking card will attack
            defending_deck[def_card_index].damage(
                attacking_deck[att_card_index])

            if not defending_deck[def_card_index].alive:
                return True

            else:
                attacking_deck[att_card_index].damage(
                    defending_deck[def_card_index])
                return True

        elif "Flying" == attacking_deck[att_card_index].ability:

            if "Flying" == defending_deck[def_card_index].ability:
                defending_deck[def_card_index].damage(
                    attacking_deck[att_card_index])
                attacking_deck[att_card_index].damage(
                    defending_deck[def_card_index])
                return True

            else:
                defending_player.life -= attacking_deck[att_card_index].attack
                return True

        # Defender can't attack
        elif "Defender" == attacking_deck[att_card_index].ability:
            return False

        else:
            defending_deck[def_card_index].damage(
                attacking_deck[att_card_index])
            attacking_deck[att_card_index].damage(
                defending_deck[def_card_index])

            return True
