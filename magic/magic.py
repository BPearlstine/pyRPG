import random

from utility.bcolors import bcolors
from utility.combat import choose_target, deathCheck


class Spell:
    def __init__(self, name, cost, dmg, description, type):
        self.name = name
        self.cost = cost
        self.dmg = dmg
        self.description = description
        self.type = type
    
    def generate_damage(self,character):
        wisMod = character.getAbilityScore(character.wis)
        
        return random.randrange(1, 6) + wisMod

    def castSpell(self,character,enemies):       
        if self.type == "white":
            magic_dmg = self.generate_damage(character)
            character.heal(magic_dmg)
            print(bcolors.OKBLUE + character.name + " heals for " +
                str(magic_dmg) + "\n" + bcolors.ENDC)
        elif self.type == "black":
            enemy = enemies[choose_target(enemies)]
            wisMod = character.getAbilityScore(character.wis)
            attackRoll = random.randrange(1, 20) + wisMod
            if attackRoll < enemy.ac:
                print(bcolors.FAIL + character.name + " tries to attack " +
                    enemy.name + " but misses!" + bcolors.ENDC)
            else:
                magic_dmg = self.generate_damage(character)
                enemy.take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + character.name + " deals " +
                    str(magic_dmg) + " points of damage to " + enemies[enemy].name + "." + bcolors.ENDC)
                deathCheck(enemies, enemy)
