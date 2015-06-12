from __future__ import division
from detectionDifference import DetectionDifference
import random

class Dataset:
    
    def __init__(self, probeSet, gallerySet, camera, descriptor):
        self.probeSet = probeSet
        self.gallerySet = gallerySet
        self.camera = camera
        self.descriptor = descriptor
        self.probeDict = {}
        self.galleryDict = {}
        self._prepareDictionaries()
        
    # TODO: change name and signature
    def getRanking(self, probe):
        euclideanDistances = []
        for gallery in self.gallerySet:
            euclideanDistances.append(DetectionDifference(probe, gallery))
        ranking = sorted(euclideanDistances, cmp=DetectionDifference.compare)
        return ranking
            
    def getRankingMvsM(self, peopleid, N):
        probe = self.chooseProbeSubList(peopleid, N)
        gallery = self.chooseGallerySubDict(N)
        euclideanDistances = []
        for galleryId in gallery:
            euclideanDistances.append(self._computeMinNxN(probe, gallery[galleryId]))
        ranking = sorted(euclideanDistances, cmp=DetectionDifference.compare)
        return ranking
    
    def getRankingSvsAll(self, peopleid):
        probe = self.chooseProbeSubList(peopleid, 1)[0]
        euclideanDistances = []
        for gallery in self.gallerySet:
            euclideanDistances.append(DetectionDifference(probe, gallery))
        ranking = sorted(euclideanDistances, cmp=DetectionDifference.compare)
        return ranking
    
    #TODO: change name (not dict, list)
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
            
    #TODO: change name (not dict, list)
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