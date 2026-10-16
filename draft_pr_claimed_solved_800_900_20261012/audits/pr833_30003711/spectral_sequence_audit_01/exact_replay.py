#!/usr/bin/env python3
"""Exact F3 certificates for the PR833 spectral-sequence dependency audit.
No source code from the candidate package is executed. No network or service writes.
"""
import itertools
import json
import argparse
from pathlib import Path

P = 3
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parent / 'EXACT_RESULTS.json',
                    help='Explicit result destination; default is beside this script, independent of caller directory.')
args = parser.parse_args()

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def rank(rows, width):
    basis = {}
    for row in rows:
        v = [x % P for x in row]
        for pivot in sorted(basis):
            a = v[pivot]
            if a:
                v = [(x-a*y) % P for x,y in zip(v,basis[pivot])]
        nz = next((i for i,x in enumerate(v) if x), None)
        if nz is not None:
            inv = pow(v[nz], -1, P)
            basis[nz] = [(inv*x) % P for x in v]
    return len(basis)

class GradedRing:
    def __init__(self, names, degrees, odd):
        self.names, self.degrees, self.odd = names, degrees, odd
        self.n = len(names)
        self.relations = []
    def mono(self, **powers):
        return tuple(powers.get(name,0) for name in self.names)
    def poly(self, *terms):
        out = {}
        for coefficient, powers in terms:
            m = self.mono(**powers)
            out[m] = (out.get(m,0)+coefficient) % P
        return {m:c for m,c in out.items() if c}
    def degree(self,m):
        return sum(a*b for a,b in zip(m,self.degrees))
    def monomials(self,n):
        return [m for m in itertools.product(*[range(min(n//d,1)+1) if o else range(n//d+1) for d,o in zip(self.degrees,self.odd)]) if self.degree(m)==n]
    def multiply_mono(self,a,b):
        if any(o and x+y>1 for x,y,o in zip(a,b,self.odd)):
            return None,0
        signs = sum(a[i]*b[j] for i in range(self.n) for j in range(i) if self.odd[i] and self.odd[j])
        return tuple(x+y for x,y in zip(a,b)), (-1)**signs
    def multiply(self,a,b):
        out = {}
        for ma,ca in a.items():
            for mb,cb in b.items():
                m,s = self.multiply_mono(ma,mb)
                if m is not None:
                    out[m] = (out.get(m,0)+s*ca*cb) % P
        return {m:c for m,c in out.items() if c}
    def plus(self,*polys):
        out = {}
        for poly in polys:
            for m,c in poly.items():
                out[m]=(out.get(m,0)+c)%P
        return {m:c for m,c in out.items() if c}
    def vector(self,poly,mons):
        return [poly.get(m,0) for m in mons]
    def ideal_rows(self,n,extra=()):
        mons=self.monomials(n)
        rows=[]
        for rel in self.relations+list(extra):
            degs={self.degree(m) for m in rel}
            require(len(degs)==1,'Relation must be homogeneous')
            d=next(iter(degs))
            for m in self.monomials(n-d) if n>=d else []:
                rows.append(self.vector(self.multiply(rel,{m:1}),mons))
        return mons,rows
    def quotient_dimension(self,n,extra=()):
        mons,rows=self.ideal_rows(n,extra)
        return len(mons)-rank(rows,len(mons))
    def zero(self,poly,extra=()):
        if not poly:return True
        n={self.degree(m) for m in poly}
        require(len(n)==1,'Query must be homogeneous')
        mons,rows=self.ideal_rows(next(iter(n)),extra)
        return rank(rows,len(mons))==rank(rows+[self.vector(poly,mons)],len(mons))

R=GradedRing(['y','yp','x','xp','c','z'],[1,1,2,2,4,6],[1,1,0,0,0,0])
f=R.poly
R.relations=[
 f((1,{'x':1,'yp':1}),(-1,{'xp':1,'y':1})),
 f((1,{'x':3,'yp':1}),(-1,{'xp':3,'y':1})),
 f((1,{'x':3,'xp':1}),(-1,{'xp':3,'x':1})),
 f((1,{'c':1,'y':1}),(1,{'x':2,'y':1})),
 f((1,{'c':1,'yp':1}),(1,{'xp':2,'yp':1})),
 f((1,{'c':1,'x':1}),(1,{'x':3})),
 f((1,{'c':1,'xp':1}),(1,{'xp':3})),
 f((1,{'c':2}),(-1,{'x':4}),(-1,{'xp':4}),(1,{'x':2,'xp':2})),
]
u=f((1,{'y':1,'yp':1})); c=f((1,{'c':1})); z=f((1,{'z':1})); C=f((1,{'y':1,'x':1,'xp':2}))
require(R.quotient_dimension(7)==6,'Leary R7 dimension mismatch')
require(R.quotient_dimension(7,[u,c,z])==1,'Chern quotient must have dimension one')
require(not R.zero(C,[u,c,z]),'Candidate class unexpectedly in correct Chern ideal')
require(R.zero(R.multiply(u,c)),'c1*c2 must vanish')
require(R.zero(R.multiply(u,u)),'c1 squared must vanish')
require(R.zero(R.multiply(u,f((1,{'x':1})))),'c1*x must vanish')
require(R.zero(R.multiply(u,f((1,{'xp':1})))),'c1*xprime must vanish')
# E5^{2,4}: coefficients of a1 a3 in degree 2; d4 is c2 multiplication.
mons6,rows6=R.ideal_rows(6)
images=[R.vector(R.multiply(c,f((1,m))),mons6) for m in ({'x':1},{'xp':1},{'y':1,'yp':1})]
image_rank=rank(rows6+images,len(mons6))-rank(rows6,len(mons6))
require(image_rank==2,'d4 on degree-two row-four coefficient space must have rank two')
# If the erroneous printed c2*yprime relation is read literally, C is already in I.
Rliteral=GradedRing(R.names,R.degrees,R.odd)
Rliteral.relations=R.relations[:]
Rliteral.relations[4]=f((1,{'c':1,'yp':1}),(1,{'x':2,'yp':1}))
require(Rliteral.zero(C,[u,c,z]),'Literal printed relation must put C into the Chern ideal')

# Concrete alternate-fibration identity in Leary Theorem 7.
S=GradedRing(['y','yp','x','xp','Y','Yp'],[1,1,2,2,2,2],[1,1,0,0,0,0])
g=S.poly
S.relations=[
 g((1,{'y':1,'yp':1})),
 g((1,{'x':1,'yp':1}),(-1,{'xp':1,'y':1})),
 g((1,{'y':1,'Y':1}),(-1,{'x':1,'yp':1})),
 g((1,{'yp':1,'Yp':1}),(-1,{'x':1,'yp':1})),
 g((1,{'y':1,'Yp':1}),(-1,{'yp':1,'Y':1})),
 g((1,{'Y':1,'Yp':1}),(-1,{'x':1,'xp':1})),
 g((1,{'Y':2}),(-1,{'x':1,'Yp':1})),
 g((1,{'Yp':2}),(-1,{'xp':1,'Y':1})),
]
L=g((1,{'yp':1,'Y':1}))
cs=g((-1,{'x':1,'Yp':1}),(-1,{'xp':1,'Y':1}),(-1,{'x':2}),(-1,{'xp':2}))
Cs=g((1,{'y':1,'x':1,'xp':2}))
require(S.zero(S.plus(S.multiply(cs,L),Cs)),'Theorem 7 must imply C2*L=-C')

# Exact actual matrix normal forms and central-coordinate coboundary.
E=list(itertools.product(range(3),repeat=3))
def mul(a,b):
    x,y,t=a; X,Y,T=b
    return ((x+X)%3,(y+Y)%3,(t+T+y*X)%3)
def matrix(e):
    a,b,t=e
    return tuple(((j+a)%3,(t+b*j)%3) for j in range(3))
def mmul(g,h):
    return tuple((g[h[j][0]][0],(h[j][1]+g[h[j][0]][1])%3) for j in range(3))
require(len({matrix(e) for e in E})==27,'Matrix forms must be distinct')
cochain_rows=[]
for a,b in itertools.product(E,repeat=2):
    ab=mul(a,b)
    require(matrix(ab)==mmul(matrix(a),matrix(b)),'Matrix product mismatch')
    dt=(b[2]-ab[2]+a[2])%3
    require(dt==(-a[1]*b[0])%3,'delta central coordinate is -yprime*y')
    row=[0]*27
    for e,v in [(b,1),(ab,-1),(a,1)]:row[E.index(e)]+=v
    cochain_rows.append(row)
for a,b,c0 in itertools.product(E,repeat=3):
    require(mul(mul(a,b),c0)==mul(a,mul(b,c0)),'Associativity mismatch')
r=rank(cochain_rows,27)
require(r==25,'H1 must have dimension two')
results={
 'field':3,'matrix_forms':27,'matrix_product_checks':729,'associativity_checks':19683,
 'central_coordinate_coboundary_checks':729,'one_cochain_differential_rank':r,'H1_dimension':27-r,
 'Leary_R7_dimension':6,'degree_seven_Chern_ideal_quotient_dimension':1,
 'candidate_C_nonzero_mod_correct_Chern_ideal':True,
 'literal_chen_wan_c2_yprime_typo_puts_C_in_Chern_ideal':True,
 'E5_2_4_dimension':3-image_rank,
 'Leary_Theorem7_identity_C2_times_yprimeY_equals_minus_C':True,
 'scope':'Exact algebra certificates; manifold, spectral-sequence and Poincare-duality deductions are in REPORT.md.'
}
args.output.write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
