#!/usr/bin/env python3
"""Independent exact arithmetic: range-reduced alternating Taylor intervals.

This does not import or execute the author's certificate. All acceptance
comparisons are rational. Analytic implications are reviewed in AUDIT.md.
"""
from fractions import Fraction as F
import json
import sys

GRID = 200
ROUND_LIMIT = F(129, 200)
LENGTH = 10000
SCALE = 10**24


def require(condition, message):
    if not condition:
        raise ValueError(message)


def down(x):
    return F(x.numerator * SCALE // x.denominator, SCALE)


def up(x):
    return F(-((-x.numerator * SCALE) // x.denominator), SCALE)


def negative_exp_interval(x):
    require(F(0) <= x <= 64, 'exponential argument range')
    y = x / 512
    require(y <= F(1, 8), 'range-reduced argument')
    term = F(1)
    total = term
    for k in range(1, 16):
        term *= -y / k
        total += term
    low = down(total)  # degree 15 is an alternating-series lower bound
    term *= -y / 16
    high = up(total + term)  # degree 16 is an upper bound
    require(0 <= low <= high <= 1, 'initial positive exponential interval')
    for _ in range(9):
        low, high = down(low * low), up(high * high)
    require(0 <= low <= high <= 1, 'squared exponential interval')
    return low, high


def sqrt_interval(x):
    # Integer bisection, deliberately independent of math.isqrt.
    scale = 10**10
    a, b = 0, 2 * scale
    require(F(b*b, scale*scale) >= x, 'square root search range')
    while b-a > 1:
        mid = (a+b)//2
        if F(mid*mid, scale*scale) <= x:
            a = mid
        else:
            b = mid
    lo, hi = F(a, scale), F(b, scale)
    require(lo*lo <= x < hi*hi, 'square root bracket')
    return lo, hi


def arctan_interval(x):
    total = sum(((-1)**k * x**(2*k+1) / (2*k+1)
                 for k in range(30)), F(0))
    return total, total + x**61/61


def decimal(x, direction):
    scale=10**15
    q=x.numerator*scale//x.denominator
    if direction=='up':
        q += 1
    return f'{q//scale}.{q%scale:015d}'


def calculate():
    # arctan(1/2)+arctan(1/3)=pi/4 by the tangent addition formula.
    a,b=arctan_interval(F(1,2)), arctan_interval(F(1,3))
    pi_lo,pi_hi=4*(a[0]+b[0]),4*(a[1]+b[1])
    require(F(157,50)<pi_lo<pi_hi<F(22,7),'pi interval')
    sqlo,sqhi=F(1772,1000),F(1773,1000)
    require(sqlo**2<pi_lo and pi_hi<sqhi**2,'sqrt(pi) enclosure')
    e_term=e_sum=F(1)
    for k in range(1,21):
        e_term /= k
        e_sum += e_term
    e_high=e_sum+(e_term/21)/(1-F(1,22))
    require(e_high<F(2719,1000),'e enclosure')
    require(2*pi_lo**2>1,'negative Poisson correction for t<=1')
    require(sqhi/3<ROUND_LIMIT,'small-time round bound')
    require(F(36,25)/12<F(1,2),'tail ratio for j>=5 at t>=1')

    cells=[]
    for k in range(GRID,2*GRID):
        a,b=F(k,GRID),F(k+1,GRID)
        pref=b*sqrt_interval(b)[1]
        # Four exact spherical modes, followed by a geometric tail at j=5.
        partial=sum((j*j*negative_exp_interval(a*(j*j-F(1,4)))[1]
                    for j in range(1,5)),F(0))
        tail=50*negative_exp_interval(a*F(99,4))[1]
        upper=pref*(partial+tail)
        require(upper<ROUND_LIMIT,'round interval bound')
        cells.append((upper,k))
    worst,k=max(cells)
    lower=F(1772,2719)*(LENGTH-4*sqhi)/(LENGTH+4)
    require(LENGTH>4*sqhi,'positive Gaussian integral lower bound')
    require(lower>F(13,20)>ROUND_LIMIT,'strict cylinder separation')
    # An independent lower bound at t=2 ensures literal round maximum exists.
    two_first=2*sqrt_interval(F(2))[0]*negative_exp_interval(F(3,2))[0]
    require(two_first>sqhi/4,'round value exceeds normalized Weyl limit')
    require(sqhi/4<F(13,20),'cylinder value exceeds normalized Weyl limit')
    return {
      'problem_id':30001168,'accepted':True,'grid_cells':GRID,
      'round_grid_upper_decimal':decimal(worst,'up'),
      'round_grid_worst_interval':[str(F(k,GRID)),str(F(k+1,GRID))],
      'cylinder_rational_lower':str(lower),
      'cylinder_lower_decimal':decimal(lower,'down'),
      'round_time_2_first_mode_lower_decimal':decimal(two_first,'down'),
      'round_all_time_threshold':'129/200','cylinder_strict_threshold':'13/20',
      'method':'Exact fractions; alternating exponential Taylor bounds with range reduction and outward rounding; integer bisection square roots; 200 intervals; four modes plus rigorously bounded tail',
      'scope':'Arithmetic only; the analytic proof is audited separately.'
    }


if __name__=='__main__':
    require(len(sys.argv)==1,'No arguments accepted')
    print(json.dumps(calculate(),indent=2,sort_keys=True))
