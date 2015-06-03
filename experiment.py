from __future__ import division
import matplotlib.pyplot as plt
import pylab
import numpy

class Experiment:
    
    def __init__(self, dataset, N):
        self.dataset = dataset
        self.accuracyStrategies = []
        self.N = N
        
    def addAccuracyStrategy(self, aStrategy):
        self.accuracyStrategies.append(aStrategy)
        
    def _initAccuracy(self):
        self.accuracies = {}
        for aStrategy in self.accuracyStrategies:
            self.accuracies[aStrategy] = Experiment.Accuracy()
            
    def _computeRankedAccuracy(self,ranking):
        for aStrategy in self.accuracyStrategies:
            if aStrategy.isProbeSuccessfullyRecognized(ranking):
                self.accuracies[aStrategy].addSuccessfulProbe()
            else:
                self.accuracies[aStrategy].addUnsuccessfulProbe()
        
    def computeAccuracy(self):
        self._initAccuracy()
        distancesSum = 0
        for probe in self.dataset.probeSet:
            #TODO: move ranking computation in next method
            ranking, averageDistance = self.dataset.getRanking(probe)
            distancesSum += averageDistance
            self._computeRankedAccuracy(ranking)
        average = distancesSum / len(self.dataset.probeSet)
        print average
        return self.accuracies
    
    def computeAccuracyMvsM(self):
        self._initAccuracy()
        splits = 100 #greater Stability
        self.dataset.verifyN(self.N)
        distancesSum = 0
        for __ in range(0, splits):
            for peopleid in self.dataset.getProbeKeys():
                ranking, averageDistance = self.dataset.getRankingMvsM(peopleid, self.N)
                distancesSum += averageDistance
                self._computeRankedAccuracy(ranking)
        average = distancesSum / (splits*len(self.dataset.getProbeKeys()))
        print average
        return self.accuracies
    
    def computeAccuracySvsAll(self):
        self._initAccuracy()
        splits = 1
        distancesSum = 0
        probes = self.dataset.getProbeKeys()
        for ranking in range(0, splits):
            for probe in probes:
                ranking, averageDistance = self.dataset.getRankingSvsAll(probe)
                distancesSum += averageDistance
                self._computeRankedAccuracy(ranking)
        average = distancesSum / (splits*len(probes))
        print average 
        return self.accuracies
            
    
    def computeAndPlotCMCCurve(self):
        if(self.N==-1):
            self.computeAccuracy()
        elif(self.N==0):
            self.computeAccuracySvsAll()
        else:
            self.computeAccuracyMvsM()
        x = []
        rank = []
        for aStrategy in self.accuracyStrategies:
            x.append(aStrategy.rank)
            rank.append(self.accuracies[aStrategy].computeYourself() * 100)
        __, ax = plt.subplots()
        print rank #To be printed in a result file
        ax.plot(x,rank)
        ax.set_title("CMC-Curve")
        ax.set_xlabel("Rank")
        ax.set_xticks(numpy.arange(0, max(x) + 1, len(x)/5))
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
            
        def getSuccesfulProbes(self):
            return self._successfulProbes
 
        def setSuccesfulProbes(self, successfulProbes):
            self._successfulProbes = successfulProbes     
        
        def __repr__(self):
            return "{0:.4f}".format(self.computeYourself())