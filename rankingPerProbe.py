from detectionDifference import DetectionDifference


#TODO: change names
class RankingPerProbe:
    
    def __init__(self, probes, galleries):
        self.totalProbeRanking = {}
        self.probes = probes
        self.galleries = galleries
        for probe in self.probes:
            self.totalProbeRanking[probe] = self.computeProbeRanking(probe)
            
    def computeProbeRanking(self, probe):
        euclideanDistances = []
        for gallery in self.galleries:
            euclideanDistances.append(DetectionDifference(probe, gallery))
        ranking = sorted(euclideanDistances, cmp=DetectionDifference.compare)
        return ranking
    
    def getProbes(self):
        return self.totalProbeRanking.keys()
    
    def getRankingFromProbe(self, probe):
        return self.totalProbeRanking[probe]