from inventory.items import Item

class Armor(Item):
    def __init__(self,name,bonus):
        super().__init__(name)
        self.bonus = bonus