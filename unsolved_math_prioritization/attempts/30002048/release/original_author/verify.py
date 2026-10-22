#!/usr/bin/env python3
"""Exact, standard-library-only certificates for the scoped results in PROOF.md.
Polynomials use coefficients in ascending order. No coefficient-height cutoff.
"""
from fractions import Fraction
from itertools import product
from math import gcd, isqrt
import json
import sys


def trim(a):
    a = list(a)
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def add(a, b):
    c = [0] * max(len(a), len(b))
    for i, v in enumerate(a): c[i] += v
    for i, v in enumerate(b): c[i] += v
    return trim(c)


def scale(a, v): return trim([v * t for t in a])


def mul(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, u in enumerate(a):
        for j, v in enumerate(b): c[i + j] += u * v
    return trim(c)


def rem(a, b):
    assert b[-1] == 1
    a = trim(a)
    while len(a) >= len(b) and a != [0]:
        k, v = len(a) - len(b), a[-1]
        for j, u in enumerate(b): a[k+j] -= v*u
        a = trim(a)
    return a


def monomial(j): return [0] * j + [1]


def determinant(a):
    """Bareiss elimination, including exact-division assertions."""
    a = [list(row) for row in a]
    n, sign, previous = len(a), 1, 1
    if not n: return 1
    for k in range(n-1):
        pivot = next((r for r in range(k,n) if a[r][k]), None)
        if pivot is None: return 0
        if pivot != k: a[k], a[pivot] = a[pivot], a[k]; sign *= -1
        v = a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                numerator = a[i][j]*v-a[i][k]*a[k][j]
                assert numerator % previous == 0
                a[i][j] = numerator // previous
            a[i][k] = 0
        previous = v
    return sign*a[-1][-1]


def norm_mod(f, h):
    """Res(h,f): determinant of multiplication by f in Q[x]/(h)."""
    n = len(h)-1
    columns = [rem([0]*j+f,h) for j in range(n)]
    return determinant([[c[i] if i<len(c) else 0 for c in columns] for i in range(n)])


def solve(a, b):
    a = [[Fraction(v) for v in row]+[Fraction(t)] for row,t in zip(a,b)]
    n=len(a)
    for j in range(n):
        k=next(k for k in range(j,n) if a[k][j])
        a[j],a[k]=a[k],a[j]
        v=a[j][j]; a[j]=[t/v for t in a[j]]
        for k in range(n):
            if k!=j:
                v=a[k][j];a[k]=[u-v*t for u,t in zip(a[k],a[j])]
    return [row[-1] for row in a]


PHI={1:[-1,1],2:[1,1],3:[1,1,1],4:[1,0,1],5:[1,1,1,1,1],
     6:[1,-1,1],7:[1]*7,8:[1,0,0,0,1],9:[1,0,0,1,0,0,1],10:[1,-1,1,-1,1]}
MS=[1,2,3,4,6]
P=[1]
for n in MS:P=mul(P,PHI[n])
assert P==[-1,0,-1,0,0,0,1,0,1]
OPTS=[[[1],[-1]],[[1],[-1]],[[1],[-1],[0,1],[0,-1],[1,1],[-1,-1]],
      [[1],[-1],[0,1],[0,-1]],[[1],[-1],[0,1],[0,-1],[-1,1],[1,-1]]]


def residues():
    rows=[]
    for m in MS:
        h=PHI[m]
        columns=[rem(monomial(j),h)+[0]*8 for j in range(8)]
        rows.extend([[c[i] for c in columns] for i in range(len(h)-1)])
    inverse_columns=[solve(rows,[int(i==j) for i in range(8)]) for j in range(8)]
    out=[];total=0
    for opts in product(*OPTS):
        total+=1; rhs=[]
        for m,v in zip(MS,opts):rhs+=v+[0]*(len(PHI[m])-1-len(v))
        r=[sum(inverse_columns[j][i]*rhs[j] for j in range(8)) for i in range(8)]
        if all(t.denominator==1 for t in r):
            r=trim([int(t) for t in r]);out.append(r)
            for m,v in zip(MS,opts):assert rem(r,PHI[m])==v
    assert total==576 and len(out)==24 and len({tuple(r) for r in out})==24
    expected={tuple(scale(rem(monomial(j),P),e)) for j in range(12) for e in [-1,1]}
    assert {tuple(r) for r in out}==expected
    return out


def evaluate(a,t):
    v=0
    for c in reversed(a):v=v*t+c
    return v


def integer_roots(a):
    """Exhaustive integer roots by the rational-root theorem, not a search box."""
    a=trim(a);out=set()
    assert a!=[0]
    while a[0]==0:
        out.add(0);a=a[1:]
    c=abs(a[0]);divisors=set()
    for i in range(1,isqrt(c)+1):
        if c%i==0:divisors.update([i,c//i,-i,-c//i])
    out.update(i for i in divisors if evaluate(a,i)==0)
    return sorted(out)


def mod_rem(a,b,p):
    a=trim([c%p for c in a]);b=trim([c%p for c in b])
    while a!=[0] and len(a)>=len(b):
        k=len(a)-len(b);v=a[-1]*pow(b[-1],-1,p)%p
        for j,u in enumerate(b):a[k+j]=(a[k+j]-v*u)%p
        a=trim(a)
    return a


def mod_gcd(a,b,p):
    while b!=[0]:a,b=b,mod_rem(a,b,p)
    return scale(a,pow(a[-1],-1,p)) if a!=[0] else a


def power_mod(a,n,f,p):
    out=[1]
    while n:
        if n&1:out=mod_rem(mul(out,a),f,p)
        a=mod_rem(mul(a,a),f,p);n//=2
    return out


def prime_divisors(n):
    out=[]
    for p in range(2,n+1):
        if n%p==0:
            out.append(p)
            while n%p==0:n//=p
    return out


def irreducible_mod(f,p):
    d=len(f)-1;x=[0,1]
    assert mod_rem(add(power_mod(x,p**d,f,p),scale(x,-1)),f,p)==[0]
    for q in prime_divisors(d):
        g=mod_rem(add(power_mod(x,p**(d//q),f,p),scale(x,-1)),f,p)
        assert len(mod_gcd(f,g,p))==1
    return True


def cs(f,k): return [norm_mod(f,PHI[n]) for n in range(1,k+1)]


def main():
    rs=residues()
    d7=[r for r in rs if len(r)==8 and r[-1]==1]
    assert len(d7)==3 and all(r[0]==0 for r in d7)
    d8_all=[add(P,r) for r in rs]
    d8_c5=[f for f in d8_all if norm_mod(f,PHI[5])==1]
    d8_c7=[f for f in d8_c5 if norm_mod(f,PHI[7])==1]
    d8_nonzero=[f for f in d8_c7 if f[0]!=0]
    assert (len(d8_c5),len(d8_c7),len(d8_nonzero))==(7,3,2)
    assert all(norm_mod(f,PHI[8])==9 for f in d8_nonzero)
    quartics=[];d9=[]
    for r in rs:
        base=add([0]+P,r)
        vals=[norm_mod(add(base,scale(P,a)),PHI[5])-1 for a in range(5)]
        q=solve([[a**j for j in range(5)] for a in range(5)],vals)
        assert all(v.denominator==1 for v in q)
        q=[int(v) for v in q];assert q[-1]==5
        # Extra exact evaluations check interpolation implementation, not the degree bound.
        for a in [-3,-1,5,11]:
            assert evaluate(q,a)==norm_mod(add(base,scale(P,a)),PHI[5])-1
        roots=integer_roots(q)
        quartics.append({'residue':r,'quartic':q,'integer_roots':roots})
        for a in roots:
            f=add(base,scale(P,a));d9.append({'residue':r,'a':a,'f':f,'C7':norm_mod(f,PHI[7])})
    d9_c7=[z for z in d9 if z['C7']==1]
    assert len(d9)==15 and len(d9_c7)==3 and all(z['f'][0]==0 for z in d9_c7)
    witnesses=[([-1,-1,-1,0,1,1,1,1],2,5),([-1,-1,-1,0,0,1,1,1,1],2,7),
               ([-1,-1,-1,-1,0,1,1,1,1,1],5,6)]
    witness_data=[]
    for f,p,e in witnesses:
        irreducible_mod(f,p);c=cs(f,e+1)
        assert all(abs(v)==1 for v in c[:e]) and abs(c[e])!=1
        witness_data.append({'f':f,'prime':p,'E0':e,'norms_Res_Phi_f':c})
    # Substitution route: compare exact cyclic norms and its gcd identity.
    f5=[-1,-1,0,1,1,1]
    substitutions=[]
    for k in range(1,9):
        fk=[0]*(5*k+1)
        for i,a in enumerate(f5):fk[i*k]=a
        first=None
        for n in range(1,5*k+2):
            g=gcd(n,k);v=norm_mod(f5,[-1]+[0]*(n//g-1)+[1])**g
            if n<=12:
                assert norm_mod(fk,[-1]+[0]*(n-1)+[1])==v
            if abs(v)!=1:first=n;break
        assert first is not None
        substitutions.append({'k':k,'degree':5*k,'prefix':first-1,'first_failed_n':first})
    output={'status':'unsolved','proved_scoped_values':{'e(7)':5,'e(8)':7,'e(9)':6},
       'crt_tuple_count':576,'integral_residue_count':24,'P':P,
       'd7_all_candidates_for_E_ge_6':d7,
       'd8_C5_survivors':[{'f':f,'norms_Res_Phi_f':cs(f,8)} for f in d8_c5],
       'd9_quartic_certificates':quartics,'d9_C5_survivors':d9,
       'witnesses':witness_data,'substitution_controls':substitutions}
    print(json.dumps(output,indent=2,sort_keys=True))


if __name__=='__main__': main()
