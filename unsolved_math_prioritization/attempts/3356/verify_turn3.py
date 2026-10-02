import json
from certify_turn1 import certify
summary,rows=certify(1000000)
n=0;patterns={'1_mod3':0,'2_mod3':0}
for row in rows:
 if row[2]!='lucas_prime_primitive':continue
 q,p=row[:2];s=(-4*q*q)%p
 assert pow(3,4*q**4,p)==s
 assert s*s%p==p-1
 x=pow(3,4*q**3,p)
 target=pow(s,q%4,p)
 assert (pow(x,4,p)==1)==(x==target)
 assert x!=target
 octic=pow(3,2*q**4,p);v=8*q**3%p
 assert octic in (v,(-v)%p)
 legendre_q3=1 if q%3==1 else -1
 assert octic==(-legendre_q3*v)%p
 n+=1;patterns[str(q%3)+'_mod3']+=1
print(json.dumps({'status':'PASS_FINITE_QUARTIC_AND_OCTIC_CONTROLS','q_bound':1000000,'certified_prime_cases':n,'octic_sign_pattern_counts':patterns,'qualification':'Quartic identity has a reciprocity proof. Octic sign is finite evidence only and is not used to claim the original conjecture.'},indent=2))
