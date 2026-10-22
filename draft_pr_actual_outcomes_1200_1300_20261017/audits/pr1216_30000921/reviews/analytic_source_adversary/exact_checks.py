#!/usr/bin/env python3
"""Independent finite diagnostics only; never imports candidate/source code.

These finite calculations prove no hypercyclicity, density, or infinite limit.
All complex comparisons use rational squared norms; no floating point is used.
The product oracle convolves ordinary Taylor coefficients independently of the
candidate's derivative-normalized recursion. Shifted global checks additionally
expand (x-alpha)^j and differentiate in the global x basis.
"""
from fractions import Fraction as Q
from math import comb, factorial
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json

class G:
    __slots__ = ("r", "i")
    def __init__(self, r=0, i=0):
        if isinstance(r, G):
            self.r, self.i = r.r, r.i
        else:
            self.r, self.i = Q(r), Q(i)
    def __add__(self, other):
        t = G(other)
        return G(self.r+t.r, self.i+t.i)
    __radd__ = __add__
    def __neg__(self): return G(-self.r, -self.i)
    def __sub__(self, other): return self+-G(other)
    def __rsub__(self, other): return G(other)+-self
    def __mul__(self, other):
        t = G(other)
        return G(self.r*t.r-self.i*t.i, self.r*t.i+self.i*t.r)
    __rmul__ = __mul__
    def __truediv__(self, other):
        t = G(other)
        d = t.norm2()
        if not d: raise ZeroDivisionError()
        return self*G(t.r/d, -t.i/d)
    def __pow__(self, n):
        if n < 0: return (G(1)/self)**(-n)
        value = G(1)
        for _ in range(n): value = value*self
        return value
    def norm2(self): return self.r*self.r+self.i*self.i
    def __eq__(self, other):
        t = G(other)
        return self.r == t.r and self.i == t.i
    def pair(self): return [str(self.r), str(self.i)]

COUNTS = Counter()
BRANCHES = Counter()

def check(condition, label):
    if not condition: raise RuntimeError(label)
    COUNTS[label] += 1

def convolution(x, y):
    out = [G() for _ in range(len(x)+len(y)-1)]
    for j, a in enumerate(x):
        for k, b in enumerate(y): out[j+k] = out[j+k]+a*b
    return out

def ordinary_product_derivative(q, normalized_b, n):
    ordinary_b = [v/factorial(k) for k, v in enumerate(normalized_b)]
    coeffs = convolution(q, ordinary_b)
    return coeffs[n]*factorial(n) if n < len(coeffs) else G()

def expand_from_center(coefficients, alpha):
    out = [G() for _ in coefficients]
    for j, v in enumerate(coefficients):
        for k in range(j+1):
            out[k] = out[k]+v*comb(j, k)*((-alpha)**(j-k))
    return out

def global_derivative_at(coefficients, n, alpha):
    return sum((v*Q(factorial(j), factorial(j-n))*(alpha**(j-n)) for j, v in enumerate(coefficients) if j >= n), G())

def z_tests():
    for eta in [Q(1), Q(1, 1000), Q(7, 3)]:
        for k in range(16):
            t = eta/(k+1)
            boundary = [G(t), G(-t), G(0, t), G(0, -t), G(t*Q(3,5), t*Q(4,5))]
            values = boundary+[G(t*Q(r,4), t*Q(i,4)) for r in range(-5,6) for i in range(-5,6)]
            for a in values:
                b = a if a.norm2() >= t*t else G(t)
                c = b-a
                check(b.norm2() >= t*t, "z_floor")
                check(c.norm2() <= 4*t*t, "z_correction_bound")
                if a.norm2() == t*t:
                    check(c == 0, "z_threshold_equality_kept")
                check(((k+1)*b).norm2() >= eta*eta, "z_derivative_floor")
    b = [G(Q(1,k+1), Q((-1)**k,k+1)) for k in range(18)]
    for m in range(1,8):
        q = [G()]*m+[G(1)]
        for n in range(m+len(b)):
            direct = ordinary_product_derivative(q, b, n)
            if n < m:
                check(direct == 0, "monomial_low_orders")
            else:
                lower = Q(factorial(n), factorial(n-m)*(n-m+1))
                check(lower >= 1, "monomial_factorial_floor")
                check(direct.norm2() >= lower*lower, "monomial_product_floor")
                check(direct == b[n-m]*Q(factorial(n), factorial(n-m)), "monomial_product_identity")
    for n in [0,1,2,3,10,100]:
        for w in [G(0)] if n == 0 else [G(1), G(-1), G(0,1), G(Q(3,5),Q(4,5)),G(100,-30)]:
            check((w-G(Q(1,2))).norm2() >= Q(1,4), "open_disk_exclusion_including_zero")

def fixed_polynomial_tests():
    cases = []
    K = 12
    for m in range(1,6):
        for extension in [0,1,3]:
            for pattern in range(3):
                for eta in [Q(1),Q(1,10**6),Q(5,7)]:
                    d = m+extension
                    qm = [G(0,1),G(Q(1,100),Q(-2,300)),G(-3,2)][pattern]
                    q = [G() for _ in range(d+1)]
                    q[m] = qm
                    for j in range(m+1,d+1):
                        q[j] = G(0) if j == m+2 else G(Q((-1)**j*(j+3),2),Q(j-m,3))
                    a = [G() if pattern == 0 else (G(eta if k == 0 else 0) / qm if pattern == 1 else G(Q((7*k)%13-6,7),Q((5*k)%11-5,9))) for k in range(K)]
                    corrections = []
                    locked = []
                    for k in range(K):
                        n = k+m
                        A = qm*Q(factorial(n),factorial(k))
                        S = A*a[k]
                        for j in range(m+1,min(d,n)+1):
                            ell = n-j
                            S = S+q[j]*Q(factorial(n),factorial(ell))*(a[ell]+corrections[ell])
                        c = G() if S.norm2() >= eta*eta else (G(eta)-S)/A
                        BRANCHES["kept" if c == 0 else "corrected"] += 1
                        if S.norm2() == eta*eta:
                            check(c == 0,"fixed_threshold_equality_kept")
                        check(c.norm2()*A.norm2() <= 4*eta*eta,"fixed_correction_bound")
                        corrections.append(c)
                        b = [a[ell]+corrections[ell] for ell in range(k+1)]
                        direct = ordinary_product_derivative(q,b,n)
                        check(direct == S+A*c,"fixed_independent_convolution_identity")
                        check(direct.norm2() >= eta*eta,"fixed_barrier")
                        if c != 0: check(direct == eta,"fixed_exact_complex_target")
                        for old_k, old_value in enumerate(locked):
                            check(ordinary_product_derivative(q,b,old_k+m) == old_value,"fixed_old_values_unchanged")
                        locked.append(direct)
                        for low in range(m): check(ordinary_product_derivative(q,b,low) == 0,"fixed_all_low_orders")
                        for ell in range(k+1):
                            check(corrections[ell].norm2()*qm.norm2()*factorial(m)**2 <= 4*eta*eta,"uniform_eta_sup_bound")
                    alpha = [G(0),G(1,Q(1,2)),G(Q(-2,3),Q(1,3))][pattern]
                    global_p = expand_from_center(q,alpha)
                    for n in range(m):
                        check(global_derivative_at(global_p,n,alpha) == 0,"global_root_multiplicity_low_orders")
                    check(global_derivative_at(global_p,m,alpha) == qm*factorial(m),"global_root_first_nonzero_order")
                    global_F = expand_from_center([v/factorial(k) for k,v in enumerate(b)],alpha)
                    global_product = convolution(global_p,global_F)
                    for n in range(m+K):
                        check(global_derivative_at(global_product,n,alpha) == ordinary_product_derivative(q,b,n),"global_shifted_root_check")
                    cases.append({"m":m,"d":d,"eta":str(eta),"alpha":alpha.pair(),"qm":qm.pair(),"pattern":pattern,"steps":K})
    return cases

def factorial_tail_tests():
    for m in range(1,9):
        for n in range(30):
            r = Q(factorial(n),factorial(n+m))
            check(r <= Q(1,factorial(m)),"factorial_global_sup")
            check(r <= Q(1,n+1),"factorial_explicit_decay")
            for k in range(n,n+20):
                check(Q(factorial(k),factorial(k+m)) <= r,"factorial_tail_monotonicity")

def controls():
    z_fixture = [G(Q(1,2),Q(-1,3)),G(Q(2,3),Q(1,5))]
    q_fixture = [G(),G(1),G(1)]
    b_fixture = [G(1),G(1)]
    earlier_ratio = Q(factorial(0),factorial(1))
    later_ratio = Q(factorial(1),factorial(2))
    predicates = {
        "omit_z_replacement": G().norm2() >= Q(1,1),
        "drop_z_factor_n": ordinary_product_derivative([G(),G(1)],z_fixture,2) == z_fixture[1],
        "drop_fixed_polynomial_cross_term": ordinary_product_derivative(q_fixture,b_fixture,2) == q_fixture[1]*factorial(2)*b_fixture[1],
        "reverse_factorial_tail_inequality": later_ratio >= earlier_ratio,
        "use_open_disk_at_zero_ignoring_n0": G().norm2() >= Q(1,16),
    }
    for name,predicate in predicates.items():
        if predicate: raise RuntimeError("Mutation was not rejected: "+name)
    check(Q(factorial(7),factorial(7)) == 1,"constant_case_no_factorial_decay_control")
    return {name:"REJECTED" for name in predicates}

def main():
    z_tests()
    cases = fixed_polynomial_tests()
    factorial_tail_tests()
    mutation_results = controls()
    receipt = {"schema":"independent-exact-diagnostics-v1","status":"PASS","arithmetic":"exact Gaussian rationals using fractions.Fraction","candidate_or_source_program_imported":False,"scope":"Finite algebra corroboration only. Infinite analytic claims rest on the written proof audit.","counts":dict(sorted(COUNTS.items())),"fixed_polynomial_cases":len(cases),"recursive_branches":dict(BRANCHES),"mutation_controls":mutation_results,"program_sha256":sha256(Path(__file__).read_bytes()).hexdigest()}
    print(json.dumps(receipt,sort_keys=True,indent=2))

if __name__ == "__main__": main()
