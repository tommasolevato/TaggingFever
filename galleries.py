from experiment import Experiment
from dbData import DBData
from accuracyStrategy import AccuracyStrategy
from dataset import Dataset
import argparse

#TODO: move in a function
parser = argparse.ArgumentParser()
parser.add_argument('height', type=int)
parser.add_argument('visibility_ratio', type=float)
parser.add_argument('descriptor', type=int)
args = parser.parse_args()
args = vars(args)

DBData.initialize(args)
dataset = Dataset(DBData.probes, DBData.getAllGalleryData())

N = 5 # N=0: (All vs All), N=1 (SvsS) N=3,5,10 (MvsM)
e = Experiment(dataset, N)
for i in range(1,51):
    e.addAccuracyStrategy(AccuracyStrategy(i))
#pprint.pprint(e.computeAccuracy())
e.computeAndPlotCMCCurve()