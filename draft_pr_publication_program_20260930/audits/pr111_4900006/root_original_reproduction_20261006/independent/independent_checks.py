#!/usr/bin/env python3
"""Independent exact Jacobian/frame and exterior-volume checks. No author imports."""
from fractions import Fraction as Q
from itertools import combinations,product
from pathlib import Path
import json,hashlib
count=0

def ck(ok):
 global count
 assert ok
 count+=1

def trim(a):
 a=list(a)
 while len(a)>1 and a[-1]==0:a.pop()
 return a

def padd(a,b):
 c=[Q(0)]*max(len(a),len(b))
 for i,x in enumerate(a):c[i]+=x
 for i,x in enumerate(b):c[i]+=x
 return trim(c)
def pmul(a,b):
 c=[Q(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return trim(c)
def pscale(k,a):return trim([k*x for x in a])
def pd(a):return trim([i*a[i] for i in range(1,len(a))] or [Q(0)])
def pe(a,x):
 v=Q(0)
 for c in reversed(a):v=v*x+c
 return v
p=list(map(Q,[-4,5,-1]));q=list(map(Q,[1,0,1]))
pprime=padd(pmul(pd(p),q),pscale(-1,pmul(p,pd(q))))
ck(pprime==list(map(Q,[5,6,-5])))
ck(padd(p,pscale(4,q))==list(map(Q,[0,5,3])))
# Upper bound f <=3/2: a positive square plus3 in the numerator.
ck(padd(pscale(Q(3,2),q),pscale(-1,p))==padd(pscale(Q(5,2),pmul([-1,1],[-1,1])),[3]))
q2=pmul(q,q)
left=padd(pscale(8,q2),pscale(-2,pmul([0,1],pprime)))
right=padd(pscale(5,padd(padd(pmul([-1,1],[-1,1]),[0,0,1]),[0,0,0,0,1])),padd(pscale(3,pmul([-1,0,1],[-1,0,1])),[0,0,0,10]))
ck(left==right) # positive for every real s>=0, an exact global certificate

def f(s):return pe(p,s)/pe(q,s)
def fp(s):return pe(pprime,s)/pe(q2,s)
def mm(A,B):return [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def tr(A):return [list(x) for x in zip(*A)]
O=[[Q(0),Q(-1)],[Q(1),Q(0)]]
frame_cases=0
for r in [Q(1,5),Q(1,2),Q(1),Q(3,2),Q(2),Q(5,2),Q(4)]:
 for k in range(-15,16):
  a=Q(k,7);c=(1-a*a)/(1+a*a);h=2*a/(1+a*a)
  R=[[c,-h],[h,c]];x,y=r*c,r*h;s=x*x+y*y
  ck(s==r*r);ck(mm(tr(R),R)==[[1,0],[0,1]])
  for omega in [Q(0),Q(1),Q(-3,2)]:
   J=[[f(s)+2*x*x*fp(s),2*x*y*fp(s)-omega],[2*x*y*fp(s)+omega,f(s)+2*y*y*fp(s)]]
   JR=mm(tr(R),mm(J,R))
   rotated=[[JR[i][j]-omega*O[i][j] for j in range(2)] for i in range(2)]
   ck(rotated==[[f(s)+2*s*fp(s),0],[0,f(s)]])
   ck(J[0][0]+J[1][1]==2*f(s)+2*s*fp(s))
   ck(J[0][0]+J[1][1]<=11)
   frame_cases+=1
# Signs and radial stationary sets; symbolic factoring is the all-radius proof.
ck(pe(p,Q(1))==pe(p,Q(4))==0 and pe(p,0)==-4)
ck(f(Q(1))+2*fp(Q(1))==3)
ck(f(Q(4))+8*fp(Q(4))==Q(-24,17))
for j in range(1,161):
 r=Q(j,20);s=r*r
 ck((f(s)<0)==(r<1 or r>2))
 ck((f(s)>0)==(1<r<2))
 ck(-4<=f(s)<=Q(3,2))
# Compute each exterior-volume exponent directly as a maximal subset sum.
states={'O':(Q(-4),Q(-4)),'U':(Q(3),Q(0)),'S':(Q(0),Q(-24,17))}
table={};global_M=[Q(-1000)]*5
for u,v in product(states,repeat=2):
 raw=states[u]+states[v]+(Q(-100),)
 M=[Q(0)]+[max(sum(w) for w in combinations(raw,k)) for k in range(1,6)]
 spectrum=[M[k]-M[k-1] for k in range(1,6)]
 ck(spectrum==sorted(raw,reverse=True))
 j=max(k for k in range(6) if M[k]>=0)
 point=Q(j)+M[j]/(-spectrum[j])
 fixed=Q(4)+M[4]/100
 ck(M[5]<0 and spectrum[4]==-100)
 ck(M[j]+(point-j)*spectrum[j]==0)
 ck(0<=point<=5)
 for k in range(5):global_M[k]=max(global_M[k],M[k+1])
 table[u+v]={'spectrum':[str(z) for z in spectrum],'KY':str(point),'fixed_j4':str(fixed)}
ck(global_M==[3,6,6,6,-94])
ck(Q(table['UU']['KY'])==Q(203,50))
ck(Q(table['UU']['fixed_j4'])==Q(203,50))
for key,row in table.items():
 if key!='UU':
  ck(Q(row['KY'])<Q(203,50));ck(Q(row['fixed_j4'])<Q(203,50))
# Isolated periodic candidates: each radius nonzero requires1 or2.
# Both active frequencies have irrational ratio; algebraic certificate sqrt2∉Q.
# Finite controls below check the integer equation only; the proof uses infinite descent.
for m in range(1,41):
 for n in range(1,41):ck(m*m!=2*n*n)
root=Path(__file__).resolve().parent
result={'verdict':'PASS','assertions':count,'method':'Independent standard-library rational polynomial identities, Cartesian Jacobian conjugation in rotating orthonormal frames, and maximal exterior-volume subset sums','frame_cases':frame_cases,'ordered_spectral_types':table,'global_partial_sums':[str(x) for x in global_M],'frozen_artifact_sha256':hashlib.sha256((root/'author_replay/COUNTEREXAMPLE.md').read_bytes()).hexdigest(),'limitations':['Finite controls do not establish global attraction, completeness, irrationality, or asymptotic limits; those are checked analytically in REVIEW.md.','The result concerns only the unrestricted maximizer assertion; no Lorenz, chaotic, typical-system or novelty claim.']}
(root/'independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'verdict':result['verdict'],'assertions':count,'frame_cases':frame_cases}))
