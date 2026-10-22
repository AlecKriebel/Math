# Research report: full monomial signatures

## Target and outcome

AIM's *Components of Hilbert schemes*, Problem 16, concerns injectivity of
\(C\mapsto\operatorname{Mon}(C)\) on irreducible components of
\(\operatorname{Hilb}^d(\mathbb A^n)\), with a corresponding question for
\(\operatorname{Hilb}^P(\mathbb P^n)\). The source mentions a possible
curve-Hilbert-scheme counterexample in Richard Liebling's thesis. This
investigation did not recover that thesis's full text and does not confirm
the suggested counterexample.

The broad affine and projective questions are **not solved here**. The result
is an explicit refinement of the earlier small-length partial result, plus
checks that rule out two tempting but invalid shortcuts. No claim of novelty
is made; the new derivations may be known informally or elsewhere.

## Exact recovery and prior work

The requested numeric landing page was tried first; the web reader reported
it inaccessible. The complete supplied problem corpus and complete research
report corpus were parsed. The selected record's exact statement hash agrees
with the catalog, and AIM's own PDF text independently confirms Problem 16,
its affine/projective scope and its separate Liebling remark.

The full prior report, not merely its summary, was read. It already proves
the ambient-smooth-anchor criterion, the smoothable anchor, affine
injectivity through length eight in characteristic zero, the singular
collision example and the characteristic-zero projective two-Borel boundary.
Those results are not rebranded as new. The present additions are:

1. An exact description and count of the *entire* nonsmoothable-component
   signature at length eight in every ambient dimension, including boundary
   functions (1,5,2), (1,6,1), (1,7).
2. The characteristic ranges already justified by primary literature:
   affine characteristic different from 2,3 and projective two-Borel in all
   characteristics.
3. A sharp obstruction to the proposed affine search strategy: every
   nonsmoothable component's monomial points are ambient-singular because
   they are all also smoothable.
4. An explicit full-signature separator for BCR's equal-double-generic pair.

The repository's actual main attempts directory was inspected: 62 entries,
none for this numeric ID. Exact ID/default-branch code, branch, commit and PR
searches, plus code and PR title searches for the monomial-signature phrase
and exact-code PR search, returned no selected attempt. A recursive main-tree
request failed with a transport error; the successful attempts-directory
inspection is narrower. No absence claim is made about deleted branches,
unindexed material or unpublished work. No remote mutation was performed.

## Five substantive approaches

### 1. Primary recovery and later literature

Recovered the original scope and audited the imported report against CEVV,
Reeves--Stillman, Ramkumar v4, Staal v2, BCR Example 6.12, and Jelisiejew's
July 2026 survey update. Bérczi--Svendsen's current arXiv entry confirms the
characteristic-zero punctual curvilinear-incidence result; that is stronger
incidence information than ordinary smoothability but is not an injectivity
theorem. Farkas--Pandharipande--Sammartano's August 2026 revision concerns
irrational components, not equality of full monomial sets. Searches for
Liebling's thesis recovered university metadata and later citations, not a
verifiable full-signature example. This bounded search is not proof that no
later resolution exists.

### 2. All-characteristic structural reduction

The classical distraction construction proves that every finite-colength
monomial ideal is smoothable. A complete proof is supplied, along with the
regular-sequence tangent calculation at the curvilinear monomial ideal.
Hence the smoothable component is always separated and any equal-signature
pair must be nonsmoothable. This rules out ambient-smooth monomial anchors
on those components. A counterexample requires at least three components.

### 3. Exact length-eight incidence

The imported CEVV classification leaves two components. To find the whole
second signature, the proof uses normalized traces in the universal length-
eight algebra: centered triple products vanish and pair-product rank is at
most three, both closed conditions. At monomial ideals these imply precisely
cube-zero and embedding dimension at least four. Conversely, an explicit
free rank-eight multiplication table turns some socle variables into
quadratic products for nonzero parameter, producing a (1,4,3) algebra.
This proves the claimed criterion and the closed binomial count.

The higher-dimensional closure matters. A family with multiplication
(x_1^2=tw) can increase embedding dimension in the special fiber. Counting
only ideals with Hilbert function (1,4,3) would incorrectly give
(120\binom n4\) when (n>4). The correct count adds the three boundary
Hilbert functions. This refinement is new relative to the supplied report,
not asserted novel in the literature.

### 4. Projective characteristic boundary

Reeves--Stillman's theorem applies over any field to the saturated lex point.
Ramkumar's 2022 v4 explicitly combines characteristic-independent deformation
computations with Staal's arbitrary-characteristic classification. Thus the
two-Borel result need not be restricted to characteristic zero. The
characteristic-two exception concerns which Hilbert polynomials have two
Borel-fixed points; the theorem is conditioned on the actual number and
does not confuse strongly stable ideals with all Borel-fixed ideals.

### 5. Candidate collisions and falsification controls

The CEVV collision point has tangent dimension 33, versus component dimensions
32 and 25, and is separated from the smoothable anchor of tangent dimension
32. Sharing a singular point is not sharing an entire signature.

BCR's two nonlex components of \(\operatorname{Hilb}^{3t+2}(\mathbb P^3)\)
have the same double-generic initial ideal. The monomial ideal
\((x_3,x_0^2)\cap(x_1,x_2)\) separates them. Its scheme is a disjoint double
line and line and deforms to a disjoint conic and line. A proper flag-Hilbert
projection forces any limit of twisted cubic plus point to contain a
subscheme of polynomial (3t+1), which is impossible in this pure locally
Cohen--Macaulay scheme. Full details are in Proposition 7.1.

Finally, an explicit union of two invariant smooth projective conics has
identical torus-fixed sets on its two components. It is not an ordinary
Hilbert scheme counterexample, but proves that abstract fixed-point and
projectivity arguments alone do not settle the AIM question.

## Verified controls

`results/verification.json` records deterministic PASS output. All arithmetic
is exact. The implementation uses only the Python standard library.

- Exhaustive length-eight down-set counts in dimensions 1–7:
  1, 22, 160, 684, 2145, 5507, 12300.
- Corresponding nonsmoothable signatures:
  0, 0, 0, 120, 705, 2451, 6553, matching the formula.
- 247 multiplication models and 512 associativity identities per model,
  checked as polynomial identities with integer coefficients.
- The tangent dimensions over \(\mathbb Q\) of all 120 four-variable
  (1,4,3) monomial points are at least 33. Both the imported collision and
  the published variable-permuted version give 33; the anchor gives 32.
- The projective separator's Hilbert function equals (3d+2) in each
  tested degree 2–12. The proof establishes its polynomial independently.

Rational tangent calculations do not certify all positive characteristics;
characteristic-uniform assertions rely on the proofs and specifically cited
published results. Enumeration is not used to certify component membership
without the geometric argument.

## Remaining gap and disposition

The investigation provides no general comparison of two nonsmoothable
components for length at least nine, and no general projective comparison
once the small-Borel theorem ceases to apply. It also makes no assertion
about the small-length classification in characteristics 2 or 3, nilpotent
thickenings or scheme-theoretic equality of fixed loci. Liebling's indicated
example remains a verification gap. The correct disposition is partial
progress with the original question unresolved, not solved or disproved.

A fresh independent audit should concentrate on Theorem 3.1 (closed trace/
rank conditions and the flat converse), the closure warning, Proposition
7.1 (properness and purity), and the arbitrary-characteristic projective
inference. The author replay does not supply that independent audit.
