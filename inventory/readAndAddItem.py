from inventory.weapon import Weapon
from inventory.items import Item

def findItem(csv,toFind):
    fileName =".\\inventory\\" + csv + ".csv"
    with open(fileName) as f:
        items = f.readlines()
        for item in items:
            line = item.split(",")
            if line[0] == toFind:
                if csv == "weapons":
                    newWeapon = Weapon(line[0],line[1],int(line[2]),line[3].strip('\n'))
                    return newWeapon
                elif csv == "items":
                    newItem = Item(line[0], line[1], int(
                        line[2]), line[3].strip('\n'))
                    return newItem                    
    return False
