from experiment import Experiment
from dbData import DBData
from accuracyStrategy import AccuracyStrategy
from dataset import Dataset

DBData.initialize()
rankOne = AccuracyStrategy(1)
dataset = Dataset(DBData.probes, DBData.getAllGalleryData())
e = Experiment(dataset, rankOne)
print e.computeAccuracy()