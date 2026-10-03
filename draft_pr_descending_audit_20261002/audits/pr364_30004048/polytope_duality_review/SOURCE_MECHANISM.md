# Independent source and mechanism checkpoint

Author: adversarial LP / polytopes / weighted-duality reviewer. This document was written before reading the candidate, its programs, histories, queue, PR body, or other review families. Target conclusions are hypotheses.

## Source receipt

Fresh downloads on 2026-10-03 UTC, retained privately. Exact URLs are those in the original `SOURCE_MANIFEST.json`, which was the only candidate routing file read before this checkpoint. Fresh byte counts and SHA256 match all three pins:

| Source | Bytes | SHA256 |
|---|---:|---|
| OWR 1/2019, exact Seymour contribution printed 46–47 / PDF 42–43 | 531122 | `66495150dd3e51e3c59fbb6ffe3d2c618b0214f788d7c50d476e5d99202f9c5c` |
| arXiv 1902.10878v3 | 509798 | `b4624846a9e536b72f404adf2cc07e71a681d93c0641fe94739f162741311ab4` |
| EJC 29(2) (2022), P2.47 | 1658799 | `000f8166ae81985e6a1144ba7c161911496ead3c597ca8fc24ed29353069d3fa` |

Read scopes: OWR complete Seymour contribution; both papers' definitions, weighted theorem 2.1, complete LP lemma 2.2 and symmetry proof 2.3, adjacent caveat, 2.4–2.5, full 4.1–4.5, and 12.1–12.2. The published triangular-star description following 2.5 and v3 4.6 were also read. Published 4.5 has an apparent units/typesetting error `w(N(v)) >= y|B'|`; normalized weights require `>= y`. This is a source-level concern, not a candidate finding.

Visual checks: OWR PDF43 confirms `x+ky>1`, `kx+y>=1` and the exact universal symmetry question. Published PDF8–10 confirms nonnegative weights, all four non-strict degree constraints, strict `<z` for the weighted-to-finite contradiction, LP primal `Mq>=1` and dual `p^T M<=1^T`, positivity of every retained B weight, and the explicit caveat for the biconstrained case. Published PDF18 confirms the fraction in 4.1. v3 PDF8 (printed6) confirms its terminal `phi(y,z)<=z` is a typographical variable error corrected to `phi(y,x)<=z` in the published version. Whole PDFs, extracted text and render images stay private.

## Exact target and matrix model

For each finite tripartite graph with no A–C edges, use binary matrices M (A by B) and N (B by C). Let R be the Boolean product: `R_ij=1` iff some B vertex gives an A_i–B–C_j path. With normalized vectors a,b,c >= 0 and each sum equal to 1, biconstraints are

`M b >= x 1_A`, `M^T a >= x 1_B`, `N c >= y 1_B`, `N^T b >= y 1_C`.

The reverse two-step target is `max_j (R^T a)_j`. The source question is whether the infimum of this maximum over all finite biconstrained graphs equals the corresponding infimum after exchanging x and y. Reversal swaps M,N and a,c and preserves the degree class; it does not preserve the maximum column mass objective pointwise. Different directional maxima in a single graph are not a disproof of the infimum equality.

For fixed M,N, feasibility splits into an a-polytope, a coupled b-polytope and a c-polytope. The objective can be minimized by an LP with a,t and `R^T a <= t 1_C`. All fixed-size feasible sets with nonnegative weights and normalized masses are compact. Compactness at a fixed topology does not prove attainment over unbounded graph sizes. The maximum guaranteed z exists simply because an infimum is a lower bound on every individual graph; an extremal witness attaining the infimum does not follow.

## Duality mechanism and obstruction

Lemma 2.2 is a covering LP with primal `min 1^T q`, `Mq>=1`, `q>=0`; dual `max 1^T p`, `M^T p<=1`, `p>=0`. Equal objectives and feasibility imply complementary slackness. After normalization by their common positive objective, the reversed degree equals the optimized degree only for columns with positive primal weight. Minimal support supplies this positivity in the one-direction proof. Zero columns cannot simply be ignored while retaining their vertices and applying the conclusion to all vertices.

Exact control: with M rows `(1,1)` and `(1,0)`, q=(1,0), p=(0,1) are feasible with objective1. The normalized reversed degrees are (1,0). The unsupported claim that all reversed degrees equal1 is false; the second primal coordinate is zero.

In the biconstrained setting, optimizing B weights for M alone can break `N^T b>=y`. Exact all-positive control: M is the 2 by 2 identity; N has rows `(1,1)` and `(1,0)`; x=2/5, y=3/5; a=(1/2,1/2), b=(3/5,2/5), c=(3/5,2/5). This is biconstrained. The unique max-min optimizer for M is b'=(1/2,1/2), which breaks the second C vertex's y-degree. Its max two-step objective is1, so this is an obstruction to the transferred mechanism, not a counterexample to symmetry.

Similarly, reweighting A to optimize complement two-step constraints can violate `M^T a>=x`, and reweighting C can violate `N c>=y`. The source proof deliberately has only one constrained direction for each reweighting. A simultaneous polytope reweighting theorem would carry the central unproved difficulty; the route is blocked unless a new mechanism supplies that theorem or a genuine separation certificate.

## Rationality, finite realization and boundaries

For rational x,y, choose rational t below the target z but above a proposed strict witness maximum. A feasible system with rational coefficients and rational right-hand sides has a rational point; a rational vertex argument or Gaussian elimination on a feasible face makes this checkable. Common-denominator blowup then creates an exact finite unweighted graph. All four degree ratios and two-step maxima must be recomputed in that realization. Zero-weight vertices may be removed; removing zero B vertices can only delete paths. Each part remains nonempty because its total mass is1.

Rounding weights coordinatewise, even while maintaining sums, can violate a saturated non-strict constraint. An LP with irrational right-hand sides need not contain rational points on its exact feasible face: `b1>=x`, `b2>=y`, `b1+b2=1`, `x+y=1` forces b1=x if x is irrational. This generic example does not by itself disprove source 2.1, since a strict two-step witness can impose further structure. Its brief rationality assertion must not be treated as a general approximation theorem for every simultaneous boundary. Exact rational candidate parameters and exact blowups avoid this gap.

The start of source 2.3 assumes a witness at z=phi(x,y). For purposes of a checkable proof, replace this with arbitrary threshold z>phi(x,y), choose an actual graph with objective<z, minimize its support within the threshold class, run the support argument, and take z down to phi. This avoids assuming the global infimum is attained. It still cannot transfer to psi because of the coupled constraints above.

Rotation of triangular triples rotates the asterisk constraints as well. `(x*,y*,z)` rotated is `(z,x*,y*)`; it is not generally the unstarred or a differently starred instance used to identify psi with exchanged arguments. A proposed proof must carry every bidirectional requirement through the rotation.

## Candidate routes to falsify or verify

1. A candidate disproof can use exact rational finite upper certificates for suitable arguments together with a rigorous universal reversed lower bound separated by a strict rational gap. If it proves only that universal symmetry cannot hold, it must not claim a particular directed ordering or exact psi value without additional proof.
2. A counting or extremal argument could refute universal symmetry without identifying an ordered pair, but needs exact independent deductions from the degree and reachability polytopes and source theorem hypotheses.
3. A symmetry proof based only on source2.2, reversal, complement or unstarred rotation is blocked by simultaneous constraints unless independently strengthened.
4. Finite searches or rational LP feasibility are evidence about enumerated topologies, not universal lower bounds or claims about all graph sizes.

Success criteria for this family: independently check the candidate's quantified conclusion, the exact normalization and every dual/separation certificate, finite realization, boundaries, and absence of an unsupported infimum-attainment step. No conclusion about novelty or all later literature is available from these sources alone.

Checkpoint completion estimate: 20% toward this audit family's full review; source mechanism complete, candidate and execution audit not yet begun.
