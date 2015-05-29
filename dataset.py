from detectionDifference import DetectionDifference
import random

class Dataset:
    
    def __init__(self, probeSet, gallerySet):
        self.probeSet = probeSet
        self.gallerySet = gallerySet
        
    # TODO: change name and signature
    def getRanking(self, probe):
        euclideanDistances = []
        for gallery in self.gallerySet:
            euclideanDistances.append(DetectionDifference(probe, gallery))
        ranking = sorted(euclideanDistances, cmp=DetectionDifference.compare)
        return ranking
    
    def extractNdetectionPerId(self, N):
        galleryPerPeopleId = {}
        for gallery in self.gallerySet:
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
