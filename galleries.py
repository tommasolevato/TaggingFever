import MySQLdb
from config import Config
import argparse
import descriptorIO
import numpy

parser = argparse.ArgumentParser()
parser.add_argument('height', type=int)
parser.add_argument('visibility_ratio', type=float)
parser.add_argument('#probes', type=int)
args = parser.parse_args()
args = vars(args)
probes = args['#probes']


db = MySQLdb.connect(**Config.getAllParams())
cursor = db.cursor()

if probes==1:
    select = "select peopleid, count(peopleid) from people where cameraid='C1' and bb_height > " + args['height'].__str__() + " and bb_x<320 and bb_y>193 and bb_width*bb_height *" + args["visibility_ratio"].__str__() + "< bbV_width*bbV_height group by peopleid;"
elif probes==3:
    select = "select peopleid, count(peopleid) from people where cameraid='C1' and bb_height > " + args['height'].__str__() + " and bb_x<348 and bb_y>192 and bb_width*bb_height *" + args["visibility_ratio"].__str__() + "< bbV_width*bbV_height group by peopleid;"
elif probes==5:
    select = "select peopleid, count(peopleid) from people where cameraid='C1' and bb_height > " + args['height'].__str__() + " and bb_x<582 and bb_y>129 and bb_width*bb_height *" + args["visibility_ratio"].__str__() + "< bbV_width*bbV_height group by peopleid;"
elif probes==10:
    select = "select peopleid, count(peopleid) from people where cameraid='C1' and bb_height > " + args['height'].__str__() + " and bb_x<753 and bb_y>121 and bb_width*bb_height *" + args["visibility_ratio"].__str__() + "< bbV_width*bbV_height group by peopleid;"
    
cursor.execute(select)
#print len(cursor.fetchall())

parser = descriptorIO.DescriptorIO()


x = numpy.load('/home/tommaso/description-desc_value_pickle.bin')
y = numpy.load('/home/tommaso/description-desc_value_pickle2.bin')
print len(x)

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