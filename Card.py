import random
import ScreenTools

class Card:
    #   I was considering implementing cards with heavy OOP, maybe using multiple inheritance,
    #   but since moves/priority (first strike) in this game are decided at run time and
    #   a card's battle methods have to modify both cards' states, (i.e. two person battles),
    #   I'd rather just have a list of abilities or something.

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

        self.tapped = False

        self.player = None

        pass

    def damage(self, thingwithlife):
        damage_number = self.attack

        # Thank you dynamic typing, very cool
        thingtype = type(thingwithlife)

        # I can't just make two methods with common signatures for both because
        # I need to set the card alive state to false if it dies
        if thingtype == Card:
            if damage_number >= thingwithlife.defense:
                thingwithlife.alive = False
        elif thingtype == Player:
            thingwithlife.life -= damage_number

            # Assuming no trample for now

            # if self.ability == "trample":
            #     playerdamage = self.defense - damage_number
            # else:
            #     playerdamage = 0
            # return playerdamage

        # return alive
        
        pass

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


        card_tapped_mask = [["\   "],
                            [" \\"],
                            ["  \\"],
                            ["   \\"]]


        for i, line in enumerate(card_template):
            if type(line) == list:
                # and len(line) == 0:
                card_template[i] = self.render_card_line(*line)

            card_template[i] = list(card_template[i])

        if self.tapped:
            maskx = len(card_template[0]) - len(card_tapped_mask[0])
            card_template = ScreenTools.render_array_in_array(card_template, card_tapped_mask, maskx, 0)

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

    def battle(self, def_card, turn):
        # Haste

        if len(def_card.player.battlefield) == 0:
            self.damage(def_card.player)

        if self.turnplayed == turn:
            if self.ability == "Haste":
                self.damage(def_card)
                def_card.damage(self)
            else:
                # Can't attack turn it's played
                return "Card can't attack turned played"

        if "First strike" == self.ability:
            #  First strike assumes that the attacking card will attack
            self.damage(def_card)

            if def_card.alive:
                def_card.damage(self)

        elif "Flying" == self.ability:
            if "Flying" == def_card.ability:
                self.damage(def_card)
                def_card.damage(self)

            else:
                def_card.player.life -= self.attack

        # Defender can't attack
        elif "Defender" == self.ability:
            return "Defender cards can't attack"

        else:
            self.damage(def_card)
            def_card.damage(self)

        self.tapped = True
        return True

