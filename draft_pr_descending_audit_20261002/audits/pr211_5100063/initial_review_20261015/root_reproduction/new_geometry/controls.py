"""Independent audit controls. Exact algebra proves identities; numerics are support only.

This file was authored from INDEPENDENT_DERIVATION.md before inspecting inherited
checker implementations. It reads no submitted checker or reviewer result.
"""
from pathlib import Path
import hashlib
import json
import math
import platform
import sys

import mpmath as mp
import sympy as S

HERE = Path(__file__).parent
PRIVATE = HERE / 'private'


def exact_controls():
    m, t, x, k, s, C, d = S.symbols('m t x k s C d')
    q = 1-t
    ds = 1-m*t
    U = 1-2*m*t+m*t*t
    V = 1-2*t+m*t*t
    W = 1-m*t*t
    Z = W*W-4*m*t*t*q*ds
    D3 = U*W-2*m*t*q*V
    C3 = V*W-2*t*ds*U
    polys = {
        'confocal_axis_difference': ds-(1-m)-m*q,
        'sine_product_numerator': x*q*ds-t*(1-x)*(1-m*x)-(x-t)*(1-m*t*x),
        'distance_s_squared': ds**2-(1-m)-m*V,
        'distance_constant': (1-m)+m*q*q-U,
        'distance_linear': U+V-2*q*ds,
        'denominator_linear_coefficient': ds*(V*V-U*U*t)+q*(U*U-m*V*V*t)-2*U*V*q*ds,
        'triple_dn_numerator': U*U-m*V*V*t-ds*D3,
        'triple_cn_numerator': V*V-U*U*t-q*C3,
        'triple_norm': ds*D3*D3-m*q*C3*C3-(1-m)*Z*Z,
    }
    reduced = {name: str(S.factor(expr)) for name, expr in polys.items()}
    assert all(value == '0' for value in reduced.values()), reduced

    # A fully rational Jacobi addition datum, with beta retained as one radical.
    # k=25/39, sn(v)=sn(u)=3/5, cn=4/5, dn=12/13.
    # Its real v exists uniquely on (0,K). Taking u=v verifies signed formulas.
    kr = S.Rational(25,39)
    hr = S.Rational(3,5)
    Cr = S.Rational(4,5)
    dr = S.Rational(12,13)
    gr = 1-kr*kr
    assert hr*hr+Cr*Cr == 1 and dr*dr+kr*kr*hr*hr == 1
    qr = Cr*Cr
    tr = hr*hr
    Ur = U.subs({m:kr*kr,t:tr})
    Vr = V.subs({m:kr*kr,t:tr})
    ar, br = dr/Cr, S.sqrt(gr)/Cr
    Ar, Br = dr*dr/qr, S.sqrt(gr)/qr
    D = 1-kr*kr*tr*hr*hr
    sp, sm = (hr*Cr*dr+hr*Cr*dr)/D, S.Integer(0)
    yp, ym = (Cr*Cr-hr*hr*dr*dr)/D, S.Integer(1)
    Q = S.Matrix([-Ar*hr,Br*Cr])
    f = S.Matrix([kr,0])
    tangent_plus = S.simplify(-Q[0]*sp/ar+Q[1]*yp/br-1)
    tangent_minus = S.simplify(-Q[0]*sm/ar+Q[1]*ym/br-1)
    distance = S.simplify((Q-f).dot(Q-f))
    factored = (1+kr*hr)*(Ur+kr*Vr*hr)/qr**2
    assert tangent_plus == 0 and tangent_minus == 0
    assert S.simplify(distance-factored) == 0
    # Edge endpoints Q(u-v)=Q(0) and Q(u+v)=Q(2v).
    Qm, Qp = S.Matrix([0,Br]), S.Matrix([-Ar*sp,Br*yp])
    Im = (Qm-f)/S.simplify((Qm-f).dot(Qm-f))
    Ip = (Qp-f)/S.simplify((Qp-f).dot(Qp-f))
    edge = S.simplify(S.det(S.Matrix.hstack(Im,Ip))/2)
    L0 = (Ur*Ur-kr*kr*Vr*Vr*tr)/dr
    L1 = (Vr*Vr-Ur*Ur*tr)/Cr
    C0 = Br*hr*dr*qr**4/Cr
    edge_formula = C0*dr*D/((dr+kr*Cr*hr)**2*(L0+kr*L1*hr))
    assert S.simplify(edge-edge_formula) == 0
    assert edge > 0
    # Rigid scaling of geometry must give lambda^-2 for each unit-inverse edge.
    for lam in [S.Rational(1,7), S.Integer(7)]:
        def inv(V):
            return V/V.dot(V)
        lm, lp = lam*(Qm-f), lam*(Qp-f)
        scaled = S.simplify(S.det(S.Matrix.hstack(inv(lm),inv(lp)))/2)
        assert S.simplify(scaled-edge/lam**2) == 0
    return {
        'polynomial_residuals': reduced,
        'rational_jacobi_datum': {'k':str(kr),'sn_v':str(hr),'cn_v':str(Cr),'dn_v':str(dr)},
        'exact_translated_inverse_edge': str(edge),
        'exact_geometry_and_q4_match': True,
        'exact_scale_factors': ['1/7','7'],
    }


def numerical_controls():
    mp.mp.dps = 100
    maxes = {}
    counts = {'local_cases':0, 'closed_families':0, 'polygon_phases':0, 'reversed_axis_families':0}
    rows = []

    def record(name, a, b):
        err = abs(a-b)/max(mp.mpf(1),abs(a),abs(b))
        maxes[name] = max(maxes.get(name,mp.mpf(0)),err)
        if err >= mp.mpf('1e-55'):
            raise AssertionError((name,mp.nstr(err,8)))

    def funcs(z,m):
        return tuple(mp.ellipfun(f,z,m) for f in ('sn','cn','dn'))

    def constants(m,v,alpha=mp.mpf(1)):
        k=mp.sqrt(m); kp=mp.sqrt(1-m)
        h,C,d=funcs(v,m); t=h*h; q=C*C
        U=1-2*m*t+m*t*t; V=1-2*t+m*t*t; W=1-m*t*t
        Z=W*W-4*m*t*t*q*d*d
        L0=(U*U-m*V*V*t)/d; L1=(V*V-U*U*t)/C
        a=alpha*d/C; b=alpha*kp/C; A=a*d/C; B=b/C; c=alpha*k
        return locals()

    def tangent_intersection(z1,z2,m,cc):
        sn1,cn1,_=funcs(z1,m); sn2,cn2,_=funcs(z2,m)
        aa=-sn1/cc['a']; bb=cn1/cc['b']; dd=-sn2/cc['a']; ee=cn2/cc['b']
        determinant=aa*ee-bb*dd
        assert determinant != 0
        return ((ee-bb)/determinant,(aa-dd)/determinant)

    def q_formula(z,m,cc):
        sn,cn,_=funcs(z,m)
        return (-cc['A']*sn,cc['B']*cn)

    def inv(Q,c):
        x=Q[0]-c; y=Q[1]; dd=x*x+y*y
        assert dd>0
        return (x/dd,y/dd)

    def edge(Q,R,c):
        x,y=inv(Q,c); X,Y=inv(R,c)
        return (x*Y-y*X)/2

    def e_formula(u,m,cc):
        sn,cn,dn=funcs(u,m)
        h,C,d,q=cc['h'],cc['C'],cc['d'],cc['q']
        L0,L1,k=cc['L0'],cc['L1'],cc['k']
        C0=cc['B']*h*d*q**4/(cc['alpha']**3*C)
        result=C0*dn*(1-m*cc['t']*sn**2)/((d+k*C*sn)**2*(L0+k*L1*sn))
        assert result>0
        return result

    def area(Qs,c):
        return sum(edge(Qs[j],Qs[(j+1)%len(Qs)],c) for j in range(len(Qs)))

    # Severe open-domain corners; these are diagnostics and not interval proofs.
    parameters=[mp.mpf('1e-20'),mp.mpf('.04'),mp.mpf('.49'),1-mp.mpf('1e-20')]
    v_fractions=[mp.mpf('1e-10'),mp.mpf('1e-5'),mp.mpf('.25'),mp.mpf('.5'),1-mp.mpf('1e-5'),1-mp.mpf('1e-10')]
    for m in parameters:
        K=mp.ellipk(m)
        for frac in v_fractions:
            v=frac*K; cc=constants(m,v)
            sn3,cn3,dn3=funcs(3*v,m)
            record('triple_dn',cc['L0'],cc['Z']*dn3)
            record('triple_cn',cc['L1'],cc['Z']*cn3)
            assert cc['Z']>0 and cc['L0']>0
            for phase in ['0','.37','1','2.31']:
                u=mp.mpf(phase)*K
                Q=tangent_intersection(u-v,u+v,m,cc)
                expected=q_formula(u,m,cc)
                record('outer_x',Q[0],expected[0]); record('outer_y',Q[1],expected[1])
                sn,cn,dn=funcs(u,m)
                distance=(Q[0]-cc['c'])**2+Q[1]**2
                factor=cc['alpha']**2/cc['q']**2*(1+cc['k']*sn)*(cc['U']+cc['k']*cc['V']*sn)
                record('focal_distance',distance,factor)
                Qm=tangent_intersection(u-2*v,u,m,cc)
                Qp=tangent_intersection(u,u+2*v,m,cc)
                geom=edge(Qm,Qp,cc['c']); form=e_formula(u,m,cc)
                assert geom>0
                record('inverse_edge',geom,form)
                counts['local_cases']+=1

    # Direct outer tangent intersections and actual Euclidean inversion, including stars.
    for m in [mp.mpf('1e-12'),mp.mpf('.04'),mp.mpf('.49'),mp.mpf('.9999'),1-mp.mpf('1e-16')]:
        K=mp.ellipk(m)
        for N in [3,5,7,9,11]:
            for tau in range(1,(N+1)//2):
                if math.gcd(tau,N)!=1:
                    continue
                v=2*K*tau/N; delta=2*v; cc=constants(m,v)
                if cc['B']>cc['A']:
                    counts['reversed_axis_families']+=1
                products=[]
                for phase in ['0','.137','.381','1.731']:
                    w=mp.mpf(phase)*K
                    Qs=[tangent_intersection(w+j*delta,w+(j+1)*delta,m,cc) for j in range(N)]
                    bp,bm=area(Qs,cc['c']),area(Qs,-cc['c'])
                    assert bp>0 and bm>0
                    ef=sum(e_formula(w+2*v+j*delta,m,cc) for j in range(N))
                    record('polygon_area_formula',bp,ef)
                    reversed_points=list(reversed(Qs))
                    record('reversal_plus',area(reversed_points,cc['c']),-bp)
                    record('reversal_minus',area(reversed_points,-cc['c']),-bm)
                    products.append(bp*bm)
                    counts['polygon_phases']+=1
                for value in products[1:]:
                    record('product_constancy_support',value,products[0])
                # Scaling uses a fresh tangent geometry, not only multiplying an area formula.
                w=mp.mpf('.381')*K
                for lam in [mp.mpf(1)/7,mp.mpf(7)]:
                    scaled=constants(m,v,lam)
                    scaled_Q=[tangent_intersection(w+j*delta,w+(j+1)*delta,m,scaled) for j in range(N)]
                    scaled_product=area(scaled_Q,scaled['c'])*area(scaled_Q,-scaled['c'])
                    record('area_product_scaling',scaled_product,products[2]/lam**4)
                rows.append({'m':str(m),'N':N,'tau':tau,'B_greater_A':bool(cc['B']>cc['A']),'product':mp.nstr(products[0],35)})
                counts['closed_families']+=1

    (PRIVATE/'numerical_rows.json').write_text(json.dumps(rows,indent=2)+'\n')
    return {'certified':False,'meaning':'high precision diagnostics only; no interval enclosures',
            'decimal_digits':mp.mp.dps,'counts':counts,'maximum_normalized_discrepancies':{k:mp.nstr(v,10) for k,v in maxes.items()}}


def main():
    PRIVATE.mkdir(exist_ok=True)
    result={'python':sys.version,'sympy':S.__version__,'mpmath':mp.__version__,
            'independent_derivation_sha256':hashlib.sha256((HERE/'INDEPENDENT_DERIVATION.md').read_bytes()).hexdigest(),
            'exact':exact_controls(),'numerical':numerical_controls()}
    (HERE/'CONTROL_SUMMARY.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
