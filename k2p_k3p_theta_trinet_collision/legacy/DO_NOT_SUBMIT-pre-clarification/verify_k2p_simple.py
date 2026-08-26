#!/usr/bin/env python3
"""Short exact audit of the simple K2P tree/theta collision.

Only Python's standard library is used. Algebra is in Q(s), s^2=71.
"""
from __future__ import annotations
import itertools,json
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path
C=json.loads((Path(__file__).parent/'certificate_k2p_simple.json').read_text())
def need(x,msg):
    if not x:raise AssertionError(msg)
@dataclass(frozen=True)
class Q:
    a:F;b:F=F(0)
    def __add__(self,o):return Q(self.a+o.a,self.b+o.b)
    def __radd__(self,o):return self if o==0 else NotImplemented
    def __neg__(self):return Q(-self.a,-self.b)
    def __sub__(self,o):return self+(-o)
    def __mul__(self,o):return Q(self.a*o.a+71*self.b*o.b,self.a*o.b+self.b*o.a)
    def scale(self,r):r=F(r);return Q(r*self.a,r*self.b)
    def __pow__(self,n):
        z=ONE;y=self
        while n:
            if n&1:z=z*y
            y=y*y;n//=2
        return z
    def interval(self):
        lo,hi=map(F,C['field']['positive_root_interval'])
        return ((self.a+self.b*lo,self.a+self.b*hi) if self.b>=0 else (self.a+self.b*hi,self.a+self.b*lo))
    def positive(self,msg):need(self.interval()[0]>0,msg)
    def raw(self):return [str(self.a),str(self.b)]
ZERO=Q(F(0));ONE=Q(F(1))
def parse(x):return Q(F(x[0]),F(x[1]))
def vparse(row):return tuple(parse(x) for x in row)
V={k:vparse(v) for k,v in C['network_vectors'].items()}
TREE={k:vparse(v) for k,v in C['comparison_tree'].items() if k in ('alpha','beta','gamma')}
P=vparse(C['core_factors']['P']);R=vparse(C['core_factors']['R'])
H=((1,1,1,1),(1,1,-1,-1),(1,-1,1,-1),(1,-1,-1,1));SYM='ACGT'
def probs(e):
    _,c,g,t=e
    return ((ONE+c+g+t).scale(F(1,4)),(ONE+c-g-t).scale(F(1,4)),(ONE-c+g-t).scale(F(1,4)),(ONE-c-g+t).scale(F(1,4)))
def topology():
    nodes={x['id']:x['type'] for x in C['rooted_network']['vertices']};arcs=[(x['parent'],x['child']) for x in C['rooted_network']['arcs']]
    indeg={x:0 for x in nodes};out={x:0 for x in nodes}
    for a,b in arcs:out[a]+=1;indeg[b]+=1
    need(indeg['rho']==0 and out['rho']==2,'root type')
    for x,t in nodes.items():
        if t=='tree':need((indeg[x],out[x])==(1,2),x+' tree type')
        if t=='reticulation':need((indeg[x],out[x])==(2,1),x+' reticulation type')
        if t=='leaf':need((indeg[x],out[x])==(1,0),x+' leaf type')
    D=indeg.copy();stack=[x for x in nodes if D[x]==0];seen=[]
    while stack:
        x=stack.pop();seen.append(x)
        for a,b in arcs:
            if a==x:
                D[b]-=1
                if D[b]==0:stack.append(b)
    need(len(seen)==len(nodes),'acyclic')
    core={tuple(sorted(e)) for p in C['semi_directed']['theta_paths'] for e in zip(p,p[1:])}
    want={tuple(sorted(e)) for e in [('p','u'),('u','q'),('p','r2'),('r2','q'),('p','r3'),('r3','q')]}
    need(core==want,'theta core');need(len(C['semi_directed']['incident_leaf_edges'])==3,'three leaf sides')
    print('[topology] PASS  rooted binary DAG suppresses to a strict level-two theta 3-blob')
def edges():
    for name,e in V.items():
        need(e[0]==ONE and e[1]==e[3],name+' K2P form')
        for x in e[1:]:x.positive(name+' eigenvalue');(ONE-x).positive(name+' eigenvalue <1')
        ps=probs(e)
        for p in ps:p.positive(name+' transition')
        need(sum(ps,ZERO)==ONE,name+' transition sum')
    for name,e in TREE.items():
        need(e[1]==e[3],name+' K2P form')
        for x in e[1:]:x.positive(name+' eigenvalue');(ONE-x).positive(name+' eigenvalue <1')
        for p in probs(e):p.positive(name+' transition')
    need(V['K_odot_K']==tuple(V['K'][i]*V['K'][i] for i in range(4)),'root suppression edge')
    print('[parameters] PASS  all network, effective, and tree edges lie strictly in Theta_0')
def collision():
    K,U,W,S,T0=V['K'],V['U'],V['V'],V['S'],V['T'];M={}
    for y,z in itertools.product(range(4),repeat=2):
        x=y^z;terms=(S[y]*S[z]*U[x],S[y]*T0[z]*U[y]*W[z],T0[y]*S[z]*U[z]*W[y],T0[y]*T0[z]*W[x])
        M[y,z]=sum(terms,ZERO).scale(F(1,4));need(M[y,z]==P[x]*R[y]*R[z],f'factor {y,z}')
    qn={};qt={}
    for x,y,z in itertools.product(range(4),repeat=3):
        if x^y^z:qn[x,y,z]=qt[x,y,z]=ZERO
        else:qn[x,y,z]=K[x]*K[x]*K[y]*K[z]*M[y,z];qt[x,y,z]=TREE['alpha'][x]*TREE['beta'][y]*TREE['gamma'][z]
        need(qn[x,y,z]==qt[x,y,z],f'Fourier {x,y,z}')
    pp={}
    for a,b,c in itertools.product(range(4),repeat=3):
        z=ZERO
        for x,y,y3 in itertools.product(range(4),repeat=3):z+=qn[x,y,y3].scale(F(H[x][a]*H[y][b]*H[y3][c],64))
        z.positive(f'pattern {a,b,c}');pp[a,b,c]=z
    need(sum(pp.values(),ZERO)==ONE,'pattern normalization')
    q=lambda s:qn[tuple(SYM.index(c) for c in s)]
    inv=q('AGG')*q('GAG')*(q('CCA')**2)-q('AAA')*q('GGA')*(q('TCG')**2);need(inv==ZERO,'Q')
    m=min(pp,key=lambda x:pp[x].interval()[0]);need(pp[m].raw()==C['minimum_pattern']['value'],'minimum')
    print('[collision] PASS  all 16 factors, 64 Fourier coordinates, and 64 positive patterns; Q=0')
    print('[collision] INFO  minimum pattern =',pp[m].raw())
if __name__=='__main__':topology();edges();collision();print('\nALL SIMPLE K2P CHECKS PASSED')
