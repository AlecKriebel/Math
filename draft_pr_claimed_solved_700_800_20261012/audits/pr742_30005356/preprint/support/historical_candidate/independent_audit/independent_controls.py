#!/usr/bin/env python3
"""Independent exact sanity controls; these are not an ACFH model or proof."""
import argparse
import itertools
import json
from pathlib import Path


def remainder(a, monic, p):
    a = [v % p for v in a]
    while a and a[-1] == 0:
        a.pop()
    while len(a) >= len(monic):
        k, c = len(a) - len(monic), a[-1]
        for j, v in enumerate(monic):
            a[k+j] = (a[k+j] - c*v) % p
        while a and a[-1] == 0:
            a.pop()
    return a


def irreducible(f, p):
    d = len(f)-1
    return not any(not remainder(f, list(c)+( [1]), p)
                   for k in range(1, d//2+1)
                   for c in itertools.product(range(p), repeat=k))


class Field:
    """Polynomial quotient in arbitrary small degree, packed as base-p digits."""
    def __init__(self, p, d):
        self.p, self.d, self.q = p, d, p**d
        self.f = next(list(c)+[1] for c in itertools.product(range(p), repeat=d)
                      if irreducible(list(c)+[1], p))
        self.digits = [tuple((x//p**i) % p for i in range(d)) for x in range(self.q)]
        self.add = [[self.pack([(a+b) % p for a,b in zip(self.digits[x],self.digits[y])])
                     for y in range(self.q)] for x in range(self.q)]
        self.mul = [[self.product(x,y) for y in range(self.q)] for x in range(self.q)]

    def pack(self, coefficients):
        return sum(c*self.p**i for i,c in enumerate(coefficients))

    def product(self, x, y):
        coefficients = [0]*(2*self.d-1)
        for i,a in enumerate(self.digits[x]):
            for j,b in enumerate(self.digits[y]):
                coefficients[i+j] += a*b
        return self.pack(remainder(coefficients,self.f,self.p))

    def power(self, x, exponent):
        value = 1
        while exponent:
            if exponent & 1:
                value = self.mul[value][x]
            x = self.mul[x][x]
            exponent //= 2
        return value


def field_control(p, d):
    f = Field(p,d)
    # Obtain inverse Frobenius from its graph, not from a presumed exponent.
    preimages = [[y for y in range(f.q) if f.power(y,p)==x] for x in range(f.q)]
    assert all(len(row)==1 for row in preimages)
    rho = [row[0] for row in preimages]
    assert all(rho[x]==f.power(x,p**(d-1)) for x in range(f.q))
    assert rho[0]==0 and rho[1]==1
    for x,y in itertools.product(range(f.q), repeat=2):
        assert rho[f.add[x][y]] == f.add[rho[x]][rho[y]]
        assert rho[f.mul[x][y]] == f.mul[rho[x]][rho[y]]
    for x in range(1,f.q):
        for k in range(f.q-1):
            assert rho[f.power(x,k)] == f.power(rho[x],k)
    # Mutation control: field-characteristic p does not zero the endomorphism [p].
    assert any(f.power(x,p)!=1 for x in range(1,f.q))
    # Deliberately show why finite tests cannot prove non-polynomiality.
    assert all(f.power(x,p**(d-1))==rho[x] for x in range(1,f.q))
    return {"p":p,"degree":d,"order":f.q,"modulus_ascending":f.f,
            "unique_root_graph":True,"additive_multiplicative_pair_checks":2*f.q*f.q,
            "commutation_checks":(f.q-1)**2,"power_p_is_not_ring_zero":True,
            "inverse_is_integer_power_on_this_finite_field":p**(d-1),
            "is_ACFH_model":False}


def formal_controls():
    tested, shift_tested = 0, 0
    primes = [2,3,5,7,11,13]
    for length in range(1,6):
        for a in itertools.product(range(-3,4),repeat=length):
            # In a free abelian group with shift S, Q(S)e_0 has coefficient vector Q.
            if any(a):
                unit = (1,)+(0,)*(length-1)
                result = tuple(sum(a[j]*(unit[i-j] if i>=j else 0)
                                   for j in range(length)) for i in range(length))
                assert result==a and any(result)
                shift_tested += 1
            for p in primes:
                b = (p*a[0]-1,)+tuple(p*v for v in a[1:])
                assert b[0]%p==p-1 and any(b)
                tested += 1
    return {"coefficient_range":[-3,3],"vector_lengths":[1,5],"primes":primes,
            "pP_minus_one_checks":tested,"nonzero_shift_vector_checks":shift_tested,
            "universal_proof_is_arithmetic_not_enumeration":True}


def compute():
    return {"status":"PASS","independent_implementation":True,
            "formal_proof_assistant_verification":False,
            "limitation":"Finite sanity controls only; the universal proof is in INDEPENDENT_PROOF.md.",
            "finite_fields":[field_control(p,d) for p,d in [(2,2),(2,3),(2,4),(3,2),(3,3),(5,2),(7,2)]],
            "integer_and_free_group_controls":formal_controls()}


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',type=Path)
    args=parser.parse_args()
    result=compute()
    if args.check:
        assert result==json.loads(args.check.read_text()), 'Control results differ'
        print('PASS: independently recomputed exact controls match')
    else:
        print(json.dumps(result,indent=2,sort_keys=True))
