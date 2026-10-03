"""Exact five-gap theorem checks; no random matrices or approximate arithmetic."""
from itertools import product
from collections import Counter,defaultdict
import json
import sympy as S

def canonical(p):return min(p[i:]+p[:i] for i in range(len(p)))
def deck(p):return tuple(sorted(Counter((p[i],p[(i+1)%len(p)]) for i in range(len(p))).items()))

def run():
    target=(2,1,0,0,0,1,1,0,0) # b11^2 b12 b23 b31
    paths=[]
    for states in product(range(3),repeat=5):
        edges=[0]*9
        for i in range(5):edges[3*states[i]+states[(i+1)%5]]+=1
        if tuple(edges)==target:paths.append(states)
    assert len(paths)==5 and {canonical(s) for s in paths}=={(0,0,0,1,2)}
    classes=defaultdict(set)
    for gaps in product(range(5),repeat=5):classes[deck(gaps)].add(canonical(gaps))
    collisions=[]
    for sig,cs in classes.items():
        if len(cs)<=1:continue
        assert len(cs)==2
        first=min(cs);counts=Counter(first)
        assert sorted(counts.values())==[1,1,3]
        r=next(t for t,n in counts.items() if n==3)
        s,t=sorted(t for t,n in counts.items() if n==1)
        assert cs=={canonical((r,r,s,r,t)),canonical((r,r,t,r,s))}
        collisions.append(sorted(cs))
    assert len(collisions)==30
    cc=S.symbols('c0:9');C=S.Matrix(3,3,cc)
    pp=S.symbols('P0:3');qq=S.symbols('Q0:3');P=S.diag(*pp);Q=S.diag(*qq)
    d3=S.trace(P*C**2*Q*C)-S.trace(Q*C**2*P*C)
    cycle=C[0,1]*C[1,2]*C[2,0]-C[0,2]*C[2,1]*C[1,0]
    alternant=S.det(S.Matrix([[pp[i],qq[i],1] for i in range(3)]))
    assert S.expand(d3+cycle*alternant)==0
    e2=(S.trace(C)**2-S.trace(C*C))/2
    d5=S.trace(P*C**2*Q*C**3)-S.trace(Q*C**2*P*C**3)
    assert S.expand(d5+e2*d3)==0
    A=S.diag(2,3,S.Rational(1,6));B=S.Matrix([[1,1,1],[1,2,3],[0,1,3]])
    u,v=(0,0,1,0,2),(0,0,2,0,1)
    def tr(g):
        M=S.eye(3)
        for p in g:M=M*A**p*B
        return S.trace(M)
    tu,tv=tr(u),tr(v)
    assert A.det()==B.det()==1 and tu!=tv and deck(u)==deck(v) and canonical(u)!=canonical(v)
    return {'status':'PASS','coefficient_paths':len(paths),'equality_pattern_assignments':5**5,
            'deck_collision_classes':len(collisions),'collision_template':'(r,r,s,r,t) versus(r,r,t,r,s)',
            'symbolic_trace_factorization':True,'symbolic_cayley_hamilton_reduction':True,
            'example':{'gaps':[u,v],'A_diagonal':['2','3','1/6'],'B':[[int(z) for z in row] for row in B.tolist()],
                       'traces':[str(tu),str(tv)],'difference':str(tu-tv)},
            'scope':'Finite exact checks supporting an unbounded five-occurrence subfamily theorem; full problem unresolved'}

if __name__=='__main__':print(json.dumps(run(),indent=2))
