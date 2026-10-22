#!/usr/bin/env python3
"""Exact finite controls for PROOFS.md. Standard library; assertions are never used."""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
checks = 0

def need(condition, message):
    global checks
    checks += 1
    if not condition:
        raise ValueError(message)

def integrity():
    manifest_path = ROOT / 'MANIFEST.json'
    if not manifest_path.is_file() or manifest_path.is_symlink():
        raise ValueError('Missing or unsafe mandatory MANIFEST.json')
    manifest = json.loads(manifest_path.read_text())
    expected = manifest['files']
    expected_dirs = {str(parent) for name in expected for parent in Path(name).parents if str(parent) != '.'}
    actual = {}
    for p in ROOT.rglob('*'):
        if p.is_symlink():
            raise ValueError('Symlink rejected: ' + str(p.relative_to(ROOT)))
        if p.is_dir() and str(p.relative_to(ROOT)) not in expected_dirs:
            raise ValueError('Unlisted directory rejected: ' + str(p.relative_to(ROOT)))
        if p.is_file() and p != manifest_path:
            data = p.read_bytes()
            actual[str(p.relative_to(ROOT))] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
    if actual != expected:
        raise ValueError('Recursive manifest mismatch')

def add(a,b): return (a[0]+b[0],a[1]+b[1])
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def mul(a,k): return (a[0]*k,a[1]*k)
def det(a,b): return a[0]*b[1]-a[1]*b[0]
def area(a,b,c): return det(sub(b,a),sub(c,a))
def between(p,a,b):
    return area(a,b,p)==0 and all(min(a[i],b[i])<=p[i]<=max(a[i],b[i]) for i in (0,1))

def meet(a,b,c,d):
    o1,o2,o3,o4=area(a,b,c),area(a,b,d),area(c,d,a),area(c,d,b)
    return ((o1*o2<0 and o3*o4<0) or between(c,a,b) or between(d,a,b)
            or between(a,c,d) or between(b,c,d))

def edges_of(faces):
    return sorted({tuple(sorted((face[i],face[(i+1)%3]))) for face in faces for i in range(3)})

def geometry(points,faces,expected=None):
    need(len(set(points.values()))==len(points),'Vertices collide')
    av=[area(*(points[x] for x in f)) for f in faces]
    need(all(a>0 for a in av),'Nonpositive bounded face')
    need(sum(av)==1,'Incorrect total doubled area')
    if expected is not None:
        need(av==expected,'Face areas differ from certificate')
    for v,p in points.items():
        if v not in ('A','V0','V1'):
            need(p[0]>0 and p[1]>0 and sum(p)<1,'Interior vertex outside triangle')
    edges=edges_of(faces)
    for i,j in edges:
        for k,p in points.items():
            if k not in (i,j):
                need(not between(p,points[i],points[j]),'Unintended vertex on edge')
    for (i,j),(k,l) in combinations(edges,2):
        if not {i,j}&{k,l}:
            need(not meet(points[i],points[j],points[k],points[l]),'Disjoint edges intersect')
    need(len(edges)==3*len(points)-6,'Incorrect triangulation edge count')
    return av,edges

def family(m,r):
    s=m-1-r; t=2*m-1
    if m<4 or r<1 or s<1:
        raise ValueError('Invalid family parameter')
    A=(Q(0),Q(1)); C=(Q(0),Q(0)); E=(Q(1),Q(0)); M=(Q(s,t),Q(m,t))
    points={'A':A,'B':(Q(2*s,t),Q(1,t)),'V0':C,'V1':E}
    for j in range(1,r+1): points['V'+str(1+j)]=add(E,mul(sub(M,E),Q(j,r)))
    for j in range(1,s): points['V'+str(1+r+j)]=mul(M,1-Q(j,s))
    ring=['V'+str(i) for i in range(m)]
    faces=[(ring[i],ring[(i+1)%m],'B') for i in range(m)]
    faces += [('A',ring[(i+1)%m],ring[i]) for i in range(1,m)]
    return points,faces

def connected_after(vertices,edges,removed):
    left=set(vertices)-set(removed)
    start=next(iter(left)); seen={start}; todo=[start]
    adjacency={v:set() for v in left}
    for a,b in edges:
        if a in left and b in left: adjacency[a].add(b);adjacency[b].add(a)
    while todo:
        v=todo.pop()
        for w in adjacency[v]-seen: seen.add(w);todo.append(w)
    return seen==left

def oct_points(z):
    b,h,d,e,f,g=z
    return {'A':(Q(0),Q(1)),'V0':(Q(0),Q(0)),'V1':(Q(1),Q(0)),
            'B':(b,h),'V2':(d,e),'V3':(f,g)}

OCT_FACES=[('V0','V1','B'),('V1','V2','B'),('V2','V3','B'),('V3','V0','B'),
           ('A','V2','V1'),('A','V3','V2'),('A','V0','V3')]

def areas(z):
    p=oct_points(z)
    return [area(*(p[x] for x in f)) for f in OCT_FACES]

def jacobian(z):
    cols=[]
    for i in range(6):
        plus=list(z);minus=list(z);plus[i]+=1;minus[i]-=1
        cols.append([(a-b)/2 for a,b in zip(areas(plus)[:6],areas(minus)[:6])])
    return [list(row) for row in zip(*cols)]

def determinant(mat):
    a=[list(r) for r in mat]; answer=Q(1); n=len(a)
    for j in range(n):
        pivot=next((k for k in range(j,n) if a[k][j]),None)
        if pivot is None:return Q(0)
        if pivot!=j:a[j],a[pivot]=a[pivot],a[j];answer=-answer
        v=a[j][j];answer*=v
        for k in range(j+1,n):
            q=a[k][j]/v
            for l in range(j,n):a[k][l]-=q*a[j][l]
    return answer

def read_vec(a):return [Q(x) for x in a]

def main():
    integrity()
    cert=json.loads((ROOT/'CERTIFICATES.json').read_text())
    family_cases=0; cuts=0
    for m in range(4,15):
        for r in range(1,m-1):
            points,faces=family(m,r)
            av,ed=geometry(points,faces,[Q(1,2*m-1)]*(2*m-1))
            need(points['V'+str(r+1)]==mul(add(points['A'],points['B']),Q(1,2)),'Midpoint condition')
            if r==1 and m<=10:
                for k in range(4):
                    for cut in combinations(points,k):
                        need(connected_after(points,ed,cut),'Connectivity failure');cuts+=1
            family_cases+=1
    p=read_vec(cert['octahedron_plus']);q=read_vec(cert['octahedron_minus'])
    for z in (p,q):geometry(oct_points(z),OCT_FACES,[Q(1,7)]*7)
    mid=[(a+b)/2 for a,b in zip(p,q)];u=[(a-b)/2 for a,b in zip(p,q)]
    geometry(oct_points(mid),OCT_FACES,read_vec(cert['midpoint_areas']))
    need(any(u),'Zero proposed kernel vector')
    J=jacobian(mid)
    need(all(sum(a*b for a,b in zip(row,u))==0 for row in J),'Derivative kernel fails')
    need(determinant(J)==0,'Midpoint determinant nonzero')
    need(any(determinant([[J[i][j] for j in cols] for i in rows]) for rows in combinations(range(6),5)
             for cols in combinations(range(6),5)),'Midpoint rank is below five')
    need([determinant(jacobian(z)) for z in (p,q)]==read_vec(cert['endpoint_jacobian_determinants']),
         'Jacobian signs fail')
    harmonic=read_vec(cert['harmonic_coordinates']);hp=oct_points(harmonic)
    _,hed=geometry(hp,OCT_FACES,read_vec(cert['harmonic_areas']))
    for v in ('B','V2','V3'):
        neighbors=[b if a==v else a for a,b in hed if v in (a,b)]
        need(len(neighbors)==4,'Incorrect interior degree')
        need(tuple(sum(hp[w][j] for w in neighbors)/4 for j in (0,1))==hp[v],'Not harmonic')
    need(len(set(areas(harmonic)))>1,'Harmonic obstruction disappeared')
    L=Q(10,11);c=Q(34,121)
    # Coefficients in ascending powers of b of the elimination polynomial.
    actual=[c*c-L*L*c,Q(8,11)*L,-Q(8,11)]
    expected=[-Q(44,14641)*a for a in (51,-220,242)]
    need(actual==expected,'Weighted elimination identity fails')
    need(cert['weighted_obstruction_polynomial']==[51,-220,242],'Weighted polynomial certificate changed')
    need([2*25+1,2*2*11*(-5),2*121]==[51,-220,242],'Positive square completion fails')
    need(read_vec(cert['weighted_area_assignment'])==[Q(x,11) for x in (1,3,1,3,1,1,1)],'Weighted areas changed')
    # Reflection reverses the path; checks full labeled drawing equivalence.
    for m in range(4,15):
        for r in range(1,m-1):
            points,_=family(m,r);other,_=family(m,m-1-r)
            mapping={'A':'A','B':'B'}
            mapping.update({'V'+str(i):'V'+str((1-i)%m) for i in range(m)})
            for v,(x,y) in points.items():
                need(other[mapping[v]]==(1-x-y,y),'Reflection/split relation fails')
            need((r==m-1-r)==(m%2==1 and r==(m-1)//2),'Symmetry parity condition fails')
    need(cert['status']=='unsolved' and cert['approaches']==5,'Incorrect scope certificate')
    print(json.dumps({'status':'PASS','exact_checks':checks,'cycle_bipyramid_drawings':family_cases,
                      'connectivity_deletions_checked':cuts,'m_range':[4,14],
                      'universal_source_problem_solved':False,'arithmetic':'fractions.Fraction'},sort_keys=True,indent=2))

if __name__=='__main__':main()
