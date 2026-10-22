#!/usr/bin/env python3
"""Independent, standard-library controls for the fixed-type volume-product audit.

Run from any directory. An optional first argument specifies the frozen author
package, which defaults to ../public. Never writes to that package. Source PDFs
and network access are not needed. Exact finite checks supplement the report;
they are not a replacement for its universal mathematical argument.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import hashlib, json, shutil, subprocess, sys, tempfile

HERE = Path(__file__).resolve().parent
AUTHOR = Path(sys.argv[1]).resolve() if len(sys.argv)>1 else HERE.parent/'public'

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
manifest = json.loads((AUTHOR/'FROZEN_AUTHOR_MANIFEST.json').read_text())
assert manifest['classification']=='partial'
assert manifest['problem_id']==20001282
for name, details in manifest['files'].items():
    path=AUTHOR/name
    assert len(path.read_bytes())==details['bytes'], name
    assert digest(path)==details['sha256'], name
manifest_digest=digest(AUTHOR/'FROZEN_AUTHOR_MANIFEST.json')
assert manifest_digest=='7b6c57bd4b49dea51101bf0a34058ea83f90d925e2a138c8df0b55152e72fd72', 'Unexpected author freeze'

# Replay the original checker only in an isolated copy, preserving the freeze.
with tempfile.TemporaryDirectory(prefix='volume_product_audit_') as temp:
    copy=Path(temp)/'check_exact.py'
    shutil.copyfile(AUTHOR/'check_exact.py',copy)
    run=subprocess.run([sys.executable,str(copy)],capture_output=True,text=True,check=True)
    replay=json.loads(run.stdout)
    assert replay==json.loads((AUTHOR/'exact_results.json').read_text())

# Independent hull reconstruction: Gauss-Jordan supporting planes, then volume
# by each facet's centroid-edge triangles. No author function is imported.
def dot(x,y): return sum(a*b for a,b in zip(x,y))
def det(rows):
    a,b,c=rows
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])
def solve(rows, rhs):
    m=[[F(t) for t in row]+[F(v)] for row,v in zip(rows,rhs)]
    for k in range(3):
        pivot=next((j for j in range(k,3) if m[j][k]),None)
        if pivot is None:return None
        m[k],m[pivot]=m[pivot],m[k]
        c=m[k][k];m[k]=[t/c for t in m[k]]
        for j in range(3):
            if j!=k:
                c=m[j][k];m[j]=[a-c*b for a,b in zip(m[j],m[k])]
    return tuple(row[-1] for row in m)
def neg(v): return tuple(-a for a in v)
def points(p,q,r):
    return [(F(1),F(0),F(0)),(p,q,r),(F(0),F(1),F(0)),
            (F(-1),F(0),F(0)),(-p,-q,-r),(F(0),F(-1),F(0)),
            (F(0),F(0),F(1)),(F(0),F(0),F(-1))]
def hull(vertices):
    planes={}
    for indices in combinations(range(len(vertices)),3):
        normal=solve([vertices[i] for i in indices],[1,1,1])
        if normal is None:continue
        values=[dot(normal,v) for v in vertices]
        if max(values)<=1:
            planes[normal]=frozenset(i for i,v in enumerate(values) if v==1)
    fs=list(planes.values());volume=F(0)
    for face in fs:
        center=tuple(sum(vertices[j][i] for j in face)/len(face) for i in range(3))
        edges={frozenset(face & other) for other in fs if len(face & other)==2}
        for edge in edges:
            i,j=sorted(edge)
            volume+=abs(det([center,vertices[i],vertices[j]]))/6
    return planes,volume
EXPECTED={frozenset([a,i,(i+1)%6]) for a in [6,7] for i in range(6)}
def chamber(p,q,r):
    return p>0 and q>0 and abs(r)<p+q-1 and abs(p-q)+abs(r)<1

def formula(p,q,r):
    return F(4,3)*(p+q+1)*(4-((p+q-1)**2+r*r/3)/(p*q))

# Independent section integration via exact polygon clipping, without using the
# two-corner triangle formula. The area is quadratic in z inside the chamber.
def clip(poly,p,q,c):
    out=[]
    for a,b in zip(poly,poly[1:]+poly[:1]):
        va=p*a[0]+q*a[1]-c;vb=p*b[0]+q*b[1]-c
        if va<=0:out.append(a)
        if (va<0<vb) or (vb<0<va):
            t=va/(va-vb)
            out.append(tuple(a[k]+t*(b[k]-a[k]) for k in range(2)))
    return out

def section_area(p,q,r,z):
    poly=[(F(-1),F(-1)),(F(1),F(-1)),(F(1),F(1)),(F(-1),F(1))]
    poly=clip(poly,p,q,1-r*z)
    poly=clip(poly,-p,-q,1+r*z)
    return abs(sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(poly,poly[1:]+poly[:1])))/2

samples=[]
for s,d in product(map(F,['9/8','5/4','3/2','2','5/2','4','17']),map(F,['-3/4','-1/3','0','1/2','7/8'])):
    p,q=(s+d)/2,(s-d)/2
    m=min(s-1,1-abs(d))
    for t in map(F,['-9/10','-1/3','0','1/2','11/12']):
        samples.append((p,q,t*m))
marking_checks=0
transverse_negative_controls=0
for p,q,r in samples:
    assert chamber(p,q,r)
    vs=points(p,q,r)
    primal,v=hull(vs)
    assert set(primal.values())==EXPECTED,(p,q,r)
    dual,pv=hull(list(primal))
    assert sorted(map(len,dual.values()))==[4]*6+[6]*2
    assert set(dual)==set(vs)
    assert v==F(2,3)*(p+q+1)
    integral=(section_area(p,q,r,F(-1))+4*section_area(p,q,r,F(0))+section_area(p,q,r,F(1)))/3
    assert pv==integral==8-2*((p+q-1)**2+r*r/3)/(p*q)
    assert v*pv==formula(p,q,r)
    assert F(32,3)<v*pv<=12
    if r:
        assert v*pv!=formula(p,q,F(0))
        assert det([vs[0],vs[2],vs[1]])==r
        transverse_negative_controls+=1
    for start,direction,pole in product(range(6),[1,-1],[6,7]):
        u,w,vv=[vs[(start+j*direction)%6] for j in range(3)]
        a=vs[pole]
        rows=list(zip(u,vv,a))
        coords=solve(rows,w)
        assert coords is not None and chamber(*coords)
        assert formula(*coords)==formula(p,q,r)
        marking_checks+=1

# Face-labelled chamber equivalence across a grid including both sides of every
# inequality. Outside the chamber another choice of distinguished poles may have
# the same unlabelled type, so test the marked incidence rather than facet counts.
chamber_cases=0
for p,q,r in product(map(F,['1/4','3/4','1','5/4','2']),map(F,['1/4','3/4','1','5/4','2']),map(F,['-5/4','-1','-1/2','0','1/2','1','5/4'])):
    ns,_=hull(points(p,q,r))
    assert (set(ns.values())==EXPECTED)==chamber(p,q,r),(p,q,r)
    chamber_cases+=1

# Positivity and the distinguished pole choice are genuine marking conditions.
for p,q,r in [(F(-1),F(1),F(0)),(F(1),F(-1),F(0)),(F(-1),F(-1),F(0)),(F(0),F(1),F(1,3))]:
    ns,_=hull(points(p,q,r))
    assert set(ns.values())!=EXPECTED and not chamber(p,q,r)
    chamber_cases+=1

# Genuine degenerations cannot be included as interior stationary points.
ns,v=hull(points(F(1),F(1),F(1)))
ns2,pv=hull(list(ns))
assert sorted(map(len,ns.values()))==[4]*6
assert sorted(map(len,ns2.values()))==[3]*8
assert v*pv==F(32,3)
assert not chamber(F(1),F(1),F(1))
for p,q,r in [(F(3,4),F(3,4),F(1,2)),(F(3,2),F(1,2),F(0)),(F(1,2),F(1,2),F(0))]:
    ns,_=hull(points(p,q,r))
    assert set(ns.values())!=EXPECTED
    assert not chamber(p,q,r)

# Affine invariance and contragredient polarity, including determinant sign.
transforms=[((2,1,0),(0,3,1),(1,0,4)),((0,3,1),(2,1,0),(1,0,4))]
transform_checks=0
for (p,q,r),T in product(samples[::35],transforms):
    vs=points(p,q,r);normals,v=hull(vs);_,pv=hull(list(normals))
    tvs=[tuple(dot(row,x) for row in T) for x in vs]
    tnormals,tv=hull(tvs);_,tpv=hull(list(tnormals))
    transported={solve(list(zip(*T)),n) for n in normals}
    assert set(tnormals)==transported
    assert tv==abs(det(T))*v and tpv==pv/abs(det(T))
    assert tv*tpv==v*pv
    wrong=[tuple(dot(row,x) for row in T) for x in normals]
    assert any(dot(x,y)>1 for x in tvs for y in wrong)
    transform_checks+=1

# Second-order automatic differentiation is independent of the author's Taylor
# coefficient implementation. Exact gradients and Hessians are propagated.
class Jet:
    def __init__(self,value,g=None,h=None):
        self.v=F(value);self.g=g or [F(0)]*3;self.h=h or [[F(0)]*3 for _ in range(3)]
    @staticmethod
    def cast(x):return x if isinstance(x,Jet) else Jet(x)
    def __add__(self,other):
        b=self.cast(other)
        return Jet(self.v+b.v,[self.g[i]+b.g[i] for i in range(3)],[[self.h[i][j]+b.h[i][j] for j in range(3)] for i in range(3)])
    __radd__=__add__
    def __neg__(self):return self*(-1)
    def __sub__(self,b):return self+-self.cast(b)
    def __rsub__(self,b):return self.cast(b)+-self
    def __mul__(self,other):
        b=self.cast(other)
        return Jet(self.v*b.v,[self.g[i]*b.v+self.v*b.g[i] for i in range(3)],[[self.h[i][j]*b.v+self.v*b.h[i][j]+self.g[i]*b.g[j]+self.g[j]*b.g[i] for j in range(3)] for i in range(3)])
    __rmul__=__mul__
    def inverse(self):
        return Jet(1/self.v,[-x/self.v**2 for x in self.g],[[2*self.g[i]*self.g[j]/self.v**3-self.h[i][j]/self.v**2 for j in range(3)] for i in range(3)])
    def __truediv__(self,b):return self*self.cast(b).inverse()
    def __rtruediv__(self,b):return self.cast(b)*self.inverse()
s,d,r=[Jet(v,[F(i==j) for j in range(3)]) for i,v in enumerate([2,0,0])]
p,q=(s+d)/2,(s-d)/2
value=F(4,3)*(s+1)*(4-((s-1)*(s-1)+r*r/3)/(p*q))
expected_h=[[F(-2,3),F(0),F(0)],[F(0),F(-2),F(0)],[F(0),F(0),F(-8,3)]]
assert value.v==12 and value.g==[0]*3 and value.h==expected_h
# A noncritical planar point cannot be misclassified merely because r=0.
s,d,r=[Jet(v,[F(i==j) for j in range(3)]) for i,v in enumerate([3,0,0])]
p,q=(s+d)/2,(s-d)/2
other=F(4,3)*(s+1)*(4-((s-1)*(s-1)+r*r/3)/(p*q))
assert other.g==[F(-16,81),F(0),F(0)]

# Product-height normalization is independent of the selected interval height.
for height in map(F,['1/7','1','5']):
    planar_area=F(3);polar_planar_area=F(3)
    assert (2*height*planar_area)*(2*polar_planar_area/(3*height))==12
    assert planar_area*polar_planar_area!=12

for name,details in manifest['files'].items(): assert digest(AUTHOR/name)==details['sha256']
assert digest(AUTHOR/'FROZEN_AUTHOR_MANIFEST.json')==manifest_digest
result={
    'verdict':'PASS_PARTIAL',
    'frozen_author_manifest_sha256':manifest_digest,
    'author_hashes_unchanged':True,
    'author_replay_cases':replay['rational_interior_realizations'],
    'independent_interior_hulls':len(samples),
    'independent_polar_hulls':len(samples),
    'independent_clipped_section_integrations':len(samples),
    'finite_marking_changes':marking_checks,
    'marked_chamber_equivalence_cases':chamber_cases,
    'nonzero_transverse_negative_controls':transverse_negative_controls,
    'affine_polar_transport_controls':transform_checks,
    'boundary_controls':4,
    'hessian_s_d_r':[[str(x) for x in row] for row in value.h],
    'status_scope':'Finite exact controls pass; mathematical proof and source-hypothesis audit are in AUDIT_REPORT.md. Universal critical uniqueness is not established.'
}
(HERE/'audit_controls.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
