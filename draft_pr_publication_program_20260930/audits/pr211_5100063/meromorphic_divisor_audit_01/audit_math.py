#!/usr/bin/env python3.11
"""Authored PR211 meromorphic audit. No network, git, or source-body writes.

Writes only JSON results beside this script. Sympy computations are exact
polynomial identities. mpmath diagnostics are finite, noninterval evidence.
"""
import datetime
import hashlib
import json
import math
from pathlib import Path
import platform
import sys

SITE = '/Users/alec/Library/Python/3.11/lib/python/site-packages'
if SITE not in sys.path:
    sys.path.insert(0, SITE)
import sympy as S
import mpmath as mp

BASE = Path(__file__).resolve().parent


def symbolic():
    k, t, s, h, C, d, e, n, kp, alpha = S.symbols(
        'k t s h C d e n kp alpha', nonzero=True)
    q, d2 = 1-t, 1-k*k*t
    U, V, W = 1-2*k*k*t+k*k*t*t, 1-2*t+k*k*t*t, 1-k*k*t*t
    D = 1-k*k*t*s*s
    relations = [(h, t), (C, q), (d, d2), (e, 1-s*s),
                 (n, 1-k*k*s*s), (kp, 1-k*k)]
    checks = {}

    def reduce(expr):
        out = S.cancel(expr).as_numer_denom()[0]
        for var, val in relations:
            out = S.rem(S.Poly(out, var), S.Poly(var*var-val, var)).as_expr()
        return S.factor(out)

    def check(name, expr):
        remainder = reduce(expr)
        checks[name] = {'zero_remainder': remainder == 0,
                        'remainder': str(remainder)}
        if remainder != 0:
            raise AssertionError((name, remainder))

    sm, sp = (s*C*d-h*e*n)/D, (s*C*d+h*e*n)/D
    cm, cp = (e*C+s*h*n*d)/D, (e*C-s*h*n*d)/D
    check('addition_sn_sum', sm+sp-2*s*C*d/D)
    check('addition_sn_product', sm*sp-(s*s-t)/D)
    check('outer_tangent_minus', d*s*sm/C+e*cm/C-1)
    check('outer_tangent_plus', d*s*sp/C+e*cp/C-1)
    check('tangent_determinant', sp*cm-sm*cp-2*h*C*n/D)
    A, B = alpha*d*d/q, alpha*kp/q
    check('outer_confocal_input', (alpha*d/C)**2-(alpha*kp/C)**2-(alpha*k)**2)
    check('distance_factor', q*q*((-A*s-alpha*k)**2+(B*e)**2)
          -alpha**2*(1+k*s)*(U+k*V*s))
    check('factor_one', (1+k*sm)*(1+k*sp)-(d+k*C*s)**2/D)
    L0, L1 = (U*U-k*k*V*V*t)/d, (V*V-U*U*t)/C
    check('mixed_coefficient', d*L1+C*L0-2*U*V*C*d)
    check('factor_two', (U+k*V*sm)*(U+k*V*sp)
          -(d+k*C*s)*(L0+k*L1*s)/D)
    rawdet = ((-A*sm-alpha*k)*(B*cp)-(B*cm)*(-A*sp-alpha*k))/2
    detform = alpha*B*h*d*n*(d+k*C*s)/(C*D)
    check('exact_translated_determinant', rawdet-detform)
    C0 = B*h*d*q**4/(alpha**3*C)
    factored_distance_product = alpha**4/q**4*(d+k*C*s)**3*(L0+k*L1*s)/D**2
    check('edge_normalization_q4', detform/factored_distance_product
          -C0*n*D/((d+k*C*s)**2*(L0+k*L1*s)))
    Z = W*W-4*k*k*t*t*q*d2
    D3, C3 = U*W-2*k*k*t*q*V, V*W-2*t*d2*U
    check('triple_dn_polynomial', U*U-k*k*V*V*t-d2*D3)
    check('triple_cn_polynomial', V*V-U*U*t-q*C3)
    check('triple_L0', L0-Z*d*D3/Z)
    check('triple_L1', L1-Z*C*C3/Z)
    check('triple_positive_norm', L0*L0-k*k*L1*L1-(1-k*k)*Z*Z)
    check('first_positive_norm', d*d-k*k*C*C-(1-k*k))
    check('first_pole_D_value', (1-k*k*t*(-d/(k*C))**2)-V/q)
    check('first_pole_B_value', L0-d*L1/C-4*(1-k*k)*t*d*W)
    # Quarter-shift gives dn(r0+v)=i*kp*h/C and A'(r0+v)=-kp^2*h/C.
    a2 = C0*(S.I*kp*h/C)*(V/q)/((kp**4*t/q)*(4*kp**2*t*d*W))
    a2simple = S.I*V*q*q/(4*alpha**2*kp**4*t*W)
    check('double_laurent_coefficient', a2-a2simple)
    return {'kind': 'exact symbolic polynomial reductions',
            'assumed_relations': [str(x*x-y) for x,y in relations],
            'not_claimed': 'This computation alone does not prove the elliptic divisor argument.',
            'checks': checks, 'all_passed': all(x['zero_remainder'] for x in checks.values())}


def numeric():
    mp.mp.dps = 100
    rows, pole_rows, boundary_rows = [], [], []
    metrics = {}

    def record(name, error):
        metrics[name] = max(metrics.get(name, mp.mpf(0)), abs(error))

    def rel(a,b):
        return abs(a-b)/max(mp.mpf(1),abs(a),abs(b))

    def setup(k, N, tau):
        m, kp = k*k, mp.sqrt(1-k*k)
        K, Kp = mp.ellipk(m), mp.ellipk(1-m)
        v, delta = 2*K*tau/N, 4*K*tau/N
        sn = lambda x: mp.ellipfun('sn',x,m)
        cn = lambda x: mp.ellipfun('cn',x,m)
        dn = lambda x: mp.ellipfun('dn',x,m)
        h,C,d = sn(v),cn(v),dn(v)
        t,q = h*h,C*C
        U,V,W = 1-2*m*t+m*t*t,1-2*t+m*t*t,1-m*t*t
        Z = W*W-4*m*t*t*q*d*d
        L0,L1 = (U*U-m*V*V*t)/d,(V*V-U*U*t)/C
        a,b,A,B = d/C,kp/C,d*d/q,kp/q
        C0=B*h*d*q**4/C
        def edge(u):
            s=sn(u)
            return C0*dn(u)*(1-m*t*s*s)/((d+k*C*s)**2*(L0+k*L1*s))
        def F(u):
            return mp.fsum(edge(u+j*delta) for j in range(N))
        def tangent_vertex(u):
            # Direct 2-by-2 solve for actual tangent intersections at u+-v.
            p,q = u-v,u+v
            aa,bb,cc,dd=-sn(p)/a,cn(p)/b,-sn(q)/a,cn(q)/b
            det=aa*dd-bb*cc
            return ((dd-bb)/det,(aa-cc)/det)
        def shoelace(w,focus):
            pts=[]
            for j in range(N):
                x,y=tangent_vertex(w+j*delta)
                x-=focus
                dist=x*x+y*y
                pts.append((x/dist,y/dist))
            return mp.fsum(pts[j][0]*pts[(j+1)%N][1]-pts[j][1]*pts[(j+1)%N][0]
                           for j in range(N))/2
        return locals()

    # Every coprime primitive star for each listed odd N, with hard eccentricity limits.
    ks = ['0.000001','0.2','0.7','0.99','0.999999999999']
    for N in [3,5,7,9,11,15,21]:
        for tau in range(1,(N+1)//2):
            if math.gcd(N,tau)!=1:
                continue
            for kval in ks:
                d=setup(mp.mpf(kval),N,tau)
                K,Kp,v,delta=d['K'],d['Kp'],d['v'],d['delta']
                sn,cn,dn,edge,F=d['sn'],d['cn'],d['dn'],d['edge'],d['F']
                record('triple_L0',rel(d['L0'],d['Z']*dn(3*v)))
                record('triple_L1',rel(d['L1'],d['Z']*cn(3*v)))
                products=[]
                for phase in ['0.071','0.317','0.79']:
                    w=K*mp.mpf(phase)
                    bp,bm=d['shoelace'](w,d['k']),d['shoelace'](w,-d['k'])
                    record('direct_shoelace_vs_edge_sum',rel(bp,F(w+v)))
                    record('opposite_focus_vs_shift',rel(bm,F(w+v+2*K)))
                    products.append(bp*bm)
                    if bp<=0 or bm<=0:
                        raise AssertionError(('real positivity',N,tau,kval,phase))
                variation=max(rel(x,products[0]) for x in products)
                record('product_phase_variation',variation)
                z=K*(mp.mpf('0.239')+mp.mpf('0.17')*1j)
                r0=3*K+1j*Kp
                record('edge_real_full_period',rel(edge(z),edge(z+4*K)))
                record('edge_imaginary_anti_period',rel(edge(z),-edge(z+2j*Kp)))
                record('edge_reflection',rel(edge(z),-edge(2*r0-z)))
                record('cyclic_primitive_period',rel(F(z),F(z+4*K/N)))
                record('cyclic_reflection',rel(F(z),-F(2*(r0+v)-z)))
                record('cyclic_half_period_zero',rel(F(r0+v+2*K/N),0))
                for root in [r0-v,r0+v]:
                    record('first_fiber_root',rel(d['d']+d['k']*d['C']*sn(root),0))
                for root in [r0-3*v,r0+3*v]:
                    record('second_fiber_root',rel(d['L0']+d['k']*d['L1']*sn(root),0))
                rows.append({'N':N,'tau':tau,'k':kval,
                             'product':mp.nstr(products[0],35),
                             'phase_relative_difference':mp.nstr(variation,8)})
    # Laurent principal parts at all special N3, plus ordinary star examples.
    for kval,N,tau in [('0.2',3,1),('0.7',3,1),('0.99',3,1),
                        ('0.7',5,1),('0.7',5,2),('0.99',9,4)]:
        d=setup(mp.mpf(kval),N,tau)
        K,Kp,v=d['K'],d['Kp'],d['v']
        r0=3*K+1j*Kp
        target=1j*d['V']*d['q']**2/(4*d['kp']**4*d['t']*d['W'])
        vals=[]
        for eps in [mp.mpf('1e-12'),mp.mpf('1e-20')]:
            # Symmetric second-order extraction cancels linear and cubic contamination.
            aplus=eps**2*(d['edge'](r0+v+eps)+d['edge'](r0+v-eps))/2
            aminus=eps**2*(d['edge'](r0-v+eps)+d['edge'](r0-v-eps))/2
            item={'epsilon':mp.nstr(eps,4),'a2_exact_error':mp.nstr(rel(aplus,target),10),
                  'a2_opposite_error':mp.nstr(rel(aplus,-aminus),10)}
            p=1j*Kp
            removable=(d['edge'](p+eps)+d['edge'](p-eps))/2
            removable_exact=1j*d['C0']*d['t']/(d['q']*d['L1'])
            item['sn_pole_removable_limit_error']=mp.nstr(rel(removable,removable_exact),10)
            residue_F=eps*(d['F'](r0+v+eps)-d['F'](r0+v-eps))/2
            item['cyclic_simple_pole_residue']=mp.nstr(residue_F,30)
            if N==3:
                c=K+1j*Kp
                residue=eps*(d['edge'](c+eps)-d['edge'](c-eps))/2
                item['critical_simple_residue']=mp.nstr(residue,30)
                item['critical_quadratic_scaled']=mp.nstr(eps**2*d['edge'](c+eps),15)
            vals.append(item)
        pole_rows.append({'k':kval,'N':N,'tau':tau,'principal_part_diagnostics':vals})
    # Exact endpoints are not part of the theorem; finite approaches are controls only.
    for N,tau in [(101,1),(101,50),(401,1),(401,200)]:
        d=setup(mp.mpf('0.8'),N,tau)
        values=[d['F'](d['K']*mp.mpf(x))*d['F'](d['K']*mp.mpf(x)+2*d['K'])
                for x in ['0.137','0.487']]
        boundary_rows.append({'N':N,'tau':tau,'v_over_K':mp.nstr(d['v']/d['K'],20),
                              'product':mp.nstr(values[0],35),
                              'relative_phase_difference':mp.nstr(rel(*values),10)})
    return {'kind':'finite noninterval mpmath diagnostics, not universal certification',
            'precision_decimal_digits':mp.mp.dps,'ordinary_case_count':len(rows),
            'phases_per_ordinary_case':3,
            'max_scaled_errors':{k:mp.nstr(v,12) for k,v in sorted(metrics.items())},
            'ordinary_cases':rows,'principal_parts':pole_rows,
            'v_endpoint_approaches':boundary_rows}


def lattice_controls():
    from fractions import Fraction as Q
    rows=[]
    for N in range(3,102,2):
        for tau in range(1,(N+1)//2):
            if math.gcd(N,tau)!=1:
                continue
            v,delta=Q(2*tau,N),Q(4*tau,N)
            # Coordinates in units of K, modulo 4, ignoring common imaginary component.
            plus,minus=3+v,3-v
            a=[(plus-j*delta)%4 for j in range(N)]
            b=[(minus-j*delta)%4 for j in range(N)]
            assert len(set(a))==N and set(a)==set(b)
            cplus,cminus=(3+3*v)%4,(3-3*v)%4
            assert cplus in set(a) and cminus in set(a)
            assert (cplus==cminus)==(N==3)
            assert v not in [Q(1,4),Q(1,3),Q(1,2),Q(3,4)]
            rows.append({'N':N,'tau':tau,'double_classes':N,'critical_collision':N==3})
    return {'kind':'finite exact rational lattice controls; the universal argument is in DERIVATION.md',
            'case_count':len(rows),'all_passed':True,'cases':rows}


if __name__=='__main__':
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    print('Exact symbolic checks starting',flush=True)
    exact=symbolic()
    (BASE/'SYMBOLIC_RESULTS.json').write_text(json.dumps(exact,indent=2)+'\n')
    print('Exact symbolic checks:',len(exact['checks']),flush=True)
    lattice=lattice_controls()
    (BASE/'LATTICE_RESULTS.json').write_text(json.dumps(lattice,indent=2)+'\n')
    print('Finite rational lattice checks:',lattice['case_count'],flush=True)
    finite=numeric()
    (BASE/'NUMERIC_RESULTS.json').write_text(json.dumps(finite,indent=2)+'\n')
    run={'started_utc':started,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'python':platform.python_version(),'sympy':S.__version__,'mpmath':mp.__version__,
         'authored_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'symbolic_all_passed':exact['all_passed'],'lattice_all_passed':lattice['all_passed'],
         'numeric_case_count':finite['ordinary_case_count'],'numeric_max_scaled_errors':finite['max_scaled_errors'],
         'scope_limit':'No intervals, no machine proof of analytic completeness, no historical checker replay.'}
    (BASE/'RUN_RECEIPT.json').write_text(json.dumps(run,indent=2)+'\n')
    print(json.dumps(run,indent=2),flush=True)
