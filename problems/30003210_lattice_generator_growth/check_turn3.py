from fractions import Fraction as F
import json
checks=0
def test(x):
 global checks
 assert x;checks+=1
for q in range(1,51):
 for p in range(1,q+1):
  alpha=F(p,q)
  for a in range(1,31):
   exponent=a*(1-alpha)-alpha
   test((exponent<0)==(alpha>F(a,a+1)))
   test((exponent==0)==(alpha==F(a,a+1)))
for a in range(1,31):
 alpha=F(a,a+1);test(a*(1-alpha)-alpha==0)
for k in range(1,101):
 # exact models R=1/k^2 and permitted m<=k.
 for m in range(1,k+1):test(F(m,k*k)<=F(1,k))
print(json.dumps({'assertions':checks,'scope':'rational exponent and profile controls; no lattice counterexample or effective FMW rate'},indent=2))
