#!/usr/bin/env python3
"""Exact finite controls, not a proof of the unrestricted existence question."""
from fractions import Fraction as F
import argparse, json, sys

def add(a,b): return (a[0]+b[0],a[1]+b[1])
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def scale(t,a): return (t*a[0],t*a[1])
def dot(a,b): return a[0]*b[0]+a[1]*b[1]
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def reflect(v,tangent): return sub(scale(2*dot(v,tangent)/dot(tangent,tangent),tangent),v)
def mat(n): return ((1-2*n[0]*n[0],-2*n[0]*n[1]),(-2*n[1]*n[0],1-2*n[1]*n[1]))
def mul(a,b): return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)) for i in range(2))
def det(a): return a[0][0]*a[1][1]-a[0][1]*a[1][0]
def unit(t): return ((1-t*t)/(1+t*t), 2*t/(1+t*t))

class Checks:
    def __init__(self): self.count=0; self.groups={}
    def eq(self,a,b,label):
        self.count+=1; self.groups[label]=self.groups.get(label,0)+1
        if a != b: raise AssertionError((label,a,b))
    def yes(self,a,label): self.eq(bool(a),True,label)

class SingularRay(Exception): pass

def trace_polygon(vertices,start,velocity,cap=12):
    """Intersections and specular reflection use exact fractions throughout."""
    edges=list(zip(vertices,vertices[1:]+vertices[:1]))
    p,v=start,velocity; hits=[]
    for _ in range(cap):
        candidates=[]
        for i,(a,b) in enumerate(edges):
            e=sub(b,a); den=cross(v,e)
            if den==0: continue
            tau=cross(sub(a,p),e)/den
            lam=cross(sub(a,p),v)/den
            if tau>0 and 0<=lam<=1: candidates.append((tau,i,lam))
        if not candidates:
            if not hits: raise AssertionError('ray did not hit body')
            return p,v,hits
        tau=min(x[0] for x in candidates)
        nearest=[x for x in candidates if x[0]==tau]
        if len(nearest)!=1 or nearest[0][2] in (0,1): raise SingularRay
        _,i,_=nearest[0]
        p=add(p,scale(tau,v)); a,b=edges[i]
        v=reflect(v,sub(b,a)); hits.append((i,p,v))
    raise AssertionError('unexpected reflection cap')

def notched_body(n):
    # Clockwise polygon, orientation is irrelevant for vector reflection.
    vs=[(F(0),F(-1)),(F(0),F(0))]
    for k in range(n):
        vs += [(F(2*k+1,2*n),F(-1,2*n)),(F(k+1,n),F(0))]
    vs.append((F(1),F(-1)))
    return vs

def run(mutant=None):
    c=Checks(); units=[unit(F(t,5)) for t in range(-7,8)]
    for v in units:
        for w in units:
            r=(1-dot(v,w))/2
            c.eq(1-r,dot(add(v,w),add(v,w))/4,'defect_identity')
            c.yes(0<=r<=1,'resistance_bounds')
        for normal in units:
            tangent=(-normal[1],normal[0]); w=reflect(v,tangent)
            c.eq(dot(w,w),1,'reflection_norm')
            c.eq(w,sub(v,scale(2*dot(v,normal),normal)),'reflection_formula')
    c.eq(F(1,3)-F(-1,3),F(2,3),'exposed_integral')
    for n1 in units:
        for n2 in units:
            q=mul(mat(n2),mat(n1)); plus=((q[0][0]+1,q[0][1]),(q[1][0],q[1][1]+1))
            c.eq(det(q),1,'rotation_determinant')
            c.eq(det(plus),4*dot(n1,n2)**2,'two_bounce_rigidity')
        n2=(-n1[1],n1[0]); c.eq(mul(mat(n2),mat(n1)),((-1,0),(0,-1)),'perpendicular_pair')
    for t in [F(i,12) for i in range(-10,11)]:
        q,p=unit(t)
        for h in [F(1,3),F(2),F(7,4)]:
            Aprime=-2*h/q**3; ellprime=2*h*p/q**3
            c.eq(ellprime,-p*Aprime,'length_variation')
            sign=1 if mutant=='jacobian' else -1
            c.eq(det(((sign,Aprime),(0,-1))),1,'symplectic_sign')
    tested=0; singular=0; one=two=0
    for n in (1,2,3,5):
        body=notched_body(n)
        for k in range(n):
            for ai in range(1,8):
                a=F(ai,8)
                for ri in range(1,18):
                    r=F(ri,18)
                    if r in ((1-a)/2,1-a):
                        singular+=1; continue
                    x=(k+r)/n; v=(a,F(-1))
                    p,w,hits=trace_polygon(body,(x,F(0)),v)
                    is_two=r<1-a
                    expected=2 if is_two else 1
                    c.eq(len(hits),expected,'sawtooth_hit_count')
                    want=(-a,F(1)) if is_two else (F(-1),a)
                    if mutant=='all_retro': want=(-a,F(1))
                    c.eq(w,want,'sawtooth_velocity')
                    c.eq(dot(w,w),dot(v,v),'sawtooth_speed')
                    exitx=p[0]-p[1]*w[0]/w[1]
                    local_exit=1-a-r if is_two else (r+a-1)/a
                    c.eq(exitx,(k+local_exit)/n,'sawtooth_exit')
                    c.yes(F(k,n)<exitx<F(k+1,n),'same_cell_exit')
                    c.yes(w[0]<0 and a>0,'flat_scattering_separation')
                    one+=not is_two; two+=is_two; tested+=1
    # Branch fraction and angle-band separation are proved for all real parameters
    # in TURN_5; these finite exact evaluations are merely controls.
    result={'status':'PASS_EXACT_FINITE_CONTROLS','assertions':c.count,'groups':c.groups,
            'sawtooth_cases':tested,'one_bounce_cases':one,'two_bounce_cases':two,
            'singular_parameter_pairs_excluded':singular,'numeric_simulations':0,
            'full_problem_solved':False,'scope':'finite exact arithmetic controls; universal arguments are in the five turn documents'}
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--mutant',choices=['jacobian','all_retro']); args=parser.parse_args()
    if sys.flags.optimize: raise SystemExit('optimized Python is not an accepted verification mode')
    print(json.dumps(run(args.mutant),indent=2,sort_keys=True))
