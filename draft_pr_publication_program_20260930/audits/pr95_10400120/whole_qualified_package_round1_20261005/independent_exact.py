# Fresh verifier, written without importing or copying candidate/prior verifiers.
from itertools import permutations, product
from collections import Counter
from fractions import Fraction
import json, math, sys
N=50; DEG=20

def guard(c,m):
 if not c: raise RuntimeError(m)
def reduce(v):
 v=list(v)+[0]*max(0,(DEG+1)-len(v))
 for j in range(len(v)-1,DEG-1,-1):
  x=v[j];v[j]=0
  # z^20 = z^15-z^10+z^5-1
  for o,s in [(15,1),(10,-1),(5,1),(0,-1)]:v[j-DEG+o]+=s*x
 return tuple(v[:DEG])
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def scale(a,n):return tuple(n*x for x in a)
def mono(j):
 v=[0]*N;v[j%N]=1;return reduce(v)
def mul(a,b):
 v=[0]*(2*DEG-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):v[i+j]+=x*y
 return reduce(v)
def conj(a):
 r=ZERO
 for j,x in enumerate(a):r=add(r,scale(mono(-j),x))
 return r
ZERO=(0,)*DEG;ONE=mono(0)
rho=(2,1,0,-1,-2)
perms=list(permutations(range(5)))
def parity(p):return (-1)**sum(p[i]>p[j] for i in range(5) for j in range(i+1,5))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
quot=[(a,b-a,c-b,d-c,-d) for a,b,c,d in product(range(5),repeat=4)]
guard(len(set(quot))==625,'quotient count')
guard(all(sum(v)==0 and dot(v,v)%2==0 for v in quot),'root lattice/evenness')
S=add(scale(add(mono(5),mono(-5)),2),scale(ONE,-1))
guard(mul(S,S)==scale(ONE,5),'sqrt5 algebra')
rows={}; B={}
for q in [1,2,3,4,6,7,-1,-2]:
 r=ZERO; survivors=[]
 for p in perms:
  wr=tuple(rho[i] for i in p);v=tuple(q*x-y for x,y in zip(rho,wr));res=[x%5 for x in v]
  ch=ZERO
  for nu in quot:
   # r*q/p = 2q, so exp(pi*i*2q*nu^2)=1 exactly.
   guard((2*q*dot(nu,nu))%2==0,'quadratic phase')
   ch=add(ch,mono(10*dot(nu,v)))
  predicts=all(x==res[0] for x in res)
  guard(ch==(scale(ONE,625) if predicts else ZERO),'annihilator character')
  if predicts:
   term=scale(mono(-dot(rho,wr)),parity(p));r=add(r,term)
   survivors.append({'p':p,'wrho':wr,'parity':parity(p),'dot':dot(rho,wr),'residue':res[0],'in_5Y':all(x%5==0 for x in v)})
 guard(len(survivors)==5,'survivor count')
 rows[q]=survivors;B[q]=r
A=ZERO
for p in perms:A=add(A,scale(mono(-5*dot(rho,tuple(rho[i] for i in p))),parity(p)))
guard(A==add(scale(ONE,10),scale(S,-5)),'vacuum denominator')
nA=mul(A,conj(A)); guard(nA==add(scale(ONE,225),scale(S,-100)),'vacuum square')
inverse=add(scale(ONE,225),scale(S,100));guard(mul(nA,inverse)==scale(ONE,625),'inverse denominator')
guard(B[1]==add(add(mono(-10),scale(ONE,2)),scale(mono(5),2)),'B1')
guard(B[2]==scale(add(add(ONE,scale(mono(-5),2)),scale(mono(5),2)),-1),'B2')
expected=[(11,2,3475,1550),(9,4,4025,1800)]
if '--false-target' in sys.argv: expected[0]=(11,2,3476,1550)
for q,(a,b,c,d) in enumerate(expected,1):
 norm=mul(B[q],conj(B[q]));guard(norm==add(scale(ONE,a),scale(S,b)),'B norm')
 target=mul(norm,inverse);guard(target==add(scale(ONE,c),scale(S,d)),'claimed squared magnitude')
for q in [1,2]:
 guard(B[q+5]==B[q],'q periodic')
 guard(mul(B[5-q],conj(B[5-q]))==mul(B[q],conj(B[q])),'inverse/orientation norm')
 guard(conj(B[q])==B[-q],'orientation polynomial')
# Positive embedding is separately established by 0<2*pi/10<pi/2 and
# 2cos(pi/5)>1; sqrt5=4cos(pi/5)-1>0. Fractions prove s>0.
guard(225*225>100*100*5,'positive exact norm denominator')
labels=[v for v in product(range(6),repeat=4) if sum(v)<=5]
guard(len(labels)==math.comb(9,4)==126,'full weight count')
print(json.dumps({'ring':'Z[zeta50]/Phi50','algorithmic_counts':{'quotient_representatives':625,'Weyl_permutations':120,'labels':126,'q_checks':8},'sqrt5_polynomial':S,'A':A,'survivors':rows,'targets':['3475+1550sqrt5','4025+1800sqrt5'],'checks':'passed','limits':'Finite counts are not theorem or quality counts; HT and RT imported.'},indent=2))
