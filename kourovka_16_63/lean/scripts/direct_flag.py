#!/usr/bin/env python3
"""Exact research checks for a direct flag-rigidity proof.

This is an independent standard-library reconstruction from the raw
transvectant formula. It is executable evidence, NOT a Lean soundness proof.
The generated DAG gives explicit two-generator expressions for all 31 basis
vectors. Fractions are exact; every denominator is coprime to 1009.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
from itertools import combinations
from math import comb, gcd
from pathlib import Path
import json, time, hashlib

P = 1009
D = 31
MODULES = [('U', 6, 3), ('V', 4, 10), ('W', 6, 15),
           ('T', 2, 22), ('R', 4, 25), ('Z', 0, 30)]
BASIS = ['h', 'e', 'f'] + [f'{s}{j}' for s,m,o in MODULES for j in range(m+1)]
INDEX = {s:i for i,s in enumerate(BASIS)}
V = dict[int, F]

def clean(a: V) -> V:
    return {i:F(c) for i,c in a.items() if c}

def add(a: V, b: V) -> V:
    out = dict(a)
    for i,c in b.items(): out[i] = out.get(i,F(0)) + c
    return clean(out)

def scale(c: F | int, a: V) -> V:
    return clean({i:F(c)*v for i,v in a.items()})

def unit(i: int | str) -> V:
    return {INDEX[i] if isinstance(i,str) else i:F(1)}

def falling(a: int, r: int) -> int:
    if r > a: return 0
    ans = 1
    for j in range(r): ans *= a-j
    return ans

def raw(m: int, n: int, r: int, i: int, j: int) -> tuple[int,int]:
    k = i+j-r
    if not 0 <= k <= m+n-2*r: return k,0
    return k, sum((-1)**q * comb(r,q) * falling(m-i,r-q) * falling(i,q)
                  * falling(n-j,q) * falling(j,r-q) for q in range(r+1))

def reconstruct() -> dict[tuple[int,int],V]:
    out: dict[tuple[int,int],V] = {}
    def insert(i:int,j:int,k:int,v:int):
        if not v: return
        assert i != j
        assert k not in out.get((i,j),{}), 'duplicate structure-constant insertion'
        out.setdefault((i,j),{})[k] = F(v)
        out.setdefault((j,i),{})[k] = F(-v)
    insert(0,1,1,2); insert(0,2,2,-2); insert(1,2,0,1)
    for s,m,o in MODULES:
        for j in range(m+1):
            insert(0,o+j,o+j,m-2*j)
            if j > 0: insert(1,o+j,o+j-1,j)
            if j < m: insert(2,o+j,o+j+1,m-j)
    mods = {s:(m,o) for s,m,o in MODULES}
    for a,b,c,r in [('U','U','W',3),('U','V','T',4),('U','W','T',5),
                     ('U','R','T',4),('V','V','T',3),('V','R','Z',4),('R','R','T',3)]:
        m,aa = mods[a]; n,bb = mods[b]; degree,cc = mods[c]
        assert degree == m+n-2*r
        for i in range(m+1):
            for j in range(n+1):
                if a==b and i>=j: continue
                k,v = raw(m,n,r,i,j)
                if v: insert(aa+i,bb+j,cc+k,v)
    return out

C = reconstruct()
def bracket(a: V,b: V) -> V:
    out: V = {}
    for i,x in a.items():
        for j,y in b.items():
            for k,z in C.get((i,j),{}).items():
                out[k] = out.get(k,F(0)) + x*y*z
    return clean(out)

X = unit('h')
Y = {}
for s in ['e','f','U1','V0','R2']: Y = add(Y,unit(s))
T = unit('U0')

def serial_vector(a:V):
    return [[i,c.numerator,c.denominator] for i,c in sorted(a.items())]

class DAG:
    def __init__(self):
        self.nodes: list[dict] = []
        self.values: list[V] = []
        self.labels: dict[str,int] = {}
    def emit(self, node:dict, value:V, label:str|None=None) -> int:
        k = len(self.nodes); self.nodes.append(node); self.values.append(value)
        if label is not None:
            assert label not in self.labels
            self.labels[label] = k
        return k
    def inp(self,i:int,label:str):
        return self.emit({'op':'input','index':i},[X,Y][i],label)
    def smul(self,c:F|int,a:int,label:str|None=None):
        c = F(c)
        assert gcd(c.denominator,P)==1
        return self.emit({'op':'scale','numerator':c.numerator,
                          'denominator':c.denominator,'arg':a},scale(c,self.values[a]),label)
    def plus(self,a:int,b:int,label:str|None=None):
        return self.emit({'op':'add','left':a,'right':b},add(self.values[a],self.values[b]),label)
    def lie(self,a:int,b:int,label:str|None=None):
        return self.emit({'op':'bracket','left':a,'right':b},bracket(self.values[a],self.values[b]),label)
    def linear(self,cs:list[tuple[int|F,int]],label:str):
        z = self.smul(0,0)
        for c,i in cs: z = self.plus(z,self.smul(c,i))
        self.labels[label] = z
        return z

def generation_certificate():
    d = DAG(); x=d.inp(0,'h'); y=d.inp(1,'y')
    h1=d.lie(x,y,'Hy'); h2=d.lie(x,h1,'H2y'); h3=d.lie(x,h2,'H3y')
    e=d.linear([(F(-1,16),h3),(F(1,8),h2),(F(1,2),h1)],'e')
    f=d.linear([(F(-1,48),h3),(F(1,8),h2),(F(-1,6),h1)],'f')
    z=d.linear([(F(1,48),h3),(F(-1,12),h1)],'z')
    r=d.linear([(F(1,16),h3),(F(-1,4),h2),(F(-1,4),h1),(1,y)],'r')
    d.lie(e,z,'U0')
    for j in range(1,7):
        a=d.lie(f,d.labels[f'U{j-1}']); d.smul(F(1,7-j),a,f'U{j}')
    d.plus(z,d.smul(-1,d.labels['U1']),'V0')
    for j in range(1,5):
        a=d.lie(f,d.labels[f'V{j-1}']); d.smul(F(1,5-j),a,f'V{j}')
    a=d.lie(e,d.lie(e,r)); d.smul(F(1,2),a,'R0')
    for j in range(1,5):
        a=d.lie(f,d.labels[f'R{j-1}']); d.smul(F(1,5-j),a,f'R{j}')
    a=d.lie(d.labels['U0'],d.labels['U3']); d.smul(F(1,720),a,'W0')
    for j in range(1,7):
        a=d.lie(f,d.labels[f'W{j-1}']); d.smul(F(1,7-j),a,f'W{j}')
    a=d.lie(d.labels['U0'],d.labels['V4']); d.smul(F(1,8640),a,'T0')
    a=d.lie(f,d.labels['T0']); d.smul(F(1,2),a,'T1')
    d.lie(f,d.labels['T1'],'T2')
    a=d.lie(d.labels['V0'],d.labels['R4']); d.smul(F(1,576),a,'Z0')
    for s in BASIS:
        assert d.values[d.labels[s]] == unit(s), (s,d.values[d.labels[s]])
    cert = {'version':1,'prime':P,'basis':BASIS,'input_vectors':[serial_vector(X),serial_vector(Y)],
            'nodes':d.nodes,'targets':[{'basis_index':INDEX[s],'node':d.labels[s]} for s in BASIS],
            'named_nodes':d.labels,'status':'external exact rational DAG, not a formal proof'}
    return d,cert

def verify_dag(cert:dict):
    assert cert['version'] == 1 and cert['prime'] == P and cert['basis'] == BASIS
    assert cert['input_vectors'] == [serial_vector(X),serial_vector(Y)]
    vals=[]
    for k,node in enumerate(cert['nodes']):
        op=node['op']
        if op=='input':
            i=node['index']; assert 0<=i<2; v=[X,Y][i]
        elif op=='scale':
            a=node['arg']; den=node['denominator']; assert 0<=a<k and den>0 and gcd(den,P)==1
            v=scale(F(node['numerator'],den),vals[a])
        else:
            a,b=node['left'],node['right']; assert 0<=a<k and 0<=b<k
            assert op in ('add','bracket')
            v=(add if op=='add' else bracket)(vals[a],vals[b])
        vals.append(v)
    assert sorted(t['basis_index'] for t in cert['targets'])==list(range(D))
    for target in cert['targets']:
        assert 0 <= target['node'] < len(vals)
        assert vals[target['node']]==unit(target['basis_index'])
    return True

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--check-only',action='store_true')
    args=parser.parse_args(); root=Path(__file__).resolve().parents[1]; start=time.perf_counter()
    assert all(P%d for d in range(2,32))
    triples=0
    for i,j,k in combinations(range(D),3):
        assert not add(add(bracket(unit(i),bracket(unit(j),unit(k))),
                           bracket(unit(j),bracket(unit(k),unit(i)))),
                       bracket(unit(k),bracket(unit(i),unit(j)))), (i,j,k)
        triples+=1
    exported=json.loads((root/'data/lie31_brackets.json').read_text())
    actual=[[i,j,k,int(v)] for (i,j),out in sorted(C.items()) if i<j for k,v in sorted(out.items())]
    assert actual==exported['terms']
    checked=[]
    def identity(name,left,right):
        assert left==right,(name,left,right)
        checked.append({'name':name,'common_value':serial_vector(left)})
    identity('[x,t]=6t',bracket(X,T),scale(6,T))
    identity('[y,t]=6U1',bracket(Y,T),scale(6,unit('U1')))
    identity('[x,y]=2e-2f+4U1+4V0',bracket(X,Y),
             add(add(scale(2,unit('e')),scale(-2,unit('f'))),add(scale(4,unit('U1')),scale(4,unit('V0')))))
    z=add(unit('U1'),unit('V0'))
    identity('[e,z]=t',bracket(unit('e'),z),T)
    identity('[R2,t]=0',bracket(unit('R2'),T),{})
    identity('[U2,U6]=2880W5',bracket(unit('U2'),unit('U6')),scale(2880,unit('W5')))
    identity('[U0,W5]=86400T0',bracket(T,unit('W5')),scale(86400,unit('T0')))
    identity('[U0,V4]=8640T0',bracket(T,unit('V4')),scale(8640,unit('T0')))
    H1=bracket(X,Y); H2=bracket(X,H1); H3=bracket(X,H2)
    identity('projector e',scale(F(1,16),add(add(scale(-1,H3),scale(2,H2)),scale(8,H1))),unit('e'))
    identity('projector f',scale(F(1,48),add(add(scale(-1,H3),scale(6,H2)),scale(-8,H1))),unit('f'))
    identity('projector z',scale(F(1,48),add(H3,scale(-4,H1))),z)
    identity('projector r',scale(F(1,16),add(add(H3,scale(-4,H2)),add(scale(-4,H1),scale(16,Y)))),unit('R2'))
    dag,cert=generation_certificate(); assert verify_dag(cert)
    if args.check_only:
        stored=json.loads((root/'data/generation_dag.json').read_text())
        assert verify_dag(stored)
        assert stored == cert, 'stored certificate differs from deterministic reconstruction'
    # Mutation is rejected at the mathematical target, not at parsing/import/setup.
    bad=json.loads(json.dumps(cert)); q=next(i for i,n in enumerate(bad['nodes'])
             if n['op']=='scale' and n['denominator']==720)
    bad['nodes'][q]['denominator']=721
    rejected=False
    try: verify_dag(bad)
    except AssertionError: rejected=True
    assert rejected
    log={'prime':P,'dimension':D,'integer_basis_jacobi_triples':triples,
         'original_export_matched':True,'flag_identity_count':len(checked),'flag_identities':checked,
         'generation_nodes':len(dag.nodes),'generation_targets':31,'generation_dag_accepted':True,
         'changed_W0_divisor_rejected':True,'elapsed_seconds':time.perf_counter()-start,
         'lean_checked':False,'classification_free_flag_proof':'see docs/DIRECT_FLAG_RIGIDITY.md',
         'status':'EXACT_RESEARCH_CHECKS_PASSED; not Lean certification'}
    if not args.check_only:
        (root/'data/generation_dag.json').write_text(json.dumps(cert,indent=2)+'\n')
        (root/'logs/direct_flag.json').write_text(json.dumps(log,indent=2)+'\n')
    print(json.dumps(log,indent=2))

if __name__=='__main__': main()
