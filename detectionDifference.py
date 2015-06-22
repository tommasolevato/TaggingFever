from numpy.linalg import norm

class DetectionDifference:
    
    def __init__(self, firstDetectionGroup, secondDetectionGroup):
        self.firstDetectionGroup = firstDetectionGroup
        self.secondDetectionGroup = secondDetectionGroup
        self.distance = self.computeDistance()
    
    def getProbeDetection(self):
        return self.firstDetectionGroup
    
    def getGalleryDetection(self):
        return self.secondDetectionGroup
    
    def computeDistance(self):
        firstDetectionList = self.firstDetectionGroup.getDetections()
        secondDetectionList = self.secondDetectionGroup.getDetections()
        if len(firstDetectionList) > 1 or len(secondDetectionList) > 1:
            minimum = DetectionDifference(firstDetectionList[0], secondDetectionList[0])
            for probe in firstDetectionList:
                for gallery in secondDetectionList:
                    tmp = DetectionDifference(probe, gallery)
                    if(DetectionDifference.compare(tmp,minimum)<0):
                        minimum=tmp
            return minimum.computeDistance()
        else:
            return norm(self.firstDetectionGroup.getPersonDescription() - self.secondDetectionGroup.getPersonDescription())
        
    @staticmethod
    def compare(dif1, dif2):
        if dif1.distance < dif2.distance:
            return -1
        if dif1.distance == dif2.distance:
            return 0
        if dif1.distance > dif2.distance:
            return 1