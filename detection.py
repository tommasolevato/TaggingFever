class Detection:
    
    def __init__(self, personId, description):
        self.personId = personId
        self.description = description
        
    def getPersonId(self):
        return self.personId
    
    def getPersonDescription(self):
        return self.description