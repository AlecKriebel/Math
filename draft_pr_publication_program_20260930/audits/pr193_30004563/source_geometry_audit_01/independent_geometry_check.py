#!/usr/bin/env python3
"""Independent exact arithmetic reconstruction; no original checker/data imported."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
from datetime import datetime, timezone
import json, sys
sys.set_int_max_str_digits(0)

N_CHECKS=0
def check(x):
    global N_CHECKS
    N_CHECKS+=1
    if not x: raise ArithmeticError("Independent interval check failed")
class I:
    def __init__(self,a,b=None):
        if isinstance(a,I): self.a,self.b=a.a,a.b
        else: self.a,self.b=F(a),F(a if b is None else b)
        check(self.a<=self.b)
    def __add__(self,o):
        o=I(o);return I(self.a+o.a,self.b+o.b)
    __radd__=__add__
    def __neg__(self):return I(-self.b,-self.a)
    def __sub__(self,o):return self+-I(o)
    def __rsub__(self,o):return I(o)+-self
    def __mul__(self,o):
        o=I(o);v=[x*y for x in (self.a,self.b) for y in (o.a,o.b)];return I(min(v),max(v))
    __rmul__=__mul__
    def __truediv__(self,o):
        o=I(o);check(o.a>0 or o.b<0);return self*I(1/o.b,1/o.a)
    def __pow__(self,n):
        check(isinstance(n,int) and n>=0)
        if n==0:return I(1)
        if n%2:return I(self.a**n,self.b**n)
        if self.a>=0:return I(self.a**n,self.b**n)
        if self.b<=0:return I(self.b**n,self.a**n)
        return I(0,max(self.a**n,self.b**n))
    def sign(self):
        if self.a>0:return 1
        if self.b<0:return -1
        return 0
    def dump(self):return {'lo':str(self.a),'hi':str(self.b),'approx':[float(self.a),float(self.b)]}

def root8_exact(q):
    q=F(q);check(q>=0)
    if q==0:return I(0)
    scale=1<<220
    n=(q.numerator*scale**8)//q.denominator
    # General integer bisection for eighth root, independent of chained isqrt.
    lo,hi=0,1<<((n.bit_length()+7)//8)
    while hi-lo>1:
        mid=(lo+hi)//2
        if mid**8<=n:lo=mid
        else:hi=mid
    check(F(lo,scale)**8<=q<F(hi,scale)**8)
    return I(F(lo,scale),F(hi,scale))
def root8(q):
    q=I(q);check(q.a>=0);return I(root8_exact(q.a).a,root8_exact(q.b).b)
def add(p,q):return tuple(x+y for x,y in zip(p,q))
def sub(p,q):return tuple(x-y for x,y in zip(p,q))
def norm2(p):return p[0]**2+p[1]**2
def dist16(p,q):return norm2(sub(p,q))**8
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def orient(a,b,c):return det(sub(b,a),sub(c,a))
def bbox_disjoint(p,q):return any(a.b<b.a or b.b<a.a for a,b in zip(p,q))
def strict_cross(a,b,c,d):
    z=[orient(a,b,c),orient(a,b,d),orient(c,d,a),orient(c,d,b)]
    return z[0].sign()*z[1].sign()==-1 and z[2].sign()*z[3].sign()==-1,z

def level_parameter(q,h,level):
    n=norm2(q);check(n.sign()>0)
    def f(t):return n**8*((I(t-1)**2+I(h)**2)**8-(I(t)**2+I(h)**2)**8)-level
    lo,hi=F(-16),F(16)
    check(f(lo).sign()==1 and f(hi).sign()==-1)
    for _ in range(190):
        mid=(lo+hi)/2;s=f(mid).sign();check(s!=0)
        if s>0:lo=mid
        else:hi=mid
    check(f(lo).sign()==1 and f(hi).sign()==-1)
    return I(lo,hi)
def boundary(q,h,level,base=(I(0),I(0))):
    t=level_parameter(q,F(h),I(level));x,y=q
    return add(base,(t*x-h*y,t*y+h*x)),t
A=(I(0),I(0));B=(I(F(2073,10000)),I(0));C=(I(F(4719,10000)),I(F(64,10000)))
lam=F(27,1250);mu=F(1)
A1,t1=boundary(C,10,mu)
A3,t3=boundary(B,1,lam)
A5,t5=boundary(sub(C,B),-10,mu-lam,B)
P=[A1,A,A3,B,A5,C]
# Verify all 20 boundary triple determinants nonzero, all pairs distinct.
triples=[]
for i,j,k in combinations(range(6),3):
    z=orient(P[i],P[j],P[k]);check(z.sign()!=0);triples.append({'indices':[i+1,j+1,k+1],'det':z.dump()})
for i,j in combinations(range(6),2):check(bbox_disjoint(P[i],P[j]))

# Outgoing scalar construction with arbitrary vector foci.
def construct(s,base,b,c,L,M):
    s=I(s);u=root8(s);v=root8(s+L);w=root8(s+M)
    D=det(b,c);check(D.sign()!=0)
    r=norm2(b)+u-v;t=norm2(c)+u-w
    rel=((r*c[1]-t*b[1])/(2*D),(b[0]*t-c[0]*r)/(2*D))
    return norm2(rel)-u,add(base,rel)
G=lambda s:construct(s,A,B,C,lam,mu)
cuts=list(map(F,['9/10000','11/10000','13/10000','1/2','1','100000000000000000']))
signs=[G(s)[0] for s in cuts]
for z,sgn in zip(signs,[1,-1,1,-1,1,-1]):check(z.sign()==sgn)
centers=[];root_intervals=[]
for lo,hi in zip(cuts,cuts[1:]):
    sl=G(lo)[0].sign()
    for _ in range(180):
        mid=(lo+hi)/2;sm=G(mid)[0].sign();check(sm!=0)
        if sl==sm:lo=mid
        else:hi=mid
    check(G(lo)[0].sign()*G(hi)[0].sign()==-1)
    z,x=G(I(lo,hi));centers.append(x);root_intervals.append([str(lo),str(hi)])

# Incoming scalar construction, using interval-enclosed exact algebraic foci/levels.
L=dist16(B,A5)-dist16(B,A3)
M=dist16(A,A1)-dist16(A,A3)
check(L.sign()==M.sign()==1)
b=sub(A5,A3);c=sub(A1,A3)
H=lambda s:construct(s,A3,b,c,L,M)
hlo,hhi=F(1,100),F(11,1000)
hbounds=[H(hlo)[0],H(hhi)[0]];check(hbounds[0].sign()==1 and hbounds[1].sign()==-1)
z=H(I(hlo,hhi))[1]

# Center exclusions and all line degeneracies independently checked.
for x in centers+[z]:
    for p in P:check(bbox_disjoint(x,p))
    for i,j in combinations(range(6),2):check(orient(P[i],P[j],x).sign()!=0)
for i,j in combinations(range(5),2):check(bbox_disjoint(centers[i],centers[j]))

# Source equations directly enclose zero, in addition to symbolic cancellation proof.
def quad(a,b,c,x):return dist16(a,b)+dist16(c,x)-dist16(a,x)-dist16(b,c)
new=[]
for x in centers:
    row=[quad(P[i],P[(i+1)%6],P[(i+2)%6],x) for i in (1,3,5)]
    for r in row:check(r.a<=0<=r.b)
    new.append([r.dump() for r in row])
old=[quad(P[i],P[i+1],P[(i+2)%6],z) for i in (0,2,4)]
for r in old:check(r.a<=0<=r.b)

# Independent transversality: determinant of exact polynomial gradient rows.
def grad_diff(x,q,r):
    a=sub(x,q);b=sub(x,r)
    return tuple(16*(a[k]*norm2(a)**7-b[k]*norm2(b)**7) for k in (0,1))
outgoing_jacobians=[det(grad_diff(x,B,A),grad_diff(x,C,A)) for x in centers]
for j in outgoing_jacobians:check(j.sign()!=0)
incoming_jacobian=det(grad_diff(z,A5,A3),grad_diff(z,A1,A3))
check(incoming_jacobian.sign()!=0)

# Boundary fixed-crossing certificates; count proper faces, show strict crosses when present.
outer_cross=[]
for i,j in combinations(range(6),2):
    if (i-j)%6 in (1,5):continue
    yes,ds=strict_cross(P[i],P[(i+1)%6],P[j],P[(j+1)%6])
    if yes:outer_cross.append({'edges':[str(i+1)+str((i+1)%6+1),str(j+1)+str((j+1)%6+1)],'orientation_determinants':[d.dump() for d in ds]})
def face_geometry(x,indices):
    out=[]
    for i in indices:
        verts=[P[i],P[(i+1)%6],P[(i+2)%6],x]
        cross=[]
        for e,f in [(0,2),(1,3)]:
            yes,ds=strict_cross(verts[e],verts[(e+1)%4],verts[f],verts[(f+1)%4])
            if yes:cross.append({'opposite_edge_indices':[e,f],'determinants':[d.dump() for d in ds]})
        area=sum((det(verts[k],verts[(k+1)%4]) for k in range(4)),I(0))/2
        check(area.sign()!=0)
        out.append({'boundary_triple':[i+1,(i+1)%6+1,(i+2)%6+1],'signed_area':area.dump(),'strict_crossings':cross})
    return out
out={'utc':datetime.now(timezone.utc).isoformat(),'status':'INDEPENDENT_EXACT_RECONSTRUCTION_PASS','checks':N_CHECKS,'method':'Fraction intervals; direct integer-bisection eighth-root brackets; all original author code and certificate excluded','boundary':[{'A':i+1,'coordinates':[v.dump() for v in p]} for i,p in enumerate(P)],'parameter_boxes':[t.dump() for t in (t1,t3,t5)],'boundary_triple_determinants':triples,'G_cutpoint_certificates':[{'s':str(s),'G':v.dump()} for s,v in zip(cuts,signs)],'outgoing_root_intervals':root_intervals,'outgoing_coordinate_boxes':[[v.dump() for v in x] for x in centers],'incoming_levels':[L.dump(),M.dump()],'H_endpoint_certificates':[h.dump() for h in hbounds],'incoming_coordinate_box':[v.dump() for v in z],'direct_new_quad_residual_enclosures':new,'direct_old_quad_residual_enclosures':[r.dump() for r in old],'outgoing_jacobian_determinants':[j.dump() for j in outgoing_jacobians],'incoming_jacobian_determinant':incoming_jacobian.dump(),'boundary_crossings':outer_cross,'incoming_face_geometry':face_geometry(z,(0,2,4)),'outgoing_face_geometry':[face_geometry(x,(1,3,5)) for x in centers]}
out['checks']=N_CHECKS
Path(__file__).with_name('INDEPENDENT_CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'checks':N_CHECKS,'G':[[str(s),v.sign(),float(v.a)] for s,v in zip(cuts,signs)],'incoming_H':[float(h.a) for h in hbounds],'outer_crossings':[r['edges'] for r in outer_cross],'outgoing_jacobians':[float(j.a) for j in outgoing_jacobians],'incoming_jacobian':incoming_jacobian.dump()['approx'],'incoming_faces_crossed':[bool(t['strict_crossings']) for t in out['incoming_face_geometry']],'outgoing_faces_crossed':[[bool(t['strict_crossings']) for t in row] for row in out['outgoing_face_geometry']],'center_boxes':[[[float(v.a),float(v.b)] for v in x] for x in centers]},indent=2))
