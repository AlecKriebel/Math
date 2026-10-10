# Independent AI audit of the SIRSN exterior covering result

Problem 9700033, AMR-096-0033, rank 935. Audit date: 2026-10-06 UTC.

## Decision and exact accepted scope

**Accept the separately pinned corrected derivative as an UNSOLVED scoped partial result, with 3 of at most 5 approaches used.** The frozen author version has a sound geometric argument but leaves the measurability of its exact selected component count implicit. The correction replaces that expectation with the expectation of an explicitly measurable route-witness count. This is a technical repair, not a disproof of the author's expectation under an appropriate component-measurability formalization.

The accepted theorem is: for each fixed r>0, almost surely there is a measurable finite integer H_r>=1 and a finite measurable radius M_r such that at most H_r distinct unbounded connected components of E(infinity,r) together come within infimum distance 2r of every x with |x|>M_r. Each such component meets circle(0,2r). Moreover H_r<=N_r, where N_r is the number of E(infinity,r) intersections with that circle, and E[H_r]<=E[N_r]=8p(1).

The corrected theorem does not take the expectation of the exact number of distinct topological components. Several witnesses may occupy one component. It does not count all unbounded components, prove uniqueness, produce a SIRSN counterexample, or establish historical novelty. Fixed-r almost-sure statements may be intersected over positive rational r; no simultaneous all-real-r statement is accepted.

This audit was performed by an independent AI review pass that inspected the frozen inputs, primary sources, mathematical argument, and tests. It is not human peer review, formal proof verification, or a novelty certificate. No GitHub write was performed.

## Frozen inputs and corpus identity

The original ZIP is 10,738 bytes with SHA-256 5bd8726384871fa1f3f97543db1a88d7340d2474287f8e90feb4509a73746523. Its external manifest is 999 bytes with SHA-256 47cf2deb9dc39191fe5a7ff78aa2cef3bf245f4e9e47eae3092583e6735ea5c9. Both match the audit assignment. Every archive member matches the author's live safe-directory file. The originals remain unchanged in this audit's original directory and in AUTHOR_SAFE_FREEZE.zip.

All three full local corpus files were independently rehashed. The problems file has 15,458 records, the report map 6,701 entries, and the catalog 15,458 entries. Their sizes and SHA-256 hashes agree with the author manifest. The complete exact-ID record and report were selected afresh, serialized using the specified default json.dumps settings with sorted keys, and compared byte-for-byte with the author's canonical pair. The 4,823-byte pair has SHA-256 21b8f492c3e9bbdc7d788b8dde10d0d0d9ea6b46a947b1bf4f9447507155d8f0 and matches the catalog review hash. Rank 935, ID 9700033, and AMR-096-0033 agree. The inherited material is a literature report, not a substantive inherited mathematical proof. Its speed-scale gloss is inaccurate; the author correctly repaired that interpretation.

The accepted 3/5 approach count records the author's three substantive approaches. Audit repairs and package checks do not constitute a fourth approach. The source manifest's earlier GitHub search and queue observations remain historical author observations; this audit does not certify the current remote queue or absence of all repository history. No remote publication is part of this decision.

INPUT_BINDINGS.json records hashes, byte counts, and match results. It includes no corpus record text or dataset contents.

## Source-first verification

The three local scholarly PDFs were rehashed. Their respective 595,604-byte, 455,350-byte, and 673,770-byte copies match the author manifest. Fresh pdftotext extraction reproduces every byte of the author's saved extraction for all three PDFs. The audit additionally rendered and inspected printed pages 28, 30, and 38 of the published Aldous paper, confirming the intensity formula, the circle-crossing application, the planted-root identity, and the exact problem. These inspections use the existing local source copies; a fresh web reader opening does not establish remote PDF byte identity.

Primary source locations:

- David Aldous, Scale-invariant random spatial networks, Electronic Journal of Probability 19 (2014), paper 15, pages 1-41, https://doi.org/10.1214/EJP.v19-2920 and https://emis.de/ft/43138 . Printed pages 6-8, section 2.2, define feasible compatible routes, measurable finite-dimensional distributions, endpoint-disc removal, and the finiteness assumptions. Printed page 28, equation (6.2), gives the inverse-radius intensity. Printed pages 29-30, Proposition 6.3 and equation (6.4), give the intrinsic network and the single planted root. Printed page 38, section 8.4.2, states published Open Problem 7.
- David Aldous, long 2012 preprint, https://www.stat.berkeley.edu/~aldous/206-SNET/Papers/aldous_SIRSN_long.pdf . Printed page 49 identifies the same question as Open Problem 33. The immediately following Open Problem 34 concerns a supremum of route lengths. It is a separate target, corresponding to nearby ID 9700034.
- Jonas Kahn, Improper Poisson line process as SIRSN in any dimension, Annals of Probability 44 (2016), 2694-2725, https://doi.org/10.1214/15-AOP1032 and https://arxiv.org/abs/1503.03976 . The construction theorem concerns a specific Poisson-road model, not uniqueness of the unbounded major-road component for all SIRSNs.
- Guillaume Blanc, Nicolas Curien, Jonas Kahn, Geodesics in planar Poisson road random metric, Proceedings of the London Mathematical Society 131 (2025), e70070, https://doi.org/10.1112/plms.70070 . The readable arXiv author version at https://arxiv.org/html/2407.07887 uses the plural “roads” in its title. Its introduction, main theorem statements, and confluence section concern Kendall's particular Poisson-road metric. Neither local confluence nor absence of interior pauses states the general target here.
- Aldous's maintained page, https://www.stat.berkeley.edu/~aldous/Research/OP/sirsn.html , was reopened during this audit. It is a source index, not a current proof that every individual question remains open.

Fresh web openings succeeded for the Aldous published text, long preprint, Kahn arXiv record, Blanc-Curien-Kahn arXiv HTML, and maintained Aldous page. The publisher's bibliographic search result confirms the 2025 PLMS publication. A direct publisher full-text request timed out. The exact live UnsolvedMath URL, https://www.unsolvedmath.com/problems/9700033 , remained unavailable in the reader. The audit therefore verifies the target from the exact corpus binding and primary Aldous source, not by claiming live-site confirmation.

Searches for SIRSN unbounded-component uniqueness and the named papers did not identify a general resolution. This finite pass does not prove present literature openness or novelty. Source documents, copied extracts, raw tool responses, and source-page renderings are excluded from the safe audit package.

## Mathematical dependency audit

### The actual network and source axioms

The r parameter is a Euclidean endpoint-exclusion radius. E(lambda,r) is formed from sampled endpoint-pair routes after removing the two closed discs. E(infinity,r) is the increasing union over sample intensities. It is not defined by a speed threshold. In a particular Poisson-road model speed marks are useful, but translating a theorem about those marks into a statement about E(infinity,r) requires proof.

The proof imports the measurable route-system setup and the intensity and planted-root results of Aldous. It does not reconstruct the paper's full measure-theoretic foundations, which the source itself outlines in places. Its additional measurable operations use countably many continuous route random variables. No ergodicity, finite-energy road resampling, independent road insertion, or common coalescent geodesic family is smuggled into the proof.

### The circle bound

A radius-2r circle has length 4 pi r. Multiplication by (2/pi) and p(1)/r gives 8p(1), not 4p(1), 16p(1), or an r-dependent bound. Aldous already applies the line intersection identity to a unit circle in Proposition 6.1. The transfer to radius 2r is legitimate.

The expectation counts distinct physical intersection points, with overlapped edge portions counted as a union. A countable union of feasible route pieces has a countable segment representation. Stationarity makes the exceptional fixed-circle events involving segment endpoints, tangency, or multiple non-collinear segments negligible; directional intersection integration then gives the stated count. Finite mean yields almost-sure finiteness. Finite local edge length by itself would not justify finite intersection count for every deterministic curve or every realization; the stochastic intersection identity is essential.

### Countable samples and planted root

The space-time Poisson union is countable and dense: each bounded space-time box has finitely many points almost surely, and every planar rational ball eventually receives a point almost surely. A countable rational-ball intersection supplies density. It is unbounded for the same reason.

Equation (6.4) is an equality of the full planted-root major-road network and the original major-road network for the fixed r. Thus it handles all root-to-sample routes at once. The proof does not substitute an invalid uncountable intersection of deterministic endpoint events. The corrected proof enumerates finite Poisson shells before sorting; it does not assume the infinite plane has an earliest Poisson arrival.

### The trimmed subroute

For |xi|>4r the two closed radius-2r discs are disjoint. The first encounter with the destination disc and the last prior encounter with the origin disc exist by continuity and compactness. Between them the route stays outside both interiors. Both boundary endpoints, and the entire compact subpath, lie at least 2r from the original route endpoints. Since 2r>r, removing the closed radius-r discs does not delete either boundary endpoint or any part of the subpath.

Using the first exit from the origin disc instead would fail when a route leaves and re-enters it before reaching the destination disc. The author's last-exit formulation avoids this. The path is a finite piece of one feasible route; it is connected without needing to take a closure or a limit route.

### The measurability repair

The author's pathwise step of listing the finitely many connected components meeting the circle is legitimate as a set-theoretic statement. Its later expectation E[K] implicitly requires a measurable distinct-component count. That requirement is not supplied by the displayed proof, and the source's general random-network formalization does not explicitly prove this particular component functional measurable. The audit therefore does not silently certify it.

The derivative bypasses that issue. Enumerate the eligible sampled endpoints measurably, form their compact trimmed paths A_n, and record their circle exit points q_n. Group indices by exact equality of q_n, taking each first occurrence as a representative. There are at most N_r representatives. Each group union G_j is path-connected because all its paths share q_j.

Let a_n be the maximum distance to the origin along A_n and let b_j be the supremum of a_n over the group. Hitting times, evaluations, compact path maxima, point equalities, and countable suprema are measurable in the continuous-path model. Unboundedness is the countable event that for every positive integer L the group contains a path with a_n>L. Hence the number H_r of unbounded groups is measurable. In explicit countable-index notation it is the sum over j of the indicator that q_j first occurs at j and b_j is infinite. It is at most N_r.

The maximum radius B_r of the finitely many bounded groups, set to zero if there are none, is finite and measurable. A sampled endpoint farther than B_r+2r cannot have its trimmed path in one of those groups. There must be an unbounded group because endpoints are unbounded. Thus the unbounded groups cover all sufficiently distant sampled endpoints within distance 2r.

Each unbounded group belongs to one genuine unbounded connected component of E_r. Different groups may belong to the same component. Removing those repetitions is used only in a pathwise existence conclusion. No random component selection, component equality test, component closure, or expectation of the exact distinct-component cardinality is used. The accepted expectation is E[H_r]<=8p(1).

### Density and quantifiers

Distance to every nonempty subset is 1-Lipschitz, even when the subset is not closed and no minimizer exists. Approximate each exterior point by eligible sampled endpoints that remain exterior; then pass the inequality to the limit. This proves distance to the actual union of witness sets, so it also proves distance to their actual components. It does not add limiting points to the network.

The bound is for each fixed r. Countably many such events may be intersected, so positive rational r are covered simultaneously. A standard warning is that, for a continuously distributed random T, each fixed-r event T!=r has probability one although the intersection over all r is empty. No unsupported all-r strengthening appears in the derivative.

## Statistical countermodel and remaining approaches

The marked parallel-line process is a valid countermodel to a symmetry-and-intensity-only argument. Under (t,s)->(ct,cs), the Jacobian c^2 cancels the factor c^2 in s^2. Integrating ds/s^2 over [r,infinity) gives the offset intensity 1/r. Conditional on the direction, disjoint offsets give distinct parallel-line components. A bounded transverse interval contains finitely many offsets at fixed r. The mean number of lines meeting a radius-R disc is 2R/r; each generic line contributes two boundary points, yielding 4R/r.

The direction is a nonconstant translation-invariant random variable, so the isotropic mixture is not translation ergodic. Fixing the direction restores transverse Poisson ergodicity but loses isotropy. The author's distinctions are correct. Across all r the set of offsets is countable. A continuous path whose normal projection lies in that countable set has constant normal projection; it cannot connect different lines. No complete compatible routing is constructed. In particular the example fails the accepted exterior-covering consequence and is not a SIRSN counterexample.

Collective finite covering does not by itself imply a single component. As a separate deterministic logical check, take one square-grid half-network in y>=1 and another in y<=-1: in each half, include the vertical lines of integer x clipped to that half and the horizontal lines of integer y lying in that half. The two connected unbounded components are disjoint, their union is within distance 1 of every point, and each has locally finite length. This example lacks the SIRSN symmetries and routing axioms; its only role is to show the geometric implication from a finite coarse cover to connectedness is invalid.

A Burton-Keane strategy would need a lawful local modification and its probability, not merely an independent sample of endpoint probes. A geodesic strategy would need both a coalescing family and proof that every unbounded component contains an appropriate tail. Paths formed by switching finite routes need not be geodesics. Those missing inputs are correctly left open. No fourth approach is being claimed.

## Artifact and adversarial verification

The independent replay recreated all 21 author controls: four relocated execution modes; eight mutation types under normal and optimized Python; and the external-anchor rejection of a coherent result/certificate rewrite. All expected results were reproduced. The finite diagnostic counts in each successful verifier run were 625 scaling rectangles, 100 tail sums, 9,841 last-exit controls, and three negative mathematical controls.

Seventeen additional controls passed their specified outcomes: same-size body changes; a forged canonical hash with certificate rebinding; deliberately false corpus metadata with rebinding; duplicate JSON keys; traversal, duplicate-member, and symlink ZIPs; exact unified-patch reproduction; and four relocated modes for the corrected derivative.

One deliberate negative trust test is important: the author verifier accepts coherent rebinding of false corpus metadata, because it does not read the full datasets and was never a standalone authenticity oracle. The fixed external author pin rejects the altered package. This audit independently recomputed the real corpus hashes and canonical pair rather than relying on that internal verifier. Its README already discloses the need for an external anchor. No claim is made that an adversary who can replace both the files and the user-held trust pin can be detected.

The actual patch reproduces the corrected directory byte-for-byte when applied to the original directory. The corrected verifier passes normal, optimized, isolated, and isolated-optimized Python. The original verifier is unchanged; its limited diagnostic scope remains explicit. No finite test proves the continuous geometric theorem or makes the mathematical audit formal.

The audit's separate byte verifier requires the SHA-256 of its external manifest as an argument, checks the full explicit inventory, rejects symlinks and duplicate JSON keys, binds every file including both certificates and this report, and executes the original and corrected package verifiers. The external manifest also binds the final audit ZIP and separately identifies the corrected derivative.

## Acceptance conditions and stopping point

Use corrected/RESULT.md for the reviewed mathematical result. Keep original/RESULT.md as the unchanged frozen submission. Apply MEASURABILITY_CORRECTION.patch only to an exact copy of the original packet. ACCEPTANCE.json pins the exact accepted corrected proof, full derivative, and patch.

Recommended disposition remains UNSOLVED_SCOPED_PARTIAL, approaches_used=3, approach_limit=5. A concise findings statement is: “A finite family of unbounded E(infinity,r) components coarsely covers the exterior for each fixed r, with an explicit measurable witness count H_r of mean at most 8p(1). General component uniqueness remains unproved.”

The audit ends with that correction, exact-byte acceptance, and the identified uniqueness gap. It does not authorize a solved status, certify novelty, or substitute the auxiliary parallel-line process for a SIRSN.
