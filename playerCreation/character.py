import random
from math import floor
from utility.bcolors import bcolors
from magic.magic import Spell

class Character:
    def __init__(self,name,strgth,dex,wis,cha):
        self.name = name
        self.str = strgth
        self.dex = dex
        self.wis = wis
        self.cha = cha
        self.ac = self.getAbilityScore(dex) + 10
        self.weapons = []
        self.armor = []
        self.dfns = self.dex + self.str + 10
        self.maxHp = 20
        self.hp = 20
        self.actions = ['options','attack','items']
        self.items = []
        self.magic = []
        self.maxMP = 0
        self.mp = 0
        self.equippedWeapon = None

    def equipWeapon(self,weapon):
        if weapon in self.weapons:
            self.equippedWeapon = weapon
    
    def getAbilityScore(self,stat):
        return floor(stat - 10) - 2

    def addMagic(self,spells):
        with open(".\\magic\\spells.csv") as f:
            data = f.readlines()
            for line in data:
                line = line.strip('\n').split(",")
                if line[0] in spells:
                    newSpell = Spell(line[0], int(line[1]), int(line[2]), line[3], line[4])
                    self.magic.append(newSpell)
    
    def get_hp(self):
        return self.hp
    
    def get_max_hp(self):
        return self.maxHp

    def takeDamage(self,dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
    
    def heal(self,healed):
        self.hp += healed
        if self.hp > self.maxHp:
            self.hp = self.maxHp
    
    def get_mp(self):
        return self.mp
    
    def reduce_mp(self,cost):
        self.mp -= cost

    def gain_mp(self,gain):
        self.mp += gain
        if self.mp > self.maxMP:
            self.mp = self.maxMP
    
    def removeArmor(self,armor):
        if armor in self.armor: 
            self.armor.remove(armor)
            self.ac -= armor.bonus

    def addArmor(self,armor):
        self.armor.append(armor)
        self.ac += armor.bonus
    
    def attack(self):
        if not self.equippedWeapon:
            return self.str
        else:
            if self.equippedWeapon.type == 'ranged':
                return self.dex
            if self.equippedWeapon.type == 'melee':
                return self.str
    
    def damage(self,enemy):
        statToUse = 0
        if not self.equippedWeapon:
            statToUse = self.getAbilityScore(self.str)
        else:
            if self.equippedWeapon.type == 'melee':
                statToUse = self.getAbilityScore(self.str)
            elif self.equippedWeapon.type == 'ranged':
                statToUse = self.getAbilityScore(self.dex) 
        attackRoll = random.randrange(1,20) + statToUse
        if attackRoll > enemy.ac:
            if not self.equippedWeapon:
                return random.randrange(1,6) + statToUse
            else:
                return random.randrange(1,int(self.equippedWeapon.affect)) + statToUse
        print(bcolors.FAIL + self.name + " tries to attack "+ enemy.name + " but misses!" + bcolors.ENDC)
        return False

    def __str__(self):
        return self.name + ", Str: " + str(self.str) + ", Dex: " + str(self.dex) + ", Wis: " + str(self.wis) + ", Cha: " + str(self.cha)

    def buildBars(self,currStat,maxStat,divisor):
        bar = ""
        bar_ticks = (currStat / maxStat) * 100 / divisor
        while bar_ticks >= 0:
            bar += "█"
            bar_ticks -= 1
        while len(bar) <= (100/divisor):
            bar += " "
        return bar

    def padStatString(self,currStat,maxStat):
        statString = str(currStat) + "/" + str(maxStat)
        paddedStat = ""
        if len(statString) < 11:
            decreased = 11 - len(statString)
            while decreased > 0:
                paddedStat += " "
                decreased -= 1
        paddedStat += statString
        return paddedStat
    
    def padName(self):
        name = self.name
        if len(name) < 10:
            decreased = 0
            while decreased > 0:
                name += " "
                decreased -= 1
        return name


