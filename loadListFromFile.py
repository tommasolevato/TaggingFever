import ast

def loadListFromFile(fileToLoadFrom):
    with open(fileToLoadFrom) as f:
        for line in f:
            if line[0] == '[':
                y = ast.literal_eval(line)
                y = y[0:10]
                break
    return y

def loadRank1FromFile(fileToLoadFrom):
    return loadListFromFile(fileToLoadFrom)[0]