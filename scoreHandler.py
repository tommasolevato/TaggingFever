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
            bins[int(score*20)] += 1
        return bins