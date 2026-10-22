# Independent adversarial audit: problem 30000638

Audit date: 2026-10-06 UTC. Rank 814; OWR-1394-015.

## Decision

**Accept the mathematical partial results. Accept the separately corrected
verifier within its stated finite scope. The general conjecture remains
UNSOLVED.** No claim of novelty or formal proof verification is made.

The frozen author verifier has two reproduced gaps: unmanifested Python
bytecode can bypass recomputation, and rehashed source-status flags can
contradict the partial-result status. Accordingly, the uncorrected verifier
does **not** receive unqualified fail-closed acceptance. These are executable
verification/metadata defects, not counterexamples to the mathematical claims.

The original author ZIP and all ten extracted members remain unchanged.
Only `verify.py` and its corresponding `MANIFEST.json` entry change in the
separate `corrected` derivative. `correction.patch` is the exact difference.
The delivered tests apply that patch to a fresh frozen copy, compare every
resulting file with the derivative, and execute the actual patched verifier
in both normal and optimized Python modes.

## 1. Scope, normalization, and source identity

The target is the lower bound

    n! vol_n(P) >= 2^(n-1) (I(P)+1)

for full-dimensional origin-symmetric lattice polytopes, with ordinary
Euclidean volume and I counting strictly interior lattice points. The
complete supplied problem record, every nested field, and the absent-report
object `{}` were independently reviewed. Their specified canonical review
serialization is 3,670 bytes with SHA-256
`7c16b99985deb840b0695c618ce1f79f12c7da37eaecaa1e33145695b89756e6`.
The catalog agrees with that identity and identifies rank 814.

All three complete corpus byte counts/hashes and the four locally held
public-source PDF hashes match the author's metadata. Those datasets,
source PDFs, extracts, and rendered pages are excluded from this package.

The primary OWR page was independently inspected visually by rendering
printed page 3386 from the hash-verified PDF. The web reader retrieved the
report text, but its screenshot endpoint failed; that failed call was not
treated as visual inspection. The problem site's web-reader access also
failed. The target and the adjacent stronger coefficient conjecture were
checked against the primary report, rather than inferred from the failed
website access. See [OWR 56/2006, p.3386](https://doi.org/10.4171/owr/2006/56).

For full-dimensional P=-P, zero is interior. Every other interior lattice
point is paired with its distinct negative, so I is positive and odd.
Boundary lattice points are similarly paired and B is even. Here B counts
all boundary lattice points, never merely vertices. A nonlattice symmetry
center and a lower-dimensional ambient-volume formulation are outside the
author's claims.

## 2. Mathematical audit

### Base cases and Hibi's hypothesis

The interval calculation and the planar Pick-theorem calculation are
correct. In dimension two, equality is equivalent to B=4, hence to a
parallelogram with no boundary lattice points other than its four vertices.
In every dimension, choosing n independent lattice vertices produces an
inscribed lattice crosspolytope of normalized volume at least 2^n. Thus
I=1 is correctly certified.

The Ehrhart coefficients used here are the h-star/binomial-basis
coefficients. Their identities give h_0=1, h_n=I,
h_1=I+B-n-1, and sum h_i=n!vol. Hibi's lower bounds for the middle
coefficients require an interior lattice point. That requirement holds
here, since zero is interior; the bounds are not being applied to hollow
polytopes. The relevant explicit hypothesis is present in
[Henk–Tagami, introduction, equation (1.6)](https://arxiv.org/pdf/0710.2665).

Combining the middle-coefficient floors gives exactly

    V >= 1+I+sum_{i=1}^{n-1} max(binomial(n,i), I+B-n-1).

Discarding the binomial floor yields
V >= nI+(n-1)B-n^2+2. Rearranging this last inequality against the target
gives the author's criterion (HB), with the correct constants and direction.

In dimension three, B>=6. If B=6, there are at least six vertices and at
most six boundary lattice points, hence exactly three independent antipodal
vertex pairs. Their convex hull is a lattice crosspolytope. Otherwise
evenness gives B>=8, so

    V >= 3I+2B-7 >= 3I+9 >= 4I+4  when I<=5.

This proves the entire asserted I=1,3,5 range, not just the finite examples.
The abstract vector (1,11,11,7) indeed passes the expressly listed numerical
tests and has total 30<32. No realizability claim is made. The parity test
is also valid: every dilation has an odd closed lattice-point count, and
reducing the Ehrhart generating function modulo two gives h-star
congruent to (1+t)^n.

### Crosspolytope quotient argument and equality

The determinant index is exactly D=|det A|. Two interior points in the same
coset differ, in A-coordinates, by an integral vector of l1 norm strictly
below two, hence by a signed coordinate unit vector. Three distinct points
would require two distinct signed unit differences whose difference has
l1 norm two. This is impossible. The zero coset contains only zero; the
remaining D-1 cosets contain at most two points each. Thus I<=2D-1, and
V=2^nD proves the target.

The strict inequality defining the interior is essential and is correctly
retained. No lattice-index or boundary-count substitution was found. This
proof also gives an exact occupancy characterization of equality: every
nonzero quotient coset must contain two interior points. The stretched
examples realize equality for every positive odd I; the author does not
claim they classify all equality cases. The known crosspolytope result,
the planar case, and binomial coefficient floors are correctly credited to
[Bey–Henk–Wills, Proposition 1.4 and Remark 1.6](https://arxiv.org/pdf/math/0606089).

The interior-preserving containment corollary is valid. Mere containment
does not identify interior counts, as the stated scaled-crosspolytope/cube
example correctly illustrates.

### Products and free sums

The product proof correctly requires n,m>=1. Interiors multiply and
normalized volumes acquire binomial(n+m,n). Since this binomial is at
least two and I,J>=1, the claimed strict inequality follows. Dimension-zero
factors would not justify this strictness and are explicitly excluded.

For a free sum in complementary coordinate spaces, its gauge is p(x)+q(y).
When Q has only zero as an interior lattice point, every nonzero integral y
has q(y)>=1. Such a y cannot occur in a strict inequality p(x)+q(y)<1,
including at boundary gauge q(y)=1. Therefore the interior lattice points
are precisely (x,0) with x interior to P. The beta-integral for the sections
gives V(P free-sum Q)=V(P)V(Q) with the stated factorial normalization.
The lower bound V(Q)>=2^m completes the proof without reflexivity or an
Ehrhart-series factorization. This proof uses positive dimensions, as in
the global setup; a zero-dimensional factor, if separately allowed, gives
the trivial identity instead of the displayed positive-dimensional integral.

There is no overlooked boundary contribution. A useful equality check is
that a free sum here is an equality case exactly when P is an equality case
and V(Q)=2^m. The latter is equivalent to Q being a unimodular
crosspolytope: the inscribed minimal crosspolytope must fill Q, since strict
containment of full-dimensional convex bodies would strictly increase volume.
This observation is an audit consequence, not a new classification claim
about the unresolved conjecture.

For precision, writing Delta(P)=V(P)-2^(n-1)(I(P)+1), the general free-sum
gap is

    Delta(S)=V(Q)Delta(P)+2^(n-1)(I(P)+1)(V(Q)-2^m).

Thus satisfaction is preserved and the gap is at least V(Q)Delta(P).
The gap is exactly multiplied only when V(Q)=2^m. This makes precise the
informal gap-preservation sentence following Theorem C without changing
the theorem or its proof.

### Successive minima and Henze

The lower half of Minkowski's second theorem has the direction and n!
normalization used in the proof. The cube obstruction correctly shows
failure of an extra sufficient condition, not failure of the conjecture.

Henze's theorem has an epsilon-dependent dimension threshold and uses the
closed lattice count G(K), not I+1. The positive-coefficient Laguerre
polynomial and equation (2.4) give the author's fixed-dimensional bound
and boundary criterion exactly. Its coefficient identity is correct by
substituting k=n-i in the two sums. The exact factor 2^(n-1) cannot be
obtained simply by setting epsilon to zero or replacing G with I+1.
See [Henze, Theorem 1.1 and equation (2.4)](https://arxiv.org/pdf/1203.4075).

The independently repeated bounded literature search did not identify an
authoritative general resolution. This is a limited search outcome, not
proof of global absence. The reviewed work remains a partial investigation.

## 3. Independent finite and adversarial checks

The normal and optimized original replays reproduce 37 geometric cases,
seven residue cases, 20 rational Laguerre identities, and 4,900 product
parameter checks. The original 36-test fail-closed harness also replays.

An independently written standard-library engine imports no author code.
It recomputes all 37 volumes, interior counts, dilation counts, h-star
vectors, and facet counts. Facet areas are obtained by exhaustive supporting
edges and a divergence-formula calculation, rather than the author's
monotone-chain hull and origin-tetrahedron fan. Both computations use exact
integer/rational arithmetic. This is a genuine finite cross-check, while
sharing the elementary supporting-plane characterization of convex hulls.
It remains neither exhaustive polytope enumeration nor a machine proof of
the general statements.

### Finding A: unmanifested bytecode execution

The frozen `verify.py` ignores `__pycache__` in its file inventory, then
imports `exact_geometry`. Setting `sys.dont_write_bytecode=True` prevents
cache creation but does not prevent cache loading. A valid-timestamp cache
can supply a replacement computation returning the stored results, yielding
PASS_PARTIAL without recomputation. The audit reproduces this in normal
and optimized modes with a harmless temporary marker. None of the frozen
source/manifest bytes is changed. The delivered archive itself contained
no malicious cache, and its clean-run numerical outputs remain valid.

Correction: reject every extra inventory entry, retain the just-verified
source bytes, and compile/execute those exact bytes rather than using an
import that could consult caches. The mutated derivative rejects the cache
before executing it. The source-only execution is defense in depth.

### Finding B: source-status flags not semantically checked

Changing `SOURCES.json` to claim full resolution, then refreshing that
file's manifest entry, passes the frozen verifier. Other claim booleans,
missing claim keys, an extra claim, and integer zero in place of false
also pass. This is not an integrity collision: it is a missing semantic
guard, within the rehashed-mutation model used by the author's own tests.

Correction: require the exact five expected claim keys and literal false
values. The corrected verifier rejects all tested contradictory or
malformed claims. The existing original metadata is unchanged; its
`independent_audit_claimed=false` describes the original author package.
This independent report is separate.

## 4. Acceptance and reproducibility

Run `python audit.py` from any working directory. Python 3.10+ and the
standard library suffice for computation; the exact-patch application
test also requires the ordinary `patch` command. `python -O audit.py`
is supported. Results are recorded in `audit_results.json`; the file is
regenerated only with the explicit `--write-results` argument.

The audit executes the corrected normal and optimized verifier, the
original 36-case harness against both fixtures (72 checks), and 52
additional mutation probes across both fixtures and modes. It also applies
the delivered patch to a fresh original, confirms byte-for-byte identity
with the tested derivative, and runs the applied files in both modes.

An audit manifest binds every delivered member other than itself. The
outer ZIP hash must be checked separately. This is reproducibility and
scope checking for trusted Python and trusted anchored code, not a sandbox
against a hostile interpreter, standard library, or wholesale replacement
of both code and its unanchored manifest. No remote mutation, publication,
or external outreach was performed by this audit.
