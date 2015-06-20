from dbData import DBData

#contiene i set di probe e gallery di interesse (dati al costruttore) e si occupa di calcolare i ranking
#TODO: non passare i set ma prenderli dal db
class DetectionsDataset:
    
    def __init__(self, args):
        self.height = args['height']
        self.ratio = args['visibility_ratio']
        self.descriptor = args['descriptor']
        self.cam = args['cam']
    
    def getProbeSet(self):
        DBData.initializeDetectionsParams(self.height, self.ratio, self.descriptor, self.cam)
        return DBData.getProbeData()
    
    def getGallerySet(self):
        DBData.initializeDetectionsParams(self.height, self.ratio, self.descriptor, self.cam)
        return DBData.getGalleryData(self.cam)

class TracesDataset:
    def __init__(self, args):
        self.cam = args['cam']
        self.traceType = args['trace_type']
    
    def getProbeSet(self):
        DBData.initializeTracesParams(self.cam, self.traceType)
        return DBData.getProbeTraces()
    
    def getGallerySet(self):
        DBData.initializeTracesParams(self.cam, self.traceType)
        return DBData.getGalleryTraces(self.cam)
    
#     def getRankingTrace(self, probe, galleries):
#         euclideanDistances = []
#         for gallery in galleries:
#             euclideanDistances.append(DetectionDifference(probe, gallery))
#         ranking = sorted(euclideanDistances, cmp=DetectionDifference.compare)
#         return ranking
#     
#     def _prepareTraceSets(self, traceProbesDict, traceGalleriesDict):
#         probes = []
#         galleries = []
#         for k in traceProbesDict:
#             listToChooseFrom = traceProbesDict[k]
#             detection = random.choice(listToChooseFrom)
#             probes.append(detection)
#         raw_input()
#         for k in traceGalleriesDict:
#             listToAverage = traceGalleriesDict[k]
#             desc = self._average(listToAverage)
#             print listToAverage[0].getPersonId()
#             galleries.append(Detection(listToAverage[0].getPersonId(), desc))
#         return probes, galleries
#     
#     def _average(self, list):
#         sum = numpy.zeros(len(list[0].getPersonDescription()))
#         for detection in list:
#             sum = sum + detection.getPersonDescription()
#         return numpy.divide(sum, len(list))
#     
#     def verifyN(self, N):
#         probeDict = self.chooseProbeSubDict(N)
#         galleryDict = self.chooseGallerySubDict(N)
#         distractors = []
#         for probe in probeDict:
#             if len(probeDict[probe]) < N:
#                 print "Not enough detections for id " + str(probe) + " in probe set."
#             if probe not in galleryDict:
#                 print "There are no galleries for id " + str(probe) + "."
#         for gallery in galleryDict:
#             if len(galleryDict[gallery]) < N:
#                 print "Not enough detections for id " + str(gallery) + " in gallery set."
#             if gallery not in probeDict:
#                 distractors.append(gallery)
#         print "There are " + str(len(distractors)) + " distractors: " + str(distractors)