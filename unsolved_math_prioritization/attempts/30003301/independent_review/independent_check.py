"""Separate algebraic review controls. No author checker is imported.
The topology/source hypotheses are audited in the written review.
"""
from itertools import permutations,product
import json
import sympy as s
count=0
# Universal conjugation-product identity in a free word model.
def inv(w):return [-x for x in w[::-1]]
def red(w):
 st=[]
 for x in w:
  if st and st[-1]==-x:st.pop()
  else:st.append(x)
 return st
for n in range(1,16):
 xs=list(range(1,n+1));fs=list(range(n+1,2*n+1))
 lhs=[];rhs=[];prefix=[]
 for x,f in zip(xs,fs):
  lhs += [x,f,-x]
  delta=[x,f,-x,-f]
  rhs += prefix+delta+inv(prefix)
  prefix += [f]
 rhs += fs
 assert red(lhs)==red(rhs);count+=1
# Integral triangular prefix generators: no saturation permitted.
for g in (2,3,4):
 dim=2*g;J=s.zeros(dim)
 for j in range(g):J[2*j,2*j+1]=1;J[2*j+1,2*j]=-1
 vecs=[]
 for j in range(7):
  v=s.zeros(dim,1);v[j%dim]=1;v[(j+2)%dim]+=(j%3)-1;vecs.append(v)
 V=s.Matrix.hstack(*vecs);U=s.eye(len(vecs));prefix=s.eye(dim);Bs=[]
 for i,v in enumerate(vecs):
  Bs.append(prefix*v)
  coeff=s.eye(len(vecs))[:,i]
  for j in range(i-1,-1,-1):
   w=V*coeff;coeff[j]+=(w.T*J*vecs[j])[0]
  U[:,i]=coeff
  prefix=prefix*(s.eye(dim)-v*v.T*J)
 assert V*U==s.Matrix.hstack(*Bs);count+=dim*len(vecs)
 assert U.det()==1;count+=1
 # Every transvection preserves the integral symplectic form.
 for v in vecs:
  A=s.eye(dim)-v*v.T*J;assert A.T*J*A==J;count+=dim*dim
# A rational span can be larger than the integral vanishing-cycle lattice.
V=s.Matrix([[1,1],[0,2]])
assert V.det()==2 and V.inv()*s.Matrix([0,1])==s.Matrix([-s.Rational(1,2),s.Rational(1,2)]);count+=1
# Integral Heisenberg quotient using 3x3 matrices, rather than triples.
X=s.eye(3);X[0,1]=1;Y=s.eye(3);Y[1,2]=1;Z=s.eye(3);Z[0,2]=1
comm=lambda a,b:a*b*a.inv()*b.inv()
assert comm(X,Y)==Z;count+=9
assert comm(X,Y)*comm(Y,X)==s.eye(3);count+=9
x,y,z,m=s.symbols('x y z m',integer=True)
U=s.Matrix([[1,x,z],[0,1,y],[0,0,1]]);Zm=s.eye(3);Zm[0,2]=m
assert U*Zm*U.inv()==Zm;count+=9
assert (Z*Z)[0,2] not in (0,1);count+=1
# Lagrangian kernel and positive transvection sum, symbolic.
J=s.diag(s.Matrix([[0,1],[-1,0]]),s.Matrix([[0,1],[-1,0]]))
P=s.Matrix([[1,0,0,1],[0,1,1,0]])
a,b,c,d=s.symbols('a b c d',real=True)
v=s.Matrix([a,b,-b,-a]);w=s.Matrix([c,d,-d,-c])
assert P*v==s.zeros(2,1);count+=2
assert (v.T*J*w)[0]==0;count+=1
Nv=-v*v.T*J;Nw=-w*w.T*J
assert s.simplify(Nv*Nw)==s.zeros(4);count+=16
assert s.expand(s.trace(v*v.T))==2*a*a+2*b*b;count+=1
# Ordered finite quotient criterion on S3 with nontrivial inner automorphisms.
G=list(permutations(range(3)));E=(0,1,2)
def mul(a,b):return tuple(a[b[i]] for i in range(3))
def inverse(a):return tuple(a.index(i) for i in range(3))
def conjugate(h,a):return mul(mul(h,a),inverse(h))
zvals=[(1,0,2),(1,2,0),(2,1,0)]
hvals=[(1,2,0),(1,0,2),(2,0,1)]
Ds=[]
for z0,h in zip(zvals,hvals):
 Ds.append({mul(mul(x,E if epsilon==0 else z0),conjugate(h,inverse(x))) for x in G for epsilon in (0,1)})
reachable={E};prefix=E
for D,h in zip(Ds,hvals):
 reachable={mul(r,conjugate(prefix,d0)) for r in reachable for d0 in D};prefix=mul(prefix,h)
direct=set();order_witness=False
for ds in product(*Ds):
 r=E;h=E
 for d0,hi in zip(ds,hvals):r=mul(r,conjugate(h,d0));h=mul(h,hi)
 direct.add(r);count+=1
 bad=mul(mul(ds[0],ds[1]),ds[2])
 order_witness |= bad!=r
assert reachable==direct and order_witness;count+=2
# Manual transcription of only the seven source rows used by the certificate.
vectors={
'w3':[1,2,2,2,1,2,2,2,2]+[0,0,2,0,0,0,-1,0,0],
'a3':[1,3,2,2,1,2,2,3,2]+[0,0,2,0,0,0,-1,0,-1],
'a3prime':[1,2,2,3,1,3,2,2,2]+[0,0,2,0,0,0,-1,0,-1],
'z2':[0,0,0,1,0,1,0,0,0]+[0,0,0,-1,1,-1,0,0,0],
'b3':[0,1,0,1,0,1,0,1,0]+[0,0,0,0,0,0,1,0,-2],
'b4':[0]*9+[1,-1,1,-1,1,-1,2,-1,-1],
'b4prime':[0]*9+[1,-1,1,-1,1,-1,2,-1,0]}
co={'a3':2,'a3prime':2,'w3':-4,'z2':-1,'b3':-1,'b4prime':1,'b4':-1}
target=[0,1,0,0,0,0,0,1,0]+[0,0,0,1,-1,1,-1,0,-1]
assert [sum(co[k]*vectors[k][i] for k in co) for i in range(18)]==target;count+=18
# Spin algebraic dual. This is intersection arithmetic, not embedded realization.
t=s.symbols('t',integer=True);form=s.Matrix([[2*t,1],[1,0]]);S=s.Matrix([1,-t-1]);F=s.Matrix([0,1])
assert s.expand((S.T*form*S)[0])==-2;count+=1
assert (S.T*form*F)[0]==1;count+=1
print(json.dumps({'status':'PASS','exact_assertions_and_instances':count,'source_table_rows_manually_transcribed':7,'finite_quotient_fixture':'S3 with nontrivial inner automorphisms, not a mapping-class realization','ordered_fixture_reachable_size':len(reachable),'ordered_action_changes_an_individual_word':order_witness,'limitations':'Independent group, lattice and intersection controls; no full nonabelian Baykur-Hamada monodromy certificate, section or original-target counterexample.'},indent=2))
