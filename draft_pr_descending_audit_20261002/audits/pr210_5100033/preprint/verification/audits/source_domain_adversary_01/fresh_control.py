#!/usr/bin/env python3
"""Fresh PR210 controls. No imports/reads from submitted implementations.

Run with the audit environment's Python -B; stdout is deterministic JSON.
All floating-point claims are UNCERTIFIED. Exact SymPy reductions are algebraic
checks, not a machine-checked proof of the elliptic-function theorem.
"""
import json
import math
import sys
import mpmath as mp
import sympy as sp

mp.mp.dps = 75


def enc(x):
    if isinstance(x, (mp.mpf, mp.mpc)):
        if isinstance(x, mp.mpc):
            return {"real": mp.nstr(x.real, 35), "imag": mp.nstr(x.imag, 35)}
        return mp.nstr(x, 35)
    if isinstance(x, dict):
        return {k: enc(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [enc(v) for v in x]
    return x


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def sub(x, y):
    return (x[0] - y[0], x[1] - y[1])


def scale(t, x):
    return (t * x[0], t * x[1])


def dot(x, y):
    return x[0] * y[0] + x[1] * y[1]


def det(x, y):
    return x[0] * y[1] - x[1] * y[0]


def norm(x):
    return mp.sqrt(abs(x[0])**2 + abs(x[1])**2)


def area(vertices):
    return sum(det(vertices[j], vertices[(j + 1) % len(vertices)])
               for j in range(len(vertices))) / 2


def line_intersection(n, m):
    """Solve n.X = m.X = 1 without a geometry library."""
    d = det(n, m)
    return ((m[1] - n[1]) / d, (n[0] - m[0]) / d)


def foot_on_line(f, u, v):
    d = sub(v, u)
    return add(u, scale(dot(sub(f, u), d) / dot(d, d), d))


def physical_step(p, a, b, alpha, beta):
    """Find both real tangents from p to caustic, choose positive winding.

    The affine image of the caustic is a unit circle. A contact vector h has
    h.h=1, h.(p_x/alpha,p_y/beta)=1. Continue its tangent to the second
    intersection with the outer ellipse. No Jacobi function is used here.
    """
    u = (p[0] / alpha, p[1] / beta)
    rho2 = dot(u, u)
    base = scale(1 / rho2, u)
    off = scale(mp.sqrt(rho2 - 1) / rho2, (-u[1], u[0]))
    possibilities = []
    for contact_unit in [add(base, off), sub(base, off)]:
        contact = (alpha * contact_unit[0], beta * contact_unit[1])
        d = sub(contact, p)
        t = -2 * (p[0] * d[0] / a**2 + p[1] * d[1] / b**2)
        t /= d[0]**2 / a**2 + d[1]**2 / b**2
        q = add(p, scale(t, d))
        if det(p, q) > 0:
            possibilities.append((q, contact, t))
    assert len(possibilities) == 1
    return possibilities[0]


def outer_and_feet(points, a, b, focus):
    normals = [(p[0] / a**2, p[1] / b**2) for p in points]
    outer = [line_intersection(normals[j], normals[(j + 1) % len(points)])
             for j in range(len(points))]
    feet = [foot_on_line(focus, outer[j - 1], outer[j]) for j in range(len(points))]
    return outer, feet


def symbolic_checks():
    a, c, x, y = sp.symbols('a c x y', nonzero=True, real=True)
    b2 = a*a-c*c
    n = sp.Matrix([x/a**2, y/b2])
    f = sp.Matrix([c, 0])
    raw = f + (1-(n.dot(f))) / n.dot(n) * n
    expected = sp.Matrix([a*a*(c+x)/(a*a+c*x), a*a*y/(a*a+c*x)])
    ellipse_y2 = b2*(1-x*x/(a*a))
    def reduce(expr):
        numerator = sp.together(expr).as_numer_denom()[0]
        return sp.factor(sp.rem(numerator, y*y-ellipse_y2, y))
    checks = {
        'orthogonal_foot_x': reduce(raw[0]-expected[0]) == 0,
        'orthogonal_foot_y': reduce(raw[1]-expected[1]) == 0,
        'foot_on_tangent': reduce(n.dot(expected)-1) == 0,
        'circle_bilinear_identity': reduce(expected.dot(expected)-a*a) == 0,
        'normal_norm_factorization': reduce(n.dot(n)-(a*a-c*c*x*x/(a*a))/(a*a*b2)) == 0,
    }
    assert all(checks.values())
    return checks


def family(k_string, N, tau, alpha_string='1'):
    k = mp.mpf(k_string)
    alpha = mp.mpf(alpha_string)
    beta = alpha*mp.sqrt(1-k*k)
    c = alpha*k
    K = mp.ellipk(k*k)
    v = 2*K*tau/N
    a = alpha*mp.ellipfun('dn', v, k*k)/mp.ellipfun('cn', v, k*k)
    b = beta/mp.ellipfun('cn', v, k*k)
    errors = {key: mp.mpf(0) for key in [
        'ellipse', 'caustic_contact', 'caustic_tangent', 'closure',
        'canonical_match', 'reflection', 'outer_side_tangent', 'projection_match',
        'aux_circle', 'focus_switch', 'cyclic_shift', 'orientation_area',
        'orientation_product', 'repetition_area', 'repetition_product']}
    products = []
    mutant_products = []
    single_areas = []
    min_outer_side = mp.inf
    min_tangent_det = mp.inf
    max_chord_foot_distance = mp.mpf(0)
    turns = []
    for phase in [mp.mpf(0), mp.mpf(1)/17, mp.mpf(3)/11, mp.mpf(7)/13, mp.mpf(19)/23]:
        theta = 2*mp.pi*phase
        initial = (a*mp.cos(theta), b*mp.sin(theta))
        w = mp.ellipf(theta-mp.pi/2, k*k)
        points = [initial]
        contacts = []
        for j in range(N):
            q, contact, t = physical_step(points[-1], a, b, alpha, beta)
            assert t > 1
            contacts.append(contact)
            points.append(q)
        errors['closure'] = max(errors['closure'], norm(sub(points[-1], initial))/a)
        points.pop()
        for j,p in enumerate(points):
            q = points[(j+1)%N]
            d = sub(q,p)
            h = contacts[j]
            errors['ellipse'] = max(errors['ellipse'], abs(p[0]**2/a**2+p[1]**2/b**2-1))
            errors['caustic_contact'] = max(errors['caustic_contact'], abs(h[0]**2/alpha**2+h[1]**2/beta**2-1))
            errors['caustic_tangent'] = max(errors['caustic_tangent'], abs(h[0]*d[0]/alpha**2+h[1]*d[1]/beta**2))
            canonical = (-a*mp.ellipfun('sn',w+2*j*v,k*k), b*mp.ellipfun('cn',w+2*j*v,k*k))
            errors['canonical_match'] = max(errors['canonical_match'], norm(sub(p,canonical))/a)
            previous = points[j-1]
            incoming = scale(1/norm(sub(p,previous)),sub(p,previous))
            outgoing = scale(1/norm(d),d)
            normal = (p[0]/a**2,p[1]/b**2)
            reflected = sub(incoming,scale(2*dot(incoming,normal)/dot(normal,normal),normal))
            errors['reflection'] = max(errors['reflection'],norm(sub(outgoing,reflected)))
        turns.append(sum(mp.atan2(det(points[j],points[(j+1)%N]),dot(points[j],points[(j+1)%N])) for j in range(N))/(2*mp.pi))
        outer, plus = outer_and_feet(points,a,b,(c,0))
        _, minus = outer_and_feet(points,a,b,(-c,0))
        for j,p in enumerate(points):
            n = (p[0]/a**2,p[1]/b**2)
            min_outer_side=min(min_outer_side,norm(sub(outer[j],outer[j-1]))/a)
            nn=(points[(j+1)%N][0]/a**2,points[(j+1)%N][1]/b**2)
            min_tangent_det=min(min_tangent_det,abs(det(n,nn))*a*a)
            errors['outer_side_tangent']=max(errors['outer_side_tangent'],abs(dot(n,outer[j])-1),abs(dot(n,outer[j-1])-1))
            foot=(a*a*(c+p[0])/(a*a+c*p[0]),a*a*p[1]/(a*a+c*p[0]))
            errors['projection_match']=max(errors['projection_match'],norm(sub(plus[j],foot))/a)
            errors['aux_circle']=max(errors['aux_circle'],abs(dot(plus[j],plus[j])/a**2-1))
            chordfoot=foot_on_line((c,0),p,points[(j+1)%N])
            max_chord_foot_distance=max(max_chord_foot_distance,norm(sub(chordfoot,plus[j]))/a)
        Bp,Bm=area(plus),area(minus)
        products.append(Bp*Bm/a**4)
        single_areas.append(Bp/a**2)
        shifted=[(-p[0],-p[1]) for p in points]
        _, shiftedplus=outer_and_feet(shifted,a,b,(c,0))
        errors['focus_switch']=max(errors['focus_switch'],abs(area(shiftedplus)-Bm)/a**2)
        errors['cyclic_shift']=max(errors['cyclic_shift'],abs(area(plus[2:]+plus[:2])-Bp)/a**2)
        reversedpoints=list(reversed(points))
        _,rp=outer_and_feet(reversedpoints,a,b,(c,0))
        _,rm=outer_and_feet(reversedpoints,a,b,(-c,0))
        errors['orientation_area']=max(errors['orientation_area'],abs(area(rp)+Bp)/a**2)
        errors['orientation_product']=max(errors['orientation_product'],abs(area(rp)*area(rm)-Bp*Bm)/a**4)
        repeated=points*3
        _,rrp=outer_and_feet(repeated,a,b,(c,0))
        _,rrm=outer_and_feet(repeated,a,b,(-c,0))
        errors['repetition_area']=max(errors['repetition_area'],abs(area(rrp)-3*Bp)/a**2)
        errors['repetition_product']=max(errors['repetition_product'],abs(area(rrp)*area(rrm)-9*Bp*Bm)/a**4)
        _,mutp=outer_and_feet(points,a,b,(c/2,0))
        _,mutm=outer_and_feet(points,a,b,(-c/2,0))
        mutant_products.append(area(mutp)*area(mutm)/a**4)
    span=max(products)-min(products)
    assert max(errors.values()) < mp.mpf('1e-57'), (k_string,N,tau,errors)
    if N % 2:
        assert abs(span) < mp.mpf('1e-57')
    assert max(abs(t-tau) for t in turns)<mp.mpf('1e-57')
    return {'k':k_string,'alpha':alpha_string,'N':N,'tau':tau,'least_period':N//math.gcd(N,tau),
            'a':a,'b':b,'a_over_b':a/b,'products_over_a4':products,'product_span':span,
            'single_area_span':max(single_areas)-min(single_areas),
            'nonfocal_control_product_span':max(mutant_products)-min(mutant_products),
            'winding_values':turns,'errors':errors,'min_outer_side_over_a':min_outer_side,
            'min_tangent_determinant_scaled':min_tangent_det,
            'max_chord_vs_outer_foot_distance_over_a':max_chord_foot_distance}


def analytic_diagnostics():
    rows=[]
    for k_string,N,tau in [('0.37',7,2),('0.97',9,4),('0.71',8,3)]:
        k=mp.mpf(k_string); m=k*k; kp=mp.sqrt(1-m)
        K=mp.ellipk(m); Kp=mp.ellipk(1-m); v=2*K*tau/N
        a=mp.ellipfun('dn',v,m)/mp.ellipfun('cn',v,m)
        b=kp/mp.ellipfun('cn',v,m); c=k; L=4*K/N
        def Q(z):
            s=mp.ellipfun('sn',z,m); t=mp.ellipfun('cn',z,m)
            return (a*(c-a*s)/(a-c*s),a*b*t/(a-c*s))
        def T(z):
            return sum(det(Q(z+2*j*v),Q(z+2*((j+1)%N)*v)) for j in range(N))/2
        r=K+1j*Kp; zm=r-v; zp=r+v
        qerr=[]
        for u in [-v,v,mp.mpf('0.217')]:
            z=r+u
            qerr.extend([abs(mp.ellipfun('sn',z,m)-mp.ellipfun('dn',u,m)/(k*mp.ellipfun('cn',u,m))),
                         abs(mp.ellipfun('cn',z,m)+1j*kp/(k*mp.ellipfun('cn',u,m))),
                         abs(mp.ellipfun('dn',z,m)-1j*kp*mp.ellipfun('sn',u,m)/mp.ellipfun('cn',u,m))])
        def residue(z):
            s=mp.ellipfun('sn',z,m); t=mp.ellipfun('cn',z,m); d=mp.ellipfun('dn',z,m)
            return scale(1/(-c*t*d),(a*(c-a*s),a*b*t))
        Rm,Rp=residue(zm),residue(zp)
        z=mp.mpf('0.173')+mp.mpf('0.291')*1j
        base=K-v
        identity_errors={
            'quarter_shift_max':max(qerr),
            'opposite_residue':norm(add(Rm,Rp)),
            'collinear_residue_determinant':abs(det(Rm,Rp)),
            'real_reduced_period':abs(T(z+L)-T(z)),
            'imaginary_antiperiod':abs(T(z+2j*Kp)+T(z)),
            'reflection':abs(T(2*K-z)-T(z)),
            'forced_zero':abs(T(base+1j*Kp+L/2)),
            'halfshift_product':abs(T(z)*T(z+L/2)-T(z+mp.mpf('0.381'))*T(z+mp.mpf('0.381')+L/2))}
        assert max(identity_errors.values())<mp.mpf('1e-55')
        poles=[]
        for eps_string in ['1e-6','1e-10','1e-14']:
            eps=mp.mpf(eps_string)
            # For a simple area pole eps*T tends to finite; eps^2*T tends to 0.
            poles.append({'eps':eps_string,'eps_T':eps*T(zm+eps),'eps2_T':eps*eps*T(zm+eps),
                          'eps2_adjacent_det':eps*eps*det(Q(zm+eps),Q(zp+eps))})
        rows.append({'k':k_string,'N':N,'tau':tau,'identity_errors':identity_errors,
                     'simple_pole_diagnostic':poles})
    return rows


def exact_lattice_controls():
    rows=[]
    for N in range(3,40):
        for tau in range(1,(N+1)//2):
            if math.gcd(N,tau)!=1: continue
            orbit=[(j*tau)%N for j in range(N)]
            assert len(set(orbit))==N
            # Two roots z_- and z_+=z_-+delta give exactly two singular indices.
            singular=[j for j in range(N) if (j*tau)%N in [0,tau]]
            assert singular==[0,1]
            # In units of L, 2K=N/2: half integral exactly for odd N.
            rows.append({'N':N,'tau':tau,'distinct_phase_classes':len(set(orbit)),
                         'singular_indices_at_zminus':singular,
                         'focus_shift_is_half_period':bool(N%2)})
    return rows


def main():
    cases=[]
    for k in ['0.000001','0.37','0.97','0.999999']:
        for N in [3,5,7,9,11,13]:
            for tau in range(1,(N+1)//2):
                if math.gcd(N,tau)==1:
                    cases.append(family(k,N,tau))
    for N,tau in [(4,1),(6,1),(8,3),(10,3)]:
        cases.append(family('0.71',N,tau))
    # Scaling controls: all dimensionless residuals/products remain unchanged.
    cases.append(family('0.37',7,2,'0.00001'))
    cases.append(family('0.37',7,2,'100000'))
    result={'schema':'PR210-fresh-source-domain-control-v1',
            'numerics':'UNCERTIFIED arbitrary-precision floating point; no interval certificate',
            'precision_digits':mp.mp.dps,'python':sys.version.split()[0],
            'mpmath':mp.__version__,'sympy':sp.__version__,
            'design':'Independent caustic-tangent physical stepping; tangent intersections; feet recovered from outer vertex side lines. No submitted code or report read.',
            'symbolic_checks':symbolic_checks(),'real_family_count':len(cases),
            'real_families':cases,'analytic_diagnostics':analytic_diagnostics(),
            'exact_lattice_controls':exact_lattice_controls()}
    print(json.dumps(enc(result),indent=2,sort_keys=True))


if __name__=='__main__': main()
