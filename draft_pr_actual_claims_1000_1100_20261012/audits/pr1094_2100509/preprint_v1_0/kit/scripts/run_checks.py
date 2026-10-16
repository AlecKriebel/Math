"""New exact finite controls; proof is in paper.tex, not extrapolated here."""
import argparse
from fractions import Fraction as F
import itertools
import json
import random
import sys
sys.dont_write_bytecode = True
from safety import require, verify_payload, fresh_output, write_new, json_bytes

class P:
    def __init__(self, value=0):
        self.c = value.c if isinstance(value, P) else (F(value),)
    @classmethod
    def make(cls, values):
        values = list(map(F, values))
        while len(values) > 1 and not values[-1]:
            values.pop()
        p = cls(); p.c = tuple(values); return p
    def __add__(self, other):
        b = P(other).c; a = self.c
        return P.make([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
                       for i in range(max(len(a), len(b)))])
    __radd__ = __add__
    def __neg__(self): return P.make([-x for x in self.c])
    def __sub__(self, other): return self + -P(other)
    def __rsub__(self, other): return P(other) + -self
    def __mul__(self, other):
        b = P(other).c; out = [F(0)] * (len(self.c) + len(b) - 1)
        for i, x in enumerate(self.c):
            for j, y in enumerate(b): out[i+j] += x*y
        return P.make(out)
    __rmul__ = __mul__
    def derivative(self): return P.make([i*x for i,x in enumerate(self.c)][1:] or [0])
    def at(self, u): return sum(x * F(u)**i for i,x in enumerate(self.c))
    def __eq__(self, other): return self.c == P(other).c

def matrix(n): return [[P() for _ in range(n)] for _ in range(n)]
def product(a,b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), P())
             for j in range(len(b[0]))] for i in range(len(a))] if b else []
def constraint(l):
    m=len(l)-1
    a=[[l[i][j] for j in range(m)] for i in range(m)]
    c=[[a[i][j]-(l[-1][-1] if i==j else 0) for j in range(m)] for i in range(m)]
    return product(c,[[x.derivative() for x in row] for row in a])
def zeros(a): return all(x==0 for row in a for x in row)
def torsion(l):
    n=len(l); d=[[x.derivative() for x in row] for row in l]; out={}
    for i in range(n):
        for j in range(i+1,n):
            out[i,j]=[l[-1][i]*d[k][j]-l[-1][j]*d[k][i]
                      -sum((l[k][a]*(d[a][j] if i==n-1 else 0)
                           -l[k][a]*(d[a][i] if j==n-1 else 0)
                            for a in range(n)),P()) for k in range(n)]
    return out

def compositions(n):
    if not n: yield ()
    for k in range(1,n+1):
        for rest in compositions(n-k): yield (k,)+rest

def schedule(parts, chosen, eigenvalues):
    items=list(zip(parts,eigenvalues)); active=items.pop(chosen); items.append(active)
    n=sum(parts); m=n-1; l=matrix(n); offset=0
    for r,mu in items:
        for k in range(r):
            l[offset+k][offset+k]=P(mu)
            if k+1<r: l[offset+k][offset+k+1]=P(1)
        offset+=r
    initial=[[x.at(0) for x in row] for row in l]; previous=initial; stages=0; brackets=0
    u=P.make([0,1])
    def emit(changes):
        nonlocal l, previous, stages, brackets
        s=[[P(x.at(0)) for x in row] for row in l]
        for i,j,new in changes: s[i][j]=new
        require([[x.at(0) for x in row] for row in s]==previous,'stage discontinuity')
        require(zeros(constraint(s)), 'nonzero ordered polynomial constraint')
        if n<=4:
            require(all(all(x==0 for x in v) for v in torsion(s).values()),'direct bracket torsion')
            brackets+=1
        previous=[[x.at(1) for x in row] for row in s]
        l=[[P(x) for x in row] for row in previous]; stages+=1
    emit([(i,m,l[i][m]*(1-u)) for i in range(m)])
    angular=items[:-1]+([(active[0]-1,active[1])] if active[0]>1 else [])
    offset=0
    for r,mu in angular:
        emit([(m,m,l[m][m]*(1-u)+mu*u)])
        for j in range(r-1): emit([(offset+j,offset+j+1,1-u)])
        emit([(offset+j,offset+j,P(mu)*(1-u)) for j in range(r)]+[(m,m,P(mu)*(1-u))])
        offset+=r
    require(zeros(l),'nonzero final matrix')
    return stages,brackets

def run():
    families=stages=brackets=0
    for n in range(2,7):
        for parts in compositions(n):
            for chosen in range(len(parts)):
                for mode in range(3):
                    eigenvalues=[0 if mode==0 else F(2) if mode==1 else F((-1)**i*(i+1),i+2)
                                 for i in range(len(parts))]
                    s,b=schedule(parts,chosen,eigenvalues);families+=1;stages+=s;brackets+=b
    for parts,chosen in [((12,),0),((3,1,4,2),2),((1,1,1),1)]:
        s,b=schedule(parts,chosen,[F(i-1) for i in range(len(parts))]);families+=1;stages+=s;brackets+=b
    # Generic coefficient first jets, independent of schedule and formula.
    rng=random.Random(2100509); components=0
    for n in range(1,7):
        for sample in range(9):
            l=matrix(n);m=n-1
            for i in range(n):
                for j in range(n):
                    if i<m or j==m: l[i][j]=P.make([rng.randrange(-3,4),rng.randrange(-3,4)])
            observed=torsion(l); c=constraint(l)
            for (i,j),v in observed.items():
                want=([c[k][i] for k in range(m)]+[P()]) if j==m else [P()]*n
                require(v==want,'generic first-jet identity');components+=n
    u=P.make([0,1]); fault={}
    l=matrix(4);l[0][1]=P(1);l[1][2]=1-u
    fault['reversed_arrow_order']=not zeros(constraint(l))
    l=matrix(4);l[0][1]=u;l[1][2]=u
    fault['raw_nilpotent_cutoff']=not zeros(constraint(l))
    l=matrix(2);l[0][0]=1-u;l[1][1]=P(1)
    fault['unmatched_scalar_drift']=not zeros(constraint(l))
    l=matrix(2);l[0][0]=u;l[1][1]=2*u
    fault['distinct_eigenvalue_scalar_cutoff']=not zeros(constraint(l))
    l=matrix(4);l[0][1]=1-u;l[1][2]=P(1)
    a=[row[:3] for row in l[:3]]
    fault['reversed_product_rejects_valid_stage']=zeros(constraint(l)) and not zeros(product([[x.derivative() for x in r] for r in a],a))
    require(all(fault.values()),'undetected injected mathematical fault')
    return {'status':'PASS','arithmetic':'exact univariate rational polynomial coefficients',
            'schedule_families':families,'schedule_stages':stages,'direct_bracket_stages':brackets,
            'generic_jet_scalar_components':components,'detected_faults':fault,
            'n1':'Alternating two-form torsion vanishes; scalar plateau bump is the written proof.',
            'historical_program_replay':False,'universal_proof':'paper.tex',
            'optimized_mode_uses_explicit_guards':True}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out');args=parser.parse_args()
    out=fresh_output(args.out) if args.out else None
    verify_payload(); result=run()
    if out: write_new(out,json_bytes(result))
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__': main()
