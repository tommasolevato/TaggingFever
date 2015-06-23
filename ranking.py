from detectionDifference import DetectionDifference

class Ranking:
    
    def __init__(self, probe, galleries):
        self.probe = probe
        self.galleries = galleries
        self.idToRecognise = probe.getPersonId()
        self.ranking = []

    def getRanking(self):
        if self.ranking != []:
            return self.ranking
        else:
            euclideanDistances = []
            for gallery in self.galleries:
                euclideanDistances.append(DetectionDifference(self.probe, gallery))
            self.ranking = sorted(euclideanDistances, cmp=DetectionDifference.compare)
        return self.ranking
    
    def getProbeId(self):
        return self.idToRecognise
    
    def getNthRankedDetectionId(self, n):
        return self.getRanking()[n-1].getGalleryDetection().getPersonId()
    
    def getLength(self):
        return len(self.galleries)