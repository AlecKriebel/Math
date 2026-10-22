# Independent audit of percolation GFF maximum partial results

Problem 30005140, OWR-10252936-003, rank 791. Audit date: 5 October 2026 UTC.

## Verdict

PASS for the explicitly scoped finite-network identities, conditional probability bounds, and logical counterexamples. No substantive mathematical error was found in Propositions 1, 2, 3a, 3b, 4, 5a, or 5b under their written hypotheses. The actual all-supercritical-p, almost-sure quenched maximum-convergence problem remains unresolved. The five existing approaches are exhausted; this audit does not count as a sixth research approach.

The immutable author archive has 23,503 bytes and SHA-256 c3f8c9d1de2e3ff41b40a70de3cde559ff534de22b641d81a0db6db86d71f3f1. All 168 author assertions reproduce, with complete results equality. Its manifest validates all 10 listed files. The author files in this package are byte-for-byte copies of the 11 archive members, including that manifest.

A separately written standard-library verifier passes 15,108 assertions. This includes all 4,096 open/closed configurations of the 12 edges incident to a 2 by 2 lattice box: 4 interior edges and 8 exiting edges. Of these configurations, 4,080 have a nonempty grounded part and 978 have both grounded vertices and an ungrounded complement. These are finite tests, not evidence establishing an infinite-volume probability estimate.

One provenance gap is completed here. The catalog review hash is reproducible even though the research-results entry is absent, because the repository hashes the problem record together with an empty object in that case. The matching digest is 670b3821d2bd256b0a1af6c4982912082db291daf91b035626632d8bbedb002e. See CORRECTIONS_AND_CLARIFICATIONS.md. The frozen author files have not been changed.

## Model, grounding, and normalization

The model in the author README agrees with the inspected primary theorem: independent Bernoulli bond percolation on Z^2 at fixed p>1/2, the infinite open cluster, its intersection S_N with the box {0,...,N-1}^2, and zero field outside the box. The energy is one half of the sum over unoriented open edges, with each edge counted once. Thus the covariance is C=L^(-1), where L is the grounded combinatorial Laplacian. An open exiting edge contributes to the diagonal of L. A closed exiting edge does not.

Every component of S_N reaches the exterior. Starting at any of its vertices, an infinite-cluster path must leave the finite box; the path segment up to first exit supplies grounding within that component. Consequently, zero energy forces a vector to be constant on each component and zero at an exiting edge, hence zero everywhere. This proves positive definiteness. No origin-membership conditioning and no artificial single-site pin are needed. Including unrelated finite clusters without checking grounding could instead introduce a singular precision matrix.

The finite electrical identity is

    C(x,x) = R_eff(x,B) = 1 / C_eff(x,B),

where all grounded vertices B are identified electrically. To verify it, set h(y)=C(y,x)/C(x,x). Then h(x)=1, h vanishes on B, and h is harmonic away from x. Its unit-voltage energy is h^T L h=1/C(x,x), which is the effective conductance. The diagonal covariance is therefore resistance, not conductance and not chemical distance. The independent verifier checks the reciprocal identity on 180 grounded networks and includes a two-parallel-path negative control.

There is an important time-change distinction. Let D have diagonal d_x=sum_y c_xy, counting exits, and let A be the interior weighted adjacency matrix. Then L=D-A and the killed constant-speed transition matrix is P=D^(-1)A. Its raw occupation matrix is

    (I-P)^(-1) = L^(-1)D.

Therefore raw constant-speed occupation at y must be divided by d_y to yield C(x,y). The same applies to continuous-time constant-speed walk with holding rate one. The variable-speed walk with edge rates c_xy has generator -L, so its occupation kernel with respect to counting measure is directly L^(-1). These descriptions give the same GFF only with their correct reference-measure normalization. A raw constant-speed occupation matrix need not even be symmetric on an irregular graph.

At p=1, d_y=4, so covariance is one quarter of raw simple-random-walk occupation covariance. This is consistent with the author's g_1=1/(2*pi), a_1=1 and the centering

    sqrt(g_p) [2 log N - (3/4) log log N].

The audit uses a_p exactly in the primary theorem's convention. A diffusion constant from a different walk clock or speed measure cannot simply be substituted. The distinction is especially relevant when comparing literature that calls its normalized kernel a constant-speed Green function. These are clarifications, not a detected error in the author's normalization.

## Proof-by-proof audit

### Proposition 1

The average of the sparse field is N^(-1) times the sum of N independent weighted standard Gaussians. Its variance is bounded by ||f||_infinity^2/N. This gives the claimed L^2 convergence and its joint finite-test-function version. On the torus, a point mass has finite H^(-s) norm for s>1 in dimension two, and independence eliminates cross terms, giving the same order for the squared norm.

For K>=0 the maximum event has probability Phi(K log N/N)^N; the base tends to 1/2, hence the power tends to zero. For K<0, the zero-valued sites exclude the event when N>1. This is a valid centered-Gaussian, nonnegative-covariance counterexample to a continuity inference. It is not a percolation GFF counterexample and is not presented as one.

### Proposition 2

Eliminating the remaining vertices J gives the Schur complement S_epsilon on I. The variational identity minimizes the full energy over J. The old network has no positive edge from I to J, so discarding nonnegative old J energy and added-conductance energy gives S_epsilon>=L_I. Choosing the trial value zero on J gives S_epsilon<=L_I+epsilon A, with A positive semidefinite and fixed for that finite network. Thus inversion gives 0<C_epsilon<=C_0 and the two covariance bounds squeeze C_epsilon to C_0. This argument remains valid even if J was ungrounded before regularization.

The difference C_0-C_epsilon is positive semidefinite, so it is the covariance of an independent Gaussian error. The maximum changes by no more than the largest absolute coordinate error. Applying the one-dimensional Gaussian tail bound and summing over coordinates proves 2m exp[-t^2/(2 delta)]. The hypothesis delta_N log(2m_N)->0 makes this bound tend to zero for each fixed positive t and permits the stated Slutsky transfer.

The application to S_N is valid: no open edge connects the infinite cluster to a finite cluster, and each chosen component reaches the exterior. Filling every closed edge, including exits, gives a positive-conductance network. However, the theorem at fixed epsilon concerns a whole-box maximum; restriction to the random subset S_N is a real missing step. A fixed-N convergence statement also gives no uniform asymptotic estimate for a diagonal sequence epsilon_N. Both limitations are correctly retained.

### Proposition 3a

The root field and all oriented tree increments give an invertible coordinate change with unit Jacobian. The energy splits into core energy and a separate quadratic term for each increment. Consequently the increments are independent, with variance 1/c_e, independent of the unchanged core field. Shared-path covariance and the tip variance follow by addition of independent increments. The independent tests include branched trees attached to a nontrivial two-site core, not only pipes.

The one-contact and no-grounded-tree-vertex hypotheses are essential. A second attachment or a pin at a tree vertex introduces constraints between increments and changes the covariance. The author explicitly excludes these silent changes.

### Proposition 3b

The pipe event uses L distinct open horizontal edges and 2L+1 distinct closed edges. Every prescribed edge has an endpoint strictly to the left of x_1=L, whereas the half-plane connection event uses only edges within x_1>=L. Independence therefore gives exactly theta_H(p) p^L (1-p)^(2L+1). No origin conditioning or additional event has been omitted.

All pipe vertices lie strictly inside the chosen box of side 3L+1. For each non-root vertex, its only possible open neighbors on the event are its pipe neighbors. The pipe is therefore pendant in the killed network. Its tip variance is root variance plus L and is at least L. This proves the displayed lower bound for T_0. Multiplying that probability by exp[kappa(2*pi*a*L-log(3L+1))] yields an exponentially growing lower bound when 2*pi*a*kappa>lambda(p); the logarithmic correction contributes only a polynomial factor.

Thus the moment-divergence and tail-exclusion statements are correct with a strict inequality. Nothing is proved at the endpoint kappa=lambda(p)/(2*pi*a). Positivity of theta_H(p) remains an explicit hypothesis in this package. Its omission from a later statement would change that statement's scope.

This construction does not evaluate the actual optimal defect exponent. It also does not establish any comparison between lambda(p) and a_p that rules out the needed estimates at a particular p. With a=a_p, compatibility with some exponent strictly greater than 2 requires lambda(p)/(2*pi*a_p)>2. This is only a necessary compatibility test for this form of bound, not a disproof of maximum convergence.

### Proposition 4

The exact identity

    1/(s+T) - (1/s-T/s^2) = T^2 / [s^2(s+T)] >= 0

justifies the Gaussian exponential estimate. Choose eta' in (0,eta] so that r=(2+eta')^2/2 lies strictly between 2 and kappa. The uniform moment assumption then bounds each annealed tail by C N^(-r). Summing over the ambient N^2 possible vertices gives C N^(2-r), irrespective of dependence between defects or field coordinates. Missing vertices can be assigned a zero field and zero defect for this argument.

At N=2^j these bounds are summable. Tonelli applied to the quenched tail probabilities yields an almost-sure finite sum, hence convergence to zero along that subsequence. No unjustified all-N upgrade appears.

The log-log-centering calculation is also correct. At 2s-(3/4)log s+t the logarithm of the union bound equals

    (3/2)log s-2t-[(3/4)log s-t]^2/(2s),

which tends to infinity. This diagnoses failure of that upper-bound technique; it is not a lower bound on the true maximum tail. The moment assumption has not been proved for the actual field for all p, and it alone is not the full published rare-defect criterion.

### Propositions 5a and 5b

Dominated convergence for bounded continuous test functions establishes the forward implication when almost every environment has the same limiting probability law. The mixture example has an identical annealed law at every N, while independence of the environment bits gives infinitely many occurrences of each conditional variance. Their characteristic functions distinguish the two subsequential Gaussian laws, so almost-sure quenched convergence fails. The counterexample is intentionally outside the percolation model and is used only to invalidate the converse inference.

## Primary-source audit and the unresolved gap

The official [OWR report](https://doi.org/10.4171/owr/2022/27), printed pages 1535-1536, supports the recovered 2022 problem. The catalog's parenthetical 2023 does not indicate a different target.

The inspected [Schweiger-Zeitouni arXiv v1](https://arxiv.org/abs/2205.07210) has the exact energy and centering used here. Theorem 1.9 establishes (A.2)-(A.4), (B.2)-(B.3) throughout the supercritical range, but retains a near-one hypothesis for (A.1), (B.1). Question 1.10 asks about the extension; Remark 4.15 identifies difficult local resistance tails. Thus an all-p homogenization statement cannot be promoted to an all-p maximum theorem. The latter needs quantitative control on exceptional high-variance sites and covariance differences. The finite identities and conditional bounds audited here do not supply it.

[Andres-Slowik-Sokol](https://arxiv.org/abs/2508.17369), Section 1.4, does not resolve the target. Its displayed Conjecture 1.16 assumes positive conductances almost surely, and its summary of earlier percolation work should be read with the restrictions of the primary theorem. [Peter-Slowik](https://arxiv.org/abs/2605.10884), Remark 1.15(iii)-(iv), expressly reports that the available upper-bound constant and uncontrolled random-scale tails are insufficient for the missing maxima estimate. Its Sobolev and nonlinear-field limits do not repair this.

The [Chiarini-Pasqui paper](https://link.springer.com/article/10.1007/s00440-026-01529-2), published 19 August 2026, repeats the near-one 2D maximum statement around equation (6.28); its principal d>=3 hard-wall results address a different regime. All five PDFs were independently retrieved and reproduce the frozen input hashes. The full CPAM published version was not inspected; numbering here refers to arXiv v1. A bounded current search found no later full resolution. This is not a claim of exhaustive literature coverage or a proof of global unsolved status.

## Provenance and publication boundary

The complete supplied catalog, problems, and research-results files were hashed and parsed: 15,458 catalog entries, 15,458 problem entries, and 6,701 research-report entries. The unique problem identity, statement hash, and review hash match. Exact report searches found no target entry. Five broad percolation/Gaussian candidates were examined and address other targets.

Fresh read-only repository checks found no target artifact in default-branch code searches, issue/PR searches, all 814 branch names returned during the audit, or the complete 725-entry pinned problems subtree. The author's earlier count of 812 branches is historical; the audit observed 814. Non-default branch contents and complete commit history were not exhaustively inspected, so no repository-wide absence claim is made.

The package contains only authored exposition, code, replay results, manifests, and verification metadata. It contains no source PDFs, extracts, images, raw corpus records, downloaded repository response bodies, or private coordination material. No remote write was made. Hash checks establish identity; the analytic review above supplies the separate mathematical assessment. No novelty, full solution, or editorial-readiness claim is warranted.
