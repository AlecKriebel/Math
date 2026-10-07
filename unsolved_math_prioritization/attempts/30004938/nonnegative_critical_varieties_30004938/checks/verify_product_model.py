from pathlib import Path
BASE = Path(__file__).resolve().parent
import itertools,json,math
from fractions import Fraction as Q

def H(a,b):
 A,B,C=a;D,E,F=b
 return (0,B*E,B*D,A*E,A*D,A*F,C*E,C*D,C*F,0)
def inverse(v):
 _,BE,BD,AE,AD,AF,CE,CD,CF,_=v
 den=AD+AE+CD+CE
 assert den>0
 L=2/(1+(BD+BE)/den); R=2/(1+(AF+CF)/den)
 return ((L*(AD+AE)/den,L*(BD+BE)/den,L*(CD+CE)/den),
         (R*(AD+CD)/den,R*(AE+CE)/den,R*(AF+CF)/den))
T=[(Q(a,4),Q(b,4),Q(c,4)) for a,b,c in itertools.product(range(5),repeat=3) if a+b+c==8]
count=0
for a,b in itertools.product(T,repeat=2):
 v=H(a,b);assert inverse(v)==(a,b)
 # Scaling invariance of the inverse is checked with a non-unit rational factor.
 assert inverse(tuple(Q(7,3)*x for x in v))==(a,b)
 count+=1
limits=[]
for scale in [1,2]:
 values=[]
 for t in [1e-2,1e-3,1e-4]:
  A,B,C=math.sin(scale*t),math.sin(t),math.sin((scale+1)*t)
  D=E=F=math.sqrt(3)/2
  v=H((A,B,C),(D,E,F));values.append(v[3]/v[1])
 limits.append({'scale':scale,'Delta134_over_Delta124':values})
assert abs(limits[0]['Delta134_over_Delta124'][-1]-1)<1e-9
assert abs(limits[1]['Delta134_over_Delta124'][-1]-2)<1e-7
out={'rational_triangle_grid_size':len(T),'pairs_checked':count,'inverse_and_projective_scaling':'PASS','distinct_boundary_limits':limits,'status':'PASS'}
print(json.dumps(out,indent=2));open(BASE / 'product_model_verification.json','w').write(json.dumps(out,indent=2))
