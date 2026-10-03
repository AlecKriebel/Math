from fractions import Fraction as Q
from pathlib import Path
import itertools,json,runpy,contextlib,io
with contextlib.redirect_stdout(io.StringIO()):
 old=runpy.run_path(str(Path(__file__).with_name('independent_controls.py')))
PL=old['PL'];E=old['IDENTITY'];a=old['a'];t=old['t'];conjugate=old['conjugate']
counts={};n=0
def ck(b):
 global n
 assert b;n+=1
def finish(k):
 global n
 counts[k]=n;n=0
# Independent matrix realization of the exact nilpotent presentation.
IE=((Q(1),Q(0),Q(0)),(Q(0),Q(1),Q(0)),(Q(0),Q(0),Q(1)))
def mm(A,B):return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(3)) for j in range(3)) for i in range(3))
def mi(A):return ((Q(1),-A[0][1],A[0][1]*A[1][2]-A[0][2]),(Q(0),Q(1),-A[1][2]),(Q(0),Q(0),Q(1)))
def mp(A,k):
 B=IE;g=A if k>=0 else mi(A)
 for _ in range(abs(k)):B=mm(B,g)
 return B
def comm(A,B):return mm(mm(mm(A,B),mi(A)),mi(B))
def matrix(a,b,c,m):return ((Q(1),Q(a),Q(c,m)),(Q(0),Q(1),Q(b)),(Q(0),Q(0),Q(1)))
def coords(A,m):return (A[0][1],A[1][2],m*A[0][2])
pts=list(itertools.product(range(-2,3),repeat=3))
for m in (2,5,9):
 X,Y,Z=matrix(1,0,0,m),matrix(0,1,0,m),matrix(0,0,1,m)
 ck(comm(X,Y)==mp(Z,m));ck(comm(X,Z)==IE);ck(comm(Y,Z)==IE)
 for u in pts:
  A=matrix(*u,m);ck(mm(A,mi(A))==IE)
  aa,bb,cc=u
  ck(mm(mm(mp(X,aa),mp(Y,bb)),mp(Z,cc-m*aa*bb))==A)
  for k in range(-5,6):ck(coords(mp(A,k),m)==(k*aa,k*bb,k*cc+m*k*(k-1)*aa*bb//2))
  for v in pts[::7]:
   B=matrix(*v,m);C=comm(A,B)
   ck(coords(C,m)==(0,0,m*(u[0]*v[1]-v[0]*u[1])))
   ck(comm(C,X)==IE);ck(comm(C,Y)==IE)
   ck((coords(mm(mm(mi(B),A),B),m)>(0,0,0))==(u>(0,0,0)))
   if u>(0,0,0) and v>(0,0,0):ck(coords(mm(A,B),m)>(0,0,0))
 for k in (-5,-1,1,4):ck(len({mp(matrix(*u,m),k) for u in pts})==len(pts))
finish('rational_matrix_nilpotent_signed_powers_order_normalforms')
# Nondyadic support endpoints in genuine F, with correct crossing extraction.
g=PL([(0,0),(Q(1,8),Q(1,16)),(Q(5,16),Q(1,4)),(Q(3,8),Q(1,2)),(Q(5,8),Q(5,8)),(1,1)])
def supports(f):
 cuts=set(x for x,y in f.p)
 for (x,y),(xx,yy) in zip(f.p,f.p[1:]):
  s=(yy-y)/(xx-x)
  if s!=1:
   root=(s*x-y)/(s-1)
   if x<root<xx:cuts.add(root)
 cuts=sorted(cuts);out=[]
 for x,xx in zip(cuts,cuts[1:]):
  if f.at((x+xx)/2)!=(x+xx)/2:
   if out and out[-1][1]==x and f.at(x)!=x:out[-1]=(out[-1][0],xx)
   else:out.append((x,xx))
 return out
def right_slope(f,x):
 for (u,v),(uu,vv) in zip(f.p,f.p[1:]):
  if u<=x<uu:return (vv-v)/(uu-u)
 raise ValueError(x)
ck(g.isF());ck(g.at(Q(1,3))==Q(1,3));ck(supports(g)==[(Q(0),Q(1,3)),(Q(1,3),Q(5,8))]);ck(right_slope(g,Q(1,3))==4)
for i,j in itertools.product(range(-8,9),repeat=2):
 u,v=g.power(i),g.power(j)
 ck((u@v).at(Q(1,3))==Q(1,3));ck(right_slope(u@v,Q(1,3))==right_slope(u,Q(1,3))*right_slope(v,Q(1,3)))
 for k in (-3,-1,1,3):ck(u.power(k)==g.power(i*k))
 # positive roots of this multibump cyclic control are unique
 ck((u.power(3)==v.power(3))==(u==v))
# Ordinary cyclic N=<a> is not normal in W: its support is translated, so its endpoints are not ambient fixed points.
ck(t.at(Q(1,2))!=Q(1,2));ck(supports(conjugate(a,t))!=supports(a))
for p,q in itertools.product(range(-7,8),repeat=2):
 if p and q:ck((Q(4)**p==Q(4)**q)==(p==q))
finish('actual_F_nondyadic_germs_multibump_roots_normality_boundary')
# Infinite, nonabelian SL(2,Z) lamps: exact matrix conjugation changes entries but never their nonidentity support.
I=(1,0,0,1)
def m2(A,B):a,b,c,d=A;e,f,g,h=B;return (a*e+b*g,a*f+b*h,c*e+d*g,c*f+d*h)
def i2(A):a,b,c,d=A;ck(a*d-b*c==1);return (d,-b,-c,a)
L=[I,(1,1,0,1),(1,0,1,1),(2,1,1,1),(1,-2,0,1),(1,0,-3,1)]
def clean(b):return {i:v for i,v in b.items() if v!=I}
def bm(b,c):return clean({i:m2(b.get(i,I),c.get(i,I)) for i in b.keys()|c.keys()})
def shift(b,k):return {i+k:v for i,v in b.items()}
def wm(x,y):b,k=x;c,l=y;return bm(b,shift(c,k)),k+l
def wi(x):b,k=x;return shift({i:i2(v) for i,v in b.items()},-k),-k
B=[clean(dict(zip((-5,0,11),v))) for v in itertools.product(L,repeat=3)]
changed=False
for b in B:
 for c in B[::31]:
  for k in (-11,-2,3,13):
   x=(b,0);s=(c,k);con=wm(wm(wi(s),x),s)
   ck(set(con[0])=={i-k for i in b});ck(con[1]==0);ck(wm(s,wi(s))==({},0))
   changed |= con[0]!=shift(b,-k)
ck(changed);finish('infinite_nonabelian_matrix_lamp_support_transport')
# Dropping simplicity falsifies the self-normalizer lemma: parity fiber in S3^2 is proper and normal.
S=list(itertools.permutations(range(3)));e=(0,1,2)
def pm(p,q):return tuple(p[q[i]] for i in range(3))
def pi(p):return tuple(p.index(i) for i in range(3))
def parity(p):return sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))%2
D={(p,q) for p,q in itertools.product(S,repeat=2) if parity(p)==parity(q)}
ck(len(D)==18);ck({p for p,q in D}==set(S));ck({q for p,q in D}==set(S))
for a,b in itertools.product(S,repeat=2):
 ck({(pm(pm(a,p),pi(a)),pm(pm(b,q),pi(b))) for p,q in D}==D)
ck(len(S)**2>len(D))
finish('self_normalizer_fails_without_simple_factors')
print(json.dumps({'result':'PASS','mechanism_counts':counts,'total':sum(counts.values()),'scope':'Independent post-candidate exact constructions; no author imports. Finite checks supplement the universal proof audit.'},indent=2))
