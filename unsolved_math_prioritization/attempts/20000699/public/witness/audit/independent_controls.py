#!/usr/bin/env python3
"""Independent exact rational and finite-coefficient controls for the audit.
These controls certify identities and detect regression errors, not asymptotics.
"""
import json, hashlib
from pathlib import Path
import sympy as S
OUT=Path(__file__).parent
checks={}
q,A,B,C,D,Z=S.symbols('q A B C D Z', nonzero=True)
base=(1-q*C/A)*(1-q*D/B)
den=1-q/(A*B*Z)
density_local=(base+q*C*D*Z*den)/den
correct=(1-q*C/A-q*D/B+q*C*D*Z)/den
printed=(1-q*Z*C/A-q*Z*D/B+q*Z*C*D)/(1-q*Z/(A*B))
assert S.factor(density_local-correct)==0
checks['displaced_euler_identity']=True
assert S.factor(correct-printed)!=0
checks['printed_euler_identity_is_not_same']=True
assert S.cancel(printed.subs({A:1,B:1,C:1,D:1}))==1
checks['printed_all_zero_local_factor_is_one']=True
checks['printed_vs_correct_rational_witness']={
 'correct':str(correct.subs({q:S.Rational(1,2), A:S.Rational(11,10),B:S.Rational(12,10),C:S.Rational(13,10),D:S.Rational(14,10),Z:S.Rational(15,10)})),
 'printed':str(printed.subs({q:S.Rational(1,2), A:S.Rational(11,10),B:S.Rational(12,10),C:S.Rational(13,10),D:S.Rational(14,10),Z:S.Rational(15,10)}))}
for n in range(1,2001):
    fac=S.factorint(n)
    assert sum(int(S.mobius(e)) for e in S.divisors(n)) == (n==1)
    for p in fac:
        va=sum(int(S.mobius(e))*S.factorint(n//e).get(p,0) for e in S.divisors(n))
        vg=sum(int(S.mobius(e))*S.factorint(e).get(p,0) for e in S.divisors(n))
        target=int(len(fac)==1)
        assert va==target and vg==-target
checks['divisor_collision_and_log_derivatives_n_le_2000']=True
for p in list(S.primerange(2,200)):
    for h in range(1,201):
        cp=p-1 if h%p==0 else -1
        nu=1 if h%p==0 else 2
        ram=1+S.Rational(cp,(p-1)**2)
        hl=(1-S.Rational(nu,p))/(1-S.Rational(1,p))**2
        assert ram==hl
checks['ramanujan_equals_hl_local_factors']=True
phi,psi,lam=S.Rational(3,4),S.Rational(1,4),S.Rational(6,5)
assert 0<psi<=phi<1 and 1<lam<2 and lam*phi<1 and lam*(1-psi)<1
checks['nonempty_admissible_example']={'phi':str(phi),'psi':str(psi),'lambda':str(lam),'lambda_phi':str(lam*phi),'lambda_1minuspsi':str(lam*(1-psi))}
checks['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
(OUT/'independent_controls.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
