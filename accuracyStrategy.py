from __future__ import division
from __builtin__ import True

class AccuracyStrategy:
    
    def __init__(self, rank):
        self.rank = rank
        self.successfulProbesSeen = 0
        self.totalProbesSeen = 0
        
    def updateWithNewProbe(self, ranking):
        if(self.rank > ranking.getLength()):
            limit = ranking.getLength()
        else:
            limit = self.rank
        isSuccessful = False
        i = 0
        while isSuccessful == False and i < limit:
            if ranking.getProbeId() == ranking.getNthRankedDetectionId(i+1):
                self.__addSuccessfulProbe()
                isSuccessful = True
            i += 1
        if isSuccessful == False:
            self.__addUnsuccessfulProbe()
        
    def getAccuracy(self):
        if self.totalProbesSeen == 0:
            return 0
        return self.successfulProbesSeen / self.totalProbesSeen
        
    def __addSuccessfulProbe(self):
        self.successfulProbesSeen += 1
        self.totalProbesSeen += 1
    
    def __addUnsuccessfulProbe(self):
        self.totalProbesSeen += 1
        
    def __repr__(self):
        return "Rank-" + str(self.rank) + ": " + str(self.getAccuracy())
    