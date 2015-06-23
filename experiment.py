#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import matplotlib.pyplot as plt
import pylab
import numpy
from ranking import Ranking

class Experiment:
    
    def __init__(self, modality, filenameToSaveFigureTo):
        self.accuracyStrategies = []
        self.scoreHandlers = []
        self.path = filenameToSaveFigureTo
        self.modality = modality
    
    def computeAccuracy(self):
        for __ in range(0, self.modality.getNumberOfSplits()):
            probes, galleries = self.modality.getSplits()
            for probe in probes:
                ranking = Ranking(probe, galleries)
                for aStrategy in self.accuracyStrategies:
                    aStrategy.updateWithNewProbe(ranking)
            
    def addAccuracyStrategy(self, aStrategy):
        self.accuracyStrategies.append(aStrategy)
        
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
        pylab.savefig(self.path + '.png')