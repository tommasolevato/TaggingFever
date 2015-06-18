from config import Config
import os
from filenameFromParams import filenameFromParams
from loadListFromFile import loadRank1FromFile

def stringFromDescriptorAndCamera(descriptor, camera):
    modList = ['SvA', 'SvS', '5v5', '10v10']
    hList = ['h0_v0', 'h100_v50']
    
    stringToWrite = '&' + descriptor + '&'
    
    for mod in modList:
        dir = Config.getTestPath() + camera + '/' + mod + '/'
        for h in hList:
            internalDir = dir + h + '/' + descriptor + '/'
            file = internalDir + filenameFromParams(h, descriptor, cam, mod)
            rank1 = loadRank1FromFile(file)
            stringToWrite = stringToWrite + str(rank1) + '&'
    stringToWrite = stringToWrite[:-1] + '\\\\'
    return stringToWrite        
           
           
camList = ['cam1', 'cam2', 'cam3', 'cam4']
descList = ['d1', 'd2', 'd3', 'd4']


fileToSave = '/home/tommaso/tabella'
print '\\begin{table}'
print '\\begin{tabular}{| l | l || c | c || c | c || c | c || c | c ||}'
print '\\hline'
print '\\multicolumn{2}{|c||}{} & \\multicolumn{2}{|c||}{SvA} & \\multicolumn{2}{|c||}{SvS} & \\multicolumn{2}{|c||}{5v5} & \\multicolumn{2}{|c||}{10v10} \\\\'
print '\\hline'
print '\\multicolumn{2}{|c||}{} & h0_v0 & h100_v50 & h0_v0 & h100_v50 & h0_v0 & h100_v50 & h0_v0 & h100_v50 \\\\'
print '\\hline\\hline'


 
for cam in camList:
    print '\\multirow{4}{*}{' + cam + '}' + stringFromDescriptorAndCamera(descList[0], cam)
    for desc in descList[1:]:
        print stringFromDescriptorAndCamera(desc, cam)
    print '\\hline\\hline'
    
print '\\hline'
print '\\end{tabular}'
print '\\end{table}'