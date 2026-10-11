#!/usr/bin/env python3
"""Read-only probe of frozen author helper, after independent mathematics freeze."""
import runpy,random,json
from pathlib import Path
root=Path(__file__).resolve().parent
m=runpy.run_path(str(root/'public/qss-self-duality-verification/controls/verify_intrinsic.py'))
k=m['Field'](5,[1,1,0,1]); t=5
f,v=m['word_module']('FFVFVV')
mm=lambda a,b:m['multiply'](a,b,k)
tw=lambda a,aut:m['twist'](a,aut)
tr=m['transpose'];rank=lambda a:m['rank'](a,k)
# Unitriangular inverse, exact in characteristic five.
def inverse(P):
 N=[[k.sub(P[i][j],int(i==j)) for j in range(6)] for i in range(6)]
 power=m['eye'](6); answer=m['eye'](6)
 for j in range(1,6):
  power=mm(power,N)
  for i in range(6):
   for z in range(6):answer[i][z]=k.add(answer[i][z],k.neg(power[i][z]) if j%2 else power[i][z])
 assert mm(answer,P)==m['eye'](6)
 return answer
sig2=[k.sigma[k.sigma[x]] for x in range(k.q)]
tau2=[k.tau[k.tau[x]] for x in range(k.q)]
rows=[]
for name in ('minimal','dense'):
 P=m['eye'](6)
 if name=='minimal':P[0][1]=t
 else:
  rng=random.Random(34002)
  for i in range(6):
   for j in range(i+1,6):P[i][j]=k.encode([rng.randrange(5),rng.randrange(1,5),rng.randrange(5)])
 Pi=inverse(P);A=mm(mm(Pi,f),tw(P,k.sigma));B=mm(mm(Pi,v),tw(P,k.tau))
 inv=m['invariants'](A,B,k)
 A2=mm(A,tw(A,k.sigma));B2=mm(B,tw(B,k.tau))
 corrected=rank(A2)+rank(B2)-rank(m['join'](tr(tw(B2,sig2)),tr(tw(A2,tau2))))
 assert inv['delta2']==0 and inv['dual_delta2']==1 and inv['dual_kernel_formula']==0 and corrected==1
 assert mm(A,tw(B,k.sigma))==m['zeros'](6,6)==mm(B,tw(A,k.tau))
 assert rank(A)==rank(B)==3
 rows.append(dict(name=name,P_encoded=P,P_digits=[[k.decode(x) for x in r] for r in P],inverse_encoded=Pi,F_encoded=A,V_encoded=B,F2_encoded=A2,V2_encoded=B2,author_invariants=inv,corrected_formula=corrected))
print(json.dumps(dict(status='EXPECTED_AUTHOR_FORMULA_FAILURE',field='F5[t]/(t^3+t+1)',encoding='a+5b+25c represents a+b*t+c*t^2',t=t,t5=k.power(t,5),t25=k.power(t,25),witnesses=rows,verdict='NEEDS_REPAIR',scope='Concrete defect in generic dual_kernel_formula only; main theorem remains valid.'),indent=2))
