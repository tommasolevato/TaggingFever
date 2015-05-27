class RankNAccuracy:
    
    def __init__(self, rank):
        self.rank = rank
        
    def isProbeSuccessfullyRecognized(self, ranking):
        for i in range(0, self.rank):
            if ranking[0].firstDetection.personId == ranking[i].secondDetection.personId:
                return True
        return False