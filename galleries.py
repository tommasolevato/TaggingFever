from experiment import Experiment
from dbData import DBData
from accuracyStrategy import AccuracyStrategy
from dataset import Dataset

DBData.initialize()
dataset = Dataset(DBData.probes, DBData.getAllGalleryData())

N = 5 # N=0: (All vs All), N=1 (SvsS) N=3,5,10 (MvsM)
e = Experiment(dataset, N)
for i in range(1,11):
    e.addAccuracyStrategy(AccuracyStrategy(i))
#pprint.pprint(e.computeAccuracy())
e.computeAndPlotCMCCurve()