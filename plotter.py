import numpy
import ast

import matplotlib.pyplot as plt
import pylab
from modalityFolderName import getModalityFolderName

def loadListFromFile(fileToLoadFrom):
    with open(fileToLoadFrom) as f:
        for line in f:
            if line[0] == '[':
                y = ast.literal_eval(line)
                y = y[0:10]
                break
    return y

def plotList(ax, aListToPlot, options, i, j):
    x = numpy.arange(1,len(aListToPlot)+1)
    
    
    #ax[i][j].aspect('equal')
    ax[i][j].set_xticks(numpy.arange(0, 11, 1))
    ax[i][j].set_yticks(numpy.arange(0, 101, 10))
    ax[i][j].set_ylim(0, 101)
    ax[i][j].set_xlim(1, 10)
    ax[i][j].grid(True)
    ax[i][j].plot(x,aListToPlot, options)
    
    
    


path = '/home/tommaso/LiClipse Workspace/Mnemosyne/curves/'
NList = [0,1,5,10]
camList = ['cam1', 'cam2', 'cam3', 'cam4']
protocolList = ['h0_v0', 'h100_v50']
descriptorList = ['d1', 'd2', 'd3', 'd4']

f, ax = plt.subplots(4, 4, sharex='col', sharey='row',figsize=(12,12))

j = 0
for N in NList:
    i = 0
    for cam in camList:
        folder = path + cam + '/' + getModalityFolderName(N) + '/'
        for protocol in protocolList:
            for descriptor in descriptorList:
                #TODO: horrible
                file = folder + protocol + '/' + descriptor + '/' + cam[0] + cam[3] + '_' + protocol + '_' + getModalityFolderName(N) + '_' + descriptor
                options = ''
                if descriptor == 'd1':
                    options = options + ('m')
                if descriptor == 'd2':
                    options = options + ('r')
                if descriptor == 'd3':
                    options = options + ('c')
                if descriptor == 'd4':
                    options = options + ('b')
                if protocol == 'h0_v0':
                    options = options + ('--')
                plotList(ax, loadListFromFile(file), options, i, j)
        i += 1
    j += 1
    
# ax[0][0].set_title('SvA')
# ax[0][1].set_title('SvS')
# ax[0][2].set_title('5v5')
# ax[0][3].set_title('10v10')
# ax[0][0].set_ylabel('c1', rotation='horizontal')
# ax[1][0].set_ylabel('c2', rotation='horizontal')
# ax[2][0].set_ylabel('c3', rotation='horizontal')
# ax[3][0].set_ylabel('c4', rotation='horizontal')

pylab.show()



# __, ax = plt.subplots()
# plotList(ax, loadListFromFile('/home/tommaso/Dropbox/DBMM/cam1/3v3/h0_v0/d1/c1_h0_v0_3v3_d1'), 'm')
# y = numpy.arange(1,51)
# plotList(ax, y, 'b--')
# ax.grid()
# pylab.show()