import golly as g 

glider_cells = g.parse("3o$o$bo!")
#block_cells = g.parse("2o$2o!")
block_cells = g.parse("2o$2o!", 0, 1)

def Read(path):
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
			
		array.append([0, x, y, vals[1]])
		
	ins.close()

	return array
	
def LeftMost(recipe):

	g.new("")
	g.setstep(3)
	
	g.putcells(block_cells)
	
	for r in recipe:
		#g.putcells(glider_cells, 80, 80 + r )
		g.putcells(glider_cells, 80, 80 + 2 - r )
		g.step()
		g.step()
		
	rect = g.getrect()
	
	return rect[0]
	
path = "C:\\Users\\SimSim314\\Documents\\GitHub\\GlueNew\\Glue\\MonochromaticP2\\534725[[0, 0], [1, 0], [0, 1], [1, 1]]"
ar = Read(path + ".txt")

length  = len(ar) 

for i in xrange(length):
	
	if (i + 1) % 100 == 0:
		g.show(str(i) + "/" + str(length) + " : " + str((i * 100 / length)) + "%")
		g.update()
		
	l = LeftMost(ar[i][3])
	ar[i][0] = l

f = open(path + "_Fixed1.txt", "w" )

for i in xrange(length):

		
	f.write(str(ar[i][0]) + ",") 
	f.write(str(ar[i][2]) + ",") 
	f.write(str(ar[i][1] + 1) + ":") 
	
	for r in xrange(len(ar[i][3]) - 1):
		#f.write(str(ar[i][3][r]) + ",") 
		f.write(str(2 - ar[i][3][r]) + ",") 
		
	#f.write(str(ar[i][3][len(ar[i][3]) - 1]) + "\n") 
	f.write(str(2 - ar[i][3][len(ar[i][3]) - 1]) + "\n") 
	
f.close()
