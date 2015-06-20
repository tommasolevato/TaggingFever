import random
from detectionGroup import DetectionGroup

class Modality(object):
    def __init__(self, probes, galleries):
        self.probes = probes
        self.galleries = galleries
        
    def getDictionary(self, setToChooseFrom):
        detectionsDict = {}
        for detection in setToChooseFrom:
            if detection.getId() not in detectionsDict:
                detectionsDict[detection.getId()] = [detection]
            else:
                detectionsDict[detection.getId()].append(detection)
        return detectionsDict
    
    @staticmethod
    def getName(N):
        if N == -1:
            return 'AvA'
        elif N == 0:
            return 'SvA'
        elif N == 1:
            return 'SvS'
        else:
            return str(N) + 'v' + str(N)
    
    #TODO: generatore
    def getNumberOfSplits(self):
        return self.numberOfSplits
    
    
    
class AllvsAllModality(Modality):
    def __init__(self, probes, galleries):
        Modality.__init__(self, probes, galleries)
        self.numberOfSplits = 1
        
    def getSplits(self):
        return self.probes, self.galleries



class SvSModality(Modality):
    def __init__(self, probes, galleries):
        Modality.__init__(self, probes, galleries)
        self.numberOfSplits = 100
        
    #TODO: renderlo astratto
    def getSplits(self):
        probesToTest = self.__getRightSplitFromSet(self.probes)
        galleriesToTest = self.__getRightSplitFromSet(self.galleries)
        return probesToTest, galleriesToTest
        
    def __getRightSplitFromSet(self, setToChooseFrom):
        detectionsDict = self.getDictionary(setToChooseFrom)
        detectionsToReturn = []
        for probeId in detectionsDict:
            toAppend = random.choice(detectionsDict[probeId])
            detectionsDict[probeId].remove(toAppend)
            detectionsToReturn.append(toAppend)
        return detectionsToReturn



class MvsMModality(Modality):
    def __init__(self, probes, galleries, N):
        Modality.__init__(self, probes, galleries)
        self.N = N
        self.numberOfSplits = 100
    
    def getSplits(self):
        probesToTest = self.__getRightSplitFromSet(self.probes)
        galleriesToTest = self.__getRightSplitFromSet(self.galleries)
        return probesToTest, galleriesToTest
    
    def __getRightSplitFromSet(self, setToChooseFrom):
        detectionsDict = self.getDictionary(setToChooseFrom)
        detectionsToReturn = []
        for personId in detectionsDict:
            detectionsList = detectionsDict[personId]
            toAppend = DetectionGroup(self.__getSubListOfNElementsAtBest(detectionsList))
            detectionsToReturn.append(toAppend)
        return detectionsToReturn
    
    def __getSubListOfNElementsAtBest(self, listToChooseFrom):
        if len(listToChooseFrom) < self.N:
            limit = len(listToChooseFrom)
        else:
            limit = self.N
        toReturn = []
        while len(toReturn) < limit:
            toAppend = random.choice(listToChooseFrom)
            listToChooseFrom.remove(toAppend)
            toReturn.append(toAppend)
        return toReturn
    
    
    
class SvsAllModality(Modality):
    def __init__(self, probes, galleries):
        Modality.__init__(self, probes, galleries)
        self.numberOfSplits = 100
        
    def getSplits(self):
        probesToTest = self.__getProbeSplit()
        galleriesToTest = self.galleries
        return probesToTest, galleriesToTest
        
    def __getProbeSplit(self):
        detectionsDict = self.getDictionary(self.probes)
        detectionsToReturn = []
        for probeId in detectionsDict:
            #TODO: non remove ma controllo
            toAppend = random.choice(detectionsDict[probeId])
            detectionsDict[probeId].remove(toAppend)
            detectionsToReturn.append(toAppend)
        return detectionsToReturn
        