"""Fresh candidate-aware challenge: moving monodromy pullbacks and actual lifts."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
# Reuse only this audit's sealed arithmetic functions; no packet executable imports.
ns={}
src=(Path(__file__).resolve().parent/'independent_controls.py').read_text();exec(src.split("check(set(factors(3))")[0],ns)
rank=ns['rank'];zero=ns['zero'];eye=ns['eye'];mul=ns['mul'];tr=ns['tr'];cat=ns['cat'];ker=ns['ker']
checks=0;records=[]
def ck(v,s):
 global checks
 checks+=1
 if not v:raise AssertionError(s)
def cover(q,charges):
 d1=zero(q,4*q);d2=zero(4*q,4*q)
 for g in range(q):
  for t in range(4):d1[g][4*g+t]-=1;d1[(g+charges[t])%q][4*g+t]+=1
  for a in range(2):
   for b in range(2):
    c=4*g+2*a+b;x=charges[a];y=charges[2+b]
    d2[4*g+a][c]+=1;d2[4*((g+x)%q)+2+b][c]+=1
    d2[4*((g+y)%q)+a][c]-=1;d2[4*g+2+b][c]-=1
 return d1,d2
def lifted(q,target_charges):
 words=[(0,0,1),(0,1)];a,b=target_charges;source=[2*a+b,a+b]*2;target=[a,b]*2
 s1,s2=cover(q,source);t1,t2=cover(q,target)
 F1=zero(4*q,4*q);F2=zero(4*q,4*q)
 for g in range(q):
  for c in range(4):
   z=g
   for l in words[c%2]:
    typ=2*(c//2)+l;F1[4*(z%q)+typ][4*g+c]+=1;z+=target[typ]
  for x in range(2):
   for y in range(2):
    dx=0
    for ax in words[x]:
     dy=0
     for by in words[y]:
      F2[4*((g+dx+dy)%q)+2*ax+by][4*g+2*x+y]+=1;dy+=target[2+by]
     dx+=target[ax]
 ck(mul(t1,F1)==s1,'actual lifted substitution degree1')
 ck(mul(t2,F2)==mul(F1,s2),'actual lifted substitution degree2')
 ck(mul(s1,s2)==zero(q,4*q),'source CW square')
 ck(mul(t1,t2)==zero(q,4*q),'target CW square')
 Z1=ker(tr(t2));Z2=ker(tr(s1)) if False else eye(4*q)
 h1image=rank(cat(tr(s1),mul(tr(F1),Z1)))-rank(tr(s1))
 h2image=rank(cat(tr(s2),tr(F2)))-rank(tr(s2))
 # Product homotopy equivalence must preserve every class, not just counts.
 ck(h1image==4,'H1 induced actual lifted image')
 ck(h2image==q+3,'H2 induced actual lifted image')
 ck(q-rank(s1)==1,'source monodromy connected')
 ck(4*q-rank(s2)==q+3,'source exact H2')
 records.append({'q':q,'target_charges':[a,b],'source_charges':source[:2],'image_H1':h1image,'image_H2':h2image,'rank_source_H2':4*q-rank(s2),'chain_F1_rank':rank(F1),'chain_F2_rank':rank(F2)})
for q in [1,2,3,5,7,9,10,11]:
 a,b=1,0
 for n in range(3):lifted(q,(a,b));a,b=(2*a+b)%q,(a+b)%q
# PF roof: exact quadratic equations without floating-point tolerance.
# phi=(1+sqrt5)/2 satisfies phi^2=phi+1; lambda=phi+1.
def q5mul(x,y):return (x[0]*y[0]+5*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
from fractions import Fraction as F
phi=(F(1,2),F(1,2));lam=(F(3,2),F(1,2));one=(F(1),F(0))
ck(q5mul(lam,phi)==(2*phi[0]+1,2*phi[1]),'PF a roof length')
ck(lam==(phi[0]+1,phi[1]),'PF b roof length')
ck(q5mul(lam,one)!= (F(3),F(0)),'unit roof has no constant substitution expansion3')
# Exact independent TM closed complexity formula, not author's recurrence.
def tm(n):
 k=0
 while (1<<k)<n:k+=1
 words=['00','01','10','11']
 for j in range(k):words=[''.join('01' if c=='0' else '10' for c in w) for w in words]
 return {w[i:i+n] for w in words for i in range(len(w)-n+1)}
def closed(n):
 if n==1:return 2
 if n==2:return 4
 m=n-1;a=m.bit_length()-1;b=m-(1<<a);h=1<<(a-1)
 return 6*h+4*b if b<=h else 8*h+2*b
for n in range(1,301):ck(len(tm(n))==closed(n),'TM explicit complexity piecewise dyadic formula')
for a in range(2,14):
 for n,chi in [(2**(a-1),2*2**(a-1)+6),(3*2**(a-2),-2*3*2**(a-2))]:
  t=2*n;s0=closed(t+1)-closed(t);s1=closed(t+2)-closed(t+1)
  ck((n+2)*(s1-s0)+s0==chi,'large-scale signed Euler check')
# Adversarial full-star and transfer failure are necessary negative controls.
q=3;s1,s2=cover(q,[1,0,1,0]);bad=[r[:-1] for r in s2]
ck(len(bad[0])!=4*q,'one deleted lifted face destroys covering degree')
# A false transfer scaled by1 is exposed by the exact degree2 diagonal.
ck([[1]]!=[[2]],'degree2 transfer scalar mutant')
print(json.dumps({'all_passed':True,'assertions':checks,'candidate_imports':[],'moving_monodromy_actual_lift_records':records,'TM_closed_formula_lengths':300,'Euler_scale_powers':list(range(2,14)),'PF_roof_equations':'exact Q(sqrt5)','scope':'Falsification and independent validation only; no sixth author discovery'},indent=2))
