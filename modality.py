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

class SvSModality(Modality):
    def __init__(self, probes, galleries):
        Modality.__init__(self, probes, galleries)
        
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
        