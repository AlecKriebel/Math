#!/usr/bin/env python3
"""Independent standard-library exact checks; writes only final result beside this file.
Sparse polynomial Bareiss determinants, not imported package checker code, supply
norm and universal six-node conic identities. Finite controls supplement proofs.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product, permutations, combinations
import json, sys
HERE=Path(__file__).resolve().parent
PKG=HERE.parents[1]/'preprint_package_v01'
checks=[]
def check(name, condition):
    if not condition: raise AssertionError(name)
    checks.append(name)
def add(*polys):
    result={}
    for p in polys:
        for e,v in p.items(): result[e]=result.get(e,Q(0))+v
    return {e:v for e,v in result.items() if v}
def scale(p,c): return {e:v*c for e,v in p.items() if v*c}
def mul(p,q):
    result={}
    for e,v in p.items():
        for f,w in q.items():
            ef=tuple(a+b for a,b in zip(e,f));result[ef]=result.get(ef,Q(0))+v*w
    return {e:v for e,v in result.items() if v}
def unit(n): return {(0,)*n:Q(1)}
def var(n,k):
    e=[0]*n;e[k]=1;return {tuple(e):Q(1)}
def power(p,k,n):
    ans=unit(n)
    for _ in range(k):ans=mul(ans,p)
    return ans
def exact_div(p,q):
    if not q:raise ZeroDivisionError()
    answer={};remainder=p.copy();qe=max(q);qv=q[qe]
    while remainder:
        pe=max(remainder);pv=remainder[pe];e=tuple(a-b for a,b in zip(pe,qe))
        if min(e)<0:raise ArithmeticError('nonexact polynomial division')
        term={e:pv/qv};answer=add(answer,term);remainder=add(remainder,scale(mul(term,q),-1))
    return answer
def bareiss(matrix,nvars):
    m=[[v.copy() for v in row] for row in matrix];n=len(m);previous=unit(nvars);sign=1
    for k in range(n-1):
        if not m[k][k]:
            found=next((r for r in range(k+1,n) if m[r][k]),None)
            if found is None:return {}
            m[k],m[found]=m[found],m[k];sign=-sign
        pivot=m[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                m[i][j]=exact_div(add(mul(pivot,m[i][j]),scale(mul(m[i][k],m[k][j]),-1)),previous)
        for i in range(k+1,n):m[i][k]={}
        previous=pivot
    return scale(m[-1][-1],sign)
def numeric_det(matrix):
    m=[[Q(x) for x in r] for r in matrix];out=Q(1);n=len(m)
    for k in range(n):
        r=next((r for r in range(k,n) if m[r][k]),None)
        if r is None:return Q(0)
        if r!=k:m[k],m[r]=m[r],m[k];out=-out
        v=m[k][k];out*=v
        for i in range(k+1,n):
            c=m[i][k]/v
            for j in range(k+1,n):m[i][j]-=c*m[k][j]
    return out
# Read actual data rather than importing the checker, and pin the displayed f.
data=json.loads((PKG/'data.json').read_text())
def parsed(name):return {tuple(map(int,e.split(','))):Q(c) for e,c in data['polynomials'][name].items()}
f=parsed('f');g=parsed('g');p=parsed('p');q=parsed('q')
expected_f={(4,0,0):Q(1),(1,3,0):Q(1),(0,4,0):Q(1),(2,1,1):Q(-3),(1,2,1):Q(-4),(2,0,2):Q(2),(1,0,3):Q(1),(0,1,3):Q(1),(0,0,4):Q(1)}
check('released f exactly matches the displayed nine terms',f==expected_f)
check('p equals 1+f',p==add(unit(3),f))
check('g equals rational unit-ball generator',g==add(unit(3),scale(var(3,0),0),{(2,0,0):Q(-1),(0,2,0):Q(-1),(0,0,2):Q(-1)}))
x,y,z=[var(3,k) for k in range(3)];zero={}
# Multiplication matrix in basis 1,t,t^2,t^3, using t^4=t-1.
A=[[x,zero,scale(z,-1),scale(y,-1)],[y,x,z,add(y,scale(z,-1))],[z,y,x,z],[zero,z,y,x]]
D=bareiss(A,3)
check('independent polynomial Bareiss norm determinant equals f',D==f)
# h and derivative Sylvester matrix: determinant = discriminant since degree 4.
h=[1,0,0,-1,1];dh=[4,0,0,-1]
syl=[]
for i in range(3):syl.append([0]*i+h+[0]*(2-i))
for i in range(4):syl.append([0]*i+dh+[0]*(3-i))
disc=numeric_det(syl)
check('h discriminant is 229',disc==229)
check('2 and 3 are unramified in the factor-cycle calculation',disc%2!=0 and disc%3!=0)
def rem(a,b,prime):
    a=[v%prime for v in a]
    while a and a[-1]==0:a.pop()
    while len(a)>=len(b):
        k=len(a)-len(b);c=a[-1]*pow(b[-1],-1,prime)%prime
        for j,v in enumerate(b):a[k+j]=(a[k+j]-c*v)%prime
        while a and a[-1]==0:a.pop()
    return a
hlow=[1,-1,0,0,1]
check('h mod 2 has no factor of degree 1 or 2',all(rem(hlow,list(v)+[1],2) for d in (1,2) for v in product(range(2),repeat=d)))
cubic=[1,1,-1,1]
check('mod 3 cubic factor is irreducible',all(sum(c*a**i for i,c in enumerate(cubic))%3 for a in range(3)))
check('mod 3 factorization is (t+1)(t^3-t^2+t+1)',[v%3 for v in [cubic[0],cubic[0]+cubic[1],cubic[1]+cubic[2],cubic[2]+cubic[3],cubic[3]]]==[v%3 for v in hlow])
check('mod 3 factors are distinct',sum(c*(-1)**i for i,c in enumerate(cubic))%3!=0)
# Exhaustive finite group classification independently confirms the S4 inference.
perms=tuple(permutations(range(4)));identity=tuple(range(4))
def compose(a,b):return tuple(a[b[i]] for i in range(4))
def closure(generators):
    seen={identity};todo=[identity]
    while todo:
        a=todo.pop()
        for b in generators:
            c=compose(a,b)
            if c not in seen:seen.add(c);todo.append(c)
    return frozenset(seen)
subgroups={frozenset([identity])};todo=list(subgroups)
while todo:
    H=todo.pop()
    for v in perms:
        if v in H:continue
        J=closure(tuple(H)+(v,))
        if J not in subgroups:subgroups.add(J);todo.append(J)
def cycle_type(a):
    seen=set();lengths=[]
    for i in range(4):
        if i in seen:continue
        j=i;length=0
        while j not in seen:seen.add(j);length+=1;j=a[j]
        lengths.append(length)
    return tuple(sorted(lengths))
qualifying=[H for H in subgroups if any(cycle_type(a)==(4,) for a in H) and any(cycle_type(a)==(1,3) for a in H)]
check('S4 has 30 subgroups',len(subgroups)==30)
check('only S4 contains both a 4-cycle and a 3-cycle',len(qualifying)==1 and len(qualifying[0])==24)
# Universal six-intersection conic evaluation determinant for distinct roots.
a,b,c,d=[var(4,k) for k in range(4)];roots=[a,b,c,d];ones=unit(4)
rows=[]
for r,s in combinations(roots,2):
    u=mul(r,s);v=scale(add(r,s),-1);w=ones
    check('generic pair point lies on both parameter lines',add(u,mul(r,v),mul(mul(r,r),w))=={} and add(u,mul(s,v),mul(mul(s,s),w))=={})
    rows.append([mul(u,u),mul(u,v),mul(u,w),mul(v,v),mul(v,w),mul(w,w)])
incidence_det=bareiss(rows,4)
vand=ones
for r,s in combinations(roots,2):vand=mul(vand,add(s,scale(r,-1)))
vand2=mul(vand,vand)
incidence_sign=1 if incidence_det==vand2 else -1
check('universal six-node conic determinant equals signed Vandermonde squared',incidence_det==scale(vand2,incidence_sign))
# Independent explicit SOS identity by rational beta inversion and cubic reduction.
# beta^{-1}=beta^2-4 follows from beta^3-4beta-1=0.
def extended(poly):return {e+(0,):v for e,v in poly.items()}
B=var(4,3);inv=add(mul(B,B),scale(unit(4),-4));X,Y,Z=[var(4,k) for k in range(3)]
U=add(scale(mul(X,X),2),mul(B,mul(Y,Y)),scale(mul(Y,Z),-1),mul(add(scale(unit(4),2),inv),mul(Z,Z)))
V=add(scale(mul(X,Y),2),scale(mul(inv,mul(Y,Y)),-1),scale(mul(inv,mul(X,Z)),2),mul(B,mul(Y,Z)),scale(mul(Z,Z),-1))
sos_residual=add(mul(U,U),scale(mul(B,mul(V,V)),-1),scale(extended(f),-4))
def reduce_beta(poly):
    result=poly.copy()
    while any(e[3]>=3 for e in result):
        e=next(e for e in result if e[3]>=3);v=result.pop(e)
        low1=e[:3]+(e[3]-2,);low2=e[:3]+(e[3]-3,)
        result=add(result,{low1:4*v,low2:v})
    return result
check('independent SOS identity with beta^{-1}=beta^2-4',reduce_beta(sos_residual)=={})
check('negative beta root has endpoints of opposite sign',(-2)**3-4*(-2)-1<0<(-1)**3-4*(-1)-1)
# Universal symbolic degree-four jet with generic quadratic/cubic/quartic factors.
mons=[e for e in product(range(5),repeat=3) if 2<=sum(e)<=4]
n=3+2*len(mons)
factors=[];leads=[]
for index in range(2):
    factor={};lead={}
    for k,e in enumerate(mons):
        exponent=list(e)+( [0]*(n-3));exponent[3+index*len(mons)+k]=1;term={tuple(exponent):Q(1)}
        factor=add(factor,term)
        if sum(e)==2:lead=add(lead,term)
    factors.append(factor);leads.append(lead)
G={(0,)*n:Q(1)}
for i in range(3):e=[0]*n;e[i]=2;G=add(G,{tuple(e):Q(-1)})
full=add(mul(factors[0],factors[0]),mul(G,mul(factors[1],factors[1])))
jet={e:v for e,v in full.items() if sum(e[:3])==4}
check('generic symbolic fourth jet equals squares of quadratic jets',jet==add(mul(leads[0],leads[0]),mul(leads[1],leads[1])))
check('generator correction starts at degree six',all(sum(e[:3])>=6 for e in mul(add(G,scale(unit(n),-1)),mul(factors[1],factors[1]))))
# Exact actual moment data, matrix spectra, and alternative separator.
m={tuple(e['exponents']):Q(e['value']) for e in data['moments']['entries']}
allindices={e for e in product(range(5),repeat=3) if sum(e)<=4}
check('exact 35 moment positions and only stated two nonzero values',set(m)==allindices and len(m)==35 and {e:v for e,v in m.items() if v}=={(0,0,0):Q(1),(4,0,0):Q(-1)})
def L(poly):return sum(v*m[e] for e,v in poly.items())
check('L_m(p)=L_m(q)=0 and mass 1',L(p)==0 and L(q)==0 and m[(0,0,0)]==1)
check('rational alternative q-1=(x^2)^2',add(q,scale(unit(3),-1))==power(x,4,3))
basis=sorted(e for e in product(range(3),repeat=3) if sum(e)<=2)
M=[[m[tuple(a+b for a,b in zip(e,h))] for h in basis] for e in basis]
expected_M=[[Q(0) for _ in basis] for _ in basis]
expected_M[basis.index((0,0,0))][basis.index((0,0,0))]=1
expected_M[basis.index((2,0,0))][basis.index((2,0,0))]=-1
check('M2 is exactly diagonal with eigenvalues 1,-1,0x8',M==expected_M)
# Positive rescaling thresholds are analytic, not sampled: min(cp-1)=c-1 for c>=0.
result={'status':'PASS','python':sys.version.split()[0],'independent_exact_checks':len(checks),'checks':checks,'norm_terms':{','.join(map(str,e)):str(v) for e,v in sorted(D.items())},'h_discriminant':str(disc),'S4_subgroups':len(subgroups),'subgroups_containing_4_and_3_cycles':len(qualifying),'incidence_determinant_sign':incidence_sign,'actual_six_node_conic_determinant':str(incidence_sign*disc),'moment_matrix_eigenvalues':['1','-1']+['0']*8,'scope':'Exact algebra and finite group checks plus universal jet identity; analytic proof supplies all finite multiplier degrees and all rational rescalings.'}
(HERE/'independent_exact_result.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('checks','norm_terms')},indent=2,sort_keys=True))
