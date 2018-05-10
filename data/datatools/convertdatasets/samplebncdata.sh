rm samplebncdata
touch samplebncdata

for i in 2554/2554/download/Texts/A/A0/A00.xml; do 
echo "converting $i"; python3 BNCtoGenERRateSGML.py $i >> samplebncdata; done

for i in 2554/2554/download/Texts/A/A0/A00.xml; do 
echo "converting $i"; python3 BNCtoWordList.py $i >> samplebncwordlist; done