#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from config import Config
from modality import Modality
from dataset import DetectionsDataset
import os
from experiment import Experiment
from accuracyStrategy import AccuracyStrategy

class ExperimentSeries:
    def __init__(self, args):
        self.args = args
        if args['detections'] == True:
            self.__completeArgsIfNotSpecified('height', [0, 100])
            self.__completeArgsIfNotSpecified('visibility_ratio', [0, 0.5, 0.75, 1])
            self.__completeArgsIfNotSpecified('descriptor', [1, 2, 3 ,4])
            self.__completeArgsIfNotSpecified('cam', [1, 2, 3, 4])
            self.__completeArgsIfNotSpecified('N', [0, 1, 5, 10])
        if args['traces'] == True:
            self.__completeArgsIfNotSpecified('cam', [1, 2, 3, 4])
            self.__completeArgsIfNotSpecified('trace_type', [4, 5])
                
    def __completeArgsIfNotSpecified(self, arg, valuesToInclude):
        if len(self.args[arg]) == 0:
            self.args[arg] = valuesToInclude
            
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
                            #per evitare modalità tipo h0_v50 o h100_v0
                            if (h==0 and v != 0) or (h!=0 and v==0):
                                continue
                            sys.stdout = sys.__stdout__
                            directoryToSaveIn = Config.getTestPath() + 'cam' + str(c) + '/' + Modality.getName(n) + '/h' + str(h) + '_v' + str(int(v*100)) + '/d' + str(d) + '/'
                            fileToSaveTo = 'c' + str(c) + '_h' + str(h) + '_v' + str(int(v * 100)) + '_' + Modality.getName(n) + '_d' + str(d)
                            print 'Cam=' + str(c) + ', N=' + str(n) + ', height=' + str(h) + ', visibility Ratio=' + str(v) + ', Descriptor=' + str(d)
                            #mi creo la cartella dei test se non esiste
                            if not os.path.exists(directoryToSaveIn):
                                os.makedirs(directoryToSaveIn)
                            f = open(directoryToSaveIn+fileToSaveTo, 'w')
                            #TODO: uncomment
                            #sys.stdout = f
                            dataset = DetectionsDataset(self.__makeDetectionArgs(v, d, n, c, h))
                            e = Experiment(dataset, n)
                            #aggiungo i rank che mi interessano
                            for i in range(1,51):
                                e.addAccuracyStrategy(AccuracyStrategy(i))
                            e.computeAndPlotCMCCurve()
                            print 'Cam=' + str(c) + ', N=' + str(n) + ', height=' + str(h) + ', visibility Ratio=' + str(v) + ', Descriptor=' + str(d)
    
    def __makeDetectionArgs(self, v, d, n, c, h):
        args = {}
        args['visibility_ratio'] = v
        args['descriptor'] = d
        args['N'] = n
        args['cam'] = c
        args['height'] = h
        return args
    
    def __makeTraceArgs(self, c, t):
        args = {}
        args['trace_type'] = t
        args['cam'] = c
        return args