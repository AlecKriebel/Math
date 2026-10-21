#!/usr/bin/env python3
"""Independent finite exact checks; not a proof of the all-order theorem.

Only the Python standard library is used. All checks use explicit exceptions,
so Python optimization cannot remove them. Run with --output <JSON path>.
"""
from fractions import Fraction as F
from itertools import permutations
from math import comb
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import sys


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def trim(p):
    p = [F(v) for v in p]
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def add(p, q):
    return trim([(p[k] if k < len(p) else 0) +
                 (q[k] if k < len(q) else 0)
                 for k in range(max(len(p), len(q)))])


def scale(p, s):
    return trim([s * v for v in p])


def mul(p, q):
    a = [F(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            a[i+j] += x*y
    return trim(a)


def power(p, k):
    require(k >= 0, 'negative polynomial exponent')
    result = [F(1)]
    while k:
        if k % 2:
            result = mul(result, p)
        p = mul(p, p)
        k //= 2
    return result


def compose(p, q):
    result = [F(0)]
    for c in reversed(p):
        result = add(mul(result, q), [c])
    return result


def evaluate(p, x):
    result = F(0)
    for c in reversed(p):
        result = result*x+c
    return result


def integrate(p, lo=F(0), hi=F(1), shift=0):
    return sum((c*(hi**(j+shift+1)-lo**(j+shift+1))/
                (j+shift+1) for j, c in enumerate(p)), F(0))


def kernel_chebyshev(m):
    require(m >= 1, 'kernel requires m>=1')
    old, current = [F(1)], [F(1), F(-2)]
    total = add(old, scale(current, 2))
    for k in range(2, m+1):
        old, current = current, add(scale(mul([1, -2], current), 2), scale(old, -1))
        total = add(total, scale(current, 2))
    return scale(total, F(1, 2*m+1))


def kernel_binomial(m):
    # Imaginary part of (cos(v)+i sin(v))^(2m+1), divided by sin(v).
    result = [F(0)]
    for j in range(m+1):
        term = [F(0)]*j + scale(power([1, -1], m-j), (-1)**j*comb(2*m+1, 2*j+1))
        result = add(result, term)
    return scale(result, F(1, 2*m+1))


def moment(a, b, c):
    if a % 2 or b % 2:
        return F(0)
    return F(4, (a+1)*(b+1)*(a+b+c+3))


def transformed_moment(a, b, c):
    # x=s*u,y=s*v,z=s, Jacobian s^2; integrate over [-1,1]^2 x [0,1].
    iu = (F(1)-F(-1)**(a+1))/(a+1)
    iv = (F(1)-F(-1)**(b+1))/(b+1)
    return iu*iv/F(a+b+c+3)


def indices(r):
    return [(a, b, d-a-b) for d in range(r+1)
            for a in range(d+1) for b in range(d-a+1)]


def matrix(r, z_shift):
    ix = indices(r)
    return [[moment(a[0]+b[0], a[1]+b[1], a[2]+b[2]+z_shift)
             for b in ix] for a in ix]


def positive_ldl(a):
    n = len(a)
    l = [[F(0)]*n for _ in range(n)]
    d = []
    for i in range(n):
        l[i][i] = F(1)
        pivot = a[i][i]-sum((l[i][k]**2*d[k] for k in range(i)), F(0))
        require(pivot > 0, f'nonpositive LDL pivot at {i}: {pivot}')
        d.append(pivot)
        for j in range(i+1, n):
            l[j][i] = (a[j][i]-sum((l[j][k]*l[i][k]*d[k] for k in range(i)), F(0)))/pivot
    # Full exact reconstruction is an additional independent consistency check.
    for i in range(n):
        for j in range(n):
            require(a[i][j] == sum((l[i][k]*d[k]*l[j][k]
                                   for k in range(min(i,j)+1)), F(0)), 'LDL reconstruction')
    return d


def determinant_polynomial(a):
    n = len(a)
    total = [F(0)]
    for perm in permutations(range(n)):
        inversions = sum(perm[i] > perm[j] for i in range(n) for j in range(i+1, n))
        term = [F((-1)**inversions)]
        for i in range(n):
            term = mul(term, a[i][perm[i]])
        total = add(total, term)
    return total


def check_shell_exponent(n, exponent):
    require(exponent > n+1, 'dyadic geometric bound does not converge')


def check_witness_degree(n, r, m):
    require(2*m*(n+2) <= r, 'root polynomial exceeds hierarchy order')


def expect_failure(fn, name):
    try:
        fn()
    except RuntimeError:
        return name
    raise RuntimeError('negative control did not reject '+name)


def run_checks():
    counts = {}
    for m in range(1, 17):
        a = kernel_chebyshev(m)
        require(a == kernel_binomial(m), 'independent kernel identities disagree')
        require(len(a)-1 == m, 'wrong kernel degree')
        require(evaluate(a,F(0)) == 1, 'kernel endpoint zero')
        require(evaluate(a,F(1)) == F((-1)**m,2*m+1), 'kernel endpoint one')
    counts['exact_kernel_polynomial_identities'] = 16
    counts['rational_envelope_grid'] = 0
    counts['rational_core_grid'] = 0
    for m in range(1,13):
        a = kernel_chebyshev(m)
        n2 = (2*m+1)**2
        for j in range(128):
            t = F(j,127)
            v = evaluate(a,t)
            require(v*v <= 1, 'unit envelope failure')
            require(n2*t*v*v <= 1, 'tail envelope failure')
            counts['rational_envelope_grid'] += 1
        for j in range(65):
            t = F(j,64*n2)
            # 226/355 < 2/pi from pi < 355/113; finite test is deliberately weaker.
            require(evaluate(a,t) >= F(226,355), 'rational core lower bound failure')
            counts['rational_core_grid'] += 1
    counts['degree_integer_cases'] = 0
    for n in range(1,21):
        ell = n+2
        for r in range(1,1001):
            if r >= 2*ell:
                m = r//(2*ell)
                check_witness_degree(n,r,m)
                require(2*m+1 >= F(r,2*ell), 'floor comparison')
            else:
                require(F(4*ell*ell,r*r) > 1, 'small-order constant comparison')
            counts['degree_integer_cases'] += 1
    shell_records = []
    for n in range(1,6):
        ell = n+2
        check_shell_exponent(n,ell)
        for p in range(1,n+1):
            for m in range(1,5):
                q = power(kernel_chebyshev(m),2*ell)
                h = F(1,(2*m+1)**2)
                denom = p*integrate(q,shift=p-1)
                num = p*integrate(q,shift=p)
                core_d = p*integrate(q,hi=h,shift=p-1)
                core_n = p*integrate(q,hi=h,shift=p)
                require(denom > 0 and 0 < num < denom, 'power-law normalization')
                require(core_d >= F(226,355)**(2*ell)*h**p, 'exact core integral')
                require(core_n <= h**(p+1), 'exact core numerator')
                total_d,total_n = core_d,core_n
                j = 0
                while 2**j*h < 1:
                    lo,hi = 2**j*h,min(F(1),2**(j+1)*h)
                    d = p*integrate(q,lo,hi,shift=p-1)
                    v = p*integrate(q,lo,hi,shift=p)
                    endpoint_f = min(F(1),2**(j+1)*h)**p
                    bound = 2**(j+1)*h*F(1,2**(j*ell))*endpoint_f
                    relative_bound = h**(p+1)*2**(n+1)*F(1,2**j)
                    require(0 <= v <= bound <= relative_bound, 'dyadic shell bound')
                    total_d,total_n = total_d+d,total_n+v
                    j += 1
                require(total_d == denom and total_n == num, 'mass omitted in shell partition')
                require(num <= (1+2**(n+2))*h**(p+1), 'summed exact numerator bound')
                # Independent Stieltjes/Tonelli calculation in the audit report.
                require(num <= ((n+1)*h-n*h*h)*h**p,
                        'independent integration-by-parts numerator bound')
                shell_records.append({'n':n,'cumulative_power':p,'m':m,
                                      'normalization':str(denom),'objective':str(num/denom),
                                      'N_squared_objective':str(num/denom/h),
                                      'alternative_numerator_bound':str(((n+1)*h-n*h*h)*h**p)})
    counts['exact_power_law_all_mass_shell_cases'] = len(shell_records)
    counts['pyramid_monomial_moments'] = 0
    for a in range(9):
        for b in range(9):
            for c in range(7):
                require(moment(a,b,c) == transformed_moment(a,b,c), 'pyramid moment mismatch')
                counts['pyramid_monomial_moments'] += 1
    require(moment(0,0,0) == F(4,3), 'pyramid volume')
    ldl_records = []
    for r in range(5):
        h,z = matrix(r,0),matrix(r,1)
        hz = [[h[i][j]-z[i][j] for j in range(len(h))] for i in range(len(h))]
        record={'r':r,'dimension':len(h)}
        for name,a in [('H',h),('Z',z),('H_minus_Z',hz)]:
            pivots=positive_ldl(a)
            record[name+'_pivots']=[str(v) for v in pivots]
        ldl_records.append(record)
    counts['exact_positive_definite_matrices'] = 15
    # r=1 basis order is [1,z,y,x]; parity makes the last two modes scalar.
    h,z = matrix(1,0),matrix(1,1)
    characteristic = determinant_polynomial([[[z[i][j],-h[i][j]]
                                             for j in range(4)] for i in range(4)])
    expected = mul(power([F(2,9),F(-4,15)],2),[F(2,75),F(-4,45),F(1,15)])
    require(characteristic == expected, 'pyramid r=1 characteristic determinant')
    pyramid_witnesses=[]
    for m in range(1,7):
        q=power(kernel_chebyshev(m),10)
        require(len(q)-1 == 10*m, 'linear pyramid witness degree')
        denom=4*integrate(q,shift=2)
        num=4*integrate(q,shift=3)
        require(denom > 0 and F(0) < num/denom < 1, 'pyramid all-mass witness')
        for t in [F(-7),F(-1),F(2),F(5)]:
            require(evaluate(q,t) >= 0, 'global square sample outside K')
        pyramid_witnesses.append({'m':m,'hierarchy_order':5*m,
                                  'normalization':str(denom),'objective':str(num/denom)})
    counts['exact_pyramid_witnesses'] = 6
    families = [
        ('affine_boundary',[0,1],[0,F(1,2),F(1,2)],2,F(0),F(1)),
        ('interior_stationary',[F(1,4),-1,1],[1,-4,4],F(1,2),F(0),F(1)),
        ('vanishing_hessian',[0,0,0,0,1],[0,0,1],7,F(-1),F(1)),
        ('nonconvex_boundary',[0,1,-1],[0,1,2],1,F(0),F(1,2)),
        ('constant_objective',[0],[0,0,1],1,F(0),F(1)),
    ]
    family_records=[]
    for name,f,u,g,lo,hi in families:
        for m in range(1,5):
            q=power(compose(kernel_chebyshev(m),u),6)
            d=integrate(q,lo,hi)
            v=integrate(mul(f,q),lo,hi)
            proxy=integrate(mul(u,q),lo,hi)*g
            require(d > 0 and 0 <= v <= proxy, 'quadratic-proxy family')
            require(len(q)-1 <= 12*m,'quadratic proxy degree')
            family_records.append({'family':name,'m':m,'objective':str(v/d),
                                   'proxy_objective':str(proxy/d),'degree':len(q)-1})
    counts['exact_proxy_family_cases']=len(family_records)
    controls=[]
    controls.append(expect_failure(lambda:check_shell_exponent(3,4),'critical_exponent_L_equals_n_plus_1'))
    controls.append(expect_failure(lambda:check_witness_degree(3,9,1),'insufficient_degree_r_equals_2L_minus_1'))
    controls.append(expect_failure(lambda:require(evaluate(power(kernel_chebyshev(1),9),F(1)) >= 0,
                                                  'odd exponent is negative'), 'odd_exponent_is_not_global_nonnegative'))
    snapshot=Path(__file__).resolve().parents[2]/'SUBMITTED_SNAPSHOT.json'
    submitted_check=[]
    for entry in json.loads(snapshot.read_text())['files']:
        body=(snapshot.parent/entry['local']).read_bytes()
        digest=hashlib.sha256(body).hexdigest()
        require(len(body)==entry['bytes'] and digest==entry['sha256'],'submitted snapshot mismatch')
        submitted_check.append({'path':entry['local'],'bytes':len(body),'sha256':digest})
    return {'status':'PASS_FINITE_EXACT_CHECKS','run_utc':datetime.now(timezone.utc).isoformat(),
            'python':sys.version,'optimization':sys.flags.optimize,
            'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'counts':counts,'negative_controls_rejected':controls,
            'pyramid_r1_characteristic_coefficients':[str(c) for c in characteristic],
            'pyramid_r1_minimum':'(10-sqrt(10))/15',
            'pyramid_ldl':ldl_records,'pyramid_witnesses':pyramid_witnesses,
            'power_law_cases':shell_records,'quadratic_proxy_cases':family_records,
            'submitted_snapshot_verified':submitted_check,
            'limits':'Finite exact arithmetic checks supplement, but do not prove, the independent analytic argument.'}


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    result=run_checks()
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'optimization':result['optimization'],
                      'counts':result['counts'],'negative_controls_rejected':result['negative_controls_rejected'],
                      'output':str(Path(args.output).resolve())},indent=2))
