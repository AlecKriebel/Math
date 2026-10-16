# Independent acceptance audit: K3 Problem 1.22

Audit date: 8 October 2026 (UTC).

## Verdict

**Accept the frozen package as a source-grounded, incomplete mathematical
research report: five distinct approaches completed; the general problem remains
unresolved.** No mathematical correction is required by this audit. This verdict
does not certify a proof, a counterexample, or completeness of the literature.

The reviewed report is identified by SHA-256
`deb6777556d7fed299d31b2759a5f21cd0a8135d115e5cd542f9d35af775ef94`.
Its checker is identified by SHA-256
`4c9f9a9bc5bae8d2d5ff703ffd003efb6f3085e0042b399da671008c1d428df9`.
`FROZEN_INPUTS.json` pins all eight author-package files and the source-free
archive. The author files were not changed during this audit. No correction patch
was generated.

## Problem identity and source scope

The inspected K3 author PDF, printed page 30, Problem 1.22, asks for the
non-L-space conclusion for the double branched cover of a hyperbolic L-space
knot. It is the precise question addressed by the report. K3 also records the
higher-order results separately. The report does not substitute the older Kirby
list's identically numbered problem. The source is
[K3: A New Problem List in Low-Dimensional Topology](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf).

The two source corrections are justified:

- In [Boyer–Gordon–Hu, Recalibrating R-order trees and
  Homeo+(S1)-representations of link groups](https://arxiv.org/abs/2306.10357v3),
  Theorem 7.2 distinguishes left-orderability for cover orders at least two from
  the non-L-space result for orders at least three. Corollary 7.3 is the
  orderability statement. The discussion on printed pages 39–40 explicitly
  retains the double-cover question. K3's bibliography assigns its BGH25 key to
  the different Seifert-links paper. The latter's Theorems 1.1 and 1.3 require
  the Seifert-exterior hypothesis; that hypothesis is not available for a
  hyperbolic knot. The report correctly refuses both a citation substitution and
  the unproved general implication from orderability to non-L-space status.
- [Baker–Kegel](https://arxiv.org/abs/2203.12013v3), Proposition 2.1 and
  Theorem 4.4, supply the hyperbolic L-space family and its displayed Alexander
  polynomial. Remark 4.6 supplies the signature formula and states the failure
  of definiteness. The v3 metadata was independently checked on arXiv: the
  revision is dated 19 August 2026 and identifies K3 Problem 1.21(c)(iii), rather
  than 1.22, as negatively answered. The report makes this distinction correctly.

All eleven source PDF hashes and byte counts, and all eleven corresponding
text-extraction hashes and byte counts, match the source manifest. Matching
source bytes establishes which copies were inspected; it does not independently
prove their theorems. No source document or copied source body is included in
this audit package.

## Mathematical review

### 1. Integral monodromy and cyclotomic algebra

The fibered hypothesis makes the integral Seifert matrix unimodular. With
`A=V^{-1}V^T`, direct multiplication gives both `A^T V A=V` and
`A^T(V+V^T)A=V+V^T`. A sign change of the definite symmetric form does not
change `A`. A positive definite form bounds every column of each integral
isometry; the resulting finite set of matrices contains all powers of `A`.
Coinciding powers imply finite order because `A` is invertible. The proof is
complete and does not make the invalid converse inference from characteristic
polynomial to mapping class.

For the formal companion example, independent polynomial division verifies that
`Phi_6^2 Phi_30` divides `(t^30-1)^2` but not `t^30-1`. The companion minimal
polynomial is the specified degree-twelve polynomial, so the nonzero square-zero
part of `C^30-I` and infinite order follow. No knot realization is asserted.

For the Baker–Kegel family, the two numerator factors have simple, disjoint root
sets: the exponents are odd and even, so a common root would give incompatible
values for its product-exponent power. The denominator removes the distinct
cyclotomic factors `Phi_2` and `Phi_4`. The resulting characteristic polynomial
is squarefree and divides `t^L-1`, with `L=lcm(2a,2b)`. Cayley–Hamilton therefore
applies to the actual integral homological monodromy, not merely to an invented
companion matrix. Degree and evaluation give genus `4n+2` and determinant
`4n+5`. Applying, rather than independently recomputing, the published signature
formula gives defect `4n>0`. For `n=1`, these values are genus 6, determinant 9,
and homological order dividing 36.

An independent factorization through distinct cyclotomic factors was checked for
32 family members, extending the author's eight examples. This also verifies
that the least exponent annihilating the characteristic polynomial is the
displayed `L` in those examples. The report only needs its weaker divisibility
claim. Its residual gap is correctly retained: definiteness plus the L-space
knot hypothesis is stronger than finite homological order.

The conditional definiteness input matches
[Boileau–Boyer–Gordon, Theorem 1.1 and Corollary 1.2](https://arxiv.org/abs/1710.07658v2).
The same-Seifert-form warning matches the introduction and Theorem 1 of
[Misev–Spano](https://arxiv.org/abs/1906.11760v1); those examples do not have
L-space surgeries.

### 2. Boundary rotation and taut foliations

The cover and slope conventions match
[Boyer–Hu, Theorem 1.2](https://arxiv.org/abs/1711.04578v3): the meridian upstairs
maps to twice the meridian downstairs, the longitude maps to the longitude,
and meridional filling gives the branched cover. The sufficient inequality is
`|2c-q|>=1`. Strong quasipositivity and the pseudo-Anosov setting supply positive
`c` after the positive mirror choice; right-veering alone does not supply a
uniform lower bound of one half.

For `0<c<1/2`, solving the strict reverse inequality over integers gives exactly
`q=0,1`. The target `q=0` is covered at `c=1/2` by equality. The report does not
infer a foliation at an omitted slope from foliations at other slopes. The
orientation-obstruction argument is also valid: a time-direction cyclic cover
restricts to the identity on each fiber, so a nonzero fiberwise orientation
class persists. The missing coorientation, filling extension, and tautness
arguments are stated rather than presumed.

### 3. Standard positive Hopf-tree fibers

The ADE proof is complete for the specified tree forms. A degree-four vertex
gives the stated null principal submatrix. Two branching vertices, their joining
path, and two extra neighbors at either endpoint give the second null principal
submatrix. These obstructions leave paths and single trivalent vertices. The
path determinant recurrence and central Schur complement classify the latter
as `(1,1,c)`, `(1,2,2)`, `(1,2,3)`, and `(1,2,4)`. The strict inequality excludes
the affine boundary cases; finite computer checks are not substituted for this
universal proof.

Passing back to a knot requires the actual standard arborescent Hopf-plumbing
hypothesis. Under it, the boundary identifications agree with Section 9,
Proposition 9.3 of [BBG19a](https://arxiv.org/abs/1710.07658v2), and the
introduction of [BBG19b](https://arxiv.org/abs/1811.08862v2). The surviving knot
boundaries are `T(2,2g+1)`, `T(3,4)`, and `T(3,5)`. The parity test is valid:
the knot intersection form is unimodular, its reduction modulo two agrees with
the symmetrized form, and the latter must have odd determinant. This excludes
the determinant-four D family and determinant-two E7; odd-rank paths cannot be
knot fibers.

The report correctly distinguishes an embedded fiber from an abstract lattice.
BBG19b Theorem 1.5 requires a prime strongly quasipositive link, definiteness,
and BKL exponent at least two. Its other definite basket examples prevent the
missing geometric classification from being treated as automatic.

### 4. Surgery exact triangles

The mapping-torus exact sequence gives a free meridian summand and
`coker(A^2-I)`. The longitude is null-homologous because it bounds the fiber.
The determinant factorization gives torsion order
`|Delta(1)Delta(-1)|=D`, so all displayed integral meridian-plus-longitude
fillings have order `D`, while longitude filling retains first Betti number one.
The three selected slopes have pairwise distance one and admit the surgery
triangle orientation convention.

For a cyclic exact triangle, the dimension identities in the report are exactly
rank-nullity. Inclusion, projection, and the zero map realize
`(D,D+r,r)` with exactness at all three terms. An even positive `r` is compatible
with the elementary parity constraint for the rational-homology-sphere terms.
Larger `r` also defeats any fixed lower bound on the third term. No geometric
realization is needed or claimed: this disproves the proposed inference from
the listed rank information, not the knot conjecture. Further geometric,
Spin-c, grading, or cobordism-map constraints could still matter.

### 5. Khovanov spectral sequences

The reduced Khovanov-to-Floer direction and the rank bounds agree with
[Ozsvath–Szabo, Theorem 1.1 and Corollary 1.2](https://arxiv.org/abs/math/0309170).
The page-dimension drop is twice the differential rank. In the explicit filtered
complex, the differential lowers filtration by two, the excess generators form
acyclic pairs, and `e_1` is never a boundary. The model correctly demonstrates
that a protected class and excess initial rank need not force excess terminal
rank. It is not asserted to reproduce every grading restriction of a link
spectral sequence.

[Baldwin, Section 9](https://arxiv.org/abs/0809.3293), printed pages 34–35,
provides the actual `T(3,4)` warning: reduced Khovanov rank five becomes Floer
rank three with the distinguished class surviving. The report explicitly
recognizes that this knot is not hyperbolic. The unresolved need for additional
hyperbolicity-sensitive survival information is stated accurately.

## Remaining scope and approach count

[Farber–Reinoso–Wang, Theorem A and Corollary 1.3](https://arxiv.org/abs/2203.01402v2)
exclude genus-two hyperbolic L-space knots and settle the higher-order question.
Together with the standard genus-one classification, the report's genus-at-least
three residual condition is justified. The remaining conditions are necessary
reductions under a hypothetical counterexample, not evidence that one exists.

There are five distinct mathematical routes: integral monodromy; taut
foliations; geometric Hopf plumbing; Floer surgery triangles; and the Khovanov
spectral sequence. The fourth and fifth are distinct despite both using ranks:
one studies cobordism exactness between different fillings, the other studies
differential cancellation for a single branched cover. Each includes a
mathematical derivation and an explicit unresolved step. Source inspection,
bibliographic correction, and computational tests receive no additional
attempt credit. **The proper status is unresolved, with 5/5 attempts recorded.**

## Execution and independent arithmetic

`REPLAY_AUDIT.json` records:

- Real UID and effective UID both 1000, Python 3.12.14.
- Checker copies with file mode 0444 inside a directory of mode 0555; direct
  append and new-file probes both failed with permission denial.
- Normal, `-O`, and `-OO` checker executions all returned zero and produced
  byte-identical saved output, including 878 positive and three internal negative
  controls per run.
- Eight separate mutations rejected in every mode, totaling 24 failing control
  executions: monodromy order, cyclotomic normalization, Baker–Kegel determinant,
  ADE strict boundary, exceptional filling slopes, triangle projection,
  differential rank, and permanent-cycle protection.
- No assertion statements in the author checker, and only standard-library
  imports. The standalone checker requires neither sources nor network access.

The separate `independent_checks.py` imports no author code. It uses
fraction-free Bareiss determinants, integer backward substitution, independent
cyclotomic construction, and bit-mask GF(2) rank calculations. Its 1,071 checks
cover four definite monodromy examples, 32 Baker–Kegel polynomials, the formal
companion divisibility, 62 trivalent-tree cases, 600 rational slope examples,
25 exact-triangle models, and 25 filtered-complex models. Its normal, `-O`, and
`-OO` outputs are byte-identical. These finite checks supplement the written
proofs; they do not verify imported topology or recompute knot signatures.

To reproduce, run the independent checker in all three Python modes and compare
with `independent_results.json`. Run `replay_audit.py` with the author package
directory as its sole argument using a real nonroot account; it makes a temporary
read-only copy, runs the three modes and eight mutations, and prints its result.
The observed account IDs and Python version are recorded, not assumed portable
across machines.

## Publication boundary

The reviewed author archive contains exactly eight public files: the seven
entries pinned by its manifest and the manifest itself, with byte-for-byte
matches. It contains no source PDFs or extracted source
bodies. This audit contains only authored review text, authored checker and
control code, exact arithmetic outputs, and verification metadata. No external
publication, repository modification, or queue edit was performed in this audit.
