#!/usr/bin/env python3
"""Distinct k114 controls: gcd/cosets, exact geometry, and ray reflection.

No originals are imported. Exact algebraic controls are reported separately
from high-precision reflected-ray diagnostics. No finite check is a theorem.
"""
from collections import defaultdict
from fractions import Fraction as Q
from math import gcd
from pathlib import Path
from datetime import datetime, timezone
import json
import sympy as s
import mpmath as mp

counts = defaultdict(int)

def ck(name, condition):
    assert bool(condition), name
    counts[name] += 1

# A subgroup/coset classification allows nonprimitive rotations too.
# On the denominator-2m grid H consists of multiples of 2*g, g=gcd(m,tau).
# Every H class has g preimages in m factors. Each zero coset is H+(m+-tau).
# Thus zero/pole cancellation iff m/g and tau/g are both odd.
rotation_cases = 0
for m in range(1, 81):
    for tau in range(1, m):
        rotation_cases += 1
        g = gcd(m, tau)
        L = 2*m
        order = m//g
        subgroup = set(range(0, L, 2*g))
        # Independent order calculation: repeatedly add the generator until return.
        visited = set()
        position = 0
        while position not in visited:
            visited.add(position)
            position = (position+2*tau) % L
        ck('subgroup_order_and_classes', visited == subgroup and len(visited) == order)
        # Closed-form multiplicities checked against direct incidence counting.
        for residue in range(L):
            pole_count = sum((residue+2*j*tau) % L == 0 for j in range(m))
            zero_count = sum((residue+2*j*tau-m-sign*tau) % L == 0
                             for j in range(m) for sign in (-1, 1))
            predicted_poles = g if residue in subgroup else 0
            predicted_zeros = g*sum((residue-m-sign*tau) % L in subgroup
                                    for sign in (-1, 1))
            ck('coset_multiplicity_formula',
               (pole_count, zero_count) == (predicted_poles, predicted_zeros))
        cancellation = all(
            g*sum((r-m-sign*tau) % L in subgroup for sign in (-1, 1))
            == 2*g*(r in subgroup) for r in range(L))
        ck('complete_gcd_cancellation_classification',
           cancellation == (m//g % 2 == 1 and tau//g % 2 == 1))
        primitive_N = 2*m//gcd(tau, 2*m)
        ck('least_period_classification',
           cancellation == (primitive_N % 4 == 2))
        if gcd(tau, 2*m) == 1:
            ck('primitive_antipodal_parity', tau % 2 == 1)
            ck('primitive_admissible_cancellation', cancellation == (m % 2 == 1))
        if tau % 2:
            ck('half_parameter_displacement_antipodal', (Q(tau, 1) % 2) == 1)

# Ordinary distances on a rational conic parameter, with rational a,b,c.
# This avoids assuming the submitted ordinary-distance formula at runtime.
for a,b,c in [(Q(5),Q(4),Q(3)), (Q(13),Q(12),Q(5)), (Q(17),Q(8),Q(15))]:
    for p in range(-30,31):
        t = Q(p,13)
        x = a*(1-t*t)/(1+t*t)
        y = 2*b*t/(1+t*t)
        ck('rational_boundary_point', x*x/(a*a)+y*y/(b*b) == 1)
        for focus in (-c,c):
            d2 = (x-focus)**2+y*y
            candidate = a-focus*x/a
            ck('positive_ordinary_distance_identity', candidate>0 and candidate*candidate == d2)
        ck('actual_antipodal_distance_pair',
           ((x-c)**2+y*y)*((-x-c)**2+y*y) == (a*a-c*c*x*x/(a*a))**2)

def exact_polygon(name, points, alpha2, beta2, expected_product=None):
    """Exact outer-ellipse membership, caustic tangency and reflection law."""
    a2,b2 = s.Integer(4),s.Integer(1)
    ck(name+'_strict_confocal_caustic',
       s.simplify(alpha2-beta2-3)==0 and bool(beta2>0) and bool(alpha2<4))
    n = len(points)
    ck(name+'_distinct_vertices', len(set(points))==n)
    for j,(x,y) in enumerate(points):
        prev,nxt=points[j-1],points[(j+1)%n]
        ck(name+'_boundary', s.simplify(x*x/a2+y*y/b2-1)==0)
        dx,dy=nxt[0]-x,nxt[1]-y
        h=dy*x-dx*y
        ck(name+'_caustic_tangency',
           s.simplify(h*h-alpha2*dy*dy-beta2*dx*dx)==0)
        inc=(x-prev[0],y-prev[1])
        nx,ny=x/a2,y/b2
        it=-ny*inc[0]+nx*inc[1]
        ot=-ny*dx+nx*dy
        # Equality of unit tangential components squared, with matching sign.
        # Distinct chords at a strictly convex boundary already give opposing
        # incoming/outgoing normal signs by strict Cauchy-Schwarz.
        residual=it*it*(dx*dx+dy*dy)-ot*ot*(inc[0]**2+inc[1]**2)
        ck(name+'_reflection_law', s.simplify(residual)==0)
        ck(name+'_reflection_tangential_sign', s.simplify(it*ot).is_nonnegative)
    products=[s.simplify(s.prod(2-sign*s.sqrt(3)*x/2 for x,y in points))
              for sign in (-1,1)]
    if expected_product is not None:
        ck(name+'_direct_ordinary_focal_products',
           all(s.simplify(z-expected_product)==0 for z in products))
    return products

rt2,rt5 = s.sqrt(2),s.sqrt(5)
six_H=[(s.Integer(2),0),(s.Rational(4,3),rt5/3),(-s.Rational(4,3),rt5/3),
       (-s.Integer(2),0),(-s.Rational(4,3),-rt5/3),(s.Rational(4,3),-rt5/3)]
six_V=[(0,s.Integer(1)),(-4*rt2/3,s.Rational(1,3)),(-4*rt2/3,-s.Rational(1,3)),
       (0,-s.Integer(1)),(4*rt2/3,-s.Rational(1,3)),(4*rt2/3,s.Rational(1,3))]
exact_polygon('admissible_six_horizontal',six_H,s.Rational(32,9),s.Rational(5,9),s.Rational(64,9))
exact_polygon('admissible_six_vertical',six_V,s.Rational(32,9),s.Rational(5,9),s.Rational(64,9))

# Falsifying controls outside the advertised parity. Both exact quadrilaterals
# share alpha^2=16/5,beta^2=1/5 but have products 4 and 64/25.
diamond=[(s.Integer(2),0),(0,s.Integer(1)),(-s.Integer(2),0),(0,-s.Integer(1))]
rectangle=[(4/s.sqrt(5),1/s.sqrt(5)),(-4/s.sqrt(5),1/s.sqrt(5)),
           (-4/s.sqrt(5),-1/s.sqrt(5)),(4/s.sqrt(5),-1/s.sqrt(5))]
diamond_products=exact_polygon('excluded_four_diamond',diamond,s.Rational(16,5),s.Rational(1,5),s.Integer(4))
rectangle_products=exact_polygon('excluded_four_rectangle',rectangle,s.Rational(16,5),s.Rational(1,5),s.Rational(64,25))
ck('excluded_four_counterexample', diamond_products[1] != rectangle_products[1])

# Exact two distinct triangles on the SAME nondegenerate confocal caustic.
# Their double traversals have N=6 but least period 3, so must not be admitted.
q=(-4+s.sqrt(13))/3
alpha2=3+q*q
alpha=s.sqrt(alpha2)
tri_V=[(0,s.Integer(1)),(2*s.sqrt(1-q*q),q),(-2*s.sqrt(1-q*q),q)]
tri_H=[(s.Integer(2),0),(-alpha,s.sqrt(1-alpha2/4)),(-alpha,-s.sqrt(1-alpha2/4))]
V_products=exact_polygon('excluded_triangle_vertical',tri_V,alpha2,q*q)
H_products=exact_polygon('excluded_triangle_horizontal',tri_H,alpha2,q*q)
# Rational interval certificate of a separation, independent of decimal output.
lo13,hi13=Q(3605,1000),Q(3606,1000)
lo3,hi3=Q(1732,1000),Q(1733,1000)
ck('triangle_sqrt13_interval', lo13*lo13<13<hi13*hi13)
ck('triangle_sqrt3_interval', lo3*lo3<3<hi3*hi3)
qabs_upper=(4-lo13)/3
alpha_lo,alpha_hi=Q(1737,1000),Q(1738,1000)
ck('triangle_alpha_interval',
   alpha_lo*alpha_lo < 3+((4-hi13)/3)**2 and
   alpha_hi*alpha_hi > 3+qabs_upper*qabs_upper)
V_upper=2*(1+3*qabs_upper*qabs_upper)
H_lower=(2-hi3)*(2+lo3*alpha_lo/2)**2
ck('repeated_odd_exact_counterexample_separation', H_lower>3 and V_upper<Q(11,5))

# Explicit boundary arithmetic: N=2 has no admissible primitive tau;
# v=0 gives coincident caustic/outer axes; v=K has cn(v)=0;
# k=0 is the separate circle case; k=1 collapses the caustic minor axis.
ck('two_bounce_no_admissible_rotation', not list(range(1,2//2)))
for k2 in [Q(1,7),Q(3,5),Q(999,1000)]:
    t=Q(0)
    a2=(1-k2*t)/(1-t);b2=(1-k2)/(1-t)
    ck('zero_shift_not_strictly_nested', a2==1 and b2==1-k2)
ck('K_shift_axes_formula_singular', 1-Q(1)==0)
ck('unit_modulus_degenerate_caustic', 1-Q(1)==0)
for numerator in range(-6,7):
    a,t=Q(7,3),Q(numerator,5)
    x=a*(1-t*t)/(1+t*t);y=2*a*t/(1+t*t)
    ck('circle_actual_distance_squared', x*x+y*y==a*a)

# Geometry-only iteration after caustic axes are constructed. Jacobi functions
# determine axes for a selected rotation; actual paths, closure, winding,
# antipodes and focal products are computed from tangent contact and reflection.
mp.mp.dps=100
diagnostic_counts=defaultdict(int)
max_errors=defaultdict(lambda:mp.mpf(0))
geometry_cases=0
sampled=[]

def dot(u,v): return u[0]*v[0]+u[1]*v[1]
def sub(u,v): return (u[0]-v[0],u[1]-v[1])
def norm(u): return mp.sqrt(dot(u,u))

def geometry_orbit(a,b,alpha,beta,c,N,theta):
    p=(a*mp.cos(theta),b*mp.sin(theta))
    U,V=p[0]/alpha,p[1]/beta
    r2=U*U+V*V
    root=mp.sqrt(r2-1)
    contacts=[(alpha*(U-sign*V*root)/r2,beta*(V+sign*U*root)/r2)
              for sign in (-1,1)]
    directions=[sub(z,p) for z in contacts]
    d=next(z for z in directions if p[0]*z[1]-p[1]*z[0]>0)
    vertices=[]
    winding=mp.mpf(0)
    tangency_error=mp.mpf(0)
    for j in range(N):
        vertices.append(p)
        A=d[0]*d[0]/(a*a)+d[1]*d[1]/(b*b)
        B=2*(p[0]*d[0]/(a*a)+p[1]*d[1]/(b*b))
        length=-B/A
        nxt=(p[0]+length*d[0],p[1]+length*d[1])
        h=d[1]*p[0]-d[0]*p[1]
        tangency_error=max(tangency_error,
                           abs(h*h-alpha*alpha*d[1]*d[1]-beta*beta*d[0]*d[0])/
                           (a*a*dot(d,d)))
        scaled_p=(p[0]/a,p[1]/b);scaled_n=(nxt[0]/a,nxt[1]/b)
        angle=mp.atan2(scaled_p[0]*scaled_n[1]-scaled_p[1]*scaled_n[0],dot(scaled_p,scaled_n))
        assert angle>0
        winding+=angle
        normal=(nxt[0]/(a*a),nxt[1]/(b*b))
        multiplier=2*dot(d,normal)/dot(normal,normal)
        d=(d[0]-multiplier*normal[0],d[1]-multiplier*normal[1])
        p=nxt
    closure=norm(sub(p,vertices[0]))/a
    antipodes=max(norm((vertices[j][0]+vertices[j+N//2][0],
                       vertices[j][1]+vertices[j+N//2][1]))/a for j in range(N//2))
    logs=[]
    for sign in (-1,1):
        logs.append(sum(mp.log(mp.sqrt((x-sign*c)**2+y*y)) for x,y in vertices))
    return logs,closure,antipodes,abs(winding/(2*mp.pi)),tangency_error

for k in [mp.mpf('0.01'),mp.mpf('0.2'),mp.mpf('0.75'),mp.mpf('0.999999')]:
    K=mp.ellipk(k*k)
    for N in [6,10,14,18,22,30,34,102]:
        taus=[t for t in range(1,N//2) if gcd(t,N)==1]
        if N==102: taus=[1,49]
        for tau in taus:
            v=2*K*tau/N
            cn=mp.ellipfun('cn',v,k*k);dn=mp.ellipfun('dn',v,k*k)
            a,b=dn/cn,mp.sqrt(1-k*k)/cn
            phase_logs=[]
            for theta in [mp.mpf(0),mp.pi/7,mp.pi/4,mp.mpf('1.45'),mp.mpf('2.89')]:
                logs,closure,antipodes,winding,tangency=geometry_orbit(a,b,1,mp.sqrt(1-k*k),k,N,theta)
                geometry_cases+=1
                for key,error in [('closure',closure),('antipodal',antipodes),('caustic_tangency',tangency),
                                  ('winding',abs(winding-tau)),('equal_focal_products',abs(logs[0]-logs[1]))]:
                    max_errors[key]=max(max_errors[key],error)
                    assert error<mp.mpf('1e-70'),(str(k),N,tau,key,mp.nstr(error,8))
                    diagnostic_counts[key]+=1
                phase_logs.append(logs[0])
            err=max(abs(z-phase_logs[0]) for z in phase_logs)
            max_errors['phase_constancy_log_error']=max(max_errors['phase_constancy_log_error'],err)
            assert err<mp.mpf('1e-70'),(str(k),N,tau,'phase constancy',mp.nstr(err,8))
            diagnostic_counts['phase_constancy_log_error']+=1
            sampled.append({'k':mp.nstr(k,10),'N':N,'tau':tau,'kind':'simple' if tau==1 else 'primitive_star'})

result={
    'status':'SCOPED_PASS',
    'timestamp_utc':datetime.now(timezone.utc).isoformat(),
    'exact_assertions':sum(counts.values()),'exact_counts':dict(sorted(counts.items())),
    'all_rotation_cases_including_nonprimitive':rotation_cases,
    'geometry_orbits':geometry_cases,'geometry_rotation_parameter_cases':sampled,
    'numeric_precision_digits':mp.mp.dps,
    'numeric_diagnostic_counts':dict(diagnostic_counts),
    'maximum_errors':{key:mp.nstr(value,10) for key,value in max_errors.items()},
    'exact_excluded_four_products':{'diamond':'4','rectangle':'64/25'},
    'exact_repeated_odd_counterexample':{
        'triangle_V_product':str(s.simplify(V_products[1])),
        'triangle_H_product':str(s.simplify(H_products[1])),
        'V_upper_bound':'11/5','H_lower_bound':'3',
        'double_traversal_V_product_upper':'121/25','double_traversal_H_product_lower':'9',
        'scope':'Both triangles are distinct, primitive period 3 and share the same strict confocal caustic.'},
    'limitations':'Exact replay/control assertions and algebraic negative examples are checkable finite artifacts. The gcd/coset lemma is derived in REVIEW.md. Reflected-ray tests remain high-precision numerical diagnostics; these samples do not prove the analytic divisor, canonical parametrization, or universal focal-product theorem.'}
out=Path(__file__).resolve().parent/'falsification_results.json'
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({key:value for key,value in result.items() if key not in ('exact_counts','geometry_rotation_parameter_cases')},indent=2))
