#!/usr/bin/env python3
"""Bounded independent exact audit; no imported author checker or external files."""
import itertools
import json
import math
import os
import sys
from collections import Counter
from fractions import Fraction as F


def require(ok, message):
    if not ok:
        raise ValueError(message)


def area2(points, tri):
    a, b, c = (points[i] for i in tri)
    return abs(a[0]*b[1]+b[0]*c[1]+c[0]*a[1]-a[1]*b[0]-b[1]*c[0]-c[1]*a[0])


def signed_total(points):
    return sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(points, points[1:]+points[:1]))


def strict(points):
    n=len(points)
    require(n>=3 and len(set(points))==n, 'distinct vertices')
    # Every third vertex is strictly on the same oriented side of every edge.
    orientation = 1 if signed_total(points)>0 else -1
    for i in range(n):
        a,b=points[i],points[(i+1)%n]
        for j in range(n):
            if j in (i,(i+1)%n):
                continue
            c=points[j]
            require(orientation*((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))>0, 'strict convexity')


def crossing(e,f):
    a,b=sorted(e);c,d=sorted(f)
    return a<c<b<d or c<a<d<b


def edge(a,b):
    return tuple(sorted((a,b)))


def diagonal_triangulations(n):
    # Independent of recursive Catalan/ear-deletion generation: choose all n-3
    # diagonals, retain pairwise noncrossing choices, recover their triangular faces.
    boundary={edge(i,(i+1)%n) for i in range(n)}
    diagonals=[e for e in itertools.combinations(range(n),2) if e not in boundary]
    result=[]
    for chosen in itertools.combinations(diagonals,n-3):
        if any(crossing(a,b) for a,b in itertools.combinations(chosen,2)):
            continue
        graph=boundary|set(chosen)
        faces=tuple(t for t in itertools.combinations(range(n),3)
                    if all(edge(a,b) in graph for a,b in itertools.combinations(t,2)))
        require(len(faces)==n-2, 'triangular faces')
        incidence=Counter(edge(a,b) for t in faces for a,b in itertools.combinations(t,2))
        require(all(incidence[e]==(1 if e in boundary else 2) for e in graph), 'face incidences')
        result.append(faces)
    expected=math.comb(2*(n-2),n-2)//(n-1)
    require(len(result)==expected, 'Catalan count')
    return result


def spectrum(points, expect_distinct=None):
    strict(points)
    rows=diagonal_triangulations(len(points))
    profiles=Counter()
    total=abs(signed_total(points))
    for triangles in rows:
        areas=tuple(sorted(area2(points,t) for t in triangles))
        require(sum(areas)==total, 'area partition')
        if expect_distinct is not None:
            require(len(set(areas))==expect_distinct, 'area diversity')
        profiles[areas]+=1
    return {'triangulations':len(rows), 'total_doubled_area':total,
            'profiles':[{'areas':list(a),'count':c} for a,c in sorted(profiles.items())]}


def caps(face, tri):
    positions=sorted(face.index(i) for i in tri)
    a,b,c=positions
    arcs=[face[a:b+1],face[b:c+1],face[c:]+face[:a+1]]
    return [arc for arc in arcs if len(arc)>=3]


def cap_check(points, triangle, enforce_maximum=True):
    n=len(points)
    value=area2(points,triangle)
    if enforce_maximum:
        require(value==max(area2(points,t) for t in itertools.combinations(range(n),3)), 'maximum premise')
    sizes=[]
    for arc in caps(tuple(range(n)),triangle):
        mass=abs(signed_total(tuple(points[i] for i in arc)))
        require(mass < value if n>=5 else mass<=value, 'cap area bound')
        sizes.append(mass)
    return sizes


def packing(points):
    strict(points)
    n=len(points)
    unselected=[tuple(range(n))];selected=[];palette=set()
    while True:
        choice=None
        for face_index,face in enumerate(unselected):
            # Minimum-area new triangle, rather than a maximum-area choice.
            available=[(area2(points,t),t) for t in itertools.combinations(face,3) if area2(points,t) not in palette]
            if available:
                value,tri=min(available)
                choice=(face_index,face,value,tri)
                break
        if choice is None:
            break
        i,face,value,tri=choice
        unselected.pop(i);unselected.extend(caps(face,tri))
        selected.append(tri);palette.add(value)
    k=len(selected);r=len(unselected)
    boundary={edge(i,(i+1)%n) for i in range(n)}
    inserted={edge(a,b) for tri in selected for a,b in itertools.combinations(tri,2)}-boundary
    d=len(inserted)
    require(k>=1 and len(palette)==k, 'rainbow cardinality')
    require(not any(crossing(a,b) for a,b in itertools.combinations(inserted,2)), 'crossing selected diagonals')
    require(d<=3*k and k+r==d+1 and r<=2*k+1, 'face count')
    require(3*k+sum(map(len,unselected))==n+2*d, 'edge count')
    require(n==k+2+sum(len(f)-2 for f in unselected), 'Euler reduction')
    for f in unselected:
        require(all(area2(points,t) in palette for t in itertools.combinations(f,3)), 'maximality')
        fixed=Counter(area2(points,(f[0],f[1],v)) for v in f[2:])
        require(max(fixed.values())<=2 and len(f)-2<=2*k, 'fixed-base multiplicity')
    require(n<=4*k*k+3*k+2, 'packing bound')
    triangles=selected+[ (f[0],f[i],f[i+1]) for f in unselected for i in range(1,len(f)-1)]
    require(len(triangles)==n-2, 'completion count')
    require(sum(area2(points,t) for t in triangles)==abs(signed_total(points)), 'completion area')
    require(len({area2(points,t) for t in triangles})>=k,'completion rainbow')
    return {'n':n,'k':k,'r':r,'d':d,'residual_sizes':list(map(len,unselected))}


def cross(a,b):
    return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])


def primitive(u):
    require(any(u) and math.gcd(*u)==1, 'primitive nonzero normal')


def lattice(points2,v,w,normal):
    primitive(normal)
    raw=[tuple(x*v[j]+y*w[j] for j in range(3)) for x,y in points2]
    mins=[min(p[j] for p in raw) for j in range(3)]
    points=[tuple(p[j]-mins[j] for j in range(3)) for p in raw]
    m=max(max(p) for p in points)
    U=max(map(abs,normal));require(U<=m,'normal coordinate bound')
    require(all(sum(normal[j]*(p[j]-points[0][j]) for j in range(3))==0 for p in points),'plane')
    allunits={};projections=0
    for tri in itertools.combinations(range(len(points)),3):
        a,b,c=(points[i] for i in tri)
        cp=cross(tuple(b[j]-a[j] for j in range(3)),tuple(c[j]-a[j] for j in range(3)))
        pivot=next(j for j in range(3) if normal[j])
        lam=F(cp[pivot],normal[pivot])
        require(lam.denominator==1 and lam!=0,'integer nonzero area unit')
        require(tuple(lam*x for x in normal)==cp,'parallel cross product')
        k=abs(lam.numerator)
        require(k<=m*m//U,'cube triangle bound')
        require(sum(x*x for x in cp)==k*k*sum(x*x for x in normal),'squared area scale')
        allunits[tri]=k
        for j in range(3):
            if normal[j]:
                projected=tuple(tuple(p[q] for q in range(3) if q!=j) for p in points)
                strict(projected)
                require(area2(projected,tri)==k*abs(normal[j]),'projection determinant scale')
                projections+=1
    masses=set()
    for tris in diagonal_triangulations(len(points)):
        units=[allunits[t] for t in tris];S=sum(units);q=len(set(units))
        masses.add(S)
        require(S<=2*m*m//U,'polygon mass bound')
        require(q<=min(len(points)-2,m*m//U),'palette upper bound')
        require(S>=len(points)-2+q*(q-1)//2,'distinct-unit mass bound')
    require(len(masses)==1,'triangulation-independent mass')
    return {'normal':normal,'basis_cross':cross(v,w),'cube_side':m,'K':m*m//U,
            'S':next(iter(masses)),'triangle_count':len(allunits),'projection_checks':projections,
            'area_units':sorted(set(allunits.values()))}


def rejection(label,callback):
    try:
        callback()
    except ValueError as e:
        return {'label':label,'rejected':True,'reason':str(e)}
    raise ValueError('negative control survived: '+label)


def main():
    require(os.getuid()==1000 and os.geteuid()==1000,'execution uid')
    p5=((0,0),(1,0),(2,1),(1,2),(0,1))
    p6=((0,0),(1,0),(2,1),(2,2),(1,2),(0,1))
    square=((0,0),(1,0),(1,1),(0,1))
    out={'uid':os.getuid(),'euid':os.geteuid(),'optimization':sys.flags.optimize,'python':sys.version.split()[0]}
    out['catalan_counts']={str(n):len(diagonal_triangulations(n)) for n in range(3,8)}
    out['small_witnesses']={'P3':spectrum(((0,0),(1,0),(0,1)),1),'P4':spectrum(square,1),
                            'P5':spectrum(p5,2),'P6':spectrum(p6,2)}
    rows=[]
    for a,b,c in itertools.combinations(range(6),3):
        gaps=tuple(sorted((b-a,c-b,6-c+a)));expected={(1,1,4):1,(1,2,3):2,(2,2,2):3}[gaps]
        actual=area2(p6,(a,b,c));require(actual==expected,'P6 gap-type area')
        rows.append({'vertices':[a,b,c],'gaps':gaps,'doubled_area':actual})
    out['P6_all_twenty_triples']=rows
    suite=[p5,p6]+[tuple((i,i*i) for i in range(n)) for n in range(3,13)]
    cap_count=0;quad_equalities=0
    for points in suite+[square]:
        strict(points)
        maximum=max(area2(points,t) for t in itertools.combinations(range(len(points)),3))
        for tri in itertools.combinations(range(len(points)),3):
            if area2(points,tri)==maximum:
                values=cap_check(points,tri);cap_count+=len(values)
                if len(points)==4:quad_equalities+=sum(v==maximum for v in values)
    out['caps']={'nonempty_caps_checked':cap_count,'quadrilateral_equalities_observed':quad_equalities}
    out['packing_runs']=[packing(points[offset:]+points[:offset]) for points in suite for offset in (0,1,2)]
    out['lattice']=[lattice(p6,*fixture) for fixture in [
        ((1,0,0),(0,1,0),(0,0,1)),
        ((1,1,0),(0,1,1),(1,-1,1)),
        ((3,-2,0),(1,1,-1),(2,3,5)),
        ((3,-2,0),(5,0,-2),(2,3,5)),
        ((2,0,-3),(0,1,0),(3,0,2))]]
    G={3:1,4:1};B={}
    for n in range(3,10001):
        if n>=5:G[n]=1+G[(n+5)//3]
        k=1
        while n>4*k*k+3*k+2:k+=1
        require(n<=4*k*k+3*k+2 and (k==1 or n>4*(k-1)**2+3*(k-1)+2),'least quadratic root')
        j=1
        while n>(5*3**(j-1)+3)//2:j+=1
        require(G[n]==j,'log threshold identity')
        B[n]=k
    out['bounds']={'n_checked':[3,10000],'G_at_10000':G[10000],'B_at_10000':B[10000]}
    out['negative_controls']=[
        rejection('false P5 diversity three',lambda:spectrum(p5,3)),
        rejection('false P6 diversity three',lambda:spectrum(p6,3)),
        rejection('nonprimitive normal',lambda:primitive((2,2,2))),
        rejection('zero normal',lambda:primitive((0,0,0))),
        rejection('weak convexity excluded',lambda:strict(((0,0),(1,0),(2,0),(2,1),(0,1)))),
        rejection('self-crossing polygon excluded',lambda:strict(((0,0),(1,1),(0,1),(1,0)))),
        rejection('nonmaximum triangle cannot start cap proof',lambda:cap_check(p5,(0,1,4))),
        rejection('strict cap bound fails for square',lambda:require(all(v<1 for v in cap_check(square,(0,1,2))),'strict cap equality'))]
    out['status']='PASS'
    print(json.dumps(out,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
