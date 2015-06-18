import random
import numpy

class ProbeTraceStrategy(object):
    def selectDescription(self, detections):
        return random.choice(detections).getPersonDescription()
    
class GalleryFullAverageStrategy(object):
    def selectDescription(self, detections):
        descriptionToReturn = numpy.zeros(len(detections[0].getPersonDescription()))
        for detection in detections:
            descriptionToReturn += detection.getPersonDescription()
        descriptionToReturn = numpy.divide(descriptionToReturn, len(detections))
        return descriptionToReturn