import MySQLdb
from config import Config
import argparse
import descriptorIO
import numpy
import pickle
import detection
import time
from descriptorDifference import DescriptorDifference
import matplotlib.pyplot as plt


def rank_n(distances, rank):
    for i in range(0, rank+1):
        if distances[0].getProbeId() == distances[i].getTestId():
            return 1
    return 0

parser = argparse.ArgumentParser()
parser.add_argument('height', type=int)
parser.add_argument('visibility_ratio', type=float)
parser.add_argument('#probes', type=int)
args = parser.parse_args()
args = vars(args)
probes = args['#probes']


db = MySQLdb.connect(**Config.getAllParams())
probeCursor = db.cursor()
testCursor = db.cursor()
# if probes==1:
probeSelect = "select des.desc_value_pickle, pp.peopleid from cam1.description as des, cam1.detection as det, mnemosyne.people as pp where des.detection_id=det.id and det.x<753 and det.y>121 and det.h>30 and pp.cameraid='C1' and pp.bb_x=det.x and pp.bb_y=det.y and pp.bb_width=det.w and pp.bb_height=det.h and cast(SUBSTRING_INDEX(pp.frameid, 'F', -1) as unsigned)=des.image_id;"

cam1Gallery = "select des.desc_value_pickle, pp.peopleid from cam1.description as des, cam1.detection as det, mnemosyne.people as pp where des.detection_id=det.id and not (det.x<753 and det.y>121) and det.h>30 and pp.cameraid='C1' and pp.bb_x=det.x and pp.bb_y=det.y and pp.bb_width=det.w and pp.bb_height=det.h and cast(SUBSTRING_INDEX(pp.frameid, 'F', -1) as unsigned)=des.image_id;"
cam2Gallery = "select des.desc_value_pickle, pp.peopleid from cam2.description as des, cam2.detection as det, mnemosyne.people as pp where des.detection_id=det.id and det.h>30 and pp.cameraid='C2' and pp.bb_x=det.x and pp.bb_y=det.y and pp.bb_width=det.w and pp.bb_height=det.h and cast(SUBSTRING_INDEX(pp.frameid, 'F', -1) as unsigned)=des.image_id;"
cam3Gallery = "select des.desc_value_pickle, pp.peopleid from cam3.description as des, cam3.detection as det, mnemosyne.people as pp where des.detection_id=det.id and det.h>30 and pp.cameraid='C3' and pp.bb_x=det.x and pp.bb_y=det.y and pp.bb_width=det.w and pp.bb_height=det.h and cast(SUBSTRING_INDEX(pp.frameid, 'F', -1) as unsigned)=des.image_id;"
cam4Gallery = "select des.desc_value_pickle, pp.peopleid from cam4.description as des, cam4.detection as det, mnemosyne.people as pp where des.detection_id=det.id and det.h>30 and pp.cameraid='C4' and pp.bb_x=det.x and pp.bb_y=det.y and pp.bb_width=det.w and pp.bb_height=det.h and cast(SUBSTRING_INDEX(pp.frameid, 'F', -1) as unsigned)=des.image_id;"

howManyProbes = 0
rank1 = 0
rank2 = 0

start_time = time.time()

probeCursor.execute(probeSelect)

gallery = []

testCursor.execute(cam1Gallery)
for testRawData in testCursor:
    test = detection.Detection(testRawData[1], pickle.loads(testRawData[0]))
    gallery.append(test)

testCursor.execute(cam2Gallery) 
for testRawData in testCursor:
    test = detection.Detection(testRawData[1], pickle.loads(testRawData[0]))
    gallery.append(test)

testCursor.execute(cam3Gallery)
for testRawData in testCursor:
    test = detection.Detection(testRawData[1], pickle.loads(testRawData[0]))
    gallery.append(test)

testCursor.execute(cam4Gallery)
for testRawData in testCursor:
    test = detection.Detection(testRawData[1], pickle.loads(testRawData[0]))
    gallery.append(test)

elapsed_time = time.time() - start_time

print "Retrieved probes and galleries in " + elapsed_time.__str__() + " seconds."

rank = []
for i in range(0, 50):
    rank.append(0)

for probeRawData in probeCursor:
    
    start_time = time.time()
    
    probe = detection.Detection(probeRawData[1], pickle.loads(probeRawData[0]))
    howManyProbes += 1
    euclideanDistances = []
    
    for test in gallery:
        dif = DescriptorDifference(probe.getPersonId(), test.getPersonId(), numpy.linalg.norm(probe.getPersonDescription() - test.getPersonDescription()))
        euclideanDistances.append(dif)
        
    euclideanDistances = sorted(euclideanDistances, cmp=DescriptorDifference.compare)
#     if euclideanDistances[0].getProbeId() == euclideanDistances[0].getTestId():
#         rank1+=1
#     
#     elif euclideanDistances[0].getProbeId() == euclideanDistances[1].getTestId():
#         rank2+=1
    
    for i in range(0, len(rank)):
        rank[i] += rank_n(euclideanDistances, i)
    
    elapsed_time = time.time() - start_time
    print "Processed " + howManyProbes.__str__() + " probes in " + elapsed_time.__str__() + " seconds."
        
        
print "Number of probes: " + howManyProbes.__str__()
for i in range(0, len(rank)):
    print str(i+1) + ": " + str(float(rank[i]) / howManyProbes)

x = numpy.linspace(1, 50)
plt.plot(x,rank)
plt.show()

#cam1Total = "select des.desc_value_pickle, pp.peopleid from cam1.description as des, cam1.detection as det, mnemosyne.people as pp where des.detection_id=det.id and det.h>30 and pp.cameraid='C1' and pp.bb_x=det.x and pp.bb_y=det.y and pp.bb_width=det.w and pp.bb_height=det.h and cast(SUBSTRING_INDEX(pp.frameid, 'F', -1) as unsigned)=des.image_id;"
# elif probes==3:
#     select = "select peopleid, count(peopleid) from people where cameraid='C1' and bb_height > " + args['height'].__str__() + " and bb_x<348 and bb_y>192 and bb_width*bb_height *" + args["visibility_ratio"].__str__() + "< bbV_width*bbV_height group by peopleid;"
# elif probes==5:
#     select = "select peopleid, count(peopleid) from people where cameraid='C1' and bb_height > " + args['height'].__str__() + " and bb_x<582 and bb_y>129 and bb_width*bb_height *" + args["visibility_ratio"].__str__() + "< bbV_width*bbV_height group by peopleid;"
# elif probes==10:
#     select = "select peopleid, count(peopleid) from people where cameraid='C1' and bb_height > " + args['height'].__str__() + " and bb_x<753 and bb_y>121 and bb_width*bb_height *" + args["visibility_ratio"].__str__() + "< bbV_width*bbV_height group by peopleid;"
#     
#cursor.execute(cam1Total)
#print len(cursor.fetchall())

#print cursor.rowcount

#cam1 = MySQLdb.connect(host='localhost', user='root', passwd='eddie?54', db='cam1')
#cursor = cam1.cursor()



# select = "select desc_value_pickle from description"
# cursor.execute(select)
# # data = cursor.fetchone()[0]
# # while data is not None:
# for result in cursor:
#     data = result[0]
#     onthefly = pickle.loads(data)
# #     with open('test.bin', 'wb') as f:
# #         f.write(data)
# #     ondisk = numpy.load('test.bin')
# #     assert numpy.array_equal(onthefly, ondisk)
#     print numpy.sum(onthefly)
# print "done"

#print data[0]
# for i in range(0,40000):
#     with open('test.bin', 'wb') as f:
#         f.write(data)
#     x = numpy.load('test.bin')
#     #print len(x)
# print "done"
# print len(x)
# with open('/home/tommaso/description-desc_value_pickle.bin', 'rb') as f:
#     data = f.read()
# print data
# 
# x = numpy.load('/home/tommaso/description-desc_value_pickle.bin')
# y = numpy.load('/home/tommaso/description-desc_value_pickle2.bin')
# print numpy.sum(x)
# print numpy.sum(y)

# with open('/home/tommaso/description-desc_value_pickle.bin', 'rb') as f:
#    data = f.read()
# points, descriptors = parser.readDescriptors('/home/tommaso/description-desc_value_pickle.bin')
# print descriptors
#print data
#print args['height']


# db = MySQLdb.connect(**Config.getAllParams())
# 
# cursor = db.cursor()
# 
# cursor.execute("select * from people where peopleid in (select person from probe) and cameraid='C1' and bb_x<800 and bb_y>150")
# print len(cursor.fetchall())

#cursor.execute("select * from people where peopleid in (select person from probe) and not (cameraid='C1' and bb_x<800 and bb_y>150)")

#select * from people where peopleid in (select person from probe) and cameraid="C1" and bb_x<800 and bb_y>150;