
from pathlib import Path

def loadData(fileName):
	p = Path(fileName)
	lines = p.read_text().splitlines()
	X = [line.split(maxsplit=1)[1] for line in lines]
	y = [int(line.split(maxsplit=1)[0]) for line in lines]
	return X,y

def loadErrorCountDataToScore(fileName):
	X,y = loadData(fileName)
	y = [-count for count in y]
	return X,y