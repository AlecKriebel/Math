# Independent audit of adaptive transport approximation

## Decision

Accept the frozen packet as five mathematically valid, explicitly scoped partial or conditional approaches. No blocking proof correction is required. Retain problem 30002760 / OWR-13487-001, rank 990, as `unsolved`, with `5/5` author approaches. This decision concerns the packet's unresolved broad target; it is not a claim that the literature contains no solution to any interpretation of the 2015 question.

The substantial affirmative stationary result of Erath and Praetorius remains essential: it cannot be erased by the packet's counterexamples, and cannot be promoted into a general parabolic or parameter-uniform preasymptotic theorem. The abstract hypotheses in Approaches 3 and 4 and the certification requirement in Approach 2 have not been established for the full source problem. The packet already states those limitations.

This is an independent AI-assisted mathematical and computational audit, not formal verification or human peer review. No publication, repository mutation, source-document redistribution, or original-packet edit was performed.

## Object and integrity

The reviewed object contains 18 bound files plus `FROZEN_MANIFEST.json`. Its externally supplied SHA-256 is:

`6881ffec2ec0cdf4c44f9aa0a1b5155efe171d31e4b801f21961afaa9166a260`

The digest matches. All 18 lengths and hashes match; the directory contains exactly the bound files and manifest. The reviewer read the five mathematical reports, all accompanying qualifications, numerical claims, attempt ledger, prior-attempt summary, source metadata, and all four verification programs. The audit's independent checker pins this digest and uses its own explicit 18-file allowlist.

This audit is separate from the reviewed directory. Its source-free deliverables contain authored analysis, programs, receipts, public source identities, and hashes only. No source PDFs, extracted third-party texts, corpus entries, screenshots, or private coordination material are included.

## Primary source and literature scope

### Original question

The organizers' introduction on printed page 88 of the 2015 Oberwolfach report asks whether adaptive finite-element approximation for elliptic or parabolic transport-dominated diffusion achieves the rate available from best partitions in a refinement family such as newest-vertex bisection. Its adjacent anisotropy discussion concerns a different benchmark: the limitations of isotropic approximation as the Péclet number grows. The question leaves important conventions unspecified. In particular, parameter-uniform preasymptotic constants are not an explicit quantifier in that passage. The packet handles this distinction correctly. The original source and inspected introductory context were independently checked. [Publisher report](https://ems.press/content/serial-article-files/46549), DOI 10.4171/OWR/2015/2.

### Erath and Praetorius

The 2019 journal citation is verified. Theorems 4.4–4.5 give eventual linear estimator convergence and asymptotic algebraic optimality; Remark 4.6 compares with energy error plus oscillation. Conditions include fixed positive diffusion, polygonal Lipschitz domain in dimension at least two, boundary-resolving shape-regular conforming fixed-degree elements, and the stated algorithm. Dirichlet data are homogeneous; inflow lies in the positive-measure Dirichlet boundary. Alpha is W^{1,infinity}, beta bounded, f and g square-integrable; -div(alpha)/2+beta >= gamma and ||beta|| <= c_beta gamma. When gamma=0, the stated branch assumes divergence-free transport. Stabilization follows (15), with constants satisfying (12) or (14), as Section 2.5 requires. Optimal rates require 0 < theta < (1+C_stb^2 C_drl^2)^-1, near-minimal marking, largest-element enlargement, and NVB. Section 4.2 explicitly limits robustness; onset and constants are not uniform preasymptotic guarantees. The reviewer inspected text pages 2–16, the page-14 raster, and online metadata. The manuscript's internal July 28, 2021 date is distinguished from journal publication. [Manuscript and journal metadata](https://arxiv.org/abs/1806.11000).

### Parabolic developments

Stevenson and Westerdiep's September 2021 v2 addresses asymmetric spatial operators. Its introduction distinguishes ordinary discrete stability, stronger operator-uniform energy estimates, and still stronger estimator conditions. Such same-space quasi-optimality alone is not adaptive best-mesh rate optimality. The packet imports no uninspected proof. The reviewer independently checked the introduction and version metadata. [Primary manuscript](https://arxiv.org/abs/2106.01090).

Feischl, Henríquez and Niederkofler's May 29, 2026 v2 studies adaptive time stepping for a finite-dimensional Gelfand triple with an elliptic self-adjoint spatial operator. Its complexity measure is the number of time steps. The inspected model does not justify a statement for arbitrary nonsymmetric convection operators or joint spatial NVB complexity. No journal acceptance was verified. [Primary manuscript](https://arxiv.org/abs/2512.05676).

Gantner, Smeets and Stevenson's September 2026 v1 explains the stability difficulty on general nonslab partitions and a data-dependent test-enrichment condition. Its introduction expressly qualifies the certified residual-lift estimator's auxiliary-mesh complexity and the lack of a guaranteed upper bound for a cheaper surrogate. The packet reports those qualifications accurately. No journal acceptance was verified. [Primary manuscript](https://arxiv.org/abs/2609.01748).

The credited methodological precedents are real and appropriately attributed: [Cohen, Dahmen and Welper, 2012](https://www.numdam.org/articles/10.1051/m2an/2012003/) and [Carstensen, Feischl, Page and Praetorius, Axioms of Adaptivity](https://arxiv.org/abs/1312.1171). Their complete proofs are not treated as newly audited imports. The packet reconstructs the elementary arguments that it uses.

These are targeted source checks as of October 7, 2026. They do not certify an exhaustive present-day literature search. The source's historical open-question label and a dataset classification cannot settle current mathematical status. Recorded author retrieval and inspection history is provenance, not a historical event independently provable from a hash; the review's own reads, byte checks, fresh extraction, and online checks provide separate present evidence.

## Complete proof audit

### Approach 1

Proposition 1.1 is a valid Céa estimate. Galerkin orthogonality permits replacement of the second argument e by u-w because the difference lies in the trial space. Coercivity and continuity then give alpha ||e||^2 <= M ||e|| ||u-w||. The zero-error case is handled without division. Finite-dimensional solvability follows from coercivity when needed. No mesh selector is constructed or presumed to follow from this estimate.

Proposition 1.2 is an actual conforming one-element quadratic example, not a matrix model mislabeled as FEM. Both phi and psi vanish at the endpoints; the trial space is exactly the span of phi. Independent polynomial integration gives P=1/3, S=1/20, the derivative cross term zero, and the convection cross term 1/60. The trial coefficient is positive, 1/(20 epsilon). Energy orthogonality makes zero the best trial approximation, but does not make the Galerkin solution zero. The squared error-to-best-error ratio is exactly 1+1/(60 epsilon^2).

The bilinear form is coercive in the epsilon-weighted energy norm because the self-convection integral vanishes. The polynomial forcing depends on epsilon, legitimately for a uniform-in-data same-space inequality. The example does not disprove fixed-epsilon convergence rates, stabilized methods, sufficiently fine-mesh behavior, or existence of a successful adaptive algorithm. The packet's scope is correct.

### Approach 2

Proposition 2.1 is valid for the boundedly invertible linear operator B in the Hilbert-space setup. Reflexivity identifies the adjoint domain correctly, B* is invertible, and R_X^-1 B* defines an onto isometry after the equivalent test norm is imposed. The displayed identity b(w,v)=(w,Tv)_X yields the full dual-residual identity by Cauchy–Schwarz and the choice T v=u-w. It also covers zero error. Minimization over the finite-dimensional trial subspace is precisely orthogonal projection. This is an ideal norm construction, not an algorithm for evaluating that norm.

Proposition 2.2 correctly projects the error into Z=T(Y_T). Positive beta makes P_Z injective on U. Because P_Z U is finite-dimensional, the least-squares minimizer exists and is unique. Its projected image is the orthogonal projection of P_Z u. Therefore P_Z(u_T-w) is the projection of P_Z(u-w) onto P_Z U, with norm at most ||u-w||. Dividing by beta and using the triangle inequality proves the stated, intentionally non-sharp factor 1+beta^-1. The Fortin calculation bounds the continuous supremum by C_F times the restricted one, giving beta >= C_F^-1 in the correct direction. No best-mesh selection follows from these assertions.

Proposition 2.3 is an exact orthogonal decomposition. The tail condition is separately stated, so no circular certificate is smuggled into the proof: it is not proved merely by a stable trial/test solve. The R^2 example has beta=C_F=1, restricted residual zero, error one, and hidden tail one. It genuinely defeats the proposed estimator inference while leaving the same-space quasi-optimality theorem intact. Test-norm construction, tail certification, enrichment complexity, and trial selection remain unproved PDE-specific obligations.

### Approach 3

Proposition 3.1 uses finiteness for existence of budget minima, nestedness for E(S_k)<=E(P_k), and the overlay cardinality estimate separately. Summing budgets gives m(S_k)<=2^{k+1}-1. Score equivalence and selection imply E(P_k)<=lambda(C/c)E_{2^k}; quasi-optimal solution transfer introduces Q. The inequality m(S_k)+1<=2(2^k+1) has the correct orientation for converting the budget error into the stated 2^s cardinality factor. This holds for s>0 and includes zero errors without inverse-error expressions.

An effectively enumerable family and scores with terminating certified comparisons would make the selection step a finite computation. The packet correctly warns that arbitrary computable real scores do not provide exact comparison or zero testing. The two-sided score equivalence, selection oracle, and discrete-solve constant are conditional assumptions, not conclusions derived from the unknown exact solution. This is no circular proof of the source problem because those assumptions are explicitly left open.

Proposition 3.2 is valid for binary midpoint interval refinement. Terminal dyadic leaves determine the ancestral split tree uniquely, so different full ordered trees give different partitions. The Catalan recurrence follows by the left/right split. For N>=2 the two endpoint terms are distinct and imply C_N>=2 C_{N-1}, establishing the stated exponential lower bound. It is a lower bound on literal candidate enumeration, not on every approximation algorithm. The independent controls also generate the leaf-address partitions directly, without reusing the recurrence.

### Approach 4

All necessary logical assumptions are exposed: a finite refinement family and overlay estimate, localized discrete reliability, stability on unchanged elements, quasi-monotonicity, bounded-factor minimal Dörfler marking, mesh closure, and R-linear estimator convergence. The theorem assumes those properties for its sequence from level zero. It does not quietly substitute an eventual literature theorem for that stronger sequence-wide hypothesis.

Lemma 4.1 is correct. R contains every removed element, so T minus R is genuinely shared with H. Stability, discrete reliability and eta_H<=kappa eta_T imply 1<=r^2+(kappa+a r)^2. This expression is nondecreasing for r>=0. The strict bound on kappa and theta makes its value at sqrt(theta) less than one, contradicting r^2<theta. The endpoint observation in the packet is harmless; the desired marking conclusion is non-strict.

Theorem 4.2 is correct. Under positive indicators, A_s is positive. Since the root mesh is the sole budget-zero refinement, eta_l<=C_M eta_0<=C_M A_s. Consequently z=(C_M A_s/(kappa eta_l))^{1/s}>1. The choice N=ceil(z)-1 is an integer with 1<=N<=z and N+1>=z. A finite-family comparator mesh P exists. The overlay H has #H-#T_l<=N and eta_H<=C_M eta_P<=kappa eta_l. Lemma 4.1 and minimality then yield the marking-cardinality estimate.

The inverse-error step has the correct direction: eta_l<=C_lin q^{l-j} eta_j implies eta_j^{-1/s}<=C_lin^{1/s}q^{(l-j)/s}eta_l^{-1/s}. Mesh closure and the geometric sum prove the claimed constant; replacing the sum by 1/(1-q^{1/s}) merely overestimates it. Reliability is not needed to prove estimator optimality; it is needed to transfer that upper rate to solution error. Identification with a best-solution approximation class additionally needs efficiency/oscillation information. These distinctions are preserved.

The zero-estimator exit is explicitly a terminating case. Reliability then makes the certified error zero, without inverse-error expressions. Proposition 4.3 correctly shows that plain decay to zero, even with the proposed per-step marking bound, does not imply the desired rate versus cumulative complexity. Here complexity is quadratic in l, error is reciprocal-linear in l, and their product grows unboundedly. This is an abstract numerical counterexample, as labeled.

There is no circularity in the conditional theorem. Its application to the broad transport/parabolic problem would be incomplete until the listed hypotheses, including robustness of their constants if requested, are independently established. The packet explicitly acknowledges that gap.

### Approach 5

Proposition 5.1 is valid in the stated real Gelfand triple and time-Sobolev class, with bounded measurable bilinear forms and unit coercivity in the V norm. The energy identity gives an absolutely continuous H-norm square and continuous H-valued traces. Pairing e'+Ae=r with e and applying Young's inequality gives the estimate after integration. The smooth-approximation argument and trace continuity justify its use beyond smooth solutions.

The subsequent bound for the sum of a time supremum and the full-time integral correctly uses factor two. One cannot in general replace it by one simply by taking the supremum in the earlier joint inequality. The packet does not do so. A genuinely skew convection term contributes nothing to a(v,v); parameter dependence can remain in the chosen V norm and its comparison with other norms. Time-discontinuous approximations require reconstruction or jump terms, exactly as stated.

Proposition 5.2 is a global optimization proof for positive b_i, p, N and allocations, not merely a first-order stationarity argument. Hölder's exponents are conjugate and its factors multiply to b_i^{1/(p+1)}. Rearranging proves the lower bound; the proposed allocation attains it. Upward rounding decreases every error term and increases the total by less than M. With integer L>=2M, N=L-M gives positive integers with sum at most L and factor at most 2^p versus the real-budget benchmark. The statement is a fixed-M separable model. It neither certifies the model weights nor hides temporal, transfer, enrichment, or growing-M costs.

Proposition 5.3 is correct in the bounded linear coercive spatial setting inherited from the preceding energy proposition. The one-step backward-Euler right-hand side is f(1)=2 phi+A phi. Subtracting the exact endpoint phi leaves (I+A)w=phi in variational form. Coercivity gives unique solvability, and w=0 would contradict testing the right-hand side with the nonzero phi. The scalar endpoint 3/2 and squared error 1/4 are exact. A spatial approximation converging to this fixed discrete-time solution cannot converge to the distinct continuous endpoint. This defeats spatial-only convergence on an unrefined time grid, not a properly time-adaptive method.

## Checker audit and independent controls

The original exact arithmetic checker produces 37,329 checks, with groups 9, 309, 1,621, 2,015, 7,674 and 25,701 for schema and Approaches 1–5. The total matches the group sum. The stored mathematical, fail-closed, and integrity receipts are reproduced exactly.

All full packet runs under normal Python, `-O`, and `-OO` succeed, with identical output digests. All validation conditions use explicit exceptions or process status, and AST inspection finds no optimizable assertion statements in the four original programs.

The original fail-closed suite rejects, across its three modes, 30 false numerical claim cases, nine wrong-computation cases, and nine malformed/unsupported-claim cases. These are repeated mode executions of ten, three, and three distinct cases respectively, not 48 distinct mathematical mechanisms. Its duplicate-key hook prevents a duplicate from silently replacing a value. Integer identity/count fields reject booleans and non-integers where expressly checked; rational claims require strings and are parsed exactly. Unsupported solved promotion is rejected.

The original integrity suite rejects 24 mutations: eight distinct cases in three modes. Those cases cover changed bytes, missing/extra files, wrong sizes/hashes, directories, symlinks, and duplicate manifest keys. A manifest plus its files cannot authenticate itself against coordinated malicious replacement; the separately retained digest is necessary. The packet states that limitation.

One implementation detail matters when interpreting mode coverage: `verify_packet.py` launches some child programs without forwarding its own optimization flags. This does not invalidate the advertised result because the called negative-test programs themselves explicitly execute normal, `-O`, and `-OO` children. The independent audit also directly replays the mathematical checker in all three modes.

The independent program does not import the reviewed implementation. It uses separately written exact computations for polynomial FEM integrals, general stable oblique projections, direct dyadic leaf-address enumeration, rate-factor orientation, marking inequalities, geometric sums, allocation optima and rounding, polynomial parabolic energy bounds, and nonsymmetric coercive backward-Euler errors. It also mutates all 23 numerical claim leaves, adds 16 malformed/schema/type cases, and applies four fresh computation edits in each interpreter mode. Its final receipt records the exact checks and mode results; the suite itself is rerun under normal, `-O`, and `-OO`.

These computations test representative finite algebra, not the truth of general infinite-dimensional hypotheses. Some checks intentionally confirm elementary identities. Neither a high control count nor successful mutation rejection replaces the analytic audit above, establishes complete adversarial coverage, or proves the source problem solved.

## Provenance and boundaries

All five PDF bindings, five extracted-text bindings, two raster bindings, and two public dataset bindings match the packet metadata. Fresh `pdftotext -layout` extraction from every PDF reproduces the recorded extracted-text bytes. The source identities and relevant arXiv version/publication metadata were independently checked online. Detailed source-binding and extraction receipts are included as metadata only.

The original prior-attempt report is appropriately bounded to its visible repository/artifact search coverage. This review does not claim to have independently rerun all 984-branch and all-state PR searches. Neither its search findings nor the present audit prove absence of unpublished, inaccessible, differently identified, or future work. The author ledger lists five distinct approaches; lookup, packaging, and independent audit do not add mathematical approaches.

The overall unresolved disposition is justified by the packet's explicit gaps, not by declaring the positive stationary theorem irrelevant or treating a restricted obstruction as a universal impossibility result. No assertion of novelty or full-source resolution is accepted.

## Corrections and acceptance boundary

No mandatory mathematical, computational, or provenance correction was found. Two optional clarifications are supplied separately for future presentation: spell out the stationary theorem's small-marking-parameter restriction in the short source summary, and explicitly repeat bounded linearity in Proposition 5.3 so its inherited standing assumptions are unmistakable. Neither changes the proofs or disposition.

Acceptance is limited to the externally pinned packet, its stated scoped claims, and the audit evidence described here. It does not approve any future claim expansion, changed proof, source-document publication, or promotion to `solved` without further review.
