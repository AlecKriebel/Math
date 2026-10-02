from word_tools import parameters,negative_periods,theta_borders
import json
checks=0
def check(x):
 global checks
 assert x;checks+=1
def stagger(z):return tuple(a^(i%2) for i,a in enumerate(z))
three=two=0
for a in range(1,31):
 for b in range(1,31):
  w=stagger([0]*a+[1]*b);n=len(w)
  predicted=[p for p in range(max(a,b),n) if p%2==0]+[n]
  check(negative_periods(w,(1,0))==predicted);two+=1
  for c in range(1,21):
   w=stagger([0]*a+[1]*b+[0]*c);n=len(w)
   predicted={n-k for k in range(1,min(a,c)+1) if (n-k)%2==1}
   if b%2==0 and max(a,c)<=b:predicted.add(b)
   check(negative_periods(w,(1,0))==sorted(predicted|{n}));three+=1
classified=0
for L in range(2,14,2):
 for a in range(1,17):
  for c in range(1,17):
   M=max(a,c)
   if M<=L:expected=(L,L)
   elif M==L+1:expected=(L+2,2*L+1)
   else:expected=(M+L+1-M%2,)*2
   check(parameters(stagger([0]*a+[1]*L+[0]*c),(1,0))==expected);classified+=1
family=[]
for L in range(2,82,2):
 z=[0]*(L+1)+[1]*L+[0]*(L+1);w=stagger(z)
 # All-factor tau checked throughL=30; larger parameters follow the proved classification.
 p=min(negative_periods(w,(1,0)));check(p==2*L+1);check(len(w)==3*(L+2)-4)
 if L<=30:check(parameters(w,(1,0))==(L+2,2*L+1))
 source=stagger([0]*L+[1]*L+[0]*(L+1))
 check(min(negative_periods(source,(1,0)))==2*L+1)
 if L<=30:check(parameters(source,(1,0))==(L+2,2*L+1))
 family.append(dict(L=L,n=len(w),tau_from_proof=L+2,period=p,all_factor_tau_replayed=L<=30))
# A tempting one-sided extension produces a much longer unbordered factor.
for L in range(2,32,2):
 w=stagger([0]*L+[1]*L+[0]*(L+2))
 # suffix beginning at the final0 of the first run has a=1,c=L+2.
 u=w[L-1:]
 check(len(u)==2*L+3);check(theta_borders(u,(1,0))==[])
print(json.dumps(dict(assertions=checks,two_run_instances=two,three_run_instances=three,full_parameter_classifications=classified,symmetric_family=family,scope='Run classification and all-L family proved in TURN_3.md; finite controls are supplemental.'),indent=2,sort_keys=True))
