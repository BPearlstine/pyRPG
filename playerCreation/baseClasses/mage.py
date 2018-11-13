from playerCreation.playerCharacter import Player


class Mage(Player):

    def __init__(self, name, strgth, dex, wis, cha):
        super().__init__(name, strgth, dex, wis, cha)
        self.actions.append('spells')
        self.setUpGear('dagger')
        self.addMagic(["cure","fireball","earthquake"])
        self.maxMP = 20
        self.mp = 20
        
