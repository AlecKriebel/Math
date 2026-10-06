"""Finite corroboration only; invoke through the trusted external bootstrap."""
if globals().get('_BUNDLE_VERIFIED') != 'height-counts-30002439-v1':
    raise SystemExit('Direct execution/import forbidden: use the external bootstrap')
import sys
if not sys.flags.isolated or not sys.flags.no_site:
    raise SystemExit('Requires python -I -S')
import itertools
import json
import math
from fractions import Fraction

checks = {}
def require(condition, label):
    if not condition:
        raise RuntimeError(label)

def primitive(v):
    g=math.gcd(*v)
    require(g>0, 'zero projective vector')
    w=tuple(x//g for x in v)
    return w if next(x for x in w if x)>0 else tuple(-x for x in w)

def height(v):
    return max(map(abs,primitive(v)))

def compositions(total, length):
    if length==1:
        yield (total,)
    else:
        for i in range(total+1):
            for tail in compositions(total-i,length-1):
                yield (i,)+tail

def veronese(v,d):
    return tuple(math.prod(x**e for x,e in zip(v,a)) for a in compositions(d,len(v)))

# Coordinate selection need not preserve primitivity, but never raises height.
c=0
for length in range(2,5):
    for v in itertools.product(range(-2,3),repeat=length):
        if not any(v):
            continue
        for size in range(1,length+1):
            for I in itertools.combinations(range(length),size):
                w=tuple(v[i] for i in I)
                if any(w):
                    require(height(w)<=height(v),'coordinate selection height')
                    c+=1
checks['coordinate_subvector_height_cases']=c

# Every monomial is checked, including all pure powers.
c=0
for n in range(1,4):
    points={primitive(v) for v in itertools.product(range(-3,4),repeat=n+1) if any(v)}
    for d in range(1,5):
        require(len(tuple(compositions(d,n+1)))==math.comb(n+d,d),'section dimension')
        for p in points:
            q=veronese(p,d)
            require(math.gcd(*q)==1,'Veronese primitivity')
            require(height(q)==height(p)**d,'Veronese height identity')
            c+=1
checks['veronese_height_cases']=c

# Distinct projective images and exact height-threshold counts on finite boxes.
c=0
for n in (1,2):
    points={primitive(v) for v in itertools.product(range(-4,5),repeat=n+1) if any(v)}
    for d in range(1,4):
        image_set={primitive(veronese(p,d)) for p in points}
        require(len(image_set)==len(points),'Veronese finite injectivity')
        for B in range(1,4**d+1):
            source=sum(height(p)**d<=B for p in points)
            target=sum(height(q)<=B for q in image_set)
            require(source==target,'Veronese threshold count')
            c+=1
checks['veronese_count_thresholds']=c

c=0
for n in range(1,5):
    for d in range(1,6):
        for T in range(1,21):
            x=(T,1)+(0,)*(n-1)
            Ax=(x[0]-T*x[1],)+x[1:]
            require(height(x)==T and height(veronese(Ax,d))==1,'shear obstruction')
            c+=1
checks['shear_cases']=c

c=0
for T in range(1,101):
    coprime=sum(math.gcd(a,b)==1 for a in range(1,T+1) for b in range(1,T+1))
    require(4*coprime>=T*T,'coprime-pair lower bound')
    for n in range(1,5):
        require(4*coprime*(T+1)**(n-1)>=T**(n+1),'projective lower bound')
        c+=1
checks['sharpness_lower_bound_cases']=c

c=0
for d in range(2,101):
    target=Fraction(3,d)
    obtained=Fraction(3,2*d)+Fraction(2,d)
    require(obtained==Fraction(7,2*d),'surface exponent sum')
    require(obtained-target==Fraction(1,2*d)>0,'surface exponent gap')
    c+=1
checks['surface_exponent_cases']=c
require(Fraction(43,28)-Fraction(3,2)==Fraction(1,28),'quadratic surface gap')
checks['quadratic_surface_gap']='1/28'
c=0
for n in range(2,31):
    for d in range(2,31):
        require(d**n>=4,'dimension-growth degree hypothesis')
        require(Fraction(n)-Fraction(n+1,d)>0,'dimension-growth gap')
        c+=1
checks['general_dimension_growth_cases']=c
print(json.dumps({'problem_id':30002439,'result':'PASS','claims':'Finite arithmetic corroboration only; general conjecture unresolved','checks':checks},sort_keys=True,indent=2))
