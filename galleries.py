#!/usr/bin/env python
# -*- coding: utf-8 -*-


# from experiment import Experiment
# from accuracyStrategy import AccuracyStrategy
# from dataset import Dataset
import argparse
from experimentSeries import ExperimentSeries
# import sys
# from modalityFolderName import getModalityFolderName
# import os
# from config import Config
# from args import argsListFromSingleValues

parser = argparse.ArgumentParser()
parser.add_argument('--detections', dest = 'detections', action="store_true")
parser.add_argument('--traces', dest = 'traces', action="store_true")
parser.add_argument('--h', dest = 'height', nargs='*', type=int)
parser.add_argument('--v', dest = 'visibility_ratio', nargs='*',type=float)
parser.add_argument('--d', dest = 'descriptor', nargs='*', type=int) #id da database dei descrittori
parser.add_argument('--c', dest = 'cam', nargs='*', type=int) #cam=0(All Cam), cam=1,2,3,4(selected CamGallery)
parser.add_argument('--n', dest = 'N', nargs='*', type=int) #N=-1:(AllvAll), N=0(SvAll), N=1 (SvS) N=3,5,10 (MvM)

args = parser.parse_args()
args = vars(args)

e = ExperimentSeries(args)
e.computeSeries()


# #se non si indica un parametro, è come se si indicassero tutti i possibili valori di quel parametro
# if len(args['height']) == 0:
#     args['height'] = [0, 100]
# if len(args['visibility_ratio']) == 0:
#     args['visibility_ratio'] = [0, 0.5, 0.75, 1]
# if len(args['descriptor']) == 0:
#     args['descriptor'] = [1,2,3,4]
# if len(args['cam']) == 0:
#     args['cam'] = [1,2,3,4]
# if len(args['N']) == 0:
#     args['N'] = [0,1,5,10]
# #esempio di invocazione: python galleries.py --h 100 --v 0.5 
# 
# t = args['traces']
# 
# for v in args['visibility_ratio']:
#     for d in args['descriptor']:
#         for n in args['N']:
#             for c in args['cam']:
#                 for h in args['height']:
#                     #per evitare modalità tipo h0_v50 o h100_v0
#                     if (h==0 and v != 0) or (h!=0 and v==0):
#                         continue
#                     sys.stdout = sys.__stdout__
#                     directoryToSaveIn = Config.getTestPath() + 'cam' + str(c) + '/' + getModalityFolderName(n) + '/h' + str(h) + '_v' + str(int(v*100)) + '/d' + str(d) + '/'
#                     fileToSaveTo = 'c' + str(c) + '_h' + str(h) + '_v' + str(int(v * 100)) + '_' + getModalityFolderName(n) + '_d' + str(d)
#                     print 'Cam=' + str(c) + ', N=' + str(n) + ', height=' + str(h) + ', visibility Ratio=' + str(v) + ', Descriptor=' + str(d)
#                     #mi creo la cartella dei test se non esiste
#                     if not os.path.exists(directoryToSaveIn):
#                         os.makedirs(directoryToSaveIn)
#                     f = open(directoryToSaveIn+fileToSaveTo, 'w')
#                     #TODO: uncomment
#                     #sys.stdout = f
#                     dataset = Dataset(argsListFromSingleValues(h, v, c, d, t))
#                     e = Experiment(dataset, n)
#                     #aggiungo i rank che mi interessano
#                     for i in range(1,51):
#                         e.addAccuracyStrategy(AccuracyStrategy(i))
#                     e.computeAndPlotCMCCurve()
#                     print 'Cam=' + str(c) + ', N=' + str(n) + ', height=' + str(h) + ', visibility Ratio=' + str(v) + ', Descriptor=' + str(d)