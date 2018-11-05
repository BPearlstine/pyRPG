from inventory.object import Object

class Weapon(Object):
    def __init__(self,name,type,affect,description):
        super().__init__(name,type,affect,description)
        self.buffs = {}
    
    def addBuff(self,name,bonus):
        self.buffs[name] = bonus
        self.affect += bonus

    def removeBuff(self,name,bonus):
        del self.buffs[name]
        self.affect -= bonus