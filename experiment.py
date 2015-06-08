from __future__ import division
import matplotlib.pyplot as plt
import pylab
import numpy
from scoreHandler import ScoreHandler

class Experiment:
    
    def __init__(self, dataset, N, path):
        self.dataset = dataset
        self.accuracyStrategies = []
        self.scoreHandlers = []
        self.N = N
        self.path = path
        
    def addAccuracyStrategy(self, aStrategy):
        self.accuracyStrategies.append(aStrategy)
        self.scoreHandlers.append(ScoreHandler())
        
    def _initAccuracy(self):
        self.accuracies = {}
        self.scoreHandlers = []
        for aStrategy in self.accuracyStrategies:
            self.accuracies[aStrategy] = Experiment.Accuracy()
            self.scoreHandlers.append(ScoreHandler())
            
    def _computeRankedAccuracy(self,ranking):
        for aStrategy in self.accuracyStrategies:
            if aStrategy.isProbeSuccessfullyRecognized(ranking):
                self.accuracies[aStrategy].addSuccessfulProbe()
            else:
                self.accuracies[aStrategy].addUnsuccessfulProbe()
        
        
    #TODO: remove duplication
    def computeAccuracy(self):
        self._initAccuracy()
        handler = ScoreHandler()
        for probe in self.dataset.probeSet:
            #TODO: move ranking computation in next method
            ranking = self.dataset.getRanking(probe)
            self._updateScoreHandlers(ranking)
            handler.addDetectionRanking(ranking)
            self._computeRankedAccuracy(ranking)
        print "Average score: " + str(handler.computeAverage())
        print "Score Standard Deviation: " + str(handler.computeStandardDeviation())
        return self.accuracies
    
    def _updateScoreHandlers(self, ranking):
        i = 0
        for anElement in ranking:
            self.scoreHandlers[i].addDetectionDifference(anElement)
            i += 1
            if i == len(self.accuracyStrategies)-1:
                break
    
    def _getScores(self):
        average = []
        std = []
        for anHandler in self.scoreHandlers:
            if not anHandler.isEmpty():
                average.append(anHandler.computeAverage())
                std.append(anHandler.computeStandardDeviation())
        return average, std
    
    
    def computeAccuracyMvsM(self):
        self._initAccuracy()
        handler = ScoreHandler()
        splits = 100 #greater Stability
        self.dataset.verifyN(self.N)
        for __ in range(0, splits):
            for peopleid in self.dataset.getProbeKeys():
                ranking = self.dataset.getRankingMvsM(peopleid, self.N)
                self._updateScoreHandlers(ranking)
                handler.addDetectionRanking(ranking)
                self._computeRankedAccuracy(ranking)
        print "Average score: " + str(handler.computeAverage())
        print "Score Standard Deviation: " + str(handler.computeStandardDeviation())
        return self.accuracies
    
    def computeAccuracySvsAll(self):
        self._initAccuracy()
        splits = 30
        handler = ScoreHandler()
        probes = self.dataset.getProbeKeys()
        for ranking in range(0, splits):
            for probe in probes:
                ranking = self.dataset.getRankingSvsAll(probe)
                self._updateScoreHandlers(ranking)
                handler.addDetectionRanking(ranking)
                self._computeRankedAccuracy(ranking)
        print "Average score: " + str(handler.computeAverage())
        print "Score Standard Deviation: " + str(handler.computeStandardDeviation())
        return self.accuracies
            
    
    def computeAndPlotCMCCurve(self):
        #TODO: 
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
        #pylab.show()
        pylab.savefig(self.path + '.png')
        average, std = self._getScores()
        x = numpy.arange(1, len(average)+1, 1)
        print average
        print std
        __, ax = plt.subplots()
        ax.plot(x, average)
        ax.set_title("Average Distance per Rank")
        ax.set_xlabel("Rank")
        ax.set_ylabel("Average Distance")
        ax.grid()
        pylab.savefig(self.path + '-distances.png')
    
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