from inventory.weapon import Weapon

def findItem(csv,toFind):
    fileName =".\\inventory\\" + csv + ".csv"
    with open(fileName) as f:
        items = f.readlines()
        for item in items:
            line = item.split(",")
            if line[0] == toFind:
                newWeapon = Weapon(line[0],line[1],line[2],line[3])
                return newWeapon
    return False