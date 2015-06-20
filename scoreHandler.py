from __future__ import division
import numpy

class ScoreHandler:
    def __init__(self):
        self.scores = []
        
    def addScore(self, score):
        self.scores.append(score)
        
    def getAverageScore(self):
        return numpy.average(self.scores)
    
    def getScoreHistogram(self):
        bins = numpy.zeros(21)
        for score in self.scores:
            #TODO: verificare meglio
            bins[int(score*20)] += 1
        return bins
#     def __init__(self):
#         self.differences = []
#         
#     def addDetectionDifference(self, aDetectionDifference):
#         self.differences.append(aDetectionDifference.computeDistance())
#         
#     def addDetectionRanking(self, aRanking):
#         for aDifference in aRanking:
#             self.addDetectionDifference(aDifference)
#         
#     def computeAverage(self):
#         return numpy.average(self.differences)
#     
#     def computeStandardDeviation(self):
#         return numpy.std(self.differences)
#     
#     def isEmpty(self):
#         return self.differences == []
#     
#     