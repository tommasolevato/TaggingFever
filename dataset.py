from dbData import DBData

class DetectionsDataset:
    
    def __init__(self, h, v, d, c):
        self.__height = h
        self.__ratio = v
        self.__descriptor = d
        self.__cam = c
    
    def getProbeSet(self):
        DBData.initializeDetectionsParams(self.__height, self.__ratio, self.__descriptor, self.__cam)
        return DBData.getProbeData()
    
    def getGallerySet(self):
        DBData.initializeDetectionsParams(self.__height, self.__ratio, self.__descriptor, self.__cam)
        return DBData.getGalleryData(self.__cam)

class TracesDataset:
    def __init__(self, c, t, a):
        self.__cam = c
        self.traceType = t
        self.averageStrategy = a
    
    def getProbeSet(self):
        DBData.initializeTracesParams(self.__cam, self.traceType, self.averageStrategy)
        return DBData.getProbeTraces()
    
    def getGallerySet(self):
        DBData.initializeTracesParams(self.__cam, self.traceType, self.averageStrategy)
        return DBData.getGalleryTraces(self.__cam)