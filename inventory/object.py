class Object:
    def __init__(self,name,type,affect,description):
        self.name = name
        self.type = type
        self.affect = affect
        self.description = description
        self.qnty = 1
    
    def addToQnty(self,toAdd):
        self.qnty += toAdd
    
    def reduceQnty(self, subtract):
        self.qnty -+ subtract