from __future__ import division

class AccuracyStrategy:
    
    def __init__(self, rank):
        self.rank = rank
        
    def isProbeSuccessfullyRecognized(self, ranking):
        if(self.rank > len(ranking)):
            limit = len(ranking)
        else:
            limit = self.rank
        for i in range(0, limit):
            if ranking[0].firstDetection.personId == ranking[i].secondDetection.personId:
                return True
        return False
        
    def __repr__(self):
        return "Rank-" + str(self.rank)