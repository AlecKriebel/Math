#!/usr/bin/env python3
"""Independent exact checks. Uses Q[q]/(4q^2+2q-1), not author's Q(sqrt(5)) code."""
from fractions import Fraction as F
from itertools import permutations, product
import json

def check(x,label):
    if not x: raise ValueError(label)

# Sparse rational polynomials in (a,b,c). No author code is imported.
def add(p,r):
    out=dict(p)
    for m,v in r.items(): out[m]=out.get(m,F(0))+v
    return {m:v for m,v in out.items() if v}
def neg(p): return {m:-v for m,v in p.items()}
def mul(p,r):
    out={}
    for m,v in p.items():
        for n,w in r.items():
            k=tuple(x+y for x,y in zip(m,n));out[k]=out.get(k,F(0))+v*w
    return {m:v for m,v in out.items() if v}
def det_poly(M):
    if len(M)==1: return M[0][0]
    out={}
    for j in range(len(M)):
        minor=[row[:j]+row[j+1:] for row in M[1:]]
        term=mul(M[0][j],det_poly(minor))
        out=add(out,neg(term) if j%2 else term)
    return out

# Quotient-field arithmetic with q^2 = 1/4 - q/2.
class K:
    def __init__(self,a=0,b=0): self.a,self.b=F(a),F(b)
    @staticmethod
    def c(x): return x if isinstance(x,K) else K(x)
    def __add__(self,x):
        x=K.c(x);return K(self.a+x.a,self.b+x.b)
    __radd__=__add__
    def __neg__(self): return K(-self.a,-self.b)
    def __sub__(self,x): return self+-K.c(x)
    def __rsub__(self,x): return K.c(x)+-self
    def __mul__(self,x):
        x=K.c(x);return K(self.a*x.a+self.b*x.b/4,self.a*x.b+self.b*x.a-self.b*x.b/2)
    __rmul__=__mul__
    def __truediv__(self,x):
        x=K.c(x);n=x.a*x.a-x.a*x.b/2-x.b*x.b/4
        check(n!=0,'zero divisor');return self*K((x.a-x.b/2)/n,-x.b/n)
    def __eq__(self,x):
        x=K.c(x);return self.a==x.a and self.b==x.b
    def sign(self):
        if self==0:return 0
        lo,hi=F(0),F(1,3)
        for _ in range(512):
            l,u=sorted((self.a+self.b*lo,self.a+self.b*hi))
            if l>0:return 1
            if u<0:return -1
            mid=(lo+hi)/2
            if 4*mid*mid+2*mid<1:lo=mid
            else:hi=mid
        raise ValueError('sign not certified')
    def enc(self):return {'constant':str(self.a),'q_coefficient':str(self.b)}

def det_elimination(M):
    A=[[K.c(x) for x in r] for r in M];d=K(1)
    for j in range(len(A)):
        pivot=next((k for k in range(j,len(A)) if A[k][j]!=0),None)
        if pivot is None:return K()
        if pivot!=j:A[j],A[pivot]=A[pivot],A[j];d=-d
        d=d*A[j][j]
        for k in range(j+1,len(A)):
            ratio=A[k][j]/A[j][j]
            for l in range(j,len(A)):A[k][l]=A[k][l]-ratio*A[j][l]
    return d

def main():
    one={(0,0,0):F(1)};a={(1,0,0):F(1)};b={(0,1,0):F(1)};c={(0,0,1):F(1)}
    D=det_poly([[one,c,a,c],[c,one,c,b],[a,c,one,c],[c,b,c,one]])
    factor=mul(mul(add(one,neg(a)),add(one,neg(b))),add(mul(add(one,a),add(one,b)),neg(mul({(0,0,0):F(4)},mul(c,c)))))
    check(D==factor,'universal polynomial determinant identity')
    q=K(0,1);r=q/(1-q)
    check(4*q*q+2*q==1 and q.sign()>0 and (K(F(1,3))-q).sign()>0,'q branch')
    check(r*r==K(F(1,5)) and r.sign()>0,'dihedral invariant')
    tri=[[K(1) if i==j else -q for j in range(3)] for i in range(3)]
    check(det_elimination(tri)==(1+q)*(1+q)*(1-2*q),'trivalent determinant')
    check((1+q).sign()>0 and (1-2*q).sign()>0,'trivalent PSD and full rank')
    check(q*q-r*(1-q*q)==-q and q*q+r*(1-q*q)==K(F(1,2)),'both normal signs')
    check((1-q)*(1-q)-4*q*q==q*q,'positive uniform lower bound')
    cases=[]
    for i,(x,y) in enumerate(product([-q,K(F(1,2))],repeat=2)):
        M=[[1,-q,x,-q],[-q,1,-q,y],[x,-q,1,-q],[-q,y,-q,1]]
        d=det_elimination(M)
        expected=[K(F(1,8),F(1,8)),K(F(5,16),F(3,8)),K(F(5,16),F(3,8)),K(F(5,16),F(1,2))][i]
        check(d==expected and d.sign()>0,'positive forbidden determinant')
        # Every row permutation represents the same rank contradiction.
        for p in permutations(range(4)):
            check(det_elimination([[M[j][k] for k in p] for j in p])==d,'ray relabeling')
        cases.append({'a':x.enc(),'b':y.enc(),'determinant':d.enc()})
    stars=[]
    for t in [F(1,2),F(3,4)]:
        T=K(t);s=q/T;x=2*T*T-1;y=2*s*s-1
        check((T-q).sign()>0 and (1-T).sign()>0 and s.sign()>0 and (1-s).sign()>0,'star quadrant signs')
        check(T*s==q and (1+x)*(1+y)==4*q*q,'unit rays and neighbor dots')
        check(det_elimination([[1,-q,x,-q],[-q,1,-q,y],[x,-q,1,-q],[-q,y,-q,1]])==0,'realizable star Gram rank')
        stars.append({'t':str(t),'s':s.enc(),'a':x.enc(),'b':y.enc()})
    masks=[m for m in range(16) if all(not((m>>i)&1 and (m>>((i+1)%4))&1) for i in range(4))]
    check(len(masks)==7 and all(m.bit_count()<=2 for m in masks),'cycle-independent trivalent-edge subsets')
    incidence_count=0
    for n4,n5,n6 in product(range(5),repeat=3):
        n3=20+2*n4+5*n5+8*n6;V=n3+n4+n5+n6;Faces=12+2*n4+4*n5+6*n6;E=5*Faces//2
        check(V-E+Faces==2 and 3*n3+4*n4+5*n5+6*n6==2*E,'Euler formulas')
        check(Faces-4*n4-5*n5-6*n6==12-2*n4-n5,'all-trivalent-face lower bound')
        incidence_count+=1
    print(json.dumps({'passed':True,'problem_id':5500072,'basis':'Q[q]/(4q^2+2q-1), q positive','universal_determinant_identity':True,'forbidden_cases':cases,'relabeling_checks':96,'local_star_fixtures':stars,'admissible_trivalent_edge_masks':masks,'incidence_fixtures_only':incidence_count,'geometric_proof_machine_verified':False,'global_resolution':False},indent=2,sort_keys=True))
if __name__=='__main__':main()
