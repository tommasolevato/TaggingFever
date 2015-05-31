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
        
    def initAccuracy(self):
        self.accuracies = {}
        for aStrategy in self.accuracyStrategies:
            self.accuracies[aStrategy] = Experiment.Accuracy()
            
    def computeRankedAccuracy(self,ranking):
        for aStrategy in self.accuracyStrategies:
            if aStrategy.isProbeSuccessfullyRecognized(ranking):
                self.accuracies[aStrategy].addSuccessfulProbe()
            else:
                self.accuracies[aStrategy].addUnsuccessfulProbe()
        
    def computeAccuracy(self):
        self.initAccuracy()
        for probe in self.dataset.probeSet:
            ranking = self.dataset.getRanking(probe)
            self.computeRankedAccuracy(ranking)
        return self.accuracies

    def computeAccuracyMvsM(self):
        tmpAccuracies = {}
        splits = 10
        for i in range(splits):
            self.initAccuracy()
            self.dataset.prepareDictionariesMvsM(self.N)
            for peopleid in self.dataset.getProbeKeys():
                ranking = self.dataset.getRankingMvsM(peopleid)
                self.computeRankedAccuracy(ranking)
            
            #brutta la mia gestione delle accuracy
            for aStrategy in self.accuracies:
                if(aStrategy not in tmpAccuracies):
                    tmpAccuracies[aStrategy] = self.accuracies[aStrategy]
                    tmpAccuracies[aStrategy].setSuccesfulProbes(float(tmpAccuracies[aStrategy].getSuccesfulProbes())/splits)
                else:
                    tmpAccuracies[aStrategy].setSuccesfulProbes( float(tmpAccuracies[aStrategy].getSuccesfulProbes()) + (float(self.accuracies[aStrategy].getSuccesfulProbes()) / splits) )
                    
        for aStrategy in tmpAccuracies:
            print aStrategy, tmpAccuracies[aStrategy]
            self.accuracies[aStrategy] = tmpAccuracies[aStrategy]
        return self.accuracies
    
    
    def computeAndPlotCMCCurve(self):
        if(self.N==0):
            self.computeAccuracy()
        else:
            self.computeAccuracyMvsM()
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
            
        def getSuccesfulProbes(self):
            return self._successfulProbes
 
        def setSuccesfulProbes(self, successfulProbes):
            self._successfulProbes = successfulProbes     
        
        def __repr__(self):
            return "{0:.4f}".format(self.computeYourself())