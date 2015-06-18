import numpy
from loadListFromFile import loadListFromFile

import matplotlib.pyplot as plt
import pylab
from modalityFolderName import getModalityFolderName
from filenameFromParams import filenameFromParams

def plotList(ax, aListToPlot, options, i, j):
    x = numpy.arange(1,len(aListToPlot)+1)
    
    
    #ax[i][j].aspect('equal')
    ax[i][j].set_xticks(numpy.arange(0, 11, 1))
    ax[i][j].set_yticks(numpy.arange(0, 101, 10))
    ax[i][j].set_ylim(0, 101)
    ax[i][j].set_xlim(1, 10)
    ax[i][j].grid(False)
    ax[i][j].plot(x,aListToPlot, options)
    
    
    


directoryToSaveIn = '/home/tommaso/LiClipse Workspace/Mnemosyne/curves/'
NList = [0,1,5,10]
camList = ['cam1', 'cam2', 'cam3', 'cam4']
protocolList = ['h0_v0']
descriptorList = ['d2', 'd3']

f, ax = plt.subplots(4, 4, sharex='col', sharey='row',figsize=(12,12))
f.subplots_adjust(hspace=0.1, wspace=0.1, left=0.05, right = 0.95, bottom=0.05, top=0.95)

j = 0
for N in NList:
    i = 0
    for cam in camList:
        folder = directoryToSaveIn + cam + '/' + getModalityFolderName(N) + '/'
        for protocol in protocolList:
            for descriptor in descriptorList:
                #TODO: horrible
                internalFolder = folder + protocol + '/' + descriptor + '/'
                file = internalFolder + filenameFromParams(protocol, descriptor, cam, getModalityFolderName(N))
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
                    options = options + ('')
                plotList(ax, loadListFromFile(file), options, i, j)
        i += 1
    j += 1
    
ax[0][0].legend(labels=['d2','d3'], bbox_to_anchor=(1, 0.5),fontsize = 'xx-large')
ax[0][0].set_title('SvA',size=20)
ax[0][1].set_title('SvS',size=20)
ax[0][2].set_title('5v5',size=20)
ax[0][3].set_title('10v10',size=20)
ax[0][0].set_ylabel('c1', rotation='horizontal',size=15)
ax[1][0].set_ylabel('c2', rotation='horizontal',size=15)
ax[2][0].set_ylabel('c3', rotation='horizontal',size=15)
ax[3][0].set_ylabel('c4', rotation='horizontal',size=15)

pylab.show()



# __, ax = plt.subplots()
# plotList(ax, loadListFromFile('/home/tommaso/Dropbox/DBMM/cam1/3v3/h0_v0/d1/c1_h0_v0_3v3_d1'), 'm')
# y = numpy.arange(1,51)
# plotList(ax, y, 'b--')
# ax.grid()
# pylab.show()