# Independent challenge of final provisional leaders

Audit date: 2026-09-22 UTC. Reviewer: shard 0 desk-review agent, auditing other reviewers' candidates. Scope: a bounded literature and formulation check, not five-turn proof attempts. Shard 0 is complete: 2,577/2,577 individual reviews, 100% coverage. This additional audit is complete for the assigned shortlist; mathematical solvability remains unverified. No person was contacted.

## Immediate exclusion: 2624 / Kourovka 21.115

**Exclude as already resolved in a primary preprint.** Benjamin Sambale's *On the complement of a union of cosets*, posted September 8, 2026, explicitly identifies Kourovka 21.115 in its introduction. Theorem 1 includes arbitrary left **or right** cosets and covers the group by at most 2^n translates of their nonempty complement. The finite-group density bound in our record is its stated immediate consequence. Thus this is a full-target match, not a subgroup-only or abelian special case. The paper also characterizes equality. I inspected the theorem and its finite-case proof structure; this desk audit is not a separate formal verification of the paper. [Primary full text, Theorem 1](https://arxiv.org/html/2609.09052v1).

This new source supersedes the earlier unsuccessful search recorded in LEADER_AUDIT.md. It illustrates why an old dataset label and an attractive short proof route cannot establish current novelty.

## Billiard candidates: correct the geometry and avoid counting one mechanism repeatedly

**5100025, 5100045, 5100048: repair the proposed routes before promotion.** Their review notes describe the four-periodic billiard polygon P as a rectangle; 5100048 additionally describes the outer polygon as a rhombus. The original source instead explicitly identifies **P′, the outer polygon, as the rectangle** at N=4. Its tables confirm the target constants for k804,b and k806,b, so this objection invalidates the readiness rationale, not the target identities themselves. A parameterization of the wrong polygon could prove an irrelevant special case. The antipedal centroid problem 5100025 likewise requires the correct P′ family and both specified centroid conventions. [Original paper, pages 8–11 and Tables 7–9](https://arxiv.org/pdf/2004.12497).

**5100024, 5100035–5100038, 5100064, 5100065: retain at most as a low-impact, correlated family, conditional on exact conventions.** The later journal paper already proves analogous focal-pedal area equalities by central symmetry and explicitly suggests antipedal analogues. That supports a short mechanism, but reduces likely novelty and makes these poor independent evidence for a broad AI success rate. Before an attempt, require the orbit class, primitive period, finite transformed vertices, and nonzero denominators. For an area centroid, nonzero signed area is also necessary. A zero signed area can make a ratio or centroid undefined despite a valid numerator identity. [Journal version, pages 8–9](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf).

Per-record remaining gap, based on the actual target statements:

| ID | Required check before a five-turn attempt |
|---|---|
| 5100024 | Central symmetry of the admitted outer polygon must pass through the centered antipedal construction; both vertex and area centroids must exist. |
| 5100025 | Use the outer rectangle P′; constancy of two different centroids is stronger than displaying one symmetric orbit. |
| 5100035 | Respect the N divisible by four restriction and antipedal intersections; do not replace the target by the easier pedal identity. |
| 5100036 | Confirm focal antipedal symmetry for P′, with the same vertex indexing and a defined area ratio. |
| 5100037 | Establish the appropriate symmetry of the inner tangency polygon P″; original-vertex symmetry alone is incomplete. |
| 5100038 | Combine inner-polygon symmetry with existence of every antipedal intersection; parallel defining lines are a boundary case. |
| 5100045 | Invert the actual P family, preserve signed-area conventions, and verify the unit-radius inversion normalization. |
| 5100048 | Use the correct P and P′ pair; compare corresponding focal inversions throughout the orbit family. |
| 5100064 | Focal inversion of P″ requires avoiding the inversion centers and a nonzero area denominator. |
| 5100065 | The foci belong to the elliptic locus of P′; substituting the original billiard foci changes the assertion. |

These are finite symbolic or symmetry investigations, not exhaustive-search jobs. No proof, counterexample, or claim that all exceptional configurations occur is made here. Recommendation: correct the three N=4 notes and discount duplicated impact across the symmetry cluster. A conditional candidate is justified; a certified novel easy result is not.

## 6700025: a real family requirement survives the simple pointwise intuition

Gromov's surrounding discussion specifies the standard bi-invariant metric on U(N), normalized by shortest closed geodesics of length 2π. Question 24 asks for contraction to constant maps **continuously in the input map**, not just nullhomotopy of each individual map. A fixed-basepoint logarithm is a concrete avenue, but its domain, continuity as the map varies, and the intended Lipschitz control through the contraction must be made explicit. The wording does not independently clarify every homotopy constraint. [Primary source, pages 34–35](https://www.ihes.fr/~gromov/wp-content/uploads/2018/08/101-problemsOct1-2017.pdf).

**Recommendation: retain provisionally, with moderate probability only.** The source supports a bounded proof-first route, but a familiar individual nullhomotopy would not establish the requested result. Novelty may be narrow if a standard functional-calculus lemma already supplies the family. No claim of a solution is made.

## 6000011: the dimension-two shortcut is a test, not an established solution route

The supplied target concerns integrability of every radial orthogonal distribution and one-conformal flatness of the dual statistical manifold. Rank-one distributions are automatically integrable locally, making dimension two an appropriate boundary test. That observation alone says nothing about whether the conclusion is automatic in that dimension: one must first recover the precise one-conformal equivalence and flatness definitions, their local versus global meaning, and the admissible dimensions. A proposed counterexample must satisfy the statistical compatibility assumptions as well.

**Recommendation: retain only conditionally; do not raise its solve probability on the rank-one observation alone.** The original article page was accessible, but its PDF retrieval failed during this independent audit. The earlier primary review's report that page 126 has no explicit n≥3 restriction is therefore inherited evidence, not an independently confirmed source reading here. [Original article](https://www.jstage.jst.go.jp/article/iis/4/2/4_2_125/_article).

## 20001666: substantial known content and a narrower residual target

A July 29, 2026 primary paper explicitly discusses arbitrarily large and small Maxwell eigenvalues under fixed volume, gives both cuboid degeneration families, and points to older convex-domain estimates. Its Theorem 1.2 also produces arbitrarily small eigenvalues of any fixed index near a ball in Hausdorff distance, in a broader domain class. The paper distinguishes these global facts from remaining local questions under convexity; that distinction matters for our target. [Lamberti–Provenzano–Sempio, introduction and Theorem 1.2](https://arxiv.org/html/2607.26983v1).

The thin-set paper supplies spectral convergence and examples with arbitrarily many small eigenvalues, but its abstract alone does not certify the exact smooth-convex residual. [Ferraresso–Provenzano, version 2, March 2026](https://arxiv.org/abs/2510.01846). Savo's older convex-body paper gives geometric bounds for the first differential-form eigenvalue; its degree and boundary-condition translation must be checked before it is used for all three Maxwell eigenvalues. [Author's institutional record](https://iris.uniroma1.it/handle/11573/375743).

**Recommendation: lower novelty/readiness, and require a precise remaining claim before allocating proof turns.** The original broad optimal-shape question is substantially answered by known degeneration results. Merely redoing the cuboid calculation is not a contribution. A smooth convex approximation argument might close the remaining formulation, but spectral convergence and preservation of the correct boundary-condition subspace are the actual work; calling the rounding harmless would conceal it. This audit did not verify a full theorem covering the smooth-convex first-three target, so exclusion of that exact residual is not asserted.

## Ranking consequence

Remove 2624. Repair the N=4 billiard routes and avoid treating the symmetry cluster as many independent high-impact opportunities. Keep 6700025 and 6000011 conditional on their exact source-level definitions. Reassess 20001666 after stating what remains beyond the existing global degeneration literature. None of these brief desk checks certifies a highest-possible expected-value ordering or guarantees a five-turn solution.

## Final-tail Hayman checks requested after the initial audit

The dataset summaries conflict with the source's own updates:

- **2304002 / Problem 4.2: exclude as solved.** Update 4.2 attributes the full coefficient inequality to Kristiansen, after describing earlier partial work. Constant-polynomial conventions do not create a new research contribution here.
- **2305061 / Problem 5.61: exclude as solved.** Update 5.61 explicitly credits Goldstein, Hall, Sheil-Small, and Smith with the general higher-derivative implication.
- **2304026 / Problem 4.26: retain conditionally, lower readiness.** Update 4.26 gives a coefficient-energy upper bound and two exact degrees, with general asymptotics still conjectural. The requested maximum is for arbitrary n. A finite-dimensional reformulation or another small degree does not complete it; Fejer–Riesz factorization alone transfers the optimization problem.

[Primary Hayman–Lingham PDF, printed pages 73, 79–80, and 108](https://arxiv.org/pdf/1809.07200). These are source-status corrections, not new solutions. The first two initial reviews relied on misleading imported summaries; the individual statement readings remain recorded, and root-level overrides should preserve that audit trail.
