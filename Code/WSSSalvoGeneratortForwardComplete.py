import golly as g 
from WSSStapler import *
from RecipeManager import *
from WssReader import *
from gotoAPI import *

'''
hwssRecipe = [-4, -14, -8, 20, 22, 24, 32, 12, 24, 30, 48, 48, 38, 44, 72, 74, 76, 84, 64, 76, 82, 100, 100, 90, 96, 124, 126, 128, 136, 116, 128, 134, 152, 152, 158, 158, 148, 146, 148, 140, 140, 136, 150, 158, 146, 148, 160, 150, 140, 146, 164, 164, 162, 162, 168, 162, 156, 170, 154, 164, 172, 166, 170, 178, 174, 176, 162, 160, 162, 176, 166, 168, 180, 174, 170, 152, 156, 160, 168, 186, 160, 160, 158, 150, 170, 176, 162, 182, 180, 172, 192, 198, 184, 214, 214, 214, 218, 220, 218, 220, 228, 238, 240, 230, 236, 254, 254, 260, 258, 250, 252, 250, 256, 254, 266, 274, 268, 258, 260, 272, 256, 240, 256]
hwssRecipe.insert(63,'SKIP')
hwssRecipe.insert(63,'SKIP')
hwssRecipe.insert(97,'SKIP')
hwssRecipe.insert(97,'SKIP')


#hwssRecipe = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
hwssRecipe = [6, 6, 8, 8, 6, 6, -2, 2, 14, 6, 2]
'''

step = 250
period = 2000
directionType = "B"

distBack = period / 2 + step
distForward = period / 2 - step

def PlaceReadingHeads(hwssRecipe):

	g.new("")

	if directionType == "B":
		for y in xrange(-3 * len(hwssRecipe), 1):
			MakeBackwardSalvo(step, 0, distBack * y, step * len(hwssRecipe) + 100, y == 0, y == 0)
		
		MakeBackwardRecipe(step, 0, 0, hwssRecipe)
		
	else:
		for y in xrange(0, 3 * len(hwssRecipe) + 1):
		   MakeForwardSalvo(step, 0, distForward * y, -step * len(hwssRecipe) - 100, y == 0, y == 0)
		
		MakeForwardRecipe(step, 0, 0, hwssRecipe)

def FindWssByDirection(isUp, modY):
	wssList = pickle.load(open(path.join(g.getdir("data"),"WssData.pkl"),"rb") )
	wssLaneList = pickle.load(open(path.join(g.getdir("data"),"WssLaneData.pkl"),"rb") )
	
	dy = 0
	if isUp:
		dy = 1
		
	objects = []
	
	for i in xrange(dy, len(wssList), 2):
		objects += FindObj(wssList[i], i)
		
	objects.sort()
	
	result = []
	
	for obj in objects:
		if len(result) == 0:
			x, y, v = obj
			result.append((x, y % modY, v))
		else:
			x, y, v = result[len(result) - 1]
			nx, ny, nv = obj
			
			if x == nx and y % modY == ny % modY and v == nv:
				continue
				
			result.append((nx, ny % modY, nv))
	
	tempRes = []
	
	for r in result:
		x, y, v = r
		l, r = wssLaneList[v]
		
		if isUp:
			tempRes.append((x + r, x, y, v))
		else:
			tempRes.append((x + l, x, y, v))
	
	tempRes.sort()
	
	result = [] 
	
	for r in tempRes:
		t, x, y, v = r 
		result.append((x, y, v))
		
	return result

def TestRecipe(recipe, recipes):
	recipes.Goto(-23, 1)
	
	for i in xrange(0, len(recipe)):
		recipes.recipe.append(recipe[i] + recipes.blockY - recipes.blockX)
		
	PlaceReadingHeads(recipes.recipe)
	
	goto(150000)
	g.fit()
	g.update()
	
	x, y, res = FindWssByDirection(True, distForward)[0]
	x += 23
	y += -21
	y = y % distForward
	
	g.show(str((x, y, res)))
	
def CreateWssMovementData(recipes, dir):

	result = [] 
	
	g.show(str(len(recipes.WssCreator)))
	for i in xrange(0, len(recipes.WssCreator)):
	
		recipes.Reset()
		recipes.Goto(-23, 1)
		recipes.AddWss(i)

		PlaceReadingHeads(recipes.recipe)
		goto(150000)
		g.fit()
		g.update()
		
		x, y, res = FindWssByDirection(True, distForward)[0]
		x += 23
		y += -21
		y = y % distForward
		
		result.append((x, y, res))
		
	pickle.dump(result, open(path.join(dir, str(step) + "_" + str(period) + "_ForwardWssBase.pkl"), "wb"))
	g.note(str(result))

def FingRecipeIdx(dx, dy, wssTypeIdx, wssMovementList):
	
	parity = (dx + dy) % 2
	
	idx = 0
	
	for move in wssMovementList:
		mx, my, t = move
		
		if (mx + my) % 2 == parity and t == wssTypeIdx:
			break
		
		idx += 1
		
	return idx
	
def PlaceWssAt(dx, dy, wssTypeIdx, wssMovementList, recipes, modY):

	idx = FingRecipeIdx(dx, dy, wssTypeIdx, wssMovementList)
	
	rx = wssMovementList[idx][0]
	ry = wssMovementList[idx][1]
	
	xD = dx - rx
	yD = (ry - dy - xD) / 2
	
	if (yD + xD) % 2 != 0:
		yD += modY/2
	
	yD = yD % modY
	
	if yD > modY/2:
		yD -= modY
	
	recipes.Goto(xD, yD)
	
	eX = xD + rx
	eY = -xD - 2 * yD + ry
	
	
	while True:
		skipState = (len(recipes.recipe) + 1) % 3
		skipDelta = (2 * step)
	
		cY = (eY + skipState * skipDelta) % distForward
		
		if cY != dy:
			recipes.recipe.append('SKIP')
		else:
			break
	
	recipes.AddWss(idx)
	
def SaveSalvoData():
	g.new("")
	MakeForwardSalvo(step, 0, 0, 0, True, True)
	g.run(3)
	
	forwardRecipe = FindWssByDirection(True, 750)
	forwardRecipe.reverse()
	fRecipe = [] 

	for i in xrange(0, len(forwardRecipe)):
		x, y, d = forwardRecipe[i]
		fRecipe.append((x - 400, y + 1, d))
		
	pickle.dump(fRecipe, open(path.join(dir, str(step) + "_ForwardSalvo.pkl"), "wb"))
	
dir = r'C:\Users\SimSim314\Documents\GitHub\GlueNew\Glue\MonochromaticP2'
recipes = RecipeConstructor()

recipes.Init(path.join(dir, "OptimizedEven.txt"), path.join(dir, "OptimizedOdd.txt"), path.join(dir, "WSS.txt"))
#recipes.Init(path.join(dir, "1.txt"), path.join(dir, "1.txt"), path.join(dir, "WSS.txt"))
#CreateWssMovementData(recipes, dir)
#SaveSalvoData()

wssMovementList = pickle.load(open(path.join(dir, str(step) + "_" + str(period) + "_ForwardWssBase.pkl"),"rb"))
wssForward = pickle.load(open(path.join(dir, str(step) + "_ForwardSalvo.pkl"),"rb"))

#TestRecipe([-4,-12,-6,-2,-8,-6,-12,-10,-12,-16,-6,-10,-8], recipes)
#g.show(str(wssForward))

#recipes.Goto(-23, 1)
#idx = FingRecipeIdx(-150, 0, 19, wssMovementList)
#recipes.AddWss(idx)

shufle = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
#shufle = [3, 4, 5]
for i in xrange(0, len(shufle)):
	x, y, tw = wssForward[shufle[i]]
	PlaceWssAt(x, y, tw, wssMovementList, recipes, 250)

	
#PlaceWssAt(-150, 0, 9, wssMovementList, recipes, 250)
#PlaceWssAt(-198, 182, 9, wssMovementList, recipes, 250)

PlaceReadingHeads(recipes.recipe)
#goto(1500000)
#g.note(str(FindWssByDirection(True, distForward)))

#g.show(str(wssMovementList[0]))

#recipes.AddWss(0)
#recipes.MoveBy(-23, -23, 1)
#recipes.Goto(-52, 109)
#idx = FingRecipeIdx(-150, 0, 21, wssMovementList)
#recipes.AddWss(idx)
#g.show(str(wssMovementList[idx]))
	
#recipes.Goto(-23, 1)

#PlaceWssAt(-150, 21, 21, wssMovementList, recipes, 250)
#g.show(str(recipes.sequence))
#PlaceReadingHeads(recipes.recipe)
#goto(6000000)
#g.note(str(FindWssByDirection(True, distForward)))

#Run + dy(0) - 0, 1
#Run + dy(1) - 3