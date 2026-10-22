"""Exact generic coefficient checks for the three-occurrence mixed-sign proof."""
from itertools import product
from collections import Counter
import json
import sympy as S

def clean(p):return tuple(sorted((k,v) for k,v in p.items() if v))
def first_coeff(p,q,r):
    return clean_sum([
        ((q,p+r,0),-1),((q,p,r),1),((q,r,p),1),((q,0,p+r),-1)])
def clean_sum(items):
    c=Counter()
    for mon,coef in items:c[mon]+=coef
    return clean(c)
def second_coeff(p,q,r):
    return clean_sum([((p+q,r,0),1),((q+r,0,p),1),((q,r,p),-1)])

def run():
    bs=S.symbols('b0:9');B=S.Matrix(3,3,bs)
    pp=S.symbols('P0:3');qq=S.symbols('Q0:3');rr=S.symbols('R0:3')
    F=S.Poly(S.expand(S.trace(S.diag(*pp)*B*S.diag(*qq)*B*S.diag(*rr)*B.adjugate())),*bs)
    c1=F.coeff_monomial(B[0,1]*B[0,2]*B[1,0]*B[2,0])
    c2=F.coeff_monomial(B[0,0]*B[0,1]*B[1,2]*B[2,0])
    assert S.expand(c1+qq[0]*(pp[1]-pp[2])*(rr[1]-rr[2]))==0
    wanted=qq[0]*(pp[0]*rr[1]+pp[2]*rr[0]-pp[2]*rr[1])
    assert S.expand(c2-wanted)==0
    swapped=wanted.xreplace(dict(list(zip(pp,rr))+list(zip(rr,pp))))
    alternant=S.det(S.Matrix([[pp[i],rr[i],1] for i in range(3)]))
    assert S.expand(wanted-swapped-qq[0]*alternant)==0
    seen={};count=0
    nz=[-3,-2,-1,1,2,3]
    for p,q,r in product(nz,range(-3,4),nz):
        sig=(p+q+r,first_coeff(p,q,r),second_coeff(p,q,r))
        assert sig not in seen or seen[sig]==(p,q,r),(seen.get(sig),(p,q,r))
        seen[sig]=(p,q,r);count+=1
    A=S.diag(2,3,S.Rational(1,6));b=S.Matrix([[1,1,1],[1,2,3],[0,1,3]])
    gaps=(1,0,-1),(-1,0,1)
    def tr(g):
        p,q,r=g
        return S.trace(A**p*b*A**q*b*A**r*b.inv())
    vals=list(map(tr,gaps))
    assert A.det()==b.det()==1 and vals[0]!=vals[1]
    return {'status':'PASS','generic_B_monomials':len(F.terms()),'both_coefficient_formulas':True,
            'alternant_difference':True,'reconstruction_triples':count,
            'example':{'gaps':gaps,'A_diagonal':['2','3','1/6'],
                       'B':[[int(t) for t in row] for row in b.tolist()],'traces':list(map(str,vals))},
            'scope':'Exact checks for unbounded mixed-sign three-occurrence lemma; no full resolution'}

if __name__=='__main__':print(json.dumps(run(),indent=2))
