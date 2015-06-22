from __future__ import division

class Trace:
    def __init__(self, traceId, detections, descriptionSelector, mainId):
        self.detections = detections
        self.traceId = traceId
        self.descriptionSelector = descriptionSelector
        self.mainId = mainId
        
    def getDetections(self):
        return [self]
        
    def getId(self):
        return self.traceId
    
    def getPersonId(self):
        return self.mainId
    
    def getPersonDescription(self):
        return self.descriptionSelector.selectDescription(self.detections)
    
    def getScore(self):
        count = 0
        for detection in self.detections:
            if detection.getPersonId() == self.mainId:
                count += 1
        return count/len(self.detections)