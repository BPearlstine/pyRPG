from classes.bcolors import bcolors
import random

def castMagic(player, enemy,enemies):
    player.choose_magic()
    magic_choice = int(input("\tChoose magic: ")) - 1

    if magic_choice == -1:
        return False

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
        enemy = choose_target(enemies)
        enemies[enemy].take_damage(magic_dmg)
        print(bcolors.OKBLUE + "\n" + spell.name + " deals " +
                str(magic_dmg) + " points of damage to " + enemies[enemy].name + "." + bcolors.ENDC)
        deathCheck(enemies, enemy)
    return True

def useItem(player, enemy, party,enemies):
    player.choose_item()
    item_choice = int(input("\tChoose item: ")) - 1

    if item_choice == -1:
        return False
    if player.items[item_choice].qnty == 0:
        print(bcolors.FAIL + "\nNone left..." + bcolors.ENDC)
        return False

    item = player.items[item_choice]["item"]
    player.items[item_choice].qnty -= 1

    if item.type == "potion":
        player.heal(item.prop)
        print(bcolors.OKGREEN + "\n" + item.name +
                " heals for " + str(item.prop) + "HP" + bcolors.ENDC)
    elif item.type == "elixer":
        if item.name == "MegaElixer":
            for player in party:
                player.hp = player.max_hp
                player.mp = player.max_mp
        else:
            player.hp = player.max_hp
            player.mp = player.max_mp
            print(bcolors.OKGREEN + "\n" + item.name +
                " fully restores HP/MP" + bcolors.ENDC)
    elif item.type == "attack":
        enemy = choose_target(enemies)
        enemies[enemy].take_damage(item.prop)
        print(bcolors.FAIL + "\n" + item.name + " deals " +
                str(item.prop) + " points of damage to " + enemies[enemy].name + "." + bcolors.ENDC)
        deathCheck(enemies, enemy)
    return True

def choose_target(enemies):
    i = 1
    print("\n" + bcolors.FAIL + bcolors.BOLD + "\tTarget:" + bcolors.ENDC)
    for enemy in enemies:

        enemy.get_enemy_stats(i)
        i += 1
    return int(input("\tChoose target: ")) - 1

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
    if enemies[enemy].get_hp() == 0:
        print(bcolors.FAIL + enemies[enemy].name + " has died!" +bcolors.ENDC)
        del enemies[enemy]

def combat(party, enemies):
    combat = True
    print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)
    while combat:
        print("-----------------------------------")

        print("\n\n")
        print("NAME                 HP")
        for player in party:
            player.getStats()
        print("\n")

        for enemy in enemies:
            enemy.get_enemy_stats(False)

        for player in party:
            player.choose_action()
            choice = input("\tChoose action: ")
            index = int(choice) - 1

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

        combat = checkWinCon(party,enemies)
