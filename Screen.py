import os

class Screen:
    def __init__(self):

        self.height, self.width = [int(dim) for dim in os.popen('stty size', 'r').read().split()]

        # Add spaces at bottom for input
        self.height -= 4
        # self.width = 130

        self.screen = self.generate_screen_buffer(self.height, self.width)

        pass

    def render(self):
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
                (_______/|/     \|(_______)(_______)\_______/(_______/  """)
        print("")
        print( "                   The Refactoring")
        print("\n\n")
        input("                Press Enter to continue")


    # Polymorphism for screen as well as utility functions for subrendering.


    def render_array(self, input_array, startx, starty):
        for y in range(len(input_array)):
            for x in range(len(input_array[0])):
                self.screen[starty + y][startx + x] = input_array[y][x]

        pass
    
    def render_text(self, text, x, y):
        # x, y - start coordinates of text
        # Assuming horizontal test
        self.render_array([list(text)], x, y)

        pass


    def render_center_text(self, text):
        y = self.height // 2
        x = (self.width // 2) - (len(text) // 2)

        # x, y - start coordinates of text
        # Assuming horizontal test

        self.render_array([list(text)], x, y)
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





