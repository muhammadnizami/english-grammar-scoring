import sys

import xml.etree.ElementTree as ET

inputFileName = sys.argv[1]
tree = ET.parse(inputFileName)
sentencexmlelems = tree.findall('.//s')

for sentenceelem in sentencexmlelems:
	sys.stdout.write('<s>')
	for wordelem in sentenceelem.iter():
		if wordelem.tag=='w' or wordelem.tag=='c':
			if wordelem.text is not None:
				sys.stdout.write(wordelem.text.replace("\n","").strip())
				sys.stdout.write(' ')
	print('</s>')

