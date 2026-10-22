#!/usr/bin/env python3
"""Independent exact geometry/algebra controls; Python standard library only.
No author module is imported. Finite checks supplement the written universal audit.
"""
import hashlib
import json
import stat
import sys
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COUNT = 0

def require(ok, why):
    global COUNT
    COUNT += 1
    if not ok:
        raise ValueError(why)

def integrity(root=ROOT):
    mf = root / 'MANIFEST.json'
    require(mf.is_file() and not mf.is_symlink(), 'Mandatory regular manifest absent')
    expected = json.loads(mf.read_text())['files']
    require(all(isinstance(k, str) and not Path(k).is_absolute() and '..' not in Path(k).parts for k in expected), 'Unsafe manifest path')
    dirs = {str(d) for k in expected for d in Path(k).parents if str(d) != '.'}
    actual = {}
    for p in sorted(root.rglob('*')):
        mode = p.lstat().st_mode
        rel = str(p.relative_to(root))
        if stat.S_ISDIR(mode):
            require(rel in dirs, 'Unlisted directory: ' + rel)
        else:
            require(stat.S_ISREG(mode), 'Nonregular member: ' + rel)
            if p != mf:
                b = p.read_bytes()
                actual[rel] = {'bytes':len(b), 'sha256':hashlib.sha256(b).hexdigest()}
    require(actual == expected, 'Recursive manifest mismatch')

def det(a,b): return a[0]*b[1]-a[1]*b[0]
def minus(a,b): return (a[0]-b[0],a[1]-b[1])
def orient(a,b,c): return det(minus(b,a),minus(c,a))

def segments_bad(p,q,r,s,shared):
    """Use exact intersection parameters, including incident edges and overlaps."""
    u,v,w = minus(q,p),minus(s,r),minus(r,p)
    d = det(u,v)
    if d:
        a,b = det(w,v)/d,det(w,u)/d
        if not (0 <= a <= 1 and 0 <= b <= 1): return False
        hit = (p[0]+a*u[0],p[1]+a*u[1])
        return hit not in shared
    if det(w,u): return False
    axis = 0 if u[0] else 1
    lo=max(min(p[axis],q[axis]),min(r[axis],s[axis]))
    hi=min(max(p[axis],q[axis]),max(r[axis],s[axis]))
    if lo>hi:return False
    if lo<hi:return True
    return not any(x[axis]==lo for x in shared)

def expected_complex(m):
    faces = [(i,(i+1)%m,'B') for i in range(m)]
    faces += [('A', (i+1)%m, i) for i in range(1,m)]
    edges = {frozenset((i,(i+1)%m)) for i in range(m)}
    edges |= {frozenset((a,i)) for a in ('A','B') for i in range(m)}
    return faces,edges

def candidate(m,r):
    if not (m>=4 and 1<=r<=m-2):raise ValueError('Invalid parameter')
    s=m-r-1;t=2*m-1
    p={'A':(F(0),F(1)),'B':(F(2*s,t),F(1,t)),0:(F(0),F(0))}
    # Explicit integer numerators, independently expanded from the two chains.
    for i in range(1,r+2):
        k=i-1
        p[i]=(F(r*t-k*(t-s),r*t),F(k*m,r*t))
    for i in range(r+2,m):
        p[i]=(F(m-i,t),F(m*(m-i),s*t))
    return p

def validate(p,m, equal=True, faces=None):
    expected_faces,edges=expected_complex(m)
    faces=expected_faces if faces is None else faces
    require(set(p)==set(range(m))|{'A','B'},'Wrong vertex labels')
    require(p['A']==(0,1) and p[0]==(0,0) and p[1]==(1,0),'Fixed outer coordinates altered')
    require(len(set(p.values()))==m+2,'Vertex collision')
    require(Counter(faces)==Counter(expected_faces),'Wrong labeled oriented faces')
    incidence=Counter()
    for f in faces:
        for j in range(3):incidence[frozenset((f[j],f[(j+1)%3]))]+=1
    require(set(incidence)==edges,'Wrong abstract graph')
    outer={frozenset(x) for x in [('A',0),('A',1),(0,1)]}
    require(all(n==(1 if e in outer else 2) for e,n in incidence.items()),'Wrong face-edge incidences')
    require(len(edges)==3*m and len(faces)==2*m-1,'Wrong Euler counts')
    for v in sorted(set(p)-{'A',0,1},key=str):
        x,y=p[v];require(min(x,y,1-x-y)>0,'Vertex outside open triangle')
    aa=[orient(*(p[v] for v in f)) for f in faces]
    require(all(a>0 for a in aa),'Face orientation or degeneracy')
    require(sum(aa)==1,'Wrong total area')
    if equal:require(aa==[F(1,2*m-1)]*(2*m-1),'Unequal face areas')
    ed=[tuple(e) for e in edges]
    for e,f in combinations(ed,2):
        shared={p[v] for v in set(e)&set(f)}
        require(not segments_bad(p[e[0]],p[e[1]],p[f[0]],p[f[1]],shared),'Illegal edge intersection or overlap')
    return aa

class Poly:
    """Sparse polynomial ring over Q in six formal variables."""
    def __init__(self,a=0):
        if isinstance(a,Poly):self.d=dict(a.d)
        elif isinstance(a,dict):self.d={k:F(v) for k,v in a.items() if v}
        else:self.d={(0,)*6:F(a)} if a else {}
    @staticmethod
    def var(i):
        e=[0]*6;e[i]=1;return Poly({tuple(e):1})
    def __add__(self,b):
        out=dict(self.d)
        for k,v in Poly(b).d.items():out[k]=out.get(k,0)+v
        return Poly(out)
    __radd__=__add__
    def __neg__(self):return Poly({k:-v for k,v in self.d.items()})
    def __sub__(self,b):return self+-Poly(b)
    def __rsub__(self,b):return Poly(b)+-self
    def __mul__(self,b):
        out={}
        for k,v in self.d.items():
            for l,w in Poly(b).d.items():
                q=tuple(a+b for a,b in zip(k,l));out[q]=out.get(q,0)+v*w
        return Poly(out)
    __rmul__=__mul__
    def __pow__(self,n):
        out=Poly(1)
        for _ in range(n):out=out*self
        return out
    def __eq__(self,b):return self.d==Poly(b).d
    def derivative(self,i):
        out={}
        for e,c in self.d.items():
            if e[i]:k=list(e);k[i]-=1;out[tuple(k)]=c*e[i]
        return Poly(out)
    def evaluate(self,z):
        answer=F(0)
        for e,c in self.d.items():
            for x,k in zip(z,e):c*=x**k
            answer+=c
        return answer

def rank(a):
    a=[list(row) for row in a];h=0
    for j in range(len(a[0])):
        pivot=next((i for i in range(h,len(a)) if a[i][j]),None)
        if pivot is None:continue
        a[h],a[pivot]=a[pivot],a[h];v=a[h][j]
        a[h]=[x/v for x in a[h]]
        for i in range(len(a)):
            if i!=h:
                v=a[i][j];a[i]=[x-v*y for x,y in zip(a[i],a[h])]
        h+=1
        if h==len(a):break
    return h

def determinant(a):
    # Leibniz expansion is independent of the author's Gaussian determinant.
    from itertools import permutations
    total=F(0)
    for p in permutations(range(len(a))):
        term=F((-1)**sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p))))
        for i,j in enumerate(p):term*=a[i][j]
        total+=term
    return total

def symbolic_controls():
    r,s,j=[Poly.var(i) for i in range(3)]
    m=r+s+1;t=2*m-1;D=r*s*t
    A=(Poly(0),D);C=(Poly(0),Poly(0));E=(D,Poly(0))
    B=(2*r*s*s,r*s);M=(r*s*s,r*s*m)
    def left(k):return (s*(r*t-k*(t-s)),s*k*m)
    def right(k):return (r*s*(s-k),r*m*(s-k))
    want=r*r*s*s*t
    for U,V in [(left(j),left(j+1)),(right(j),right(j+1))]:
        require(orient(A,V,U)==want,'Formal A-fan identity')
        require(orient(U,V,B)==want,'Formal B-fan identity')
        require(orient(U,V,M)==0,'Formal midpoint concurrence')
    require(orient(C,E,B)==want,'Formal base face')
    require(orient(C,E,A)==t*want,'Formal total area')
    require(tuple(2*x for x in M)==tuple(x+y for x,y in zip(A,B)),'Formal midpoint')
    require(left(0)==E and left(r)==M and right(0)==M and right(s)==C,'Formal endpoint identities')
    # Polynomial area map and its analytic derivatives, independently derived.
    b,h,d,e,f,g=[Poly.var(i) for i in range(6)]
    p={'A':(Poly(0),Poly(1)),0:(Poly(0),Poly(0)),1:(Poly(1),Poly(0)),'B':(b,h),2:(d,e),3:(f,g)}
    faces,_=expected_complex(4);areas=[orient(*(p[v] for v in face)) for face in faces]
    explicit=[h,-b*e+d*h+e-h,b*e-b*g+d*g-d*h-e*f+f*h,b*g-f*h,1-d-e,-d*g+d+e*f-f,f]
    require(areas==explicit,'Area polynomials disagree')
    require(sum(areas)==1,'Formal face-area sum')
    plus=[F(x,7) for x in (2,1,4,2,1,4)];minus_=[F(x,7) for x in (4,1,2,4,1,2)]
    middle=[(x+y)/2 for x,y in zip(plus,minus_)];u=[(x-y)/2 for x,y in zip(plus,minus_)]
    J=[[a.derivative(i) for i in range(6)] for a in areas[:6]]
    mats=[[[v.evaluate(z) for v in row] for row in J] for z in (plus,minus_,middle)]
    require([determinant(a) for a in mats]==[F(8,49),-F(8,49),0],'Jacobian determinants')
    require([rank(a) for a in mats]==[6,6,5],'Jacobian ranks')
    require(all(sum(a*v for a,v in zip(row,u))==0 for row in mats[2]),'Midpoint kernel')
    def points(z):return {'A':(F(0),F(1)),0:(F(0),F(0)),1:(F(1),F(0)),'B':tuple(z[:2]),2:tuple(z[2:4]),3:tuple(z[4:])}
    for z in (plus,minus_):validate(points(z),4)
    require(validate(points(middle),4,False)==[F(x,49) for x in (7,8,4,8,7,8,7)],'Midpoint areas')
    harmonic=[F(x,5) for x in (2,1,2,2,1,2)];p=points(harmonic)
    require(validate(p,4,False)==[F(x,25) for x in (5,3,1,3,5,3,5)],'Harmonic area pattern')
    _,edges=expected_complex(4)
    for v in ('B',2,3):
        nbr=[next(iter(edge-{v})) for edge in edges if v in edge]
        require(tuple(sum(p[w][k] for w in nbr)/len(nbr) for k in (0,1))==p[v],'Harmonic neighbor equations')
    # Weighted elimination: retain e,g,b without divisions.
    L=F(10,11);c=F(34,121)
    q=242*b*b-220*b+51
    require(q==2*(11*b-5)**2+1,'Strict positive-square identity')
    require(c*c-L*L*c+F(8,11)*b*(L-b)==-F(44,14641)*q,'Weighted elimination polynomial')
    # Check the three substitutions from the original seven area equations.
    def subst(pol, values):
        ans=Poly(0)
        for ex,coeff in pol.d.items():
            term=Poly(coeff)
            for x,k in zip(values,ex):term=term*x**k
            ans=ans+term
        return ans
    z=[b,Poly(F(1,11)),L-e,e,Poly(F(1,11)),g]
    target=[F(x,11) for x in (1,3,1,3,1,1,1)]
    residual=[subst(a,z)-v for a,v in zip(areas,target)]
    require(residual[1]==e*(L-b)-c and residual[3]==b*g-c,'Weighted product equations')
    require(residual[5]==e*g-L*(e+g)+F(8,11),'Weighted third equation')
    require(residual[0]==0 and residual[4]==0 and residual[6]==0,'Weighted boundary equations')

def geometric_negative_controls():
    p=candidate(6,2);faces,_=expected_complex(6)
    cases=[]
    q=dict(p);q[2]=q[3];cases.append(('colliding vertices',q,None))
    q=dict(p);q[2]=(F(3,2),F(1,2));cases.append(('outside vertex',q,None))
    q=dict(p);q[2],q[4]=q[4],q[2];cases.append(('label crossing',q,None))
    q={v:(x+F(1,1000),y-F(1,500)) for v,(x,y) in p.items()};cases.append(('equivariant translated outer triangle',q,None))
    q=dict(p);q[2]=tuple((a+b)/2 for a,b in zip(q['A'],q[1]));cases.append(('vertex on boundary edge',q,None))
    ff=list(faces);ff[1]=(ff[1][1],ff[1][0],ff[1][2]);cases.append(('face reversed',p,ff))
    ff=list(faces);ff[1]=ff[0];cases.append(('duplicated face',p,ff))
    for name,q,ff in cases:
        failed=False
        try:validate(q,6,faces=ff)
        except ValueError:failed=True
        require(failed,'Bad geometry accepted: '+name)
    # Test intersection primitive directly, so area/label gates cannot mask it.
    tests=[(((0,0),(2,2),(0,2),(2,0),set()),True),
           (((0,0),(2,0),(1,0),(3,0),set()),True),
           (((0,0),(2,0),(0,0),(1,0),{(0,0)}),True),
           (((0,0),(1,0),(1,0),(2,0),{(1,0)}),False),
           (((0,0),(1,0),(1,0),(1,1),{(1,0)}),False),
           (((0,0),(1,0),(2,0),(3,0),set()),False),
           (((0,0),(1,0),(1,0),(1,1),set()),True)]
    for args,want in tests:
        args=tuple(tuple(F(x) for x in a) for a in args[:4])+(args[4],)
        require(segments_bad(*args)==want,'Segment primitive control')
    return len(cases)+len(tests)

def main():
    integrity()
    controls_before=COUNT
    drawn=0
    quick = sys.argv[1:] == ['--quick']
    require(not sys.argv[1:] or quick, 'Unsupported arguments')
    for m in range(4,8 if quick else 25):
        seen=set()
        for r in range(1,m-1):
            p=candidate(m,r);validate(p,m);drawn+=1
            key=tuple(p[i] for i in range(m))+(p['B'],)
            require(key not in seen,'Labeled drawings duplicate');seen.add(key)
            midpoint=tuple((a+b)/2 for a,b in zip(p['A'],p['B']))
            require([v for v in range(m) if p[v]==midpoint]==[r+1],'Wrong unique midpoint vertex')
            other=candidate(m,m-1-r)
            mapping={'A':'A','B':'B',**{i:(1-i)%m for i in range(m)}}
            require(all(other[mapping[v]]==(1-x-y,y) for v,(x,y) in p.items()),'Reflection labeling')
            require((p==other)==(2*r==m-1),'Reflection fixed-point condition')
        require(len(seen)==m-2,'Incorrect candidate count')
    stress = [] if quick else [(37,1),(37,18),(37,35),(64,1),(64,31),(64,62),(101,1),(101,50),(101,99)]
    for m,r in stress:
        validate(candidate(m,r),m);drawn+=1
    symbolic_controls()
    negative=geometric_negative_controls()
    print(json.dumps({'status':'PASS','mathematical_checks':COUNT-controls_before,'family_drawings':drawn,
      'exhaustive_m_range':[4,7 if quick else 24],'additional_m_r':[list(x) for x in stress],
      'invalid_geometry_and_segment_controls':negative,'formal_polynomial_identities':True,
      'jacobian_method':'analytic polynomial derivatives; Leibniz determinants',
      'author_code_imported':False,'universal_problem_solved':False},sort_keys=True,indent=2))

if __name__=='__main__':main()
