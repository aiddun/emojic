import os
from Card import Card


class Screen:
    def __init__(self):

        self.height, self.width = [
            int(dim) for dim in os.popen('stty size', 'r').read().split()]
        # Add spaces at bottom for input
        self.height -= 4

        self.screen = self.generate_screen_buffer(self.height, self.width)

        with open("help.txt", 'r') as helptxt:
            # Repr -> read raw text including fancy optional formatting
            self.helptext = helptxt.read()

        pass

    def refresh(self):

        # Get new screen size, if there is one
        # Code from StackOverflow
        self.height, self.width = [
        int(dim) for dim in os.popen('stty size', 'r').read().split()]

        self.height -= 4

        self.clearscreen()
        for line in self.screen:
            print(''.join(line))

        pass

    def clearscreen(self):

        # method and os names from from geeksforgeeks.com
        # for windows
        if os.name == 'nt':
            _ = os.system('cls')

            # for mac and linux(here, os.name is 'posix')
        else:
            _ = os.system('clear')

        pass

    def clearbuffer(self):
        self.screen = self.generate_screen_buffer(self.height, self.width)

    def splash_screen(self):
        self.clearscreen()

        # Vanity, might not convert this to screen api
        self.render_center_text("Welcome to", -7)
        self.render_center_text("""
 _______  _______  _______  _______ _________ _______   
(  ____ \(       )(  ___  )(  ____ \\__   __/(  ____ \  
| (    \/| () () || (   ) || (    \/   ) (   | (    \/  
| (__    | || || || |   | || |         | |   | |        
|  __)   | |(_)| || |   | || | ____    | |   | |        
| (      | |   | || |   | || | \_  )   | |   | |        
| (____/\| )   ( || (___) || (___) |___) (___| (____/   
(_______/|/     \|(_______)(_______)\_______/(_______/  
  🤽‍♀️       🐌      🚴‍       🦄       🤠      👩‍🔬 """, -6)
        self.render_center_text("The Refactoring", 5)
        self.render_center_text("Press Enter to continue", 8)

        self.refresh()
        input()

    def render_array(self, input_array, startx, starty):
        for y in range(len(input_array)):
            if starty + y >= len(self.screen) - 1:
                continue

            for x in range(len(input_array[0])):
                if startx + x >= len(self.screen[0]) - 1:
                    continue

                self.screen[starty + y][startx + x] = input_array[y][x]

        pass

    def render_text(self, text, x, y):
        # x, y - start coordinates of text
        # Assuming horizontal test
        self.render_array([list(text)], x, y)

        pass

    def render_center_text(self, text, ymargin=0, valign=False):
        # Allow for centered text above or below the absolute center

        splittext = text.splitlines()

        if valign:
            y = (self.height // 2) - (len(splittext) // 2)
        else: 
            y = self.height // 2 + ymargin 

        # x, y - start coordinates of text
        # Assuming horizontal test

        for linenum, line in enumerate(splittext):
            x = (self.width // 2) - (len(line) // 2)
            self.render_array([list(line)], x, y + linenum)

        pass

    def fancy_input(self):

        return input((self.width // 2 - 10) * " " + " ━☆ﾟ    ")

    def generate_screen_buffer(self, height, width):
        #   Using native lists to minimise dependencies
        screenbuffer = []
        # Row
        for i in range(height):
            screenbuffer.append([])
            # Column
            for j in range(width):
                screenbuffer[i].append(" ")

        return screenbuffer

    # def player_select_screen(self):

    #     playernum = 2
    #     players = []

    #     for i in range(players):


    def display_player_screen(self, playerlist: list, error=False, error_text=""):
        self.clearscreen()
        self.clearbuffer()

        # Keep track of an index such that we can map each card to an index on the board
        cardindexoffset = 0

        # Render current player first so index format is always consistant
        for i, player in enumerate(playerlist):
            if player.turn:
                cardindexoffset = self.render_current_player(player, cardindexoffset)
                break

        otherplayerindex = i ^ 1

        self.render_other_player(playerlist[otherplayerindex], cardindexoffset)

        # player1view = playerlist[0].render(player1turn)
        # self.render_array(player1view, , 0)

        # self.Screen.render_array(playerlist[1].render(True))

        if error:
            self.render_center_text(
                "invalid command. please try again or enter 'help' for command help", self.height // 2 - 1)
        else:
            self.render_center_text(
                "enter 'help' for command help", self.height // 2 - 1)

        if error_text:
            self.render_center_text(error_text, (self.height // 2) - 2)

        self.refresh()

        pass

    def render_current_player(self, player, cardindexoffset):
        # Render hand
        hand_view = player.render_cards(player.hand, cardindexoffset)
        self.render_array(hand_view, 0, self.height - Card.height - 4)

        # Keep track of an index such that we can map each card to an index on the board
        cardindexoffset += len(player.hand)

        # Add hand caption
        self.render_text("Hand", len(
            hand_view[0]) // 2, self.height - 3)
        self.render_text("{}".format(player.name), len(
            hand_view[0]) // 2, self.height - 2)

        # Render current player battlefield
        battlefield_view = player.render_cards(
            player.battlefield, cardindexoffset)

        # Only try to render battlefield view if there is one (cards on battlefield)
        if battlefield_view:
            # Calculate offset for battlefield 6 spaces after the hand before rendering battlefields
            battlefield_x_offset = self.width - len(battlefield_view[0]) - 1 - 10
            self.render_array(
                battlefield_view, battlefield_x_offset, self.height - Card.height - 4)
            cardindexoffset += len(player.battlefield)

        return cardindexoffset

    def render_other_player(self, player, cardindexoffset):
        battlefield_view = player.render_cards(
            player.battlefield, cardindexoffset)

        # Only try to render battlefield view if there is one (cards on battlefield)
        if battlefield_view:
            battlefield_x_offset = self.width - \
                                   len(battlefield_view[0]) - 1 - 10
            self.render_array(battlefield_view,
                              battlefield_x_offset, 3)
            cardindexoffset += len(player.battlefield)

        return cardindexoffset

    def display_prompt(self, prompt_text):
        self.clearscreen()
        self.clearbuffer()

        self.render_center_text(prompt_text)
        self.render_center_text("Press ENTER to Continue", 4)

        self.refresh()

        input()

        pass

    def display_help(self):
        self.clearscreen()
        self.clearbuffer()

        self.render_center_text(self.helptext, None, valign=True)
        self.refresh()
        input()

        pass
