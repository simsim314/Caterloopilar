import golly as g 
from WSSStapler import *

hwssRecipe = [-4, -14, -8, 20, 22, 24, 32, 12, 24, 30, 48, 48, 38, 44, 72, 74, 76, 84, 64, 76, 82, 100, 100, 90, 96, 124, 126, 128, 136, 116, 128, 134, 152, 152, 158, 158, 148, 146, 148, 140, 140, 136, 150, 158, 146, 148, 160, 150, 140, 146, 164, 164, 162, 162, 168, 162, 156, 170, 154, 164, 172, 166, 170, 178, 174, 176, 162, 160, 162, 176, 166, 168, 180, 174, 170, 152, 156, 160, 168, 186, 160, 160, 158, 150, 170, 176, 162, 182, 180, 172, 192, 198, 184, 214, 214, 214, 218, 220, 218, 220, 228, 238, 240, 230, 236, 254, 254, 260, 258, 250, 252, 250, 256, 254, 266, 274, 268, 258, 260, 272, 256, 240, 256]
hwssRecipe.insert(63,'SKIP')
hwssRecipe.insert(63,'SKIP')
hwssRecipe.insert(97,'SKIP')
hwssRecipe.insert(97,'SKIP')

step = 250
period = 2000
directionType = "B"

distBack = period / 2 + step
distForward = period / 2 - step

g.new("")

if directionType == "B":
	for y in xrange(-3 * len(hwssRecipe), 1):
		MakeBackwardSalvo(step, 0, distBack * y, step * len(hwssRecipe) + 100, y == 0, y == 0)
	
	MakeBackwardRecipe(step, 0, 0, hwssRecipe)
	
else:
	for y in xrange(0, 3 * len(hwssRecipe) + 1):
	   MakeForwardSalvo(step, distForward * y, y == 0, y == 0)
	
	MakeForwardRecipe(step, 0, 0, hwssRecipe)
	
g.fit()


