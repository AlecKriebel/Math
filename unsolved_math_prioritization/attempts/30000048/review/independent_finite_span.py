"""Independent exact re-enumeration of the frozen turn-2 character span."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
points=[(F(j,10)**2,2*F(j,10)**3) for j in range(-10,31)]
survivors=[];excluded=0
for A,B,C in product(range(-8,9),range(-10,11),range(-27,28)):
 if any((1-A+2*B)+(A-4*B)*x+C*x*x+(B-C)*y<0 for x,y in points):excluded+=1
 else:survivors.append([A,B,C])
assert survivors==[[0,0,0],[1,0,0],[1,0,1],[2,1,1]]
out={'status':'PASS','independently_reenumerated_triples':19635,'excluded':excluded,'survivors':survivors,'points':'real traces t=j/10, -10<=j<=30, all realized by diag(1,e^itheta,e^-itheta)'}
print(json.dumps(out,indent=2));Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
