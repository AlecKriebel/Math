"""Boundary/arithmetic controls independent of binary floating point."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from random import Random
import sys,json
HERE=Path(__file__).resolve().parent
ORIG=HERE.parent/'original_submission/files/unsolved_math_prioritization/attempts/5000007'
sys.path.insert(0,str(ORIG));sys.path.insert(0,str(HERE))
from check_certificate import K,Z,R,polygon,reconstruct
from independent_exact import C,T,SQRT5,ONE,ZERO,norm,det,develop,require

checks=0
rng=Random(190)
for k in range(160):
    a,b,c,d=[F(rng.randrange(-100,101),rng.randrange(1,50)) for _ in range(4)]
    x,y=K(a,b),K(c,d);u,v=C(a)+b*SQRT5,C(c)+d*SQRT5
    require(x.sign()==u.sign(),'field sign agreement');checks+=1
    for z,w in [(x+y,u+v),(x-y,u-v),(x*y,u*v)]:
        require((z.a,z.b)==w.real_pair(),'field operation agreement');checks+=1
    if y.sign(): require((x/y).a==(u/v).real_pair()[0] and (x/y).b==(u/v).real_pair()[1],'field quotient');checks+=1
# p+q sqrt5=(9+4sqrt5)^n. Its conjugate is positive and exponentially small.
p,q=1,0;float_zero=0
for n in range(1,81):
    p,q=9*p+20*q,4*p+9*q
    require(p*p-5*q*q==1,'Pell invariant')
    require(K(p,-q).sign()==1 and K(-p,q).sign()==-1,'near cancellation exact sign')
    require((C(p)-q*SQRT5).sign()==1,'independent near cancellation exact sign');checks+=3
    try:float_zero+=float(K(p,-q))==0
    except OverflowError:pass
for expression in [lambda:K(1)/K(),lambda:Z(1)/Z(),lambda:ONE/ZERO]:
    try:expression()
    except (ZeroDivisionError,ValueError):checks+=1
    else:raise ValueError('zero denominator was accepted')
# Boundary directions are exactly vertices of the first pentagon; no arbitrarily
# long continuation through that vertex is allowed by shortness.
polys,labels=develop([1]);p0=polys[0][0]
for label,point in polys[0].items():
    if label==0:continue
    v=point-p0
    boundary=[j for j,z in polys[0].items() if det(v,z-p0)==0]
    require(len(boundary)==2 and set(boundary)=={0,label},'direct vertex ray');checks+=1
require(T*T*T*T*T==ONE and norm(T)==ONE,'rotation identity');checks+=1
out={'exact_controls_passed':checks,'random_cases':160,'Pell_cancellation_cases':80,'binary_float_zero_cases_despite_positive_exact_value':float_zero,'division_by_zero_rejected':3,'direct_vertex_rays':4,'source_hashes':{str(p):sha256(p.read_bytes()).hexdigest() for p in [ORIG/'check_certificate.py',HERE/'independent_exact.py']}}
(HERE/'EDGE_CASE_SUMMARY.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
