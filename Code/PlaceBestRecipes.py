import golly as g
from WssReader import *

inputFile = r'C:\Users\SimSim314\Documents\GitHub\GlueNew\Glue\MonochromaticP2\WSS.txt'
outputFile = r'C:\Users\SimSim314\Documents\GitHub\GlueNew\Glue\MonochromaticP2\WSS_D.txt'
g.new("")
ins = open(inputFile, "r")
recipes = []
blokcDist = [] 
lines = [] 

for line in ins:
	
	splitVals = line.split(':')[1].split(",")
	lines.append(line)
	res = []
	for i in xrange(0, len(splitVals)):
		res.append(int(splitVals[i]))
		
	recipes.append(res)

gld = g.parse("3o$o$bo!")
block = g.parse("2o$2o!", 0, 0)

d = 0 
for r in recipes:
	g.putcells(block, d)
	for i in xrange(0, len(r)):
		g.putcells(gld, 200 * (i + 1) + d, 200 * (i + 1) + r[i])
		
	d += 1000

g.run(50000)
wssList = pickle.load(open(path.join(g.getdir("data"),"WssData.pkl"),"rb") )
objects = FindObjects(wssList)
objects.sort()

res = "Gen:50000,Step:200\n"
for i in xrange(0, len(objects)):
	x, y, val = object[i]
	x -= 1000 * i
	res += str((x, y)) + ":" + lines[i] + "\n"
	
with open(outputFile, "w") as text_file:
    text_file.write(res)