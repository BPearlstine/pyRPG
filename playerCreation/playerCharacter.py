import random
from utility.bcolors import bcolors
from playerCreation.character import Character
from inventory.readAndAddItem import findItem
from utility.combat import deathCheck

class Player(Character):
    def __init__(self,name,strgth,dex,wis,cha):
        super().__init__(name,strgth,dex,wis,cha) 
        self.xp = 0

    def choose_action(self):
        i = 1
        # print("\n\t" + bcolors.BOLD + self.name + bcolors.ENDC)
        print("\n\n\n")
        self.getStats()
        print(bcolors.OKBLUE + bcolors.BOLD + "\tActions" + bcolors.ENDC)
        for item in self.actions:
            print("\t\t" + str(i) + ": " + item)
            i+= 1
    
    def choose_magic(self):
        i = 1
        print("\n" + bcolors.OKBLUE + bcolors.BOLD + "\tMagic:" + bcolors.ENDC)
        for spell in self.magic:            
            print("\t\t" + str(i) + ": " + spell.name +
                  ", cost: " + str(spell.cost) + ", " + spell.description)
            i += 1
    
    def choose_item(self):
        i = 1
        print("\n" + bcolors.OKBLUE + bcolors.BOLD + "\tItems:" + bcolors.ENDC)
        for item in self.items:
            print("\t\t" + str(i) + ":" + item.name + "; " +
                  item.description + ", available: " + str(item.qnty))
            i +=1

    def getStats(self):
        hp_bar = self.buildBars(self.hp,self.maxHp,4)
        mp_bar = self.buildBars(self.mp, self.maxMP, 10)

        current_hp = self.padStatString(self.hp,self.maxHp)
        current_mp = self.padStatString(self.mp, self.maxMP)

        name = self.padName()

        print("                   ==========================                     ===========")
        print(bcolors.BOLD + name + "    "+ current_hp + "|" + bcolors.OKGREEN + hp_bar +\
              bcolors.ENDC + "|        " + current_mp + "|" +
              bcolors.OKBLUE + mp_bar + bcolors.ENDC + "|")


    def setUpGear(self,weapon):
        weapon = findItem("weapons", weapon)
        if weapon:
            self.weapons.append(weapon)
            self.equipWeapon(weapon)
        potions = ["potion","megapotion","elixer","megaElixer"]
        for potion in potions:
            item = findItem("items",potion)
            if item:
                item.addToQnty(4)
                self.items.append(item)

