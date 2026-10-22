"""Exact finite diagnostics; the general implication is proved in DERIVATION.md."""
from fractions import Fraction as F
from itertools import product
import json


def dot(x, y):
    return sum(a*b for a, b in zip(x, y))


def sub(x, y):
    return tuple(a-b for a, b in zip(x, y))


def norm2(x):
    return dot(x, x)


def det3(rows):
    a,b,c=rows
    return (a[0]*(b[1]*c[2]-b[2]*c[1])
            -a[1]*(b[0]*c[2]-b[2]*c[0])
            +a[2]*(b[0]*c[1]-b[1]*c[0]))


def run_checks():
    # An exact local sign diagnostic, not a realization of a whole comparison.
    ni=(F(1),F(0),F(0)); nj=(F(3,5),F(4,5),F(0))
    mi=ni; mj=(F(4,5),F(3,5),F(0)); hi=F(2); hj=F(3)
    a=tuple(x/hi for x in ni); b=tuple(x/hj for x in nj)
    c=tuple(x/hi for x in mi); d=tuple(x/hj for x in mj)
    source=norm2(sub(a,b)); target=norm2(sub(c,d))
    gap=2*(dot(mi,mj)-dot(ni,nj))/(hi*hj)
    if not (source==F(29,180) and target==F(17,180) and source-target==gap==F(1,15)):
        raise ValueError('polar edge sign mismatch')
    if not (norm2(a)==norm2(c) and norm2(b)==norm2(d)):
        raise ValueError('equal radii mismatch')

    # A positively rescaled cube skeleton need not retain its face planes.
    cube=list(product([-1,1],repeat=3))
    scaled=[tuple(2*v for v in p) if p==(1,1,1) else p for p in cube]
    top=[(2,2,2),(-1,1,1),(-1,-1,1),(1,-1,1)]
    volume=det3([sub(q,top[0]) for q in top[1:]])
    if volume!=-4:
        raise ValueError('non-realization witness mismatch')
    # Every source cube face remains strictly on its designated side of 0
    # at both endpoints; positive interpolation gives the same for all t.
    for axis in range(3):
        for sign in [-1,1]:
            values=[sign*q[axis] for p,q in zip(cube,scaled) if p[axis]==sign]
            if min(values)<=0:
                raise ValueError('face half-space witness mismatch')

    # Orthogonal reflection/permutation preserves all pairs, including nonedges.
    normals=[(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]
    mapped=[(n[1],-n[0],-n[2]) for n in normals]
    if any(dot(x,y)!=dot(u,v) for x,u in zip(normals,mapped) for y,v in zip(normals,mapped)):
        raise ValueError('full Gram diagnostic mismatch')
    return {'status':'PASS','arithmetic':'exact rational/integer',
            'polar_source_edge_squared':str(source),
            'polar_target_edge_squared':str(target),
            'edge_difference':str(gap),
            'scaled_cube_top_face_determinant':volume,
            'boundary_face_halfspace_diagnostic':'PASS',
            'all_pairs_orthogonal_Gram_diagnostic':'PASS',
            'scope':'Finite diagnostics only. General degree, convexity, and imported rigidity theorem require the written derivation and source assumptions.'}


if __name__=='__main__':
    print(json.dumps(run_checks(),indent=2))
