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
 
    def getRankingMvsM(self, peopleid):
        euclideanDistances = []
        self.galleryDict.keys()
        for galleryPeopleId in self.galleryDict.keys():
            euclideanDistances.append(self.computeMinNxN(peopleid, galleryPeopleId))
        ranking = sorted(euclideanDistances, cmp=DetectionDifference.compare)
        return ranking
    
    def buildDictFromSet(self, set, N):
        assert N==1 or N==3 or N==5 or N==10 
        galleryPerPeopleId = {}
        for gallery in set:
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
    
    def prepareDictionariesMvsM(self, N):
        self.probeDict = self.buildDictFromSet(self.probeSet,N)
        galleryDictComplete = self.buildDictFromSet(self.gallerySet,N)
        for peopleid in self.probeDict:
            assert peopleid in galleryDictComplete #fallisce nel caso in cui nella gallery manchi un id che invece si trova nel probe
            self.galleryDict[peopleid] = galleryDictComplete[peopleid]
    
    def getProbeKeys(self):
        assert not self.probeDict == {}
        return self.probeDict.keys()
        
    def computeMinNxN(self, probePeopleId, galleryPeopleId):
        min = DetectionDifference(self.probeDict[probePeopleId][0], self.galleryDict[galleryPeopleId][0])
        for probe in self.probeDict[probePeopleId]:
            for gallery in self.galleryDict[galleryPeopleId]:
                tmp = DetectionDifference(probe, gallery)
                if(DetectionDifference.compare(tmp,min)<0):
                    min=tmp
        return min