# Independent adversarial audit: Problem 6200007

Date: 2026-10-04 UTC. Identity: AMR-061-0007, rank 548, Kapovich's Problem 7.

## Verdict

**PASS for the stated partial results; retain `unsolved | 5/5`.**

No material mathematical defect was found in the frozen packet's scoped
claims. In particular, the finite-orbit annulus obstruction in Theorem 4.5
survives the nonconicality, compactness, graph-realization and nonproper-boundary
challenges examined below. It does not refute the original realization question.
The positive hyperbolic-plane control is essential and correct.

This is an independent AI-assisted mathematical audit, not human peer review,
formal verification, a novelty certification, or an exhaustive literature search.
The recommendation records what this packet establishes, not a certification
that the problem has no solution elsewhere in the literature.

## Frozen object and reproduction

The audited author packet contains 15 files including its hash manifest.
All 14 entries in that manifest passed independent byte-length and SHA-256
verification. No author file was changed.

- Author manifest SHA-256:
  `5f02f43dd7fad57a3bfb65205a7d53be2d9d0e42896870c8bc3aa77f72bc63b7`
- Main proof, `TURN_4.md`, SHA-256:
  `648d14899fc0f26848a59019328179cff8ab2658bbbe866a87c541b637dc34f2`
- The fresh execution of the frozen `verify.py` passed 59,002 exact finite
  assertions. Its stdout is byte-identical to frozen `CHECKS.json`.
- `CONTROL_REPLAY.json` preserves that fresh output. The separate
  `audit_verify.py` rechecks the frozen identity and replay, and runs additional
  independent rational/integer controls. It takes the author-packet directory
  as its sole argument and does not write to that directory.

The finite checks do not certify conicality, compactness, an infinite chain,
the existence of a boundary homeomorphism, or a universal realization. The
written arguments, including their cited dependencies, are the relevant proofs.

## Exact target and source scope

Kapovich's author-hosted list, Problem 7 on printed/PDF page 3, was checked
in text and visually. Its explicit every-orbit-dense clause means minimality.
The AIM list's Question 7 agrees. The target is the entire given compact
metrizable boundary and uniform quasi-action constants. It adds no finite
generation, properness, cocompactness, or prescribed boundary metric assumption.
The local-compactness discussion about CAT(0) boundaries on the preceding
page does not impose such an assumption on this separate problem.

Primary statement: [Kapovich, Problem 7](https://www.math.ucdavis.edu/~kapovich/EPR/problems.pdf#page=3).
Alternative primary list: [AIM, Question 7](https://aimath.org/WWN/groupboundaries/groupboundaries.pdf#page=3).

The relevant full arguments were read, rather than treating abstracts or
catalogue summaries as proofs:

- Bowditch 1998, Sections 2–7: finite-tree crossratio approximation,
  quasimetric realization, compatible-boundary identification, and annulus
  axioms. Section 8 was additionally checked for the infinite-system issue.
- Bowditch 1999, Proposition 1.1 and Lemmas 1.2–1.7: triple properness versus
  collapsing subsequences, allowing a finite action kernel.
- Sun 2019, the main statements and all of Section 6: the isometric graph
  action exists without an assertion that its boundary is the original space.
- Azemar 2022, Section 2.3, Section 3.1 through Proposition 3.15, and the
  full-measure argument through Proposition 3.21 and its local prerequisites:
  the boundary correspondence is restricted to the stated subsets.

All seven reading-copy fingerprints in the author source manifest matched
their recorded byte lengths and SHA-256 values. Source documents and their
full text are not reproduced in this audit.

References: [Bowditch 1998](https://bhbowditch.com/papers/bhb-topchar.pdf),
[Bowditch 1999](https://bhbowditch.com/papers/bhb-convergence.pdf),
[Sun 2019](https://arxiv.org/pdf/1707.04587v4),
[Azemar 2022](https://ems.press/content/serial-article-files/30115).

## Adversarial examination of Theorem 4.5

### 1. Finite annulus orbits really give the required compactness bounds

For Lemma 4.1, infinitely many distinct annuli yield, after fixing one of
finitely many orbit representatives, distinct translating elements. If the
repeller misses a fixed closed annulus half, convergence is uniform on that
half. Its images then have arbitrarily small diameter in a compatible metric
and cannot meet two fixed disjoint compact sets. Applying this separately
to both halves forces the repeller into both disjoint halves, a contradiction.
No stabilizer-finiteness assumption about an individual annulus is needed.

The same proof permits overlap between a compact set from the first pair and
one from the second. It needs separation within each pair only. This matters
in Lemma 4.3, where a neighborhood of the limiting point appears on one side
and the point itself on the other. Compactness and metrizability supply the
closed separated neighborhoods used there.

The A2 argument also checks out: normalize a crossing annulus to a fixed
type, pass to convergent point sequences, and note that the two limiting
points in each pair remain separated because they lie in opposite closed
halves. Lemma 4.1 bounds all annuli in the allegedly arbitrarily long other
chains. This proves a uniform crossing bound, not just pointwise finiteness.

The nesting convention in the packet is consistent with Sun and Azemar.
It implies that every annulus in a separating chain individually separates
its endpoints. Its strictness excludes repeats, so a finite count of
separating annuli bounds chain lengths. The opposite-looking formula in
the older Bowditch text is not used to reverse this argument.

### 2. Nonconical points and parabolic cyclic orbits

Lemma 4.2 correctly applies convergence to the inverses of the translating
elements. At least one of the two fixed points differs from the inverse
sequence's repeller, forcing the attractor into the negative closed half.
If the candidate nonconical point were not the repeller, its image would
put the same attractor into the positive half. It must therefore be the
repeller. Compactness then supplies a subsequence on which its own images
converge inside the positive half, giving two distinct limiting points and
a conical sequence. This contradiction proves the claimed finiteness.

For Lemma 4.3, exactly two of the nine pair-pair terms can be nonzero.
One is bounded by the finite pair-point depth; the other is uniformly
bounded by Lemma 4.1. Finitely many initial terms are harmless by A1.
This proves boundedness of the specified canonical sequence, not of every
sequence converging topologically to the point.

Lemma 4.4 uses both forward and backward collapse of the parabolic powers.
The intermediate triple gives two bounded terms, after invariance and a
permutation of coordinates. The established additive triangle inequality
then bounds the positive powers; invariance and symmetry handle negative
powers. Distinctness of the triples holds eventually. A1 handles the finite
remainder. Thus this is a bound on the full cyclic orbit in the triple
quasimetric, not merely a bounded subsequence.

### 3. The modular nonconicality argument is valid

Distinct elements of PSL_2(Z) have determinant-one integer representatives
whose maximum-entry norms escape every bound. A subsequence of normalized
matrices converges to a nonzero rank-one matrix. Projectivization converges
locally uniformly away from its kernel: on any compact set there, the norms
of the normalized output vectors have a positive lower bound.

For a supposed conical sequence at infinity, the limiting image is the
common limit on the complement, whereas the exceptional image is different.
Consequently the limiting kernel is infinity. If the columns are u_n and
v_n, the second column grows without bound, while the first is a nonzero
integer vector and has Euclidean norm at least one. The exact identity

|det(u_n,v_n)| / (||u_n||_2 ||v_n||_2)
 = 1 / (||u_n||_2 ||v_n||_2) <= 1 / ||v_n||_2

forces the projective angle between the two column lines to tend to zero.
But those lines are respectively the images of infinity and zero, which
the conical hypothesis makes converge to different projective points.
This is a contradiction. The argument handles signs, an attractor at
infinity, and column vectors whose norms grow at different rates.

The convergence-action assertion follows from the same rank-one limit.
Minimality follows because every orbit closure contains infinity under
translation and hence contains its dense rational orbit. These arguments
do not assume that the action is uniform on triples.

### 4. The graph is geodesic; properness is unnecessary

The explicit two graph bounds in Lemma 2.1 are correct. The prescribed
rough-geodesic sequence gives an edge path of length at most rho+s; an
m-edge path gives rho <= m(s+1+r). Repeated adjacent vertices can be
deleted without increasing the path length. The connected unit-edge graph
has a geodesic geometric realization even when its vertex set or degrees
are infinite: shortest vertex-to-vertex lengths are minima of nonempty
sets of nonnegative integers, and edge-interior endpoints cause no issue.

The graph action is genuinely isometric and the vertex inclusion is
equivariant and quasi-surjective. Hyperbolicity and the boundary
identification used in the sufficient A1–A3 criterion follow through the
hyperbolic path-quasimetric theory. Local finiteness, metric properness,
compact graph balls and a proper interior action are not silently assumed.

### 5. Bounded base-point displacement rules out the circle boundary

Here is a fully explicit version of the boundary step, including nonproper
spaces. For interior points of any metric space,

|(x|y)_o - (x|y)_p| <= d(o,p).

For a hyperbolic space, define a boundary product using the supremum of
liminf products over representative Gromov sequences. The same inequality
passes to these products, and isometries preserve the product when the
base point is moved with them. Therefore, if d(o,h^n o) <= D for all
integers n,

(h^n xi|h^n eta)_o >= (xi|eta)_o - D

for every n and every pair of boundary points. Other usual product
conventions change this by a fixed hyperbolicity constant only. The
Gromov-product entourages thus give uniform equicontinuity of all powers.
This argument uses neither compactness of balls nor the existence of
geodesic-ray representatives. It works with the Gromov-sequence boundary.

If the graph boundary were homeomorphic to RP^1, it would be compact and
its compatible uniformity would agree with that of the circle. The inverse
powers would then be uniformly equicontinuous. Yet n and n+1 both approach
infinity in RP^1, while applying the inverse nth translation sends them
to the two fixed distinct points 0 and 1. This contradicts equicontinuity.
Thus the asserted failure is for every equivariant boundary homeomorphism,
not just for the customary triple-space boundary map.

The exact PSL_2(Z) action on H^2 has the desired circle boundary. The two
fractional-linear identities and hyperbolic-distance substitution given in
the packet prove the isometry claim. Accordingly this example cannot be
promoted to a counterexample to Kapovich's original question.

## Other claims and the five-attempt count

- **C1 passes.** Finite stars realize all finite boundaries, including the
  elementary cases. In the infinite minimal case, an isolated-point orbit
  would make the entire compactum discrete. The compact exhaustion of
  triples correctly proves countability; a triple stabilizer contains the
  action kernel and is finite.
- **C2 passes as a credited sufficient criterion.** A1–A2 give the
  hyperbolic path quasimetric; A3 supplies compatibility with the given
  topology. This compatibility cannot be omitted. The graph realization
  turns the successful conditional construction into an exact action.
- **C3 passes.** The inverse-map equicontinuity contradiction is sound.
  The decorated tree model is a metric within one of a tree pullback,
  with a correctly bounded four-point defect and the indicated boundary.
  Fixed-element lifts have bounded additive error, whereas the explicit
  height-n witnesses force an error of 2n+1 at input distance one.
- **C5 passes.** The all-annuli construction chooses actual distance
  values tending to zero before selecting the separating radii, so it
  works even for disconnected perfect compacta. The sum and maximum
  examples give unbounded four-point defects. They are not themselves
  convergence-action counterexamples, as the packet explicitly says.

The five documented routes are mathematically distinct: elementary
reductions, the sufficient annular route, metric/fixed-height lifts,
finite-orbit repair at a cusp, and unrestricted enlargement/aggregation.
They support five substantive attempts, not five solutions or five
independent chat sessions. The subjective progress percentages are not
quantitative evidence for the universal problem.

## Nonblocking clarifications

1. The account of the infinite-annulus gap can be sharpened by mentioning
   Bowditch's Proposition 8.2: a general convergence action already has an
   invariant symmetric, possibly infinite-orbit system satisfying A1, A2
   with zero crossing constant, and A4 (separation of distinct points).
   Lemma 8.3 upgrades separation at conical points. What remains missing
   for this route is A3 at all points, including nonconical points.
   This does not contradict the packet's stated A1–A3 gap or change its
   disposition. [Bowditch, Section 8](https://bhbowditch.com/papers/bhb-topchar.pdf#page=23).
2. For maximum notational precision, use Euclidean norms for the column
   angle calculation and describe projective convergence by the nonzero
   output-vector bound (or a suitable target chart). In the fixed-height
   proof, apply the difference of common-prefix lengths to distinct
   boundary points; the equal-point case is immediate and need not use
   the undefined expression infinity minus infinity. These are
   clarifications, not repairs to the mathematical conclusions.

No mandatory mathematical repair is required for the scoped publication.
Sun's group-level hyperbolic action and Azemar's full-measure boundary
correspondence do not resolve the prescribed whole-boundary requirement.
No claim of a universal construction, a genuine non-realizable action,
historical priority, or an exhaustive current-status search is justified.

## Public-package check

The audit deliverables contain the review, structured verdict, exact
control reports, a small independent verification script, and hashes.
They contain no source-paper copies, catalogue corpus, source extraction,
credentials, private preparation records, or machine-specific paths.
Only the frozen mathematical claims and public bibliographic sources are
described. No remote mutation was performed during this audit.
