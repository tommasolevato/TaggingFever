class DetectionGroup:
    def __init__(self, detections):
        self.detections = detections
      
    def getPersonId(self):
        return self.detections[0].getPersonId()
      
    def getDetections(self):
        return self.detections