# Independent adversarial review of the Ostrovsky strong-norm candidate

## Verdict

**PASS for the precisely stated local-characteristic W^{1,∞} orbital-instability theorem.** No substantive mathematical gap was found in the frozen argument. This does not establish an L² or H¹ orbital-instability theorem, a global weak-continuation result, or a full solution of the broader source question.

- Target: 30004186 / OWR-17128-002
- Frozen artifact: `CANDIDATE.md`
- Reviewed SHA-256: `95458afe7f030f3f0aec3b9d5150857e7dedcb8688e6325c4a0407497feb1b6c`
- Reviewer: separate gpt-6-astra agent, selected effort xhigh
- Review date: 30 September 2026 UTC
- Mathematical corrections required: none
- Source-history addition requested before publication: preserve the superseded 2018 nonlinear claim described below; do not call it a formally withdrawn paper

This is an independent AI mathematical review, not human peer review or formal verification. Historical priority remains unestablished.

## 1. Exact source boundary and the earlier version warning

The full Geyer–Pelinovsky contribution in [OWR 32/2019](https://ems.press/content/serial-article-files/46811), printed pp. 1940–1942, uses the equation and peak normalization in the candidate. It describes linear and spectral instability, then leaves nonlinear instability open. It points to the failure of smooth Sobolev well-posedness to include the peak and the mismatch between the linearized domain and H¹. Its final question does not fix one nonlinear stability norm. Therefore the strong-norm theorem is a meaningful, explicitly restricted result, but it must not be reported as an L²/H¹ conclusion.

A material source-history fact surfaced during this audit. [Geyer–Pelinovsky, arXiv:1804.03788v1](https://arxiv.org/abs/1804.03788v1), posted 11 April 2018, was titled *Linear and nonlinear instability of the peaked periodic wave in the reduced Ostrovsky equation*. Section 4, Definition 4 and Lemma 10, pp. 18–21, claimed H¹ orbital instability using an L² departure. The current [v2](https://arxiv.org/abs/1804.03788v2), dated 2 January 2019, and the [published 2019 paper](https://pelinovsky.mcmaster.ca/PaperBank/PeakedWaveOstrov.pdf) remove that nonlinear claim; the published discussion explicitly identifies the evolution-space obstacle. The arXiv record is superseded, not marked withdrawn.

In the old v1 argument, the passage to a smooth perturbation of a nonsmooth peak does not itself justify importing smooth H^s existence with lifetime proportional to the inverse perturbation size. Its contradiction also assumes a bound proportional to the initial size, which generic orbital stability does not imply. These are this review's identified unsupported steps, not a quoted author correction. The current candidate avoids both: it constructs a corner-compatible flow directly and uses a fixed departure threshold. The old claim is not a valid certificate for the stronger weaker-norm conclusion.

The [2025 Natali–Pelinovsky–Wang article](https://www.cambridge.org/core/journals/journal-of-nonlinear-waves/article/instability-of-the-peaked-travelling-wave-in-a-local-model-for-shallow-water-waves/DE8AD3FB7366FEB52BC613CDB1611EC8), equations (1.6)–(1.7) and Theorem 4, is relevant methodological prior work. It explicitly distinguishes reduced Ostrovsky from its own local model, which has an additional squared-gradient term. Its gradient-instability theorem cannot simply be substituted for the candidate's equation.

## 2. The Banach evolution does include a corner

The space B={f in C¹([0,L]):f(0)=f(L)} is a closed Banach subspace. Equality of endpoint derivatives is deliberately absent. Thus the periodic continuation may have a single derivative jump at the identified endpoint, while the restriction to the closed parameter interval is C¹. The peaked profile and the proposed perturbations belong to B.

The primitive construction has the correct Jacobian and normalization. The lift obeys X(L)−X(0)=L, hence the integral of X_ξ is L. Subtracting m makes the initial primitive K vanish at both endpoints. Subtracting its X_ξ-weighted mean then gives an H with matching endpoint values, derivative (V−m)X_ξ, and zero physical mean. All these operations use only first derivatives. They define polynomial combinations of bounded linear and bilinear maps into C¹, so the vector field is locally Lipschitz, with common bounds on bounded C¹ sets. The sharp localization of the initial perturbation does not introduce a second-derivative dependence into this argument.

Differentiating the physical mean gives the displayed zero result: the H term vanishes by its weighted mean, and the V V_ξ term is an endpoint difference of V²/2. Thus m remains zero. Reconstruction by the increasing characteristic map gives a periodic, spatially continuous Lipschitz solution, classical away from the corner. Continuity of u eliminates a jump measure in the first-order distributional equation. The derivative jump alone is permitted.

This proves uniqueness in the constructed characteristic class, which is exactly the class the theorem specifies. It does not silently prove uniqueness among all arbitrary weak solutions.

## 3. Continuation and time regularity

The differentiated equations give (X_ξ)_t=V_ξ and (V_ξ)_t=V X_ξ. The quotient w=V_ξ/X_ξ therefore satisfies w_t=V−w². The same computation applies to one-sided endpoint derivatives because the ODE takes values in C¹ on the closed parameter interval. The corner-jump equation has the stated sign, and a nonzero jump remains nonzero while the endpoint slopes are bounded.

A finite physical slope bound M gives e^(−Mt)≤X_ξ≤e^(Mt), starting from X_ξ=1. The zero-mean primitive estimate bounds V in sup norm on each finite interval. The relation V_ξ=w X_ξ then bounds V in C¹, and integration bounds Y in C¹. Because the vector field is uniformly bounded and Lipschitz on these bounded sets, the trajectory has a Banach-space limit at a finite endpoint. Its Jacobian remains strictly positive, so local Picard existence restarts it. This closes the continuation argument; it is not an unjustified appeal to finite-dimensional compactness.

The initial C¹ norms and initial Jacobians are uniformly controlled, so a common positive initial existence time is valid. The continuation estimates need not be uniform as δ tends to zero at the later logarithmic time; the proof only needs them finite for each fixed δ under the hypothetical fixed slope bound.

The use of moving-corner C¹ coordinates is important. Translations of a peaked profile are not strongly continuous in periodic W^{1,∞}. The current candidate does not assert that false continuity statement. Its slope norm is continuous because it is the supremum of the continuous parameter-space function w. One-sided endpoint values equal the corresponding essential-supremum limits from nearby points, so the later slope departure is not an isolated-point artifact.

## 4. True crest forcing and the amplitude comparison

The periodic primitive kernel 1/2−x/L has L¹ norm L/4=π/2. Both compared solutions have zero mean, so it applies to u−b. Along a nonlinear characteristic, the background travelling wave is Lipschitz, and the differential inequality for the difference has coefficient bounded by κ. At times when the characteristic lies at a background crest on a set of positive measure, its relative velocity vanishes almost everywhere there. The difference also vanishes there, so the same almost-everywhere inequality is valid. No derivative of the corner is being taken illicitly.

Gronwall consequently gives the amplitude rate A=κ+π/2=(5/2)κ, independently of the perturbed spatial slope. The displacement inequality for q−ct follows from the global Lipschitz bound for the periodic background. Substitution yields the factor A/(A−κ)=5/3 in the true corner-value bound. The proof never freezes q′ or u(t,q(t)) at c. That distinction prevents a serious possible forcing error.

## 5. Narrow perturbations and logarithmic time

The initial correction has amplitude O(δ η)=O(δ³), slope O(δ), and total mass O(δ η²)=O(δ⁵) when η=δ². A fixed smooth mean-correcting function supported away from the corner does not alter the endpoint slopes and contributes only O(δ⁵) in C¹. The initial mean, continuity, right slope −κ−δ, and left slope κ are all consistent.

With y=w_++κ, the shifted Riccati identity is y′=2κy−y²+(u(t,q)−c). Dropping the nonpositive square gives an upper bound, the correct direction for forcing y negative. At Tδ=(2κ)^−1 log(2ε*/δ), the positive weighted forcing error is O(δ³ δ^−1/4)=O(δ^(11/4)), which is o(δ). The constants depend only on fixed cutoffs and the fixed wave, not on δ. Large second derivatives of the localized profile are irrelevant to the established C¹ evolution.

The first-hitting/continuation dichotomy is valid. If the slope norm reaches κ+ε* earlier, use that time. Otherwise its fixed bound forces continuation through Tδ, where the Riccati estimate reaches the threshold. Since the initial derivative discrepancy is O(δ), the hitting time is positive for sufficiently small δ. The time belongs to the Lipschitz interval; no future singularity is used as a surrogate for an actual departure.

## 6. Orbital phase and the unresolved norms

For every translation θ, the derivative of the comparison peak has norm κ. The reverse triangle inequality therefore bounds the derivative discrepancy below by ||u_x||∞−κ. This is valid uniformly in θ and immediately survives taking the infimum. It avoids any unsupported assertion about the phase minimizing the norm or aligning the corners.

The fixed derivative departure need not occupy a uniformly positive spatial region. Thus neither an L² nor an H¹ departure follows. The proof also makes no global continuation or entropy-selection claim after a possible gradient breakdown. These limitations must remain in the theorem metadata and PR. In the campaign's status convention, the broader source problem remains unsolved.

## 7. Independent diagnostics

`independent_checks.py` (SymPy 1.14.0) passed **135 exact assertions**. It independently checks the profile/primitive normalization, reconstructs the exact unperturbed characteristic flow, verifies nine nontrivial polynomial coordinate systems and their weighted-mean/Riccati identities, checks the endpoint-jump algebra, verifies the logarithmic-time exponent and forcing constants, and tests a polynomial cutoff scaling control. Its finite small-δ checks use exact rational substitutions, not floating-point simulation.

The submitted identity verifier also replayed successfully: **20 checks passed**. That submitted script writes its deterministic receipt on execution; the reviewed mathematical candidate was not changed. These diagnostics are supplementary. The general Banach evolution, continuation, chain-rule, and orbital conclusions were audited analytically above rather than inferred from finite tests.

## Source-history requirement completed

At 05:08 UTC the author-added version-history section in SOURCE_AUDIT.md
was checked. It accurately records the superseded v1 claim, the later
removal, and the distinction from this scoped proof; it does not infer an
official withdrawal or the authors' reasons for revision. The required
source addition is complete. The mathematical candidate remains at the
original reviewed hash. No required correction remains.
