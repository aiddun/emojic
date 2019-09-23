import os
from Card import Card

class Screen:
    def __init__(self):

        self.height, self.width = [int(dim) for dim in os.popen('stty size', 'r').read().split()]

        # Add spaces at bottom for input
        self.height -= 4
        # self.width = 130

        self.screen = self.generate_screen_buffer(self.height, self.width)

        pass

    def refresh(self):
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
        print("   Welcome to")
        print("""
                 _______  _______  _______  _______ _________ _______   
                (  ____ \(       )(  ___  )(  ____ \\__   __/(  ____ \  
                | (    \/| () () || (   ) || (    \/   ) (   | (    \/  
                | (__    | || || || |   | || |         | |   | |        
                |  __)   | |(_)| || |   | || | ____    | |   | |        
                | (      | |   | || |   | || | \_  )   | |   | |        
                | (____/\| )   ( || (___) || (___) |___) (___| (____/   
                (_______/|/     \|(_______)(_______)\_______/(_______/  
                     🤽‍♀️       🐌      🚴‍       🦄       🤠      👩‍🔬 """)
        print("")
        print( "                   The Refactoring")
        print("\n\n")
        input("                Press Enter to continue")


    # Polymorphism for screen as well as utility functions for subrendering.


    def render_array_to_screen(self, input_array, startx, starty):
        for y in range(len(input_array)):
            for x in range(len(input_array[0])):
                self.screen[starty + y][startx + x] = input_array[y][x]

        pass
    
    def render_text(self, text, x, y):
        # x, y - start coordinates of text
        # Assuming horizontal test
        self.render_array_to_screen([list(text)], x, y)

        pass


    def render_center_text(self, text, ymargin = 0):
        # Allow for centered text above or below the absolute center
        y = self.height // 2 + ymargin
        x = (self.width // 2) - (len(text) // 2)

        # x, y - start coordinates of text
        # Assuming horizontal test

        for linenum, line in enumerate(text.split('\n')):
            self.render_array_to_screen([list(line)], x, y + linenum)


        pass

    def fancy_input(self):

        return input((self.width // 2 - 10) * " " +  " ━☆ﾟ    ")


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

    def display_player_screen(self, playerlist: list, error=False):
        self.clearscreen()
        self.clearbuffer()


        for player in playerlist:
            if player.turn:
                hand_view = player.render_cards(player.hand)
                self.render_array_to_screen(hand_view, 0, self.height - Card.height - 4)

                battlefield_view = player.render_cards(player.battlefield)

                # Only try to render battlefield view if there is one (cards on battlefield)
                if battlefield_view:
                    # Calculate offset for battlefield 6 spaces after the hand before rendering battlefields
                    battlefield_x_offset = self.width - len(battlefield_view[0]) - 1 - 5

                    self.render_array_to_screen(battlefield_view, battlefield_x_offset, self.height - Card.height - 4)

            elif not player.turn:
                battlefield_view = player.render_cards(player.battlefield)

                # Only try to render battlefield view if there is one (cards on battlefield)
                if battlefield_view:
                    battlefield_x_offset = self.width - len(battlefield_view[0]) - 1 - 5

                    self.render_array_to_screen(battlefield_view, battlefield_x_offset, 3)

        # player1view = playerlist[0].render(player1turn)
        # self.render_array_to_screen(player1view, , 0)

        # self.Screen.render_array_to_screen(playerlist[1].render(True))


        if error:
            self.render_center_text("invalid command. please try again or enter 'help' for command help", self.height // 2 - 1)
        else:
            self.render_center_text("enter 'help' for command help", self.height // 2 - 1)

        self.refresh()

        pass

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

        helptext = \
        """
        Help:

        \033[1mAttacking:\033[0m

        play:
        \x1B[3m summons card to battlefield with mana\x1B[23m
        play {card number}

        fight:
        \x1B[3m attacks opponent with card \x1B[23m
        attack {card number} 

        \033[1mDefending:\033[0m

        block:
        \x1B[3m block player attack with card \x1B[23m
        block {card number}



        press ENTER to continue
        """


        self.render_center_text(helptext)
        self.refresh()

        pass





