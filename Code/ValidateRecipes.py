import golly as g 

glider_cells = g.parse("3o$o$bo!")
#block_cells = g.parse("2o$2o!")
block_cells = g.parse("2o$2o!", 0, 1)
lines = [] 

def Read(path):
	ins = open(path, "r" )
	array = []

	for line in ins:
		vals = line.split(":")
		lines.append(line)
		
		vals[0] = vals[0].replace("m", "")
		vals[0] = vals[0].split(",")
		x = int(vals[0][1])
		y = int(vals[0][2])
		vals[1] = vals[1].replace("E", "").replace("\n", "").replace(" ", "")
		vals[1] = vals[1].split(",")
		
		for i in xrange(0, len(vals[1])):
			vals[1][i] = int(vals[1][i])
			
		array.append([x, y, vals[1]])
		
	ins.close()

	return array
	
def Validate(recipe):

	g.new("")
	g.setstep(3)
	
	g.putcells(block_cells)
	
	for r in recipe:
		g.putcells(glider_cells, 120, 120 + r)
		#g.putcells(glider_cells, 80, 80 + 2 - r )
		g.step()
		g.step()
		
	rect = g.getrect()
	
	return rect
	
path = "C:\\Users\\SimSim314\\Documents\\GitHub\\GlueNew\\Glue\\MonochromaticP2\\534725[[0, 0], [1, 0], [0, 1], [1, 1]]_Fixed1.txt"
ar = Read(path)

length  = len(ar) 

validatedLines = []
invalids = 0

for i in xrange(length):
	
	if (i + 1) % 100 == 0:
		g.show(str(i) + "/" + str(length) + " : " + str((i * 100 / length)) + "%" + " , " + str(invalids))
		g.update()
		
	l = Validate(ar[i][2])
	
	if len(l) == 0:
		invalids += 1
		continue 
	elif not (l[0] == ar[i][0] and l[1] == ar[i][1] and l[2] == 2 and l[3] == 2):
		invalids += 1
		continue 
	
	validatedLines.append(lines[i])

filepath = "C:\\Users\\SimSim314\\Documents\\GitHub\\GlueNew\\Glue\\MonochromaticP2\\534725[[0, 0], [1, 0], [0, 1], [1, 1]]_ValidatedOdd.txt"

with open(filepath, 'w') as file:
	file.writelines(validatedLines)
