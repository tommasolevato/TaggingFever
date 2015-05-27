class DescriptorDifference:
    
    def __init__(self, probeId, testId, distance):
        self.probeId = probeId
        self.testId = testId
        self.distance = distance
        
    def getProbeId(self):
        return self.probeId
    
    def getTestId(self):
        return self.testId
    
    def getDistance(self):
        return self.distance
        
    @staticmethod
    def compare(dif1, dif2):
        if dif1.getDistance() < dif2.getDistance():
            return -1
        if dif1.getDistance() == dif2.getDistance():
            return 0
        if dif1.getDistance() > dif2.getDistance():
            return 1