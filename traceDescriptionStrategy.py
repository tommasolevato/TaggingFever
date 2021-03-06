import random
import numpy

class ProbeTraceStrategy(object):
    def selectDescription(self, detections):
        return random.choice(detections).getPersonDescription()
    
class GalleryFullAverageStrategy(object):
    def getName(self):
        return 'fullAverage'
    
    def selectDescription(self, detections):
        descriptionToReturn = numpy.zeros(len(detections[0].getPersonDescription()))
        for detection in detections:
            descriptionToReturn += detection.getPersonDescription()
        descriptionToReturn = numpy.divide(descriptionToReturn, len(detections))
        return descriptionToReturn

class GalleryOnlyColorAverageStrategy(object):
    def getName(self):
        return 'noHogAverage'
    
    def selectDescription(self, detections):
        descriptionToReturn = numpy.zeros(len(detections[0].getPersonDescription()))
        hog = random.choice(detections).getPersonDescription()[1920:2960]
        for detection in detections:
            descriptionToReturn += detection.getPersonDescription()
        descriptionToReturn = numpy.divide(descriptionToReturn, len(detections))
        descriptionToReturn[1920:2960] = hog
        return descriptionToReturn