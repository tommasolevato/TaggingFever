from detectionDifference import DetectionDifference
import random

class Dataset:
    
    def __init__(self, probeSet, gallerySet):
        self.probeSet = probeSet
        self.gallerySet = gallerySet
        self.probeDict = {}
        self.galleryDict = {}
        
    # TODO: change name and signature
    def getRanking(self, probe):
        euclideanDistances = []
        for gallery in self.gallerySet:
            euclideanDistances.append(DetectionDifference(probe, gallery))
        ranking = sorted(euclideanDistances, cmp=DetectionDifference.compare)
        return ranking
 
    def getRankingMvsM(self, peopleid, N):
        self._prepareDictionariesMvsM(N)
        euclideanDistances = []
        for galleryPeopleId in self.galleryDict.keys():
            euclideanDistances.append(self._computeMinNxN(peopleid, galleryPeopleId))
        ranking = sorted(euclideanDistances, cmp=DetectionDifference.compare)
        return ranking
    
    #TODO: split in more submethods
    def _buildDictFromSet(self, detectionSet, N):
        assert N==1 or N==3 or N==5 or N==10 
        galleryPerPeopleId = {}
        for gallery in detectionSet:
            if(gallery.getPersonId() not in galleryPerPeopleId):
                galleryPerPeopleId[gallery.getPersonId()] = [gallery]
            else:
                galleryPerPeopleId[gallery.getPersonId()].append(gallery)
        galleryMvsM = {}
        for personId in galleryPerPeopleId.keys():
            galleryMvsM[personId] = []
            addedDetectionsPerId = 0 
            assert len(galleryPerPeopleId[personId]) >= N
            while(addedDetectionsPerId < N):
                detectionToAdd = random.choice(galleryPerPeopleId[personId])
                if(detectionToAdd not in galleryMvsM):
                    galleryMvsM[personId].append(detectionToAdd)
                    addedDetectionsPerId += 1
            assert len(galleryMvsM[personId]) == N
        return galleryMvsM
    
    def _prepareDictionariesMvsM(self, N):
        self.probeDict = self._buildDictFromSet(self.probeSet,N)
        galleryDictComplete = self._buildDictFromSet(self.gallerySet,N)
        for peopleid in self.probeDict:
            assert peopleid in galleryDictComplete #fallisce nel caso in cui nella gallery manchi un id che invece si trova nel probe
            self.galleryDict[peopleid] = galleryDictComplete[peopleid]
    
    def getProbeKeys(self, N):
        self._prepareDictionariesMvsM(N)
        assert not self.probeDict == {}
        return self.probeDict.keys()
        
    def _computeMinNxN(self, probePeopleId, galleryPeopleId):
        minimum = DetectionDifference(self.probeDict[probePeopleId][0], self.galleryDict[galleryPeopleId][0])
        for probe in self.probeDict[probePeopleId]:
            for gallery in self.galleryDict[galleryPeopleId]:
                tmp = DetectionDifference(probe, gallery)
                if(DetectionDifference.compare(tmp,minimum)<0):
                    minimum=tmp
        return minimum