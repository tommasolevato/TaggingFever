from experiment import Experiment
from dbData import DBData
from accuracyStrategy import AccuracyStrategy
from dataset import Dataset
import argparse
import sys

#TODO: move in a function
parser = argparse.ArgumentParser()
parser.add_argument('height', type=int)
parser.add_argument('visibility_ratio', type=float) #Use 0 to fetch all
parser.add_argument('descriptor', type=int)
parser.add_argument('cam', type=int) #cam=0(All Cam), cam=1,2,3,4(selected CamGallery)
parser.add_argument('N', type=int) #N=-1:(AllvAll), N=0(SvAll), N=1 (SvS) N=3,5,10 (MvM)
args = parser.parse_args()
args = vars(args)

descriptorList = [3,4]
NList = [0,1,3,5,10]
camList = [1]
#visList = [0.5, 0.75, 1]

def getModalityFolderName(N):
    if N==3 or N==5 or N==10:
        return str(N)+'v'+str(N)
    if N==1:
        return 'SvS'
    if N==0:
        return 'SvA'

for d in descriptorList:
    for n in NList:
        for c in camList:
            args['descriptor'] = d
            args['N'] = n
            args['cam'] = c
            path = '/home/tommaso/LiClipse Workspace/Mnemosyne/curves/cam' + str(args['cam']) + '/' + getModalityFolderName(args['N']) + '/h' + str(args['height']) + '_v' + str(int(args['visibility_ratio']*100)) + '/d' + str(args['descriptor']) + '/'
            filename = 'c' + str(args['cam']) + '_h' + str(args['height']) + '_v' + str(int(args['visibility_ratio'] * 100)) + '_' + getModalityFolderName(args['N']) + '_d' + str(args['descriptor'])
            f = open(path+filename, 'w')
            sys.stdout = f
            DBData.initialize(args)
            if(args['cam']==0):
                dataset = Dataset(DBData.probes, DBData.getAllGalleryData(), 'all', args['descriptor'])
            else:
                dataset = Dataset(DBData.probes, DBData.getCameraGalleryData(args['cam']), args['cam'], args['descriptor'])
            e = Experiment(dataset, args['N'], path+filename)
            for i in range(1,51):
                e.addAccuracyStrategy(AccuracyStrategy(i))
            #pprint.pprint(e.computeAccuracy())
            e.computeAndPlotCMCCurve()
            print args #To be printed in a result file