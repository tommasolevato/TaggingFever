from config import Config
import MySQLdb
from detection import Detection
import pickle

class DBData:
    probes = []
    galleries = []
            
    @staticmethod
    def initialize():
        DBData.connectToDB()
        DBData.getDataFromDB()
            
    @staticmethod
    def connectToDB():
        DBData.db = MySQLdb.connect(**Config.getAllParams())
        DBData.probeCursor = DBData.db.cursor()
        DBData.galleryCursor = DBData.db.cursor()
       
    @staticmethod 
    def getDataFromDB():
        DBData.probeSelect = "select des.desc_value_pickle, pp.peopleid from cam1.description as des, cam1.detection as det, mnemosyne.people as pp where des.detection_id=det.id and det.x<753 and det.y>121 and det.h>30 and pp.cameraid='C1' and pp.bb_x=det.x and pp.bb_y=det.y and pp.bb_width=det.w and pp.bb_height=det.h and cast(SUBSTRING_INDEX(pp.frameid, 'F', -1) as unsigned)=des.image_id;"
        DBData.cam1GallerySelect = "select des.desc_value_pickle, pp.peopleid from cam1.description as des, cam1.detection as det, mnemosyne.people as pp where des.detection_id=det.id and not (det.x<753 and det.y>121) and det.h>30 and pp.cameraid='C1' and pp.bb_x=det.x and pp.bb_y=det.y and pp.bb_width=det.w and pp.bb_height=det.h and cast(SUBSTRING_INDEX(pp.frameid, 'F', -1) as unsigned)=des.image_id;"
        DBData.cam2GallerySelect = "select des.desc_value_pickle, pp.peopleid from cam2.description as des, cam2.detection as det, mnemosyne.people as pp where des.detection_id=det.id and det.h>30 and pp.cameraid='C2' and pp.bb_x=det.x and pp.bb_y=det.y and pp.bb_width=det.w and pp.bb_height=det.h and cast(SUBSTRING_INDEX(pp.frameid, 'F', -1) as unsigned)=des.image_id;"
        DBData.cam3GallerySelect = "select des.desc_value_pickle, pp.peopleid from cam3.description as des, cam3.detection as det, mnemosyne.people as pp where des.detection_id=det.id and det.h>30 and pp.cameraid='C3' and pp.bb_x=det.x and pp.bb_y=det.y and pp.bb_width=det.w and pp.bb_height=det.h and cast(SUBSTRING_INDEX(pp.frameid, 'F', -1) as unsigned)=des.image_id;"
        DBData.cam4GallerySelect = "select des.desc_value_pickle, pp.peopleid from cam4.description as des, cam4.detection as det, mnemosyne.people as pp where des.detection_id=det.id and det.h>30 and pp.cameraid='C4' and pp.bb_x=det.x and pp.bb_y=det.y and pp.bb_width=det.w and pp.bb_height=det.h and cast(SUBSTRING_INDEX(pp.frameid, 'F', -1) as unsigned)=des.image_id;"
        DBData.getProbeData()
        DBData.getGalleryData()
        
    @staticmethod
    def getProbeData():
        DBData.probeCursor.execute(DBData.probeSelect)
        for rawProbeData in DBData.probeCursor:
            DBData.probes.append(Detection(rawProbeData[1], pickle.loads(rawProbeData[0])))
    
    @staticmethod       
    def getGalleryData():
        DBData.getSingleGalleryData(DBData.cam1GallerySelect)
        DBData.getSingleGalleryData(DBData.cam2GallerySelect)
        DBData.getSingleGalleryData(DBData.cam3GallerySelect)
        DBData.getSingleGalleryData(DBData.cam4GallerySelect)
    
    @staticmethod
    def getSingleGalleryData(gallerySelect):
        DBData.galleryCursor.execute(gallerySelect)
        for rawGalleryData in DBData.galleryCursor:
            DBData.galleries.append(Detection(rawGalleryData[1], pickle.loads(rawGalleryData[0])))