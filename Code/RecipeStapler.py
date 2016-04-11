import golly as g 
import copy

gld = g.parse("3o$o$bo!")
blck = g.parse("2o$2o!")

def FindActive():

   rect = g.getrect()
   
   cells = g.getcells([rect[0], rect[1], rect[2], 1])
   
   return [cells[0], cells[1]]
         
def FindConnected(listXY):
   result = copy.copy(listXY)
   
   for xy in listXY:
      x = xy[0]
      y = xy[1]
      
      for i in xrange(-1, 2): 
         for j in xrange(-1, 2): 
            if g.getcell(x + i, y + j) > 0 and len([i for t in listXY if (t[0] == x + i and t[1] == y + j)]) == 0:
				if len([i for t in result if (t[0] == x + i and t[1] == y + j)]) == 0:
					result.append([x + i, y + j])
         
   return result
   
def RemoveList(listXY):

   for xy in listXY:
      x = xy[0]
      y = xy[1]
      g.setcell(x, y, 0)

def CountSL():
	
	result = []
	while int(g.getpop()) > 0: 
	   xy = [FindActive()]
	   
	   while True: 
		  newXY = FindConnected(xy)
		  
		  #g.getstring(str(xy) + " : " + str(newXY) )
		  
		  if len(newXY) == len(xy):
			 break
			 
		  xy = newXY
	   
	   result.append(xy)
	   RemoveList(xy)
	  
	   
	  
	return result
  
class SlowSalvoConstructor:
	
	
	def __init__(self, path = None, SLpaths = None, SLExpected = None):
		self.blockX = 0
		self.blockY = 0
		self.sequence = []
		self.recipe = []
		self.block0 = [0,0]
		self.block1 = [0,0]
		self.splitterData1 = [[-4, -14],[-8,7],[12,5],  g.parse("5$22b2o$22b2o$2b2o$2b2o!", -10, 0)]
		self.splitterData2 = [[5, 15],[7,-8],[5,12], g.parse("2$7b2o$7b2o19$5b2o$5b2o!", 0, -10)]
		self.recipeIdxList = []
		self.lastGotoIdx = -1 
		self.SLsMoveTable = []
		self.SLsExpected = SLExpected
		self.init = g.getcells(g.getrect())
		
		if path != None:
			self.moveTable = self.LoadMoveTable(path, True)
		
		if SLpaths != None:
			for pt in SLpaths:
				self.SLsMoveTable.append(self.LoadMoveTable(pt, False))
			
	def CanApplySplit(self):
		return self.CanApplyRecipe(self.splitterData1[0], self.splitterData1[3])
		
	def ApplySplit(self, splitIdx):
		self.recipeIdxList.append("ApplySplit")
		self.recipeIdxList.append(splitIdx)
		
		if splitIdx == 0:
			splitData = self.splitterData1
		else:
			splitData = self.splitterData2
			
		self.AppendRecipe(splitData[0])
		self.block1[0]  = self.block0[0] + splitData[2][0]
		self.block1[1]  = self.block0[1] + splitData[2][1]
		
		self.block0[0]  += splitData[1][0]
		self.block0[1]  += splitData[1][1]
		
	def CanApplyRecipe(self, recipe, expected):
		g.new("")
		g.setstep(3)
		
		g.putcells(blck)
		g.putcells(self.init)
		
		for r in self.recipe:
			g.putcells(gld, 80, 80 + r)
			g.step()
		
		g.select([self.block0[0], self.block0[1], 2, 2])
		g.clear(0)
		cells = g.getcells(g.getrect())
		g.putcells(blck, self.block0[0], self.block0[1])
		delta = self.block0[1] - self.block0[0]
		
		for r in recipe:
			g.putcells(gld, 80, 80 + r + delta)
			g.step()
		
		for i in xrange(0, len(cells), 2):
			x = cells[i]
			y = cells[i + 1]
			
			if g.getcell(x, y) == 0:
				return False
				
		for i in xrange(0, len(expected), 2):
		
			x = expected[i] + self.block0[0]
			y = expected[i + 1] + self.block0[1]
			
			if g.getcell(x, y) == 0:
				return False
				
		return True
	
	def GotoSmart(self, x, y, moveTableIdx):
		return self.GotoSmartConstrained(x, y, moveTableIdx, 1000000)
	
	def GotoSmartConstrained(self, x, y, moveTableIdx, maxL):
		if moveTableIdx == -1:
			return self.Goto(x, y, self.moveTable, blck, maxL)
		else:
			return self.Goto(x, y, self.SLsMoveTable[moveTableIdx],  self.SLsExpected[moveTableIdx], maxL)
			
	def Goto(self, x, y, moveTable, expected, maxL):
		dx = x - self.block0[0]
		dy = y - self.block0[1]
		
		for i in xrange(0, len(moveTable)):
			if len(moveTable[i][2]) >= maxL:
				break
				
			x1 = moveTable[i][0]
			y1 = moveTable[i][1]
			
			if x1 == dx and y1 == dy:
				if self.CanApplyRecipe(moveTable[i][2], g.transform(expected, x1, y1)):
					self.AppendRecipe(moveTable[i][2])
					self.block0[0] = x
					self.block0[1] = y
					self.lastGotoIdx = i
					return True
		
		return False
	
	def Swap(self):
		x =  self.block0[0]
		y =  self.block0[1]
		
		self.block0[0] = self.block1[0]
		self.block0[1] = self.block1[1]
		
		self.block1[0] = x
		self.block1[1] = y
		
		self.recipeIdxList.append("Swap")
		
	def GotoAdvanced(self, x, y, tableIdx, targetL = -1):
		
		if self.GotoSmart(x, y, tableIdx):
			self.recipeIdxList.append("MOVE")
			self.recipeIdxList.append(self.lastGotoIdx)
			self.recipeIdxList.append(tableIdx)
			return True
			
		xtemp0 = self.block0[0]
		ytemp0 = self.block0[1]
		tempRecipe0 = copy.copy(self.recipe)
		
		besti = -1
		bestL = 10000000
		lastx = -1 
		lasty = -1 
		worked = []
		
		for i in xrange(0, len(self.moveTable )):
		
			x1 = self.moveTable[i][0]
			y1 = self.moveTable[i][1]
			
			if (str(x1) + "," + str(y1)) in worked:
				continue
				
			g.show(str(x) + "," + str(y) + "," + str(i) + "/" + str( len(self.moveTable )) + " BESTi = {0}, BESTL {1}".format(besti, bestL))
			g.update()
		
			self.block0[0] = xtemp0
			self.block0[1] = ytemp0
			self.recipe = copy.copy(tempRecipe0)
			
			if self.CanApplyRecipe(self.moveTable[i][2], g.transform(blck, x1, y1)):
			
				worked.append(str(x1) + "," + str(y1))
				
				self.AppendRecipe(self.moveTable[i][2])
					
				self.block0[0] += x1
				self.block0[1] += y1
				
				recipeLength = bestL - len(self.recipe)
				
				if self.GotoSmartConstrained(x, y, tableIdx, recipeLength):
					if bestL > len(self.recipe) and targetL == -1:
						bestL = len(self.recipe)
						besti = i
						
					if len(self.recipe) == targetL:
						bestL = len(self.recipe)
						besti = i
						break
		
		self.block0[0] = xtemp0
		self.block0[1] = ytemp0
		self.recipe = tempRecipe0
		
		if besti == -1: 
			return False
		else:
			self.AppendRecipe(self.moveTable[besti][2])
			x1 = self.moveTable[besti][0]
			y1 = self.moveTable[besti][1]
			
			self.block0[0] += x1
			self.block0[1] += y1
			
			self.recipeIdxList.append("MOVE")
			self.recipeIdxList.append(besti)
			self.recipeIdxList.append(-1)
			
			self.GotoSmart(x, y, tableIdx)
			
			self.recipeIdxList.append("MOVE")
			self.recipeIdxList.append(self.lastGotoIdx)
			self.recipeIdxList.append(tableIdx)
			
		return True
	
	def ApplyRecipeSmart(self, idx, moveTableIdx):
		if moveTableIdx == -1:
			self.ApplyRecipeByIndex(idx, self.moveTable)
		else:
			self.ApplyRecipeByIndex(idx, self.SLsMoveTable[moveTableIdx])
			
		self.recipeIdxList.append("MOVE")
		self.recipeIdxList.append(idx)
		self.recipeIdxList.append(moveTableIdx)
		
	def ApplyRecipeByIndex(self, idx, moveTable):
		x1 = moveTable[idx][0]
		y1 = moveTable[idx][1]
		self.AppendRecipe(moveTable[idx][2])
		self.block0[0] += x1
		self.block0[1] += y1
		
			
	def PlaceAt(self, x, y, tableIdx):
		strRes = ""
		self.ApplySplit(0)
		
		s = self.GotoAdvanced(x, y, tableIdx)
		
		if s: 
			self.Swap()
			return True

			
		return False
	
	def AppendExternalRecipe(self, recipe):	
		
		self.AppendRecipe(recipe)
		self.recipeIdxList.append("EXTERNAL")
		self.recipeIdxList.append(recipe)
		
	def AppendRecipe(self, recipe):	
		
		delta = self.block0[1] - self.block0[0]
		
		for r in recipe:
			self.recipe.append(r + delta)
	
	def PlaceActionList(self, list):
		for l in list:
			if l == "ApplySplit":
				self.ApplySplit()
			elif  l == "Swap":
				self.Swap()
			elif isinstance(l, int):
				self.ApplyRecipeByIndex(l)
			else:
				self.AppendExternalRecipe(l)
	
	def PlaceRecipe(self, x = 0, y = 0, makenew = True):
		if makenew:
			g.new("Results")
			
		g.show(str(self.recipeIdxList))
		g.setclipstr(str(self.recipeIdxList))
		g.putcells(blck, x, y)
		i = 0 
		for r in self.recipe:
			g.putcells(gld, x + 80 + i * 128, y + 80 + i * 128 + r)
			i += 1

	def LoadMoveTable(self, path, report):
		ins = open(path, "r" )
		array = []
		
		bestdxrecipe = []
		
		for line in ins:
			vals = line.split(":")
			
			vals[0] = vals[0].replace("m", "")
			vals[0] = vals[0].split(",")
			x = int(vals[0][0])
			y = int(vals[0][1])
			vals[1] = vals[1].replace("E", "").replace("\n", "")
			vals[1] = vals[1].split(",")
			
			for i in xrange(0, len(vals[1])):
				vals[1][i] = int(vals[1][i])
			
			if x - y == -1 and len(bestdxrecipe) == 0:
				bestdxrecipe = vals[1]
				
			array.append([x, y, vals[1]])
			
		if report:
			g.show(str(bestdxrecipe))
			g.setclipstr(str(bestdxrecipe))
			
		ins.close()
		
		return array	
		
	def Reset(self):
		self.blockX = 0
		self.blockY = 0
		self.sequence = []
		self.recipe = []
		self.block0 = [0,0]
		self.block1 = [0,0]
		self.recipeIdxList = []
		self.lastGotoIdx = -1 

SLfiles = []

SLfiles.append("C:\\Users\\SimSim314\\Glue\\70374[[0, 0], [-1, 1], [1, 1], [-1, 2], [0, 2]].txt")
SLfiles.append("C:\\Users\\SimSim314\\Glue\\70374[[0, 0], [-1, 1], [1, 1], [-1, 2], [1, 2], [0, 3]].txt")
SLfiles.append("C:\\Users\\SimSim314\\Glue\\70374[[0, 0], [-1, 1], [1, 1], [0, 2]].txt")
SLfiles.append("C:\\Users\\SimSim314\\Glue\\70374[[0, 0], [1, 0], [-1, 1], [1, 1], [-1, 2], [0, 2]].txt")
SLfiles.append("C:\\Users\\SimSim314\\Glue\\70374[[0, 0], [1, 0], [-1, 1], [2, 1], [0, 2], [1, 2]].txt")
SLfiles.append("C:\\Users\\SimSim314\\Glue\\70374[[0, 0], [1, 0], [-1, 1], [1, 1], [-2, 2], [0, 2], [-1, 3]].txt")
SLfiles.append("C:\\Users\\SimSim314\\Glue\\70374[[0, 0], [1, 0], [-1, 1], [2, 1], [0, 2], [2, 2], [1, 3]].txt")
SLfiles.append("C:\\Users\\SimSim314\\Glue\\70374[[0, 0], [1, 0], [0, 1], [2, 1], [1, 2]].txt")
SLfiles.append("C:\\Users\\SimSim314\\Glue\\70374[[0, 0], [1, 0], [0, 1], [2, 1], [1, 2], [2, 2]].txt")
SLfiles.append("C:\\Users\\SimSim314\\Glue\\70374[[0, 0], [-1, 1], [1, 1], [-2, 2], [0, 2], [-2, 3], [-1, 3]].txt")
SLfiles.append("C:\\Users\\SimSim314\\Glue\\70374[[0, 0], [-1, 1], [1, 1], [-2, 2], [1, 2], [-1, 3], [0, 3]].txt")
#SLfiles.append("C:\\Users\\SimSim314\\Glue\\70374[[0, 0], [1, 0], [2, 0], [0, 1], [1, 2]].txt") 
#SLfiles.append("C:\\Users\\SimSim314\\Glue\\70374[[0, 0], [1, 0], [0, 1], [2, 1], [0, 2]].txt") 
#SLfiles.append("C:\\Users\\SimSim314\\Glue\\70374[[0, 0], [1, 0], [-1, 1], [0, 1], [1, 2]].txt") 
#SLfiles.append("C:\\Users\\SimSim314\\Glue\\70374[[0, 0], [-1, 1], [0, 1], [-1, 2], [1, 2]].txt") 

sls = []
sls.append(g.parse("bo$obo$2o!", -1, 0))
sls.append(g.parse("bo$obo$obo$bo!", -1, 0)) #1 - standing beehive
sls.append(g.parse("bo$obo$bo!", -1, 0)) #2 tub
sls.append(g.parse("b2o$obo$2o!", -1, 0)) #3 (-1, 1)- ship
sls.append(g.parse("b2o$obbo$b2o!", -1, 0))
sls.append(g.parse("2b2o$bobo$obo$bo!", -2, 0)) #5 longboat (-1, 1) edge up
sls.append(g.parse("b2o$o2bo$bobo$2bo!", -1, 0)) # 6 loaf diagonal down (1,1)
sls.append(g.parse("2o$obo$bo!", 0, 0)) # 7 boat diagonal (-1,1) edge up
sls.append(g.parse("2o$obo$b2o!", 0, 0)) # 8 (1, 1)- ship
sls.append(g.parse("2bo$bobo$obo$2o!", -2, 0)) #9 longboat edge down (-1, 1)
sls.append(g.parse("2bo$bobo$o2bo$b2o!", -2, 0)) # 10 loaf diagonal up (-1,1)

salvo = SlowSalvoConstructor("C:\\Users\\SimSim314\\Glue\\70374[[0, 0], [1, 0], [0, 1], [1, 1]].txt", SLfiles, sls)
#salvo = SlowSalvoConstructor("C:\\Users\\SimSim314\\Glue\\375448[[0, 0], [1, 0], [0, 1], [1, 1]].txt", SLfiles, sls)
#-4, -13, -8, -19, -11, 1, -19



def MWSS3SLsEdgeShooter(slv):
	slv.AppendExternalRecipe([-4, -13, -8, -19, -11, 1])
	slv.block0[0] += 7
	slv.block0[1] += -10
	
	slv.ApplyRecipeSmart(3737, -1)
	slv.AppendExternalRecipe([-4, -6, -13, -5,])
	slv.block0[0] = 6
	slv.block0[1] = -28
	
	#salvo.GotoAdvanced(3, -13, 6)
	
	slv.ApplyRecipeSmart(706, -1)
	slv.ApplyRecipeSmart(282, 6)
	
	slv.block0[0] = 0
	slv.block0[1] = 0
	slv.AppendExternalRecipe([-3])

	#slv.ApplyRecipeSmart(0, 2)
	#['EXTERNAL', [-4, -13, -8, -19, -11, 1], 'MOVE', 3737, -1, 'MOVE', 0, 2]
	#salvo.GotoAdvanced(-1, -10, 2)
	slv.PlaceRecipe()
	
def HWSS3SLsEdgeShooter(slv):
	
	slv.AppendExternalRecipe([-4, -6, -8, -9, -17])
	slv.block0[0] += 19
	slv.block0[1] += -12
	
	slv.block1[0] += 17
	slv.block1[1] += 1
	
	#salvo.GotoAdvanced(12, -20, 10)
	#'MOVE', 18908, -1, 'MOVE', 297, 10
	slv.ApplyRecipeSmart(18908, -1)
	slv.ApplyRecipeSmart(297, 10)
	slv.Swap()
	#'MOVE', 1968, -1, 'MOVE', 25, 5]
	#salvo.GotoAdvanced(13, -11, 5)
	slv.ApplyRecipeSmart(1968, -1)
	slv.ApplyRecipeSmart(25, 5)

	slv.block0[0] = 0
	slv.block0[1] = 0
	slv.AppendExternalRecipe([-22, -10, -27])

	slv.PlaceRecipe()
	g.setclipstr(str(slv.recipe))

def FinadOptimalRecipe(slv, idx):
	moveTable = slv.SLsMoveTable[idx]
	bests = [-1, -1]
	slCount = [1000, 1000]
	
	g.setrule("B3/S23")
	g.setalgo("HashLife")
	
	for i in xrange(0, len(moveTable)):
		g.new("")
		
		slv.ApplyRecipeSmart(i, idx)
		slv.PlaceRecipe()
		
		g.setstep(5)
		g.step()
		
		numSL = len(CountSL())
		laneID = (moveTable[i][1] + 10000) % 2
		
		if slCount[laneID] > numSL:
			slCount[laneID] = numSL
			bests[laneID] = i
		
		slv.Reset()
		
	g.setrule("LifeHistory")
	
	for i in xrange(0, len(bests)):
		slv.ApplyRecipeSmart(bests[i], idx)
		slv.PlaceRecipe(i * 100, 0, i == 0)
		slv.Reset()
	
	g.show(str(bests))
	#11 - [32, 249]
	#12 - [138, 123]
	#13 - [29, 27]
	#14 - [89, 15]
	return bests
	
def PlaceAllRecipesForIdx(slv, idx):
	g.setrule("LifeHistory")
	
	if idx >= 0:
		moveTable = slv.SLsMoveTable[idx]
	else
		moveTable = slv.MoveTable
		
	for i in xrange(0, len(moveTable)):
		slv.ApplyRecipeSmart(i, idx)
		slv.PlaceRecipe(i * 1000, 0, i == 0)
		slv.Reset()


def PlaceAdjustment(slv):
	vals = [[11, 32], [11, 249], [12, 138], [12, 123], [13, 29], [13, 27], [14, 89], [14, 15]]
	
	g.setrule("LifeHistory")
	
	for i in xrange(0, len(vals)):
		slv.ApplyRecipeSmart(vals[i][1], vals[i][0])
		slv.PlaceRecipe(i * 100, 0, i == 0)
		slv.Reset()

wssSalvo = SlowSalvoConstructor("C:\\Users\\SimSim314\\Glue\\AllWSS\\7[24].txt", [], [])


#PlaceAdjustment(salvo)
	
#FinadOptimalRecipe(salvo, 14)
#PlaceAllRecipesForIdx(salvo, 11)
#MWSS3SLsEdgeShooter(salvo)
#HWSS3SLsEdgeShooter(salvo)
#res = [5, -3, 13, 8, -5, -7, -23, -18, 8, -15]
#salvo.AppendExternalRecipe(res)
#salvo.PlaceRecipe()
'''
hwssAdjusted = [[-4, -6, -8, -9, -17, -35, -37, -39, -47, -60, -55, -37, -35, -27, -41, -48, -41, -40, -30, -21, -21, -23, -11, -19, -31, -5, -7, -9, -10, -18, -34, -12, -2, -26, -12, -35, -44, -45, -27, -26, -11, -10, -27], [-4, -6, -8, -9, -17, -35, -37, -39, -47, -60, -55, -37, -35, -27, -41, -48, -41, -40, -30, -21, -21, -23, -11, -19, -31, -5, -7, -9, -10, -18, -34, -21, -31, -18, -6, -12, 11, 7, 5, 3, 0, 8, -1, 0, 0, -10, -27], [-4, -6, -8, -9, -17, -35, -37, -39, -47, -60, -55, -37, -35, -27, -41, -48, -41, -40, -30, -21, -21, -23, -11, -19, -31, -5, -7, -9, -10, -18, -34, -21, -30, -21, -25, -22, -31, -38, -41, -32, -18, -21, -30, -20, -10, -27], [-4, -6, -8, -9, -17, -35, -37, -39, -47, -60, -55, -37, -35, -27, -41, -48, -41, -40, -30, -21, -21, -23, -11, -19, -31, -5, -7, -9, -10, -18, -34, -11, -10, -19, -28, -23, -24, -27, -22, -20, -30, -10, -10, -27], [-4, -6, -8, -9, -17, -35, -37, -39, -47, -60, -55, -37, -35, -27, -41, -48, -41, -40, -30, -21, -21, -23, -11, -19, -31, -5, -7, -9, -10, -18, -34, -12, -2, -34, -4, -13, -22, -22, -20, -25, -13, -9, -10, -27], [-4, -6, -8, -9, -17, -35, -37, -39, -47, -60, -55, -37, -35, -27, -41, -48, -41, -40, -30, -21, -21, -23, -11, -19, -31, -5, -7, -9, -10, -18, -34, -22, -23, -24, -24, -33, -33, -32, -16, -36, -39, -10, -27], [-4, -6, -8, -9, -17, -35, -37, -39, -47, -60, -55, -37, -35, -27, -41, -48, -41, -40, -30, -21, -21, -23, -11, -19, -31, -5, -7, -9, -10, -18, -34, -12, -22, -13, -10, -5, -9, -11, -18, -15, -23, -14, -9, -5, -10, -27], [-4, -6, -8, -9, -17, -35, -37, -39, -47, -60, -55, -37, -35, -27, -41, -48, -41, -40, -30, -21, -21, -23, -11, -19, -31, -5, -7, -9, -10, -18, -34, -11, -10, -20, -10, -19, -11, -25, -28, -19, -20, -10, -27]]
hwssAdjusted[6] = [-4, -6, -8, -9, -17, -35, -37, -39, -47, -60, -55, -37, -35, -27, -41, -48, -41, -40, -30, -21, -21, -23, -11, -19, -31, -5, -7, -9, -10, -18, -34, -19, -22, -10, -27]
adjustmentrecipes = [[-4, -13, -14, 4, 5], [-4, -6, -8, -11, -3, -12], [-4, -11, -14, -5, 9, 6], [-4, -13, -8, -9, -12, -7], [-4, -13, -13, -11, -16, -4], [-4, -13, -13, -12, 4, -16], [-4, -6, -13, -10, -18, -9], [-4, 4, -10, -13, -4]]
hwss = hwssAdjusted[6]
tail = [-10, -27]

moveRecipes= [[5, 15, -9, 5], [-4, -14, -1, 11, 5, 28], [-4, -13, -4, -8, -5], [6, 7], [5, 15, -17, 13], [-5, -6, -7], [5, -5, 4, 7, 12],[6, 7, -3, 7]]
blockMoves= [[30,-1], [-6, 5], [32, 5], [20, 5], [14, 5], [25,5], [10, 5], [20, 5]]
destruction = [[-11], [0,0], [-30,-20], [-20,-30, -10], [-9], [-39], [-9, -5], [-20]]

cells = []
allRecipes = []

for i in xrange(0, 8):
	salvo.Reset()
	salvo.AppendExternalRecipe(hwss)
	salvo.block0 = [22, 5]
	salvo.AppendExternalRecipe(moveRecipes[i])
	salvo.block0 = blockMoves[i]
	salvo.AppendExternalRecipe(adjustmentrecipes[i])
	salvo.block0 = [0, 0]
	salvo.AppendExternalRecipe(destruction[i])
	salvo.AppendExternalRecipe(tail)
	salvo.PlaceRecipe()
	cells.append(g.getcells(g.getrect()))
	allRecipes.append(salvo.recipe)
	
g.new("")
y = 0

for c in cells:
	g.putcells(c, 0, y)
	y += 1000

g.setclipstr(str(allRecipes))
'''
#g.setclipstr(str(salvo.recipe))

#salvo.GotoAdvanced(-12, 51, -1, 15)
#salvo.PlaceRecipe()
#g.putcells(salvo.init)
#g.setclipstr(str(salvo.recipe))

#salvo.GotoAdvanced(-62, -10, -1)
#salvo.PlaceRecipe()
#g.setclipstr(str(salvo.recipe))

#salvo.ApplyRecipeSmart(54, 9)
#salvo.PlaceRecipe()

#salvo.AppendExternalRecipe([-4, -13, -8, -14, -22, 1])

#salvo.ApplyRecipeSmart(15, 2)
#salvo.Swap()
#salvo.ApplyRecipeSmart(852, -1)

#salvo.ApplySplit(0)
#

'''
for i in xrange(0, 8):
	salvo.AppendExternalRecipe([-4, -6, -13, -5])
	salvo.block0[0] += 6
	salvo.block0[1] += -18

	#salvo.GotoAdvanced(0, -4, -1)
	salvo.ApplyRecipeSmart(3182, -1)

salvo.ApplyRecipeSmart(1, -1)
salvo.ApplyRecipeSmart(1, -1)
salvo.ApplyRecipeSmart(1, -1)
salvo.ApplyRecipeSmart(1, -1)
salvo.ApplyRecipeSmart(1, -1)
salvo.ApplyRecipeSmart(1, -1)


#Hand 
salvo.ApplySplit(0)
salvo.ApplyRecipeSmart(7, 0)
salvo.Swap()
salvo.ApplyRecipeSmart(33, -1)

#salvo.PlaceAt(-13, 20, 0) - irrelevant now
salvo.ApplySplit(0)
salvo.ApplyRecipeSmart(168, -1)
salvo.ApplyRecipeSmart(55, 0)
salvo.Swap()

#salvo.PlaceAt(15, -10, 3)
salvo.ApplySplit(0)
salvo.ApplyRecipeSmart(15543, -1)
salvo.ApplyRecipeSmart(304, 3)
salvo.Swap()

#Hand
salvo.ApplyRecipeSmart(33, -1)
salvo.ApplyRecipeSmart(853, -1)

#salvo.GotoAdvanced(10, -9, 1)
salvo.ApplyRecipeSmart(28059, -1)
salvo.ApplyRecipeSmart(8228, 1)
salvo.AppendExternalRecipe([-8])
'''

#salvo.PlaceRecipe()
#g.show(str(len(salvo.recipe)))
#g.run(50000)

'''
#Hand 
#salvo.ApplyRecipeSmart(33, -1)

#salvo.PlaceAt(7, -45, 1)
salvo.ApplySplit(0)
salvo.ApplyRecipeSmart(2817, -1)
salvo.ApplyRecipeSmart(9498, 1)
salvo.Swap()

#Hand
salvo.ApplyRecipeSmart(33, -1)
salvo.ApplyRecipeSmart(33, -1)

salvo.GotoAdvanced(12,-46,3)

#salvo.ApplyRecipeSmart(364, -1)
#salvo.PlaceAt(13, 16, 0)
#salvo.ApplyRecipeSmart(28, -1)
#salvo.PlaceAt(0, -3, 0)
#salvo.ApplyRecipeByIndex(3721)

#salvo.PlaceActionList(['ApplySplit', 1958, 'Swap', 28, 'ApplySplit', 1087, 2226, 'Swap', 3721, 'ApplySplit', 849, 2236, 'Swap', 34, 34, 'ApplySplit', 5754, 1110, 'Swap'])
#salvo.ApplyRecipeByIndex(34)
#salvo.ApplyRecipeByIndex(34)
#salvo.PlaceAt(5, -6)
salvo.PlaceRecipe()
'''