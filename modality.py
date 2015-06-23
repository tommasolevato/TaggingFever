import random
from detectionGroup import DetectionGroup
from abc import abstractmethod

class Modality(object):
    def __init__(self, dataset):
        self.probes = dataset.getProbeSet()
        self.galleries = dataset.getGallerySet()
        
    def getDictionary(self, setToChooseFrom):
        detectionsDict = {}
        for detection in setToChooseFrom:
            if detection.getId() not in detectionsDict:
                detectionsDict[detection.getId()] = [detection]
            else:
                detectionsDict[detection.getId()].append(detection)
        return detectionsDict
    
    @abstractmethod
    def getSplits(self):
        pass
    
    @staticmethod
    def getName(N):
        if str(N) == 'AvA':
            return 'AvA'
        elif str(N) == 'SvA':
            return 'SvA'
        elif N == '1':
            return 'SvS'
        else:
            return str(N) + 'v' + str(N)
    
    def getNumberOfSplits(self):
        return self.numberOfSplits
    
    
    
class AllvsAllModality(Modality):
    def __init__(self, dataset):
        Modality.__init__(self, dataset)
        self.numberOfSplits = 1
        
    def getSplits(self):
        return self.probes, self.galleries



class SvsSModality(Modality):
    def __init__(self, dataset):
        Modality.__init__(self, dataset)
        self.numberOfSplits = 100
        
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
    def __init__(self, dataset, N):
        Modality.__init__(self, dataset)
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
    def __init__(self, dataset):
        Modality.__init__(self, dataset)
        self.numberOfSplits = 100
        
    def getSplits(self):
        probesToTest = self.__getProbeSplit()
        galleriesToTest = self.galleries
        return probesToTest, galleriesToTest
        
    def __getProbeSplit(self):
        detectionsDict = self.getDictionary(self.probes)
        detectionsToReturn = []
        for probeId in detectionsDict:
            toAppend = random.choice(detectionsDict[probeId])
            detectionsDict[probeId].remove(toAppend)
            detectionsToReturn.append(toAppend)
        return detectionsToReturn
        