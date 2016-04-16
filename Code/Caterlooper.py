import golly as g 
from CaterlooperUtils import *

step = 154 
period = 1232

speed = float(step) / period

fenseY = 220
fenseX = 0 

distBack = period / 2 + step
distForward = period / 2 - step

modForward = 1
while (2 * step * modForward) % distForward != 0:
	modForward += 1

modBack = 1
while (2 * step * modBack) % distBack != 0:
	modBack += 1

modDY = distBack / modBack

#directionType = "F"
#PlaceReadingHeads([0,0,0,0,0,0,0,0,0,0,0,0,0,0])
#g.exit("")

#Crucial init don't mark
directionType = "B"
dir = r'C:\Users\SimSim314\Documents\GitHub\GlueNew\Glue\MonochromaticP2'

g.show("Loading slow salvo recipes")
recipes = RecipeConstructor()
recipes.Init(path.join(dir, "OptimizedEven.txt"), path.join(dir, "OptimizedOdd.txt"), path.join(dir, "WSS.txt"))

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
#g.note(str(recipes.recipe))
PlaceReadingHeads(recipes.recipe)

l = len(recipes.recipe) * step

iters = int(l / speed + l * 2 + l * (1 + 2 * speed) / (0.5 - speed))
iters = (1 + int(iters / distForward)) * distForward

g.show("Iterating Tail to reach " + str(iters) + " iter")

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

g.run(4 * distBack * period / step)

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
g.save(path.join(dir, str(step) + "_" + str(period) + "_Caterloopillar.rle"), "rle", False)
g.show("Finish! Here's the " + str(step) + "/" + str(period) + " caterloopillar!! Hooray")
#'''