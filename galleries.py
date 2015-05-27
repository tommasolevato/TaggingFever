# import argparse
# import numpy
# import pickle
# import time
# import matplotlib.pyplot as plt
# import random
from experiment import Experiment
from dbData import DBData
from rankingPerProbe import RankingPerProbe
from rankNAccuracy import RankNAccuracy

DBData.initialize()

totalRanking = RankingPerProbe(DBData.probes, DBData.galleries)
e = Experiment(totalRanking, 1)
for i in range(1,51):
    e.accuracyMeter = RankNAccuracy(i)
    print "Rank " + i.__str__() + ": " + e.computeAccuracy().__str__()

# def rank_n(distances, rank):
#     for i in range(0, rank+1):
#         if distances[0].probeId == distances[i].testId:
#             return 1
#     return 0
# 
# parser = argparse.ArgumentParser()
# parser.add_argument('height', type=int)
# parser.add_argument('visibility_ratio', type=float)
# parser.add_argument('#probes', type=int)
# args = parser.parse_args()
# args = vars(args)
# probes = args['#probes']
# 
# 
# 
# 
# 
# # if probes==1:
# 
# 
# 
# 
# howManyProbes = 0
# rank1 = 0
# rank2 = 0
# 
# start_time = time.time()
# 
# 
# 
# elapsed_time = time.time() - start_time
# 
# print "Retrieved probes and galleries in " + elapsed_time.__str__() + " seconds."
# 
# galleryPerPeopleId = {}
# for i in range(0, len(gallery)):
#     if( gallery[i].personId.__str__() not in galleryPerPeopleId ):
#         galleryPerPeopleId[gallery[i].personId.__str__()] = [i]
#     #elif(len(galleryPerPeoppleId[gallery[i].getPersonId()])<=3)
#     else:
#         galleryPerPeopleId[gallery[i].personId.__str__()].append(i)
# 
# galleryIndicesMVM = []
# for peopleid in galleryPerPeopleId.keys():
#     for i in range(0, probes):
#         galleryIndicesMVM.append(random.choice(galleryPerPeopleId[peopleid]))
# print galleryIndicesMVM
# 
# galleryMvsM = []
# for index in galleryIndicesMVM:
#     galleryMvsM.append(gallery[index])
# 
# 
# rank = []
# for i in range(0, 50):
#     rank.append(0)
# 
# for probeRawData in probeCursor:
#     
#     start_time = time.time()
#     
#     probe = detection.Detection(probeRawData[1], pickle.loads(probeRawData[0]))
#     howManyProbes += 1
#     euclideanDistances = []
#     
#     for test in gallery:
#         dif = DescriptorDifference(probe.personId, test.personId, numpy.linalg.norm(probe.description - test.description))
#         euclideanDistances.append(dif)
#         
#     euclideanDistances = sorted(euclideanDistances, cmp=DescriptorDifference.compare)
# #     if euclideanDistances[0].getProbeId() == euclideanDistances[0].getTestId():
# #         rank1+=1
# #     
# #     elif euclideanDistances[0].getProbeId() == euclideanDistances[1].getTestId():
# #         rank2+=1
#     
#     for i in range(0, len(rank)):
#         rank[i] += rank_n(euclideanDistances, i)
#     
#     elapsed_time = time.time() - start_time
#     print "Processed " + howManyProbes.__str__() + " probes in " + elapsed_time.__str__() + " seconds."
#         
#         
# print "Number of probes: " + howManyProbes.__str__()
# for i in range(0, len(rank)):
#     print str(i+1) + ": " + str(float(rank[i]) / howManyProbes)
# 
# x = numpy.linspace(1, 50)
# plt.plot(x,rank)
# plt.show()