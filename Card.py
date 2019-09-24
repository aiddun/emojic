import random


class Card:

    #   I was considering implementing cards with heavy OOP, maybe using multiple inheritance, but since moves/priority in this game are decided at run time (i.e. two person battles), I'd rather just have a list of abilities or something.

    # Static render information
    height = 16
    width = 22

    def __init__(self, name: str, emoji1: str, emoji2: str, color: str, mana: int, attack: int, defense: int, rarity: str, ability, turnplayed=-1):

        # Final
        if emoji2 == "":
            self.name = emoji1
        else:
            self.name = [emoji1, emoji2][random.randint(0, 1)]

        self.mana = mana
        self.attack = attack
        self.defense = defense
        self.rarity = rarity
        # Assuming single ability per card

        # Modifiable states
        self.ability = ability
        self.alive = True
        self.turnplayed = turnplayed

        tapped = False

        pass

    def damage(self, damaging_card):
        damage_number = damage_number.attack

        if damage_number >= self.defense:
            self.alive = False

            # Assuming no trample for now

            # if self.ability == "trample":
            #     playerdamage = self.defense - damage_number
            # else:
            #     playerdamage = 0
            # return playerdamage

        # return alive

    def render(self, index):
        attdef = str(self.attack) + "/" + str(self.defense)

        card_template = ["  __________________ ",
                         " /                  \\",
                         [self.rarity, "left"],
                         ["", ""],
                         ["", ""],
                         [self.name, "center", True],
                         ["", ""],
                         ["", ""],
                         ["", ""],
                         ["", ""],
                         [self.ability, "center"],
                         ["", ""],
                         ["", ""],
                         ["", ""],
                         [str(index), "leftright", False, attdef],
                         " \\___________________/"
                         ]

        for i, line in enumerate(card_template):
            if type(line) == list:
                # and len(line) == 0:
                card_template[i] = self.render_card_line(*line)

            card_template[i] = list(card_template[i])

# f""""___________________
# /                {self.rarity}   \\
# |                     |
# |                     |
# |         {self.name}        |
# |                     |
# |                     |
# |                     |
# |                     |
# |         {self.ability}           |
# |                     |
# |                     |
# |                     |
# |               {attdef}      |
# \\___________________/"""

        return card_template

    def render_card_line(self, text: str, position: str, emoji=False, optleft=" "):
        # Could be faster with fixed-length arrays but this is more legible and it's neglegable at this scale

        if emoji:
            # Problem with emoji text inferences in Python
            textlen = 1
        else:
            textlen = len(text)

        if position == "center":
            output = "|"
            output += " " * ((self.width // 2) - (textlen // 2 + 1) - 1)
            output += str(text)
            output += " " * (self.width - len(output) - 1)
            output += "|"

        elif position == "left":
            output = "|   "
            output += str(text)
            output += " " * (self.width - len(output) - 1)
            output += "|"

        elif position == "right":
            output = "|"
            output += " " * (self.width - 1 - 1 - textlen)
            output += str(text)
            output += " " * 1
            output += "|"

        elif position == "leftright":
            output = "|  "
            output += str(text)
            output += " " * (self.width - 1 - 1 - textlen - len(optleft) - 2)
            output += str(optleft)
            output += " " * 1
            output += "|"

        elif position == "" and text == "":
            output = "|"
            output += " " * (self.width - 3)
            output += "|"

        else:
            print("Error: Something went wrong.")
            exit()

        return output
