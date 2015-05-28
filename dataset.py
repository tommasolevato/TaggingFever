from detectionDifference import DetectionDifference

class Dataset:
    
    def __init__(self, probeSet, gallerySet):
        self.probeSet = probeSet
        self.gallerySet = gallerySet
        
    #TODO: change name and signature
    def getRanking(self, probe):
        euclideanDistances = []
        for gallery in self.gallerySet:
            euclideanDistances.append(DetectionDifference(probe, gallery))
        ranking = sorted(euclideanDistances, cmp=DetectionDifference.compare)
        return ranking