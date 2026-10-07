# Conditional finite-field reference reduction

`finite_fields.py` implements the Berlekamp fixed-algebra/trace-coordinate
reduction and squarefree decomposition, including inverse coefficient Frobenius
for inseparable pth roots. It is conditional on a supplied deterministic
prime-field split-polynomial oracle. The bundled oracle enumerates all p elements
and is only a toy for small examples; it gives no polynomial-in-log(p) theorem.
The implementation does not certify the upstream prime-field result or claim
practical efficiency.

The field is `F_p[t]/h`, with promised prime p, monic h of positive degree m and
coefficients in increasing degree order. The constructor checks irreducibility
using gcd tests for every j <= floor(m/2) and the p^m Frobenius identity, without
factoring m or p-1. Elements are m-tuples in the power basis. Polynomials are tuples
of such elements in increasing x degree; the empty tuple denotes zero. Complete
factorization of zero is undefined and rejected. Nonzero constants produce an
empty factor list and their unit. Irreducible output factors are monic and include
all multiplicities. `factor(..., verify_output=True)` checks reconstruction and
tests each factor's irreducibility by an independent Frobenius criterion.

Run from this directory, using Python 3.10 or newer and no third-party packages:

```sh
python3 -m unittest -v test_finite_fields.py
python3 examples.py > examples-output.json
```

The independent test comparator exhaustively enumerates trial divisors. It checks
377 monic inputs across F2, F3, F5, F4, F8 and F9, together with specified repeated,
nonmonic, constant, zero, bad-oracle and inseparable examples. These exhaustive
tests have field-size dependence and are verification examples, not a fast
factorization algorithm.

Each squarefree run records n, fixed-algebra dimension s <= n, and the bounds
m*s on trace coordinates/prime-oracle calls and s on oracle-polynomial degree.
The Berlekamp matrix is n by n over K. First dependence calculations use n by
(d+1) augmented matrices with d <= s; the generic code allows d <= n and checks
the stronger bound after finding the dependence. Arithmetic counters count
extension-field operations; integer arithmetic inside the separate modulus
check, oracle and toy enumeration is not included in those counters.

The field constructor promises that p is prime: it is not a primality test.
The code uses unbounded Python integers, so it has no machine-word overflow
assumption. Every residue is reduced modulo p. The trace implementation raises
alpha*b to p powers in the quotient ring, then sums m terms; it does not apply a
coefficientwise trace to an arbitrary polynomial. All oracle roots are checked by
reconstructing the monic queried polynomial before they are used to split.
