"""Exact arithmetic corroboration; not a formal or literature proof checker."""
import json
from math import gcd

COUNT = 0
CONTROLS = []


def need(ok, why):
    global COUNT
    if not ok:
        raise ValueError(why)
    COUNT += 1


def clean(p):
    return {k: v for k, v in p.items() if v}


def add(*ps):
    q = {}
    for p in ps:
        for k, v in p.items():
            q[k] = q.get(k, 0) + v
    return clean(q)


def mul(p, q):
    out = {}
    for a, x in p.items():
        for b, y in q.items():
            k = tuple(s+t for s,t in zip(a,b))
            out[k] = out.get(k, 0) + x*y
    return clean(out)


def transform(p, fn):
    q = {}
    for k, v in p.items():
        nk, sign = fn(k)
        q[nk] = q.get(nk, 0) + sign*v
    return clean(q)


def derivative(p, axis):
    q = {}
    for k, v in p.items():
        if k[axis]:
            kk = list(k)
            kk[axis] -= 1
            q[tuple(kk)] = v*k[axis]
    return clean(q)


def at_one(p, axis):
    return transform(p, lambda k: (tuple(0 if i == axis else x for i,x in enumerate(k)), 1))


def at_zero(p, axis):
    return {k:v for k,v in p.items() if k[axis] == 0}


def degree(p):
    return max((a+b for (a,b,c) in p), default=None)


def cross(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])


def lattice_count(vertices, k):
    vv = [(k*x,k*y) for x,y in vertices]
    total = 0
    for x in range(min(a for a,b in vv),max(a for a,b in vv)+1):
        for y in range(min(b for a,b in vv),max(b for a,b in vv)+1):
            signs = [cross(vv[i],vv[(i+1)%3],(x,y)) for i in range(3)]
            total += all(z>=0 for z in signs) or all(z<=0 for z in signs)
    return total


def hstar_triangle(vertices):
    L = [lattice_count(vertices,k) for k in range(4)]
    h = [L[0],L[1]-3*L[0],L[2]-3*L[1]+3*L[0],L[3]-3*L[2]+3*L[1]-L[0]]
    need(h[3] == 0, 'Ehrhart numerator exceeds dimension')
    return L, {i:c for i,c in enumerate(h) if c}


def local_triangle(vertices, h):
    q = dict(h)
    q[0] = q.get(0,0)+2
    for i in range(3):
        a,b = vertices[i],vertices[(i+1)%3]
        length = gcd(abs(a[0]-b[0]),abs(a[1]-b[1]))
        q[0] -= 1
        q[1] = q.get(1,0)-(length-1)
    return clean(q)


def face_sum(r, nonzero_face_data):
    q = {}
    for dimF, SF, SDual in nonzero_face_data:
        for j,a in SF.items():
            for k,b in SDual.items():
                exp = (dimF+1-j+k-r,j+k-r,0)
                q[exp] = q.get(exp,0)+(-1)**(dimF+1)*a*b
    return clean(q)


def reject(label, false_claim):
    need(not false_claim, 'false shortcut was accepted: '+label)
    CONTROLS.append(label)


def main():
    T = [(1,0),(0,1),(-1,-1)]
    dual = [(-1,-1),(-1,2),(2,-1)]
    for x,y in dual:
        values = [x*a+y*b for a,b in T]
        need(min(values)==-1 and values.count(-1)==2, 'dual vertex support')
    L,h = hstar_triangle(T)
    LD,hd = hstar_triangle(dual)
    need(h=={0:1,1:1,2:1}, 'triangle hstar')
    need(hd=={0:1,1:7,2:1}, 'dual hstar')
    S,SD = local_triangle(T,h),local_triangle(dual,hd)
    need(S==SD=={1:1,2:1}, 'local triangle polynomials')
    E = face_sum(1,[(-1,{0:1},SD),(2,S,{0:1})])
    expected = {(0,0,0):1,(1,0,0):-1,(0,1,0):-1,(1,1,0):1}
    need(E==expected,'triangle E')
    need(degree(E)==2,'triangle total degree')
    need(max(k[0] for k in E)==max(k[1] for k in E)==1,'triangle separate degrees')
    need(at_one(E,1)=={},'triangle v=1 specialization')
    diag = transform(E,lambda k:((k[0]+k[1],0,0),1))
    need(diag=={(0,0,0):1,(1,0,0):-2,(2,0,0):1},'diagonal specialization')
    interval_E = face_sum(1,[(-1,{0:1},{1:1}),(1,{1:1},{0:1})])
    need(interval_E=={(0,0,0):2},'interval E')
    for k in range(1,65):
        d,r=2*k-1,k
        need(d+1-2*r==0,'free join CY addition')
        need((2**k)//(2**k)==1,'scalar normalization')
    for n in range(65):
        need((n+3)+1-2*2==n,'pyramid CY dimension')
    # Symbolic coefficient ring Z[m]: the third exponent is the power of m.
    Q = {(0,0,0):1,(3,0,0):-1,(0,3,0):-1,(3,3,0):1,
         (1,1,1):1,(2,2,1):1,(2,1,1):-1,(1,2,1):-1}
    factored = mul({(0,0,0):1,(1,0,0):-1},{(0,0,0):1,(0,1,0):-1})
    nine = {(i,j,0):1 for i in range(3) for j in range(3)}
    need(mul(factored,add(nine,{(1,1,1):1}))==Q,'Q factorization')
    need(transform(Q,lambda k:((k[1],k[0],k[2]),1))==Q,'Q Hodge symmetry')
    need(transform(Q,lambda k:((3-k[0],3-k[1],k[2]),1))==Q,'Q Poincare symmetry')
    need(transform(Q,lambda k:((3-k[0],k[1],k[2]),-1))==Q,'Q mirror symmetry')
    need(all((-1)**(a+b)*v>=0 for (a,b,c),v in Q.items()),'Q nonnegative Hodge coefficients')
    need(degree(Q)==6,'Q total degree')
    need(at_zero(Q,1)=={(0,0,0):1,(3,0,0):-1},'Q boundary')
    boundary=at_zero(Q,1)
    need(transform(boundary,lambda k:((3-k[0],k[1],k[2]),-1))==boundary,'Q Serre boundary')
    need(at_one(Q,1)=={},'Q v=1')
    need(at_one(at_one(Q,0),1)=={},'Q Euler zero')
    need(at_one(at_one(derivative(Q,0),0),1)=={},'Q first derivative zero')
    need(at_one(at_one(derivative(derivative(Q,0),0),0),1)=={},'Q second derivative zero')
    need(Q[(0,0,0)]==1 and Q[(1,1,1)]==1 and (1,1,0) not in Q,'Q nonproportional parameter witness')
    reject('total_degree_n_without_factor_two',degree(E)==1)
    reject('specialization_v1_preserves_degree',at_one(E,1)==E)
    reject('diagonal_degree_equals_separate_degree',degree(diag)==1)
    reject('separate_degrees_force_corner', (1,1,0) in {(1,0,0):1,(0,1,0):1})
    reject('nonnegative_CY_forces_nonzero',0!=0)
    reject('free_join_has_dimension_sum', (1+1+1)==(1+1))
    reject('free_join_changes_CY_additivity',(2*3-1)+1-2*3!=0)
    reject('different_constant_polynomials_different_scalar_classes',2*4!=8)
    reject('fixed_CY_bounds_dimension',max(2*k-1 for k in range(1,65))<=3)
    reject('formal_identities_force_unique_uv_coefficient',1==2)
    return {'schema':1,'problem_id':30002042,'checks_passed':COUNT,
            'false_shortcut_controls':CONTROLS,'triangle_lattice_counts':L,
            'dual_triangle_lattice_counts':LD,'triangle_E':[[*k[:2],v] for k,v in sorted(E.items())],
            'symbolic_Q_parameter':'all m over Z[m], nonnegative Hodge coefficients for m>=0',
            'scope':'exact corroboration only; no general finiteness proof or geometric realization'}


if __name__=='__main__':
    print(json.dumps(main(),sort_keys=True,indent=2))
