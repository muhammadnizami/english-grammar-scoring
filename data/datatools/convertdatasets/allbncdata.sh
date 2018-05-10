for i in 2554/2554/download/Texts/*/*/*.xml; do echo "converting $i"; python3 BNCtoGenERRateSGML.py 2554/2554/download/Texts/C/CL/CLU.xml >> allbncdata; done
