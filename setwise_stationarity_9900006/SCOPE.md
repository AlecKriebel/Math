# Scope and acceptance report

Date: 2026-10-20. Problem ID 9900006, AMR-098-0006, Thorisson Problem 3.2. Final disposition: **partial mathematical results; UNSOLVED, 5/5 attempts** for the named problem. The auxiliary-copy equivalence below is proved, not an unproved proposal.

## Original target

Thorisson's public preprint, *Some Open Probability Problems*, Section 3, pp. 3–4, considers two processes in an arbitrary measurable state space. Problem 3.1 asks whether full-path setwise convergence of the shifted law to a stationary law implies full-path total-variation convergence. Conditional on a negative answer, Problem 3.2 asks for a coupling characterization of that setwise convergence. Problem 3.3 concerns a different, weak-convergence question. Exact wording and numbering were checked in the public preprint, not independently in the final journal PDF. See [SOURCES.md](SOURCES.md).

Write S=E^{N₀}, Σ=ℰ^{⊗N₀}, μ=Law(X), θ(x)_k=x_{k+1}, and μ_n=θ^n_*μ. The target convergence is μ_n(A)→ν(A) for every fixed A∈Σ. Such A can depend on infinitely many coordinates. It is not enough to test cylinders or one-coordinate marginals. The limit is automatically stationary: apply convergence to A and θ^{-1}A and compare the shifted index sequence. Total variation is normalized as sup_A|μ_n(A)−ν(A)|.

The source's surrounding theorems concern exact and shift couplings of two processes, but Problem 3.2 itself does not expressly prohibit auxiliary copies or impose a formal single-pair syntax. Treating one pair as an explicit source hypothesis would overstate the text.

## Accepted mathematical results

### General auxiliary-copy characterization

Attempt 3 proves, on every measurable space, the equivalence of full setwise convergence, arbitrarily accurate finite tail convex combinations along every deterministic subsequence, and an explicit random-time coupling preserving one original orbit.

For each subsequence 0≤n_1<n_2<..., one probability space carries X, all K_j, all Y_j, and all measurable H_j. The K_j have finite deterministic supports contained in {j,j+1,...}, and the entire sequence is independent of X. Each Y_j has law ν. Pointwise equality θ^{n_{K_j}}X=Y_j holds on H_j, whose failure probability is at most 2^{-j}. Hence equality is eventual on a measurable full-probability event.

This is a genuine broad literal coupling characterization of exactly the stated convergence. It is neither restricted to standard Borel spaces nor merely a partition-by-partition restatement. Stationarity is needed for the path-space interpretation of the comparison laws, not for the analytic convexification and common-part construction themselves.

### Neighboring implication and one aligned-pair candidate

Attempt 1 gives a self-contained Bernoulli-orbit example with full-path setwise convergence and TV distance identically 1/2. Its proof handles every measurable path event through a measurable orbit pullback and finite-coordinate approximation. This is a negative answer to neighboring Problem 3.1 under the source's assumptions. It does not answer Problem 3.2 by substitution, and no priority claim is attached.

That example admits one coupling satisfying the aligned-pair property

    SC: for every A∈Σ, P(1_A(θ^nX)≠1_A(θ^nX′))→0.

SC is sufficient for setwise convergence when X′ is stationary. The example only shows that SC can hold while TV convergence and distributional exact coupling fail; it does not prove a reverse implication from either stronger-looking property to SC.

Attempt 2 proves that SC is not necessary in general. Its arbitrary-bistochastic rank-one rigidity lemma is proved in the text and checked in AUDIT.md. Explicit staircase parameters satisfy a cited primary-source mixing theorem. This refutes this particular aligned-pair criterion even on a standard nonatomic state space. It is not a theorem that every two-process coupling formulation is impossible.

### Other accepted results

- COUPLING_CRITERIA.md characterizes setwise convergence by one freely recoupled sequence under separability of the control-measure algebra. The variables need not retain the joint law of successive shifts of an original process. Its unrestricted converse is valid; its forward proof is not claimed for nonseparable measure algebras.
- Attempt 4 rules out a common unshifted target under the specified independent random times, even for stationary iid Bernoulli paths. It also proves that one aligned pair fixed before every subsequence, with independent common-time randomization, is equivalent to SC. In that randomized interpretation the times must be independent of the entire pair (X,X′), not just X.
- Attempt 5 shows that considering only the original time sequence would wrongly accept an alternating orbit. It also shows that the Bernoulli example needs growing random-time supports: a mixture supported on m distinct times has TV distance at least 1/(2√(3m)), with equal weights giving at most 1/(2√m). These restrictions concern this particular independent-random-time format, not all possible characterizations.

## What is not claimed

- One construction simultaneously chosen for every deterministic subsequence, or a choice measurable in the subsequence.
- One stationary orbit supplying all the comparison variables Y_j.
- Independence of the Y_j, or independence of K_j from Y_j or H_j.
- A finite exact or distributional coupling time in the source's specific sense.
- Necessity of SC, which is disproved; impossibility of all other two-process formulations, which is not proved.
- A full unqualified resolution, novelty, literature priority, expert acceptance, or peer-reviewed status for the named problem.
- Verification of the inaccessible 2026 SSRN manuscript mentioned in SOURCES.md.

The construction can change with the subsequence but not with a test event. The explicit success flag avoids diagonal-measurability assumptions by defining Y_j pointwise by cases. It is stronger than an event-by-event choice of coupling, while remaining different from a single original-process/stationary-process pair.

## Audit corrections applied

1. Attempt 1's unsupported “strictly weaker” wording had already been replaced by the one-way example statement and is retained in corrected form.
2. Attempt 3 explicitly restricts deterministic time subsequences to nonnegative integers.
3. Attempt 3 now constructs independent uniforms U_j and residual samples Z_j, defines a measurable flag H_j, and sets Y_j equal to V_j on H_j and Z_j otherwise. This gives pointwise equality on the flag without inferring support on a nonmeasurable diagonal.
4. Attempt 4 explicitly requires independence of the random time from the whole pair for its convex-error identity.
5. Earlier chronology is reconciled: SC necessity was unproved in Attempt 1 and disproved in Attempt 2; Attempt 3 later supplies the general auxiliary-copy equivalence. Earlier negative scope assessments do not erase that positive theorem.

## Imported dependencies and verification limits

The analytic proof uses Radon–Nikodym, the finite-measure L1 duality theorem, Hahn–Banach/Mazur convexification, and countable products of probability measures. The restricted recoupling theorem also imports Vitali–Hahn–Saks. Their classical status is acknowledged; finite-cell and common-part constructions are supplied explicitly. The rank-one example imports mixing from the cited Creutz–Silva statement of Adams' theorem after checking its hypotheses; no independent reproof of that mixing theorem is claimed.

The mathematical audits accept the stated partial results and proofs, subject to those imported inputs. They do not establish exhaustive literature coverage or resolve the source's intended format. The conservative UNSOLVED 5/5 disposition is therefore a named-problem acceptance judgment, not a finding that the general positive equivalence is false, incomplete in its own scope, or ruled out by the source.

No numerical experiment or hash manifest certifies the universal mathematical statements. The manifest records bytes and SHA-256 only. No source document or dataset is redistributed with this package.
