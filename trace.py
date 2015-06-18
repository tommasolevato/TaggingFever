class Trace:
    def __init__(self, traceId, detections, descriptionSelector):
        self.detections = detections
        self.traceId = traceId
        self.descriptionSelector = descriptionSelector
        
    #TODO: non ha senso
    def getDetections(self):
        return [self]
        
    def getId(self):
        return self.traceId
    
    #TODO: change name
    def getPersonId(self):
        return self.detections[0].getPersonId()
    
    def getPersonDescription(self):
        return self.descriptionSelector.selectDescription(self.detections)