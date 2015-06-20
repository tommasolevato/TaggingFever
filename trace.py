from __future__ import division


class Trace:
    def __init__(self, traceId, detections, descriptionSelector, mainId):
        self.detections = detections
        self.traceId = traceId
        self.descriptionSelector = descriptionSelector
        self.mainId = mainId
        
    #TODO: non ha senso
    def getDetections(self):
        return [self]
        
    def getId(self):
        return self.traceId
    
    #TODO: change name
    def getPersonId(self):
        return self.mainId
    
    def getPersonDescription(self):
        return self.descriptionSelector.selectDescription(self.detections)
    
    #TODO: change name
    def getScore(self):
        count = 0
        for detection in self.detections:
            if detection.getPersonId() == self.mainId:
                count += 1
        return count/len(self.detections)