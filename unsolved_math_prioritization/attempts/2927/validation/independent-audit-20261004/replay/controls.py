#!/usr/bin/env python3
"""Exact finite controls, not a decision procedure for KP-4.51. Python 3.10+."""
from fractions import Fraction
from itertools import permutations
from pathlib import Path
import json

# Laurent polynomials are exponent -> rational coefficient dictionaries.
def p(n): return {} if n == 0 else {0: Fraction(n)}
def add(*polys):
    out = {}
    for f in polys:
        for k, v in f.items(): out[k] = out.get(k, Fraction(0)) + v
    return {k:v for k,v in out.items() if v}
def neg(f): return {k:-v for k,v in f.items()}
def sub(f,g): return add(f,neg(g))
def mul(f,g):
    out = {}
    for i,a in f.items():
        for j,b in g.items(): out[i+j] = out.get(i+j,Fraction(0))+a*b
    return {k:v for k,v in out.items() if v}
def bar(f): return {-k:v for k,v in f.items()}
def eye(n): return [[p(int(i==j)) for j in range(n)] for i in range(n)]
def mm(a,b):
    return [[add(*(mul(a[i][k],b[k][j]) for k in range(len(b))))
             for j in range(len(b[0]))] for i in range(len(a))]
def star(a): return [[bar(a[j][i]) for j in range(len(a))] for i in range(len(a[0]))]
def block(a,b):
    return [row+[{} for _ in b] for row in a]+[[{} for _ in a]+row for row in b]
def det(a):
    n=len(a); out={}
    for q in permutations(range(n)):
        sign=(-1)**sum(q[i]>q[j] for i in range(n) for j in range(i+1,n))
        term=p(sign)
        for i in range(n): term=mul(term,a[i][q[i]])
        out=add(out,term)
    return out

def cyclic(a,n):
    r=len(a); s=len(a[0]); out=[[0]*(s*n) for _ in range(r*n)]
    for i in range(r):
        for j in range(s):
            for k,v in a[i][j].items():
                assert v.denominator==1
                for b in range(n): out[i*n+(b+k)%n][j*n+b]+=int(v)
    return out

def imul(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]
def it(a): return list(map(list,zip(*a)))
def ieye(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def norm(a,v): return sum(v[i]*a[i][j]*v[j] for i in range(len(v)) for j in range(len(v)))
def positive_ldl_det(a):
    a=[list(map(Fraction,row)) for row in a]; pivots=[]
    for k in range(len(a)):
        z=a[k][k]; assert z>0; pivots.append(z)
        for i in range(k+1,len(a)):
            for j in range(i,len(a)):
                a[i][j]-=a[i][k]*a[k][j]/z
                a[j][i]=a[i][j]
    result=Fraction(1)
    for z in pivots: result*=z
    return result

z=p(0); one=p(1); two=p(2); x={1:Fraction(1)}; xb=bar(x)
s=add(x,xb); s2=mul(s,s); aa=add(one,s,s2); bb=add(s,s2); cc=add(one,s)
L=[[aa,bb,cc,s],[bb,aa,s,cc],[cc,s,two,z],[s,cc,z,two]]
assert star(L)==L and det(L)==one
A=[[aa,bb],[bb,aa]]; B=[[cc,s],[s,cc]]
B2=mm(B,B)
assert [[sub(A[i][j],mul(p(Fraction(1,2)),B2[i][j])) for j in range(2)] for i in range(2)] == [[p(Fraction(i==j,2)) for j in range(2)] for i in range(2)]
P=[[z,z,one,p(-1),p(-1)],
   [z,z,z,one,p(-1)],
   [one,one,neg(add(one,xb)),one,add(s,one)],
   [z,one,neg(xb),z,add(s,one)],
   [one,two,sub(sub(x,one),xb),one,one]]
J=block(L,[[p(-1)]])
G=block(block([[one]],[[z,one],[one,z]]),eye(2))
assert det(P)==p(-1)
assert mm(mm(star(P),J),P)==G

covers=[]
for n in range(1,13):
    Q=cyclic(L,n); r=4*n
    assert Q==it(Q)
    determinant=positive_ldl_det(Q); assert determinant==1
    w=[0]*(2*n)+[1]*(2*n); c=w.copy(); c[0]-=2
    assert all((sum(Q[i][j]*c[j] for j in range(r))-Q[i][i])%2==0 for i in range(r))
    wn=norm(Q,w); cn=norm(Q,c)
    assert wn==4*n
    expected=12 if n==1 else 8 if n==2 else 4*n-8
    assert cn==expected
    covers.append({'n':n,'rank':r,'determinant':int(determinant),'positive_exact_ldl':True,
                   'characteristic':True,'w_norm':wn,'c_norm':cn,'short_characteristic_obstruction':cn<r})

# Extended controls: polynomial shear V and its explicit polynomial inverse.
f=add({2:Fraction(1)},neg(x),p(-1)); g=add(x,xb); h=add({-2:Fraction(1)},one)
V=[[one,f,g],[z,one,h],[z,z,one]]
Vi=[[one,neg(f),sub(mul(f,h),g)],[z,one,neg(h)],[z,z,one]]
assert mm(V,Vi)==eye(3) and mm(Vi,V)==eye(3)
E=mm(star(V),V)
extended=[]
for n in (3,5,7,11):
    Q=cyclic(E,n); F=cyclic(V,n); R=cyclic(Vi,n); N=3*n
    assert Q==imul(it(F),F)
    assert imul(F,R)==ieye(N)
    assert imul(imul(it(R),Q),R)==ieye(N)
    T=cyclic([[x if i==j else z for j in range(3)] for i in range(3)],n)
    assert sum(T[i][i] for i in range(N))==0
    assert imul(imul(it(T),Q),T)==Q
    assert imul(F,imul(T,R))==T
    assert positive_ldl_det(Q)==1
    extended.append({'prime':n,'rank':N,'basis_isometry':True,'deck_isometry':True,
                     'deck_trace':0,'deck_orbits':3,'orbit_length':n})

result={'status':'PASS','arithmetic':'exact integers and fractions, Python standard library',
        'Laurent_stabilization_certificate':{'det_P':-1,'P_star_J_P':'[1] + H + I_2','all_coefficients_checked':True},
        'schur_identity_checked':True,'HT_cyclic_covers':covers,'generated_extended_controls':extended,
        'limits':['No finite tests imply the universal large-prime hypothesis.',
                  'No proof of arbitrary indefinite extension or topological splitting descent.',
                  'No smooth counterexample constructed; no novelty certification.']}
output=Path(__file__).with_name('controls.json')
output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','HT_cover_degrees':list(range(1,13)),
                  'extended_prime_degrees':[3,5,7,11],'output':output.name}))
