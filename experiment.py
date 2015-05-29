from __future__ import division
import matplotlib.pyplot as plt
import pylab
import numpy

class Experiment:
    
    def __init__(self, dataset):
        self.dataset = dataset
        self.accuracyStrategies = []
        
    def addAccuracyStrategy(self, aStrategy):
        self.accuracyStrategies.append(aStrategy)
    
    def computeAccuracy(self):
        self.accuracies = {}
        for aStrategy in self.accuracyStrategies:
            self.accuracies[aStrategy] = Experiment.Accuracy()
        for probe in self.dataset.probeSet:
            ranking = self.dataset.getRanking(probe)
            for aStrategy in self.accuracyStrategies:
                if aStrategy.isProbeSuccessfullyRecognized(ranking):
                    self.accuracies[aStrategy].addSuccessfulProbe()
                else:
                    self.accuracies[aStrategy].addUnsuccessfulProbe()
        return self.accuracies

    def computeAccuracyMvsM(self,N):
        
        splits = 10
        for i in range(splits):
            self.dataset.prepareDictionariesMvsM(N)
            for peopleid in self.dataset.getKeys():
                self.dataset.computeMinNxN(peopleid)
                #etc..
            
            
    
    def computeAndPlotCMCCurve(self):
        self.computeAccuracy()
        x = []
        rank = []
        for aStrategy in self.accuracyStrategies:
            x.append(aStrategy.rank)
            rank.append(self.accuracies[aStrategy].computeYourself() * 100)
        __, ax = plt.subplots()
        ax.plot(x,rank)
        ax.set_title("CMC-Curve")
        ax.set_xlabel("Rank")
        ax.set_xticks(numpy.arange(0, max(x), 10))
        ax.set_yticks(numpy.arange(0, 101, 10))
        ax.grid()
        ax.set_ylabel("Recognition Rate")
        ax.set_ylim(0, 101)
        pylab.show()
    
    class Accuracy:
        def __init__(self):
            self._processedProbes = 0
            self._successfulProbes = 0
            
        def computeYourself(self):
            return self._successfulProbes / self._processedProbes
        
        def addSuccessfulProbe(self):
            self._processedProbes += 1
            self._successfulProbes += 1
            
        def addUnsuccessfulProbe(self):
            self._processedProbes += 1
            
        def __repr__(self):
            return "{0:.4f}".format(self.computeYourself())