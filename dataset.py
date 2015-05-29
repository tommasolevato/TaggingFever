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
    
    def buildDictFromSet(self, set, N):
        assert N==3 or N==5 or N==10 
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
        probeDict = self.buildDictFromSet(self.probeSet,N)
        galleryDict = self.buildDictFromSet(self.gallerySet,N)
    
    def getKeys(self):
        #assert not self.probeDict == {}
        return self.probeDict.keys()
        
    def computeMinNxN(self, peopleid):
        min = 1000000
        for probe in probeDict[peopleid]:
            for gallery in galleryDict[peopleid]:
                tmp = DetectionDifference(probe, gallery).computeDistance()
                if(tmp<min):
                    min=tmp
                    
        return min
    
    