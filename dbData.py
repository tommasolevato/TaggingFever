from config import Config
import MySQLdb
from detection import Detection
import pickle
import time

class DBData:
    probes = []
    galleries = {}
    traceProbes = {}
    traceGallery1 = {}
    traceGallery2 = {}
    traceGallery3 = {}
    traceGallery4 = {}
           
    @staticmethod
    def initialize(args):
        DBData.height = args['height']
        DBData.visibilityRatio = args['visibility_ratio']
        DBData.descriptor = args['descriptor']
        DBData.cam = args['cam']
        #TODO: change to real value
        #DBData.traceType = 4
        DBData._connectToDB()
        #TODO: uncomment
        DBData._loadDataFromDB()
        
    @staticmethod
    def initializeWithSingleValues(h, v, d, c):
        DBData.height = h
        DBData.visibilityRatio = v
        DBData.descriptor = d
        DBData.cam = c
        DBData._connectToDB()
        DBData._loadDataFromDB()
            
    @staticmethod
    def _connectToDB():
        DBData.db = MySQLdb.connect(**Config.getAllDbParams())
        DBData.probeCursor = DBData.db.cursor()
        DBData.galleryCursor = DBData.db.cursor()
        DBData.tracesProbeCursor = DBData.db.cursor()
        DBData.tracesGalleryCursor = DBData.db.cursor()
       
    @staticmethod 
    def _loadDataFromDB():
        DBData.probeSelect = "select des.desc_value_pickle, pp.peopleid from cam1.description as des, cam1.detection as det, mnemosyne.people as pp where det.detection_type_id=5 and des.description_type_id=" + str(DBData.descriptor) + " and des.detection_id=det.id and det.x<753 and det.y>121 and det.h>" + str(DBData.height) + " and pp.cameraid='C1' and pp.bb_x=det.x and pp.bb_y=det.y and pp.bb_width=det.w and pp.bb_height=det.h and pp.bb_width*pp.bb_height * " + str(DBData.visibilityRatio) + " <= pp.bbV_width*pp.bbV_height and cast(SUBSTRING_INDEX(pp.frameid, 'F', -1) as unsigned)=des.image_id;"
        DBData.cam1GallerySelect = "select des.desc_value_pickle, pp.peopleid from cam1.description as des, cam1.detection as det, mnemosyne.people as pp where det.detection_type_id=5 and des.description_type_id=" + str(DBData.descriptor) + " and des.detection_id=det.id and not (det.x<753 and det.y>121) and det.h>" + str(DBData.height) + " and pp.cameraid='C1' and pp.bb_x=det.x and pp.bb_y=det.y and pp.bb_width=det.w and pp.bb_height=det.h and pp.bb_width*pp.bb_height * " + str(DBData.visibilityRatio) + " <= pp.bbV_width*pp.bbV_height and cast(SUBSTRING_INDEX(pp.frameid, 'F', -1) as unsigned)=des.image_id;"
        DBData.cam2GallerySelect = "select des.desc_value_pickle, pp.peopleid from cam2.description as des, cam2.detection as det, mnemosyne.people as pp where det.detection_type_id=5 and des.description_type_id=" + str(DBData.descriptor) + " and des.detection_id=det.id and det.h>" + str(DBData.height) + " and pp.cameraid='C2' and pp.bb_x=det.x and pp.bb_y=det.y and pp.bb_width=det.w and pp.bb_height=det.h and pp.bb_width*pp.bb_height * " + str(DBData.visibilityRatio) + " <= pp.bbV_width*pp.bbV_height and cast(SUBSTRING_INDEX(pp.frameid, 'F', -1) as unsigned)=des.image_id;"
        DBData.cam3GallerySelect = "select des.desc_value_pickle, pp.peopleid from cam3.description as des, cam3.detection as det, mnemosyne.people as pp where det.detection_type_id=5 and des.description_type_id=" + str(DBData.descriptor) + " and des.detection_id=det.id and det.h>" + str(DBData.height) + " and pp.cameraid='C3' and pp.bb_x=det.x and pp.bb_y=det.y and pp.bb_width=det.w and pp.bb_height=det.h and pp.bb_width*pp.bb_height * " + str(DBData.visibilityRatio) + " <= pp.bbV_width*pp.bbV_height and cast(SUBSTRING_INDEX(pp.frameid, 'F', -1) as unsigned)=des.image_id;"
        DBData.cam4GallerySelect = "select des.desc_value_pickle, pp.peopleid from cam4.description as des, cam4.detection as det, mnemosyne.people as pp where det.detection_type_id=5 and des.description_type_id=" + str(DBData.descriptor) + " and des.detection_id=det.id and det.h>" + str(DBData.height) + " and pp.cameraid='C4' and pp.bb_x=det.x and pp.bb_y=det.y and pp.bb_width=det.w and pp.bb_height=det.h and pp.bb_width*pp.bb_height * " + str(DBData.visibilityRatio) + " <= pp.bbV_width*pp.bbV_height and cast(SUBSTRING_INDEX(pp.frameid, 'F', -1) as unsigned)=des.image_id;"
        DBData._loadProbeData()
        DBData._loadGalleryData()
        
    @staticmethod 
    def loadTracesProbeData():
        DBData._connectToDB()
        select = "SELECT t1.acc_model_id, t1.desc_value_pickle, t2.peopleid  FROM cam1.trace_description as t1, cam1.trace_peopleid as t2 where t1.acc_model_id=t2.acc_model_id and t1.peopleid=t2.peopleid and t1.x<753 and t1.y>121 and t1.acc_model_type_id=4;"
        DBData.tracesProbeCursor.execute(select)
        for rawData in DBData.tracesProbeCursor:
            traceid = rawData[0]
            peopleid = rawData[2]
            description = pickle.loads(rawData[1])
            if traceid not in DBData.traceProbes:
                DBData.traceProbes[traceid] = [Detection(peopleid, description)]
            else:
                DBData.traceProbes[traceid].append(Detection(peopleid, description))
        #TODO: ci vuole una get
        return DBData.traceProbes
        
    @staticmethod 
    def loadTracesGalleryData():
        DBData._connectToDB()
        cam1GallerySelect = "SELECT t1.acc_model_id, t1.desc_value_pickle, t2.peopleid  FROM cam1.trace_description as t1, cam1.trace_peopleid as t2 where t1.acc_model_id=t2.acc_model_id and not (t1.x<753 and t1.y>121) and t1.acc_model_type_id=" + `DBData.traceType` + ";"
        cam2GallerySelect = "SELECT t1.acc_model_id, t1.desc_value_pickle, t2.peopleid  FROM cam2.trace_description as t1, cam2.trace_peopleid as t2 where t1.acc_model_id=t2.acc_model_id and t1.acc_model_type_id=" + `DBData.traceType` + ";"
        cam3GallerySelect = "SELECT t1.acc_model_id, t1.desc_value_pickle, t2.peopleid  FROM cam3.trace_description as t1, cam3.trace_peopleid as t2 where t1.acc_model_id=t2.acc_model_id and t1.acc_model_type_id=" + `DBData.traceType` + ";"
        cam4GallerySelect = "SELECT t1.acc_model_id, t1.desc_value_pickle, t2.peopleid  FROM cam4.trace_description as t1, cam4.trace_peopleid as t2 where t1.acc_model_id=t2.acc_model_id and t1.acc_model_type_id=" + `DBData.traceType` + ";"
        
#         DBData.tracesGalleryCursor.execute(cam1GallerySelect)
#         for rawData in DBData.tracesGalleryCursor:
#             traceid = rawData[0]
#             description = pickle.loads(rawData[1])
#             peopleid = rawData[2]
#             if traceid not in DBData.traceGallery1:
#                 DBData.traceGallery1[traceid] = [Detection(peopleid, description)]
#             else:
#                 DBData.traceGallery1[traceid].append(Detection(peopleid, description))
#         print "loaded"
#         DBData.tracesGalleryCursor.execute(cam2GallerySelect)
#         for rawData in DBData.tracesGalleryCursor:
#             traceid = rawData[0]
#             description = rawData[1]
#             peopleid = rawData[2]
#             if traceid not in DBData.traceGallery2:
#                 DBData.traceGallery2[traceid] = [Detection(peopleid, description)]
#             else:
#                 DBData.traceGallery2[traceid].append(Detection(peopleid, description))
#         print "loaded" 
#         DBData.tracesGalleryCursor.execute(cam3GallerySelect)
#         for rawData in DBData.tracesGalleryCursor:
#             traceid = rawData[0]
#             description = rawData[1]
#             peopleid = rawData[2]
#             if traceid not in DBData.traceGallery3:
#                 DBData.traceGallery3[traceid] = [Detection(peopleid, description)]
#             else:
#                 DBData.traceGallery3[traceid].append(Detection(peopleid, description))
#         print "loaded"
        DBData.tracesGalleryCursor.execute(cam4GallerySelect)
        for rawData in DBData.tracesGalleryCursor:
            traceid = rawData[0]
            description = pickle.loads(rawData[1])
            peopleid = rawData[2]
            if traceid not in DBData.traceGallery4:
                DBData.traceGallery4[traceid] = [Detection(peopleid, description)]
            else:
                DBData.traceGallery4[traceid].append(Detection(peopleid, description))
        print "loaded"
    @staticmethod
    def _loadProbeData():
        DBData.probes = []
        start = time.time()
        DBData.probeCursor.execute(DBData.probeSelect)
        for rawProbeData in DBData.probeCursor:
            DBData.probes.append(Detection(rawProbeData[1], pickle.loads(rawProbeData[0])))
        print "Finished loading probe data in " + "{0:.2f}".format(time.time() - start) + " seconds."
        
    @staticmethod       
    def _loadGalleryData():
        start = time.time()
        DBData._loadSingleGalleryData(DBData.cam1GallerySelect, 1)
        DBData._loadSingleGalleryData(DBData.cam2GallerySelect, 2)
        DBData._loadSingleGalleryData(DBData.cam3GallerySelect, 3)
        DBData._loadSingleGalleryData(DBData.cam4GallerySelect, 4)
        print "Finished loading gallery data in " + "{0:.2f}".format(time.time() - start) + " seconds."
    
    #TODO: horrible signature (camera number)
    @staticmethod
    def _loadSingleGalleryData(gallerySelect, cam):
        data = []
        DBData.galleryCursor.execute(gallerySelect)
        for rawGalleryData in DBData.galleryCursor:
            data.append(Detection(rawGalleryData[1], pickle.loads(rawGalleryData[0])))
        DBData.galleries[cam] = data
        
    @staticmethod
    def getCameraGalleryData(cam):
        return DBData.galleries[cam]
    
    @staticmethod
    def getTraceProbeData():
        return DBData.traceProbes
    
    @staticmethod    
    def getTraceGalleryData(cam):
        if cam==1:
            return DBData.traceGallery1
        if cam==2:
            return DBData.traceGallery2
        if cam==3:
            return DBData.traceGallery3
        if cam==4:
            return DBData.traceGallery4
        
        
    @staticmethod
    def getAllGalleryData():
        tmp = []
        for cam in DBData.galleries.values():
            tmp = tmp + cam
        return tmp