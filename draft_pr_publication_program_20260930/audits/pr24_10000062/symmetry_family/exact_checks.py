#!/usr/bin/env python3
"""Independent audit controls; universal conclusions are proved in REPORT.md.

No historical candidate/reviewer code is imported. Standard library only.
"""
from fractions import Fraction as F
from itertools import combinations, product
from collections import Counter
from functools import lru_cache
from pathlib import Path
import json, math

checks = []

def require(name, value):
    if not value:
        raise AssertionError(name)
    checks.append(name)

def norm(p): return p[0]*p[0]+p[1]*p[1]
def diff(p,q): return p[0]-q[0],p[1]-q[1]
def det(p,q): return p[0]*q[1]-p[1]*q[0]

class Layering:
    def __init__(self, epsilon, height=F(3)):
        self.epsilon, self.height = epsilon, height
    def delta(self,j): return F(1)+F(self.epsilon(j),2)
    @lru_cache(None)
    def offset(self,j):
        if j==0: return F(0)
        if j>0: return self.offset(j-1)+self.delta(j-1)+1
        return self.offset(j+1)-self.delta(j)-1
    def lower(self,j,k): return self.offset(j)+2*k, (self.height+1)*j
    def upper(self,j,k): return self.offset(j)+self.delta(j)+2*k, (self.height+1)*j+1
    def faces(self,j,k):
        l,u=self.lower,self.upper
        return tuple(tuple(sorted(t)) for t in [
            (l(j,k),l(j,k+1),u(j,k)),
            (u(j,k-1),u(j,k),l(j,k)),
            (u(j,k),u(j,k+1),l(j+1,k)),
            (l(j+1,k-1),l(j+1,k),u(j,k))])
    def window(self,J=range(-3,4),K=range(-12,13)):
        return {t for j in J for k in K for t in self.faces(j,k)}

def closest(a,b):
    v=diff(b,a)
    t=max(F(0),min(F(1),-(a[0]*v[0]+a[1]*v[1])/norm(v)))
    p=a[0]+t*v[0],a[1]+t*v[1]
    return norm(p),p

def inward_line(a,b,c):
    v=diff(b,a); raw=(-v[1],v[0],v[1]*a[0]-v[0]*a[1])
    if raw[0]*c[0]+raw[1]*c[1]+raw[2]<0: raw=tuple(-x for x in raw)
    mult=math.lcm(*(x.denominator for x in raw))
    integers=tuple(int(x*mult) for x in raw)
    divisor=math.gcd(*integers)
    return tuple(x//divisor for x in integers)

def disk_signature(faces,r2=F(10)):
    vertices={v for t in faces for v in t}
    edges={tuple(sorted(e)) for t in faces for e in combinations(t,2)}
    vertex_trace=frozenset(v for v in vertices if norm(v)<=r2)
    positive_edges=set(); point_edges=Counter(); positive_faces=Counter(); point_faces=Counter()
    for e in edges:
        d,p=closest(*e)
        if d<r2: positive_edges.add(e)
        elif d==r2: point_edges[p]+=1
    for t in faces:
        lines=[inward_line(t[i],t[(i+1)%3],t[(i+2)%3]) for i in range(3)]
        minima=[closest(t[i],t[(i+1)%3]) for i in range(3)]
        d,p=(F(0),(F(0),F(0))) if all(line[2]>=0 for line in lines) else min(minima)
        if d<r2:
            # Positive clipped-face boundaries consist of these directed lines
            # and the common disk. See analytic reduction in REPORT.md.
            positive_faces[tuple(sorted(line for line,minimum in zip(lines,minima) if minimum[0]<r2))]+=1
        elif d==r2: point_faces[p]+=1
    incidence={p:(sum(p in e for e in positive_edges),point_edges[p],
                  sum(p in t for t in faces if classify_positive(t,r2)),point_faces[p]) for p in point_edges}
    return (vertex_trace,frozenset(positive_edges),tuple(sorted(point_edges.items())),
            tuple(sorted(positive_faces.items())),tuple(sorted(point_faces.items())),tuple(sorted(incidence.items())))

def classify_positive(t,r2):
    lines=[inward_line(t[i],t[(i+1)%3],t[(i+2)%3]) for i in range(3)]
    return all(line[2]>=0 for line in lines) or min(closest(*e)[0] for e in combinations(t,2))<r2

def normalized_faces(layer,upper=False,J=range(-3,4),K=range(-12,13)):
    d=layer.delta(0)
    def move(p):
        x,y=p
        if upper: x,y=d-x,1-y
        if d==F(3,2): x=-x
        return x,y
    return {tuple(sorted(move(p) for p in t)) for t in layer.window(J,K)}

base=Layering(lambda j:-1)
reference=disk_signature(normalized_faces(base))
local_cases=[]
for word in product([-1,1],repeat=5):
    assignment=dict(zip(range(-2,3),word))
    layer=Layering(lambda j,a=assignment:a.get(j,1))
    for upper in (False,True):
        faces=normalized_faces(layer,upper)
        signature=disk_signature(faces)
        require('all_cell_traces_'+str((word,upper)),signature==reference)
        require('guard_window_'+str((word,upper)),signature==disk_signature(normalized_faces(layer,upper,range(-5,6),range(-20,21))))
        triples={tuple(sorted(norm(diff(a,b)) for a,b in combinations(t,2))) for t in faces}
        require('diameter_'+str((word,upper)),triples=={(F(5,4),F(13,4),F(4)),(F(4),F(10),F(10))})
        require('length2_horizontal_'+str((word,upper)),all((norm(diff(a,b))==4)==(a[1]==b[1]) for t in faces for a,b in combinations(t,2)))
        local_cases.append({'word':word,'upper':upper,'passed':True})
require('boundary_counts',dict(reference[2])=={(F(-1),F(-3)):3,(F(1),F(-3)):3})
require('boundary_face_counts',dict(reference[4])=={(F(-1),F(-3)):2,(F(1),F(-3)):2})
require('boundary_incidence',all(v==(3,3,4,2) for p,v in reference[5]))

# Intrinsic affine symmetry test. All candidates map lower row zero to the
# appropriate row m; any horizontal multiple of 2 can then be added.
def affine(layer,s,t,m,n=0):
    bx=layer.offset(m)+(layer.delta(m) if t==-1 else 0)+2*n
    by=4*m+(1 if t==-1 else 0)
    return lambda p:(s*p[0]+bx,t*p[1]+by)

def allowed_sequence(epsilon,s,t,m,J):
    return all(epsilon(j+m)==s*epsilon(j) if t==1 else epsilon(m-j)==-s*epsilon(j) for j in J)

families={
    'single_defect':lambda j:-1 if j==0 else 1,
    'negative_defect':lambda j:-1 if j==-3 else 1,
    'constant':lambda j:1,
    'alternating':lambda j:1 if j%2==0 else -1,
    'step':lambda j:1 if j>=0 else -1,
    'period3':lambda j:(-1,1,1)[j%3],
}
group_cases=[]
for name,epsilon in families.items():
    layer=Layering(epsilon)
    source=layer.window(range(-8,9),range(-3,4))
    target=layer.window(range(-24,25),range(-70,71))
    for s,t,m in product([-1,1],[-1,1],range(-4,5)):
        move=affine(layer,s,t,m)
        matching=all(tuple(sorted(move(p) for p in triangle)) in target for triangle in source)
        predicted=allowed_sequence(epsilon,s,t,m,range(-8,9))
        require('symbolic_geometric_agreement_'+str((name,s,t,m)),matching==predicted)
        if name=='single_defect':
            require('exact_defect_group_control_'+str((s,t,m)),matching==(m==0 and s==t))
        group_cases.append({'family':name,'s':s,'t':t,'m':m,'matches':matching})
    # Independently check offsets at negative indices, not just positive recursion.
    for j in range(-30,30):
        require('biinfinite_offset_'+str((name,j)),layer.offset(j+1)-layer.offset(j)==layer.delta(j)+1)

# Explicit positive controls for orientations and global affine map types.
control_expected=[('constant',1,1,1),('alternating',-1,1,1),('step',1,-1,-1),('single_defect',-1,-1,0),('negative_defect',-1,-1,-6)]
for name,s,t,m in control_expected:
    eps=families[name]; layer=Layering(eps)
    require('positive_map_'+str((name,s,t,m)),allowed_sequence(eps,s,t,m,range(-100,101)))
    require('row_phase_'+str((name,s,t,m)),all(
        (affine(layer,s,t,m)(layer.lower(j,0))[0]-(layer.offset(j+m) if t==1 else layer.offset(m-j)+layer.delta(m-j)))%2==0
        for j in range(-30,31)))

# Adversarial controls: known changes that invalidate a required subclaim.
changed=Layering(lambda j:1 if j==-1 else -1)
require('radius_enlargement_detected',disk_signature(normalized_faces(base),F(1001,100))!=disk_signature(normalized_faces(changed),F(1001,100)))
require('neighbor_shielding_at_threshold',disk_signature(normalized_faces(base))==disk_signature(normalized_faces(changed)))
face_set=normalized_faces(base)
central_face=next(t for t in face_set if (F(0),F(0)) in t and all(p[1]>=0 for p in t))
require('deleted_incident_face_detected',disk_signature(face_set-{central_face})!=reference)
taller=Layering(lambda j:-1,height=F(301,100))
require('tall_metric_diameter_mutation_detected',max(norm(diff(a,b)) for t in taller.window() for a,b in combinations(t,2))>10)
require('strict_radius_mutation_detected',max(norm(diff(a,b)) for t in base.window() for a,b in combinations(t,2))>F(999,100))
require('constant_sequence_cocompact_control',allowed_sequence(families['constant'],1,1,1,range(-100,101)))
require('wrong_negative_index_formula_detected',Layering(families['single_defect']).offset(-1)==F(-5,2))

result={
 'status':'PASS','exact_arithmetic':'fractions.Fraction','assertions_passed':len(checks),
 'rooted_disk_cases':len(local_cases),'global_affine_control_cases':len(group_cases),
 'closed_disk':{'vertices':len(reference[0]),'positive_length_edges':len(reference[1]),
                'positive_area_faces':sum(v for _,v in reference[3]),'boundary_points':2,
                'point_only_edges_each':3,'point_only_faces_each':2},
 'controls':{'deleted_face':'detected','increased_radius':'detected','increased_tall_height':'diameter violation detected',
             'strict_diameter_radius':'detected','constant_sequence':'has rank-two translations',
             'step_sequence':'horizontal glide reflection found','alternating_sequence':'vertical glide reflection found',
             'negative_defect':'halfturn reverses indices about -3'},
 'scope':'Finite exact controls supplement the universal proofs in REPORT.md; do not infer infinite group exclusion by finite search.',
 'checks':checks,'group_cases':group_cases
}
Path(__file__).with_name('EXACT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['checks','group_cases']},indent=2))
