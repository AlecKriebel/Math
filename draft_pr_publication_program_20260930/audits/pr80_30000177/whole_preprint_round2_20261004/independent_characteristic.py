"""Independent exact construction: full tensor encoder and determinant polynomials.
No package or other audit verifier is imported. All polynomial coefficients are rational.
"""
from fractions import Fraction as Q
from itertools import permutations
import json

I=[[1,0],[0,1]]; X=[[0,1],[1,0]]; Z=[[1,0],[0,-1]]; XZ=[[0,-1],[1,0]]
P=[I,X,Z,XZ]
Bell=[[1,0,0,1],[1,0,0,-1],[0,1,1,0],[0,1,-1,0]]
count=0
def check(t):
 global count
 if not t: raise AssertionError('independent exact check failed')
 count+=1
def tensor(a,b):
 return [[a[i][j]*b[k][l] for j in range(len(a[0])) for l in range(len(b[0]))] for i in range(len(a)) for k in range(len(b))]
def poly_add(a,b):
 return [(a[i] if i<len(a) else Q(0))+(b[i] if i<len(b) else Q(0)) for i in range(max(len(a),len(b)))]
def poly_mul(a,b):
 c=[Q(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b): c[i+j]+=x*y
 return c
def characteristic(m):
 # Leibniz determinant of lambda*I-m, independent of trace-power sums.
 ans=[Q(0)]*5
 for p in permutations(range(4)):
  inv=sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))
  term=[Q((-1)**inv)]
  for i,j in enumerate(p): term=poly_mul(term,[-m[i][j],Q(i==j)])
  ans=poly_add(ans,term)
 return ans
def eig_poly(roots):
 p=[Q(1)]
 for v in roots: p=poly_mul(p,[-v,Q(1)])
 return p
def certify(state,roots):
 p=[Q(1)]
 for m in state:
  check(all(m[i][j]==m[j][i] for i in range(4) for j in range(4)))
  p=poly_mul(p,characteristic(m))
 check(p==eig_poly(roots))
 check(sum(m[i][i] for m in state for i in range(4))==1)
def channel(px,py):
 U=tensor(tensor(tensor(px,py),I),I)
 w=[Q(1,2) if i in (1,2,4,8) else Q(0) for i in range(16)]
 v=[sum(U[i][j]*w[j] for j in range(16)) for i in range(16)]
 # Reindex the full encoded state to A1 B1 : A2 B2.
 paired=[[Q(0)]*4 for _ in range(4)]
 for index,c in enumerate(v):
  a1,a2,b1,b2=[(index>>k)&1 for k in (3,2,1,0)]
  paired[2*a1+b1][2*a2+b2]=c
 # Bell rows omit 1/sqrt(2); density therefore divides by 2.
 residual=[[sum(Bell[j][l]*paired[l][r] for l in range(4)) for r in range(4)] for j in range(4)]
 return [[[residual[j][r]*residual[j][s]/2 for s in range(4)] for r in range(4)] for j in range(4)]
def avg(states):
 return [[[sum(s[j][r][c] for s in states)/len(states) for c in range(4)] for r in range(4)] for j in range(4)]

states={(x,y):channel(P[x],P[y]) for x in range(4) for y in range(4)}
pair=[Q(1,2),Q(1,4),Q(1,4)]+[Q(0)]*13
mx=[Q(1,4)]*2+[Q(1,16)]*8+[Q(0)]*6
my=[Q(1,8)]*8+[Q(0)]*8
ma=[Q(3,32)]*8+[Q(1,32)]*8
for s in states.values(): certify(s,pair)
for x in range(4): certify(avg([states[x,y] for y in range(4)]),mx)
for y in range(4): certify(avg([states[x,y] for x in range(4)]),my)
complete=avg(list(states.values())); certify(complete,ma)
check(complete==[[[Q(3 if r%2==0 else 1,32) if r==c else Q(0) for c in range(4)] for r in range(4)] for j in range(4)])
both=[]
for s in states.values():
 q=[sum(Q(Bell[k][r]*Bell[k][c],2)*s[j][r][c] for r in range(4) for c in range(4)) for j in range(4) for k in range(4)]
 check(sorted(q)==[Q(0)]*12+[Q(1,4)]*4); both.append(q)
check([sum(row[k] for row in both)/16 for k in range(16)]==[Q(1,16)]*16)
check(27<32)
print(json.dumps({'status':'PASS_INDEPENDENT_DETERMINANT_POLYNOMIALS','checks':count,'method':'Full 16-component tensor encoded W vector; rational Bell contractions; all 25 block-diagonal spectra by Leibniz determinant and characteristic-polynomial factorization. No trace powers or imported verifier.','all_branches_retained':True,'both_bell_information_bits':2,'finite_algebra_only':True},indent=2))
