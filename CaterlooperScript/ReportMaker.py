import golly as g 
from fractions import Fraction
import glob

#Fraction(100, 10000)

result = [] 

files = glob.glob('*.rle')
for r in files:
	r1 = r.split('_')
	f = Fraction(int(r1[0]), int(r1[1]))
	result.append((f.denominator, f.numerator, f.denominator))

result.sort()

g.show(str(result))
g.exit("")
minpop = 1000000000000000000
maxpop = -10000 
period = 2100
for i in xrange(period):
	
	pop = int(g.getpop())
	
	minpop = min(minpop, pop)
	maxpop = max(maxpop, pop)
	g.run(1)

g.show(str((minpop, maxpop)))