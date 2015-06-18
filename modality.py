import random
from detectionGroup import DetectionGroup

class Modality:
    def __init__(self, probes, galleries):
        self.probes = probes
        self.galleries = galleries
        
    def __getDictionary(self, setToChooseFrom):
        detectionsDict = {}
        for detection in setToChooseFrom:
            if detection.getPersonId() not in detectionsDict:
                detectionsDict[detection.getPersonId()] = [detection]
            else:
                detectionsDict[detection.getPersonId()].append(detection)
        return detectionsDict

class SvSModality(Modality):
    def __init__(self, probes, galleries):
        Modality.__init__(self, probes, galleries)
        
    #TODO: spostare in Modality
    def __getDictionary(self, setToChooseFrom):
        detectionsDict = {}
        for detection in setToChooseFrom:
            if detection.getPersonId() not in detectionsDict:
                detectionsDict[detection.getPersonId()] = [detection]
            else:
                detectionsDict[detection.getPersonId()].append(detection)
        return detectionsDict
        
    #TODO: renderlo astratto
    def getSplits(self):
        probesToTest = self.__getRightSplitFromSet(self.probes)
        galleriesToTest = self.__getRightSplitFromSet(self.galleries)
        return probesToTest, galleriesToTest
        
    
    def __getRightSplitFromSet(self, setToChooseFrom):
        detectionsDict = self.__getDictionary(setToChooseFrom)
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
    
    def __getDictionary(self, setToChooseFrom):
        detectionsDict = {}
        for detection in setToChooseFrom:
            if detection.getPersonId() not in detectionsDict:
                detectionsDict[detection.getPersonId()] = [detection]
            else:
                detectionsDict[detection.getPersonId()].append(detection)
        return detectionsDict
    
    def getSplits(self):
        probesToTest = self.__getRightSplitFromSet(self.probes)
        galleriesToTest = self.__getRightSplitFromSet(self.galleries)
        return probesToTest, galleriesToTest
    
    def __getRightSplitFromSet(self, setToChooseFrom):
        detectionsDict = self.__getDictionary(setToChooseFrom)
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
        
    def __getDictionary(self, setToChooseFrom):
        detectionsDict = {}
        for detection in setToChooseFrom:
            if detection.getPersonId() not in detectionsDict:
                detectionsDict[detection.getPersonId()] = [detection]
            else:
                detectionsDict[detection.getPersonId()].append(detection)
        return detectionsDict
        
    def getSplits(self):
        probesToTest = self.__getProbeSplit()
        galleriesToTest = self.galleries
        return probesToTest, galleriesToTest
        
    def __getProbeSplit(self):
        detectionsDict = self.__getDictionary(self.probes)
        detectionsToReturn = []
        for probeId in detectionsDict:
            toAppend = random.choice(detectionsDict[probeId])
            detectionsDict[probeId].remove(toAppend)
            detectionsToReturn.append(toAppend)
        return detectionsToReturn
        