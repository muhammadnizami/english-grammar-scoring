import numpy as np
from bllipparser import RerankingParser
from sklearn import datasets, linear_model, neural_network, metrics
from pathlib import Path

import data_load
import grammar_scoring

X,y = data_load.loadErrorCountDataToScore("data/errorCountCorpus_train")
Xtest,ytest = data_load.loadErrorCountDataToScore("data/errorCountCorpus_test")

print("parsing...")
probs = grammar_scoring.parseProbs(X)
sentenceLengths=[grammar_scoring.sentenceLength(x) for x in X]
probsTest = grammar_scoring.parseProbs(Xtest)
sentenceLengthsTest=[grammar_scoring.sentenceLength(x) for x in Xtest]
print("parsing done")


print("EXPERIMENTS")
classifiers = [linear_model.LinearRegression(), neural_network.MLPRegressor(hidden_layer_sizes=(5,))]
numAttrs = [1,3,5]
isTransformeds = [True,False]

print("NoReg")
print("train:")
grammarScorer = grammar_scoring.GrammarScorer(grammar_scoring.NoReg())
grammarScorer.fitParsed(probs,sentenceLengths,y)
y_predict = grammarScorer.predictParsed(probs,sentenceLengths)
with open("experiment-train-NoReg","w") as outfile:
	for item in y_predict:
		outfile.write(str(item)+"\n")
print("corr:")
print(np.corrcoef(y_predict,y))
print("test:")
y_predict = grammarScorer.predictParsed(probsTest,sentenceLengthsTest)
with open("experiment-test-NoReg","w") as outfile:
	for item in y_predict:
		outfile.write(str(item)+"\n")
print("corr:")
print(np.corrcoef(y_predict,ytest))

for isTransformed in isTransformeds:
	for classifier in classifiers:
		for numAttr in numAttrs:
			print(str(type(classifier).__name__)+",numAttrs:"+str(numAttr)+",isTransformed:"+str(isTransformed))
			print("train:")
			grammarScorer=grammar_scoring.GrammarScorer(classifier,numAttr,isTransformed)
			grammarScorer.fitParsed(probs,sentenceLengths,y)
			y_predict = grammarScorer.predictParsed(probs,sentenceLengths)
			with open("experiment-train-"+str(type(classifier).__name__)+",numAttrs:"+str(numAttr)+",isTransformed:"+str(isTransformed),"w") as outfile:
				for item in y_predict:
					outfile.write(str(item)+"\n")
			print("corr:")
			print(np.corrcoef(y_predict,y))
			print("mse:")
			print(metrics.mean_squared_error(y,y_predict))
			print("test:")
			y_predict = grammarScorer.predictParsed(probsTest,sentenceLengthsTest)
			with open("experiment-test-"+str(type(classifier).__name__)+",numAttrs:"+str(numAttr)+",isTransformed:"+str(isTransformed),"w") as outfile:
				for item in y_predict:
					outfile.write(str(item)+"\n")
			print("corr:")
			print(np.corrcoef(y_predict,ytest))
			print("mse:")
			print(metrics.mean_squared_error(ytest,y_predict))