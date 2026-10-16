#!/usr/bin/env python3
"""Independent exact physical controls, without Jacobi coordinates or fitted traces."""
import datetime
import json
from pathlib import Path
import sympy as S

R = S.Rational
sqrt = S.sqrt
groups = {}

def reduce(x):
    return S.simplify(S.radsimp(S.expand(x)))

def check(group, value):
    assert value is True or value == S.true, (group, value)
    groups[group] = groups.get(group, 0) + 1

def zero(group, value):
    check(group, reduce(value) == 0)

def positive(group, value):
    check(group, reduce(value).is_positive is True)

def dot(p, q):
    return p[0]*q[0] + p[1]*q[1]

def det(p, q):
    return p[0]*q[1] - p[1]*q[0]

def sub(p, q):
    return tuple(reduce(x-y) for x,y in zip(p,q))

def area(p):
    return reduce(sum(det(p[i], p[(i+1)%len(p)]) for i in range(len(p)))/2)

def physical(name, points, lam):
    p = [tuple(S.sympify(x) for x in z) for z in points]
    positive('strict_caustic_positive_lambda', lam)
    positive('strict_caustic_positive_minor_axis', 1-lam)
    outer = []
    feet = []
    n = [(x/4,y) for x,y in p]
    for i,z in enumerate(p):
        zero('on_outer_ellipse', z[0]**2/4+z[1]**2-1)
        d = sub(p[(i+1)%len(p)], z)
        positive('nonzero_chord', dot(d,d))
        m = (d[1],-d[0])
        h = dot(m,z)
        zero('same_caustic_tangency_discriminant', h*h-(4-lam)*m[0]**2-(1-lam)*m[1]**2)
        contact_parameter = reduce(-(z[0]*d[0]/(4-lam)+z[1]*d[1]/(1-lam))/(d[0]**2/(4-lam)+d[1]**2/(1-lam)))
        positive('contact_inside_chord_lower', contact_parameter)
        positive('contact_inside_chord_upper', 1-contact_parameter)
        incoming = sub(z, p[(i-1)%len(p)])
        reflected = tuple(reduce(incoming[j]-2*dot(incoming,n[i])/dot(n[i],n[i])*n[i][j]) for j in (0,1))
        zero('exact_specular_reflection', det(reflected,d))
        positive('reflection_forward_direction', dot(reflected,d))
        nj = n[(i+1)%len(p)]
        de = reduce(det(n[i], nj))
        check('finite_outer_vertex', de != 0)
        o = (reduce((nj[1]-n[i][1])/de),reduce((n[i][0]-nj[0])/de))
        q = tuple(reduce(x/dot(n[i],n[i])) for x in n[i])
        zero('outer_tangent_incidence_first', dot(n[i],o)-1)
        zero('outer_tangent_incidence_second', dot(nj,o)-1)
        zero('foot_on_outer_side', dot(n[i],q)-1)
        zero('foot_perpendicular_to_outer_side', det(n[i],q))
        outer.append(o)
        feet.append(q)
    a,b = area(outer),area(feet)
    product = reduce(a*b)
    for pp,qq in ((list(reversed(outer)),list(reversed(feet))), (outer*3,feet*3)):
        factor = 1 if len(pp)==len(outer) else 9
        zero('traversal_reversal_or_repetition', area(pp)*area(qq)-factor*product)
    return {'name': name, 'period': len(p), 'lambda': str(lam), 'vertices': [[str(x) for x in z] for z in p], 'outer_signed_area': str(a), 'center_pedal_signed_area': str(b), 'product': str(product)}

def main():
    lam3 = (8*sqrt(13)-20)/9
    x = 2*(1-sqrt(13))/3
    y = sqrt(1-x*x/4)
    z = (sqrt(13)-4)/3
    x2 = 2*sqrt(1-z*z)
    triangle_h = physical('new_three_period_horizontal', [(2,0),(x,y),(x,-y)],lam3)
    triangle_v = physical('new_three_period_vertical', [(0,1),(-x2,z),(x2,z)],lam3)
    zero('two_exact_three_period_same_caustic_products',S.sympify(triangle_h['product'])-S.sympify(triangle_v['product']))
    four_h = physical('new_excluded_four_period_diamond',[(2,0),(0,1),(-2,0),(0,-1)],R(4,5))
    four_v = physical('new_excluded_four_period_rectangle',[(4/sqrt(5),1/sqrt(5)),(-4/sqrt(5),1/sqrt(5)),(-4/sqrt(5),-1/sqrt(5)),(4/sqrt(5),-1/sqrt(5))],R(4,5))
    check('excluded_four_period_product_32',four_h['product']=='32')
    check('excluded_four_period_product_50',four_v['product']=='50')
    six_h = physical('author_six_period_horizontal_physical_validation',[(2,0),(R(4,3),sqrt(5)/3),(-R(4,3),sqrt(5)/3),(-2,0),(-R(4,3),-sqrt(5)/3),(R(4,3),-sqrt(5)/3)],R(4,9))
    six_v = physical('author_six_period_vertical_physical_validation',[(0,1),(-4*sqrt(2)/3,R(1,3)),(-4*sqrt(2)/3,-R(1,3)),(0,-1),(4*sqrt(2)/3,-R(1,3)),(4*sqrt(2)/3,R(1,3))],R(4,9))
    check('author_six_period_both_products_40',six_h['product']==six_v['product']=='40')
    result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','exact_assertions':sum(groups.values()),'groups':groups,'families':[triangle_h,triangle_v,four_h,four_v,six_h,six_v],'versions':{'sympy':S.__version__},'scope':'Six exact closed physical polygons in E:x^2/4+y^2=1. Chord tangency at an interior point and forward specular reflection checked at every edge and vertex, with true tangent intersections and perpendicular feet. New two-triangle equality and distinct excluded four-period products32/50. Six-period witnesses credited to original PR148 through the submitted PR209; validated physically here, not claimed independent discoveries. Finite controls are not the universal proof.'}
    out=Path(__file__).resolve().parent/'root_reproduction_01/ROOT_EXACT_GEOMETRY.json'
    assert not out.exists()
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
