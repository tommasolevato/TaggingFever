#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from config import Config
import matplotlib.pyplot as plt
import pylab
import numpy
from modality import SvSModality, SvsAllModality, MvsMModality, AllvsAllModality
from ranking import Ranking

#calcola l'accuratezza di un insieme di probe contro un insieme di gallery secondo le modalità di interesse

class Experiment:
    
    def __init__(self, dataset, N):
        self.dataset = dataset
        self.accuracyStrategies = []
        self.scoreHandlers = []
        self.createModality(N)
        #TODO: move away from constructor
        self.path = Config.getTestPath()
    
    #TODO: changeName
    def computeAccuracy(self):
        for __ in range(0, self.modality.getNumberOfSplits()):
            probes, galleries = self.modality.getSplits()
            for probe in probes:
                ranking = Ranking(probe, galleries)
                for aStrategy in self.accuracyStrategies:
                    aStrategy.updateWithNewProbe(ranking)
        
    def createModality(self, N):
        if N==-1:
            self.modality = AllvsAllModality(self.dataset.getProbeSet(), self.dataset.getGallerySet())
        elif N==0:
            self.modality = SvsAllModality(self.dataset.getProbeSet(), self.dataset.getGallerySet())
        elif N==1:
            self.modality = SvSModality(self.dataset.getProbeSet(), self.dataset.getGallerySet())
        elif N==3 or N==5 or N==10:
            self.modality = MvsMModality(self.dataset.getProbeSet(), self.dataset.getGallerySet(), N)
        else:
            raise ValueError("N must be either 0, 1, 3, 5 or 10")
            
    def addAccuracyStrategy(self, aStrategy):
        self.accuracyStrategies.append(aStrategy)
        #self.scoreHandlers.append(ScoreHandler())
        
#     
#     def _updateScoreHandlers(self, ranking):
#         i = 0
#         for anElement in ranking:
#             self.scoreHandlers[i].addDetectionDifference(anElement)
#             i += 1
#             if i == len(self.accuracyStrategies)-1:
#                 break
#     
#     def _getScores(self):
#         average = []
#         std = []
#         for anHandler in self.scoreHandlers:
#             if not anHandler.isEmpty():
#                 average.append(anHandler.computeAverage())
#                 std.append(anHandler.computeStandardDeviation())
#         return average, std
#                
#     def computeAccuracyTraces(self, probes, galleries):
#         self._initAccuracy()
#         splits = 100
#         for ranking in range(0, splits):
#             for probe in probes:
#                 ranking = self.dataset.getRankingTrace(probe, galleries)
#                 self._computeRankedAccuracy(ranking)
#         return self.accuracies
#     
    def computeAndPlotCMCCurve(self):
        self.computeAccuracy()
        x = []
        rank = []
        for aStrategy in self.accuracyStrategies:
            x.append(aStrategy.rank)
            rank.append(aStrategy.getAccuracy() * 100)
        __, ax = plt.subplots()
        print rank
         
        ax.plot(x,rank)
        ax.set_title("CMC-Curve")
        ax.set_xlabel("Rank")
        ax.set_xticks(numpy.arange(0, max(x) + 1, len(x)/5))
        ax.set_yticks(numpy.arange(0, 101, 10))
        ax.grid()
        ax.set_ylabel("Recognition Rate")
        ax.set_ylim(0, 101)
 
        #pylab.savefig(self.path + '.png')
        pylab.show()
#        plt.close()
#         average, std = self._getScores()
#         x = numpy.arange(1, len(average)+1, 1)
#         print average
#         print std
#         __, ax = plt.subplots()
#         ax.plot(x, average)
#         ax.set_title("Average Distance per Rank")
#         ax.set_xlabel("Rank")
#         ax.set_ylabel("Average Distance")
#         ax.grid()
#         #pylab.savefig(self.path + '-distances.png')
#         plt.close()