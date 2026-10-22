#!/usr/bin/env python3
"""Finite exact controls only; does not verify Leung's general theorem."""
from fractions import Fraction as Q
import json
from pathlib import Path

ZERO = (Q(0), Q(0))
ONE = (Q(1), Q(0))

def add(a, b): return (a[0]+b[0], a[1]+b[1])
def neg(a): return (-a[0], -a[1])
def sub(a, b): return add(a, neg(b))
def mul(a, b): return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])
def scale(a, q): return (a[0]*q, a[1]*q)
def norm2(a): return a[0]**2+a[1]**2
def div(a, b):
    d = norm2(b)
    assert d > 0
    return scale(mul(a, (b[0], -b[1])), Q(1)/d)
def power(a, n):
    r = ONE
    for _ in range(n): r = mul(r, a)
    return r

def modulus_gap_le_one(a, b):
    A, B = norm2(a), norm2(b)
    T = A+B-1
    return T <= 0 or T*T <= 4*A*B

def unit(t):
    return ((1-t*t)/(1+t*t), 2*t/(1+t*t))

def run():
    counts = {}
    def check(group, condition):
        if not condition: raise AssertionError(group)
        counts[group] = counts.get(group, 0)+1
    units = [unit(Q(t)) for t in [-3,-2,-1,Q(-1,2),0,Q(1,2),1,2,3]] + [(-Q(1),Q(0))]
    for g in units: check('unit_circle_exact', norm2(g)==1)
    zs = [(Q(a,4),Q(b,4)) for a in range(-3,4) for b in range(-3,4) if a*a+b*b<16]
    for g in units:
        for h in units:
            coeff = [ZERO,ONE]
            for n in range(1,33):
                coeff.append(sub(mul(add(g,h),coeff[n]),mul(mul(g,h),coeff[n-1])))
                check('two_pole_modulus_gap', modulus_gap_le_one(coeff[n+1],coeff[n]))
                if n <= 8:
                    # An independent convolution formula at low degree.
                    expected = ZERO
                    for j in range(n+1): expected=add(expected,mul(power(g,j),power(h,n-j)))
                    check('recurrence_convolution_match', coeff[n+1]==expected)
            for z in zs:
                den=mul(sub(ONE,mul(g,z)),sub(ONE,mul(h,z)))
                p=div(sub(ONE,mul(mul(g,h),mul(z,z))),den)
                cg=div(add(ONE,mul(g,z)),sub(ONE,mul(g,z)))
                ch=div(add(ONE,mul(h,z)),sub(ONE,mul(h,z)))
                check('logarithmic_derivative_identity',p==scale(add(cg,ch),Q(1,2)))
                check('positive_real_part',p[0]>0)
                check('cayley_real_identity',cg[0]==(1-norm2(z))/norm2(sub(ONE,mul(g,z))))
            # Exact cross-product factorization for distinct interior test points.
            for z,w in zip(zs,zs[1:]):
                dz=mul(sub(ONE,mul(g,z)),sub(ONE,mul(h,z)))
                dw=mul(sub(ONE,mul(g,w)),sub(ONE,mul(h,w)))
                lhs=sub(mul(z,dw),mul(w,dz))
                rhs=mul(sub(z,w),sub(ONE,mul(mul(g,h),mul(z,w))))
                check('injectivity_factorization',lhs==rhs and norm2(rhs)>0)
    # Exact all-index formulas evaluated on a declared finite range.
    for n in range(1,257):
        check('koebe_sharpness',abs((n+1)-n)==1)
        odd=lambda m: 1 if m%2 else 0
        check('odd_two_sided_sharpness',abs(odd(n+1)-odd(n))==1)
        check('odd_signed_direction',odd(n+1)-odd(n)==(-1 if n%2 else 1))
        third=lambda m: (1,-1,0)[(m-1)%3]
        check('third_root_recurrence',third(n+2)+third(n+1)+third(n)==0)
        check('third_root_gap',abs(abs(third(n+1))-abs(third(n)))<=1)
    for g in units:
        for n in range(1,33):
            a=(Q(n),Q(0)); b=(Q(n+1),Q(0))
            check('rotation_invariance',modulus_gap_le_one(mul(a,power(g,n-1)),mul(b,power(g,n))))
    check('identity_n1_endpoint',modulus_gap_le_one(ZERO,ONE) and abs(0-1)==1)
    check('raw_coefficient_difference_rejected',abs(-1-1)>1 and abs(abs(-1)-abs(1))==0)
    check('missing_normalization_rejected',not modulus_gap_le_one((Q(4),Q(0)),(Q(2),Q(0))))
    check('outside_bound_rejected',not modulus_gap_le_one((Q(1001,1000),Q(0)),ZERO))
    check('boundary_accepted',modulus_gap_le_one(ONE,ZERO))
    # Equality at n=1 does not force the two-pole form: the identity's a2=a3=0
    # would require g+h=0 and gh=0 by the recurrence, impossible on the unit circle.
    check('identity_not_two_pole',all(not(add(g,h)==ZERO and mul(g,h)==ZERO) for g in units for h in units))
    return {'schema_version':1,'arithmetic':'fractions.Fraction only','scope':'finite controls; not a proof of the full historical theorem','unit_parameters':len(units),'interior_parameters':len(zs),'coefficient_indices_per_pair':32,'counts':counts,'total_assertions':sum(counts.values()),'all_passed':True}

if __name__=='__main__':
    result=run()
    expected_path=Path(__file__).with_name('EXPECTED_CHECKS.json')
    if expected_path.exists():
        assert result==json.loads(expected_path.read_text()), 'Stored controls do not match replay'
    print(json.dumps(result,indent=2,sort_keys=True))
