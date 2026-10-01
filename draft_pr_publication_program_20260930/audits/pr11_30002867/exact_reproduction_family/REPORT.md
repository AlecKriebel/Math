# Exact reproduction and computational falsification report

**Verdict:** PASS for reproducibility and the tested mathematical scope. No
counterexample within the candidate's hypotheses was found. These are finite
checks; the arbitrary-dimension theorem and the global efficient-generation
step require the separate proof/source families.

Frozen head: `810559762f906624e0939191f5aface0ce7ce301`.

## 1. Exact claim and success conditions

For a positive-length quotient `A=C[x1,…,xd]/I`, `d≥1`, the input must be its
regular multiplication representation in a common basis. At each support point
`lambda`, the candidate claims

`rank(D1)=N−1`, `mu(I_local)=(d−1)N+1−rank(D2)`;

the complete-intersection target for the **full matrices** is
`rank(D2)=(d−1)(N−1)`. The computational audit seeks to falsify the local formula,
support identification, signs, common-basis invariance, and boundary assumptions.
Its independent expected counts must be certified by polynomial ideals and
resolutions rather than derived from the claimed matrix identity.

The global identity `mu_R(I)=max mu(I_local)` is not established by these
examples. This report does not promote a global theorem, novelty, or priority
claim from finite computation.

## 2. Frozen-suite reproduction

`reproduce_frozen.py` verifies all 14 manifest SHA-256 hashes and sizes, verifies
the 13 embedded `SHA256SUMS` entries, copies the frozen source to ignored scratch,
and executes both supplied checking scripts there. No frozen file is imported
into the new checker or written by either rerun.

| Suite | Examples | Result comparison | SHA-256 of reproduced JSON |
|---|---:|---|---|
| Author `check_koszul.py` | 13 | Parsed JSON and bytes identical | `29536eeefe6ffe22dc6955fae2407778b7b2fedb31675587a922d61d717df3ff` |
| Prior `independent_checks.py` | 20 | Parsed JSON and bytes identical | `208a840110f36ee5dee6b5ad9b73233c0fe9acc64cf10e9b95992931d257b196` |

Both processes return zero, with empty stderr. The complete 14-file manifest is
checked again after the runs and remains unchanged. The result is in
`frozen_reproduction_results.json`. Prior code is treated as untrusted evidence;
its reproducibility does not by itself validate its expected answers.

## 3. Materially independent exact construction

`independent_quotients.py` accepts polynomial ideals, constructs Groebner normal
forms, and derives a certified finite standard-monomial basis. Pure powers in
the leading ideal bound the enumeration, and the divisor test determines the
entire basis. The multiplication matrices are derived by reducing each
coordinate times each basis monomial. Every supplied ideal relation is also
evaluated in the resulting matrices and vanishes.

This differs from both frozen suites, which mostly construct prescribed
staircase multiplication tables directly. Exact rank uses SymPy's
`DomainMatrix`, not either supplied Gaussian-elimination routine. All Koszul
differentials are independently generated from the generic exterior-boundary
rule, and every consecutive product is checked to be zero. The tests compute
the complete Betti vector, compare it with separately certified resolutions,
verify that the unit's polynomial orbit spans dimension N, and verify the
first/second ranks after a nontrivial rational simultaneous conjugation.

Arithmetic fields used are `QQ`, `QQ_I`, `QQ<sqrt(2)>`,
`QQ<sqrt(2)+I>`, and `QQ<2^(1/4)>`. No symbolic expression field or floating-point
arithmetic is permitted in the rank-certification routine.

| Ideal-derived test | d | N | Independent local counts |
|---|---:|---:|---|
| `(x⁴+x²)`; nonreduced point and two nonreal reduced points | 1 | 4 | 1,1,1 |
| `(x²−y³,xy,y⁴)`; hidden redundant generator | 2 | 5 | 2 |
| `K=(x⁴,xy−x³,y²)`; nonlinear non-CI | 2 | 5 | 3 |
| `J=(x²,y²,xz,yz,z²−xy)`; Gorenstein non-CI | 3 | 5 | 5 |
| `(x²−y²,x²−z²,xy,xz,yz)`; second Gorenstein model | 3 | 5 | 5 |
| `(x³,(y−x²)²,z−xy)`; nonlinear CI | 3 | 6 | 3 |
| `K+(s²,t²)` | 4 | 20 | 5 |
| `J+(s²,t²)` | 5 | 20 | 7 |
| Square of the five-variable maximal ideal | 5 | 6 | 15 |
| `(b0⁷,b1−b0²,…,b5−b0⁶)` | 6 | 7 | 6 |
| `(x²−2,y²)`; algebraic nonreduced support | 2 | 4 | 2,2 |
| `(x²−2,y²+1)`; four algebraic reduced points | 2 | 4 | 2,2,2,2 |
| `(x²−sqrt(2),y²)`; algebraic coefficient and support | 2 | 4 | 2,2 |
| Product of length 5,5,6,1 quotients at four points | 3 | 17 | 4,5,3,3 |

All 14 cases pass. Length-20 checks cover nonreduced and nondiagonalizable
coordinates; diagonalizability is never assumed. In the four-point test, the
first coordinate separates support at 0, −2, 2, 7, giving a direct CRT
certificate of the regular representation. Individual spectra generate 36
Cartesian candidates; exact D1 ranks retain four and reject 32. At all support
points, the first rank is 16 and the full-matrix CI target is 32. The second
ranks are respectively 31,30,32,32, so the local counts are 4,5,3,3.

The certificate family in `ideal_certificate/` proves counts, lengths, and
resolutions independently. Some especially useful elementary certificates are:

- `y(x²−y³)−x(xy)=−y⁴`, so a superficially three-equation example is actually
  a two-equation CI of length five.
- The triangular coordinates `a=x,b=y−x²` identify K with `(a⁴,ab,b²)`.
  An explicit Hilbert–Burch matrix gives its minimal resolution ranks 1,3,2.
- J has five independent degree-two generators, all cubic monomials vanish,
  and basis `1,x,y,z,xy`. Its socle is the line spanned by xy; Gorenstein
  does not imply CI in three variables.
- Tensoring minimal resolutions with `(s²,t²)` gives local Betti vectors
  `(1,5,9,7,2)` for K and `(1,7,16,16,7,1)` for J.
- Lexicographic linear quotients of the generators of `m²` give
  `beta_i(S/m²)=i*binomial(d+1,i+1)` for i≥1; for d=5 the vector is
  `(1,15,40,45,24,5)`.

Detailed exact normal forms, bases, ranks, Betti vectors, conjugation checks,
and outside-support acyclicity checks are in `independent_quotient_results.json`.
The remaining principal, algebraic-support, curvilinear, CRT-product, and
fixed-basis perturbation expected data are proved in
`ADDITIONAL_IDEAL_CERTIFICATES.md`.
Both ideal-certificate scripts were independently rerun from another ignored
scratch copy; their mathematical outputs match exactly after excluding the
timestamp field. See `certificate_reproduction_results.json`. A separate
adversarial reread checks the report-to-data agreement and the expected ideal
certificates; see the review in `ideal_certificate/gorenstein_falsifier/`.

## 4. Scope falsifiers

### Regular representation is essential

Let X,Y be the transposes of regular multiplication matrices of
`C[x,y]/(x,y)²`. They commute and have the same annihilator `(x,y)²`, which has
three minimal quadratic generators and is not CI. With N=3, their D2 rank is 2,
which equals the proposed CI target 2. But D1 has rank 1 rather than N−1=2.
Thus the D2 criterion gives a false positive for an arbitrary commuting tuple.
This is outside the candidate's explicitly stated regular-representation
hypothesis, and demonstrates why that restriction must remain visible.

The new checker verifies the three annihilator relations and independence of
the matrices I,X,Y. Faithfulness is also immediate because polynomial
evaluation in commuting transposed matrices is the transpose of evaluation in
the original regular representation.

### A local size must not replace the full N

Take the product of the plane square-zero quotient of length three at the
origin and a reduced point at (2,3). Global N=4. At the non-CI component,
D1 rank is 3 and D2 rank is 2. The correct full target is 3; replacing N by
the component length gives target 2 and a false CI answer. The candidate's
full-matrix caution is necessary and is borne out by this exact fixture.

### Exact rank has no uniformly stable approximate-input decision

In the fixed basis `1,x,y`, impose

`x²=xy=0`, `y²=epsilon*x`.

Every epsilon gives a valid regular quotient of length three. If epsilon=0,
the ideal is `(x,y)²` and has three minimal generators. If epsilon≠0, eliminate
x using `x−y²/epsilon`; the ideal becomes `(x−y²/epsilon,y³)`, a CI. Hence the
CI indicator changes in a family of valid inputs arbitrarily close in matrix
entries. D1 rank remains 2; D2 rank changes from 1 at zero to 2 elsewhere.

At epsilon=10^-18 the exact matrix rank is 2. The floating-point D2 singular
values reported by NumPy are approximately `(sqrt(2),10^-18,0)`, and its
default numerical rank is 1. This is an illustration of the proved
discontinuity, not a new numerical certification scheme. The candidate's
approximate-input disclaimer is substantively necessary.

## 5. No-primary-decomposition and executable-field claims

The matrix-only evaluator takes solely the multiplication matrices. It extracts
each individual exact spectrum, forms the Cartesian product, and filters it
by first rank. It does not construct a polynomial generating set, Groebner
basis, or primary decomposition. Groebner bases are used only by the separate
test-data constructor to certify what the input matrices represent.

This provides finite evidence for an executable procedure over rational and
explicit algebraic number fields. It does not make arbitrary complex entries
computable. An effective field must provide exact arithmetic and equality,
and operations in a splitting extension sufficient to extract all roots of
the coordinate characteristic polynomials and perform the shifted rank tests.
Without such operations, the statement remains a finite mathematical
characterization. The Cartesian product may contain as many as N^d candidates;
this report establishes no efficiency or scalability bound beyond finiteness.

## 6. Reproduction and strongest result

The actual audit used the workspace's already-existing interpreter
`/Users/alec/Documents/Math/.venv/bin/python`; this family did not create or
modify that environment. From that workspace root, the commands used were:

```text
python3 draft_pr_publication_program_20260930/audits/pr11_30002867/exact_reproduction_family/reproduce_frozen.py
.venv/bin/python draft_pr_publication_program_20260930/audits/pr11_30002867/exact_reproduction_family/independent_quotients.py
```

The new exact suite uses installed SymPy 1.14.0 under Python 3.9.6; NumPy 2.0.2
is used only for the noncertifying numerical illustration. The frozen-suite
rerun uses the standard-library Python 3.9.6 environment. Both scripts locate
the audit relative to their own source path; they do not require that working
directory. In a fresh checkout, the frozen reproducer also expects the
repository's ignored `tmp/` scratch policy to remain available.

For portable reproduction, use Python 3.9–3.12 for the complete pinned stack
(the audit tested Python 3.9.6). Create an environment at a location of
your choice, install this folder's `requirements.txt`, then run the scripts
with that interpreter. For example, with `AUDIT_DIR` replaced by the absolute
path of this family folder:

```text
python3 -m venv /path/to/audit-venv
/path/to/audit-venv/bin/python -m pip install -r AUDIT_DIR/requirements.txt
/path/to/audit-venv/bin/python AUDIT_DIR/reproduce_frozen.py
/path/to/audit-venv/bin/python AUDIT_DIR/independent_quotients.py
/path/to/audit-venv/bin/python AUDIT_DIR/reproduce_certificates.py
```

The dependency file pins SymPy 1.14.0, mpmath 1.3.0, and NumPy 2.0.2. The
frozen reproducer and ideal certificate checker themselves need only the
standard library. The full new suite imports NumPy unconditionally for its
floating-point illustration; compatibility of that pinned version with later
Python releases is not promised. Result timestamps and interpreter descriptions can differ
on rerun; the frozen suite JSON bytes are compared exactly, and the newly
reported mathematical outputs should agree.

Strongest verified result: the frozen numerical artifacts are exactly
reproducible, and fourteen independently constructed quotient algebras across
dimensions 1–6 and lengths 4–20 obey the proposed support/rank identities,
including full Betti data consistent with separately proved resolutions.
The regular-representation, global-length, exact-field, and approximate-input
qualifications survive adversarial checking and are necessary.

Remaining gap: finite computations do not prove the theorem for arbitrary d,N
or verify the global efficient-generation theorem and its exact hypotheses.
Those obligations belong to the separate homological/global proof and primary
source audits. No Git mutation or external contact occurred.
