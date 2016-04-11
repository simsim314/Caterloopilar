import golly as g 

s = ":-4,-12,-6,-2,-8,-6,-12,-10,-12,-16,-6,-10,-8" 
s =g.getstring("type recipe")

v = s.split(':')
v1 = v[0].split(',')
v2 = v[1].split(',')

g.new("")
glider_cells = g.parse("3o$o$bo!")
block_cells = g.parse("2o$2o!", 0, 0)
#block_cells = g.parse("$3bo$3bo$3bo5$3o5$7b2o$7b2o8$4bo$4bo10bo$4bo9bobo$14b2o$3o3b3o2$4bo$4bo$4bo!", -20, -20)

def LeftMost(recipe):

	g.putcells(block_cells)
	
	idx = 1
	for r in recipe:
		#g.putcells(glider_cells, 80, 80 + r )
		g.putcells(glider_cells, 160 * idx, 160 * idx + int(r))
		idx += 1
		#g.step()
		
	rect = g.getrect()
	
	return rect[0]
	
LeftMost(v2)