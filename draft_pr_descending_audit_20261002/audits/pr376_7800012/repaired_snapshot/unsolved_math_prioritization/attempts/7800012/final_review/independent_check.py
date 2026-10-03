import itertools,collections,json
from fractions import Fraction as Q
import sympy as S
N=0
def ck(v):
 global N
 assert v;N+=1
# Independently count closed walks by signed shoelace area, without the author's winding code.
c=collections.Counter()
steps=[(1,0),(-1,0),(0,1),(0,-1)]
for word in itertools.product(steps,repeat=6):
 x=y=area=0
 for dx,dy in word:
  xx,yy=x+dx,y+dy;area+=x*yy-xx*y;x,y=xx,yy
 if (x,y)==(0,0):c[abs(area)//2]+=1
ck(c=={0:232,1:144,2:24})
# Formal Harper determinant, keeping the closing variable rather than fixing a twist.
z,A,B,w=S.symbols('z A B w',nonzero=True)
H=S.Matrix([[A,1,0,1/w],[1,B,1,0],[0,1,-A,1],[w,0,1,-B]])
ck(S.expand((z*S.eye(4)-H).det()- (z**4-(A*A+B*B+4)*z*z+A*A*B*B+2-w-1/w))==0)
# Independently construct the full 4x4 torus and its exact characteristic polynomial.
L=4;T=S.zeros(16)
for y in range(L):
 for x in range(L):
  i=x+L*y
  for j,v in [(((x+1)%L)+L*y,S.Integer(1)),(x+L*((y+1)%L),S.I**x)]:T[i,j]=v;T[j,i]=S.conjugate(v)
ck((T**3-8*T).applyfunc(S.simplify)==S.zeros(16));ck(S.Poly(T.charpoly().as_expr()).all_coeffs()==S.Poly(z**8*(z*z-8)**4,z).all_coeffs())
# Spectral projection formulas tested independently at all four exact eigenvalues.
r=S.sqrt(3);ev=[-1-r,1-r,-1+r,1+r]
coeff=[[12-8*r,18-10*r,2*r,r-3],[12+8*r,-18-10*r,-2*r,3+r],[12+8*r,18+10*r,-2*r,-3-r],[12-8*r,-18+10*r,2*r,3-r]]
for i,a in enumerate(coeff):
 for j,e in enumerate(ev):ck(S.simplify(sum(a[k]*e**k for k in range(4))/48)==int(i==j))
ck(S.simplify((7*r-9)/144)>0)
# Exact SOS identity on several torus cosine/sine assignments from rational points on the circle.
points=[(Q(1),Q(0)),(Q(3,5),Q(4,5)),(Q(-5,13),Q(12,13)),(Q(-1),Q(0))]
for L in [4,6,8]:
 for shift in range(4):
  vals={(x,y):points[(x+2*y+shift)%4] for x in range(L) for y in range(L)};n=L*L;tot=sum(t[0] for t in vals.values());pairs=[]
  for x,y in vals:pairs.extend([((x,y),((x+1)%L,y)),((x,y),(x,(y+1)%L))])
  defect=40*n+16*tot+12*sum(vals[a][0]*vals[b][0]-vals[a][1]*vals[b][1] for a,b in pairs)
  sos=Q(48,n)*(tot+Q(n,6))**2+6*sum((vals[a][0]+vals[b][0]-Q(2,n)*tot)**2+(vals[a][1]-vals[b][1])**2 for a,b in pairs)
  ck(defect-Q(44*n,3)==sos)
# Budget and boundary identities used in canonical tiling, including incomplete cores.
for L in range(4,62,2):
 for l in range(4,L+1,2):
  k=L//l;rem=L*L-k*k*l*l
  ck(rem%4==0);ck(k*k*(l*l//4)+rem//4==L*L//4)
  if L%l==0:ck(2*(L//l)*L==2*L*L//l)
print(json.dumps({'status':'PASS','independent_assertions':N,'scope':'Independent closed-walk areas, formal Harper determinant, exact 4x4 characteristic polynomial, spectral projectors, SOS identities and canonical particle budgets. Full Hessian certificate and analytic implications audited separately.'},indent=2))
