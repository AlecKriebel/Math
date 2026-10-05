#!/usr/bin/env python3
"""Reviewer-built finite controls. These do not prove infinite-dimensional claims.

No author functions are imported. Default execution compares saved results and
writes no files. --write intentionally regenerates INDEPENDENT_RESULTS.json.
Requires Python 3 and mpmath 1.3.0.
"""
import json
import sys
from pathlib import Path
import mpmath as m

m.mp.dps = 65
HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def near(x, y, tol=m.mpf('1e-48')):
    return abs(x-y) < tol * max(1, abs(x), abs(y))


def out(x):
    return m.nstr(x, 30)


def dot(a, b):
    return a[0]*b[0]+a[1]*b[1]


def cross(a, b):
    return a[0]*b[1]-a[1]*b[0]


def sub(a, b):
    return (a[0]-b[0], a[1]-b[1])


def turn_angles(vertices):
    """Exterior angles from consecutive polygon edges, not arctangent formulas."""
    ans = []
    for i, x in enumerate(vertices):
        before = sub(x, vertices[i-1])
        after = sub(vertices[(i+1) % len(vertices)], x)
        angle = m.atan2(cross(before, after), dot(before, after))
        require(0 < angle < m.pi, 'Polygon must be strictly convex and CCW')
        ans.append(angle)
    require(near(sum(ans), 2*m.pi), 'Turning angles must total 2 pi')
    return ans


def normal_angles(vertices):
    ans = []
    for i, x in enumerate(vertices):
        edge = sub(vertices[(i+1) % len(vertices)], x)
        angle = m.atan2(-edge[0], edge[1])
        if ans:
            while angle <= ans[-1]:
                angle += 2*m.pi
        ans.append(angle)
    return ans


def entropy(vertices):
    """Integrate log support over each actual normal-fan interval."""
    normals = normal_angles(vertices)
    total = m.mpf(0)
    for i, x in enumerate(vertices):
        left = normals[i-1] if i else normals[-1]-2*m.pi
        right = normals[i]
        total += m.quad(lambda z: m.log(x[0]*m.cos(z)+x[1]*m.sin(z)),
                        [left, (left+right)/2, right])
    return total/(2*m.pi)


def moved(vertices, weights, t):
    return [(x*m.exp(t*g), y*m.exp(t*g))
            for (x, y), g in zip(vertices, weights)]


def rank_entropy(n, k, t):
    """Independent angular integral: R=sin(theta), |P_perp U|=cos(theta)."""
    beta = m.beta(m.mpf(k)/2, m.mpf(n-k)/2)
    cutoff = m.atan(t)
    return (2/beta)*m.quad(
        lambda z: m.sin(z)**(k-1)*m.cos(z)**(n-k-1)
                  *m.log(t*m.cos(z)/m.sin(z)), [0, cutoff])


def run():
    checks = 0
    # Different route to all constants: integrate over the first-coordinate law.
    constants = []
    for n in [2, 3, 4, 5, 8, 16]:
        beta = m.beta(m.mpf(1)/2, m.mpf(n-1)/2)
        avg_log = (2/beta)*m.quad(
            lambda z: m.cos(z)**(n-2)*m.log(m.sin(z)), [0, m.pi/2])
        expected = (m.digamma(m.mpf(1)/2)-m.digamma(m.mpf(n)/2))/2
        require(near(avg_log, expected), 'Entropy constant mismatch')
        d = 2/beta
        threshold = 1/(1+d)
        require(threshold > m.exp(avg_log), 'Sampled improvement lost')
        t = m.mpf('1e-9')
        numeric = rank_entropy(n, 1, t)/t
        require(abs(numeric/d-1) < m.mpf('1e-16'), 'Line entropy derivative')
        constants.append({'n':n, 'old_bound':out(m.exp(avg_log)),
                          'new_line_threshold':out(threshold), 'd_n':out(d)})
        checks += 3
    # Noncircular lower-dimensional body: the rank estimate is uniform after
    # comparison with its inradius, not an assumption of roundness.
    rank_rows = []
    for n, k in [(3,2), (4,2), (4,3), (7,2), (7,3), (7,6)]:
        t = m.mpf('1e-7')
        coefficient = 2/(m.beta(m.mpf(k)/2,m.mpf(n-k)/2)*k*k)
        measured = rank_entropy(n,k,t)/t**k
        require(abs(measured/coefficient-1) < m.mpf('1e-12'), 'Rank entropy law')
        rank_rows.append({'n':n, 'k':k, 'coefficient':out(coefficient)})
        checks += 1
    # Direct polygon edges test the four-axis angles, including nonsymmetry.
    geometry_count = 0
    for a,b,c,d in [('1','2','3','4'),('0.02','5','0.3','2'),
                    ('8','0.1','2','0.01'),('1','1','1','1')]:
        a,b,c,d = map(m.mpf,(a,b,c,d))
        vertices=[(a,0),(0,b),(-c,0),(0,-d)]
        angles=turn_angles(vertices)
        formulas=[m.atan(a/b)+m.atan(a/d),m.atan(b/a)+m.atan(b/c),
                  m.atan(c/b)+m.atan(c/d),m.atan(d/a)+m.atan(d/c)]
        require(all(near(x,y) for x,y in zip(angles,formulas)), 'Axis geometry')
        for s in [m.mpf(1),m.mpf('1.1'),m.mpf(3)]:
            f=lambda z:(m.atan(z/b)+m.atan(z/d))/z**s
            require(m.diff(f,a)<0,'Opposite-mass monotonicity')
            checks+=1
        geometry_count+=1;checks+=1
    # Polygon normal-fan integration independently checks the nonsmooth
    # entropy variation. Both signs of perturbation are used.
    vertices=[(m.mpf(2),0),(m.mpf(1),1),(-m.mpf(1),1),
              (-m.mpf(2),0),(-m.mpf(1),-1),(m.mpf(1),-1)]
    g=list(map(m.mpf,['0.7','-0.3','0.2','0.7','-0.3','0.2']))
    angles=turn_angles(vertices)
    target=sum(w*z for w,z in zip(g,angles))/(2*m.pi)
    h=m.mpf('1e-18')
    derivative=(entropy(moved(vertices,g,h))-entropy(moved(vertices,g,-h)))/(2*h)
    require(near(derivative,target,m.mpf('1e-32')),'Nonsmooth first variation')
    checks+=1
    # Direct finite-support stationary condition, with arbitrary nonsmooth
    # origin-symmetric hexagon and negative p, verifies normalization/signs.
    masses=[]
    for s in [m.mpf(1),m.mpf('1.2'),m.mpf(2)]:
        radii=[m.sqrt(dot(v,v)) for v in vertices]
        unnorm=[z/r**s for z,r in zip(angles,radii)]
        total=sum(unnorm);mu=[z/total for z in unnorm]
        moment=sum(w*r**s for w,r in zip(mu,radii))
        balance=sum(w*r**s*gi for w,r,gi in zip(mu,radii,g))/moment-target
        require(near(balance,0),'Stationary measure balance')
        scale=total**(1/s)
        scaled=[z/(r*scale)**s for z,r in zip(angles,radii)]
        require(all(near(x,y) for x,y in zip(scaled,mu)),'Dilation normalization')
        masses.append({'s':out(s),'total_before_dilation':out(total),
                       'dilation':out(scale)})
        checks+=2
    # Oblique geometry from polygon edges, compared with stated closed form.
    oblique_count=0
    for alpha in [m.pi/30,m.pi/7,m.pi/3,m.pi/2]:
        for t in [m.mpf('0.001'),m.mpf('0.3'),m.mpf(1),m.mpf(4),m.mpf(100)]:
            vertices=[(t,0),(m.cos(alpha),m.sin(alpha)),
                      (-t,0),(-m.cos(alpha),-m.sin(alpha))]
            angles=turn_angles(vertices)
            beta=m.atan2(2*t*m.sin(alpha),1-t*t)
            require(near(angles[0],beta) and near(angles[1],m.pi-beta),'Oblique angle')
            checks+=1;oblique_count+=1
    # Boundary signature and p<-1 barrier via angular integration, not the
    # author's z-density integral. Negative second-order term at equality.
    boundary=[]
    for n in [2,3,4,8]:
        d=2/m.beta(m.mpf(1)/2,m.mpf(n-1)/2)
        t=m.mpf('1e-7')
        delta=m.log(1+d*t)-rank_entropy(n,1,t)
        require(delta<0,'Equality is not settled by positive first derivative')
        require(abs(delta/t**2+d*d/2)<m.mpf('1e-5'),'Equality second order')
        boundary.append({'n':n,'second_order_limit':out(-d*d/2)})
        checks+=2
    for s in [m.mpf('1.1'),m.mpf('1.5'),m.mpf(2),m.mpf(5)]:
        for mass in [m.mpf('0.01'),m.mpf('0.5'),m.mpf('0.99')]:
            # The asymptotic threshold can be very small when s is near 1.
            t=m.mpf('1e-60')
            delta=m.log1p((1-mass)/mass*t**s)/s-rank_entropy(2,1,t)
            require(delta<0,'p<-1 join obstruction')
            checks+=1
    # Aspect-family stationary minimum and three-root geometry.
    R=lambda s,x:m.exp(-s*x)*m.atan(m.exp(x))/m.atan(m.exp(-x))
    aspect=[]
    for s in [m.mpf('1.05'),m.mpf('1.1'),m.mpf('1.2')]:
        require(m.diff(lambda x:R(s,x),0)>0,'Central root positive slope')
        require(R(s,-100)>1 and R(s,-m.mpf('0.01'))<1,'Left outer root bracket')
        require(R(s,m.mpf('0.01'))>1 and R(s,100)<1,'Right outer root bracket')
        aspect.append({'s':out(s),'derivative_at_unit_aspect':out(4/m.pi-s)})
        checks+=3
    for s in [m.mpf('1.3'),m.mpf(2),m.mpf(4)]:
        dd=s/4-1/m.pi
        require(dd>0,'Strict aspect-family minimum')
        checks+=1
    # The proof's threshold is a supremum for <= c, not an attained maximum.
    t=m.mpf(1)
    require(near((m.atan(t)/(t*m.atan(1/t)))/(1+m.atan(t)/(t*m.atan(1/t))),m.mpf('.5')),
            'Equal diamond pair mass')
    checks+=1
    return {'schema':'independent-negative-p-controls-v1','status':'PASS',
            'kind':'finite numerical controls; deductive audit is separate',
            'checks':checks,'precision_decimal_digits':m.mp.dps,
            'constants':constants,'rank_entropy':rank_rows,
            'nonsymmetric_axis_cases':geometry_count,
            'normal_fan_variation':{'predicted':out(target),'computed':out(derivative)},
            'dilation_controls':masses,'oblique_cases':oblique_count,
            'zero_first_order_boundary':boundary,'three_root_controls':aspect,
            'full_problem_solved':False}


if __name__=='__main__':
    result=json.dumps(run(),indent=2,sort_keys=True)+'\n'
    target=HERE/'INDEPENDENT_RESULTS.json'
    if sys.argv[1:]==['--write']:
        target.write_text(result)
    elif sys.argv[1:]:
        raise SystemExit('Usage: independent_checks.py [--write]')
    else:
        require(target.read_text()==result,'Saved independent results do not match replay')
    print('PASS: reviewer-built controls reproduce; no finite test substitutes for proof')
