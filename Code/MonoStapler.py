import golly as g 
import copy

glider_cells = g.parse("3o$o$bo!")
block_cells = g.parse("2o$2o!")

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
		
		g.putcells(block_cells)
		g.putcells(self.init)
		
		for r in self.recipe:
			g.putcells(glider_cells, 80, 80 + r)
			g.step()
		
		g.select([self.block0[0], self.block0[1], 2, 2])
		g.clear(0)
		cells = g.getcells(g.getrect())
		g.putcells(block_cells, self.block0[0], self.block0[1])
		delta = self.block0[1] - self.block0[0]
		
		for r in recipe:
			g.putcells(glider_cells, 80, 80 + r + delta)
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
			return self.Goto(x, y, self.moveTable, block_cells, maxL)
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
			
			#TODO autofix odd recipes instead of ignoring them 
			if (y1 - x1) % 2 != 0:
				continue 
				
			if (str(x1) + "," + str(y1)) in worked:
				continue
				
			g.show(str(x) + "," + str(y) + "," + str(i) + "/" + str( len(self.moveTable )) + " BESTi = {0}, BESTL {1}".format(besti, bestL))
			g.update()
		
			self.block0[0] = xtemp0
			self.block0[1] = ytemp0
			self.recipe = copy.copy(tempRecipe0)
			
			if self.CanApplyRecipe(self.moveTable[i][2], g.transform(block_cells, x1, y1)):
			
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
			
			g.show(str([besti, self.lastGotoIdx]))
			
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
			
		g.show(str(self.recipe))
		g.setclipstr(str(self.recipe))
		g.putcells(block_cells, x, y)
		i = 0 
		for r in self.recipe:
			g.putcells(glider_cells, x + 80 + i * 128, y + 80 + i * 128 + r)
			i += 1

	def LoadMoveTable(self, path, report):
		ins = open(path, "r" )
		array = []
		
		bestdxrecipe = [0]
		bestdy = 1
		bestdx = 0
		idx = 0
		
		for line in ins:
			vals = line.split(":")
			
			vals[0] = vals[0].replace("m", "")
			vals[0] = vals[0].split(",")
			x = int(vals[0][0])
			y = int(vals[0][1])
			vals[1] = vals[1].replace("E", "").replace("\n", "").replace(" ", "")
			vals[1] = vals[1].split(",")
			
			for i in xrange(0, len(vals[1])):
				vals[1][i] = int(vals[1][i])
			
			if x >= 0 and y / len(vals[1]) > bestdy / len(bestdxrecipe):
				bestdxrecipe = vals[1]
				bestdx = x
				bestdy = y
				idx = len(array)
				
			array.append([x, y, vals[1]])
			
		if report:
			g.show(str([idx, bestdx, bestdy]))
			#g.setclipstr(str(bestdxrecipe))
			
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
	
	def MonochromaticFix(self):
		dy = self.block0[1] - self.block0[0]
		
		if dy % 2 == 0:
			return
		
		self.recipe.append(dy - 5)
		self.block0[0] += 2
		self.block0[1] += 1
		
	def FindIndexByDx(self, dx):
		for i in xrange(0, len(self.moveTable )):
			if dx == self.moveTable[i][0] and (self.moveTable[i][0] - self.moveTable[i][1]) % 2 == 0:
				return (i, self.moveTable[i][1]) 
		
		return -1
			
	def FindIndexByDxy(self, dx, dy):
		for i in xrange(0, len(self.moveTable )):
			if dx == self.moveTable[i][0] and dy == self.moveTable[i][1] and (self.moveTable[i][0] - self.moveTable[i][1]) % 2 == 0:
				return i
		
		return -1	
		
