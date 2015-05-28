class Experiment:
    
    def __init__(self, dataset, accuracyStrategy):
        self.dataset = dataset
        self.accuracyStrategy = accuracyStrategy
        
    def computeAccuracy(self):
        return self.accuracyStrategy.computeAccuracy(self.dataset)