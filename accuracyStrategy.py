from __future__ import division

class AccuracyStrategy:
    
    def __init__(self, rank):
        self.rank = rank
        
    def computeAccuracy(self, dataset):
        processedProbes = 0
        successfulProbes = 0
        for probe in dataset.probeSet:
            if self._isProbeSuccessfullyRecognized(dataset.getRanking(probe)):
                successfulProbes += 1
            processedProbes += 1
        #TODO: remove
        print successfulProbes
        print processedProbes
        return successfulProbes / processedProbes
        
    def _isProbeSuccessfullyRecognized(self, ranking):
        for i in range(0, self.rank):
            if ranking[0].firstDetection.personId == ranking[i].secondDetection.personId:
                return True
            return False