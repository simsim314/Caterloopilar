import golly as g 
import random
import pickle
from os import path

def CalculateLane(cells):
	g.new("")
	g.putcells(cells)
	cells = g.getcells(g.getrect())
	g.new("")
	g.putcells(cells, -cells[0], -cells[1])
	
	minx = 1000
	maxx = -1000
	
	for i in xrange(0, 4):
		rect = g.getrect()
		
		minx = min(minx, rect[0])
		maxx = max(maxx, rect[0] + rect[2])
		g.run(1)
		
	return (minx, maxx)
	
def PrepareList(cells):
	g.new("")
	g.putcells(cells)
	cells = g.getcells(g.getrect())
	g.new("")
	g.putcells(cells, -cells[0], -cells[1])
	c = g.getcells(g.getrect())
	
	result = []
	
	for i in xrange(0, len(c), 2):
		x = c[i]
		y = c[i + 1]
		
		for dx in xrange(-1,2):
			for dy in xrange(-1, 2):
				val = g.getcell(x + dx, y + dy)
				
				if (x + dx, y + dy, val) in result:
					continue
					
				result.append((x + dx, y + dy, val))

	random.shuffle(result)
	
	return result

def SaveWssLane(file):

	g.setrule("b3/s23")
	wss = [g.parse("bobo$4bo$o3bo$o3bo$4bo$bo2bo$2b3o!"), g.parse("bobo$4bo$o3bo$4bo$bo2bo$2b3o!"), g.parse("obo$3bo$3bo$o2bo$b3o!")]

	wssList = []
	for w in wss:
		for i in xrange(0, 4):
			wssList.append(CalculateLane(g.evolve(w, i)))
			wssList.append(CalculateLane(g.transform(g.evolve(w, i), 0, 0, 1, 0, 0, -1)))
	
	pickle.dump(wssList, open(path.join(g.getdir("data"),file), "wb"))

def SaveWss(file):

	g.setrule("b3/s23")
	wss = [g.parse("bobo$4bo$o3bo$o3bo$4bo$bo2bo$2b3o!"), g.parse("bobo$4bo$o3bo$4bo$bo2bo$2b3o!"), g.parse("obo$3bo$3bo$o2bo$b3o!")]

	wssList = []
	for w in wss:
		for i in xrange(0, 4):
			wssList.append(PrepareList(g.evolve(w, i)))
			wssList.append(PrepareList(g.transform(g.evolve(w, i), 0, 0, 1, 0, 0, -1)))
	
	pickle.dump(wssList, open(path.join(g.getdir("data"),file), "wb"))

def FindObj(objData, idx):
	c = g.getcells(g.getrect())
	
	result = []
	
	for i in xrange(2, len(c), 3):
		#g.show(str(i) + "/" + str(len(c)))
		x = c[i - 2]
		y = c[i - 1]
		
		found = True
		
		for r in objData:
			dx, dy, v = r
			
			if g.getcell(x + dx, y + dy) != v:
				found = False
				break
		
		if found:
			result.append((x, y, idx))
	
	return result 
	
def FindObjects(objDataList):	
	result = []
	for i in xrange(0, len(objDataList)):
		result += FindObj(objDataList[i], i)
	
	return result

#SaveWssLane("WssLaneData.pkl")
#g.show(str(wssList))
#SaveWss("WssData.pkl")
#wssList = pickle.load(open(path.join(g.getdir("data"),"WssData.pkl"),"rb") )
#objects = FindObjects(wssList)
#objects.sort()
#g.show(str(objects))

