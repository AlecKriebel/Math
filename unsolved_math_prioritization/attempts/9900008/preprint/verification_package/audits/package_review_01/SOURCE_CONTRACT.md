# Independent source contract (frozen before candidate or earlier reviews)

Frozen 2026-10-15 12:41 UTC. Sources read directly: Thorisson, *Some open probability problems*, Section 4 pp. 5–6; Last–Thorisson, arXiv:0906.2062, Sections 2–3, Definition 6.1 / Remark 6.2, Section 7 including Problem 7.5. No candidate proof or prior report has yet been read.

## Exact target

Problem 4.1 asks whether, for a diffuse random locally finite measure ξ on a locally compact second countable Abelian group G, the law of the observed pair (X,ξ) being invariant under every measurable ξ-preserving allocation shift implies mass-stationarity, without adjoining independent stationary backgrounds. A negative answer needs one admissible G and one diffuse nonzero locally finite random measure / observed pair for which the full universal allocation invariance holds but mass-stationarity fails. A deterministic auxiliary X is sufficient. A one-dimensional example suffices to refute the unrestricted assertion.

Write θ_t for shifting origin by t, so θ_t μ(B)=μ(B+t). A measurable allocation τ(ω,s) must satisfy the pointwise covariance identity τ(θ_tω,s−t)=τ(ω,s)−t for all ω,s,t. Equivalently τ(ω,s)=s+π(θ_sω) for measurable π(ω)=τ(ω,0). No injectivity, invertibility, continuity, bounded displacement, or extra randomness may be imposed. Preservation is τ(ω,·)_#ξ(ω)=ξ(ω), at least at every state charged by the candidate law (an argument valid for the larger class with preservation only law-almost surely is sufficient). The root invariance must hold for every such rule and the complete observed state, not just a marginal, statistic, bijective subgroup, or allocation chosen from a convenient subclass. The allocation must be a function of the stated observed state; hidden coordinates cannot silently help it.

Problem 7.5 has the same implication on a measurable flow with an invariant random measure, a σ-finite Q and Q(ξ(G)=0)=0; brackets restrict allocation measurability to σ(ξ)⊗B(G). A probability-law counterexample satisfying invariance for all fully measurable allocations is stronger and covers the bracketed variant if it really meets that class.

## Required failure of mass-stationarity

Definition 6.1 requires the joint identity (θ_Vω,U+V) ≡_d (ω,U), with U Haar-uniform on a relatively compact C having 0<λ(C)<∞ and λ(∂C)=0, and conditional V sampled from ξ restricted to C−U, normalized when positive. It also requires ξ nonzero Q-almost surely. Failure of the observed-state marginal under one such valid C already disproves this joint identity. A witness must handle zero window mass honestly, root-null sets and endpoint conventions; no argument may rely on an impossible conditional choice. The shorter 2010 statement says all relatively compact Borel sets, but the operative 2009 definition supplies the positive-Haar and zero-Haar-boundary convention. A regular interval witness on R avoids this distinction.

## Success / failure criteria

Success requires a checkable construction and a proof for universal measurable, potentially noninjective allocations with exact covariance, plus one explicit lawful window showing failure of mass-stationarity. Check local finiteness, diffuseness, measurable flow, ξ flow-covariance, observed-state recovery, the effect of null sets at the root, all noninjective branches, endpoint/limiting cases, and the entire joint law. Finite experiments are diagnostics only. Imported lemmas must meet hypotheses and be credited against their actual primary bodies. Prior existence or classical implication could affect novelty/credit even if the historical target is answered; no novelty claim is established by solving the target alone.

Research completion estimate at this checkpoint: 8% of this independent whole-package review; no mathematical verdict yet.
