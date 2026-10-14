#!/usr/bin/env python3
"""R2 original exact controls: source-generated angle data and first collisions.

This is finite evidence, not a proof of the universal Veech/hyperelliptic imports.
No package modules or external programs are imported or executed.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from math import gcd
from pathlib import Path
import argparse, json

parser=argparse.ArgumentParser()
parser.add_argument('--bad-chart-sign', action='store_true')
parser.add_argument('--bad-hex-first-hit', action='store_true')
parser.add_argument('--bad-first-reflection', action='store_true')
args=parser.parse_args()
counts={}
def check(name, condition):
    if not condition:
        raise RuntimeError('R2 independent failure: '+name)
    counts[name]=counts.get(name,0)+1

# Generate angles from Fuchs's source equations and their feasible intervals,
# independently of the cone-index code in the package.
for n in range(3,102):
    d=F(n-2,n)
    r=n-2 if n%2 else (n-2)//2
    for terminal in ('P','Q'):
        for s in range(-n,n+1):
            target=F(2*s,n)
            lo=max(F(0), target-1) if terminal=='P' else max(F(0), F(2,n)-target)
            hi=min(d,target-F(2,n)) if terminal=='P' else min(d,1-target)
            if lo>hi:continue
            k=(n-1-s if terminal=='P' else s-1)%(n-2)
            for a in {lo,hi,(lo+hi)/2,(3*lo+hi)/4}:
                b=target-a if terminal=='P' else target+a
                check('source_feasibility',0<=a<=d and F(2,n)<=b<=1)
                j=(-s if terminal=='P' else s-1)%n
                if n%2:
                    e=0
                    t=j if (j%2==0)==(terminal=='P') else j+n
                    cycle=2*n
                else:
                    e=j%2 if terminal=='P' else 1-j%2
                    t=j
                    cycle=n
                offset=1-b if terminal=='P' else b-F(2,n)
                m=(t*d+offset-a-(1-e))/2
                check('integer_cone_sheet',m.denominator==1)
                K=(2*int(m)+1-e)%(n-2)
                if args.bad_chart_sign:K=(-K)%(n-2)
                check('source_to_intrinsic_dictionary',K==k)
                for h in range(-3,4):
                    mh=((t+h*cycle)*d+offset-a-(1-e))/2
                    check('arbitrary_full_cone_lift',mh.denominator==1 and (int(mh)-int(m))%r==0)
                ar=1-b;br=1-a
                sr=n*(ar+br if terminal=='P' else br-ar)/2
                kr=int(n-1-sr if terminal=='P' else sr-1)%(n-2)
                check('physical_reversal_parity',kr==((-k)%(n-2) if terminal=='P' else k))
                af=d-a;bf=1+F(2,n)-b
                sf=n*(af+bf if terminal=='P' else bf-af)/2
                kf=int(n-1-sf if terminal=='P' else sf-1)%(n-2)
                check('initial_Q_fold_reflection',kf==(-k)%(n-2))
                neg=(-k)%(n-2)
                check('canonical_weight_reflection',neg==0 if k==0 else neg+1==n-k-1)

# Full dihedral orbits of bounded primitive marked-lattice directions.
def tri_norm(v):p,q=v;return p*p-p*q+q*q
def tri_rot(v):p,q=v;return p-q,p
def hex_hit(v):
    p,q=v;s=(p+q)%3;mult=1 if args.bad_hex_first_hit else (2 if s==2 else 1)
    z=(mult*p,mult*q)
    check('hex_first_actual_mark',sum(z)%3!=2)
    if mult==2:check('hex_only_skipped_point_unmarked',sum(v)%3==2)
    if (z[0]%3,z[1]%3)==(1,2):k=1
    elif z[0]%2==z[1]%2==0:k=2
    elif (z[0]%3,z[1]%3)==(2,1):k=3
    else:k=0
    w2={0:F(1,4),1:F(3,4),2:F(1),3:F(3,4)}[k]
    return F(tri_norm(z))/w2
for p in range(-25,26):
    for q in range(-25,26):
        if gcd(p,q)!=1:continue
        v=(p,q);base=hex_hit(v);z=v
        for _ in range(6):
            for zz in (z,(z[1],z[0])):
                check('triangle_full_dihedral_first_hit',gcd(*zz)==1 and tri_norm(zz)==tri_norm(v))
                check('hex_full_dihedral_ratio',hex_hit(zz)==base)
            z=tri_rot(z)
        k=int(p%2==q%2==1);base=F(p*p+q*q)/({0:F(1,2),1:F(1)}[k]);z=v
        for _ in range(4):
            for pp,qq in (z,(z[0],-z[1])):
                kk=int(pp%2==qq%2==1)
                check('square_full_dihedral_ratio',gcd(pp,qq)==1 and F(pp*pp+qq*qq)/({0:F(1,2),1:F(1)}[kk])==base)
            z=(-z[1],z[0])

# Independently compute every earliest positive collision of the pentagon path.
# Coordinates are x in Q(sqrt(5)), y divided by positive sin(pi/5).
@dataclass(frozen=True)
class Q:
    a:F=F(0)
    b:F=F(0)
    def __add__(self,other):
        o=coerce(other);return Q(self.a+o.a,self.b+o.b)
    __radd__=__add__
    def __neg__(self):return Q(-self.a,-self.b)
    def __sub__(self,other):return self+-coerce(other)
    def __rsub__(self,other):return coerce(other)+-self
    def __mul__(self,other):
        o=coerce(other);return Q(self.a*o.a+5*self.b*o.b,self.a*o.b+self.b*o.a)
    __rmul__=__mul__
    def __truediv__(self,other):
        o=coerce(other);den=o.a*o.a-5*o.b*o.b
        return self*Q(o.a/den,-o.b/den)
    def positive(self):
        if not self.b:return self.a>0
        if self.a>=0 and self.b>0:return True
        if self.a<=0 and self.b<0:return False
        return 5*self.b*self.b>self.a*self.a if self.b>0 else self.a*self.a>5*self.b*self.b
    def serial(self):return [str(self.a),str(self.b)]
def coerce(x):return x if isinstance(x,Q) else Q(F(x))
def vec(x,y):return (coerce(x),coerce(y))
def plus(u,v):return (u[0]+v[0],u[1]+v[1])
def minus(u,v):return (u[0]-v[0],u[1]-v[1])
def times(a,v):return (a*v[0],a*v[1])
def cross(u,v):return u[0]*v[1]-u[1]*v[0]
c=Q(F(1,4),F(1,4));u=Q(F(-1,4),F(1,4));s2=1-c*c
vertices=[vec(0,0),vec(-u,2*c),vec(F(1,2),2*c+1),vec(1+u,2*c),vec(1,0)]
def dot(v,w):return v[0]*w[0]+s2*v[1]*w[1]
def collide(p,d):
    hits=[]
    for j,a in enumerate(vertices):
        e=minus(vertices[(j+1)%5],a);den=cross(d,e)
        if den==Q():continue
        t=cross(minus(a,p),e)/den;b=cross(minus(a,p),d)/den
        if t.positive() and (b==Q() or b.positive()) and (1-b==Q() or (1-b).positive()):hits.append((t,j,b))
    check('collision_candidate_exists',bool(hits))
    first=hits[0][0]
    for t,j,b in hits:
        if (first-t).positive():first=t
    at=[(j,b) for t,j,b in hits if t==first]
    check('earliest_collision_order',all(t==first or (t-first).positive() for t,j,b in hits))
    return plus(p,times(first,d)),at,first
p=vertices[0];d=vec(0,1);collisions=[]
for stage,expected_side in enumerate([1,3,1,None]):
    p,at,t=collide(p,d)
    collisions.append({'stage':stage+1,'point':[a.serial() for a in p],'sides':[j for j,b in at],'ray_parameter':t.serial()})
    if expected_side is None:
        check('final_collision_is_original_vertex',p==vertices[0] and {j for j,b in at}=={0,4})
        check('final_incoming_direction_down',d[0]==Q() and (-d[1]).positive())
    else:
        check('expected_strict_side_collision',len(at)==1 and at[0][0]==expected_side and at[0][1].positive() and (1-at[0][1]).positive())
        e=minus(vertices[(expected_side+1)%5],vertices[expected_side])
        reflected=minus(times(2*dot(d,e)/dot(e,e),e),d)
        if args.bad_first_reflection and stage==0:reflected=plus(reflected,times(2,d))
        check('reflection_preserves_speed',dot(reflected,reflected)==dot(d,d))
        d=reflected
check('palindrome_points',collisions[0]['point']==collisions[2]['point'])
alpha=beta=F(1,2);k=int(F(5,2)*(beta-alpha)-1)%3
reverse=int(F(5,2)*((1-alpha)-(1-beta))-1)%3
check('physical_palindrome_label_retained',k==reverse==2)
check('old_unqualified_negation_falsified',reverse!=(-k)%3)
receipt={'status':'PASS','counts':counts,'exact_check_count':sum(counts.values()),'ranges':{'source_n':[3,101],'lattice_box':[-25,25],'sheet_lift_offsets':[-3,3]},'independent_collision_trace':collisions,'limitations':'Finite exact source/collision/lattice controls. Universal arguments and classical imports require mathematical/source review.'}
print(json.dumps(receipt,indent=2,sort_keys=True))
