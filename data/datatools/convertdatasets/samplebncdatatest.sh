rm samplebncdatatest
touch samplebncdatatest

for i in 2554/2554/download/Texts/B/B0/B01.xml; do 
echo "converting $i"; python3 BNCtoGenERRateSGML.py $i >> samplebncdatatest; done
