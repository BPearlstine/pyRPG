from inventory.object import Object
import random

class Item(Object):
    def __init__(self,name,type,affect,description):
        super().__init__(name,type,affect,description)

    def rollForAffect(self):
        return random.randrange(1,self.affect)