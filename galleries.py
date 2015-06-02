from experiment import Experiment
from dbData import DBData
from accuracyStrategy import AccuracyStrategy
from dataset import Dataset
import argparse

#TODO: move in a function
parser = argparse.ArgumentParser()
parser.add_argument('height', type=int)
parser.add_argument('visibility_ratio', type=float) #Use 0 to fetch all
parser.add_argument('descriptor', type=int)
parser.add_argument('cam', type=int) #cam=0(All Cam), cam=1,2,3,4(selected CamGallery)
parser.add_argument('N', type=int) #N=-1:(AllvAll), N=0(SvAll), N=1 (SvS) N=3,5,10 (MvM)
args = parser.parse_args()
args = vars(args)

DBData.initialize(args)
if(args['cam']==0):
    dataset = Dataset(DBData.probes, DBData.getAllGalleryData())
else:
    dataset = Dataset(DBData.probes, DBData.getCameraGalleryData(args['cam']))

e = Experiment(dataset, args['N'])
for i in range(1,51):
    e.addAccuracyStrategy(AccuracyStrategy(i))
#pprint.pprint(e.computeAccuracy())
e.computeAndPlotCMCCurve()
print args #To be printed in a result file