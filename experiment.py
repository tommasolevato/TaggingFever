from __future__ import division
import matplotlib.pyplot as plt
import pylab

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
    
    def computeAndPlotCMCCurve(self):
        self.computeAccuracy()
        x = []
        rank = []
        for aStrategy in self.accuracyStrategies:
            x.append(aStrategy.rank)
            rank.append(self.accuracies[aStrategy].computeYourself() * 100)
        plt.title("CMC-Curve")
        plt.xlabel("Rank")
        plt.ylabel("Recognition Rate")
        plt.ylim(0, 101)
        plt.plot(x,rank)
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