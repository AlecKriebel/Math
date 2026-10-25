"""Construct finite fields independently and test the distinguished-factor map."""
from itertools import product
from fractions import Fraction
import json


def divisors(n):
    return [d for d in range(1,n+1) if n%d==0]


def prime_factors(n):
    out=[]
    d=2
    while d*d <= n:
        if n%d==0:
            out.append(d)
            while n%d==0:
                n//=d
        d+=1
    if n>1:
        out.append(n)
    return out


class Field:
    def __init__(self,p,k):
        self.p,self.k,self.size=p,k,p**k
        self.powers=[p**j for j in range(k)]
        self.vectors=[]
        for x in range(self.size):
            self.vectors.append(tuple(x//p**j%p for j in range(k)))
        # Search a monic irreducible by the standard Frobenius/gcd criterion.
        for coeff in product(range(p),repeat=k):
            if not coeff[0]:
                continue
            self.modulus=coeff
            x=p
            if self.rawpow(x,p**k)!=x:
                continue
            okay=True
            for d in prime_factors(k):
                z=self.add(self.rawpow(x,p**(k//d)),self.neg(x))
                a=list(coeff)+( [1] )
                b=list(self.vectors[z])
                while len(b)>1 and b[-1]==0:
                    b.pop()
                while b!=[0]:
                    while len(a)>=len(b) and a!=[0]:
                        scale=a[-1]*pow(b[-1],-1,p)%p
                        off=len(a)-len(b)
                        for j in range(len(b)):
                            a[off+j]=(a[off+j]-scale*b[j])%p
                        while len(a)>1 and a[-1]==0:
                            a.pop()
                    a,b=b,a
                if len(a)!=1:
                    okay=False
                    break
            if okay:
                break
        else:
            raise AssertionError('no irreducible found')
        order=self.size-1
        primes=prime_factors(order)
        generator=next(g for g in range(2,self.size) if all(self.rawpow(g,order//d)!=1 for d in primes))
        self.generator=generator
        self.exps=[]
        self.logs={}
        x=1
        for i in range(order):
            assert x not in self.logs
            self.exps.append(x)
            self.logs[x]=i
            x=self.rawmul(x,generator)
        assert x==1 and len(self.logs)==order

    def encode(self,v):
        return sum((x%self.p)*weight for x,weight in zip(v,self.powers))

    def add(self,a,b):
        return self.encode(x+y for x,y in zip(self.vectors[a],self.vectors[b]))

    def neg(self,a):
        return self.encode(-x for x in self.vectors[a])

    def rawmul(self,a,b):
        p,k=self.p,self.k
        out=[0]*(2*k-1)
        for i,x in enumerate(self.vectors[a]):
            for j,y in enumerate(self.vectors[b]):
                out[i+j]=(out[i+j]+x*y)%p
        for d in range(2*k-2,k-1,-1):
            for j,c in enumerate(self.modulus):
                out[d-k+j]=(out[d-k+j]-out[d]*c)%p
        return self.encode(out[:k])

    def rawpow(self,a,n):
        b=1
        while n:
            if n%2:
                b=self.rawmul(a,b)
            a=self.rawmul(a,a)
            n//=2
        return b

    def mul(self,a,b):
        if not a or not b:
            return 0
        return self.exps[(self.logs[a]+self.logs[b])%(self.size-1)]

    def power(self,a,n):
        if not a:
            assert n>=0
            return 0 if n else 1
        return self.exps[(self.logs[a]*n)%(self.size-1)]

    def degree(self,a):
        return next(d for d in divisors(self.k) if self.power(a,self.p**d)==a)


def check(p,k):
    f=Field(p,k)
    order=f.size-1
    negative_one=f.neg(1)
    mapping={}
    orbits=set()
    full_lambdas=0
    for i in range(1,order,2):
        lam=f.exps[i]
        if f.degree(lam)!=k:
            continue
        full_lambdas+=1
        minus=f.add(lam,negative_one)
        plus=f.add(lam,1)
        assert minus and plus
        kap=f.neg(f.mul(f.power(minus,2),f.power(plus,-2)))
        assert kap and f.add(kap,1)
        assert f.degree(kap)==k
        mapping.setdefault(kap,[]).append(lam)
        assert f.power(kap,order//2)==1
        assert f.power(f.add(kap,1),order//2)==negative_one
        lhs=f.add(lam,f.power(lam,-1))
        rhs=f.mul(2,f.mul(f.add(1,f.neg(kap)),f.power(f.add(1,kap),-1)))
        assert lhs==rhs
        orbit=tuple(sorted(f.power(kap,p**j) for j in range(k)))
        assert len(set(orbit))==k
        orbits.add(orbit)
    assert all(len(v)==2 and f.mul(*v)==1 for v in mapping.values())
    assert full_lambdas >= Fraction(p**k,4)
    assert len(orbits) >= Fraction(p**k,8*k)
    d=2
    while k%(2*d)==0:
        d*=2
    def v2(n):
        return (n & -n).bit_length()-1
    target=v2(p**k-1)
    for j in range(1,129):
        if j%d:
            assert max(v2(p**j-1),v2(p**j+1)) < target
    return dict(p=p,k=k,modulus=list(f.modulus)+[1],generator=f.generator,
                maximal_two_part_full_degree_lambdas=full_lambdas,
                kappa_values=len(mapping),irreducible_factor_orbits=len(orbits),
                minimum_irreducible_count=str(Fraction(p**k,8*k)),
                dominated_factor_degrees_checked=128)


if __name__=='__main__':
    print(json.dumps(dict(status='PASS',universal_theorem_certified=False,
                         cases=[check(3,4),check(5,4),check(7,4),check(3,8)]),indent=2))
