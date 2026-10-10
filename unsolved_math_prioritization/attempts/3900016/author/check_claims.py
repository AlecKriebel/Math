#!/usr/bin/env python3
"""Bounded exact checks for partial triangulation-area results, not a solver.

Standard library only. Explicit guards survive -O and -OO. Read-only mode
requires UID 1000 and actual failed create/open-for-write probes.
"""
import argparse
import ast
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
import hashlib
from itertools import combinations
import json
from math import comb, gcd
import os
from pathlib import Path
import sys
sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def reject(call, substring):
    try:
        call()
    except (RuntimeError, ValueError) as e:
        require(substring in str(e), 'wrong rejection: '+str(e))
        return
    raise RuntimeError('expected rejection absent')


def area2(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])


def polygon2(p):
    return sum(p[i][0]*p[(i+1)%len(p)][1]-p[i][1]*p[(i+1)%len(p)][0] for i in range(len(p)))


def validate(p):
    require(3 <= len(p) <= 40, 'polygon size outside bounded checker')
    require(all(len(x)==2 and all(type(v) is int or isinstance(v,F) for v in x) for x in p), 'exact two-coordinate input required')
    require(len(set(p))==len(p), 'repeated vertex')
    require(all(area2(p[i],p[j],p[k])>0 for i,j,k in combinations(range(len(p)),3)), 'strict convex CCW order required')


@lru_cache(None)
def triangulations(i,j):
    if j==i+1:
        return ((),)
    result=[]
    for k in range(i+1,j):
        for a in triangulations(i,k):
            for b in triangulations(k,j):
                result.append(tuple(sorted(a+b+((i,k,j),))))
    return tuple(result)


@lru_cache(None)
def ears(indices):
    if len(indices)==3:
        return frozenset((tuple((tuple(sorted(indices)),)),))
    out=set()
    for i,v in enumerate(indices):
        tri=tuple(sorted((indices[i-1],v,indices[(i+1)%len(indices)])))
        for rest in ears(indices[:i]+indices[i+1:]):
            out.add(tuple(sorted(rest+(tri,))))
    return frozenset(out)


def spectra(p):
    validate(p)
    n=len(p);require(n<=10,'full enumeration limited to ten vertices')
    ts=triangulations(0,n-1)
    require(len(ts)==comb(2*(n-2),n-2)//(n-1),'Catalan count mismatch')
    require(len(set(ts))==len(ts),'duplicate triangulation')
    values={t:area2(*(p[i] for i in t)) for t in combinations(range(n),3)}
    spec=set()
    for ts1 in ts:
        require(len(ts1)==n-2,'triangle count mismatch')
        ar=tuple(sorted(values[t] for t in ts1))
        require(sum(ar)==polygon2(p),'area partition mismatch')
        spec.add(ar)
    return max(len(set(s)) for s in spec),spec


def bound_G(n):
    require(type(n) is int and n>=3,'invalid n')
    threshold=4;j=1
    while n>threshold:
        threshold=3*threshold-3;j+=1
    return j


def bound_B(n):
    require(type(n) is int and n>=3,'invalid n')
    k=1
    while 4*k*k+3*k+2<n:k+=1
    return k


def caps(face, tri):
    positions=[face.index(v) for v in tri]
    require(positions==sorted(positions),'triangle order mismatch')
    out=[]
    for a,b in zip(positions,positions[1:]+positions[:1]):
        arc=face[a:b+1] if a<b else face[a:]+face[:b+1]
        if len(arc)>=3:out.append(arc)
    return out


def max_chain(p, face=None):
    if face is None:face=tuple(range(len(p)))
    if len(face)<5:
        return [max(area2(p[a],p[b],p[c]) for a,b,c in combinations(face,3))]
    t=max(combinations(face,3),key=lambda z:area2(*(p[i] for i in z)))
    ar=area2(*(p[i] for i in t)); sub=caps(face,t)
    for f in sub:
        require(polygon2([p[i] for i in f])<ar,'strict cap area failed')
    largest=max(sub,key=len)
    rest=max_chain(p,largest)
    require(ar>max(rest),'strict maximum descent failed')
    result=[ar]+rest
    require(len(result)>=bound_G(len(face)),'G recurrence lower bound failed')
    return result


def pack(p):
    validate(p);n=len(p)
    faces=[tuple(range(n))];selected=[];palette=set()
    while True:
        found=False
        for i,face in enumerate(faces):
            for tri in combinations(face,3):
                a=area2(*(p[j] for j in tri))
                if a not in palette:
                    selected.append(tri);palette.add(a)
                    faces=faces[:i]+caps(face,tri)+faces[i+1:]
                    found=True;break
            if found:break
        if not found:break
    k=len(selected);r=len(faces)
    require(k==len(palette) and 1<=k<=n-2,'invalid rainbow packing')
    boundary={tuple(sorted((i,(i+1)%n))) for i in range(n)}
    diagonals={tuple(sorted(e)) for t in selected for e in combinations(t,2)}-boundary
    d=len(diagonals)
    require(d<=3*k and k+r==d+1 and r<=2*k+1,'subdivision count failed')
    require(n==k+2+sum(len(f)-2 for f in faces),'face incidence failed')
    completion=list(selected)
    for f in faces:
        require(len(f)-2<=2*k,'face palette bound failed')
        require(all(area2(*(p[i] for i in t)) in palette for t in combinations(f,3)),'packing not maximal')
        base=Counter(area2(p[f[0]],p[f[1]],p[v]) for v in f[2:])
        require(max(base.values())<=2,'fixed-base multiplicity failed')
        completion.extend((f[0],f[i],f[i+1]) for i in range(1,len(f)-1))
    require(len(completion)==n-2,'completion size failed')
    require(sum(area2(*(p[i] for i in t)) for t in completion)==polygon2(p),'completion area failed')
    require(n<=4*k*k+3*k+2 and k>=bound_B(n),'packing bound failed')
    return k


def hull(points):
    ps=sorted(set(points))
    if len(ps)<3:return ()
    def half(seq):
        out=[]
        for p in seq:
            while len(out)>=2 and area2(out[-2],out[-1],p)<=0:out.pop()
            out.append(p)
        return out
    h=half(ps)[:-1]+half(list(reversed(ps)))[:-1]
    return tuple(h) if len(h)>=3 else ()


def suite():
    pts=[(x,y) for x in range(3) for y in range(3)]
    shapes={hull([pts[i] for i in range(9) if mask>>i&1]) for mask in range(1<<9)}
    shapes.discard(())
    shapes.update(tuple((i,i*i) for i in range(n)) for n in range(3,11))
    # Integer parabolic polygons with larger n test the constructive mechanisms only.
    shapes.update(tuple((i,i*i) for i in range(n)) for n in (12,20,30))
    return sorted(shapes,key=lambda p:(len(p),p))


def cross(a,b):
    return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])


def lattice_checks(p):
    # z=x+2y: primitive normal (-1,-2,1), an injective oblique embedding.
    q=[(x,y,x+2*y) for x,y in p]
    u=(-1,-2,1);U=2;m=max(max(v) for v in q)
    require(m>=2 and U<=m,'fixture outside bounded-normal scope')
    S=polygon2(p)
    require(S<=2*m*m//U,'polygon mass bound failed')
    for i,j,k in combinations(range(len(p)),3):
        a=tuple(q[j][h]-q[i][h] for h in range(3));b=tuple(q[k][h]-q[i][h] for h in range(3))
        w=cross(a,b);v=area2(p[i],p[j],p[k])
        require(w==tuple(v*t for t in u),'integer normal multiple failed')
        require(v<=m*m//U,'cube spectrum bound failed')
        for drop in range(3):
            coords=[h for h in range(3) if h!=drop]
            proj=[tuple(x[h] for h in coords) for x in q]
            require(abs(area2(proj[i],proj[j],proj[k]))==abs(v*u[drop]),'projection factor failed')
    for ts in triangulations(0,len(p)-1):
        ar=[area2(*(p[i] for i in t)) for t in ts];d=len(set(ar))
        require(S>=len(p)-2+d*(d-1)//2,'mass distinctness bound failed')
    return len(list(combinations(range(len(p)),3)))


def mathematics():
    p5=((0,0),(1,0),(2,1),(1,2),(0,1))
    p6=((0,0),(1,0),(2,1),(2,2),(1,2),(0,1))
    exact=[]
    for p,expected in [(((0,0),(1,0),(0,1)),1),(((0,0),(1,0),(1,1),(0,1)),1),(p5,2),(p6,2)]:
        d,s=spectra(p);require(d==expected,'small extremal witness failed')
        require(set(triangulations(0,len(p)-1))==set(ears(tuple(range(len(p))))),'independent ear enumeration disagrees')
        exact.append({'n':len(p),'D':d,'area_multisets':[list(x) for x in sorted(s)]})
    require(spectra(p5)[1]=={(1,1,3),(1,2,2)},'pentagon spectra drift')
    require(spectra(p6)[1]=={(1,1,1,3),(1,1,2,2)},'hexagon spectra drift')
    vals=tuple(area2(p5[i-1],p5[i],p5[(i+1)%5]) for i in range(5))
    require(vals==(1,1,2,2,1),'pentagon ears incorrect')
    # Exact rational circular-arc example: every triangle in the origin fan has the same area.
    c,s=F(99,101),F(20,101);arc=[(F(0),F(0))];v=(F(1),F(0))
    for _ in range(7):arc.append(v);v=(c*v[0]-s*v[1],s*v[0]+c*v[1])
    validate(arc)
    require(len({area2(arc[0],arc[i],arc[i+1]) for i in range(1,len(arc)-1)})==1,'equal fan example failed')
    polys=suite();enumerated=0;triangle_count=0
    for p in polys:
        validate(p);chain=max_chain(p);k=pack(p)
        require(len(set(chain))==len(chain),'chain area repeats')
        if len(p)<=10:
            D,sp=spectra(p);enumerated+=1;triangle_count+=len(triangulations(0,len(p)-1))
            require(D>=max(bound_G(len(p)),bound_B(len(p)),len(chain),k),'claimed lower bound exceeds exact optimum')
    # Bounds and both boundary sides of their thresholds.
    for n in range(3,1001):
        g=bound_G(n)
        require(g==(1 if n<=4 else 1+bound_G((n+5)//3)),'G threshold recurrence failed')
        k=bound_B(n)
        require(4*k*k+3*k+2>=n and (k==1 or 4*(k-1)**2+3*(k-1)+2<n),'B minimality failed')
    for n in range(3,11):
        p=tuple((i,i*i) for i in range(n))
        require(spectra(p)[0]==n-2,'parabola maximum-distinct witness failed')
    lc=lattice_checks(p5)+lattice_checks(p6)
    reject(lambda:validate(((0,0),(1,0),(2,0))),'strict convex')
    reject(lambda:validate(tuple(reversed(p5))),'strict convex')
    reject(lambda:validate(((0,0),(1,0),(1,0))),'repeated vertex')
    reject(lambda:validate(((0.0,0),(1,0),(0,1))),'exact two-coordinate')
    reject(lambda:bound_G(2),'invalid n')
    reject(lambda:bound_B(True),'invalid n')
    reject(lambda:spectra(tuple((i,i*i) for i in range(11))),'limited to ten')
    return {'small_witnesses':exact,'all_subset_grid':'3 by 3 integer grid, unique strict hulls only',
            'polygons_constructive_checks':len(polys),'polygons_exhaustive_triangulations':enumerated,
            'triangulations_examined':triangle_count,'largest_constructive_polygon':max(map(len,polys)),
            'oblique_lattice_triangles':lc,'rational_equal_fan_vertices':len(arc),
            'bound_integer_cases':998,'guard_negative_controls':7}


def verify_pins():
    pins=json.loads((BASE/'PAYLOAD_PINS.json').read_text())
    require(pins.get('schema')==1,'unknown pin schema')
    files=pins.get('files');require(isinstance(files,list) and files,'empty pin list')
    require({p.name for p in BASE.iterdir() if p.name!='PAYLOAD_PINS.json'}=={x['path'] for x in files},'payload file set changed')
    for x in files:
        p=BASE/x['path'];require(p.parent==BASE and p.is_file() and not p.is_symlink(),'invalid pinned file')
        b=p.read_bytes();require(len(b)==x['bytes'],'pinned byte count mismatch: '+x['path'])
        require(hashlib.sha256(b).hexdigest()==x['sha256'],'pinned hash mismatch: '+x['path'])
    status=json.loads((BASE/'STATUS.json').read_text())
    require(status['problem_id']==3900016 and status['outcome']=='exhausted' and status['substantive_proof_search_approaches']==5,'research status drift')
    manifest=json.loads((BASE/'SOURCE_MANIFEST.json').read_text())
    require(manifest['source_bodies_in_payload'] is False,'source bodies forbidden')
    require(not any(isinstance(x,ast.Assert) for x in ast.walk(ast.parse(Path(__file__).read_text()))),'checker contains assert')
    return {'pinned_payload_files':len(files),'all_hashes_matched':True,'no_assert_nodes':True}


def readonly_probes():
    require(os.geteuid()==1000,'read-only verification requires UID 1000')
    require(not os.access(BASE,os.W_OK),'packet directory is writable')
    probe=BASE/('.write_probe_'+str(os.getpid()));require(not probe.exists(),'write probe collision')
    try:
        fd=os.open(probe,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
    except PermissionError:pass
    else:
        os.close(fd);probe.unlink();raise RuntimeError('packet create unexpectedly succeeded')
    denied=0
    for p in BASE.iterdir():
        require(p.is_file() and not p.is_symlink(),'unexpected probe entry')
        require(not os.access(p,os.W_OK),'packet file is writable')
        try:fd=os.open(p,os.O_WRONLY)
        except PermissionError:denied+=1
        else:os.close(fd);raise RuntimeError('file write-open unexpectedly succeeded')
    return {'directory_create_denied':True,'existing_file_write_open_denials':denied,'actual_write_probes':True}


def output_destination(value):
    p=Path(value).expanduser().resolve()
    require(p!=BASE and BASE not in p.parents,'output must be external to the packet')
    return p


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-readonly',action='store_true');parser.add_argument('--output')
    args=parser.parse_args();out=output_destination(args.output) if args.output else None
    ro=readonly_probes() if args.require_readonly else {'actual_write_probes':False}
    result={'status':'passed','uid':os.geteuid(),'python_optimization':sys.flags.optimize,'readonly_required':args.require_readonly,
            'readonly':ro,'checks':{'integrity':verify_pins(),'mathematics':mathematics()},
            'limits':'Bounded exact tests support the supplied proofs; they do not settle the extremal functions or the triple-repetition question.'}
    data=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if out:out.write_text(data)
    else:sys.stdout.write(data)


if __name__=='__main__':
    try:main()
    except Exception as e:
        sys.stderr.write(type(e).__name__+': '+str(e)+'\n');sys.exit(1)
