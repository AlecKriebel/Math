#!/usr/bin/env python3
"""Independent exact audit of finite claims; no downloads and no source-file imports.
Run from any directory with Python 3 and SymPy. Prints JSON.
The mathematical completeness arguments and limits are in AUDIT.md.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product, combinations, combinations_with_replacement
from math import ceil, floor
import hashlib, json, platform
import sympy as s

BASE=Path(__file__).resolve().parent.parent
EXPECTED='a4087c4f62929196749da8c9d1925792be34b714719c7cb4469fa32b997b0c2c'
manifest=BASE/'public'/'FROZEN_MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()==EXPECTED
m=json.loads(manifest.read_text())
for f in m['files']:
    b=(BASE/'public'/f['path']).read_bytes()
    assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256']

PAIRS=((1,3),(2,4),(5,6))
CONES=list(product(*PAIRS))
def rays(e,a,b):
    return {i+1:s.Matrix(v) for i,v in enumerate(((1,0,0),(0,1,0),(-1,e,a),(0,-1,b),(0,0,1),(0,0,-1)))}
def pair(v,w): return sum(x*y for x,y in zip(v,w))
def induced_betti(S):
    faces={d:sorted({tuple(sorted(c)) for cone in CONES for c in combinations(set(cone)&set(S),d+1)}) for d in range(3)}
    rank={}
    for d in (1,2):
        M=s.zeros(len(faces[d-1]),len(faces[d]))
        for j,c in enumerate(faces[d]):
            for k in range(len(c)):
                M[faces[d-1].index(c[:k]+c[k+1:]),j]=(-1)**k
        rank[d]=M.rank()
    return (max(0,len(faces[0])-rank[1]-1),len(faces[1])-rank[1]-rank[2])

patterns=[]
for bits in product((False,True),repeat=4):
    S=tuple(i+1 for i,b in enumerate(bits) if b)
    h=induced_betti(S)
    if any(h): patterns.append((S,h))
assert patterns==[((2,4),(1,0)),((1,3),(1,0)),((1,2,3,4),(0,1))]
# A selected fiber vertex makes the induced complex a cone. The two fiber
# vertices cannot both be selected because their ray pairings have opposite sign.
for bits in product((False,True),repeat=4):
    S=tuple(i+1 for i,b in enumerate(bits) if b)
    for k in (5,6): assert induced_betti(S+(k,))==(0,0)

def integer_polyhedron(ineq):
    """All integer solutions of A*x+B*y<=C, via exact Fourier-Motzkin.
    In all cases used here the feasible solution set is bounded.
    """
    lowers=[];uppers=[]; xine=[]
    for A,B,C in ineq:
        if B>0: uppers.append((-Q(A,B),Q(C,B)))
        elif B<0: lowers.append((-Q(A,B),Q(C,B)))
        else: xine.append((Q(A),Q(C)))
    for l,l0 in lowers:
        for u,u0 in uppers: xine.append((l-u,u0-l0))
    lo=None;hi=None
    for A,C in xine:
        if A==0:
            if C<0:return []
        elif A>0: hi=min(hi,C/A) if hi is not None else C/A
        else: lo=max(lo,C/A) if lo is not None else C/A
    if lo is not None and hi is not None and lo>hi:return []
    assert lo is not None and hi is not None, 'Unbounded x projection'
    out=[]
    for x in range(ceil(lo),floor(hi)+1):
        assert lowers and uppers, 'Unbounded y fiber'
        ylo=max(l*x+c for l,c in lowers); yhi=min(u*x+c for u,c in uppers)
        out.extend((x,y) for y in range(ceil(ylo),floor(yhi)+1))
    return out

def full_data(params):
    e,a,b=params; rs=rays(*params)
    dets=[int(s.Matrix.hstack(*(rs[i] for i in c)).det()) for c in CONES]
    assert all(abs(d)==1 for d in dets)
    # An explicit integral polytope with these inward facet normals.
    # 0<=z<=1, 0<=y<=1+b*z, 0<=x<=A+e*y+a*z.
    A=1+max(0,-a); offsets={1:0,2:0,3:A,4:1,5:0,6:1}
    vertices=[]
    for cone in CONES:
        N=s.Matrix.vstack(*(rs[i].T for i in cone))
        v=N.inv()*s.Matrix([-offsets[i] for i in cone])
        slack={i:int(pair(rs[i],v)+offsets[i]) for i in rs}
        assert all(q>=0 for q in slack.values())
        assert {i for i,q in slack.items() if q==0}==set(cone)
        assert all(q.q==1 for q in v)
        vertices.append(list(map(int,v)))
    assert len({tuple(v) for v in vertices})==8
    t1=[];t2=[]
    for rho in rs:
        z=-1 if rho==5 else 1 if rho==6 else 0
        for support,betti in patterns:
            if rho in support:continue
            ineq=[]
            for j,n in rs.items():
                nx,ny,nz=map(int,n)
                if j==rho:
                    ineq.extend([(nx,ny,-1-nz*z),(-nx,-ny,1+nz*z)])
                elif j in support: ineq.append((nx,ny,-1-nz*z))
                else: ineq.append((-nx,-ny,nz*z))
            for x,y in integer_polyhedron(ineq):
                u=(x,y,z)
                actual=tuple(j for j,n in rs.items() if pair(n,u)<(-1 if j==rho else 0))
                assert actual==support and pair(rs[rho],u)==-1
                datum={'ray':rho,'degree':list(u),'support':list(support)}
                if betti[0]:t1.append(datum)
                if betti[1]:t2.append(datum)
    t1.sort(key=lambda d:(d['ray'],d['degree']));t2.sort(key=lambda d:(d['ray'],d['degree']))
    return {'parameters':params,'determinants':dets,'polytope_vertices':vertices,'T1':t1,'T2':t2,
      'counts':[len({tuple(induced_betti(d['support'])) for d in t1}),len({tuple(d['support']) for d in t1}),len({(d['ray'],tuple(d['support'])) for d in t1}),len(t1)]}

fans={name:full_data(params) for name,params in [('A',(3,-4,3)),('B',(4,-4,3)),('C',(2,-4,4))]}
assert fans['A']['counts']==fans['B']['counts']==[1,2,3,7]
assert len(fans['C']['T1'])==9
assert [d['degree'] for d in fans['A']['T2']]==[[-1,-2,-1]]
assert [d['degree'] for d in fans['B']['T2']]==[[-3,-2,-1],[-2,-2,-1],[-1,-2,-1]]
assert [d['degree'] for d in fans['C']['T2']]==[[-1,-3,-1]]

UA=((0,-1,-1),(1,-1,-1),(-1,0,1),(-1,-1,0),(-2,0,1),(-2,-1,0),(-3,0,1))
UB=((0,-1,-1),(-1,-1,0),(-1,0,1),(-2,-1,0),(-2,0,1),(-3,-1,0),(-3,0,1))
def monomial_solutions(U,v):
    ell=(-2,-2,-1);w=[pair(ell,u) for u in U];B=pair(ell,v)
    assert min(w)>0
    ans=[]
    for exp in product(*(range(B//w0+1) for w0 in w)):
        if tuple(sum(p*u[j] for p,u in zip(exp,U)) for j in range(3))==v:ans.append(exp)
    return ans
MA=monomial_solutions(UA,(-1,-2,-1));MB={str(k):monomial_solutions(UB,(-k,-2,-1)) for k in (1,2,3)}
assert len(MA)==5 and all(len(v)==2 for v in MB.values())

def edge_obstruction(params,r,u,c,t,v,d):
    rs=rays(*params); edges=[]
    # Euler-sheaf bracket: [chi^u f_r,chi^v f_t]
    # = r(v) f_t - t(u) f_r. BCH(-alpha_i,alpha_j)
    # contributes -[alpha_i,alpha_j]/2.
    bracket=s.zeros(6,1)
    bracket[t-1]+=pair(rs[r],v);bracket[r-1]-=pair(rs[t],u)
    for i,j in ((0,1),(1,2),(2,3),(3,0)):
        edges.append(-s.Rational(1,2)*(c[i]*d[j]-d[i]*c[j])*bracket)
    return {'edges':[[str(a) for a in E] for E in edges], 'sum':[str(a) for a in sum(edges,s.zeros(6,1))]}
c=(0,1,1,0);d=(0,0,1,1)
qa=[edge_obstruction((3,-4,3),5,UA[i],c,2,UA[j],d) for i,j in ((0,3),(1,5))]
qb=[edge_obstruction((4,-4,3),5,UB[0],c,2,UB[2*k-1],d) for k in (1,2,3)]
qc=edge_obstruction((2,-4,4),5,(0,-2,-1),c,2,(-1,-1,0),d)
for z in qa+qb:assert z['sum']==['0','0','0','0','-1','0']
assert qc['sum']==['0','0','0','0','-2','0']

t=s.symbols('t1:8');h=s.symbols('h');a3,a4,a5=s.symbols('a3 a4 a5')
f=-t[0]*t[3]-t[1]*t[5]+a3*t[0]**2*t[2]+a4*t[1]**2*t[6]+a5*t[0]*t[1]*t[4]
forward=list(t);forward[3]=-t[3]+a3*t[0]*t[2]+a5*t[1]*t[4];forward[5]=-t[5]+a4*t[1]*t[6]
quad=t[0]*t[3]+t[1]*t[5]
assert s.expand(quad.subs(dict(zip(t,forward)),simultaneous=True)-f)==0
assert all(s.expand(g.subs(dict(zip(t,forward)),simultaneous=True)-v)==0 for g,v in zip(forward,t))
assert s.det(s.Matrix(forward).jacobian(t))==1
assert s.hessian(quad,t).rank()==4
# Exact polynomial intersection certificate; the report supplies the formal proof.
GB=s.groebner([h*t[0]]+[(1-h)*t[j] for j in (1,3,5)],h,*t,order='lex')
intersection=[g.as_expr() for g in GB.polys if not g.as_expr().has(h)]
assert set(intersection)=={t[0]*t[j] for j in (1,3,5)}

z=s.symbols('z1:5');P=z[0]*z[1]*z[3]
assert s.expand(z[3]*(z[2]-P)**2-(z[2]**2*z[3]-2*z[0]*z[1]*z[2]*z[3]**2+z[0]**2*z[1]**2*z[3]**3))==0
mock=z[3]*(z[2]**2-P**2)
assert s.expand(mock-z[3]*(z[2]-P)*(z[2]+P))==0
assert all(mock.subs({z[j]:0 for j in range(4) if j!=i})==0 for i in range(4))
U4=((0,-1,-1),(1,-1,-1),(0,-2,-1),(-1,0,1))
assert tuple(U4[0][j]+U4[1][j]+U4[3][j] for j in range(3))==U4[2]
assert tuple(2*U4[2][j]+U4[3][j] for j in range(3))==tuple(2*U4[0][j]+2*U4[1][j]+3*U4[3][j] for j in range(3))

UC={'x':(-1,-1,0),'a':(-3,0,1),'b':(-2,0,1),'c':(-1,0,1),'d':(-1,1,1),'y':(0,-2,-1),'p':(0,-1,-1),'q':(1,-1,-1),'r':(2,-1,-1)}
v=(-1,-3,-1)
qmons=[i+j for i,j in combinations_with_replacement(UC,2) if tuple(UC[i][k]+UC[j][k] for k in range(3))==v]
assert qmons==['xy']
assert tuple(UC['d'][k]+UC['q'][k] for k in range(3))==(0,0,0)
assert tuple(2*UC['c'][k]+2*UC['p'][k]+UC['q'][k] for k in range(3))==v
saved=json.loads((BASE/'public'/'verification_results.json').read_text())
for name in ('A','B'):
    assert fans[name]['T1']==sorted([{key:d[key] for key in ('ray','degree','support')} for d in saved['count_collision'][name]['first_order']],key=lambda d:(d['ray'],d['degree']))
assert fans['C']['T1']==sorted([{key:d[key] for key in ('ray','degree','support')} for d in saved['resonant_candidate']['data']['first_order']],key=lambda d:(d['ray'],d['degree']))

print(json.dumps({'status':'PASS','python':platform.python_version(),'sympy':s.__version__,
 'frozen_manifest_sha256':EXPECTED,'frozen_payload_hashes':'all six matched; manifest is seventh file',
 'independent_method':'all induced complexes; exact Fourier-Motzkin integer enumeration; explicit polytope; symbolic algebra',
 'fans':fans,'complete_monomial_support_A':MA,'complete_monomial_support_B':MB,
 'quadratic_cochains':{'A':qa,'B':qb,'C':qc},'A_coordinate_change_jacobian':1,
 'B_intersection_generators':list(map(str,intersection)),
 'candidate':{'unique_quadratic':qmons,'coefficient':-2,'normalized_residual':'NOT COMPUTED'},
 'limits':['Does not compute an all-order toric candidate hull','Does not prove the universal tangent-cone claim','Does not answer every possible relation in Question 5','Exact arithmetic supports the accompanying mathematical argument; it is not a substitute for it']},indent=2))
