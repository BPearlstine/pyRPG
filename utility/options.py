import sys

from utility.inputChecks import checkForGoodInput

def options():
    options = ["Quit Game","Back"]

    print("Options: ")
    for i in range(0,len(options)):
        print("[" + str(i + 1) + "] " + options[i])
    optionIndex = checkForGoodInput(": ", len(options))
    option = options[optionIndex]

    if option == "Quit Game":
        sys.exit(0)
    elif option == "Back":
        return False
    