import golly as g 
import copy
from os import path

glider_cells = g.parse("3o$o$bo!")
block_cells = g.parse("2o$2o!")

class RecipeConstructor(object):
	
	def __init__(self):
		self.blockX = 0
		self.blockY = 0
		self.sequence = []
		self.recipe = []
		self.BlockMoveTableEven = {}
		self.BlockMoveTableOdd = {}
		self.WssCreator = []
		self.minD = 0
		self.maxY = 0
		self.maxX = 0
		
	def Reset(self):
		self.blockX = 0
		self.blockY = 0
		self.sequence = []
		self.recipe = []
		
	def AddWss(self, idx):
		delta = self.blockY - self.blockX
		dx = self.WssCreator[idx][0]
		dy = self.WssCreator[idx][1]
		rec = self.WssCreator[idx][2]
		
		for i in rec:
			self.recipe.append(i + delta)
		
		self.sequence.append((idx))
		self.blockX += dx
		self.blockY += dy
		
	def Goto(self, x, y):
		
		dx = x - self.blockX
		dy = y - self.blockY
		
		#g.note(str((x, y,  self.blockX,  self.blockY, dx, dy)))
		
		if dx >= self.minD and dx <= self.maxX and abs(dy) <= self.maxY:
			
			d = min(-3, dx)
			self.MoveBy(d, dx, dy)
			
		else: 
			
			if dy != 0:
				dx_dy = int(self.maxY * float(dx) / float(abs(dy)) + 0.5)
			else:
				dx_dy = 0 
				
			if dy != 0 and abs(dy) > self.maxY and dx_dy <= self.maxX and dx_dy >= self.minD:
			
				d = min(-3, dx_dy)
				self.MoveBy(d, dx_dy, self.maxY * (dy / abs(dy)))
				self.Goto(x, y)
				
			elif dx < self.minD:
				
				dy_dx = int(self.minD * float(dy) / float(dx) + 0.5)
				self.MoveBy(self.minD, self.minD, dy_dx)
				self.Goto(x, y)
			
			elif dx > self.maxX:
				
				dy_dx = int(self.maxX * float(dy) / float(dx) + 0.5)
				self.MoveBy(-3, self.maxX, dy_dx)
				self.Goto(x, y)
			'''
		if dx < -26:
			if dy >= 101:
				self.MoveBy(-23, -23, 101)
				self.Goto(x, y)
			elif dy <= -101:
				self.MoveBy(-23, -23, -101)
				self.Goto(x, y)
			elif abs(dy) >= abs(dx):
			
				if dy < 0:
					self.MoveBy(-23, -23, -23)
				else:
					self.MoveBy(-23, -23, 23)
					
				self.Goto(x, y)
			else:
				self.MoveBy(-23, -23, 1)
				self.Goto(x, y)
			
		elif dx < -23:
			if dy >= 101:
				self.MoveBy(-11, -11, 101)
				self.Goto(x, y)
			elif dy <= -101:
				self.MoveBy(-11, -11, -101)
				self.Goto(x, y)
			else: 
				self.MoveBy(-11, -11, 1)
				self.Goto(x, y)
		
		elif dx <= 50:
			
			d = dx
			delta = 0 
			
			if d > -3:
				d = -3
			
			if d < -3:
				delta = d
				
			if dy >= 100:
				self.MoveBy(d, delta, 100 + delta)
				self.Goto(x, y)
			elif dy <= -100:
				self.MoveBy(d, delta, -100 - delta)
				self.Goto(x, y)
			else: 
				self.MoveBy(d, dx, dy)
				
		else:
			
			if dy >= 100:
				self.MoveBy(-3, 50, 100)
				self.Goto(x, y)
			elif dy <= -100:
				self.MoveBy(-3, 50, -100)
				self.Goto(x, y)
			else: 
				self.MoveBy(-3, 50, 0)
				self.Goto(x, y)
	'''
	def DeleteBlock(self):
		delta = self.blockY - self.blockX
		
		if delta % 2 == 1:
			delta -= 1
			
		self.recipe.append(delta)

	def MoveBy(self, d, dx, dy):
	
		delta = self.blockY - self.blockX
		isEven = True
		
		if (self.blockY + self.blockX) % 2 == 1:
			delta -= 1
			isEven = False
			
		if isEven:
			rec = self.BlockMoveTableEven[(d, dx, dy)]
		else:
			rec = self.BlockMoveTableOdd[(d, dx, dy + 1)]
		
		for i in rec:
			self.recipe.append(i + delta)
		
		self.blockX += dx
		self.blockY += dy
		self.sequence.append((d, dx, dy))
		
	def Init(self, pathEven, pathOdd, pathWss):
		
		self.LoadMoveTable(pathEven, True)
		self.LoadMoveTable(pathOdd, False)
		self.LoadWssTable(pathWss)

	def LoadMoveTable(self, path, isEven):
		ins = open(path, "r" )
		array = []
		
		for line in ins:
			vals = line.split(":")
			
			vals[0] = vals[0].replace("m", "")
			vals[0] = vals[0].split(",")
			
			d = int(vals[0][0])
			x = int(vals[0][1])
			y = int(vals[0][2])
			
			self.minD = min(self.minD, d)
			self.maxY = max(self.maxY, abs(y))
			self.maxX = max(self.maxX, x)
			
			
			vals[1] = vals[1].replace("E", "").replace("\n", "").replace(" ", "")
			vals[1] = vals[1].split(",")
			
			if vals[1][0] != 'X' and vals[1][0] != '':
				for i in xrange(0, len(vals[1])):
					vals[1][i] = int(vals[1][i])
			
			if isEven:
				self.BlockMoveTableEven[(d, x, y)] = vals[1]
			else:
				self.BlockMoveTableOdd[(d, x, y)] = vals[1]
			
		ins.close()
		self.maxY -= 2
		self.maxX -= 1
		
	def LoadWssTable(self, path):
		ins = open(path, "r" )
		array = []
		
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
		
			self.WssCreator.append([x, y, vals[1]])	
			
		ins.close()
		
def FindBestDx(recipes):

	bestX = -1
	bestY = -1
	bestRation = -10000
	for x in xrange(-24, -4):
		for y in xrange(-50, 51):
			val = recipes.BlockMoveTableEven[(-23, x, y)]
			if  val[0] == 'X' or val[0] == '':
				continue
			
			if -x / len(val) > bestRation:
				bestRation = -x / len(val)
				bestX = x
				bestY = y

	g.show(str((bestX, bestY)))
	


