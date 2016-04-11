import golly as g 

'''
hwssRecipe = [-4,2,2,-8,-10,-8,-16,-16,-20,-6,2,-10,-8,4]
step = 200
period = 1600
directionType = "B"

distBack = period / 2 + step
distForward = period / 2 - step
'''

def MakeBackwardSalvo(distance, dx, dy, helixSLdy, toPlaceHelixSL = False, toPlaceFirstSL = False):
   
   backHelixSL = g.parse("bo$obo$obo$bo!", 201, 1083)
   backHelixSL2GliderWSS = g.parse("bobo$o$o3bo$o$o2bo$3o!", 196, 1076)
   backHelixReflect = g.parse("b2o$b3o$ob2o$3o$bo16$2bobo$bo$bo3bo$bo$bo2bo$b3o!", 131, 853)
   backHelixGlider2SL = g.parse("bobo$4bo$o3bo$4bo$bo2bo$2b3o!", 200, 635)

   backErasingReflectorWSS = g.parse("bobo$o$o3bo$o$o2bo$3o73$23bobo$26bo$22bo3bo$26bo$23bo2bo$24b3o69$42bobo$45bo$41bo3bo$45bo$42bo2bo$43b3o!", 63, 641)
   backSL = g.parse("b2o$o2bo$obo$bo!", 6, 629)
   backFrontPart = g.parse("bobo$o$o$o2bo$3o42$65bobo$64bo$64bo3bo$64bo$64bo2bo$64b3o23$59bobo$58bo$58bo$58bo2bo$58b3o35$51b2o$51b3o$50bob2o$50b3o$51bo6$31bobo$30bo$30bo3bo$30bo$30bo2bo$30b3o10$24b2o$24b3o$23bob2o$23b3o$24bo64$43b2o$42b3o$42b3o$42b2obo$43b3o$44bo10$52b2o$51b3o$51b3o$51b2obo$52b3o$53bo!", -30, 387)
   backReflectingPart = g.parse("36bobo$39bo$39bo$36bo2bo$37b3o11$b2o$3o$2obo$b3o$2bo14$9bobo$12bo$12bo$9bo2bo$10b3o!", 67, 257)
   backBackPart = g.parse("b2o$3o$2obo$b3o$2bo!", 2, 0)
   
   d = (distance - 144) / 2
   
   if toPlaceHelixSL:
	g.putcells(backHelixSL, d + dx, d * 3 + dy + helixSLdy)
   
   g.putcells(backHelixSL2GliderWSS, d + dx, d * 3 + dy)
   g.putcells(backHelixReflect, dx, dy)
   g.putcells(backHelixGlider2SL, d + dx, -d * 3 + dy)
   g.putcells(backErasingReflectorWSS,dx, dy)
   g.putcells(backFrontPart, -d + dx, -d + dy)
   g.putcells(backReflectingPart, 0 + dx, -4 * d + dy)
   g.putcells(backBackPart, -d + dx, -d * 7 + dy)
   
   if toPlaceFirstSL:
	g.putcells(backSL, -d + dx, -d + dy)
   
def MakeBackwardRecipe(distance, dx, dy, recipe): 
   d = (distance - 144) / 2
   backSL = g.parse("b2o$o2bo$obo$bo!", 6 - d + dx, 629 - d + dy)
   curd = distance + 2
   
   recipe.insert(0, -4)
   
   for r in recipe: 
   	  if r != 'SKIP':	
		g.putcells(backSL, 0, curd - r)

   	  curd += distance

def MakeForwardSalvo(distance, dx, dy, helixSLdy, toPlaceHelixSL = False, toPlaceFirstSL = False):

   frontHelixSL = g.parse("6bo$5bobo$5bobo$6bo2$b2o7b2o$o2bo5bo2bo$b2o7b2o2$6bo$5bobo$5bobo$6bo!", 0, 0)
   frontHelixSL2GliderWSS = g.parse("2b3o$bo2bo$4bo$o3bo$4bo$bobo!", 7, 16)
   frontHelixReflect = g.parse("8b3o$7bo2bo$10bo$10bo$7bobo2$3o$o2bo$o$o3bo$o$bobo!", 54, 71)
   frontHelixGlider2SL = g.parse("bo$3o$ob2o$b3o$b3o$b2o!", 5, 123)

   frontErasingReflectorWSS = g.parse("28bo$27b3o$26b2obo$26b3o$27b2o23$5bo$4b3o$3b2obo$3b3o$4b2o5$2bo$b3o$2obo$3o$b2o!", 68, 172)
   frontSL = g.parse("bo$obo$o2bo$b2o!", 132, 314)
   frontFrontPart = g.parse("2b3o$2bo2bo$2bo$2bo3bo$2bo$3bobo24$20bo$19b3o$19bob2o$20b3o$20b3o$20b2o35$4b3o$3bo2bo$6bo$2bo3bo$6bo$3bobo8$22b3o$22bo2bo$22bo$22bo$23bobo17$29bo$28b3o$28bob2o$29b3o$29b2o6$bo$3o$ob2o$b3o$b2o!", 122, 287)
   frontReflectingPart = g.parse("2bo$b3o$2obo$3o$3o$b2o2$12b3o$12bo2bo$12bo$12bo3bo$12bo$13bobo12$17b3o$16bo2bo$19bo$15bo3bo$19bo$16bobo!", 80, 464)
   frontBackPart = g.parse("11b3o$11bo2bo$11bo$11bo3bo$11bo$12bobo4$3o$o2bo$o$o3bo$o3bo$o$bobo!", 132, 556)
  
   d = (distance - 98) / 2
   
   if toPlaceHelixSL:
	g.putcells(frontHelixSL, -d + dx, -d + dy + helixSLdy)
   
   g.putcells(frontHelixSL2GliderWSS, -d + dx, -d + dy)
   g.putcells(frontHelixReflect, dx, dy)
   g.putcells(frontHelixGlider2SL, -d + dx, d + dy)
   g.putcells(frontErasingReflectorWSS, dx, dy)

   g.putcells(frontFrontPart, d + dx, d + dy)
   g.putcells(frontReflectingPart, 0 + dx, 2 * d + dy)
   g.putcells(frontBackPart, d + dx, 3 * d + dy)
   
   if toPlaceFirstSL:
	g.putcells(frontSL, d + dx, d + dy + helixSLdy)
   
def MakeForwardRecipe(helixSLdy, distance, dx, dy, recipe): 
	d = (distance - 98) / 2

	frontSL = g.parse("bo$obo$o2bo$b2o!", 132 + d + dx, 314 + d + dy)
	curd = helixSLdy + distance

	for r in recipe: 
	  if r != 'SKIP':	
		g.putcells(frontSL, 0, curd + r)

	  curd += distance
'''  
if directionType == "B":
	for y in xrange(-3 * len(hwssRecipe), 1):
	  MakeBackwardSalvo(step, 0, distBack * y, step * len(hwssRecipe) + 100, y == 0, y == 0)

	MakeBackwardRecipe(step, 0, 0, hwssRecipe)

else:
   for y in xrange(0, 3 * len(hwssRecipe) + 1):
      MakeForwardSalvo(step, distForward * y, y == 0, y == 0)
   
   MakeForwardRecipe(step, 0, 0, hwssRecipe)
   
g.fit()
'''