import numpy as np
from . import data_load
from pathlib import Path
from bllipparser import RerankingParser
from sklearn import datasets, linear_model
import pickle

MAX_NUMATTR = 5

def parse(sentence,nbest=MAX_NUMATTR):
	if 'rrp' not in globals():
		global rrp
		rrp=RerankingParser.fetch_and_load('WSJ+Gigaword-v2')
	rrp.set_parser_options(nbest=nbest)
	return rrp.parse(sentence)

def parseProb(sentence,nbest=MAX_NUMATTR):
	a = [tree.parser_score for tree in parse(sentence,nbest)[:MAX_NUMATTR]]
	if len(a)<nbest:
		a.extend([a[-1]]*(nbest-len(a)))
	return a;

def parseProbs(sentences,nbest=MAX_NUMATTR):
	return np.array([parseProb(sentence,nbest) for sentence in sentences])

def sentenceLength(sentence):
	return len(sentence.split(" "))

class GrammarScorer:
	def __init__(self, regressionModel=linear_model.LinearRegression(), numAttrs=5, isTransformed=True):
		if numAttrs>MAX_NUMATTR:
			print("cannot use more than " + str(MAX_NUMATTR) + " attrs. Setting it to " + str(MAX_NUMATTR) + " instead.")
		self.regressionModel = regressionModel;
		self.numAttrs=5;
		self.isTransformed=True;

	def fit(self,sentences,scores):
		probs = parseProbs(sentences,self.numAttrs)
		sentenceLengths=[sentenceLength(x) for x in sentences]
		self.fitParsed(probs,sentenceLengths,scores)

	def fitParsed(self,probs,sentenceLengths,scores):
		attrs = self.createAttrs(probs,sentenceLengths)
		self.regressionModel.fit(np.array(attrs),scores)

	def predict(self,sentences):
		probs = parseProbs(sentences,self.numAttrs)
		sentenceLengths=[sentenceLength(x) for x in sentences]
		return self.predictParsed(probs,sentenceLengths)

	def predictParsed(self,probs,sentenceLengths):
		attrs = self.createAttrs(probs,sentenceLengths)
		return self.regressionModel.predict(np.array(attrs))

	def createAttrs(self, probs, sentenceLengths):
		attrs = [x[:self.numAttrs] for x in probs]
		if self.isTransformed:
			attrs = [np.divide(attrs[i],sentenceLengths[i]) for i in range(len(sentenceLengths))]
		return attrs
			
class NoReg:
	def __init__(self):
		pass

	def fit(self,X,y):
		pass

	def predict(self,X):
		return [x[0] for x in X]

def loadModel(modelFileName="pretrained_model"):
	return pickle.load(open(modelFileName,"rb"))

def trainAndSaveModel(trainFileName="data/errorCountCorpus_train", modelFileName="pretrained_model", regressionModel=linear_model.LinearRegression(), numAttrs=5, isTransformed=False):
	X,y = data_load.loadErrorCountDataToScore(trainFileName)

	print("parsing...")
	probs = parseProbs(X)
	sentenceLengths=[len(x) for x in X]
	print("parsing done")
	grammarScorer = GrammarScorer(NoReg())
	grammarScorer.fitParsed(probs,sentenceLengths,y)
	pickle.dump(grammarScorer,open(modelFileName,"wb"))