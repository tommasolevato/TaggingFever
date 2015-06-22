class Detection:
    
    def __init__(self, mainId, description):
        self.mainId = mainId
        self.description = description
        
    def getPersonId(self):
        return self.mainId
    
    def getPersonDescription(self):
        return self.description
    
    #TODO: Bruttura
    def getDetections(self):
        return [self]
    
    def __repr__(self):
        return "ID=" + `self.mainId`
    
    def getId(self):
        return self.mainId