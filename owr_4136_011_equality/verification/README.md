# Exact finite verifier

Run from the research folder with Python 3. No third-party packages are needed:

```sh
python3 verification/verify.py
python3 -O verification/verify.py
```

Both commands must print JSON with `"status": "passed"` and identical results.
Failures raise an exception and return a nonzero exit status. All checks use
`fractions.Fraction`; none depends on floating-point tolerances or Python's
optional `assert` statements.

The script independently integrates the affine coordinate polynomials and
their squares over the standard simplex, using the iterated beta-integral
monomial formula. It compares those integrals with the paper's simplex identity
and verifies the two nonnegative terms in the deficit formula. The examples
include a nonregular inscribed triangle with nonzero centroid, equality and
strict interval cases, a strict square, and equality/strict rational simplices
in dimensions 1 through 6.

A separate exact planar convex-hull implementation checks visible-edge shell
updates, containment, and disjoint interiors. Polygon boundary-integral
formulas compute area, first moments, and second moments independently of the
simplex calculation. A six-vertex inscribed polygon tests the entire finite
extreme-vertex decomposition and its strictly positive deficit.
The square and hexagon also check the completed-square identity and the
positive retained-pair lower bound in the independent finite-approximation
proof.

An auxiliary update exercises a new point lying on an old edge's supporting
line. This tests the shell identity's coplanar boundary case only: three
distinct collinear planar points cannot all be extreme points of a single
convex body.

These are reproducible finite checks, not a computer proof of the countable
geometric decomposition or the universal equality theorem. They also do not
verify priority. The written proof and literature audit remain essential.
