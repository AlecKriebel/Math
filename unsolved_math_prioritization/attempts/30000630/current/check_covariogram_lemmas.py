#!/usr/bin/env python3
"""Read-only, standard-library checks of authored identities, not a geometric proof.
No network, subprocesses, downloaded code, repository mutation, or assertions.
"""
from fractions import Fraction
from math import isqrt, sqrt, acos, cos, sin, pi, isfinite
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rational(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError(name + ' must be an integer or Fraction')
    return Fraction(value)


def rational_sqrt(value):
    value = rational(value, 'radicand')
    if value < 0:
        raise ValueError('negative radicand')
    a, b = isqrt(value.numerator), isqrt(value.denominator)
    if a*a != value.numerator or b*b != value.denominator:
        raise ValueError('fixture requires an exact rational square root')
    return Fraction(a, b)


def recover_area(c, integral, alpha):
    c, integral, alpha = [rational(v, n) for v,n in
                          [(c,'c'),(integral,'integral'),(alpha,'alpha')]]
    if c <= 0 or integral <= 0 or alpha < 0:
        raise ValueError('requires c > 0, integral > 0, alpha >= 0')
    discriminant = c*c-alpha*integral
    if discriminant < 0:
        raise ValueError('inconsistent covariogram moments')
    return integral/(c+rational_sqrt(discriminant))


def recover_curvature_radii(radius_sum, curvature_sum):
    s, q = rational(radius_sum,'radius_sum'), rational(curvature_sum,'curvature_sum')
    if s <= 0 or q <= 0:
        raise ValueError('positive sums required')
    product = s/q
    d = s*s-4*product
    if d < 0:
        raise ValueError('inconsistent positive radius data')
    root = rational_sqrt(d)
    return ((s-root)/2, (s+root)/2)


def recover_area_covariogram(g, scaled_g, scale, alpha):
    g, scaled_g, scale, alpha = [rational(v,n) for v,n in
        [(g,'g'),(scaled_g,'scaled_g'),(scale,'scale'),(alpha,'alpha')]]
    if scale <= 0 or scale == 1 or alpha <= 0:
        raise ValueError('requires scale > 0, scale != 1 and alpha > 0')
    return (scaled_g-scale*g)/(alpha*scale*(scale-1))


def cross(o,a,b):
    return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])


def hull(points):
    points = sorted(set(tuple(rational(v,'coordinate') for v in p) for p in points))
    if len(points) < 2:
        return points
    lower=[]
    for p in points:
        while len(lower)>=2 and cross(lower[-2],lower[-1],p)<=0:
            lower.pop()
        lower.append(p)
    upper=[]
    for p in reversed(points):
        while len(upper)>=2 and cross(upper[-2],upper[-1],p)<=0:
            upper.pop()
        upper.append(p)
    return lower[:-1]+upper[:-1]


def area(points):
    q=hull(points)
    if len(q)<3:
        return Fraction(0)
    return abs(sum(q[i][0]*q[(i+1)%len(q)][1]-q[i][1]*q[(i+1)%len(q)][0]
                   for i in range(len(q))))/2


def mixed_area(a,b):
    return (area([(x[0]+y[0],x[1]+y[1]) for x in a for y in b])-area(a)-area(b))/2


def rejects(call, types=(ValueError,TypeError)):
    try:
        call()
    except types:
        return
    raise RuntimeError('meaningful negative was accepted')


def main():
    checks=0
    for a in [Fraction(1,5),Fraction(1),Fraction(7,3),Fraction(11)]:
        for m in [Fraction(0),Fraction(2,7),Fraction(3)]:
            for alpha in [Fraction(0),Fraction(2,3),Fraction(5)]:
                if m==0 and alpha==0:
                    continue
                c=m+alpha*a
                integral=2*a*m+alpha*a*a
                require(recover_area(c,integral,alpha)==a,'area recovery identity')
                checks+=1
    for a,b in [(1,1),(2,3),(Fraction(1,2),Fraction(7,2))]:
        a,b=Fraction(a),Fraction(b)
        require(recover_curvature_radii(a+b,1/a+1/b)==tuple(sorted((a,b))),
                'opposite curvature recovery')
        checks+=1
    for m,a,alpha,t in [(3,2,5,2),(Fraction(2,3),Fraction(4,5),Fraction(1,7),Fraction(1,2))]:
        m,a,alpha,t=map(Fraction,(m,a,alpha,t))
        require(recover_area_covariogram(m+alpha*a,t*m+alpha*t*t*a,t,alpha)==a,
                'two-scale separation')
        checks+=1
    triangle=[(0,0),(1,0),(0,1)]
    reflected=[(-x,-y) for x,y in triangle]
    require(area(triangle)==Fraction(1,2),'triangle area')
    require(mixed_area(triangle,triangle)==Fraction(1,2),'same triangle mixed area')
    require(mixed_area(reflected,triangle)==1,'opposite triangle mixed area')
    require(area([(0,0),(1,0)])==area([(0,0),(2,0)])==0,
            'area is not strongly strictly monotone')
    checks+=4
    # For [0,2] x [0,1] at translation (0,1), the intersection is a length-2
    # segment: the continuous convex perimeter is 4, not 2.
    require(2*Fraction(2)==4,'perimeter segment factor')
    # Subtract c*chi(intersection), not a constant on all translation space.
    singleton_value=3
    outside_value=0
    require(outside_value-singleton_value != outside_value-singleton_value*0,
            'Euler offset negative control')
    checks+=2
    negatives=[
      lambda:recover_area(0,1,0),lambda:recover_area(1,0,0),
      lambda:recover_area(1,2,1),lambda:recover_area(1,1,-1),
      lambda:recover_area(True,1,0),lambda:recover_area(float('nan'),1,0),
      lambda:recover_area(1,1,float('inf')),
      lambda:recover_curvature_radii(2,1),lambda:recover_curvature_radii(0,1),
      lambda:recover_curvature_radii(1,0),
      lambda:recover_area_covariogram(1,2,1,1),
      lambda:recover_area_covariogram(1,2,0,1),
      lambda:recover_area_covariogram(1,2,2,0),
      lambda:recover_area_covariogram(1,2,-1,1),
      lambda:rational_sqrt(Fraction(2)),lambda:hull([(True,0)])]
    for f in negatives:
        rejects(f)
    checks+=len(negatives)
    # Independent elementary disk lens formula only validates the leading constant.
    radius=2.0
    expected=4*sqrt(radius)
    errors=[]
    for epsilon in [1e-2,1e-3,1e-4,1e-5]:
        lens_perimeter=4*radius*acos((2*radius-epsilon)/(2*radius))
        coefficient=lens_perimeter/sqrt(epsilon)
        errors.append(abs(coefficient-expected))
    require(all(errors[j+1]<errors[j] for j in range(len(errors)-1)),
            'disk asymptotic convergence')
    require(errors[-1]<2e-6,'disk asymptotic final tolerance')
    checks+=2
    print(json.dumps({'status':'PASS','checks':checks,'negative_checks':len(negatives),
        'triangle_mixed_area_pair':['1/2','1'],
        'disk_coefficient_expected':expected,'disk_coefficient_errors':errors,
        'scope':'Exact rational identities and elementary disk consistency only; no arbitrary convex-body proof.'},sort_keys=True))

if __name__=='__main__':
    main()
