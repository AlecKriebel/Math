#!/usr/bin/env python3
"""Independent exact reconstruction. No external repository code is imported.
Q(sqrt(5)) arithmetic and complex coordinates 1,zeta, zeta=exp(2*pi*i/5).
Only the literal face/path data originate in the external certificate.
"""
from fractions import Fraction as F
from dataclasses import dataclass
from math import sqrt, atan2, pi
import json

@dataclass(frozen=True)
class K:
    a:F=F(0)
    b:F=F(0)
    def __post_init__(self):
        object.__setattr__(self,'a',F(self.a)); object.__setattr__(self,'b',F(self.b))
    @staticmethod
    def of(x): return x if isinstance(x,K) else K(x)
    def __add__(self,x):
        x=K.of(x); return K(self.a+x.a,self.b+x.b)
    __radd__=__add__
    def __neg__(self): return K(-self.a,-self.b)
    def __sub__(self,x): return self+-K.of(x)
    def __rsub__(self,x):return K.of(x)+-self
    def __mul__(self,x):
        x=K.of(x); return K(self.a*x.a+5*self.b*x.b,self.a*x.b+self.b*x.a)
    __rmul__=__mul__
    def __truediv__(self,x):
        x=K.of(x); return self*K(x.a,-x.b)/(x.a*x.a-5*x.b*x.b) if x.b else K(self.a/x.a,self.b/x.a)
    def sign(self):
        a,b=self.a,self.b
        if b==0:return (a>0)-(a<0)
        if a==0:return (b>0)-(b<0)
        if a>0 and b>0:return 1
        if a<0 and b<0:return -1
        q=a*a-5*b*b
        return ((q>0)-(q<0))*((a>0)-(a<0))
    def __float__(self):return float(self.a)+float(self.b)*sqrt(5)
    def __repr__(self):return f'({self.a})+({self.b})*sqrt(5)'

C=K(F(-1,2),F(1,2)) # 2 cos72 = phi-1
@dataclass(frozen=True)
class Z:
    a:K=K()
    b:K=K()
    def __post_init__(self):
        object.__setattr__(self,'a',K.of(self.a));object.__setattr__(self,'b',K.of(self.b))
    @staticmethod
    def of(x):return x if isinstance(x,Z) else Z(x)
    def __add__(self,x):
        x=Z.of(x);return Z(self.a+x.a,self.b+x.b)
    __radd__=__add__
    def __neg__(self):return Z(-self.a,-self.b)
    def __sub__(self,x):return self+-Z.of(x)
    def __rsub__(self,x):return Z.of(x)+-self
    def __mul__(self,x):
        x=Z.of(x);return Z(self.a*x.a-self.b*x.b,self.a*x.b+self.b*x.a+C*self.b*x.b)
    __rmul__=__mul__
    def conj(self):return Z(self.a+C*self.b,-self.b)
    def norm(self):return self.a*self.a+C*self.a*self.b+self.b*self.b
    def __truediv__(self,x):
        x=Z.of(x); q=self*x.conj(); n=x.norm();return Z(q.a/n,q.b/n)
    def xy(self):return float(self.a)+float(self.b)*float(C)/2,float(self.b)*sqrt(1-float(C)**2/4)

R=Z(0,1)
def det(u,v):return u.a*v.b-u.b*v.a # actual determinant divided by positive sin72

def arg(z):x,y=z.xy();return atan2(y,x)*180/pi

def interior_angle(u,v):return abs((arg(v)-arg(u)+180)%360-180)

FACES=[[6,18,4,8,10],[10,8,0,16,2],[17,16,0,12,1],[3,13,2,16,17],[5,9,1,12,14],[14,12,0,8,4],[5,14,4,18,19],[3,17,1,9,11],[11,9,5,19,7],[6,10,2,13,15],[19,18,6,15,7],[15,13,3,11,7]]
WORD=[1,3,11,8,6,5,1,3,11,10,8,6,4,5,2,1]
EDGES=[(2,16),(3,13),(7,11),(5,19),(4,14),(0,8),(2,16),(3,13),(7,15),(7,19),(5,19),(5,14),(12,14),(0,12),(0,16)]

def polygon(face,u,v,pu,pv):
    """Use the physical cyclic face order, maintaining CCW orientation."""
    i=face.index(u); assert face[(i+1)%5]==v
    out={u:pu}; edge=pv-pu; p=pu
    for k in range(1,5):
        p=p+edge;out[face[(i+k)%5]]=p;edge=edge*R
    assert p+edge==pu
    return out

def reconstruct():
    polys=[polygon(FACES[1],0,16,Z(),Z(1))]
    labels=[{v:i for i,v in enumerate([0,16,2,10,8])}]
    for k,face_no in enumerate(WORD[1:]):
        old=polys[-1];face=FACES[face_no];u,v=EDGES[k]
        assert set(FACES[WORD[k]])&set(face)=={u,v}
        if face[(face.index(u)+1)%5]!=v:u,v=v,u
        new=polygon(face,u,v,old[u],old[v]);polys.append(new)
        # Reflect old labeled occurrence in its shared edge, not its physical orientation.
        a,b=old[u],old[v];d=b-a
        reflected={a+d*((z-a)/d).conj():labels[-1][w] for w,z in old.items()}
        assert set(reflected)==set(new.values())
        labels.append({w:reflected[z] for w,z in new.items()})
    return polys,labels

def check():
    polys,labels=reconstruct();origin=polys[0][0];end=polys[-1][2];v=end-origin
    assert v.norm()==K(F(307,2),F(137,2))
    graph={i:set() for i in range(20)}
    edges={}
    for face in FACES:
        for a,b in zip(face,face[1:]+face[:1]):
            graph[a].add(b);graph[b].add(a);edges.setdefault(tuple(sorted([a,b])),[]).append((a,b))
    assert len(edges)==30 and all(len(x)==2 and x[0]==x[1][::-1] for x in edges.values())
    assert all(len(x)==3 for x in graph.values())
    dist={0:0};todo=[0]
    for a in todo:
        for b in graph[a]:
            if b not in dist:dist[b]=dist[a]+1;todo.append(b)
    assert dist[2]==2
    crossings=[];prev=K()
    for i,(a,b) in enumerate(EDGES):
        p,q=polys[i][a]-origin,polys[i][b]-origin;e=q-p
        t=det(p,e)/det(v,e);s=det(p,v)/det(v,e)
        assert t.sign()>0 and (1-t).sign()>0 and s.sign()>0 and (1-s).sign()>0 and (t-prev).sign()>0
        assert v*t==p+e*s
        crossings.append((t,s));prev=t
    # Convexity proves every segment between consecutive contacts stays in its face.
    cuts=[K()]+[t for t,s in crossings]+[K(1)]
    hits=[]
    for i,poly in enumerate(polys):
        face=FACES[WORD[i]]
        mid=v*((cuts[i]+cuts[i+1])/2)+origin
        for a,b in zip(face,face[1:]+face[:1]):
            assert det(poly[b]-poly[a],mid-poly[a]).sign()>0
        for w,z in poly.items():
            if det(v,z-origin).sign()==0:
                t=(z-origin)/v;assert t.b==K()
                if t.a.sign()>=0 and (1-t.a).sign()>=0:hits.append((i,w,t.a))
    assert hits==[(0,0,K()),(15,2,K(1))]
    s0=polys[0][16]-origin
    # Figure8: alpha interior angle from outgoing initial polygon boundary;
    # pi-beta interior angle from outgoing terminal BILLIARD boundary.
    terminal_label=labels[-1][2]
    next_billiard=next(w for w,l in labels[-1].items() if l==(terminal_label+1)%5)
    source_ray=polys[-1][next_billiard]-end
    physical_ray=polys[-1][10]-end
    alpha=interior_angle(s0,v)
    source_beta=180-interior_angle(source_ray,-v)
    physical_angle=interior_angle(physical_ray,-v)
    assert next_billiard==16
    assert source_ray==R*R*R*s0 # source terminal ray216degrees
    assert -s0==R*physical_ray # external ray identity itself is correct
    assert det(s0,v).sign()>0 and det(v,polys[0][8]-origin).sign()>0
    assert det(v,-R*R*R).sign()>0 # 0<alpha<36degrees, exact branch certificate
    assert det(-v,source_ray).sign()>0 # reversed tangent180+alpha; ray216
    # Thus pi-beta=36-alpha and beta-alpha=144degrees exactly: source typeA1.
    return dict(squared_length=repr(v.norm()),length=sqrt(float(v.norm())),graph_distance=dist[2],vertex_hits=[(i,w,repr(t)) for i,w,t in hits],crossings=[dict(t=repr(t),s=repr(s)) for t,s in crossings],terminal_billiard_labels=labels[-1],alpha_degrees=alpha,fuchs_beta_degrees=source_beta,fuchs_beta_minus_alpha=source_beta-alpha,external_terminal_interior_angle_degrees=physical_angle,external_interior_minus_alpha=physical_angle-alpha,source_ray=repr(source_ray),physical_ray=repr(physical_ray),endpoint=repr(v))

if __name__=='__main__':
    print(json.dumps(check(),indent=2))
