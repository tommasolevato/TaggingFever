from __future__ import division
import numpy

class ScoreHandler:
    
    def __init__(self):
        self.differences = []
        
    def  addDetectionDifference(self, aDetectionDifference):
        self.differences.append(aDetectionDifference.computeDistance())
        
    def addDetectionRanking(self, aRanking):
        for aDifference in aRanking:
            self.addDetectionDifference(aDifference)
        
    def computeAverage(self):
        return numpy.average(self.differences)
    
    def computeStandardDeviation(self):
        return numpy.std(self.differences)
    
    