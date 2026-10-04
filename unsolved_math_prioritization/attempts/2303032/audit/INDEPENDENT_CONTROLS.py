#!/usr/bin/env python3
"""Independent exact algebra/negative controls. Not an analytic proof checker."""
import json
from fractions import Fraction as F

# Sparse polynomials in n,a,p,e. Coefficients and equality are exact.
class P:
    def __init__(self, terms=0):
        self.t = terms if isinstance(terms, dict) else ({(0,0,0,0): F(terms)} if terms else {})
        self.t = {k:F(v) for k,v in self.t.items() if v}
    def __add__(self, other):
        other = other if isinstance(other,P) else P(other)
        out = self.t.copy()
        for k,v in other.t.items(): out[k]=out.get(k,F(0))+v
        return P(out)
    __radd__ = __add__
    def __neg__(self): return P({k:-v for k,v in self.t.items()})
    def __sub__(self, other): return self + (-other if isinstance(other,P) else -P(other))
    def __rsub__(self, other): return P(other)-self
    def __mul__(self, other):
        other=other if isinstance(other,P) else P(other)
        out={}
        for k,v in self.t.items():
            for l,w in other.t.items():
                m=tuple(x+y for x,y in zip(k,l));out[m]=out.get(m,F(0))+v*w
        return P(out)
    __rmul__=__mul__
    def __eq__(self, other): return self.t==(other.t if isinstance(other,P) else P(other).t)

n,a,p,e=[P({tuple(int(i==j) for i in range(4)):1}) for j in range(4)]
checks=[]
def check(name, condition):
    assert condition, name
    checks.append(name)
check('branch_difference_symbolic', n*(a-1)-(n+a-2)==(n-1)*(a-2))
b=-(a+n-2)
check('cone_characteristic_root_symbolic', b*(b+n-2)==a*(a+n-2))
check('whitney_weight_symbolic_after_multiplying_by_p', p*(a-2)+(p*(2-a)-n*(p-1))==-n*(p-1))
check('holder_boundary_criterion_symbolic', (a-2+e)*p-(1-p)==(a-1+e)*p-1)
m=n+2
check('quadratic_kelvin_laplacian_symbolic',m*(m-n-2)==0)
check('quadratic_laplacian_symbolic',2*(n-1)-2*(n-1)==0)
check('cone_endpoint_radial_degree_symbolic',n-1-n==-1)
for nn in (2,3,4,17,101):
    aa=F(3); cutoff=1/(aa-1); cone=F(nn,nn+aa-2)
    check(f'a3_dimension{nn}_cone_is_weaker',cutoff<cone)
    check(f'a3_dimension{nn}_cone_integrable_at_smaller_endpoint',nn-1-cutoff*(aa+nn-2)>-1)
    check(f'dimension{nn}_a2_common_endpoint',F(nn,nn+2-2)==F(1))
    check(f'dimension{nn}_smooth_endpoint_radial_degree',nn-1-F(nn,nn-1)*(nn-1)==-1)
check('reject_bad_sign_branch',F(1,1-3)<0<F(1,3-1))
check('reject_bad_whitney_scaling',F(3,2)/3-3 != F(3,1)/F(3,2)-3)
# theta/pi=1/6 in the planar angle formula gives a=3 exactly.
check('planar_angle_ratio_control',1/(2*F(1,6))==3)
# At p=1/(a-1), the Holder boundary exponent is >1 for every e>0.
for aa in (F(2),F(21,10),F(3),F(100)):
    pp=1/(aa-1)
    for ee in (F(1,10000),F(1,7),F(3)):
        check(f'reject_holder_endpoint_a{aa}_e{ee}',(aa-1+ee)*pp>1)
# Exact tangent circle check, t=1, sin(theta)=3/5, cos(theta)=4/5.
s,c=F(3,5),F(4,5); rr,zz=s*c,c*c
check('capped_cone_tangent_point_on_sphere',rr*rr+(zz-1)*(zz-1)==s*s)
check('capped_cone_tangency_orthogonality',rr*rr+zz*(zz-1)==0)
print(json.dumps({'result':'passed','total_assertions':len(checks),'checks':checks,
'limits':['Symbolic identities certify only the displayed polynomial algebra.',
'Rational examples are negative/transcription controls, not proofs of analytic hypotheses.',
'No cone eigenvalues, Green estimates, boundary regularity, or a>2 optimality are computed.']},indent=2))
