from classes.items import Item

class Weapon(Item):
    def __init__(self,name,type,dmg,description):
        super().__init__(name)
        self.type = type
        self.dmg = dmg
        self.description = description