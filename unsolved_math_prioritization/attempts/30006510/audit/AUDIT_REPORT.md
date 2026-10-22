# Independent adversarial audit: typical hyperbolic cells

Problem 30006510 / OWR-14299586-001, rank 501. Audit date: 3 October 2026.

## Verdict

**PASS for the stated scoped partial results. The original problem remains UNSOLVED, with five substantive approaches recorded. No full-solution promotion is warranted.**

No blocking mathematical error was found in Propositions 1, 2, 3, 4, 6, or 7, or in the ideal-polygon examples. The proofs retain the assumptions needed for their conclusions. In particular, the finite-volume construction is not silently extended to infinite-volume cells, a positive finite intensity is required before normalizing a Palm probability, and the two obstruction theorems are not asserted to exclude every possible interpretation of typicality.

The reviewed author manifest has SHA-256:

`bbe672f14e9a541bc1700d76454c809654478ff159038c0982f17b75f3191648`

All seven author-file lengths and hashes match. The release was not modified. The author controls were reproduced on a disposable copy: 40/40 passed. The separate audit controls passed 80/80 integrity, symbolic-algebra, and finite-normalization checks. These counts do not certify the geometric theorems; the analytic audit below is the substantive basis for the verdict.

This is an AI-assisted independent review of a frozen author packet, not formal verification or human peer review. It makes no novelty certification and does not authorize remote publication.

## 1. Source and scope fidelity

The original OWR report was inspected in its local PDF, including a rendered visual inspection of printed page 3046 (PDF page 16). It defines tessellations using countably many locally finite closed convex full-dimensional cells with disjoint interiors and full coverage. Boundedness is not assumed. Its usual center-intensity/Palm construction is discussed under full-isometry invariance and bounded cells. The subsequent obstruction concerns infinite volume, whereas the open extension question concerns unbounded cells. These are genuinely different conditions.

The frozen packet preserves that distinction. The ideal-triangle test is therefore relevant rather than a counterexample to the source's infinite-volume obstruction. The packet also correctly treats the question as open-ended. A no-go theorem for ambient probability roots is not a negative solution to all possible alternative notions of typicality. [OWR report, p. 3046](https://ems.press/content/serial-article-files/52444).

The following primary-source definitions and scopes were independently checked:

- Bühler--Gusakova--Recke, Theorem 2.1 and Lemma 2.2: the MTP requires a finite outgoing marginal on an open set; the existing point-root obstruction concerns infinite-volume components. The paragraph after Lemma 2.2 explains why allowing the point outside the cell does not remove that obstruction. The packet's probability-kernel formulation is a direct extension of this transport argument. [arXiv:2512.19425v1](https://arxiv.org/abs/2512.19425v1).
- Last, Section 8, especially equations (8.11), (8.14), and (8.15): the proper-partition reciprocal-volume and mean-volume identities are established prior theory. The packet's self-contained truncation argument has the appropriate hyperbolic unimodular specialization. [Author manuscript](https://publikationen.bibliothek.kit.edu/1000012083/1022543).
- D'Achille--Curien--Enriquez--Lyons--Ünel, Sections 4.1 and 5.3: the ideal-cell construction uses an ideal nucleus in a marked corona. The corona action has noncompact isotropy; insertion/Mecke and disintegration replace the compact-isotropy construction. Comparison across embeddings is made on the isometry-invariant sigma-field. The packet accurately preserves this model-specific positive result. [arXiv:2303.16831v3](https://arxiv.org/abs/2303.16831v3).
- D'Achille--Thäle, Section 2 before Corollary 2.4: bounded lower-dimensional ideal faces have ordinary positive finite counting densities, while the usual full-dimensional IPVT typical cell is distinguished from them. [arXiv:2606.26049v1](https://arxiv.org/abs/2606.26049v1).
- Besau--Gusakova--Thäle: the September 2026 model has a chosen horoball/ideal direction and projects to a stationary Euclidean tessellation. Its typical projected-cell statement is not a universal full-hyperbolic-isometry result. [arXiv:2609.10007v1](https://arxiv.org/abs/2609.10007v1).

Live arXiv metadata confirmed the cited version dates: 22 December 2025, 10 June 2025, 24 June 2026, and 9 September 2026 respectively. A fresh targeted search did not reveal a contrary general construction. This limited search is not an exhaustive literature-status guarantee. The remote repository's prior-attempt search and initial queue state were not independently repeated in this audit; the disposition here follows the mathematics of the frozen packet and its five distinct recorded approaches.

## 2. Ambient framework, measurability, and MTP

**Finding: pass.**

The full group `G = Isom(H^d)` is unimodular, and the stabilizer `K` of an ambient point is compact. The action on hyperbolic space is proper. These are the correct hypotheses for the cited MTP and the normalized compact-fiber Haar construction. No uniform probability on `G` exists or is used.

The fiber over `x` is a coset `g_x K`. Pushing normalized Haar measure on `K` through `k -> g_x k` is independent of the representative: replacing `g_x` by `g_x k_0` changes the integration variable by a Haar-preserving left translation of `K`. Choosing `g g_x` for `g x` proves the displayed covariance. The kernel is Borel: the homogeneous space has a Borel section, or one can use continuous hyperbolic transvections from the fixed origin. The packet's pointwise description thus defines a legitimate measurable kernel, not merely a formal family of measures.

The incidence relation `(y,C): y in C` is Borel for the stated closed-set measurable structure. Integrating it against volume makes `V(C)` and `m(C intersect B)` measurable. The full-dimensional convex and finite-volume domains are Borel. These observations justify the measurable integrations used throughout.

Each full-dimensional convex cell has a volume-null boundary. Countability gives a volume-null union of boundaries for each tessellation. Fubini and transitivity of the invariant law then imply that every deterministic point lies in that random boundary union with probability zero. This is the needed justification for `C_o`, not an assertion that all spatial points simultaneously have unique cells. For the incidence identity, a jointly measurable cell-at-location version can be selected on the uniqueness set from the measurable cell-counting measure; arbitrary measurable choices on the boundary do not affect the integral.

The two MTP applications establish a finite outgoing marginal before invoking the theorem:

1. The finite-volume transport uses `V >= 1/n` and bounded `F`, giving density at most `n ||F||_infinity`.
2. The infinite-volume probability-root transport sends total mass at most one per unit ambient volume.

Thus neither application assumes that a locally finite random count already has finite expectation. This is an important and correctly handled issue.

## 3. Proposition 1: moment-free geometric median

**Finding: pass, including existence, uniqueness, cell membership, equivariance, and Borel measurability.**

### Integrability and the noncompact moment issue

The objective is the integral of the single signed difference

`d(x,y) - d(a,y)`.

Its absolute value is bounded by `d(x,a)`. It is integrable against the finite-volume probability measure even if the two individual distance integrals would both be infinite. The proof never subtracts two infinite quantities. The objective is 1-Lipschitz in `x`, and reference-point changes add a finite constant independent of `x`. This supplies both continuity and independence of the arbitrary reference point.

### Strict convexity

For extra verification, take a unit-speed complete geodesic and use hyperboloid coordinates. If `y` lies outside that geodesic, its distance `h(t)` to the geodesic point has

`cosh h(t) = u(t) = A cosh t + B sinh t`, with `A^2-B^2 > 1`.

Then

`h''(t) = u(t)(A^2-B^2-1)/(u(t)^2-1)^(3/2) > 0`.

The symbolic numerator identity is independently checked by the audit script. A geodesic has zero d-dimensional volume when `d >= 2`; hence the normalized cell-volume measure assigns full mass to points off the geodesic. Integrating the pointwise strict convexity inequality gives strict convexity of the objective. The subtraction of the reference-distance term has no effect on this conclusion. The dimension assumption is essential to this particular argument and is present.

### Coercivity and attainment

For each probability measure, a sufficiently large ball about `a` contains mass `p > 1/2`. The displayed lower bound

`F(x) >= (2p-1)d(x,a) - 2pR`

is correct, with strictly positive escape coefficient. It implies compact sublevel sets because hyperbolic space is proper. A finite continuous coercive function therefore attains a minimum. Strict convexity makes it unique. No compactness of the cell and no uniform choice of `R` across cells is needed.

### Membership and equivariance

Metric projection onto a nonempty closed convex subset of a Hadamard manifold is well defined. The CAT(0) projection inequality gives, for `p = projection_C(x)` and `y in C`,

`d(x,y)^2 >= d(x,p)^2 + d(p,y)^2`.

If `x` is outside `C`, distance to every `y in C` decreases strictly. Integrating the finite difference contradicts minimality of an outside minimizer. The center lies in the cell. Isometries preserve the difference objective up to the harmless reference change; uniqueness then forces equivariance.

### Borel dependence

At each dense test point `q_j`, measurable incidence integration makes `F_C(q_j)` measurable in `C`. The countable infimum is measurable and agrees with the actual infimum by continuity. Selecting the first `q_j` within `1/n` of the infimum is a measurable selection. For each fixed cell these selected points remain in a compact sublevel set. Every convergent subsequence has the unique minimizer as its limit, so the entire selected sequence converges. The pointwise limit is measurable. No unproved arbitrary argmin selection is required.

## 4. Proposition 2: reciprocal-volume intensity and Palm normalization

**Finding: pass, with the stated finite-positive-intensity restriction essential.**

Because the center belongs to its cell, centers in a compact set are bounded in number by cells meeting that set. Thus the centered counting measure is almost surely locally finite. Multiplicity, if present, can be retained in the counting measure and does not invalidate the marked Campbell construction.

For bounded nonnegative invariant `F`, the truncated transport has outgoing density

`E[1_{1/n <= V(C_o) < infinity} F(C_o)/V(C_o)]`.

Its incoming marginal on `B` is exactly the expected centered count weighted by `F`, because integrating over the whole cell cancels `V(C)`. The finite outgoing bound permits MTP. The sets `V >= 1/n` increase with `n`; monotone convergence removes the volume cutoff. Truncating `F` then handles arbitrary nonnegative invariant functions, including unbounded `F = V` on the finite-volume sector. Extended values are legitimate at this stage.

Setting `F = 1` gives precisely

`gamma_f = E[1_{V(C_o)<infinity}/V(C_o)]`.

Only when `0 < gamma_f < infinity` is division by this number used to obtain a probability law. Under that hypothesis, `F = V` gives

`gamma_f E_typ[V] = p_f`,

rather than silently using one in a tessellation with an infinite-volume spatial sector. Positivity follows from `p_f > 0`; finiteness does not follow from almost-sure local finiteness. The packet explicitly states these distinctions.

The sufficient local count-moment condition is also correct: the expected number of centers in the unit ball is `gamma_f m(B(o,1))`, and is at most the expected number of cells hitting that ball. No reverse implication is asserted.

### Embedded law versus shape law

The covariance of the Haar fiber implies that `S_z f` is invariant, even when `f` is not. Applying the proven invariant-function identity to `S_z f` yields exactly the source's center-based marked counting formula. Since `S_z 1 = 1`, the displayed `Q_z` is a probability measure. It is supported on cells with `z(C)=o`, is `K`-invariant, and is independent of the volume-one observation set. Its embedded distribution can depend on the chosen center.

The expression `Q_vol` is separately normalized by the same reciprocal-volume expectation. It is supported on cells containing the origin, not necessarily centered there. Its interpretation is the count-typical shape rooted at a uniform volume point, with the isotropic frame convention understood. It agrees with `Q_z` on invariant shape observables. The packet distinguishes these two embedded laws rather than conflating them.

## 5. Proposition 3: infinite-volume probability-root obstruction

**Finding: pass in the precise ambient-kernel scope stated.**

The assignment may depend on the whole tessellation and on additional jointly invariant randomness. Its expected transport is measurable and diagonally invariant. The total outgoing mass from a bounded set is at most its ambient volume because each selected cell kernel has total mass one and cell interiors are disjoint.

For a particular infinite-volume cell, its incoming contribution to a bounded ball is the nonnegative iterated integral of `q_C(B)` over the cell. It is infinite whenever `q_C(B)>0`, and zero when that value is zero. This is a valid integral statement, not an undefined product convention.

Every probability measure on the ambient space gives positive mass to some member of the increasing countable ball exhaustion. On the positive-probability event that any infinite-volume cell exists, some ball therefore receives infinite mass from at least one such cell. The event is a countable union over balls, so at least one deterministic ball has positive probability of infinite incoming mass. Its expected incoming mass is consequently infinite, contradicting MTP. No distinguished exceptional cell, finite center-count moment, or support-inside-the-cell assumption is needed.

Normalizing a finite nonzero equivariant measure gives the forbidden probability kernel; that corollary is valid without assuming a uniform lower bound on its mass. The ambient-volume Palm identity likewise precludes infinite-volume cells under a positive finite ordinary allocation intensity.

These results do not exclude a probability law on isometry classes, a model-specific ideal nucleus, a marked corona, or a different sigma-finite state space. The frozen packet explicitly leaves such possibilities open.

## 6. Proposition 4 and ideal-polygon examples

**Finding: pass.**

If every cell contains an inball of fixed radius `r` at its chosen center, a center within radius `R+r` implies a hit of the radius-`R` window. Conversely, a contained cell forces its inball, hence its center, to lie within radius `R-r`. The deterministic inequalities are in the correct directions. Expectations turn center counts into `gamma` times volume; expected hit counts are permitted to be infinite.

The hyperbolic ball-volume growth has exponent `d-1`, so for fixed `s`,

`m(B(o,R+s))/m(B(o,R)) -> exp((d-1)s)`.

This follows directly by integrating the leading exponential term of `sinh(t)^(d-1)`. The audit's exact binomial controls verify that leading-term algebra in dimensions 2 through 12; the written asymptotic proof applies to all integer `d >= 2`. Thus the outward and inward factors in (4.2) are correct. The statement concerns expectations and does not claim an unavailable large-ball almost-sure ergodic theorem.

A compact hyperbolic reflection chamber yields a genuine bounded-cell example with a positive inradius. Randomizing a fixed tiling by the normalized invariant measure on `G/Gamma` is legitimate because `Gamma` is a finite-covolume lattice and preserves the tiling. It is not sampling a uniform element of the noncompact group. Torsion or finite cell stabilizers do not invalidate this quotient construction.

The ideal-triangle reflection tiling is locally finite in the interior hyperbolic space; accumulation toward ideal vertices occurs outside compact subsets of that space. Its chambers are closed relative to hyperbolic space, unbounded, convex, full-dimensional, and have area `pi`. Proposition 2 gives intensity `1/pi`; no such cell fits inside a finite-radius ball. A regular ideal quadrilateral similarly has area `2pi`. Mixing the two invariant laws equally is a valid nonergodic invariant tessellation law. The packet correctly computes

`gamma = 3/(4pi)`, `P_typ(triangle)=2/3`, `P_typ(quadrilateral)=1/3`,

while the zero-cell mixture weights remain `1/2, 1/2`. This is a valid count-bias test and a valid demonstration that unboundedness alone is not the obstruction.

## 7. Proposition 6 and boundary/corona scope

**Finding: pass.**

For a finite invariant boundary measure, normalization to a probability is legitimate. North-south dynamics of a loxodromic isometry and dominated convergence force that probability to be supported on the two fixed endpoints. A second loxodromic isometry with disjoint endpoints forces incompatible support. Such a pair exists for every `d >= 2`. The argument does not accidentally use a nonexistent uniform boundary probability.

The theorem is about a finite invariant measure on the bare ideal boundary. It does not prove nonexistence of all equivariant per-cell boundary markings, or of invariant measures on marked extensions. In particular, the established corona-Palm ideal-cell construction is compatible with it. The packet makes these limitations explicit and does not pretend that a general canonical corona for arbitrary multi-ended cells has been constructed.

## 8. Proposition 7: universal sigma-finite mean cell measure

**Finding: pass; sigma-finiteness does not need a local count first moment.**

Expectation of the measurable random cell-counting measure gives a countably additive invariant measure on cell space. The explicit cover is effective:

`A_(n,k) = {C: m(C intersect B(o,n)) >= 1/k}`.

Disjoint interiors make the sum of these incidence volumes at most `m(B(o,n))`. Thus there are deterministically at most `k m(B(o,n))` cells in `A_(n,k)`, and its mean measure is finite. Every full-dimensional cell has a positive-volume intersection with some ball and therefore belongs to one of these countably many sets. This proves sigma-finiteness even if every ordinary expected local hit count were infinite. It does not prove Radon local finiteness in the Fell topology, and the packet does not claim that stronger property.

The incidence identity follows by Tonelli: for almost every spatial point precisely one cell contributes. Both sides may be infinite. The reconstruction weight `w(x)=exp(-d d(o,x))` is strictly positive and integrable because hyperbolic radial volume grows with exponent `d-1`. Hence `0 < Z_w(C) < infinity` for every full-dimensional cell, including those of infinite ordinary volume. Substituting the stated `h` integrates each selected cell weight to exactly one and proves the reconstruction formula. No absolute-integrability or moment exchange beyond nonnegative Tonelli is used.

At a deterministic origin the measure restricted to cells containing that origin has mass one and equals the zero-cell law, using the boundary-null argument. This assertion does not mean that the full mean measure is finite. Nor does the mean measure determine all correlations of the tessellation; the packet claims only recovery of this first-moment measure from location-indexed zero-cell laws.

On the finite-volume sector, center/Palm disintegration is available under the specified finite intensity. On the infinite-volume sector, an equivariant ambient probability-root disintegration is excluded by Proposition 3. Retaining the sigma-finite cell-space measure is a sound universal alternative, but it is not the sought scalar-intensity/typical-probability pair.

## 9. Degenerate and mixed-sector stress cases

The invariant one-cell tessellation `{H^d}` is allowed by the framework. It has `p_f = gamma_f = 0`, so the packet correctly declines to normalize a finite-volume Palm law. Its mean cell measure is the finite measure `delta_{H^d}`, and the incidence/reconstruction identities remain valid. An invariant ambient probability root still cannot exist. There is nevertheless a trivial unrooted shape probability, demonstrating concretely why the ambient-root obstruction must not be called a prohibition on every notion of typicality.

Mix this one-cell tessellation with probability `1-p` and an invariant ideal-triangle tiling with probability `p`, where `0<p<1`. Then `gamma_f=p/pi`, the finite-cell typical area is `pi`, and their product is `p_f=p`. This is a genuine tessellation example checking the missing-spatial-mass factor, not only a formal finite-vector normalization. Both components and their mixture are locally finite and fully invariant.

## 10. Controls, packaging, and nonblocking clarifications

The reproducible audit script uses only the Python standard library. Run it from any working directory:

`python3 audit/check_audit.py [path-to-release]`

If the optional release path is omitted, the script expects `release` beside `audit`. It verifies the pinned manifest and all seven file hashes, runs a temporary copy of the author controls, checks exact symbolic strict-convexity algebra and independent finite normalizations, and then verifies that the release remained unchanged. The receipt is written only beside the audit script.

There are no blocking corrections. Two interpretive points should remain explicit in any subsequent presentation:

1. The sufficient first-moment condition for local counts is an additional hypothesis, not a consequence of local finiteness; the finite-volume extension is conditional on positive finite reciprocal-volume intensity before Palm normalization.
2. The center-based and uniformly volume-rooted embedded laws differ, even though invariant shape observables obey the same reciprocal-volume identity.

Both are already expressed in the frozen result. The audit's extra strict-convexity calculation and measurable-kernel explanation are supporting details, not repairs to false statements.

The separate audit files contain only authored analysis, machine-readable findings, portable controls, and their receipt. They contain no source PDFs, full extracted source text, source screenshots, corpus records, credentials, or private coordination. The five entries in the research log are substantively different approaches, not five independent researchers. No remote mutation was performed.

## Final disposition

Accept this packet as rigorous, appropriately qualified partial progress. Preserve `rigorous_partial_results_original_unsolved`, the queue recommendation `unsolved`, the count `5/5`, and `novelty_claim: false`. The missing universal construction for infinite-volume cells is a mathematical limitation of the attempted approaches, not a defect that the finite arithmetic controls could resolve.
