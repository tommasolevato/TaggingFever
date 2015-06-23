from config import Config
import MySQLdb
from detection import Detection
import pickle
import time
from trace import Trace
from traceDescriptionStrategy import ProbeTraceStrategy

class DBData:
    parameters = {}
    probes = []
    galleries = {}
    traceProbes = {}
    traceGallery1 = {}
    traceGallery2 = {}
    traceGallery3 = {}
    traceGallery4 = {}
    probeSelect = "select des.desc_value_pickle, pp.peopleid from cam1.description as des, cam1.detection as det, mnemosyne.people as pp where det.detection_type_id=5 and des.description_type_id={descriptor} and des.detection_id=det.id and det.x<753 and det.y>121 and det.h>{height} and pp.cameraid='C1' and pp.bb_x=det.x and pp.bb_y=det.y and pp.bb_width=det.w and pp.bb_height=det.h and pp.bb_width*pp.bb_height * {ratio} <= pp.bbV_width*pp.bbV_height and cast(SUBSTRING_INDEX(pp.frameid, 'F', -1) as unsigned)=des.image_id;"
    gallery1Select = "select des.desc_value_pickle, pp.peopleid from cam1.description as des, cam1.detection as det, mnemosyne.people as pp where det.detection_type_id=5 and des.description_type_id={descriptor} and des.detection_id=det.id and not (det.x<753 and det.y>121) and det.h>{height} and pp.cameraid='C1' and pp.bb_x=det.x and pp.bb_y=det.y and pp.bb_width=det.w and pp.bb_height=det.h and pp.bb_width*pp.bb_height * {ratio} <= pp.bbV_width*pp.bbV_height and cast(SUBSTRING_INDEX(pp.frameid, 'F', -1) as unsigned)=des.image_id;"
    gallerySelect = "select des.desc_value_pickle, pp.peopleid from cam{cam}.description as des, cam{cam}.detection as det, mnemosyne.people as pp where det.detection_type_id=5 and des.description_type_id={descriptor} and des.detection_id=det.id and det.h>{height} and pp.cameraid='C{cam}' and pp.bb_x=det.x and pp.bb_y=det.y and pp.bb_width=det.w and pp.bb_height=det.h and pp.bb_width*pp.bb_height * {ratio} <= pp.bbV_width*pp.bbV_height and cast(SUBSTRING_INDEX(pp.frameid, 'F', -1) as unsigned)=des.image_id;"
    probeTraceSelect = "SELECT t1.acc_model_id, t1.desc_value_pickle, t2.peopleid, t1.peopleid  FROM cam1.trace_description as t1, cam1.trace_peopleid as t2 where t1.acc_model_id=t2.acc_model_id and t1.x<753 and t1.y>121 and t1.acc_model_type_id={trace_type};"
    gallery1TraceSelect = "SELECT t1.acc_model_id, t1.desc_value_pickle, t2.peopleid, t1.peopleid  FROM cam1.trace_description as t1, cam1.trace_peopleid as t2 where t1.acc_model_id=t2.acc_model_id and not (t1.x<753 and t1.y>121) and t1.acc_model_type_id={trace_type};"
    galleryTraceSelect = "SELECT t1.acc_model_id, t1.desc_value_pickle, t2.peopleid, t1.peopleid  FROM cam{cam}.trace_description as t1, cam{cam}.trace_peopleid as t2 where t1.acc_model_id=t2.acc_model_id and t1.acc_model_type_id={trace_type};"
        
    @staticmethod
    def initializeDetectionsParams(h, v, d, c):
        DBData.height = h
        DBData.visibilityRatio = v
        DBData.descriptor = d
        DBData.cam = c
       
    @staticmethod
    def initializeTracesParams(c, t, a):
        DBData.__cam = c
        DBData.traceType = t
        DBData.averageStrategy = a
        
    @staticmethod
    def getProbeData():
        start = time.time()
        select = DBData.probeSelect.format(descriptor = DBData.descriptor, height = DBData.height, ratio = DBData.visibilityRatio)
        probes = DBData.__getDetectionsData(select)
        print "Finished loading probe data in " + "{0:.2f}".format(time.time() - start) + " seconds."
        return probes
    
    @staticmethod
    def getGalleryData(cam):
        if cam==0:
            return DBData.getAllGalleryData()
        else:
            if cam==1:
                select = DBData.gallery1Select.format(descriptor = DBData.descriptor, height = DBData.height, ratio = DBData.visibilityRatio)
            else:
                select = DBData.gallerySelect.format(descriptor = DBData.descriptor, height = DBData.height, ratio = DBData.visibilityRatio, cam = DBData.cam)
            start = time.time()
            galleries = DBData.__getDetectionsData(select)
            print "Finished loading __cam" + str(cam) + " gallery data in " + "{0:.2f}".format(time.time() - start) + " seconds."
            return galleries
    
    @staticmethod
    def __getDetectionsData(select):
        toReturn = []
        connection = MySQLdb.connect(**Config.getAllDbParams())
        cursor = connection.cursor()
        cursor.execute(select)
        for rawProbeData in cursor:
            toReturn.append(Detection(rawProbeData[1], pickle.loads(rawProbeData[0])))
        cursor.close()
        connection.close()
        return toReturn

    @staticmethod 
    def getProbeTraces():
        start = time.time()
        select = DBData.probeTraceSelect.format(trace_type=DBData.traceType)
        probes = DBData.__getTracesData(select, ProbeTraceStrategy())
        print "Finished loading probes traces in " + "{0:.2f}".format(time.time() - start) + " seconds."
        return probes
    
    @staticmethod 
    def getGalleryTraces(cam):
        if cam==0:
            return DBData.getAllGalleryTraces()
        if cam==1:
            select = DBData.gallery1TraceSelect.format(trace_type=DBData.traceType)
        else:
            select = DBData.galleryTraceSelect.format(trace_type=DBData.traceType, cam=cam)
        start = time.time()
        toReturn = DBData.__getTracesData(select, DBData.averageStrategy)
        print "Finished loading __cam" + str(cam) + " gallery traces in " + "{0:.2f}".format(time.time() - start) + " seconds."
        return toReturn
    
    @staticmethod
    def __getTracesData(select, strategy):
        connection = MySQLdb.connect(**Config.getAllDbParams())
        cursor = connection.cursor()
        cursor.execute(select)
        traces = {}
        mainIds = {}
        for rawData in cursor:
            traceid = rawData[0]
            description = pickle.loads(rawData[1])
            mainId = rawData[2]
            peopleid = rawData[3]
            if traceid not in traces:
                traces[traceid] = [Detection(peopleid, description)]
                mainIds[traceid] = mainId
            else:
                traces[traceid].append(Detection(peopleid, description))
        toReturn = []
        for traceId in traces:
            toReturn.append(Trace(traceId, traces[traceId], strategy, mainIds[traceId]))
        cursor.close()
        connection.close()
        return toReturn
    
    #TODO: template method
    @staticmethod    
    def getAllGalleryData():
        galleries = []
        for i in range(0,4):
            galleries += DBData.getCameraGalleryData(i)
        return galleries
        
    @staticmethod
    def getAllGalleryTraces():
        galleries = []
        for i in range(0,4):
            galleries += DBData.getGalleryTraces(i)
        return galleries