#!/usr/bin/env python3
"""Fresh algebraic controls before reading any submitted executable.
Own sparse commutative/word polynomial and exact matrix implementations.
"""
from collections import defaultdict
from itertools import product
from pathlib import Path
from datetime import datetime,timezone
import json,random
HERE=Path(__file__).resolve().parent

def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def add(a,b):
 c=dict(a)
 for m,v in b.items():
  c[m]=c.get(m,0)+v
  if not c[m]:del c[m]
 return c
def neg(a):return {m:-v for m,v in a.items()}
def sub(a,b):return add(a,neg(b))
def scale(a,n):return {m:v*n for m,v in a.items() if v*n}
def mul(a,b,cap=None,comm=True):
 c=defaultdict(int)
 for m,v in a.items():
  for n,w in b.items():
   if cap is not None and len(m)+len(n)>cap:continue
   k=tuple(sorted(m+n)) if comm else m+n;c[k]+=v*w
 return {m:v for m,v in c.items() if v}
ONE={():1}
def var(i):return {(i,):1}
def eye(n):return [[dict(ONE) if i==j else {} for j in range(n)] for i in range(n)]
def mm(A,B,cap=None):
 n=len(A);C=[[{} for _ in range(n)] for _ in range(n)]
 for i in range(n):
  for j in range(n):
   for k in range(n):C[i][j]=add(C[i][j],mul(A[i][k],B[k][j],cap))
 return C
def ma(A,B):return [[add(a,b) for a,b in zip(r,s)] for r,s in zip(A,B)]
def ms(A,B):return [[sub(a,b) for a,b in zip(r,s)] for r,s in zip(A,B)]
def mscale(A,p):return [[mul(a,p) for a in r] for r in A]
def bracket(A,B,cap=None):return ms(mm(A,B,cap),mm(B,A,cap))
def zero(A):return all(not a for r in A for a in r)
def P(X,Y,Z):return bracket(bracket(bracket(X,Y),bracket(X,Z)),X)
def Q(X,Y):return P(X,Y,bracket(X,Y))
def det3(A):
 z={}
 for p,sgn in [((0,1,2),1),((1,2,0),1),((2,0,1),1),((0,2,1),-1),((2,1,0),-1),((1,0,2),-1)]:
  z=add(z,scale(mul(mul(A[0][p[0]],A[1][p[1]]),A[2][p[2]]),sgn))
 return z
X=[[var(0),var(1)],[var(2),var(3)]];Y=[[var(4),var(5)],[var(6),var(7)]];Z=[[var(8),var(9)],[var(10),var(11)]]
require(zero(P(X,Y,Z)),'universal 12-variable integer PI')
require(zero(Q(X,Y)),'universal 8-variable weighted PI')
# Distinct algebraic mechanism: an explicit centralizer formula, no CH invocation.
coords=lambda A:[sub(A[0][0],A[1][1]),A[0][1],A[1][0]]
det=det3([coords(X),coords(Y),coords(Z)])
tr=add(X[0][0],X[1][1]);central=ms(mscale(X,{():2}),mscale(eye(2),tr))
C=bracket(bracket(X,Y),bracket(X,Z))
require(zero(ma(C,mscale(central,det))),'explicit centralizer determinant identity')
# Noncommutative leading polynomials and independently constructed literal words.
def ncbr(a,b):return sub(mul(a,b,comm=False),mul(b,a,comm=False))
p=ncbr(ncbr(ncbr(var(1),var(2)),ncbr(var(1),var(3))),var(1))
q=ncbr(ncbr(ncbr(var(1),var(2)),ncbr(var(1),ncbr(var(1),var(2)))),var(1))
require(p.get((1,1,2,1,3))==-1 and q.get((1,1,1,2,1,2))==1,'integral coefficient')
def red(word):
 out=[]
 for x in word:
  if out and out[-1]==-x:out.pop()
  else:out.append(x)
 return tuple(out)
def inv(word):return tuple(-x for x in reversed(word))
def wc(a,b):return red(a+b+inv(a)+inv(b))
w=wc(wc(wc((1,),(2,)),wc((1,),(3,))),(1,))
v=wc(wc(wc((1,),(2,)),wc((1,),wc((1,),(2,)))),(1,))
def magnus(word,cap):
 out=ONE
 for x in word:
  factor=add(ONE,var(x)) if x>0 else {(-x,)*k:(-1)**k for k in range(cap+1)}
  out=mul(out,factor,cap,comm=False)
 return sub(out,ONE)
ww=magnus(w,5);vv=magnus(v,6)
require(ww==p and vv==q,'literal full Magnus expansions')
# Exact inverse substitutions in free words, on minimal ranks and two larger ranks.
def substitute(word,images):
 out=()
 for x in word:out=red(out+(images[x] if x>0 else inv(images[-x])))
 return out
inverses=0
for u,t in [(w,4),(v,3)]:
 for n in [t,t+1,t+4]:
  phi={i:(i,) for i in range(1,n+1)};psi=dict(phi);phi[t]=(t,)+u;psi[t]=(t,)+inv(u)
  for i in range(1,n+1):
   require(substitute(phi[i],psi)==(i,) and substitute(psi[i],phi)==(i,),'free inverse');inverses+=2
# Direct integral unitriangular multiplication gives finite lower-central witnesses.
def imul(A,B):return [[sum(A[i][k]*B[k][j] for k in range(len(A))) for j in range(len(A))] for i in range(len(A))]
def ieye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def iadd(A,B):return [[a+b for a,b in zip(r,s)] for r,s in zip(A,B)]
def ineg(A):return [[-a for a in r] for r in A]
def iinv(A):
 n=len(A);N=iadd(A,ineg(ieye(n)));power=ieye(n);out=ieye(n)
 for k in range(1,n):power=imul(power,N);out=iadd(out,power if k%2==0 else ineg(power))
 require(imul(A,out)==ieye(n) and imul(out,A)==ieye(n),'unitriangular inverse');return out
def U(n,edges):
 A=ieye(n)
 for i,j in edges:A[i-1][j-1]+=1
 return A
def evalword(word,images):
 d=len(next(iter(images.values())));out=ieye(d);inverse={i:iinv(A) for i,A in images.items()}
 for z in word:out=imul(out,images[z] if z>0 else inverse[-z])
 return out
u6=evalword(w,{1:U(6,[(1,2),(2,3),(4,5)]),2:U(6,[(3,4)]),3:U(6,[(5,6)])});want=ieye(6);want[0][5]=-1;require(u6==want,'UT6 witness')
u7=evalword(v,{1:U(7,[(1,2),(2,3),(3,4),(5,6)]),2:U(7,[(4,5),(6,7)])});want=ieye(7);want[0][6]=1;require(u7==want,'UT7 witness')
# Actual multivariable nilpotent ideal quotients, not one-parameter evaluations.
# S=Z[s,t,u]/(s,t,u)^8; arbitrary matrices I+B are units (no determinant premise).
def minv(A,cap):
 B=ms(A,eye(2));power=eye(2);out=eye(2)
 for k in range(1,cap+1):power=mm(power,B,cap);out=ma(out,power if k%2==0 else mscale(power,{():-1}))
 require(zero(ms(mm(A,out,cap),eye(2))),'nilpotent inverse');return out
def eval_polyword(word,images,cap):
 inverses={i:minv(A,cap) for i,A in images.items()};out=eye(2)
 for z in word:out=mm(out,images[z] if z>0 else inverses[-z],cap)
 return ms(out,eye(2))
rng=random.Random(23387442);ideal=[]
for it in range(4):
 images={}
 for i in range(1,4):
  B=[[{} for _ in range(2)] for _ in range(2)]
  for r,c in product(range(2),repeat=2):
   for m in [(0,),(1,),(2,),(0,0),(0,1),(1,2)]:
    coeff=rng.randrange(-2,3)
    if coeff:B[r][c][m]=coeff
  images[i]=ma(eye(2),B)
 for name,word,order in [('w',w,6),('v',v,7)]:
  T=eval_polyword(word,images,7);degrees=[len(m) for row in T for entry in row for m in entry]
  require(all(d>=order for d in degrees),'actual ideal order')
  ideal.append({'case':it,'word':name,'minimum_observed_degree':min(degrees) if degrees else None,'nonzero_coefficients':len(degrees)})
# Negative matrix-size controls with exact traceless 3x3 matrices.
def cons(A):return [[({():v} if v else {}) for v in row] for row in A]
X3=cons([[-1,0,0],[0,0,0],[0,0,1]]);Y3=cons([[0,1,0],[0,0,0],[0,0,0]]);Z3=cons([[0,0,0],[0,0,1],[0,0,0]])
p3=P(X3,Y3,Z3);require(p3[0][2]=={():2},'3x3 P negative control')
X3q=cons([[-1,0,0],[0,-2,0],[0,0,3]]);Y3q=cons([[0,1,0],[0,0,1],[0,0,0]]);q3=Q(X3q,Y3q);require(q3[0][2]=={():120},'3x3 Q negative control')
# A generic lower commutator is nonzero, ruling out accidental zero arithmetic.
require(not zero(bracket(X,Y)),'nonzero bracket control')
# Wrong word parenthesization destroys matrix identity for a concrete 2x2 witness.
X2=cons([[1,0],[0,-1]]);Y2=cons([[0,1],[0,0]]);Z2=cons([[0,0],[1,0]])
wrong=bracket(bracket(bracket(X2,Y2),X2),bracket(X2,Z2));require(not zero(wrong),'parenthesization fault')
result={'completed_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','scope':'Exact universal polynomial identities plus finite independent controls; whole theorem requires the written argument.','before_helper_inspection':True,'universal_P_generic_variables':12,'universal_Q_generic_variables':8,'explicit_centralizer_formula_verified':True,'P_terms':len(p),'Q_terms':len(q),'w_reduced_length':len(w),'v_reduced_length':len(v),'P_target_coefficient':p[(1,1,2,1,3)],'Q_target_coefficient':q[(1,1,1,2,1,2)],'inverse_composition_checks':inverses,'unitriangular_results':{'w_UT6_corner':u6[0][5],'v_UT7_corner':u7[0][6]},'multivariable_ideal_quotients':ideal,'negative_controls':{'P_3x3_corner':2,'Q_3x3_corner':120,'generic_bracket_nonzero':True,'wrong_parenthesization_nonzero':True}}
(HERE/'independent_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
