# Reproducible verification of the counterexample

## Evidence hierarchy

PROOF.md is a self-contained analytic proof; no program is a mathematical dependency. It establishes the exact n=3 counterexample through joint-inclusion probabilities and supplies a second, independent n=4 counterexample by integrating only empty tails over two parameter triangles.

The private standard-library rational verifier uses a materially different route to recompute the full n=3 lattice integral directly from the definition. It ranges over every possible modular floor and every ordering of the points, clips the resulting polygons using exact fractions, and integrates the discrepancy polynomial on each polygon. No random sampling, floating-point approximation, assumed triple probability, or external package is used.

## Direct chamber calculation

For n=3 the algorithm produces six triangles in the (z,Delta) square. Two have area 1/4 and contribute 79/15552 each to the fourth-moment integral. Four have area 1/8 and contribute 61/155520 each. Thus their total area is 1 and their contributions sum to

2(79/15552) + 4(61/155520) = 19/1620.

The two area-1/4 triangles are the nonwrapping ascending and descending configurations. Every other configuration is represented by exactly one of the remaining four triangle interiors; floor and order boundaries have area zero.

For an affine function L on a triangle of area A, let a,b,c be its values at the vertices. The exact integration identity used is

integral_triangle L^m = [2A/((m+1)(m+2))] sum_{i+j+k=m} a^i b^j c^k.

It follows by expanding in barycentric coordinates and integrating monomials. On a chamber with sorted point coordinates b_1,...,b_n and endpoints b_0=0,b_(n+1)=1, integration over the box endpoint x first gives

sum_{k=0}^n [(b_(k+1)-k/n)^(p+1) - (b_k-k/n)^(p+1)]/(p+1).

For the required even p this is exactly the p-th power of the anchored discrepancy, integrated over x. These identities give an independent reproducible calculation without the analytic proof's count-distribution formula.

## Exact checks

- n=3,d=1,p=4 lattice moment: 19/1620
- n=3,d=1,p=4 iid moment: 4/405
- Strict difference: 1/540
- Ratio: 19/16
- n=4 lattice moment from chamber calculation: 139/17280
- n=4 sufficient analytic lower bound: 2/315
- n=4 iid moment: 11/1920
- n=4 lower-bound margin: 5/8064
- p=2, d=1, n=1,2,3,4: respectively 1/6, 1/12, 1/18, 1/24
- p=4, d=1, n=1,2: lattice and iid respectively 1/15, 1/48

The programs and detailed machine outputs are excluded from this public edition. The author calculations were checked in normal, -O and -OO Python; the independent audit recomputation and frozen-input verification were replayed in all three modes during publication preparation. Integrity and mathematical tests use explicit exceptions, so disabling assertions does not disable validation. Adverse controls reject deliberately corrupted inputs and artifacts. These historical verification results are supplementary metadata, not an omitted dependency of the standalone proof.

## Limitations

The complete proof subsequently passed a separately tasked independent internal AI-assisted mathematical audit; its full reasoning and acceptance are included as AUDIT.md and ACCEPTANCE.md. The original and distributed proof identities are distinguished in ACCEPTANCE.json. Only the known inline TeX delimiter defects are repaired in the distributed proof. The manuscript and audit are unrefereed. No external human peer review, proof-assistant certification, exhaustive literature review or historical novelty is claimed.
