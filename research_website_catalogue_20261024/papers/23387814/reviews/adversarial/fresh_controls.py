"""Fresh exact controls derived from the published five-page construction.
No submitted mathematics helper or archived result is imported.
"""
from fractions import Fraction as Q
from pathlib import Path
from datetime import datetime,timezone
import json
R=Path(__file__).resolve().parent
checks=0
def ck(v,msg):
 global checks; checks+=1
 if not v:raise AssertionError(msg)
def inter(a,b):return a[0]*b[0]-sum(x*y for x,y in zip(a[1:],b[1:]))
def add(a,b):return [x+y for x,y in zip(a,b)]
def mul(c,a):return [c*x for x in a]
def rem(a,b):
 a=list(map(Q,a));b=list(map(Q,b))
 while a and a[-1]==0:a.pop()
 while len(a)>=len(b):
  k=len(a)-len(b);fac=a[-1]/b[-1]
  for i,x in enumerate(b):a[i+k]-=fac*x
  while a and a[-1]==0:a.pop()
 return a
def gcd(a,b):
 while b:a,b=b,rem(a,b)
 return [x/a[-1] for x in a]
def poly_add(*ps):
 d={}
 for p in ps:
  for m,c in p.items():d[m]=d.get(m,0)+c
 return {m:c for m,c in d.items() if c}
def derivative(p,k):
 out={}
 for powers,c in p.items():
  if powers[k]:q=list(powers);q[k]-=1;out[tuple(q)]=c*powers[k]
 return out
def times_var(p,k):
 out={}
 for powers,c in p.items():q=list(powers);q[k]+=1;out[tuple(q)]=c
 return out
cases=[]
for d in range(3,41):
 m=d-1;f={(m,0,1):1,(0,m,1):-1,(d,0,0):1};partials=[derivative(f,k) for k in range(3)]
 ck(poly_add(*(times_var(p,k) for k,p in enumerate(partials)))=={a:d*b for a,b in f.items()},'homogeneous Euler identity')
 ck(gcd([-1]+[0]*(m-1)+[1],[0]*(m-1)+[m])==[1],'ordinary tangent squarefree')
 ck(not any(c for pow,c in f.items() if pow[0]+pow[1]<m),'multiplicity lower terms absent')
 ck(any(c for pow,c in f.items() if pow[0]+pow[1]==m),'multiplicity exact')
 dim=lambda e:e*(e+3)//2
 for a in range(1,d):ck(dim(d)-dim(a)-dim(d-a)==a*(d-a),'reducible locus codimension identity')
 ck(min(a*(d-a) for a in range(1,d))==d-1,'minimal codimension')
 ck(dim(d)-d+2<dim(d),'join proper')
 H=[1]+[0]*d**2;E=[0,1]+[0]*(d**2-1);F=[d]+[-1]*d**2;KY=[-3]+[1]*d**2;A=add(mul(2,F),E);N=add(KY,mul(2,F))
 ck(inter(F,F)==0 and inter(F,E)==1 and inter(E,E)==-1,'fibre section intersections')
 ck(inter(A,A)==3 and inter(A,E)==1 and inter(A,F)==1,'polarization intersections')
 ck(N==add(mul(d-3,H),F),'canonical class equality')
 ck(inter(N,N)==3*(d-1)*(d-3),'canonical square')
 ck(inter(N,E)==1 and inter(N,F)==d*(d-3),'canonical curve degrees')
 ck(2*inter(A,A)==6 and 2*inter(N,N)==6*(d-1)*(d-3),'degree-two intersection')
 # Euler characteristic check, independent of the asserted proof: topological
 # double-cover formula using four disjoint smooth degree-d fibres.
 genus=(d-1)*(d-2)//2;c2=2*(3+d*d)-4*(2-2*genus);K2=2*inter(N,N)
 ck(c2==6*(d-1)**2,'cover Euler characteristic consistency')
 ck((K2+c2)//12==(d-1)*(d-2) and (K2+c2)%12==0,'Noether integrality consistency')
 if d>=4:
  strict=(d-3)**4>K2
  ck(strict==((d-3)**3>6*(d-1)),'positive fourth-power equivalence')
  ck(strict==(d>=7),'threshold in tested range')
 cases.append({'d':d,'K2':K2,'L2':6,'upper_quotient':str(Q(1,d-1)),'strict_bound_contradiction':d>=7,'c2_consistency':c2})
for d in list(range(4,2001))+[10**20,10**100]:
 P=lambda x:(x-3)**3-6*(x-1)
 ck(P(d+1)-P(d)==3*(d-3)**2+3*(d-3)-5,'forward difference identity')
 if d>=7:ck(P(d)>0 and P(d+1)>P(d),'integer positivity and monotonicity')
# Deliberate construction changes invalidate precisely the property checked.
d=7;H=[1]+[0]*49;E=[0,1]+[0]*48;F=[d]+[-1]*49;KY=[-3]+[1]*49
ck(inter(add(F,E),E)==0,'one-fibre polarization not ample')
ck(inter(add(KY,F),E)==0,'two-branch-fibre canonical not ample')
ck(inter(KY,E)==-1,'omitting cover retains exceptional curves')
ck((6-3)**3<=6*(6-1),'d6 strict comparison fails')
ck((7-3)**3>6*(7-1),'d7 strict comparison succeeds')
# If the branch locus included the singular fibre, w^2=f(x,y) at its singular
# point would have all three first partials zero (m>=2), hence not be smooth.
branch={(0,0,2):1,(d-1,0,0):-1,(0,d-1,0):1,(d,0,0):-1}
ck(all(derivative(branch,j).get((0,0,0),0)==0 for j in range(3)),'singular-fibre branch negative control gradient vanishes')
smooth_branch={(0,0,2):1,(0,1,0):-1}
ck(derivative(smooth_branch,1).get((0,0,0),0)==-1,'smooth-fibre branch model has nonzero t derivative')
res={'completed_utc':datetime.now(timezone.utc).isoformat(),'completion_percent':65,'status':'ALL_FRESH_EXACT_CONTROLS_PASSED','assertions':checks,'degree_cases':cases,'inequality_control_count':1999,'negative_controls':{'A_F_plus_E_has_zero_section_degree':True,'only_two_branch_fibres_gives_zero_canonical_section_degree':True,'without_cover_KY_exceptional_degree_minus_one':True,'d6_does_not_contradict_bound':True,'branching_at_singular_fibre_gives_vanishing_gradient':True},'limits':'Polynomial/intersection/arithmetic consistency controls, not a computation of a generic companion curve or a replacement for Bertini, transversality, ampleness or connectedness proofs. No actual surface points are numerically approximated.'}
(R/'fresh_results.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'status':res['status'],'assertions':checks,'degrees':len(cases),'smallest_example':next(x for x in cases if x['d']==7),'negative_controls':res['negative_controls']},indent=2))
