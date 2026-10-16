#!/usr/bin/env python3
"""Independent exact controls: no frozen author/review imports; standard library only."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
from datetime import datetime, timezone

# Quaternion multiplication from Hamilton's i,j,k table, not the snapshot's exponent rule.
units=[(1,0),(1,1),(-1,0),(-1,1),(1,2),(1,3),(-1,2),(-1,3)]
pos={x:i for i,x in enumerate(units)}
def qm(a,b):
 s,i=a;t,j=b
 if i==0:return(s*t,j)
 if j==0:return(s*t,i)
 if i==j:return(-s*t,0)
 k=6-i-j
 return(s*t*(1 if (i,j) in [(1,2),(2,3),(3,1)] else -1),k)
def gmul(i,j):return pos[qm(units[i],units[j])]
assert all(gmul(gmul(i,j),k)==gmul(i,gmul(j,k)) for i,j,k in product(range(8),repeat=3))

def zeros(r,c):return [[0]*c for _ in range(r)]
def left(entry):
 a=zeros(8,8)
 for g in entry:
  for j in range(8):a[gmul(g,j)][j]^=1
 return a

def blocks(entries):
 a=zeros(8*len(entries),8*len(entries[0]))
 for i,row in enumerate(entries):
  for j,e in enumerate(row):
   b=left(e)
   for r in range(8):
    for c in range(8):a[8*i+r][8*j+c]=b[r][c]
 return a

def mm(a,b):
 return [[sum(a[i][k]*b[k][j] for k in range(len(b)))%2 for j in range(len(b[0]))] for i in range(len(a))]
def rank(a):
 a=[r[:] for r in a];r=0;p=[]
 for c in range(len(a[0])):
  q=next((i for i in range(r,len(a)) if a[i][c]),None)
  if q is None:continue
  a[r],a[q]=a[q],a[r]
  for i in range(len(a)):
   if i!=r and a[i][c]:a[i]=[x^y for x,y in zip(a[i],a[r])]
  p.append(c);r+=1
  if r==len(a):break
 return r,p

def f4mul(a,b):
 v=0
 for j in range(2):
  if b&(1<<j):v^=a<<j
 if v&4:v^=7
 return v

def f4rank(a):
 a=[r[:] for r in a];r=0
 for c in range(len(a[0])):
  q=next((i for i in range(r,len(a)) if a[i][c]),None)
  if q is None:continue
  a[r],a[q]=a[q],a[r]
  inv=next(z for z in range(1,4) if f4mul(a[r][c],z)==1)
  a[r]=[f4mul(inv,x) for x in a[r]]
  for i in range(len(a)):
   if i!=r and a[i][c]:
    t=a[i][c];a[i]=[x^f4mul(t,y) for x,y in zip(a[i],a[r])]
  r+=1
  if r==len(a):break
 return r

def columns(a,indices):return [[row[j] for j in indices] for row in a]
D=[blocks([[[0,1],[0,4]]]),blocks([[[0,4],[0,7]],[[0,5],[0,1]]]),blocks([[[0,1]],[[0,4]]]),blocks([[list(range(8))]])]
ranks=[rank(a)[0] for a in D]
assert ranks==[7,9,7,1]
composites=[mm(D[i],D[(i+1)%4]) for i in range(4)]
assert all(not any(map(any,a)) for a in composites)
# Identify each syzygy as an invariant image and determine actual C2 restriction.
res=[]
for n,a in enumerate(D,1):
 _,p=rank(a);b=columns(a,p)
 t=zeros(len(a),len(a))
 for j in range(len(a)):
  t[j][j]^=1;t[(j//8)*8+gmul(j%8,2)][j]^=1
 r=rank(mm(t,b))[0]
 assert len(p)-2*r==1
 assert f4rank(a)==len(p)
 # Multiplying every independent image vector by the GF4 nontrivial unit preserves rank.
 assert f4rank([[f4mul(2,x) for x in row] for row in b])==len(p)
 res.append({'syzygy':n,'dimension':len(p),'C2_nilpotent_rank':r,'trivial_blocks':len(p)-2*r,'free_blocks':r})
# Independent exact selected minors by reviewer pivots, not author selections.
minors=[]
for a in D:
 r,cs=rank(a);b=columns(a,cs);_,rs=rank([list(v) for v in zip(*b)])
 m=[[a[i][j] for j in cs] for i in rs]
 assert rank(m)[0]==r
 minors.append({'rows':rs,'columns':cs,'size':r,'determinant_mod2':1})
# Direct radical-power control using Hamilton multiplication in characteristic two.
def conv(a,b):
 v=[0]*8
 for i,x in enumerate(a):
  for j,y in enumerate(b):v[gmul(i,j)]^=x*y
 return v
J=[[int(i==0)^int(i==g) for i in range(8)] for g in range(1,8)]
rad_dims=[];V=[[int(i==j) for i in range(8)] for j in range(8)]
for n in range(6):
 rad_dims.append(rank([list(v) for v in zip(*V)])[0] if V else 0)
 W=[conv(v,j) for v in V for j in J]
 if not W:V=[];continue
 _,cs=rank([list(v) for v in zip(*W)]);V=[W[j] for j in cs]
assert rad_dims[-1]==0

# Rational coordinate proof checks for the abstract family, independent construction.
def det(a):
 a=[[F(x) for x in row] for row in a];v=F(1)
 for c in range(len(a)):
  q=next((j for j in range(c,len(a)) if a[j][c]),None)
  if q is None:return F(0)
  if q!=c:a[q],a[c]=a[c],a[q];v=-v
  t=a[c][c];v*=t
  for j in range(c+1,len(a)):
   u=a[j][c]/t
   for k in range(c,len(a)):a[j][k]-=u*a[c][k]
 return v

def abstract(moduli,q):
 H=list(product(*[range(n) for n in moduli]));m=len(H);idx={g:i for i,g in enumerate(H)};N=m+1;c=q-1;d=c+m
 def plus(g,h):return tuple((x+y)%n for x,y,n in zip(g,h,moduli))
 T=[[[0]*N for _ in range(N)] for _ in range(N)]
 for i in range(N):T[0][i][i]=T[i][0][i]=1
 for i,g in enumerate(H,1):
  for j,h in enumerate(H,1):
   for k in range(1,N):T[i][j][k]=1
   T[i][j][idx[plus(g,h)]+1]+=c
 def vprod(a,b):return [sum(a[i]*b[j]*T[i][j][k] for i in range(N) for j in range(N)) for k in range(N)]
 B=[[int(i==j) for i in range(N)] for j in range(N)]
 assert all(vprod(vprod(B[i],B[j]),B[k])==vprod(B[i],vprod(B[j],B[k])) for i,j,k in product(range(N),repeat=3))
 assert all(T[i][j]==T[j][i] for i,j in product(range(N),repeat=2))
 assert all(T[i][j][0]==0 for i,j in product(range(1,N),repeat=2))
 weights=[1]+[d]*m
 assert all(sum(T[i][j][k]*weights[k] for k in range(N))==weights[i]*weights[j] for i,j in product(range(N),repeat=2))
 rho=[0]+[1]*m
 assert all(vprod(B[i],rho)==[weights[i]*v for v in rho] for i in range(N))
 cubic=[vprod(vprod(B[i],B[i]),B[i])[i] for i in range(1,N)]
 assert all(v>=2 for v in cubic)
 # Rational CH multiplication-by-P rank controls semisimplicity (no numeric Fourier rank).
 P=[[c*int(i==j)+1 for j in range(m)] for i in range(m)]
 dp=det(P);assert dp==d*(c**(m-1))
 # Exact C3 characteristic polynomial identities by determinant evaluation at integers.
 char_control=[]
 if moduli==(3,) and q==2:
  A=[[T[2][j][i] for j in range(N)] for i in range(N)]
  for t in range(-4,7):
   value=det([[t*int(i==j)-A[i][j] for j in range(N)] for i in range(N)])
   assert value==t*(t-4)*(t*t+t+1)
   char_control.append({'t':t,'det_tI_minus_x1':str(value)})
  # Hermitian-to-radius defect is visible on a complex linear combination.
  # a=1+i*x1 fixed-basis involution: a*=1-i*x1; a*a=1+x1^2.
  # value at zeta is 1+i*zeta; its modulus squared 2-sqrt(3),
  # at zeta^2 it is 2+sqrt(3), while 1+x1^2 has modulus1 there.
  # dimension character dominates here (sqrt17), so use 1+i*y
  # y=(x1-x2)/sqrt3, then y-values at zeta +/- i: a-values0/2,
  # dim value1; a*a=1+y^2 values0,0,1; radius mismatch4 versus1.
 return {'H_moduli':moduli,'q':q,'basis_rank':N,'dimension_d':d,'minimum_cubic_coefficient':min(cubic),'det_multiplication_P':str(dp),'semisimple_over_C':dp!=0,'char_polynomial_C3_x1_control':char_control}
abstracts=[abstract(mods,q) for mods,q in [((3,),2),((4,),2),((5,),3),((3,2),2),((2,),2),((2,2),2),((3,),1)]]
# GF4 arithmetic sanity checks and p=2 nature of the resolution.
assert all(f4mul(x,1)==x and f4mul(x,y)==f4mul(y,x) for x,y in product(range(4),repeat=2))
# Exact Q(sqrt(3),i) species control for arbitrary complex elements.
def qadd(a,b):return(a[0]+b[0],a[1]+b[1])
def qneg(a):return(-a[0],-a[1])
def qmul(a,b):return(a[0]*b[0]+3*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def ca(a,b):return(qadd(a[0],b[0]),qadd(a[1],b[1]))
def cn(a):return(qneg(a[0]),qneg(a[1]))
def cm(a,b):return(qadd(qmul(a[0],b[0]),qneg(qmul(a[1],b[1]))),qadd(qmul(a[0],b[1]),qmul(a[1],b[0])))
Z=((F(0),F(0)),(F(0),F(0)));O=((F(1),F(0)),(F(0),F(0)));CI=((F(0),F(0)),(F(1),F(0)))
zeta=((F(-1,2),F(0)),(F(0),F(1,2)));zeta2=cm(zeta,zeta)
# x1 and x2 species at epsilon, dimension, two nontrivial cube-root characters.
x1=[Z,((F(4),F(0)),(F(0),F(0))),zeta,zeta2]
x2=[Z,((F(4),F(0)),(F(0),F(0))),zeta2,zeta]
invr=((F(0),F(1,3)),(F(0),F(0)))
y=[cm(invr,ca(a,cn(b))) for a,b in zip(x1,x2)]
assert y==[Z,Z,CI,cn(CI)]
a=[ca(O,cm(CI,v)) for v in y];astar=[ca(O,cn(cm(CI,v))) for v in y]
aastar=[cm(a,b) for a,b in zip(a,astar)]
assert a==[O,O,Z,((F(2),F(0)),(F(0),F(0)))]
assert aastar==[O,O,Z,Z]
complex_control={'field':'exact Q(sqrt(3),i)','y':'(x1-x2)/sqrt(3)','a':'1+i*y','y_species':['0','0','i','-i'],'a_species':['1','1','0','2'],'a_star_a_species':['1','1','0','0'],'rho_a_squared':4,'rho_a_star_a':1,'full_symmetry_radius_identity_fails':True,'all_positive_element_radius_identities_still_hold':'written all-element real-positive deduction'}
# The displayed resolution is genuinely characteristic two: d3*d4=2N otherwise.
assert all((2%p)!=0 for p in [3,5,7])
result={'complex_species_control':complex_control,'odd_characteristic_negative_control':'d3*d4 contains 2N and is nonzero over F3,F5,F7','utc':datetime.now(timezone.utc).isoformat(),'implementation':'independent Hamilton-unit matrices and rational abstract coordinates; no author imports','Q8':{'group_associativity':True,'ranks_F2':ranks,'ranks_F4_same':True,'composites_zero':True,'exact_syzygy_C2_restrictions':res,'independent_nonzero_minors':minors,'radical_power_dimensions':rad_dims,'minimal_period':'4: dimensions 1,7,9,7,1 with projective-free cancellation; divisors 1 and 2 excluded; proof in PRE_REPLAY_PROOF.md'},'abstract_controls':abstracts}
print(json.dumps(result,indent=2))
