import random
from classes.bcolors import bcolors
from classes.character import Character

class Enemy(Character):
    def __init__(self,name,strgth,dex,wis,cha):
        super().__init__(name,strgth,dex,wis,cha)

    def get_enemy_stats(self,index):
        hp_bar = self.buildBars(self.hp,self.maxHp,2)
        
        current_hp = self.padStatString(self.hp,self.maxHp)

        name = self.padName()
        if not index:
            print("                       ===================================================")
            print(bcolors.BOLD + name + "    " + current_hp + "|" + bcolors.FAIL + hp_bar +
                  bcolors.ENDC + "|")
        else:
            print(
                "\t\t                          ===================================================")
            print("\t\t" + bcolors.BOLD + str(index) + ". " + name + "    " + current_hp + "|" + bcolors.FAIL + hp_bar +
                  bcolors.ENDC + "|")

    def choose_enemy_spell(self):
        magic_choice = random.randrange(0, len(self.magic))
        spell = self.magic[magic_choice]
        dmg = spell.generate_damage()

        pct = self.hp / self.maxHp * 100

        if spell.type == "white" and pct > 50:            
            self.choose_enemy_spell()
        else:
            return spell, dmg
            