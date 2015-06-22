#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from experimentSeries import ExperimentSeries

parser = argparse.ArgumentParser()
parser.add_argument('--detections', dest = 'detections', action="store_true")
parser.add_argument('--traces', dest = 'traces', action="store_true")
parser.add_argument('--h', dest = 'height', nargs='*', type=int)
parser.add_argument('--v', dest = 'visibility_ratio', nargs='*',type=float)
parser.add_argument('--d', dest = 'descriptor', nargs='*', type=int) #id da database dei descrittori
parser.add_argument('--c', dest = 'cam', nargs='*', type=int) #cam=0(All Cam), cam=1,2,3,4(selected CamGallery)
parser.add_argument('--n', dest = 'N', nargs='*', type=int) #N=-1:(AllvAll), N=0(SvAll), N=1 (SvS) N=3,5,10 (MvM)
parser.add_argument('--t', dest = 'trace_type', nargs='*', type=int)
parser.add_argument('--a', dest = 'average_strategy', nargs='*', type=str)
args = parser.parse_args()
args = vars(args)

e = ExperimentSeries(args)
e.computeSeries()