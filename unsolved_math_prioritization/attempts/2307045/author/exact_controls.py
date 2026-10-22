#!/usr/bin/env python3
"""Finite algebraic controls; does not prove the global slit comparison."""
from fractions import Fraction as F
from pathlib import Path
import argparse
import cmath
import json
import math


def add(z, w):
    return z[0] + w[0], z[1] + w[1]


def sub(z, w):
    return z[0] - w[0], z[1] - w[1]


def mul(z, w):
    return z[0]*w[0] - z[1]*w[1], z[0]*w[1] + z[1]*w[0]


def norm2(z):
    return z[0]*z[0] + z[1]*z[1]


def div(z, w):
    a, b = mul(z, (w[0], -w[1]))
    d = norm2(w)
    assert d > 0
    return a/d, b/d


ONE, ZERO = (F(1), F(0)), (F(0), F(0))


def run():
    counts = {}
    count = 0
    # Disk automorphism identity, exact over rational complex coordinates.
    for m in range(1, 10):
        a = F(m, 10)
        for j in range(-9, 10):
            for k in range(-9, 10):
                w = (F(j, 10), F(k, 10))
                if norm2(w) >= 1:
                    continue
                num = sub(w, (a, F(0)))
                den = sub(ONE, mul((a, F(0)), w))
                assert norm2(den)-norm2(num) == (1-a*a)*(1-norm2(w))
                assert norm2(div(num, den)) < 1
                count += 1
    counts['disk_automorphism_rational_points'] = count
    count = 0
    for m in range(1, 10):
        a = F(m, 10)
        for k in range(11):
            w = a+(1-a)*F(k, 10)
            v = (w-a)/(1-a*w)
            assert 0 <= v <= 1
            assert (v == 0) == (k == 0)
            assert (v == 1) == (k == 10)
            count += 1
    counts['slit_endpoint_and_order_checks'] = count
    count = 0
    for j in range(-9, 10):
        for k in range(1, 10):
            s = (F(j, 10), F(k, 10))
            if norm2(s) >= 1:
                continue
            den = sub(ONE, s)
            q = div(add(ONE, s), den)
            assert q[0] == (1-norm2(s))/norm2(den)
            assert q[1] == 2*s[1]/norm2(den)
            assert q[0] > 0 and q[1] > 0
            count += 1
    counts['quadrant_map_rational_points'] = count
    count = 0
    for m in range(1, 10):
        t = F(m, 10)
        s = ((1-t*t)/(1+t*t), 2*t/(1+t*t))
        assert norm2(s) == 1
        q = div(add(ONE, s), sub(ONE, s))
        assert q[0] == 0 and q[1] > 0
        x = (F(m-5, 10), F(0))
        qx = div(add(ONE, x), sub(ONE, x))
        assert qx[1] == 0 and qx[0] > 0
        count += 1
    counts['boundary_component_checks'] = count
    count = 0
    for m in range(1, 10):
        s = F(m, 10)
        a = s*s
        assert div(sub(ZERO, (a,F(0))), sub(ONE, mul((a,F(0)),ZERO))) == (-a,F(0))
        assert mul((F(0),s),(F(0),s)) == (-a,F(0))
        q = div((F(1),s),(F(1),-s))
        assert q == ((1-s*s)/(1+s*s),2*s/(1+s*s))
        assert q[1]/q[0] == 2*s/(1-s*s)
        count += 1
    counts['evaluation_point_and_double_angle_checks'] = count
    count = 0
    for m in range(1, 16):
        r = F(m,16)
        for p in range(1,13):
            assert 0 < r**p < 1
            assert r**(p+1) < r**p
            if m < 15:
                assert r**p < F(m+1,16)**p
            count += 1
    counts['positive_power_monotonicity_checks'] = count
    # Exact arithmetic in Q(sqrt(2)): r = sqrt(2)-1 satisfies
    # r^2 + 2r - 1 = 0, the identity behind tan(pi/8) = r.
    def q2mul(x,y):
        return (x[0]*y[0]+2*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
    r = (F(-1),F(1))
    rr = q2mul(r,r)
    assert (rr[0]+2*r[0]-1,rr[1]+2*r[1]) == (0,0)
    counts['quadratic_field_half_value_check'] = 1
    errors = []
    for p in (1,2,3,5,8):
        for r in (0.01,0.1,0.5,0.9,0.999):
            s = r**(p/2)
            a = 4/math.pi*math.atan(s)
            b = 2/math.pi*cmath.phase((1+1j*s)/(1-1j*s))
            errors.append(abs(a-b))
            assert abs(a-b) < 1e-13
            assert 0 < a < 1
    half_error = abs(4/math.pi*math.atan(math.sqrt(2)-1)-0.5)
    assert half_error < 1e-13
    return {
        'problem_id':'2307045',
        'exact_control_groups':counts,
        'exact_control_instances':sum(counts.values()),
        'exact_arithmetic':'Python fractions.Fraction; all checks above exact',
        'numerical_controls':{
            'configuration_values_checked':len(errors),
            'max_formula_disagreement':max(errors),
            'half_value_error':half_error,
            'tolerance':1e-13,
            'status':'sanity checks only; not interval certificates'},
        'scope':'Finite controls for authored conformal-value calculation; not a proof of Dubinin comparison',
        'result':'PASS'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true')
    args = parser.parse_args()
    result = run()
    path = Path(__file__).with_name('EXACT_RESULTS.json')
    if args.check:
        expected = json.loads(path.read_text())
        # Numerical last bits may vary by libm; test them above, and compare
        # their stated precision rather than hardcoding a floating bit pattern.
        for key in ('max_formula_disagreement','half_value_error'):
            assert expected['numerical_controls'][key] < 1e-13
            result['numerical_controls'][key] = expected['numerical_controls'][key]
        assert result == expected, 'Recorded controls differ from replay'
        print('PASS: exact controls and bounded numerical sanity replay')
    else:
        path.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result,indent=2))
