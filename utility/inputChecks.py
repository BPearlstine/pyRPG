def checkForGoodInput(inputString, max):
    goodChoice = False
    while not goodChoice:
        try:
            choice = int(input(inputString)) - 1
            if choice < max:
                goodChoice = True
            else:
                print("Unavailable option")
        except:
            print("Please enter an index number")
    return choice
