# Independent ranking calibration audit

Checkpoint: 2026-09-22 05:10 UTC. Reviewer: shard 1. Shard review completion: **2,576/2,576 (100%)**; ordered assignment equality and unique IDs verified. This bounded audit is complete (100% of its review scope). It does not establish any new mathematical solution.

## Scope and conclusion

Read all 50 complete statements and notes at the head of `cache/provisional_review_leaders.json`, compare representative lower-ranked proof candidates across all six ledgers, and inspect selected original statements in the catalog. Read `LEADER_AUDIT.md` and preserve its source findings. The leader snapshot is provisional: other reviewers were still completing their shards. No new literature search was performed in this audit.

The leading candidates include credible bounded proof routes, but the current ordering overstates several probabilities. Some proposed mechanisms simply name the central missing theorem. A few attractive extracted statements also omit definitions or quantifiers. These should lose queue readiness before spending five research turns. The scores remain subjective, uncalibrated estimates; this audit cannot certify a uniquely highest expected-value ordering.

## Calibration across reviewers

Candidate counts at this checkpoint (partial shards explicitly retained in the denominator):

| Shard | Records reviewed | Candidates | Candidates with p_solve ≥ .08 | Fraction of candidates |
|---|---:|---:|---:|---:|
| 0 | 2,370 | 340 | 48 | 14.1% |
| 1 | 2,576 | 330 | 37 | 11.2% |
| 2 | 2,076 | 330 | 129 | 39.1% |
| 3 | 2,520 | 203 | 13 | 6.4% |
| 4 | 2,427 | 324 | 68 | 21.0% |
| 5 | 2,576 | 448 | 194 | 43.3% |

Most reviewers use the same .03/.08 bands, but their upper-tail frequencies differ substantially. Subject composition explains some difference; these statistics do **not** justify automatic normalization by shard or collection. Record-level route comparisons below do justify corrections. The .25–.35 ellipse probabilities have more concrete symmetry or coordinate mechanisms than many .08 candidates and need not be flattened simply for being high. Their novelty and shared impact need separate treatment.

## Proposed readiness repairs

These are recommendations only; no overrides or other reviewers' files were edited. Keep existing impact unless a replacement is stated. A repaired statement may regain its previous score after verification.

| ID | Proposed correction | Specific reason |
|---|---|---|
| 30006446 | `repair`; impact 3, p_solve .03, p_valid_open .35 | The “realizations” and homological-dimension bound are undefined. Original context concerns categorification and analytic lattice homology, so a staircase/minimal-free-resolution argument may address the wrong category. Retrieve the actual bound and realization definition. |
| 30002809 | `repair`; p_valid_open .25 | All four agents coincident form an incorrect equilibrium. For positive desired distances, its transverse linearization is a positive weighted graph Laplacian: it is repelling modulo translations, not a saddle in the strict dynamical sense. Check whether the source means unstable, includes maxima in “saddle,” or excludes collapsed configurations. This is a scope check, not a claimed novel solution. |
| 30003337 | `repair`; p_valid_open .25 | The extracted random-subgraph bound omits a probability qualifier. Every finite graph has positive probability that all edges are deleted. Determine whether the intended claim concerns expectation, positive probability, or high probability before scoring its proof route. |
| 30006090 | `repair`; p_solve .03, p_valid_open .35 | A stochastic Bures–Wasserstein consensus limit needs the actual update, noise scaling, and the precise well-posedness/consensus target. A formal matrix Taylor expansion does not settle all requested conclusions. |
| 30005044 | `repair`; p_solve .08, p_valid_open .35 | The contact-process explosion question requires fitness assumptions, rate conventions, and quantifiers. A fast branching ray by itself does not control recovery or establish the full infinite-mean threshold. |
| 30004905 | `repair` pending duplicate confirmation; then canonicalize to 30006113 | The earlier “standard FVS relaxation” extraction suggests small cycle-LP witnesses; the later record explicitly identifies the Chudak–Goemans–Hochbaum–Williamson relaxation and cites the earlier workshop question. My own .08 assignment for 30004905 is too generous until the LP is identified. Do not spend independent attempts on these apparent duplicate targets. |

The exact I2 functional in 30003169 also remains a readiness requirement, already identified in the parent's source audit. Do not replace it with a convenient generic level-set functional.

## Proposed probability and scope corrections

These reductions concern full resolution in five turns, not whether a route is mathematically interesting. They apply uniformly across collections.

| ID | Proposed p_solve | Reason the current route is insufficient |
|---|---:|---|
| 4700020 | .03 | Pointwise spectral-radius contraction of absolute Jacobians does not supply a common contracting norm or global trapping argument. Constructing that norm is essentially the missing global theorem. |
| 2624 | .03 | Coset-complement induction still needs precisely the intersection estimate highlighted in the source audit. No established reduction warrants .08 merely because this is a Kourovka problem. |
| 2678 | .03 | Choosing a knot crossing the sphere does not exhibit an invariant detecting its changed isotopy class after twisting. Peripheral-data detection remains the main obstacle across arbitrary ambient manifolds. |
| 2665 | .08 | Stabilizing Seifert forms is useful, but recovering the prescribed unstabilized forms on one boundary knot is the central difficulty. The known genus-one/fixed-knot work does not complete that step. |
| 20001666 | .08 | Known cuboid degenerations leave a smooth-domain spectral transfer problem for the first three eigenvalues. Set impact to 3 if this is the precise residual target; do not count the already-known degeneration as new impact. |
| 5100026 | .08 | Symmetry constrains the even-period outer-antipedal centroid but does not itself establish its claimed phase independence. This is weaker than the direct paired-area identities nearby. |
| 6200089 | .03 | The required relative-cohomology/Garland vanishing statement is not supplied by naming the method. Triangle-of-groups stabilizers and local spectral assumptions must actually imply the needed global estimate. |
| 20001753 | .03 | Generating the lattice with Voronoi facet vectors does not give a unimodular subset. “Basis exchange” names the missing assertion unless an exchange lemma is proved. |
| 30000750 | .03 | A coefficient-norm dual argument must handle arbitrary-degree multipliers uniformly; the note does not remove this central optimization difficulty. |
| 30002437 | .01 | The factorization identity controls solutions for a fixed variable, but obtaining a uniform subpolynomial bound after summing that variable is the difficult number-theoretic step. |
| 30002508 | .03 | Hilbert-space projection may prove continuity of the approximation distance. Strict decrease also requires a nonzero residual correlation; that is the unresolved part of the bundled target. |
| 30000510 | .03 | Stabilizer stratification of the cyclic-projective configuration quotient is a starting point, not a calculation of all components and cohomology; the nonproper quotient adds substantial scope. |
| 30000700 | .03 | Logarithmic derivatives and Nevanlinna estimates do not yet control the exceptional shared-value multiplicities needed for the asserted global exponential classification. |
| 30002753 | .03 | Symmetry simplifies the random-transposition entropy Hessian, but the curvature bound must hold over all densities. The proposed representation reduction does not establish the missing uniform inequality. |
| 30003442 | .03 | Monotonicity of the largest root under stability-preserving symmetrization is essentially the desired conjecture. No independent monotonicity mechanism has been identified. |
| 7000022 | .03 | Projection and planar isoperimetry leave an average of squared projected lengths. A fixed mean length does not upper-bound that average by Jensen's inequality; the sharp geometric estimate remains missing. |

For 4700004, set impact to 2 and p_solve to .08 unless a specific workable Dulac ansatz is identified. The numerical Lie-algebra result is already known; only a new proof by the requested method could be the contribution. Preserve that method-specific scope rather than advertising a newly solved theorem.

These suggestions intentionally do not penalize every abstract proof route. For example, 30001163 has a more definite equality-case mechanism through finite invariant eigenspaces, and 30003646 has a concrete multiplicative/renewal decomposition to investigate.

## Conditional promotions from below the leader group

These deserve source/novelty checks before attempting less concrete leaders. Increased conditional solvability must **not** be interpreted as increased novelty probability.

| ID | Proposed p_solve after scope check | Concrete mechanism and remaining check |
|---|---:|---|
| 30003813 | .15 | Complement alternating coordinates in the sign-sequence polytope; each adjacent-sum constraint becomes an order inequality. This gives an order polytope, whose h*-polynomial has a linear-extension/descent interpretation. Check the source demands no stronger structure and that this standard consequence is genuinely unresolved. Retain p_valid_open .60 at most pending that check. |
| 30005325 | .15 | A support-constrained uniform-marginal coupling can be tested through Hall/Strassen-type conditions; requiring mass in each member of a countable relative base, then mixing admissible couplings, offers a route to exact support. Verify the criterion is explicit enough to answer the question and not already known. Retain p_valid_open .60 at most pending novelty review. |
| 30006217 | .15 | Given an existing finite DC decomposition, its piece count supplies a finite upper bound. Candidate max-of-affine representations with each smaller piece count can be expressed in real quantifier elimination, including global equality to the input CPWL function. This supplies a potential finite-procedure proof without executing an enormous enumeration. Check coefficient/input model, objective convention, and whether the source excludes this general algorithmic interpretation. Retain p_valid_open .60 at most pending those checks. |

Do not automatically promote the NP-hardness candidates 30003996/30003997: a named set-cover reduction still needs the gadget. Likewise, 30005718 bundles a concrete recurrence with a broader criterion, so solving only the recurrence cannot justify high full-target probability.

Representative conservative comparisons support the proposed demotions: 30001100 (mixed-integer hull intersection), 20000610 (Toeplitz-minor real-rootedness), and 20001454 (section log-concavity) already sit at .03 because uncrossing, stability, or Brascamp–Lieb would need a new central lemma. The same standard should apply to .08 leaders whose note merely names basis exchange, symmetrization, or a common norm. The .03 Kirby entries 2801 and 2863 also expose the optimism of assigning .15 to a universal knot-detection statement with no distinguishing invariant.

## Related targets and marginal impact

The focal polygon family (including 5100024, 5100035–5100038, 5100064–5100065) plausibly shares one central-inversion lemma. Give the family one initial five-turn research budget, with linked individual statuses and separate checks for primitive period, signed area, undefined centroids, and novelty. Do not add their impacts as independent discoveries. The N=4 coordinate targets 5100025, 5100045, and 5100048 may share another calculation. A .35 conditional success estimate can be reasonable for such a bounded identity while its novel/open probability remains much lower.

No collection receives an impact bonus. Age may increase significance modestly but also records resistance; the existing bounded age adjustment should not override missing scope or an unsupported proof mechanism.

Retain 30000990, 6000011, and 6700025 as provisional leaders subject to the parent's source gates. In particular, 6700025 must produce contractions continuously depending on the input map, not merely individual null-homotopies. Preserve the demotion of 30006349: its proposed rank-locus/Pfaffian mechanism is known to fail for the actual target pair. Preserve the exclusion of 30001156 from the parent's published-expansion check.

## Handoff

All shard 1 reviews are complete. This audit proposes corrections only and changes no ranking overrides. The most urgent actions are the six scope/duplicate repairs, probability reductions for routes that restate their main difficulty, and checking the three explicit lower-ranked mechanisms before allocating the next five-turn attempts.

## Primary-source follow-up on the three conditional promotions

Checkpoint: 2026-09-22 05:14 UTC. Bounded source/novelty check complete (100% of the requested three records). These findings supersede the conditional-promotion suggestions above. No proof attempt or new solution claim was made; absence of a located result is not proof of novelty.

### 30003813 — retain, do not promote yet

Recommended fields: `candidate`, impact 3, p_solve .08, p_valid_open .50.

The actual 2018 report, printed p. 1410, asks for the combinatorics of the h*-polynomial for exactly the adjacent-sum inequalities and arbitrary sign sequence in the extracted statement. It does **not** explicitly require a cyclic-order statistic or a stronger formula. Its surrounding discussion does concern cyclic-order descent refinements. The supplied literature assessment claiming the record contains no proposition is therefore erroneous. [Original report](https://publications.mfo.de/bitstream/handle/mfo/3645/OWR_2018_23.pdf?isAllowed=y&sequence=1).

The authors' subsequent paper distinguishes the signed family from the interval-sum family: Theorem 2.5 counts signed-family volume, whereas Theorem 2.9 gives the h*-formula for the interval-sum family. That latter theorem must not be cited as a solution for arbitrary signs. The paper already discusses classical poset polytopes; the proposed alternating-coordinate route therefore has substantial standard-corollary/novelty risk. No exact later signed-family solution or explicit dismissal of that route was located in this bounded search. Retain for a precise novelty check rather than treating a standard order-polytope interpretation as a new discovery. [Ayyer–Josuat-Vergès–Ramassamy, 2020, §§2.2–2.3 and 5](https://arxiv.org/html/1803.10351).

### 30005325 — exclude the extracted target as claimed solved

Recommended fields: `exclude`, impact 3, p_solve .001, p_valid_open .01. Do not promote the Hall/Strassen-plus-mixture route.

The authors' August 2026 preprint, Theorem 10, characterizes **every closed subset of the square** supporting a permuton, using compliance and shavability of occupied rational cells. Its proof combines a local positive-mass assignment, a remaining-marginal coupling, and a countable weighted mixture: this is the proposed mechanism. Theorem 11 gives the simpler compliance-plus-expansiveness criterion for regular closed sets. Thus the dataset's “partial continuous characterization” description misses the general theorem; an aesthetically simpler characterization would be a different, explicitly scoped residual task. This is a source-status exclusion, not independent certification of the entire preprint. [Coscia–Tassy–Winkler, §§3.4–3.5, Theorems 10–11](https://arxiv.org/html/2608.04135v1).

### 30006217 — promote conditionally, with exact input conventions

Recommended fields: `candidate`, retain impact 4, p_solve .15, p_valid_open .75. Queue note: “Finite max-affine representations suggest real quantifier elimination; verify coefficient representation, witness extraction, and global Pareto minimality before claiming a novel finite procedure.”

The September 2026 journal version still explicitly says no finite procedure is known for global minimal decomposition. It imposes no efficiency requirement in that statement. Definition 4.11 uses **Pareto minimality of the pair of piece counts**, not an unspecified single scalar objective; existing vertex enumeration is relative to a fixed compatible complex. The quantifier-elimination mechanism is not mentioned in the checked paper, and targeted searches located no prior use resolving this exact task. That supports a bounded attempt, not a claim that the mechanism works or is novel. Input coefficients must have a stated exact representation; the current general real-coefficient wording does not itself define a Turing input model. [Brandenburg–Grillo–Hertrich, introduction, §2.2, Definition 4.11 and Theorem 4.12](https://link.springer.com/article/10.1007/s00454-026-00875-1).

This promotion is for proving an algorithmic existence/result without running a huge search. If a satisfactory answer instead requires executing a large quantifier-elimination instance, it fails the user's proof-first resource constraint and should be deferred.
