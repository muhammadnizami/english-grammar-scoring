import sys

import xml.etree.ElementTree as ET

words=set()

inputFileName = sys.argv[1]
tree = ET.parse(inputFileName)
sentencexmlelems = tree.findall('.//s')

for sentenceelem in sentencexmlelems:
	for wordelem in sentenceelem.iter():
		if wordelem.tag=='w' or wordelem.tag=='c':
			if wordelem.text is not None:
				pos = str(wordelem.get('pos'));
				if pos == "None":
					pos = str(wordelem.get('c5'));
				words.add(wordelem.text.strip()+" "+pos)

for word in words:
	print(word)

