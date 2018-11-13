from utility.bcolors import bcolors
from utility.inputChecks import checkForGoodInput
from utility.options import options
import random

def castMagic(player, enemies):
    player.choose_magic()
    magic_choice = checkForGoodInput("\tChoose magic: ", len(player.magic))
    spell = player.magic[magic_choice]
    current_mp = player.get_mp()

    if spell.cost > current_mp:
        print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
        return False

    player.reduce_mp(spell.cost)
    spell.castSpell(player,enemies)
    return True

def elixerBoost(player,item):
    hpBoost = item.rollForAffect()
    mpBoost = item.rollForAffect()
    player.heal(hpBoost)
    player.gain_mp(mpBoost)
    print(bcolors.OKGREEN + "\n" + item.name +
            " restores HP" + str(hpBoost) + bcolors.ENDC)
    print(bcolors.OKGREEN + "\n" + item.name +
            " restores MP" + str(mpBoost) + bcolors.ENDC)

def useItem(player, party, enemies):
    player.choose_item()
    item_choice = checkForGoodInput("\tChoose item: ", len(player.items))
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
        if item.name == "megaElixer":
            for player in party:
                elixerBoost(player,item)
        else:
            elixerBoost(player,item)                
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
    choice = checkForGoodInput("\tChoose target: ",len(enemies))
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

def combatMenu(index, player, enemies, party):
    if player.actions[index] == "attack":
        enemy = enemies[choose_target(enemies)]
        dmg = player.damage(enemy)
        if dmg:
            enemy.takeDamage(dmg)
            print(bcolors.HEADER + player.name + "atacked " + enemy.name + " for " +
                    str(dmg) + " points of damage." + bcolors.ENDC)
            deathCheck(enemies, enemy)

    elif player.actions[index] == "spells":
        magicCast = castMagic(player, enemies)
        if not magicCast:
            return False

    elif player.actions[index] == "items":
        usedItem = useItem(player, party, enemies)
        if not usedItem:
            return False

    elif player.actions[index] == "options":
        choice = options()
        return choice

    return True

def combat(party, enemies):
    combat = True
    print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)
    while combat:
        print("-----------------------------------")

        print("\n\n")
        print(bcolors.OKBLUE + bcolors.BOLD + "Party Members" + bcolors.ENDC)
        print("NAME                   HP                                              MP")
        for player in party:
            player.getStats()
        print("\n")

        print(bcolors.FAIL + bcolors.BOLD + "Enemies Members" + bcolors.ENDC)
        print("NAME                   HP")
        for enemy in enemies:
            enemy.get_enemy_stats(False)

        for player in party:
            player.choose_action()
            index = checkForGoodInput("\tChoose action: ", len(player.actions))

            success = combatMenu(index, player, enemies,party)
            if not success:
                continue

            combat = checkWinCon(party, enemies)

            if not combat:
                break

        baddiesTurn(party,enemies)
        if combat:
            combat = checkWinCon(party,enemies)
