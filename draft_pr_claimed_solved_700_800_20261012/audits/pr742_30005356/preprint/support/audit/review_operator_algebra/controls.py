#!/usr/bin/env python3
"""Independent finite negative controls, not models/simulations of ACFH.
Uses finite fields solely to detect invalid generalizations and test identities.
Run: python3 controls.py
"""
from itertools import product
from pathlib import Path
from datetime import datetime, timezone
import json

class FiniteField:
    def __init__(self, p, modulus):
        self.p, self.modulus = p, tuple(modulus)
        self.r = len(modulus)-1
        assert self.modulus[-1] == 1
        self.q = p**self.r
        self.elements = list(product(range(p), repeat=self.r))
        self.zero = (0,)*self.r
        self.one = (1,)+(0,)*(self.r-1)
    def add(self, a, b):
        return tuple((x+y)%self.p for x,y in zip(a,b))
    def mul(self, a, b):
        out=[0]*(2*self.r-1)
        for i,x in enumerate(a):
            for j,y in enumerate(b): out[i+j]=(out[i+j]+x*y)%self.p
        for k in range(len(out)-1,self.r-1,-1):
            c=out[k]
            for j in range(self.r+1):
                out[k-self.r+j]=(out[k-self.r+j]-c*self.modulus[j])%self.p
        return tuple(out[:self.r])
    def pow(self, a, n):
        if n<0:
            assert a != self.zero
            return self.pow(self.pow(a,self.q-2),-n)
        out=self.one
        while n:
            if n&1: out=self.mul(out,a)
            a=self.mul(a,a)
            n//=2
        return out

def run():
    receipt={'description':'Finite negative controls; no assertion that these finite structures are ACFH.', 'generated_utc':datetime.now(timezone.utc).isoformat(), 'cases':[]}
    for p,modulus in [(2,[1,1,1]),(2,[1,1,0,1]),(3,[1,0,1]),(5,[2,0,1])]:
        f=FiniteField(p,modulus)
        nonzero=[x for x in f.elements if x != f.zero]
        # Validate field operations relevant to these tests and nonsingularity.
        for x in nonzero: assert f.pow(x,f.q-1)==f.one
        for x,y,z in product(f.elements,repeat=3):
            assert f.mul(f.mul(x,y),z)==f.mul(x,f.mul(y,z))
            assert f.mul(x,f.add(y,z))==f.add(f.mul(x,y),f.mul(x,z))
        rho=lambda x:f.pow(x,p**(f.r-1))
        frob=lambda x:f.pow(x,p)
        for x in f.elements:
            assert frob(rho(x))==x and rho(frob(x))==x
            for y in f.elements:
                assert rho(f.add(x,y))==f.add(rho(x),rho(y))
                assert rho(f.mul(x,y))==f.mul(rho(x),rho(y))
        # Integer exponents include zero and negative values; theta may have kernel.
        for x in nonzero:
            for m in range(f.q-1):
                theta=lambda u:f.pow(u,m)
                assert rho(theta(x))==theta(rho(x))
                for n in range(-7,8):
                    assert theta(f.pow(x,n))==f.pow(theta(x),n)
        # This is the contrary-to-genericity control: choose theta=rho.
        # p*theta - 1 is the constant-one map on K*.
        assert all(f.mul(f.pow(rho(x),p),f.pow(x,-1))==f.one for x in nonzero)
        power2=lambda x:f.pow(x,2)
        nonadditive=any(power2(f.add(x,y))!=f.add(power2(x),power2(y)) for x,y in product(f.elements,repeat=2))
        noninjective=any(x!=y and power2(x)==power2(y) for x,y in product(nonzero,repeat=2))
        receipt['cases'].append({'p':p,'degree':f.r,'q':f.q,'modulus_low_to_high':modulus,'inverse_frobenius_integer_exponent':p**(f.r-1),'inverse_frobenius_additive_multiplicative_bijective':True,'commutes_with_every_finite_group_power_endo_including_negative_scalar_checks':True,'theta_equals_rho_makes_pX_minus_1_vanish':True,'power2_nonadditive':nonadditive,'power2_noninjective_on_multiplicative_group':noninjective,'finite_scalar_ring_characteristic':f.q-1,'finite_field_characteristic':p})
    # Finite bounded symbolic check corroborates, but does not prove, all-integer obstruction.
    checked=0
    for p in [2,3,5,7,11]:
        for d in range(4):
            for coeffs in product(range(-3,4),repeat=d+1):
                q=[p*a for a in coeffs]
                q[0]-=1
                assert q[0]%p == p-1
                assert any(q)
                checked+=1
    receipt['bounded_polynomial_control']={'primes':[2,3,5,7,11],'max_degree':3,'coefficient_interval':[-3,3],'cases':checked,'pP_minus_1_always_nonzero':True,'status':'corroboration only; unrestricted proof is integer congruence'}
    Path('controls_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
if __name__=='__main__': run()
