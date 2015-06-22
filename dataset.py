from dbData import DBData

class DetectionsDataset:
    
    def __init__(self, h, v, d, c):
        self.height = h
        self.ratio = v
        self.descriptor = d
        self.cam = c
    
    def getProbeSet(self):
        DBData.initializeDetectionsParams(self.height, self.ratio, self.descriptor, self.cam)
        return DBData.getProbeData()
    
    def getGallerySet(self):
        DBData.initializeDetectionsParams(self.height, self.ratio, self.descriptor, self.cam)
        return DBData.getGalleryData(self.cam)

class TracesDataset:
    def __init__(self, c, t, a):
        self.cam = c
        self.traceType = t
        self.averageStrategy = a
    
    def getProbeSet(self):
        DBData.initializeTracesParams(self.cam, self.traceType, self.averageStrategy)
        return DBData.getProbeTraces()
    
    def getGallerySet(self):
        DBData.initializeTracesParams(self.cam, self.traceType, self.averageStrategy)
        return DBData.getGalleryTraces(self.cam)