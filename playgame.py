import random
from playerCreation.playerCharacter import Player
from playerCreation.enemy import Enemy
from utility.combat import combat
from inventory.readAndAddItem import findItem

from colorama import init

def main():

    init()

    chosen = False
    while not chosen:
        startGame = input("Would you like to start a new game? [yes/no] ")
        if startGame.lower() == 'yes':
            begin()
            chosen = True
        elif startGame.lower() == 'no':
            break
        else:
            print("Sorry please enter 'yes' or 'no'." )
    print("Thanks for playing!")

def chooseStat(index,chosen):
    finished = False
    statList = ['strength','dexterity','wisdom','charisma']
    diceIndex = None
    while not finished:
        diceIndex = int(input("Which value would you like to be your " + statList[index] + "? "))
        if diceIndex in chosen:
            print("That stat has already been chosen please pick again")
        else:
            finished = True
    return diceIndex

def buildCharacter(name, dice):
    
    chosen = []
    stats = []
    for i in range(0,4):
        diceIndex = chooseStat(i,chosen)
        chosen.append(diceIndex)
        stats.append(dice[diceIndex])

    return Player(name,stats[0],stats[1],stats[2],stats[3])

def begin():
    name = input("What is your name? ")
    i = 0
    dice = []
    print("Your Stats are: ")
    while i < 4:
        roll = random.randrange(0,20)
        print("[" + str(i) + "] : " + str(roll))
        dice.append(roll)
        i += 1
    
    newPlayer = buildCharacter(name, dice)
    weapon = findItem("weapons","dagger")
    if weapon:
        newPlayer.weapons.append(weapon)
        newPlayer.equipWeapon(weapon)
    
    enterCave(newPlayer)

def enterCave(newPlayer):
    party = [newPlayer]
    baddie = Enemy("Murlock",14,12,8,6)
    enemies = [baddie]
    combat(party,enemies)
    # print("You wake up in a cave, there is an exit to the east and a tunnel further into the depths, what do you want to do?")
    # print("[0] : Exit the Cave")
    # print("[1] : Go down the tunnel")
    # print("[2]: look around the current room")
    # direction = input()



main()