from utility.bcolors import bcolors
import random

def castMagic(player, enemy,enemies):
    player.choose_magic()
    magic_choice = 0
    goodChoice = False
    while not goodChoice:
        try:
            magic_choice = int(input("\tChoose magic: ")) - 1
            if magic_choice < len(player.magic):
                goodChoice = True
            else:
                print("Please choose one of the available spells")
        except:
            print("Please enter a number corresponding to a spell")

    spell = player.magic[magic_choice]
    magic_dmg = spell.generate_damage()

    current_mp = player.get_mp()

    if spell.cost > current_mp:
        print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
        return False

    player.reduce_mp(spell.cost)

    if spell.type == "white":
        player.heal(magic_dmg)
        print(bcolors.OKBLUE + spell.name + " heals for " +
                str(magic_dmg) + "\n" + bcolors.ENDC)
    elif spell.type == "black":
        enemy = enemies[choose_target(enemies)]
        enemy.take_damage(magic_dmg)
        print(bcolors.OKBLUE + "\n" + spell.name + " deals " +
                str(magic_dmg) + " points of damage to " + enemies[enemy].name + "." + bcolors.ENDC)
        deathCheck(enemies,enemy)
    return True

def useItem(player, enemy, party,enemies):
    player.choose_item()
    item_choice = 0
    goodChoice = False
    while not goodChoice:
        try:
            item_choice = int(input("\tChoose item: ")) - 1
            if item_choice < len(player.items):
                goodChoice = True
            else:
                print("Please choose on of the available items")
        except:
            print("Please enter a number corresponding to an item")

    if item_choice == -1:
        return False
    if player.items[item_choice].qnty == 0:
        print(bcolors.FAIL + "\nNone left..." + bcolors.ENDC)
        return False

    item = player.items[item_choice]
    player.items[item_choice].qnty -= 1

    if item.type == "potion":
        healAmount = item.rollForAffect()
        player.heal(healAmount)
        if player.hp > player.maxHp:
            player.hp == player.maxHp
        print(bcolors.OKGREEN + "\n" + item.name +
                " heals for " + str(healAmount)
                 + " HP" + bcolors.ENDC)
    elif item.type == "elixer":
        if item.name == "MegaElixer":
            for player in party:
                player.hp = player.maxHp
                player.mp = player.max_mp
        else:
            player.hp = player.maxHp
            player.mp = player.max_mp
            print(bcolors.OKGREEN + "\n" + item.name +
                " fully restores HP/MP" + bcolors.ENDC)
    elif item.type == "attack":
        enemy = enemies[choose_target(enemies)]
        enemy.take_damage(item.prop)
        print(bcolors.FAIL + "\n" + item.name + " deals " +
                str(item.prop) + " points of damage to " + enemies[enemy].name + "." + bcolors.ENDC)
        deathCheck(enemies,enemy)
    return True

def choose_target(enemies):
    i = 1
    choice = 0
    print("\n" + bcolors.FAIL + bcolors.BOLD + "\tTarget:" + bcolors.ENDC)
    for enemy in enemies:

        enemy.get_enemy_stats(i)
        i += 1
    item_choice = 0
    goodChoice = False
    while not goodChoice:
        try:
            item_choice = int(input("\tChoose target: ")) - 1
            if item_choice < len(enemies):
                goodChoice = True
            else:
                print("Please choose on of the available enemies")
        except:
            print("Please enter a number corresponding to an enemy")

    return choice

def checkWinCon(party,enemies):
    if not enemies:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        return False

    passedOut = 0
    for player in party:
        if player.get_hp() == 0:
            passedOut += 1
    if passedOut == len(party):
        print(bcolors.FAIL + "Your enemy has defeated you" + bcolors.ENDC)
        return False
    return True

def baddiesTurn(party,enemies):
    for enemy in enemies:
        enemy_action = random.randrange(0,len(enemies))
        target = random.randrange(0, len(party))
        if enemy.actions[enemy_action] == "attack": 
            toAttack = party[target]          
            enemy_dmg = enemy.damage(toAttack)
            if enemy_dmg:
                toAttack.takeDamage(enemy_dmg)
                print(bcolors.FAIL + "Enemy attacks " + party[target].name + " for " + str(enemy_dmg) + bcolors.ENDC)
        elif enemy.actions[enemy_action] == "magic":
            if enemy.mp < 10:
                print(bcolors.FAIL + enemy.name + " tries to cast magic but fails!" + bcolors.ENDC)
                break
            spell, dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)
            if spell.type == "white":
                enemy.heal(dmg)
                print(bcolors.FAIL + enemy.name + " heals for " + str(dmg) + " hp!" + bcolors.ENDC)
            else:
                party[target].take_damage(dmg)
                print(bcolors.FAIL + enemy.name + " casts " + spell.name + " targeting " +
                    party[target].name + " for " + str(dmg) + bcolors.ENDC)

def deathCheck(enemies,enemy):
    if enemy.get_hp() == 0:
        print(bcolors.FAIL + enemy.name + " has died!" +bcolors.ENDC)
        enemies.remove(enemy)

def combat(party, enemies):
    combat = True
    print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)
    while combat:
        print("-----------------------------------")

        print("\n\n")
        print(bcolors.OKBLUE + bcolors.BOLD + "Party Members" + bcolors.ENDC)
        print("NAME                    HP")
        for player in party:
            player.getStats()
        print("\n")

        print(bcolors.FAIL + bcolors.BOLD + "Enemies Members" + bcolors.ENDC)
        print("NAME                    HP")
        for enemy in enemies:
            enemy.get_enemy_stats(False)

        for player in party:
            player.choose_action()
            goodChoice = False
            while not goodChoice:
                try:
                    choice = input("\tChoose action: ")
                    index = int(choice) - 1
                    if index < len(player.actions):
                        goodChoice = True
                    else:
                        print("Choose one of the choices from the list")
                except:
                    print("Choose one of the choices from the list")
            if player.actions[index] == "attack":
                enemy = enemies[choose_target(enemies)]
                dmg = player.damage(enemy)
                if dmg:
                    enemy.takeDamage(dmg)
                    print(bcolors.HEADER + "You atacked " + enemy.name + " for " +
                        str(dmg) + " points of damage." + bcolors.ENDC)
                    deathCheck(enemies,enemy)

            elif player.actions[index] == "magic":
                magicCast = castMagic(player, enemy,enemies)
                if not magicCast:
                    continue

            elif player.actions[index] == "items":
                usedItem = useItem(player,enemy,party,enemies)
                if not usedItem:
                    continue

            combat = checkWinCon(party, enemies)
            if not combat:
                break

        baddiesTurn(party,enemies)
        if combat:
            combat = checkWinCon(party,enemies)
