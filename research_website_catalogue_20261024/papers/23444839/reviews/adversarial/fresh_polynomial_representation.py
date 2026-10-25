"""Direct cyclic-algebra conjugation control, not an import of LSV/package code.

Reconstructs b=1-z^-1 and b^-1 in dimension9 over F11(t), with E=F11^3.
Finite control of the polynomial representation interface, not building theory.
"""
from pathlib import Path
from datetime import datetime,timezone
import json
import sympy as S
from sympy.polys.matrices import DomainMatrix

ROOT=Path(__file__).resolve().parent
t=S.Symbol('t');F=S.GF(11).frac_field(t);zero=F.zero;one=F.one
# Pick the first theta^3+c theta+d with no F11 root; cubic irreducibility is then exact.
c,d=next((c,d) for c in range(11) for d in range(1,11) if all((x**3+c*x+d)%11 for x in range(11)))
ez=(zero,zero,zero);eo=(one,zero,zero)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def scale(a,k):return tuple(x*k for x in a)
def mul(a,b):
    out=[zero]*5
    for i in range(3):
        for j in range(3):out[i+j]+=a[i]*b[j]
    for k in (4,3):
        out[k-3]-=F(d)*out[k];out[k-2]-=F(c)*out[k]
    return tuple(out[:3])
def power(a,n):
    r=eo
    while n:
        if n&1:r=mul(r,a)
        a=mul(a,a);n//=2
    return r
ebasis=[tuple(one if i==j else zero for i in range(3)) for j in range(3)]
phibasis=[power(a,11) for a in ebasis]
def phi(a,n=1):
    for _ in range(n%3):
        r=ez
        for ai,im in zip(a,phibasis):r=add(r,scale(im,ai))
        a=r
    return a
assert all(phi(a,3)==a and power(a,11**3)==a for a in ebasis)
Z3=(one+F(t))/F(t)
def amul(a,b):
    out=[ez]*3
    for i in range(3):
        for j in range(3):
            term=mul(a[i],phi(b[j],i))
            if i+j>=3:term=scale(term,Z3)
            out[(i+j)%3]=add(out[(i+j)%3],term)
    return tuple(out)
unit=(eo,ez,ez)
b=(eo,ez,scale(eo,-F(t)/(one+F(t))))
bi=(scale(eo,one+F(t)),scale(eo,F(t)),scale(eo,F(t)))
assert amul(b,bi)==unit and amul(bi,b)==unit
basis=[tuple(ebasis[j] if i==k else ez for i in range(3)) for k in range(3) for j in range(3)]
flatten=lambda a:[v for coeff in a for v in coeff]
columns=[flatten(amul(amul(b,a),bi)) for a in basis]
invcolumns=[flatten(amul(amul(bi,a),b)) for a in basis]
M=[[columns[j][i] for j in range(9)] for i in range(9)]
Mi=[[invcolumns[j][i] for j in range(9)] for i in range(9)]
def degrees(mat):
    result=[]
    for row in mat:
        for f in row:
            assert f.denom.degree()==0
            if f:result.append(f.numer.degree())
    return result
assert max(degrees(M))<=1 and max(degrees(Mi))<=2
dm=DomainMatrix.from_list(M,F);dmi=DomainMatrix.from_list(Mi,F)
det=dm.det()
# Compare mathematical fractions by cross multiplication, and matrices by
# entries: SymPy can retain det=4/4 and distinct dense/sparse representations.
assert det.numer-det.denom==det.numer.ring.zero
product=dm.matmul(dmi).to_list()
assert all(product[i][j]==(one if i==j else zero) for i in range(9) for j in range(9))
# Constant conjugation by u in E does not change the degree bound for b_u.
out={'completed_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_DIRECT_CYCLIC_ALGEBRA_CONTROL','field_polynomial':f'theta^3+{c}theta+{d} over F11','no_base_field_root':True,'b_inverse_identity':True,'representation_dimension':9,'generator_max_entry_degree':max(degrees(M)),'inverse_max_entry_degree':max(degrees(Mi)),'determinant':str(dm.det()),'matrix_entries':[[str(f) for f in row] for row in M],'limits':'Checks the polynomial/inverse interface for b directly; constant E-conjugacy extends the same degree bound to b_u. No finite quotient enumeration or proof of vertex-regular building action.'}
(ROOT/'fresh-polynomial-representation.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='matrix_entries'}))
