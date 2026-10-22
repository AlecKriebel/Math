#!/usr/bin/env python3
"""Exact algebra certificates; stdout only unless --output NEW_FILE is given.

This verifies finite symbolic identities, not the whole analytic proof or priority.
All acceptance checks use explicit exceptions, including under Python -O.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import sympy as s


class VerificationError(Exception):
    pass


def require(condition, message):
    if condition is not True and condition is not s.true:
        raise VerificationError(message)


def check_zero(checks, name, expression, basis=None):
    expression = s.sympify(expression)
    require(not expression.has(s.nan, s.zoo, s.oo, -s.oo), name + ': nonfinite expression')
    numerator, denominator = s.together(expression).as_numer_denom()
    require(denominator != 0, name + ': identically zero denominator')
    if basis is not None:
        numerator = basis.reduce(s.expand(numerator))[1]
    residual = s.factor(numerator)
    require(residual == 0, name + ': nonzero exact residual ' + str(residual))
    checks.append({'name': name, 'residual': '0'})


def det(p, q):
    return p[0]*q[1] - p[1]*q[0]


def area(points):
    return s.simplify(sum(det(p, points[(j+1) % len(points)])
                          for j, p in enumerate(points)) / 2)


def invert(points, focus):
    inverse = []
    for p in points:
        z = (p[0]-focus, p[1])
        d = s.simplify(z[0]**2 + z[1]**2)
        require(d.is_positive is True, 'exact inversion denominator not positive')
        inverse.append((s.simplify(z[0]/d), s.simplify(z[1]/d)))
    return inverse


def unit(p):
    length = s.sqrt(s.simplify(p[0]**2 + p[1]**2))
    require(length.is_positive is True, 'exact vector length not positive')
    return (s.simplify(p[0]/length), s.simplify(p[1]/length))


def main_checks():
    checks = []
    k, t, x, U, V, W = s.symbols('k t x U V W')
    q = 1-t
    actual = {U: 1-2*k**2*t+k**2*t**2,
              V: 1-2*t+k**2*t**2, W: 1-k**2*t**2}
    z, cu, du, h, cv, dv = s.symbols('z cu du h cv dv')
    basis = s.groebner([cu**2+z**2-1, du**2+k**2*z**2-1,
                       cv**2+h**2-1, dv**2+k**2*h**2-1],
                      cu, du, cv, dv, h, z, k)

    def zero(name, expression, ring=None):
        check_zero(checks, name, expression, ring)

    zero('U_minus_V', (U-V-2*t*(1-k**2)).subs(actual))
    zero('U_plus_V', (U+V-2*q*(1-k**2*t)).subs(actual))
    zero('U_squared_minus_k2V_squared',
         (U**2-k**2*V**2-(1-k**2)*W**2).subs(actual))
    zero('U_positive_factorization', (U-(1-k**2+k**2*q**2)).subs(actual))
    zero('W_positive_factorization', (W-(1-k**2+k**2*q*(2-q))).subs(actual))
    zero('canonical_confocality', (1-k**2*t)/q-(1-k**2)/q-k**2)
    zero('strict_nesting_major_axis', (1-k**2*t)/q-1-(1-k**2)*t/q)
    zero('strict_nesting_minor_axis', (1-k**2)/q-(1-k**2)-(1-k**2)*t/q)

    # alpha=1; scaling restores arbitrary alpha>0. Jacobi addition input:
    # z=sn(u), cu=cn(u), du=dn(u), h=sn(v), cv=cn(v), dv=dn(v).
    denominator = 1-k**2*h**2*z**2
    sm = (z*cv*dv-h*cu*du)/denominator
    sp = (z*cv*dv+h*cu*du)/denominator
    cm = (cu*cv+z*h*du*dv)/denominator
    cp = (cu*cv-z*h*du*dv)/denominator
    dm = (du*dv+k**2*z*h*cu*cv)/denominator
    dp = (du*dv-k**2*z*h*cu*cv)/denominator
    a = dv/cv
    u0 = 1-2*k**2*h**2+k**2*h**4
    v0 = 1-2*h**2+k**2*h**4
    zero('dn_endpoint_sum', dm+dp-2*du*dv/denominator)
    zero('ordinary_edge_determinant_divided_by_b',
         a*(sp*cm-sm*cp)-2*h*dv*du/denominator, basis)
    translated_det = (-a*sm-k)*cp-cm*(-a*sp-k)
    zero('translated_focal_determinant_divided_by_b',
         translated_det-2*h*dv*du*(1+k*z)/denominator, basis)
    distance_product = (a+k*sm)*(a+k*sp)
    target_product = (1+k*z)*(u0+k*v0*z)/(cv**2*denominator)
    zero('endpoint_focal_distance_product', distance_product-target_product, basis)
    # b is suppressed on both sides of this edge identity.
    edge = translated_det/(2*distance_product**2)
    target_edge = h*dv*cv**4*du*denominator/((1+k*z)*(u0+k*v0*z)**2)
    zero('inverted_edge_shoelace_contribution_divided_by_b', edge-target_edge, basis)
    zero('ordinary_area_normalization_per_edge_divided_by_b',
         a*(sp*cm-sm*cp)/2-(a*h*cv/dv)*(dm+dp)/2, basis)
    a0, b0, c0 = s.symbols('a b c')
    zero('real_focal_distance_squared',
         ((-a0*z-c0)**2+b0**2*(1-z**2)-(a0+c0*z)**2)
         .subs(b0**2, a0**2-c0**2))
    # These formulas use the algebraic continuation of a+c sn, not a complex norm.
    zero('antipodal_pair_of_inverted_edges',
         (1-k**2*z**2)*(1/((1+k*z)*(U+k*V*z)**2)
         +1/((1-k*z)*(U-k*V*z)**2))
         -2*(U**2+k**2*V*(V+2*U)*z**2)/(U**2-k**2*V**2*z**2)**2)

    # Generic exact local decomposition: no specialization or sample points.
    H = U**2-k**2*V**2*x
    L = (1 - 2*k**2 * t * x)*(U**2+k**2*V*(V+2*U)*x)
    A = (1-t)/(U-V)**2
    B = U*(U**3*t+U**2*V*k**2*t-2*U**2*V-2*U*V**2*k**2*t
           +U*V**2+V**3*k**2)/((U**2-k**2*V**2)*(U-V)**2)
    D = k**2*V*(V**2-U**2*t)/((U**2-k**2*V**2)*(U-V))
    zero('generic_local_rational_decomposition',
         L-A*H**2-B*(1-k**2*x)*H
         -D*(1-k**2*x)*(U**2+(k**2*V**2-2*U**2)*x))
    y = s.symbols('y')
    zero('reciprocal_dn_addition_denominator',
         (1-k**2*x)*(1-k**2*y)-k**4*x*y*(1-x)*(1-y)
         -(1-k**2*x*y)*((1-k**2*y)-k**2*x*(1-y)))
    zero('reciprocal_dn_difference_derivative',
         (1-2*x)*H+2*k**2*V**2*x*(1-x)
         -(U**2+(k**2*V**2-2*U**2)*x))
    a2 = (V**2-U**2*t)/(4*h*cv*dv*(U**2-k**2*V**2)*(U-V))
    zero('derivative_coefficient_normalization',
         4*k**2*h*cv*dv*V*a2-D)
    lam = U*(k**4*t**3+k**4*t**2-5*k**2*t+k**2+2) \
          /(2*(1-k**2)**2*W**3)
    zero('cyclic_coefficient_Lambda', (A+B/(W*U)-lam).subs(actual))
    stable_bracket = 2*(1-k**2)**2+5*k**2*(1-k**2)*q+k**4*q**2*(4-q)
    zero('stable_Lambda_numerator',
         k**4*t**3+k**4*t**2-5*k**2*t+k**2+2-stable_bracket)
    zero('N4_coefficient_A', A.subs(V,0)-(1-t)/U**2)
    zero('N4_coefficient_B', B.subs(V,0)-t)
    zero('N4_coefficient_D', D.subs(V,0))
    zero('N4_finite_derivative_coefficient', a2.subs(V,0)+t/(4*h*cv*dv*U))
    zero('N4_paired_edge_reduction', (1-k**2*t*x)-((1-t)+t*(1-k**2*x)))

    # N=4 axial inverse area, with the correct a^2=b^2+c^2 constraint.
    axial = [(-c0/a0**2,b0/a0**2),(-1/(a0+c0),0),
             (-c0/a0**2,-b0/a0**2),(1/(a0-c0),0)]
    numerator = s.together(area(axial)-2/(a0*b0)).as_numer_denom()[0]
    zero('N4_inverse_area', s.expand(numerator).subs(c0**2,a0**2-b0**2))
    zero('N4_product_four', (2*a0*b0)*(2/(a0*b0))-4)

    # Exact repeated-triangle boundary: same confocal pair, least period 3.
    root2, root3 = s.sqrt(2), s.sqrt(3)
    P = [(2*root2,0),(-4*root2/3,s.Rational(5,3)),
         (-4*root2/3,-s.Rational(5,3))]
    M = [(-p[0],-p[1]) for p in P]
    alpha2, beta2 = s.Rational(32,9), s.Rational(5,9)
    zero('boundary_confocality', 8-5-(alpha2-beta2))
    require(0 < alpha2 < 8 and 0 < beta2 < 5, 'boundary not strictly nested')
    for label, points in [('P',P),('minus_P',M)]:
        require(len(set(points)) == 3, label+': vertices not distinct')
        for j,p in enumerate(points):
            zero(label+'_outer_vertex_'+str(j), p[0]**2/8+p[1]**2/5-1)
            qpoint = points[(j+1)%3]
            prev = points[(j-1)%3]
            # Line coefficients L x+M y=J and exact conic support criterion.
            normal = (qpoint[1]-p[1], p[0]-qpoint[0])
            support = normal[0]*p[0]+normal[1]*p[1]
            zero(label+'_side_tangency_'+str(j),
                 alpha2*normal[0]**2+beta2*normal[1]**2-support**2)
            contact = (alpha2*normal[0]/support,beta2*normal[1]/support)
            segment_parameter = [s.Rational(1,3),s.Rational(1,2),s.Rational(2,3)][j]
            for dimension in (0,1):
                zero(label+'_contact_'+str(j)+'_'+str(dimension),
                     contact[dimension]-p[dimension]
                     -segment_parameter*(qpoint[dimension]-p[dimension]))
            incoming = unit((p[0]-prev[0],p[1]-prev[1]))
            outgoing = unit((qpoint[0]-p[0],qpoint[1]-p[1]))
            n = (p[0]/8,p[1]/5)
            projection = (incoming[0]*n[0]+incoming[1]*n[1])/(n[0]**2+n[1]**2)
            for dimension in (0,1):
                zero(label+'_reflection_'+str(j)+'_'+str(dimension),
                     outgoing[dimension]-incoming[dimension]+2*projection*n[dimension])
    Ap, Am = area(P), area(M)
    Ip, Im = area(invert(P,root3)), area(invert(M,root3))
    zero('boundary_A_P', Ap-50*root2/9)
    zero('boundary_A_minus_P', Am-50*root2/9)
    zero('boundary_inverse_P', Ip-(8*root2-root3)/80)
    zero('boundary_inverse_minus_P', Im-(8*root2+root3)/80)
    zero('boundary_product_P', Ap*Ip-(80-5*s.sqrt(6))/72)
    zero('boundary_product_minus_P', Am*Im-(80+5*s.sqrt(6))/72)
    zero('boundary_12_list_product_P', area(P*4)*area(invert(P*4,root3))-(160-10*s.sqrt(6))/9)
    zero('boundary_12_list_product_minus_P', area(M*4)*area(invert(M*4,root3))-(160+10*s.sqrt(6))/9)
    difference = s.simplify(area(P*4)*area(invert(P*4,root3))
                            -area(M*4)*area(invert(M*4,root3)))
    zero('boundary_12_list_difference', difference+20*s.sqrt(6)/9)
    require(difference.is_negative is True, 'boundary products are not certified unequal')

    # Exact algebra for the continuous normalized triangular family.
    X,Y=s.symbols('X Y',real=True)
    radius=s.groebner([X**2+Y**2-1],X,Y)
    d=9*X**2+36*Y**2
    zero('connected_family_mutual_tangency',
         3*(4-36*Y**2)/d+6*(4-9*X**2)/d+2,radius)
    # General confocal reflection identity in the physical ellipse coordinates.
    px,py,vx,vy=s.symbols('px py vx vy',real=True)
    reflection_ring=s.groebner([px**2/8+py**2/5-1,vx**2+vy**2-1],px,py,vx,vy)
    zero('connected_family_confocal_reflection_identity',
         8*vy**2+5*vx**2-(-vy*px+vx*py)**2
         -40*(px*vx/8+py*vy/5)**2,reflection_ring)
    return {'schema':'pr207-portable-exact-verification-v1',
            'status':'PASS', 'sympy_version':s.__version__,
            'optimization_level':sys.flags.optimize,
            'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'exact_checks':len(checks),'checks':checks,
            'boundary_12_list_difference':str(difference),
            'scope':'Finite exact algebra certificates only. The analytic theorem, '
                    'real domains, Fourier convergence, periodic reindexing, and '
                    'connected-family explanation are stated in the note and README. '
                    'No novelty or priority conclusion is made.'}


def emit(result, output):
    text=json.dumps(result,indent=2,allow_nan=False)+'\n'
    if output is None:
        sys.stdout.write(text)
    else:
        # Exclusive creation protects source, proof, and previous results.
        with Path(output).open('x',encoding='utf-8') as stream:
            stream.write(text)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',metavar='NEW_FILE',help='exclusive creation; default stdout')
    args=parser.parse_args()
    try:
        emit(main_checks(),args.output)
    except Exception as error:
        sys.stderr.write(json.dumps({'status':'FAIL','error_type':type(error).__name__,
                                     'error':str(error)},allow_nan=False)+'\n')
        return 1
    return 0


if __name__=='__main__':
    sys.exit(main())
