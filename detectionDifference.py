from numpy.linalg import norm

class DetectionDifference:
    
    def __init__(self, firstDetection, secondDetection):
        self.firstDetection = firstDetection
        self.secondDetection = secondDetection
        self.distance = self.computeDistance()
    
    def computeDistance(self):
        return norm(self.firstDetection.description - self.secondDetection.description)
    
    @staticmethod
    def compare(dif1, dif2):
        if dif1.distance < dif2.distance:
            return -1
        if dif1.distance == dif2.distance:
            return 0
        if dif1.distance > dif2.distance:
            return 1