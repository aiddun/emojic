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

            loop_completed = False
            loop_error = False

            error_text = ""

            while not loop_completed:

                self.Screen.display_player_screen(self.playerlist, loop_error, error_text)
                command_input = self.Screen.fancy_input()

                if not command_input:
                    loop_error = True
                    continue

                splitargs = command_input.lower().split()
                firstarg = splitargs[0]

                if firstarg == "help":
                    commandinput = self.Screen.display_help()

                elif firstarg == "play":
                    if len(splitargs) != 2:
                        loop_error = True
                        error_text = "play accepts 1 argument"
                        continue
                    else:
                        index = splitargs[1]

                        if not self.is_int(index):
                            loop_error = True
                            error_text = "invalid card index type"
                            continue
                        else:
                            index = int(index)

                        loop_completed = self.playerlist[turn_index].play(index)

                elif firstarg == "battle":
                    if len(splitargs) != 3:
                        loop_error = True
                        error_text = "battle accepts 2 arguments"
                    continue

                    att_index = splitargs[1]
                    if not self.is_int(att_index):
                        loop_error = True
                        error_text = "invalid card index type"
                        continue

                    att_index = int(att_index)

                    def_index = splitargs[2]
                    if not self.is_int(def_index):
                        loop_error = True
                        error_text = "invalid card index type"
                        continue

                    def_index = int(def_index)

                    current_player_hand_len = len(self.playerlist[turn_index].hand)
                    current_player_battlefield_len = len(self.playerlist[turn_index].battlefield)

                    current_player_start_index = current_player_hand_len
                    current_player_end_index = current_player_start_index + current_player_battlefield_len + 1

                    if not (current_player_start_index <= att_index and att_index <= current_player_end_index):
                        loop_error = True
                        error_text = "invalid attacking card index"
                        continue

                    other_player_battlefield_len = len(self.playerlist[int(not turn_index)].battlefield)

                    other_player_start_index = current_player_end_index
                    other_player_end_index = other_player_start_index + other_player_battlefield_len + 1

                    if not (other_player_start_index <= def_index and def_index < other_player_end_index):
                        loop_error = True
                        error_text = "invalid defending card index"
                        continue

                    att_card = self.playerlist[turn_index].battlefield[att_index - current_player_start_index]
                    def_card = self.playerlist[self.other_player(turn_index)].battlefield[def_index - other_player_start_index]

                    battleresult = att_card.battle(def_card)
                    if battleresult == True:
                        loop_completed == True
                    else:
                        error_text = battleresult

                    exit()
                elif firstarg == "quit":
                    self.Screen.clearscreen()
                    print("Thank you for playing emojic.")
                    exit()

                else:
                    loop_error = True
                    continue

                # Refresh board and check if any cards have died or players have lost
                player_lost = self.tick()

                if player_lost:
                    self.Screen.clearscreen()
                    winner_index = self.other_player(player_lost)
                    self.screen.render_center_text("Player {num} ({name}) wins!".format(num=winner_index, name=self.playerlist[winner_index].name))
                    print("Thank you for playing emojic.")
                    exit()


                # else if firstarg == "attack":

            self.Screen.display_player_screen(self.playerlist)

            # Invert index (0 -> 1, 1 -> 0) with xor (1)
            turn_index = turn_index ^ 1

    def other_player(self, i):
        return i ^ 1

    def command_play(self, args):
        pass

    def is_int(self, thing):
        try:
            _ = int(thing)
        except ValueError:
            return False
        else:
            return True


    def tick(self):
        for playernum, player in enumerate(self.playerlist):
            if player.life <= 0:
                # Line assumes two players
                self.lose(playernum)
                return playernum

            # Can't draw
            if len(player.deck) == 0 and player.turn:
                self.lose(playernum)
                return playernum

            for i, card in enumerate(player.deck):
                if not card.alive:
                    self.playerlist[playernum].graveyard.append(card)
                    self.playerlist[playernum].deck.pop(i)

            return 0

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
