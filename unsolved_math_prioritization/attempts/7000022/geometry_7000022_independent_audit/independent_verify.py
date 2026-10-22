#!/usr/bin/env python3
"""Independent exact controls for the scoped audit of Problem 7000022.

Standard library only; does not import or execute the author's verifier.
Finite checks complement, and do not replace, the analytic audit.
Optional --author DIRECTORY cross-checks the author's saved certificates.
"""
from fractions import Fraction as F
from math import isqrt
from itertools import permutations, combinations, product
from collections import Counter
from pathlib import Path
import argparse
import json

# Intervals are immutable pairs, with rational endpoints.
def scalar(x):
    return (F(x), F(x))
def add(a, b):
    return (a[0] + b[0], a[1] + b[1])
def neg(a):
    return (-a[1], -a[0])
def sub_i(a, b):
    return add(a, neg(b))
def mul(a, b):
    p = [x*y for x in a for y in b]
    return (min(p), max(p))
def div(a, b):
    assert b[0] > 0 or b[1] < 0
    return mul(a, (1/b[1], 1/b[0]))
def scale(a, k):
    return mul(a, scalar(k))
def summation(v):
    result = scalar(0)
    for x in v:
        result = add(result, x)
    return result
def root(x):
    x = F(x)
    assert x >= 0
    unit = 10**60
    n = isqrt(x.numerator*unit*unit // x.denominator)
    a, b = F(n, unit), F(n+1, unit)
    assert a*a <= x < b*b
    return (a, a if a*a == x else b)
def positive(a):
    return a[0] > 0

def arctan_reciprocal(q):
    # Independent identity: atan(1/2) + atan(1/3) = pi/4.
    # Positive arguments; sum is in (0,pi/2), and tan(sum)=1 exactly.
    n = 160
    s = sum((F((-1)**k, (2*k+1)*q**(2*k+1)) for k in range(n)), F())
    r = F((-1)**n, (2*n+1)*q**(2*n+1))
    return (min(s, s+r), max(s, s+r))

def vec(a, b):
    return tuple(F(y)-F(x) for x, y in zip(a, b))
def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F())
def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def norm(a):
    return root(dot(a, a))
def area_triangle(v, ids):
    a, b, c = (v[i] for i in ids)
    return scale(norm(cross(vec(a,b), vec(a,c))), F(1,2))
def cycle_edges(t):
    return list(zip(t, t[1:]+t[:1]))
def canonical_cycle(t):
    k = t.index(min(t))
    a = t[k:]+t[:k]
    return min(a, (a[0],)+tuple(reversed(a[1:])))
def all_cycles(n):
    return sorted({canonical_cycle(p) for p in permutations(range(n))})
def perimeter(v, t):
    return summation(norm(vec(v[a],v[b])) for a,b in cycle_edges(t))

# Rational planar convex hull: tests projected areas without the face formula.
def turn(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def hull2(points):
    p = sorted(set(points))
    if len(p)<3:
        return p
    sides=[]
    for seq in (p, list(reversed(p))):
        s=[]
        for x in seq:
            while len(s)>=2 and turn(s[-2],s[-1],x)<=0:
                s.pop()
            s.append(x)
        sides.append(s[:-1])
    return sides[0]+sides[1]
def shoelace(v):
    if len(v)<3:
        return F()
    return abs(sum((a[0]*b[1]-a[1]*b[0] for a,b in zip(v,v[1:]+v[:1])), F()))/2

def frame(a,b):
    q=1+a*a+b*b
    u=(2*a/q,2*b/q,(1-a*a-b*b)/q)
    w=vec(u,(F(),F(),F(1)))
    if dot(w,w)==0:
        return (F(1),F(),F()),(F(),F(1),F()),u
    H=[[F(i==j)-2*w[i]*w[j]/dot(w,w) for j in range(3)] for i in range(3)]
    e=tuple(H[i][0] for i in range(3)); f=tuple(H[i][1] for i in range(3))
    assert dot(e,e)==dot(f,f)==dot(u,u)==1
    assert dot(e,f)==dot(e,u)==dot(f,u)==0
    return e,f,u

def projection_check(v,faces):
    n=0
    for a,b in product([F(),F(1,3),F(2,3),F(1),F(2)],repeat=2):
        e,f,u=frame(a,b)
        projected=shoelace(hull2([(dot(x,e),dot(x,f)) for x in v]))
        formula=sum((abs(dot(cross(vec(v[i],v[j]),vec(v[i],v[k])),u))/4 for i,j,k in faces),F())
        assert formula==projected
        n+=1
    return n

def padd(a,b):
    return [(a[k] if k<len(a) else F())+(b[k] if k<len(b) else F()) for k in range(max(len(a),len(b)))]
def pscale(a,k):
    return [x*k for x in a]
def pmul(a,b):
    c=[F()]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            c[i+j]+=x*y
    return c
def derivative(a):
    return [k*a[k] for k in range(1,len(a))] or [F()]
def average_z(a):
    return sum((x/F(k+1) for k,x in enumerate(a) if k%2==0),F())

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--author',type=Path)
    parser.add_argument('--output',type=Path,default=Path(__file__).with_name('INDEPENDENT_CHECK_RESULTS.json'))
    args=parser.parse_args()
    pi=scale(add(arctan_reciprocal(2),arctan_reciprocal(3)),4)
    assert F(314159265358979323846,10**20)<pi[0]<pi[1]<F(314159265358979323847,10**20)
    target=div(scalar(1),scale(pi,2)); mean=scale(pi,F(1,16)); projection=div(scalar(2),scale(pi,3))
    assert F(1,8)<target[0]<target[1]<mean[0]<mean[1]<projection[0]
    mean_square=scale(mul(pi,pi),F(1,16))
    assert F(1,2)<mean_square[0]<mean_square[1]<F(2,3)

    tetrahedra=[[(0,0,0),(1,0,0),(0,1,0),(0,0,1)]]
    for t in [F(1,10),F(1),F(3)]:
        tetrahedra.append([(1,0,0),(0,1,t),(-1,0,0),(0,-1,t)])
    tetra_count=0; projection_count=0
    for raw in tetrahedra:
        v=[tuple(map(F,p)) for p in raw]
        assert dot(vec(v[0],v[1]),cross(vec(v[0],v[2]),vec(v[0],v[3])))!=0
        faces=list(combinations(range(4),3))
        area=summation(area_triangle(v,f) for f in faces)
        for t in all_cycles(4):
            length=perimeter(v,t)
            assert area[1]<scale(mul(length,length),F(1,8))[0]
            tetra_count+=1
        projection_count+=projection_check(v,faces)
    assert tetra_count==12

    h=F(1,10)
    v=[(1,0,0),(0,1,0),(-1,0,0),(0,-1,0),(0,0,h),(0,0,-h)]
    v=[tuple(map(F,p)) for p in v]
    faces=[(pole,i,(i+1)%4) for pole in (4,5) for i in range(4)]
    area=summation(area_triangle(v,f) for f in faces)
    expected_area=scale(root(1+2*h*h),4)
    assert max(area[0],expected_area[0])<=min(area[1],expected_area[1])
    projection_count+=projection_check(v,faces)
    cycles=all_cycles(6)
    lengths={t:perimeter(v,t) for t in cycles}
    best_upper=min(x[1] for x in lengths.values())
    minimizers=[t for t,x in lengths.items() if x[0]<=best_upper]
    assert len(cycles)==60 and len(minimizers)==8
    pole_edge=lambda t: any({a,b}=={4,5} for a,b in cycle_edges(t))
    assert all(pole_edge(t) for t in minimizers)
    le=add(scalar(2*h),add(scale(root(1+h*h),2),scale(root(2),3)))
    assert all(max(lengths[t][0],le[0])<=min(lengths[t][1],le[1]) for t in minimizers)
    assert all(lengths[t][0]>le[1] for t in cycles if t not in minimizers)

    # Each pole-edge interior sample satisfies every octahedron facet strictly.
    # The analytic certificate is |z|/h<1 for every -h<z<h.
    for z in [h*F(k,10) for k in range(-9,10)]:
        assert abs(z)/h<1
    # All remaining minimizing edges are hull edges. Their interiors are disjoint.
    assert all(all(a>=4 or b>=4 or (a-b)%4 in (1,3) for a,b in cycle_edges(t)) for t in minimizers)
    d=scale(root(h*h+F(1,2)),2)
    midpoint=(F(1,2),F(1,2),F())
    midpoint_path=add(norm(vec(v[4],midpoint)),norm(vec(midpoint,v[5])))
    assert max(d[0],midpoint_path[0])<=min(d[1],midpoint_path[1])
    lb=add(scale(root(1+h*h),4),scale(root(2),2))
    intrinsic_lower={t:summation(d if {a,b}=={4,5} else norm(vec(v[a],v[b])) for a,b in cycle_edges(t)) for t in cycles}
    boundary_candidates=[t for t,x in intrinsic_lower.items() if x[0]<=lb[1]]
    assert len(boundary_candidates)==16
    assert all(not pole_edge(t) and all(a>=4 or b>=4 or (a-b)%4 in (1,3) for a,b in cycle_edges(t)) for t in boundary_candidates)
    assert all(intrinsic_lower[t][0]>lb[1] for t in cycles if t not in boundary_candidates)
    assert positive(sub_i(lb,le))
    assert area[1]<div(mul(le,le),scale(pi,2))[0]
    # Additional controls on both sides of the exact height threshold.
    threshold_cases=[]
    for hh in [F(1,100),F(1,10),F(1,3),F(1,2),F(1),F(10)]:
        adj=add(scalar(2*hh),add(scale(root(1+hh*hh),2),scale(root(2),3)))
        sep=add(scale(root(1+hh*hh),4),scale(root(2),2))
        expected=8*hh*hh<1
        assert (adj[1]<sep[0]) if expected else (sep[1]<adj[0])
        threshold_cases.append({'height':str(hh),'adjacent_poles_shorter':expected})

    square=[tuple(map(F,p)) for p in [(0,0,0),(1,0,0),(1,1,0),(0,1,0)]]
    square_planar=shoelace([(p[0],p[1]) for p in square]); square_surface=2*square_planar
    assert square_surface==F(4)**2/8==2
    projection_count+=projection_check(square,[(0,1,2),(0,2,3),(0,2,1),(0,3,2)])
    o=(F(),F(),F()); e=[(F(1),F(),F()),(F(),F(1),F()),(F(),F(),F(1))]
    walk=[o,e[0],o,e[1],o,e[2],o]
    tree_length=summation(norm(vec(a,b)) for a,b in zip(walk,walk[1:]))
    assert tree_length==scalar(6)
    assert all(cross(a,vec(a,b))==o for a,b in zip(walk,walk[1:]))
    tree_area=summation(area_triangle([o]+e,f) for f in combinations(range(4),3))
    assert tree_area[0]>0 and tree_area[1]<div(scalar(36),scale(pi,2))[0]

    # Exact integrated support-function identity for a convex quadratic example.
    # h(z)=2+z/4+P_2(z)/10; both curvature radii exceed 1.
    hp=[F(39,20),F(1,4),F(3,20)]
    dh=derivative(hp); ddh=derivative(dh)
    radius=padd(hp,pscale(pmul([F(),F(1)],dh),-1))
    radius2=padd(radius,pmul([F(1),F(),F(-1)],ddh))
    assert radius==[F(39,20),F(),F(-3,20)]
    assert radius2==[F(9,4),F(),F(-9,20)]
    integrated_det=average_z(pmul(radius,radius2))
    grad2=pmul([F(1),F(),F(-1)],pmul(dh,dh))
    energy=average_z(padd(pmul(hp,hp),pscale(grad2,F(-1,2))))
    assert integrated_det==energy==F(999,250)<4

    # Negative controls are false surrogate claims, explicitly rejected.
    negative={
      'jensen_second_moment_le_squared_mean': F(2,3)>mean_square[1],
      'sharp_length_only_projection_moment_le_half': mean_square[0]>F(1,2),
      'single_planar_area_is_continuous_surface_area': square_surface!=square_planar,
      'boundary_replacement_has_no_length_cost': lb[0]>le[1],
      'minimum_spanning_disk_controls_positive_hull_area': tree_area[0]>0,
      'surface_energy_has_plus_gradient_sign': average_z(padd(pmul(hp,hp),pscale(grad2,F(1,2))))!=integrated_det,
      'four_vertex_coefficient_improves_to_one_ninth': square_surface>F(16,9),
      'octahedron_is_a_counterexample_to_target': div(mul(le,le),scale(pi,2))[0]>area[1],
    }
    assert all(negative.values())
    certs={
      'pi':pi,'target_coefficient':target,'meanwidth_coefficient':mean,'projection_coefficient':projection,
      'meanwidth_factor_over_target':scale(mul(pi,pi),F(1,8)),
      'meanwidth_slack_threshold':sub_i(scalar(F(1,4)),div(scalar(1),mul(pi,root(2)))),
      'octahedron_euclidean_length':le,'octahedron_boundary_length':lb,'octahedron_gap':sub_i(lb,le),
      'octahedron_area':area,'octahedron_target_margin':sub_i(div(mul(le,le),scale(pi,2)),area),
      'tree_hull_area':tree_area,
    }
    crosschecks={}
    if args.author:
        saved=json.loads((args.author/'CHECK_RESULTS.json').read_text())
        for name,iv in certs.items():
            aa=saved['certificates'][name]; lo,hi=F(aa['lower']),F(aa['upper'])
            assert lo<=hi and max(lo,iv[0])<=min(hi,iv[1]),name
            assert abs(float((iv[0]+iv[1])/2)-aa['approximate_midpoint'])<1e-14,name
            crosschecks[name]='independent intervals overlap; displayed midpoint agrees'
        assert saved['checks']['tetrahedron_tours_checked']==tetra_count
        assert saved['checks']['octahedron_unoriented_tours']==len(cycles)
        assert saved['checks']['octahedron_minimizing_tours']==len(minimizers)
    # Keep certificates concise using outward 12-decimal rational rounding.
    def display(iv):
        n=10**12
        lo=(iv[0].numerator*n//iv[0].denominator)
        hi=-((-iv[1].numerator*n)//iv[1].denominator)
        assert F(lo,n)<=iv[0]<=iv[1]<=F(hi,n)
        return {'lower':str(F(lo,n)),'upper':str(F(hi,n)),'approximate_midpoint':float((iv[0]+iv[1])/2)}
    result={'problem_id':7000022,'audit_control_status':'PASS','full_target_resolved':False,
      'arithmetic':'rational intervals; 10^-60 radical enclosures; pi from independent atan(1/2)+atan(1/3) identity',
      'tetrahedron_tours':tetra_count,'octahedron_cycles':len(cycles),'euclidean_minimizers':len(minimizers),
      'boundary_minimizer_edge_cycles':len(boundary_candidates),'exact_projection_controls':projection_count,
      'support_function_integrated_identity':str(energy),'negative_controls_rejected':negative,
      'height_threshold_controls':threshold_cases,'minimizing_cycles':[list(t) for t in minimizers],
      'certificates':{k:display(v) for k,v in certs.items()},
      'limitations':['No mechanical certification of arbitrary curves or analytic compactness/approximation arguments.',
                    'Finite controls do not prove the full conjecture or assert novelty.']}
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    summary={k:result[k] for k in ['audit_control_status','full_target_resolved','tetrahedron_tours','octahedron_cycles','euclidean_minimizers','boundary_minimizer_edge_cycles','exact_projection_controls']}
    if args.author:
        summary['author_saved_certificate_crosschecks']=crosschecks
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    main()
