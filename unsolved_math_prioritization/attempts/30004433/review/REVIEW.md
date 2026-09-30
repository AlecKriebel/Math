# Independent review: ordinary ends in inverse-square percolation

**Verdict: PASS_CREDITED_KNOWN_CONSEQUENCE.** Under the ordinary graph-theoretic meaning of ends, the literal two-ended critical and infinitely-many-ended supercritical assertions both have negative answers. The finite-set isolation argument is valid, the classical uniqueness theorem applies at criticality, and the specified family has a genuine critical infinite cluster. No mandatory correction is requested.

Recommended campaign status: **already_solved, 0/5**, as a credited consequence of classical results with an elementary deduction, not a new discovery. This separate adversarial AI review used gpt-6-astra at xhigh reasoning on 2026-09-30. It is not human peer review or an author-approved correction to the workshop report.

## Snapshot and controls

- KNOWN_CONSEQUENCE.md: 7051efcf1d0a46c31f1c48c5926efd5bd9c9db35fb9f30d6cdd91c35615ba517
- Submitted verifier: 105f44541ce79baef090a5e38af995adef16394df07cdbad329e993f0f716e9d
- Submitted receipt: ba6f6e5f941cae00cd86fcd562470c09e39b3fadac5d9555f02377ca3a211de0
- All **1,002 submitted exact controls** reproduced with a byte-identical written receipt
- **2,303 independent exact finite diagnostics** passed

No author mathematical file was edited. The finite checks do not simulate infinite clusters or prove uniqueness, critical percolation, or the infinite-volume end count.

## 1. Original statement and meaning of ends

I read the whole Berger contribution, printed pp. 625–627, in the [official Oberwolfach report](https://ems.press/content/serial-article-files/46847), and visually inspected the model and both assertions. It specifies independent undirected edges on the integer lattice, translation-invariant symmetric probabilities strictly between zero and one, and the one-dimensional inverse-square setting for the end-count question.

Problem 2 really asks about two ends at criticality and infinitely many ends above criticality. These proposed counts are present in the original contribution, not merely in the dataset transcription. No incipient-cluster measure, directed-path convention, spanning-tree construction, or alternative definition of ends is supplied there.

The artifact explicitly uses ordinary graph ends: deletion of any finite vertex set from an infinite connected locally finite graph leaves exactly one infinite component in the one-ended case. This is the standard ray-equivalence notion. Finite-edge and finite-vertex definitions agree for locally finite graphs. Long edges drawn in an ambient line do not change this abstract graph definition.

The interpretation is a necessary scope qualification. The review does not speculate about a different invariant or law the speaker might have intended, and does not claim that an unspecified alternate meaning has been resolved. The separate triangle-condition question is untouched.

## 2. Infinite incident-edge sets and fixed cutsets

The isolation lemma is sound. Finite expected degree at every vertex makes the open graph locally finite almost surely; countability permits one common probability-one event.

For a fixed deterministic finite set $S$, its set of potential incident edges can be infinite. The proof correctly addresses this rather than invoking a finite-edge finite-energy slogan. Independence gives
\[
\mathbb P(A_S)=\prod_{e:e\cap S\ne\varnothing}(1-p_e).
\]
Summability leaves only finitely many factors with $p_e>1/2$, each strictly positive. For the rest, $\log(1-p_e)\ge-2p_e$, so the infinite product is positive. Continuity from above justifies passage from finite products to the countable event.

The event $B_S$ that the graph induced outside $S$ has at least two infinite components depends on a disjoint edge-coordinate set. It is measurable through countably many finite-path connectivity events and an exhaustion by finite vertex sets. Thus $A_S$ and $B_S$ are independent, including in the infinite product space.

If $A_S\cap B_S$ occurs, every vertex of $S$ is isolated and both outside infinite components remain distinct infinite components of the full graph. Almost-sure uniqueness therefore forces $\mathbb P(B_S)=0$. There are only countably many finite subsets of a countable vertex set, so this assertion holds simultaneously for all $S$. This also resolves the usual random-cutset issue: any finite separating set in a realization belongs to that countable collection. No random set is conditioned on as though it were deterministic.

At least one infinite component remains after a finite deletion from an infinite locally finite connected component. If the deletion meets the component, each remaining component has an edge to the deleted set; there are finitely many such edges. Only finitely many components can result, and their union is infinite. This proves existence of an infinite remaining component; uniqueness outside $S$ proves it is the only one. Local finiteness is essential at this step and has already been established.

## 3. Classical uniqueness, invariance, and critical scope

I checked the complete model setup and Proposition 1.1 on printed p. 507 of [Aizenman–Kesten–Newman 1987](https://math.bme.hu/~balint/oktatas/perkolacio/percolation_papers/aizenman_kesten_newman.pdf), including visual inspection, the introductory critical/incipient distinction, and the proof reduction on pp. 524–525.

The theorem concerns independent translation-invariant irreducible bond percolation on $\mathbb Z^d$, explicitly allowing long range. It states uniqueness almost surely whenever the origin has positive probability of belonging to an infinite cluster. The introduction explicitly includes the inverse-square critical case with positive percolation density. There is no supercritical-only restriction to add.

Every source displacement has positive edge probability, so irreducibility holds. Symmetry gives an undirected model. The product measure is translation invariant; it is also ergodic, since finite edge-coordinate cylinder events become independent under sufficiently distant shifts, and approximation by cylinder events gives the usual ergodicity argument. In any event, the exact almost-sure conclusion used here is already in AKN's theorem.

If the origin's percolation probability is zero, translation invariance and countability show that no vertex lies in an infinite cluster almost surely. If it is positive, AKN gives a unique infinite cluster almost surely. Thus the isolation lemma's at-most-one hypothesis is valid in both cases.

The displacement sum is finite for inverse-square decay in dimension one. For finite $S$, the sum of incident-edge probabilities is at most $|S|\sum_{j\ne0}p_j$. The optional exponential parametrization is legitimate: $J_j=-\log(1-p_j)$ is finite, and its tail is bounded by $2p_j$, so summability is preserved. The deduction works at each fixed parameter value, including a deterministic critical value satisfying these same assumptions. It does not assert a single common event over every parameter in an uncountable coupled family.

The imported uniqueness theorem is credited. This audit verifies its hypotheses and stated conclusion; it does not claim to reconstruct the entire free-energy argument from finite computations.

## 4. A genuine critical infinite cluster

The family in Section 4 has $p_1=t$, probabilities $1/64$ at lengths two through eight, and $p_j=1-e^{-2/j^2}$ thereafter. For every $t\in(0,1)$ it is source-admissible, and $j^2p_j\to2$.

For $t\le1/64$, its expected degree is at most
\[
2t+\frac{14}{64}+4\sum_{j=9}^\infty j^{-2}
\le\frac{16}{64}+\frac12=\frac34<1.
\]
The self-avoiding-path estimate is valid: on a self-avoiding path all edges are distinct, so its open probability is the product of its edge probabilities. Dropping the avoidance restriction only in the resulting nonnegative weighted sum bounds the expected number by $M_t^n$. This does not incorrectly treat repeated traversals of one edge as independent. Local finiteness ensures that an infinite connected cluster has simple paths of arbitrarily large length. Therefore percolation is absent throughout this interval.

I checked [Newman–Schulman 1986, Theorem 1.2](https://math.bme.hu/~balint/oktatas/perkolacio/percolation_papers/newman_schulman_1d_long_range.pdf), printed p. 549, with its preceding setup and visual statement. It fixes the longer-range probabilities and gives nonoriented percolation when the nearest-neighbor and site probabilities are sufficiently close to one, provided the inverse-square liminf exceeds one. There is no monotonicity-in-distance requirement on the finitely many shorter probabilities. Setting all sites present is the pure bond case, or follows immediately by increasing the site probability. Thus the chosen family percolates for some $t<1$, and its threshold satisfies $0<t_c<1$.

The source contribution itself discusses obtaining the transition by changing nearest-neighbor probability. Hence this one-parameter family fits its critical-case language; it is not a change to an unrelated model.

I also checked [Aizenman–Newman 1986, Proposition 1.1](https://math.bme.hu/~balint/oktatas/perkolacio/percolation_papers/aizenman_newman_1d_long_range.pdf), printed pp. 613–614, and the regularity definition on p. 612. These pages were visually inspected. In the independent translation-invariant case, regularity means every edge probability is less than one. The coefficient is the limsup of $j^2p_j$, and the conclusion for positive density is $\beta\theta^2\ge1$. Here $\beta=2$, so every $t>t_c$ has $\theta(t)\ge1/\sqrt2$.

The threshold passage is correct and uses right continuity, not left continuity. A path witnessing connection from zero out of $[-R,R]$ may be stopped at its first exit. Thus the event depends only on edges with an endpoint inside that interval. Although there are infinitely many such potential edges, only finitely many nearest-neighbor edges among them have probabilities depending on $t$. After conditioning on those finitely many variables, its probability is a polynomial in $t$; all remaining coordinates have a fixed law.

The percolation probability is the decreasing limit, or infimum, of these continuous event probabilities. It is therefore upper semicontinuous. Together with monotonicity this gives right continuity at the interior threshold. Taking $t\downarrow t_c$ yields
\[
\theta(t_c)\ge1/\sqrt2>0.
\]
Consequently the critical example is nonvacuous. Its infinite cluster exists almost surely, is unique by AKN, and has one ordinary graph end by the isolation lemma. Any parameter strictly between $t_c$ and one supplies the corresponding supercritical example.

The two renormalization results are established imported theorems. Their full PDFs were available and their relevant statements and setup were checked, but this review does not claim an independent reconstruction of their deep proofs.

## 5. Conclusions, attribution, and reproducibility

The conditional one-endedness assertion is valid throughout the stated summable independent model class. The critical family establishes actual percolation, so the negative answer does not rely on an empty collection of infinite clusters. Both literal end-count assertions fail for ordinary graph ends.

The independent finite controls check an isolation partition and probability factorization, first-exit dependence on incident coordinates, an explicit positive infinite-product model, tail bounds, and finite-parameter conditioning polynomials. For the concrete family the one-vertex isolation probability even has the useful lower bound
\[
\mathbb P(A_{\{0\}})
\ge\frac12(1-t)^2(63/64)^{14}>0,
\]
using the explicit exponential tail and $\sum_{j\ge9}j^{-2}\le1/8$. These controls do not replace the uniqueness or critical-existence theorems.

From this review directory:

    python3 independent_checks.py

Run the submitted checker inside author_replay; it writes its sibling receipt:

    cd author_replay
    python3 verify.py

All checkers use standard-library Python. The exact submitted snapshot and receipt are included.

**Final recommendation: already_solved, 0/5, for the literal ordinary-end question.** Preserve classical AKN/NS/AN attribution, the distinction from an incipient law or alternative end notion, and the absence of a novelty, published-erratum, author-endorsement, or human-peer-review claim. No mandatory correction remains.
