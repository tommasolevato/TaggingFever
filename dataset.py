from __future__ import division
from detectionDifference import DetectionDifference
import random
import numpy
from detection import Detection


#contiene i set di probe e gallery di interesse (dati al costruttore) e si occupa di calcolare i ranking
#TODO: non passare i set ma prenderli dal db
class Dataset:
    
    def __init__(self, probeSet, gallerySet):
        self.probeSet = probeSet
        self.gallerySet = gallerySet
        self.probeDict = {}
        self.galleryDict = {}
        #TODO: scommentare
        #self._prepareDictionaries()
        
    def getRanking(self, probe):
        euclideanDistances = []
        for gallery in self.gallerySet:
            euclideanDistances.append(DetectionDifference(probe, gallery))
        ranking = sorted(euclideanDistances, cmp=DetectionDifference.compare)
        return ranking
    
    def getRankingTrace(self, probe, galleries):
        euclideanDistances = []
        for gallery in galleries:
            euclideanDistances.append(DetectionDifference(probe, gallery))
        ranking = sorted(euclideanDistances, cmp=DetectionDifference.compare)
        return ranking
    
    #TODO: spostare in ranking
    def getRankingMvsM(self, peopleid, N):
        probe = self.chooseProbeSubList(peopleid, N)
        gallery = self.chooseGallerySubDict(N)
        euclideanDistances = []
        for galleryId in gallery:
            euclideanDistances.append(self._computeMinNxN(probe, gallery[galleryId]))
        ranking = sorted(euclideanDistances, cmp=DetectionDifference.compare)
        return ranking
    
    def _prepareTraceSets(self, traceProbesDict, traceGalleriesDict):
        probes = []
        galleries = []
        for k in traceProbesDict:
            listToChooseFrom = traceProbesDict[k]
            detection = random.choice(listToChooseFrom)
            probes.append(detection)
        raw_input()
        for k in traceGalleriesDict:
            listToAverage = traceGalleriesDict[k]
            desc = self._average(listToAverage)
            print listToAverage[0].getPersonId()
            galleries.append(Detection(listToAverage[0].getPersonId(), desc))
        return probes, galleries
    
    def _average(self, list):
        sum = numpy.zeros(len(list[0].getPersonDescription()))
        for detection in list:
            sum = sum + detection.getPersonDescription()
        return numpy.divide(sum, len(list))
    
    def getRankingSvsAll(self, peopleid):
        probe = self.chooseProbeSubList(peopleid, 1)[0]
        euclideanDistances = []
        for gallery in self.gallerySet:
            euclideanDistances.append(DetectionDifference(probe, gallery))
        ranking = sorted(euclideanDistances, cmp=DetectionDifference.compare)
        return ranking
    
    def chooseProbeSubList(self, peopleid, N):
        toReturn =  self._chooseSubDict(self.probeDict, peopleid, N)
        return toReturn
    
    def chooseProbeSubDict(self, N):
        toReturn = {}
        for probe in self.probeDict:
            probeList =  self._chooseSubDict(self.probeDict, probe, N)
            toReturn[probe] = probeList
        return toReturn
    
    def verifyN(self, N):
        probeDict = self.chooseProbeSubDict(N)
        galleryDict = self.chooseGallerySubDict(N)
        distractors = []
        for probe in probeDict:
            if len(probeDict[probe]) < N:
                print "Not enough detections for id " + str(probe) + " in probe set."
            if probe not in galleryDict:
                print "There are no galleries for id " + str(probe) + "."
        for gallery in galleryDict:
            if len(galleryDict[gallery]) < N:
                print "Not enough detections for id " + str(gallery) + " in gallery set."
            if gallery not in probeDict:
                distractors.append(gallery)
        print "There are " + str(len(distractors)) + " distractors: " + str(distractors)
            
    def chooseGallerySubDict(self, N):
        toReturn = {}
        for gallery in self.galleryDict:
            galleryList =  self._chooseSubDict(self.galleryDict, gallery, N)
            toReturn[gallery] = galleryList
        return toReturn
    
    def _chooseSubDict(self, dictToChooseFrom, peopleid, N):
        assert N==1 or N==3 or N==5 or N==10
        detectionList = dictToChooseFrom[peopleid]
        detectionSubset = []
        if len(detectionList) < N:
            limit = len(detectionList)
        else:
            limit = N 
        while len(detectionSubset) < limit:
            detectionToAdd = random.choice(detectionList)
            if(detectionToAdd not in detectionSubset):
                detectionSubset.append(detectionToAdd)
        assert len(detectionSubset) == limit
        return detectionSubset
    
    def _buildDictFromSet(self, detectionSet):
        galleryPerPeopleId = {}
        for gallery in detectionSet:
            if(gallery.getPersonId() not in galleryPerPeopleId):
                galleryPerPeopleId[gallery.getPersonId()] = [gallery]
            else:
                galleryPerPeopleId[gallery.getPersonId()].append(gallery)
        return galleryPerPeopleId
    
    def _prepareDictionaries(self):
        self.probeDict = self._buildDictFromSet(self.probeSet)
        self.galleryDict = self._buildDictFromSet(self.gallerySet)
    
    def getProbeKeys(self):
        assert not self.probeDict == {}
        return self.probeDict.keys()
        
    def _computeMinNxN(self, probeList, galleryList):
        minimum = DetectionDifference(probeList[0], galleryList[0])
        for probe in probeList:
            for gallery in galleryList:
                tmp = DetectionDifference(probe, gallery)
                if(DetectionDifference.compare(tmp,minimum)<0):
                    minimum=tmp
        return minimum