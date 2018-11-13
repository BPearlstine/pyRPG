from playerCreation.playerCharacter import Player


class Paladin(Player):

    def __init__(self, name, strgth, dex, wis, cha):
        super().__init__(name, strgth, dex, wis, cha)
        self.setUpGear('sword')

