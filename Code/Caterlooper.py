import golly as g 
from WSSStapler import *
from RecipeManager import *
from WssReader import *
from gotoAPI import *

def GotoLimited(gen, power):
	g.setbase(8)
	g.setstep(power)

	while gen > int(g.getgen()) + g.getbase()**power:
		g.step()
		g.update()
		
	goto(gen)
	
def CalcHelix(hwssRecipe):
	helixD = -step * len(hwssRecipe) - 2 * distBack
		
	while helixD % (2 * distBack) != 0:
		helixD -= 1
	
	return helixD
	
def PlaceReadingHeads(hwssRecipe):
	global fenseX
	
	g.new("")
	g.setrule("LifeHistoryNoMark")
	
	if directionType == "B":
		dist = int(1.5 * len(hwssRecipe) / speed)
		for y in xrange(-dist, 1):
		
			MakeBackwardSalvo(step, 0, distBack * y, step * len(hwssRecipe) + 100, y == 0, y == 0)
		
		MakeBackwardRecipe(step, 0, 0, hwssRecipe)
		
		rect = g.getrect()
		
		cells = []

		for i in xrange(1200, step * len(hwssRecipe) + 1501):
			
			cells.append(rect[0]-50)
			cells.append(i)
			cells.append(6)
		
		g.putcells(cells)
		g.putcells(cells, rect[0]-1000, 0)
		
	else:
	
		helixD = CalcHelix(hwssRecipe)
		dist = int(1.5 * len(hwssRecipe) / speed)
		for y in xrange(0, dist + 1):
		   MakeForwardSalvo(step, 0, distForward * y, helixD, y == 0, y == 0)
		
		MakeForwardRecipe(helixD, step, 0, 0, hwssRecipe)
		rect = g.getrect()
		
		cells = []
		
		fenseX = rect[0] + rect[2] + 50
		
		for i in xrange(fenseY, -helixD + 201):
			
			cells.append(rect[0] + rect[2] + 50)
			cells.append(i + helixD)
			cells.append(6)
		
		g.putcells(cells)
		
		
def FindWssByDirection(isUp, modY):
	wssList = pickle.load(open("WssData.pkl","rb"))
	wssLaneList = pickle.load(open("WssLaneData.pkl","rb"))
	
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
			
			if modY != -1:
				result.append((x, y % modY, v))
			else:
				result.append((x, y, v))
		else:
			
			nx, ny, nv = obj
			
			nmdY = ny 
			
			if modY != -1:
				nmdY = ny % modY
				
			if (nx, nmdY, nv) in result:
				continue
				
			result.append((nx, nmdY, nv))
	
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
	
def CreateWssMovementData(recipes, dir, isUp = True):

	result = [] 
	
	for i in xrange(0, len(recipes.WssCreator)):
		
		recipes.Reset()
		
		if isUp:
			recipes.Goto(-23, 1)
			
		recipes.AddWss(i)

		PlaceReadingHeads(recipes.recipe)
		
		if isUp:
			
			gen = period * (len(recipes.recipe) + 10)
			
			while gen % (2 * distForward) != 0:
				gen += 1
			
			goto(gen)
			g.fit()
			g.update()
			rect = g.getrect()
			
			g.select([rect[0], -6 * distBack, rect[2], 7 * distBack])
			g.clear(1)
			
			x, y, res = FindWssByDirection(isUp, distForward)[0]
		
			x += 23
			y += -21
			y = y % distForward
		else:
			
			gen = period * (len(recipes.recipe) + 10)
			
			while gen % (2 * distBack) != 0:
				gen += 1
			
			goto(gen)
			g.fit()
			g.update()
			
			rect = g.getrect()
			helixy = CalcHelix(recipes.recipe)
			
			g.select([rect[0], helixy - distBack, rect[2], 7 * distBack])
			g.clear(1)
			
			x, y, res = FindWssByDirection(isUp, distBack)[0]
			y = y % distBack
			
		result.append((x, y, res))
	if isUp:	
		pickle.dump(result, open(path.join(dir, str(step) + "_" + str(period) + "_ForwardWssBaseAuto.pkl"), "wb"))
	else:
		pickle.dump(result, open(path.join(dir, str(step) + "_" + str(period) + "_BackwardWssBaseAuto.pkl"), "wb"))
	
	recipes.Reset()
	#g.note(str(result))

def FingRecipeIdx(dx, dy, wssTypeIdx, wssMovementList):
	
	parity = (dx + dy) % 2
	idx = 0
	
	for move in wssMovementList:
		mx, my, t = move
		
		if (mx + my) % 2 == parity and t == wssTypeIdx:
			break
		
		idx += 1
		
	return idx

def CalcXYDiff(dx, rx, dy, ry, modY):
	
	xD = dx - rx
	yD = (ry - dy - xD) / 2
	
	if (yD + xD) % 2 != 0:
		yD += modY/2
	
	yD = yD % modY
	
	if yD > modY/2:
		yD -= modY
	
	return (xD, yD)

def BackwardPlaceWssAt(dx, dy, wssTypeIdx, wssMovementList, recipes, modY):

	idx = FingRecipeIdx(dx, dy, wssTypeIdx, wssMovementList)
	
	rx = wssMovementList[idx][0]
	ry = wssMovementList[idx][1]
	
	xD, yD = CalcXYDiff(dx, rx, dy, ry, modY)
	recipes.Goto(-xD, -yD)
	#g.note(str((-xD, -yD, recipes.blockX, recipes.blockY)))
	
	eX = xD + rx
	eY = -xD - 2 * yD + ry
	
	while True:
		skipState = len(recipes.recipe) % modBack
		skipDelta = (2 * step)
	
		cY = (eY + skipState * skipDelta) % distBack
		
		if cY != dy:
			recipes.recipe.append('SKIP')
		else:
			break
	
	recipes.AddWss(idx)
	
def ForwardPlaceWssAt(dx, dy, wssTypeIdx, wssMovementList, recipes, modY):

	idx = FingRecipeIdx(dx, dy, wssTypeIdx, wssMovementList)
	
	rx = wssMovementList[idx][0]
	ry = wssMovementList[idx][1]
	
	xD, yD = CalcXYDiff(dx, rx, dy, ry, modY)
	
	recipes.Goto(xD, yD)
	
	eX = xD + rx
	eY = -xD - 2 * yD + ry
	
	while True:
		skipState = (len(recipes.recipe) + 1) % modForward
		skipDelta = (2 * step)
	
		cY = (eY + skipState * skipDelta) % distForward
		
		if cY != dy:
			recipes.recipe.append('SKIP')
		else:
			break
	
	recipes.AddWss(idx)

#Need to accuratly place F and B together 	
def SaveBackwardSalvoData(dir):
	
	bRecipe = FindWssByDirection(False, distBack)
	bRecipe.reverse()
		
	pickle.dump(bRecipe, open(path.join(dir, str(step) + "_BackwardSalvoAuto.pkl"), "wb"))
		
def SaveForwardSalvoData(dir):
	g.new("")
	MakeBackwardSalvo(step, 0, 0, 0, True, True)
	rectB = g.getrect()
	
	g.new("")
	MakeForwardSalvo(step, 0, 0, 0, True, True)
	rectF = g.getrect()
	
	g.run(3)

	forwardRecipe = FindWssByDirection(True, distForward)
	forwardRecipe.reverse()
	fRecipe = [] 
	
	dx = rectB[0] - (rectF[0] + rectF[2]) - 100
	dx = int(dx / 8) * 8
	
	for i in xrange(0, len(forwardRecipe)):
		x, y, d = forwardRecipe[i]
		fRecipe.append((x + dx, y + 1, d))
		
	pickle.dump(fRecipe, open(path.join(dir, str(step) + "_ForwardSalvoAuto.pkl"), "wb"))

def AdaptiveGoto(hwssRecipe, enablePrinting = True):

	#g.setrule("LifeHistory")
	fense50 = g.parse("F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F$F!")

	helixD = CalcHelix(hwssRecipe)
		
	curgen = -helixD * 2
	curgen += 2 * distForward
	
	goto(curgen)
	g.setbase(8)
	g.setstep(3)
	
	delta = 10
	lastmaxi = delta
	idx = 0
	
	for i in hwssRecipe:
		
		if enablePrinting and (100 * (idx + 1)) / len(hwssRecipe) != (100 * idx) / len(hwssRecipe):
			percent = (100 * (idx + 1)) / len(hwssRecipe)
			g.update()
			
			g.show("Iterating forward progress " + str(percent) + "%")
			
		curgen += 2 * distForward
		idx += 1
		
		while int(g.getgen()) < curgen:
			g.step()
			
		if i == 'SKIP':
			continue 
			
		if i > lastmaxi:
			
			g.select([fenseX, helixD + fenseY + lastmaxi - delta, 1, delta])
			g.clear(0)
			lastmaxi += delta
			#g.update()
			
		if i < lastmaxi - delta:
			g.putcells(fense50, fenseX, helixD + fenseY + lastmaxi - 2 * delta)
			lastmaxi -= delta
			#g.update()
		
		#g.run(2 * distForward)
		#g.update()
		
def ConvertToRelative(recipe, modY):

	for idx in xrange(len(recipe)):
		idx = len(recipe) - 1 - idx
		x0, y0, i0 = recipe[0]
		x, y, i = recipe[idx]
		x -= x0
		y -= y0
		
		recipe[idx] = (x, y % modY, i)

def ConvertToList(sequence):
	
	result = []
	
	for item in sequence:
		try:
			i = len(item)
		except:
			result.append(item)
			
	return result

userSpeed = g.getstring("Please enter step/period", "1/8")

if userSpeed.split("/")[0] == 'c':
	userSpeed = userSpeed.replace("c", "1")
else:
	userSpeed = userSpeed.replace("c", "")
	
iniStep = int(userSpeed.split("/")[0]) 
iniPeriod = int(userSpeed.split("/")[1])

speed = float(iniStep) / iniPeriod

if speed >= 0.25:
	g.exit("This speed should be strictly less than c/4")

if (iniPeriod + 2 * iniStep) % 8 == 0:
	g.exit("This period and step are not supported: period + 2 * step, should not be 0 mod 8")

if (iniPeriod - 2 * iniStep) % 8 == 0:
	g.exit("This period and step are not supported: period - 2 * step, should not be 0 mod 8")

fenseY = 220
fenseX = 0 

for k in xrange(1, 1000000):

	step = iniStep * k
	period = iniPeriod * k
	distBack = period / 2 + step
	distForward = period / 2 - step
	speed = float(step) / period

	if step % 2 != 0 or period % 4 != 0 or step < 98 or period < 892:
		continue 
	
	if (period - 2 * step) % 8 == 0:
		continue
	
	if (period + 2 * step) % 8 == 0:
		continue
	
	g.show("Searching for valid period/step, " + str(step) + "/" + str(period))
	
	directionType = "F"
	PlaceReadingHeads([6,6,8,8,6,6,-2,2,14,6,2])
	
	rect = g.getrect()
	
	AdaptiveGoto([6,6,8,8,6,6,-2,2,14,6,2], False)
	
	g.fit()
	g.update()
	
	newRect = g.getrect()
	
	if newRect[2] > 2 * rect[2]:
		continue 
	
	break
	
modForward = 1
while (2 * step * modForward) % distForward != 0:
	modForward += 1

modBack = 1
while (2 * step * modBack) % distBack != 0:
	modBack += 1

modDY = distBack / modBack

#Crucial init don't mark
directionType = "B"
#dir = r'C:\Users\SimSim314\Documents\GitHub\GlueNew\Glue\MonochromaticP2'
dir = g.getdir("temp")

g.show("Loading slow salvo recipes")
recipes = RecipeConstructor()
recipes.Init("OptimizedEven.txt", "OptimizedOdd.txt", "WSS.txt")

#This code creates the Tail part of the caterloopillar
g.show("Calculating WSS relative movement for Tail")
SaveForwardSalvoData(dir)
CreateWssMovementData(recipes, dir, True)

wssMovementList = pickle.load(open(path.join(dir, str(step) + "_" + str(period) + "_ForwardWssBaseAuto.pkl"),"rb"))
wssForward = pickle.load(open(path.join(dir, str(step) + "_ForwardSalvoAuto.pkl"),"rb"))

g.show("creating the Tail part of the caterloopillar")
recipes.Goto(-23, 1)

shufle = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
for i in xrange(0, len(shufle)):
	x, y, tw = wssForward[shufle[i]]
	ForwardPlaceWssAt(x, y, tw, wssMovementList, recipes, modDY)

recipes.DeleteBlock()

PlaceReadingHeads(recipes.recipe)

l = len(recipes.recipe) * step

iters = int(l / speed + l * 2 + l * (1 + 2 * speed) / (0.5 - speed))
iters = (1 + int(iters / distForward)) * distForward

g.show("Iterating Tail to reach " + str(iters) + " iter")
g.fit()
g.update()
#The speed is negative 
Head = -speed * iters + 576
Tail = -speed * (iters - l * 2) + l + 576

GotoLimited(iters, 5)
rect = g.getrect()

g.select([rect[0], Head - 3 * distBack, rect[2], Tail - Head + 3 * distBack + 1500])
g.clear(1)

g.save(path.join(dir, str(step) + "_" + str(period) + "_Back.rle"), "rle", False)

#'''

#This code synchronize the backward recipes to fit with forward created at 0,0
g.show("synchronize the backward recipes to fit with forward")

g.new("")
MakeForwardSalvo(step, 0, 0, 0, True, True)
forwardRecipe = FindWssByDirection(True, distForward)
x0, y0, id  = forwardRecipe[0]
ConvertToRelative(forwardRecipe, distForward)

g.open(path.join(dir, str(step) + "_" + str(period) + "_Back.rle"), False)
rect = g.getrect()

cells = g.getcells([rect[0], rect[1], rect[2], 4 * distBack])
g.new("")
g.putcells(cells)

for i in xrange(4):
	cRecipe = FindWssByDirection(True, distForward)
	x1, y1, id1 = cRecipe[0]
	
	ConvertToRelative(cRecipe, distForward)

	if str(forwardRecipe) == str(cRecipe):
		break
		
	g.run(1)

dgen = int(g.getgen())

cells = g.getcells(g.getrect())

dx = x1 - x0
dy = y1 - y0

g.new("")
g.putcells(cells, -dx, -dy)

SaveBackwardSalvoData(dir)
#'''

#This code creates the Head of the caterloopillar

recipes.Reset()
g.show("Calculating WSS relative movement for Head")

directionType = "F"
CreateWssMovementData(recipes, dir, False)

wssMovementList = pickle.load(open(path.join(dir, str(step) + "_" + str(period) + "_BackwardWssBaseAuto.pkl"),"rb"))
wssBackward = pickle.load(open(path.join(dir, str(step) + "_BackwardSalvoAuto.pkl"),"rb"))

g.show("Creating the Head of the caterloopillar")

shufle = [0, 1, 3, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]

for i in xrange(0, len(shufle)):
	x, y, tw = wssBackward[shufle[i]]
	BackwardPlaceWssAt(x, y, tw, wssMovementList, recipes, modDY)

recipes.DeleteBlock()

helixD = CalcHelix(recipes.recipe)
PlaceReadingHeads(recipes.recipe)
g.fit()
g.update()
AdaptiveGoto(recipes.recipe)

gen = int(g.getgen())
GotoLimited(gen + 4 * distBack * period / step, 4)

while int(g.getgen()) % 4 != (4 - dgen) % 4:	
	g.run(1)
	
g.save(path.join(dir, str(step) + "_" + str(period) + "_Front.rle"), "rle", False)

#'''

#This code adjusts the front and the back to be at the same "rail" at the edge and combines them. 
g.show("Adjustsing the front and the back to be at the same rail")

g.open(path.join(dir, str(step) + "_" + str(period) + "_Back.rle"), False)
rect = g.getrect()

cells = g.getcells([rect[0], rect[1], rect[2], 3 * distBack])
g.new("")
g.putcells(cells)

xFT, yFT, diFT = FindWssByDirection(True, -1)[0]
wssBack = FindWssByDirection(False, -1)

i = 0
while True:
	if wssBack[len(wssBack) - 1 - i][0] == wssBack[len(wssBack) - 1][0]:
		i += 1
	else:
		i-=1 
		break

xBT, yBT, diBT = wssBack[len(wssBack) - 1 - i]
dY = yBT - yFT
dX = xBT - xFT

g.open(path.join(dir, str(step) + "_" + str(period) + "_Front.rle"), False)
rect = g.getrect()
cells = g.getcells([rect[0], helixD - 4 * distBack, rect[2], 3 * distBack])

g.new("")
g.putcells(cells)

wssFront = FindWssByDirection(True, -1)
wssBack = FindWssByDirection(False, -1)

i = 0
while True:
	if wssFront[i][0] == wssFront[0][0]:
		i += 1
	else:
		i-=1 
		break
		
xFF, yFF, diFF = wssFront[i]

idx = len(wssBack) - 1
xt, yt, it = wssBack[idx]

if (yt - yFF) % 4 != dY % 4:
	idx -= 1
	xt, yt, it = wssBack[idx]

if (yt - yFF) > dY:
	yt -= 2 * distBack
	
iter = dY - (yt - yFF)
yFF -= iter / 2 

moveX = xFF - xFT
moveY = yFF - yFT

g.open(path.join(dir, str(step) + "_" + str(period) + "_Front.rle"), False)
g.run(iter)
rect = g.getrect()
cells = g.getcells([rect[0], rect[1], rect[2], yFF + 30 - rect[1]])
g.open(path.join(dir, str(step) + "_" + str(period) + "_Back.rle"), False)
g.putcells(cells, -moveX, -moveY)
g.setrule("b3/s23")
g.save(str(step) + "_" + str(period) + "_Caterloopillar.rle", "rle", False)
g.show("Finish! Here's the " + str(step) + "/" + str(period) + " caterloopillar!! Hooray")
#'''