import random

from playerCreation.baseClasses.paladin import Paladin
from playerCreation.baseClasses.mage import Mage
from playerCreation.baseClasses.ranger import Ranger
from playerCreation.enemy import Enemy
from utility.combat import combat
from utility.inputChecks import checkForGoodInput
from inventory.readAndAddItem import findItem
from inventory.items import Item

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
    print("\nThanks for playing!")

def chooseStat(index,chosen):
    finished = False
    statList = ['strength','dexterity','wisdom','charisma']
    diceIndex = None
    while not finished:
        try:
            diceIndex = int(input("Which value would you like to be your " + statList[index] + "? "))
            if diceIndex in chosen:
                print("That stat has already been chosen please pick again")
            elif 1 <= diceIndex <= 4 :
                finished = True
            else:
                print("Sorry, please choose 1 - 4")
        except:
            print("Sorry, please choose 1 - 4")
    return diceIndex

def buildCharacter(name, dice):
    print("Which class would you like to play as?")
    classes = ["paladin", "mage", "ranger"]
    for i in range(0,3):
        print("[" + str(i + 1) + "] " + classes[i])
    classIndex = checkForGoodInput(": ", len(classes))
    startingClass = classes[classIndex]

    chosen = []
    stats = []
    for i in range(0,4):
        diceIndex = chooseStat(i,chosen)
        chosen.append(diceIndex)
        stats.append(dice[diceIndex - 1])
    if startingClass == "paladin":
        return Paladin(name,stats[0],stats[1],stats[2],stats[3])
    elif startingClass == "mage":
        return Mage(name, stats[0], stats[1], stats[2], stats[3])
    elif startingClass == "ranger":
        return Ranger(name, stats[0], stats[1], stats[2], stats[3])

def begin():
    goodName = False
    while not goodName:
        name = input("What is your name? ")
        if len(name) > 10:
            print("Please choose a name no more than 10 characters.")
        else:
            goodName = True
    i = 0
    dice = []
    print("Your Stats are: ")
    likeRolls = False
    while not likeRolls:
        while i < 4:
            roll = random.randrange(0,20)
            print("[" + str(i + 1) + "] : " + str(roll))
            dice.append(roll)
            i += 1
        i = 0
        reRoll = input("Do you want to re-roll your stats? [yes/no]: ")
        if reRoll.lower() == "no":
            likeRolls = True
        # elif reRoll.lower() != "yes":
        #     while reRoll.lower() != "yes" or reRoll.lower() != "no":
        #         print("Sorry, please enter 'yes' or 'no'")
        #         reRoll = input("Do you want to re-roll your stats? [yes/no]: ")
        #         if reRoll.lower() == "no":
        #             likeRolls = True
    
    newPlayer = buildCharacter(name, dice)
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
