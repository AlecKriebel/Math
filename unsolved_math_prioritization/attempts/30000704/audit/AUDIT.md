# Independent adversarial audit: boundary regularity of conformal metrics

Date: 2026-10-04 UTC. Target: rank 660, problem 30000704, OWR-1460-010.

## Verdict

**PASS for the intended partial mathematics, subject to one explicit theorem-statement correction. Retain unsolved / exhausted partial, 5/5 approaches. Do not mark solved or assert novelty.**

No defect was found in Theorems A and B, the proof of Theorem C under the intended positive C²/lower-curvature hypotheses, or the two constant-curvature counterexamples. Theorem C's abbreviated standalone statement must explicitly include that λ is positive C² and κλ≥−4. Its proof uses this assumption, but its displayed statement says only “Under (J).” The correction is supplied separately in CORRECTIONS.md; no original file was changed. Taken literally without the curvature assumption, that sentence is false, including on the unit disk.

The generalized minimum-boundary-condition problem remains unresolved. The reverse implication depends on the localized disk completeness comparison stated in the primary report; its original detailed proof in KRR 2007 was not available for this audit. This is an explicit established-theorem dependency, not a missing step being represented as independently proved.

The original 22 controls passed on fresh execution and their output is byte-identical to the supplied output. An independently authored set of 27 exact algebraic/limit stress controls also passed. Neither count is a proof certificate for topology, compactness, or the cited theorem.

## Binding and review method

The reviewed original manifest is SHA256SUMS.json, 1,560 bytes, SHA-256:

    860f342d02acf761c40c3bca59f959fd1e4e3d3e7c028292ccdcf7b3dca46255

Its 11 listed files were hash/length verified, including the complete 19,971-byte ANALYSIS.md, SHA-256 bf93e022a3a254031b9afe7f205fdafc6076ea3228d251c2324cf737a1186769. Review covered the complete note, five-approach log, source gate and manifest, both verification programs, recorded controls, status, and prior correction. The originals were verified again after the audit.

This audit used no helpers and made no remote writes. It independently re-derived critical implications, investigated failure modes of the assumptions, replayed the original code, and separately inspected the primary problem and the exact source dependency. New examples below test the submitted assertions rather than extending the five-approach research campaign.

BINDING.json and verify_audit.py bind this audit to the frozen author package. The audit directory is portable: verification takes the original safe directory as an explicit argument, with no hard-coded workspace path or source download requirement.

## 1. Source identity and known-theorem dependence

The primary source is Oliver Roth's contribution in [Normal Families and Complex Dynamics, Oberwolfach Report 9/2007](https://ems.press/content/serial-article-files/46093), printed p.529, PDF page 43. I freshly downloaded the 62-page PDF, compared its hash/length with the author's manifest, extracted the relevant text, and visually inspected that page. The exact match is recorded in SOURCE_CHECK.json.

The report's Problem 2 concerns weakening the boundary assumptions in its positive-metric equivalence. Its preceding corollary requires an open free C² arc and curvature bounded below by −4. On the disk, the same page expressly attributes local completeness implying a lower hyperbolic-density ratio to Yau and Bland. This supports the precise estimate used in the note. The neighboring holomorphic-map question is separate. These facts verify the note's identification and dependence, without establishing priority for its rough-boundary extension.

The bibliographic identity of Kraus–Roth–Ruscheweyh, [A boundary version of Ahlfors' Lemma, locally complete conformal metrics and conformally invariant reflection principles for analytic maps](https://doi.org/10.1007/s11854-007-0009-x), J. d'Analyse Math. 101 (2007), 219–256, was cross-checked against institutional publication records. The audit's publisher retrieval failed with a 403 tunnel response; no full-text access is claimed. The author's earlier HTML-preview result remains accurately distinguished from a PDF. No access restriction was bypassed.

For [Kraus–Roth's isolated-singularity paper](https://arxiv.org/abs/0801.2866), I inspected the supplied hash-matched PDF's extracted theorem statements 1.1, 1.2, and 1.4 and checked the live arXiv metadata. The curvature-continuity and negative-limit hypotheses are stronger than a mere lower bound. They are not silently imported into Theorems A–C.

For [Bracci–Kraus–Roth's boundary-rigidity paper](https://arxiv.org/abs/2310.05521), I inspected the supplied hash-matched version's statements in Section 2 and checked live metadata. Its principal strong Schwarz results use curvature ≤−4 and a quantitative ratio convergence condition. They do not furnish the proposed lower-curvature equivalence. The thesis and survey were not independently reviewed in full in this audit, and no conclusion rests on pretending otherwise.

## 2. Global outward approximation: Theorem A

### Connected neighborhoods and uniformization

For bounded connected G, its closure is connected and compact. The positive-radius neighborhood of this closure is open, bounded, and connected. Thus every G_n admits a disk universal covering; no simple-connectivity assumption was smuggled into the proof. Each closure(G) lies compactly inside G_n, and all G_n lie in a fixed disk. Monotonicity gives

    0 < h_fixed_disk(p) ≤ h_Gn(p) ≤ h_G(p).

Consequently L is finite and positive. Normalizing the covering derivative to be positive real is possible by rotating the covering disk. The derivative limit 1/L is nonzero, so Montel does not produce a constant limit.

### What the limit actually gives

For fixed w the images have distance tending to zero from closure(G), so the holomorphic limit lies in closure(G). The open mapping theorem, rather than a pointwise interior assertion, is what puts its whole image in int(closure(G)). Regular-openness now identifies that set with G. Schwarz–Pick gives h_G(p)/L≤1, the missing inequality opposite to monotonicity. The resulting limit is exact.

There is no need for the covering maps to be univalent, no use of global boundary accessibility, and no requirement that the neighborhoods have smooth boundaries. The argument handles infinitely connected bounded regular-open G.

### Interior maximum principle

For each fixed n, h_Gn is smooth, positive, and bounded on closure(G). Unrestricted λ→∞ at each boundary point implies every fixed positive superlevel set of log(h_Gn/λ) stays inside a compact subset of G. To justify this rigorously, a sequence in such a level set approaching the boundary has a convergent subsequence to some boundary point, contradicting the stipulated limit there. This does not require a preassigned uniform blow-up rate.

A positive value therefore leads to an attained positive maximum. At that point, the lower curvature bound has exactly the required sign:

    Δ log λ ≤ 4λ²,
    Δ log(h_Gn/λ) ≥ 4(h_Gn²−λ²) > 0.

This contradicts the second-derivative test. No boundary maximum principle for an irregular boundary is assumed: the boundary is avoided by a compact-superlevel argument. The scaling from −K to −4 is σ=(sqrt(K)/2)ρ, as stated.

## 3. Local cutoff and original-domain distances: Theorem B

### The lower bound m is genuinely uniform

The closed-ball boundary assumption is used, not merely the condition at ξ. A sequence in U with λ tending to zero has a subsequential limit in closure(Ω) intersected with the closed ball. If its limit belongs to Ω, positivity and continuity contradict it; otherwise the point lies in the stipulated portion of Γ and blow-up contradicts it. Hence m>0 throughout all of U, including all components together.

### Curvature and component boundary conditions

The cutoff is multiplicative. Thus its logarithm contributes only Δ[−log(R²−r²)], without uncontrolled gradient cross terms. Dividing the claimed inequality by ρ² reduces it to the elementary bounds (R²−r²)²≤R⁴ and λ≥m. The value K=4R⁴+4R²/m² is valid and is independent of the chosen component.

Every component G of open U is open and relatively closed in U. Since the plane is locally connected, no boundary point of G can lie in U: a small ball there would belong to one component. Thus ∂G⊂∂U. At an interior point of the circular patch boundary, the metric blows up by Γ; on the circle the cutoff blows up using the same m. Every component is bounded and receives the hypotheses of Theorem A. An infinite number of components causes no loss of the common constant.

### Punctured comparison and last crossing

Because ξ∉Ω, each G lies in B(ξ,R) minus ξ. The comparison h_G≥h_punctured_disk is in the correct direction. It yields the stated c/[r log(R/r)] barrier for r<R/2, with c=3R²/(4 sqrt(K)). The denominator is positive in this range.

For any piecewise C¹ path from z₀ outside r₀ to a final point inside r₀, continuity supplies a last crossing of r=r₀; its parameter exists because the crossing set is closed in the compact path interval. The remaining path stays inside r₀. Its radial coordinate is absolutely continuous and satisfies |r'|≤|γ'| almost everywhere. Integrating the absolute derivative of F(r)=log log(R/r) bounds length from below by c(F(r_end)−F(r₀)). This holds for every path in Ω, including those taking remote shortcuts or repeatedly entering the neighborhood. Taking an infimum cannot defeat this universal bound.

The proof establishes unrestricted divergence of metric distances at ξ, not merely infinite length along one selected radial path. It asserts nothing at boundary points outside Γ or at infinity.

## 4. Jordan patches and reverse transport: Theorem C

The corrected statement in CORRECTIONS.md is the version audited here.

For the forward direction, a sufficiently small closed ball lies in the neighborhood where Ω=P and meets ∂Ω only in Γ. A Jordan domain is regular-open. Finite intersections of regular-open sets remain regular-open: int(cl(A∩B)) is contained in int(cl A)∩int(cl B)=A∩B, while the reverse inclusion follows from openness. Each component of a regular-open planar open set is regular-open, by the local-ball argument used above. This verifies Theorem B's hypotheses without smoothness, rectifiability, or a finite-component assumption.

For the reverse direction, the bounded Jordan patch is simply connected and has a Riemann map φ. Carathéodory provides a boundary homeomorphism, so the chosen boundary subarc corresponds to an open circle arc and every approach to its point in P corresponds to an approach in the disk. No differentiability of this boundary extension is needed.

The pullback is positive and C² inside the disk: φ' never vanishes there. Its curvature is the original curvature composed with φ. The distance identity in the patch follows by conformal change of length, and restricting Ω-paths to P increases the distance infimum. Thus the original-domain completeness assumption gives precisely the disk completeness hypothesis. Changing the basepoint is harmless because connected plane domains are polygonally connected and λ is bounded on a compact connecting path.

The source estimate then applies. Hyperbolic conformal invariance cancels |φ'| in the quotient, including charts with arbitrarily degenerate boundary derivatives. The comparison with a punctured disk containing P forces h_P(z)→∞ at the selected boundary point. Finally, Ω=P locally is needed to turn a P-limit into the required unrestricted Ω-limit. Without that local equality, unseen approach components could invalidate the last step.

No reflection principle, boundary derivative bound, boundary extension of φ', or sharp λ/h_Ω statement is being inferred.

## 5. Counterexamples and adversarial geometries

### Puncture: the regular-open premise cannot just disappear

The submitted family λ_a has exactly curvature −4. For 0<a<1 it diverges at the puncture and on the unit circle while its primitive artanh(r^a) remains finite at zero. A finite-length segment supplies an upper bound on distance, which is enough to refute completeness.

The outward approximation failure can be made quantitative. For G=D minus {0}, every G_n is the disk of radius 1+1/n. Its hyperbolic densities tend to h_D, not h_G. For a=1/2 and r=1/4, λ_a=4/3 whereas h_G=1/log 2>4/3. The strict inequality follows from log 2<3/4, independently certified by a positive-derivative rational upper bound. Thus extending Theorem A to this non-regular-open domain would give a genuinely false conclusion, rather than just a gap in the given proof.

### Singleton on a smooth ambient boundary

On D the branch of ((1−z)/2)^a is holomorphic with nonzero derivative, and its values have modulus below one. Its pullback is positive, interior-real-analytic, and curvature −4. The denominator tends to one at z=1, giving density blow-up; the explicit radial primitive stays finite. This tests the absence of a neighborhood's worth of blow-up, not a failure of ambient smoothness. The same density also diverges at z=−1, which does not affect the counterexample with distinguished set {1}.

### Nonsmooth one-sided arc with a vanishing chart derivative

Use the sector 0<r<1, 0<θ<3π/2 and the vertex together with small portions of both radial sides as Γ. It is a bounded Jordan patch with a reentrant corner. With p=2/3, the restricted wedge density

    h(r,θ)=p/[2r sin(pθ)]

has curvature −4 and blows up along Γ. It is complete to the vertex by h≥p/(2r). The local chart w↦w^(3/2) has derivative tending to zero there, but the quotient cancellation in the reverse proof remains exact. This adversarial example tests the claimed removal of differentiability, not a boundary-derivative assumption hidden in the proof.

### Two-sided slit and infinitely many components

In Ω=B(0,2) minus [−1,1], near an interior point of the slit a small circular patch has two regular-open half-disk components. The ambient domain is not regular-open, and a one-sided Jordan patch cannot represent both approach sides at once, yet the componentwise forward theorem applies locally. Near a slit endpoint the component fills in its slit under regularization; Theorem B does not apply there. The audit does not label that endpoint a counterexample or resolve it.

For a genuine infinite-component stress test, set

    Ω=(−2,2)² minus (({0} union {1/n:n≥1}) × [−1,1]).

This is connected through the corridors above and below the removed vertical segments. For ξ=(0,0) and sufficiently small R, Ω∩B(ξ,R) has infinitely many components. Each is a convex vertical strip intersected with a disk, or a half disk, hence is regular-open. The boundary segments accumulate at ξ, so this is not a free-Jordan boundary there. The submitted m and K argument is nevertheless uniform across all components. No numerical sampling of these components is being treated as topological proof.

### Why omitted curvature would invalidate Theorem C

On D, τ=(1−|z|²)^(−1/2) is positive C∞ and diverges on the entire analytic boundary, but a radius has finite length π/2. Its curvature is −2/(1−|z|²), unbounded below. It refutes the theorem sentence if read without the curvature hypothesis, and simultaneously confirms why the intended statement survives. This is the reason correction C1 is mandatory for a standalone quotation of Theorem C.

### Addition and other tempting changes to the proof

The flat densities exp(Nx) and exp(−Nx) each have zero curvature. Their sum has curvature −N²/4 at x=0. Thus positive addition has no uniform lower-curvature preservation, even though both summands are flat. Their maximum is not differentiable on x=0. These mutations cannot replace the actual multiplicative cutoff proof. The independent controls verify this obstruction exactly.

## 6. Corrections, limitations, and disposition

Correction C1 adds the intended positive C²/lower-curvature assumptions to the standalone Theorem C statement. No proof change or new research approach is required. Optional clarification C2 explains that the report states the disk implication while the KRR original proof remains uninspected. The current source gate already communicates C2 accurately.

The author-side symbolic simplification repair was reproduced: the final controls pass and their output matches exactly. This audit did not claim that an earlier unsuccessful simplifier established a mathematical failure. Five approach families are explicitly logged; checking their proofs and counterexamples is not a sixth solution attempt. The recorded times and completeness probabilities are author records, not independently certified historical facts or mathematical confidence values.

The dataset/repository identity claims were inspected as supplied verification metadata but were not independently re-downloaded or checked against live repository state here. This mathematical audit therefore must not be described as an independent current queue/PR or raw-dataset provenance audit. Full KRR inspection and comprehensive priority certification remain outside its successful checks.

Recommended publication disposition: retain the frozen original plus this correction/audit addendum; label the target unsolved, 5/5, exhausted partial. A public summary may say the intended one-sided free-Jordan sufficient equivalence and componentwise forward criterion passed this audit, subject to the stated known theorem. It must not say the minimum general boundary regularity problem was solved, that all regular-open hypotheses are necessary, or that novelty has been established.

All portable files contain only authored analysis/code, exact results, and public-source metadata. No source PDF, extracted scholarly text, raw dataset, private coordination file, or credential is included.
