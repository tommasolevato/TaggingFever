#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from config import Config
from modality import Modality, AllvsAllModality, SvsAllModality, SvsSModality,\
    MvsMModality
from dataset import DetectionsDataset
from dataset import TracesDataset
import os
from experiment import Experiment
from accuracyStrategy import AccuracyStrategy
from traceDescriptionStrategy import GalleryFullAverageStrategy,\
    GalleryOnlyColorAverageStrategy

class ExperimentSeries:
    def __init__(self, args):
        self.args = args
        if args['detections'] == True:
            self.__completeArgsIfNotSpecified('height', [0, 100])
            self.__completeArgsIfNotSpecified('visibility_ratio', [0, 0.5, 0.75, 1])
            self.__completeArgsIfNotSpecified('descriptor', [1, 2, 3 ,4])
            self.__completeArgsIfNotSpecified('cam', [1, 2, 3, 4])
            self.__completeArgsIfNotSpecified('N', ['SvA', 1, 5, 10])
        if args['traces'] == True:
            self.__completeArgsIfNotSpecified('cam', [1, 2, 3, 4])
            self.__completeArgsIfNotSpecified('trace_type', [4, 5])
            self.__completeArgsIfNotSpecified('average_strategy', [GalleryFullAverageStrategy(), GalleryOnlyColorAverageStrategy()])
            self.__parseAverageStrategy()
        
                
    def __completeArgsIfNotSpecified(self, arg, valuesToInclude):
        if self.args[arg] == None:
            self.args[arg] = valuesToInclude
            
    def __parseAverageStrategy(self):
        strategyList = []
        if 'full' in self.args['average_strategy']:
            strategyList.append(GalleryFullAverageStrategy())
        if 'onlyColor' in self.args['average_strategy']:
            strategyList.append(GalleryOnlyColorAverageStrategy())
        self.args['average_strategy'] = strategyList
            
    def computeSeries(self):
        if self.args['detections'] == True:
            self.__computeDetectionsSeries()
        if self.args['traces'] == True:
            self.__computeTracesSeries()
            
    def __computeDetectionsSeries(self):
        for v in self.args['visibility_ratio']:
            for d in self.args['descriptor']:
                for n in self.args['N']:
                    for c in self.args['cam']:
                        for h in self.args['height']:
                            if (h==0 and v != 0) or (h!=0 and v==0):
                                continue
                            sys.stdout = sys.__stdout__
                            directory = Config.getDetectionsTestPath() + 'cam' + str(c) + '/' + Modality.getName(n) + '/h' + str(h) + '_v' + str(int(v*100)) + '/d' + str(d) + '/'
                            fileToSaveTo = 'c' + str(c) + '_h' + str(h) + '_v' + str(int(v * 100)) + '_' + Modality.getName(n) + '_d' + str(d)
                            print 'Cam=' + str(c) + ', N=' + str(n) + ', height=' + str(h) + ', visibility Ratio=' + str(v) + ', Descriptor=' + str(d)
                            self.__openTestFile(directory, fileToSaveTo)
                            dataset = DetectionsDataset(h, v, d, c)
                            modality = self.__createModality(n, dataset)
                            e = self.__buildExperiment(dataset, modality, directory+fileToSaveTo)
                            e.computeAndPlotCMCCurve()
    
    def __computeTracesSeries(self):
        for c in self.args['cam']:
            for t in self.args['trace_type']:
                for a in self.args['average_strategy']:
                    sys.stdout = sys.__stdout__
                    directory = Config.getTracesTestPath() + 'cam' + str(c) + '/' + '/t' + str(t) + '/'
                    fileToSaveTo = 'c' + str(c) + '_t' + str(t) + '_' + a.getName()
                    print 'Cam=' + str(c) + ', Trace Type=' + str(t) + ', Average=' + a.getName()
                    self.__openTestFile(directory, fileToSaveTo)
                    dataset = TracesDataset(c, t, a)
                    e = self.__buildExperiment(dataset, 0, directory+fileToSaveTo)
                    e.computeAndPlotCMCCurve()
                    
    def __openTestFile(self, directory, fileToSaveTo):
        if not os.path.exists(directory):
            os.makedirs(directory)
        f = open(directory+fileToSaveTo, 'w')
        sys.stdout = f
        
    def __buildExperiment(self, dataset, modality, pathToSaveTo):
        e = Experiment(modality, pathToSaveTo)
        for i in range(1,51):
            e.addAccuracyStrategy(AccuracyStrategy(i))
        return e
    
    def __createModality(self, n, dataset):
        if str(n) == 'AvA':
            return AllvsAllModality(dataset)
        elif str(n) == 'SvA':
            return SvsAllModality(dataset)
        elif str(n) == '1':
            return SvsSModality(dataset)
        else:
            return MvsMModality(dataset, n)