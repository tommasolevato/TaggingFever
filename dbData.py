from config import Config
import MySQLdb
from detection import Detection
import pickle
import time

class DBData:
    probes = []
    galleries = {}
           
    @staticmethod
    def initialize(args):
        DBData.height = args['height']
        DBData.visibilityRatio = args['visibility_ratio']
        DBData.descriptor = args['descriptor']
        DBData._connectToDB()
        DBData._loadDataFromDB()
            
    @staticmethod
    def _connectToDB():
        DBData.db = MySQLdb.connect(**Config.getAllParams())
        DBData.probeCursor = DBData.db.cursor()
        DBData.galleryCursor = DBData.db.cursor()
       
    @staticmethod 
    def _loadDataFromDB():
        DBData.probeSelect = "select des.desc_value_pickle, pp.peopleid from cam1.description as des, cam1.detection as det, mnemosyne.people as pp where des.description_type_id=" + str(DBData.descriptor) + " and des.detection_id=det.id and det.x<753 and det.y>121 and det.h>" + str(DBData.height) + " and pp.cameraid='C1' and pp.bb_x=det.x and pp.bb_y=det.y and pp.bb_width=det.w and pp.bb_height=det.h and pp.bb_width*pp.bb_height * " + str(DBData.visibilityRatio) + " <= pp.bbV_width*pp.bbV_height and cast(SUBSTRING_INDEX(pp.frameid, 'F', -1) as unsigned)=des.image_id;"
        DBData.cam1GallerySelect = "select des.desc_value_pickle, pp.peopleid from cam1.description as des, cam1.detection as det, mnemosyne.people as pp where des.description_type_id=" + str(DBData.descriptor) + " and des.detection_id=det.id and not (det.x<753 and det.y>121) and det.h>" + str(DBData.height) + " and pp.cameraid='C1' and pp.bb_x=det.x and pp.bb_y=det.y and pp.bb_width=det.w and pp.bb_height=det.h and pp.bb_width*pp.bb_height * " + str(DBData.visibilityRatio) + " <= pp.bbV_width*pp.bbV_height and cast(SUBSTRING_INDEX(pp.frameid, 'F', -1) as unsigned)=des.image_id;"
        DBData.cam2GallerySelect = "select des.desc_value_pickle, pp.peopleid from cam2.description as des, cam2.detection as det, mnemosyne.people as pp where des.description_type_id=" + str(DBData.descriptor) + " and des.detection_id=det.id and det.h>" + str(DBData.height) + " and pp.cameraid='C2' and pp.bb_x=det.x and pp.bb_y=det.y and pp.bb_width=det.w and pp.bb_height=det.h and pp.bb_width*pp.bb_height * " + str(DBData.visibilityRatio) + " <= pp.bbV_width*pp.bbV_height and cast(SUBSTRING_INDEX(pp.frameid, 'F', -1) as unsigned)=des.image_id;"
        DBData.cam3GallerySelect = "select des.desc_value_pickle, pp.peopleid from cam3.description as des, cam3.detection as det, mnemosyne.people as pp where des.description_type_id=" + str(DBData.descriptor) + " and des.detection_id=det.id and det.h>" + str(DBData.height) + " and pp.cameraid='C3' and pp.bb_x=det.x and pp.bb_y=det.y and pp.bb_width=det.w and pp.bb_height=det.h and pp.bb_width*pp.bb_height * " + str(DBData.visibilityRatio) + " <= pp.bbV_width*pp.bbV_height and cast(SUBSTRING_INDEX(pp.frameid, 'F', -1) as unsigned)=des.image_id;"
        DBData.cam4GallerySelect = "select des.desc_value_pickle, pp.peopleid from cam4.description as des, cam4.detection as det, mnemosyne.people as pp where des.description_type_id=" + str(DBData.descriptor) + " and des.detection_id=det.id and det.h>" + str(DBData.height) + " and pp.cameraid='C4' and pp.bb_x=det.x and pp.bb_y=det.y and pp.bb_width=det.w and pp.bb_height=det.h and pp.bb_width*pp.bb_height * " + str(DBData.visibilityRatio) + " <= pp.bbV_width*pp.bbV_height and cast(SUBSTRING_INDEX(pp.frameid, 'F', -1) as unsigned)=des.image_id;"
        DBData._loadProbeData()
        DBData._loadGalleryData()
        
    @staticmethod
    def _loadProbeData():
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
    def getAllGalleryData():
        tmp = []
        for cam in DBData.galleries.values():
            tmp = tmp + cam
        return tmp