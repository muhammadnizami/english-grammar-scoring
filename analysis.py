import matplotlib.pyplot as plt
import numpy as np

from pathlib import Path
from bllipparser import RerankingParser

def loadData(fileName):
	p = Path(fileName)
	lines = p.read_text().splitlines()
	X = [line.split(maxsplit=1)[1] for line in lines]
	y = [int(line.split(maxsplit=1)[0]) for line in lines]
	return X,y

X,y = loadData("data/errorCountCorpus_test")
print("test variance: "+ str(np.var(y)))

X,y = loadData("data/errorCountCorpus_train")
print("train variance: "+ str(np.var(y)))

rrp = RerankingParser.fetch_and_load('WSJ+Gigaword-v2', verbose=True)
probs = [[tree.parser_score for tree in rrp.parse(x)] for x in X]
probs = [x[0] for x in probs]
lens = [len(x) for x in X]

plt.plot(lens, probs, 'ro')
plt.show()
plt.plot(np.negative(y), probs, 'ro')
plt.show()

transformedprobs = np.divide(probs,lens)
plt.plot(lens, transformedprobs, 'ro')
plt.show()
plt.plot(np.negative(y), transformedprobs, 'ro')
plt.show()

print(np.corrcoef(probs,np.negative(y)))
print(np.corrcoef(transformedprobs,np.negative(y)))