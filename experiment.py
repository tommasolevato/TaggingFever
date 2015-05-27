from __future__ import division
from rankNAccuracy import RankNAccuracy

class Experiment:
    
    def __init__(self, rankingPerProbe, rankForAccuracyComputation):
        self.rankingPerProbe = rankingPerProbe
        self.accuracyMeter = RankNAccuracy(rankForAccuracyComputation)
        
    def computeAccuracy(self):
        processedProbes = 0
        successfulProbes = 0
        for probe in self.rankingPerProbe.getProbes():
            if self.accuracyMeter.isProbeSuccessfullyRecognized(self.rankingPerProbe.getRankingFromProbe(probe)):
                successfulProbes += 1
            processedProbes += 1
        return successfulProbes / processedProbes