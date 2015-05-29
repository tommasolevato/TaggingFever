from experiment import Experiment
from dbData import DBData
from accuracyStrategy import AccuracyStrategy
from dataset import Dataset

DBData.initialize()
dataset = Dataset(DBData.probes, DBData.getCameraGalleryData(1))
e = Experiment(dataset)
for i in range(1,51):
    e.addAccuracyStrategy(AccuracyStrategy(i))
#pprint.pprint(e.computeAccuracy())
e.computeAndPlotCMCCurve()