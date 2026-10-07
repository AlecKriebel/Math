"""Exact reduction controls. The published analytic monotonicity proof is not rerun."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from hashlib import sha256
import json
counts={}
def ck(cat,value):
    assert value,cat
    counts[cat]=counts.get(cat,0)+1

for n,k in product(range(1,31),repeat=2):
    m=2*n+k;b=F(m,k);a=1+b;D=F(-k,2*(k+n))
    ck('parameter_interval',-F(1,2)<D<0)
    ck('parameter_conversion',D==-1/a and D+1==b/a)
    ck('boundary_time',1/(D+1)==F(2*(k+n),k+2*n))
    ck('boundary_time_bounds',1<1/(D+1)<2)
    ck('rotation_exponent',((n+k+1)-n-1)%k==0)
    ck('incorrect_rotation_excluded',((n+k+1)-n-1)%(k+2)!=0)
    ck('reversing_phase',((n+k+1)-n-1)%(2*k)==k)
    # Coefficient comparison for the full polynomial vector field under x=-aY,y=-aX,s=-tau.
    # x_s = aX + a^2XY; y_s = -aY + abX^2-aY^2.
    ck('second_coordinate_y_square',a*b==(D+1)*a*a)
    ck('second_coordinate_x_square',-a==D*a*a)
    # On the published full quadratic annulus x<1, theta_t=1-x/a>1-1/a>0.
    ck('annulus_angular_lower_bound',1-1/a==b/a and b/a>0)

# Direct chain rule from R,Theta to X,Y at exact rational unit-circle points.
for u,R,b in product(range(-7,8),(F(1,5),F(1),F(7,3)),(F(3,2),F(2),F(7))):
    c=F(1-u*u,1+u*u);s=F(2*u,1+u*u)
    X=R*c;Y=R*s;Rd=b*R*R*c;Td=1+R*s
    Xd=Rd*c-R*s*Td;Yd=Rd*s+R*c*Td
    ck('polar_to_cartesian_first',Xd==-Y+b*X*X-Y*Y)
    ck('polar_to_cartesian_second',Yd==X+(1+b)*X*Y)

r=Path(__file__).resolve().parent
out={'artifact_sha256':sha256((r/'author_replay/KNOWN_RESULT.md').read_bytes()).hexdigest(),'exact_assertions':sum(counts.values()),'categories':counts,'global_analytic_theorem_reproved':False,'scope':'Parameter, phase, polynomial coefficient, chain-rule and time-normalization controls; published Theorem A supplies global monotonicity.'}
(r/'independent_checks.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,sort_keys=True))
