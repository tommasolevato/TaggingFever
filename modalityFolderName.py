def getModalityFolderName(N):
    if N==3 or N==5 or N==10:
        return str(N)+'v'+str(N)
    if N==1:
        return 'SvS'
    if N==0:
        return 'SvA'
    if N==-1:
        return 'AvA'