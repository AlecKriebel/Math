"""Independent geometric-count crossing controls with explicit false-claim tests."""
from fractions import Fraction as F
import json
checks=0
def ck(v,label):
    global checks
    if not v:raise RuntimeError(label)
    checks+=1
def renewal(law,t,strict=True):
    u=[F(0)]*(t+1);u[0]=F(1)
    for s in range(1,t+1):u[s]=sum((w*u[s-x] for x,w in law.items() if x<=s),F(0))
    masses={x:w*sum((u[s] for s in range(t+1) if (s+x>t if strict else s+x>=t)),F(0)) for x,w in law.items()}
    return masses
cases=0
for a in range(3,10):
    for pnum in range(1,9):
        for rnum in range(1,9):
            p=F(pnum,20);r=F(rnum,20);small=1-p-r
            law={1:small/2,2:small/2,a:p,2*a:r};q=p+r
            ck(sum(law.values())==1 and small>0,'law normalization')
            for t in range(a):
                mass=renewal(law,t);ck(sum(mass.values())==1,'strict renewal total')
                L=t//2+1
                bound=p/q-(1-q)**L
                ck(mass[a]>=bound,'independent geometric-count crossing lower bound')
                cases+=1
for n in range(2,101):
    e=3*4**(n-1)-2**n-1
    ck(e>=2**n-1,'symbolic lower bound on log2(p_n t_n/h_n)')
    ck((3*4**n-2**(n+1)-1)-e==9*4**(n-1)-2**n,'exact exponent increment')
    ck(9*4**(n-1)-2**n>0,'positive exponent increment')
# Three genuinely false variants of the crossing inference, not malformed inputs.
false_crossing=renewal({1:F(1,2),4:F(1,2)},8)[4]
ck(false_crossing<1-F(1,8),'success length <= time invalidates claimed Markov crossing conclusion')
false_tail=renewal({1:F(1,10),4:F(9,20),100:F(9,20)},2)[4]
ck(false_tail<1-F(1,18),'omitting hit-type tail error gives a false lower bound')
false_endpoint=renewal({1:F(1,2),4:F(1,2)},1,strict=False)
ck(sum(false_endpoint.values())!=1,'replacing strict crossing by >= double-counts endpoint renewal mass')
print(json.dumps(dict(status='PASS',exact_checks=checks,geometric_crossing_cases=cases,
    scientific_false_variants_rejected=['success too short','tail type error omitted','strict endpoint replaced by weak endpoint'],
    infinite_quantifiers_proved_analytically=True,scope='Exact finite controls of independent geometric-count bound and genuine crossing-inference counterexamples; no simulation or finite proof of universal scale exclusion.'),indent=2))
