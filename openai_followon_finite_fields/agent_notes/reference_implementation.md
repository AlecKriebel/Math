# Conditional reference implementation checkpoint

Timestamp: 2026-10-07 04:30 UTC (2026-10-06 21:30 America/Los_Angeles).
Owned scope: `code/finite_fields.py`, `test_finite_fields.py`, `examples.py`,
`README.md`, `.gitignore`, `examples-output.json`, `verification-result.json`.
No upstream-clone writes, git operations, deposits, tracker writes or external
communications were performed by this implementation task.

Local checkpoint estimates: mathematical reduction/implementation validation
100%; reference/reproducibility package 100%. These estimates cover the local
conditional reduction scope after independent crosscomparison, not the project's
unconditional prime-field dependency or readiness of its full publication package.

## Exact implemented scope

Given promised prime p, an explicitly represented monic irreducible degree-m
modulus h, and a dense polynomial f over K=F_p[t]/h, the module implements the
Berlekamp/trace reduction conditional on a prime-field oracle that completely
splits the specific queried squarefree, split polynomials. The constructor checks
h by Frobenius tests without factoring m, p-1 or any integer. It does not test
whether p is prime; primality is an explicit input promise.

The embedded exhaustive oracle enumerates all p residues and is limited to
p<=4096 by default. Its cost is O(p*degree), not polynomial in log p. It is only a
test device. The implementation does not establish a uniformly deterministic
bit-polynomial base oracle, certify the upstream theorem, prove novelty, or claim
practical efficiency.

Zero-polynomial factorization is rejected as undefined. A nonzero constant has
its unit and an empty factor list. Nonconstant output consists of distinct monic
irreducibles with positive integer multiplicities and a leading unit. All output
is reconstructed and checked by a separate Frobenius irreducibility criterion by
default. Inverse coefficient Frobenius uses a -> a^(p^(m-1)), including m=1.

## Representation and bounded dimensions

Let b=bit_length(p), n=degree(f), and N=max(1,n). A coefficient is an m-tuple of
canonical residues with b bits each. The modulus has m+1 residues. All arrays are
little-endian. Integer modular products before reduction have at most 2b+O(1)
bits; stored q=p^m and inverse-Frobenius exponents have O(m*b) bits. Multiplicities
are at most n and have O(log(n+1)) bits. Python exact integers introduce no
machine-word overflow assumption.

For each monic squarefree factor of degree n_i:

* The q-Frobenius fixed-space matrix is n_i by n_i over K. Its kernel dimension
  s_i is checked and recorded, with 1<=s_i<=n_i.
* At most m*s_i trace coordinates and oracle calls occur. Early termination once
  s_i pieces exist may reduce this count. Across squarefree-decomposition pieces,
  sum n_i<=n, hence at most m*n total prime-oracle calls.
* Every oracle polynomial has degree d<=s_i. First dependence is recomputed for
  d=1,...,s_i using an n_i by (d+1) augmented matrix over K. This reference has
  O(n_i*s_i^3) field-operation overhead per coordinate, rather than optimized
  incremental dependence elimination. The generic loop allows d<=n_i and checks
  the stronger fixed-space bound after obtaining the relation.
* Trace(alpha*b) is formed in the quotient algebra as the sum of m iterated
  p-Frobenius powers. It is not a coefficientwise trace. Powers p have b bits and
  powers q have O(m*b) bits. The code checks c^p=c and checks the minimal-polynomial
  coefficients actually lie in the embedded F_p.
* All oracle roots are canonical, distinct, and checked by reconstructing the
  entire queried polynomial before they are used in gcd splits.

Field multiplication uses schoolbook convolution and reduction. Inversion uses
polynomial extended Euclid, with O(m^2) modular coefficient operations (quotient
degrees telescope and all intermediate Bezout degrees are O(m)); the generous
bit bound O(m^2*(b+1)^3) covers both operations. For the unoptimized reference,
Gaussian elimination, schoolbook polynomial operations, repeated first-dependence
solves, trace powers, gcd splits, squarefree recursion and final Frobenius tests
are bounded coarsely by O(m^2*N^5*(b+1)*log(N+1)) field operations plus the injected
oracle cost. This loose polynomial bound is not an optimized complexity claim.
Matrix/power-array coefficient storage is O(m*N^2*b) bits; the optional saved
query/statistics trace requires additional O(m*N^2*(b+log(N+1))) bits. Test enumeration is
excluded from these reduction bounds.

## Reproducible checks actually completed

Python 3.14.6, standard library only, Darwin arm64. Seven unittest families pass:

1. Every monic polynomial in F2 through degree 5, F3 through degree 3, F5 through
   degree 2, F4 through degree 3, F8 through degree 2 and F9 through degree 2:
   377 inputs in total. A separate exhaustive monic-trial-divisor comparator
   agrees with every factorization. Each output also passes reconstruction,
   trial-divisor irreducibility and the Frobenius irreducibility criterion.
2. Inseparable and repeated F4 factors with multiplicities 4 and 3, including a
   nontrivial coefficient pth root.
3. Nonmonic inputs, constants, zero rejection, extension degree one, and a
   nonzero root in a linear field modulus.
4. Valid/reducible/nonmonic moduli and non-pth-power rejection.
5. Exhaustive field inverse, Frobenius, commutativity, associativity and
   distributivity checks in the tested fields.
6. Missing/duplicate oracle roots are rejected; oversized toy-oracle input is
   rejected.
7. All eight distinct K-component values in F8 split, with eight degree-one
   factors, six recorded toy-oracle calls and fixed-algebra dimension eight.

Four saved example fixtures reconstruct and pass irreducibility checks:

| Fixture | Input degree | Factor degree/multiplicity pairs | Oracle calls |
|---|---:|---|---:|
| F3, m=1, repeated factors | 7 | (1,2), (2,1), (1,3) | 0 |
| F4, characteristic two coefficient roots | 7 | (1,4), (1,3) | 0 |
| F9, mixed coincident factors | 5 | (1,3), (1,1), (1,1) | 3 |
| F8, all component values | 8 | eight (1,1) | 6 |

The zero-call fixtures are not evidence of an oracle-free general algorithm:
their distinct multiplicities already separate their squarefree pieces. In the
F9 fixture, x^2+1 splits over F9 and overlaps one prescribed linear generator;
the multiplicity three is the correct reconstructed outcome.

A clean temporary directory containing only the three Python sources reproduced
all tests and the exact example JSON bytes. `verification-result.json` records
the exact source/README/example SHA-256 hashes, UTC time, software version and
test transcript. This is finite computational evidence, not a proof of the
unconditional core theorem or a full-package publication review.

Independent extension-reduction agent inspected the trace/minimal-polynomial
implementation and identified the original exponent-inversion overhead. That
was repaired by extended Euclid before the current saved hashes were generated.
The agent's distinct direct-p-fixed-space implementation uses its own arithmetic
and independent trial division. `code/extension_crosscheck.py` compared all 345
monic polynomials over F2 through degree 4, F3/F4 through degree 3 and F5/F8/F9
through degree 2, plus the F8 all-eight-values fixture: all 346 comparisons agree.
The independent agent reported no mathematical defect after inspecting the
trace-relation, kernel and gcd logic. Its receipt names current
`finite_fields.py` SHA-256
`4d8fc155249d053229033af123fda2fc2c57bd3c51b91ddb4484cb4755a47ec3`.
This code comparison is separate from the required full-publication-package
reviews and does not certify the upstream prime-field algorithm.
