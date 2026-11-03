# Independent mathematical audit: resonant nodal compactness

Date: 2026-10-21.

Reviewed report: `RESONANT_NODAL_ANALYSIS.md` in this directory.

SHA256 of the exact reviewed report bytes:
`b6cb50858de1136ed41a78bc1666c51ca2e15210e1da472f2bde1927bd4649ec`

## Verdict and review scope

PASS for the main general-p spectral sandwich theorem and its least-energy, nonzero finite C¹ subsequential resonant-limit consequence. No mathematical correction to that theorem is required. The compactness assertion is understood asymptotically as q approaches p from below, as in the report's explicit sequential formulation. This audit does not assert novelty or resolve the explicitly excluded stronger conclusions.

The review read the complete report and independently checked the main argument against the inspected Tanaka (2025) text, particularly Theorem 1.6, Proposition 1.7 and its proof, Lemma 2.1, Proposition 2.3, and Proposition 3.1. Public bibliographic source: Mieko Tanaka, “Remarks on the non-local eigenvalue problems for the p-Laplacian,” Boundary Value Problems (2025), https://doi.org/10.1186/s13661-025-02016-8. The audit's principal certification is the unconditional theorem in Approach 1; the p=2 projection was also independently checked. The other approaches remain subject to their stated conditional or special-case scope.

## Hypotheses and normalized compactness

The theorem assumes a bounded connected C^{1,1} domain Ω, p>1, weight identically one, and 1<q<p sufficiently close to p. Dirichlet conditions and C¹ convergence up to the boundary are essential parts of the stated setting. The paper's regular-domain compactness result supplies the latter; this audit does not extrapolate it to arbitrary bounded domains.

The normalized equation is correctly written because ||w_q||_q=1: the otherwise present homogeneous normalization factor equals one. The least nodal eigenvalue is attained by Theorem 1.6; Proposition 1.7 gives μ_q→λ₂. Lemma 2.1 then applies to every sequence of normalized associated eigenfunctions with q→p, yielding a C¹-convergent subsequence, a limiting p-eigenfunction, and limiting Lp norm one. Connectedness ensures that a nonzero one-signed p-eigenfunction belongs to λ₁, not λ₂. Thus every such λ₂ limit is nodal.

## Uniform nodal nonvanishing and exponent estimates

The uniform estimates in Approach 1A follow by contradiction over arbitrary choices of normalized least-nodal eigenfunctions, not only over a preselected branch. Failure arbitrarily near p would give a sequence q_n→p with either unbounded sup norm or a nodal Lp mass tending to zero. The compactness just described excludes the former and makes the latter contradict nodality of the limit. Hence a common M bounds the sup norms and a common c>0 bounds both nodal Lp masses below.

There is no differentiation gap at the nodal zero set. Fix δ>0 with p−δ>1. The quantity t^r|log t|, with value zero at t=0, is bounded uniformly for 0≤t≤M and p−δ≤r≤p. The exponent mean value estimate therefore gives a uniform pointwise bound |t^q−t^p|≤C(p−q). Integration on the finite-measure domain and division by the positive nodal masses produce exactly the asserted ratios 1+O(p−q).

## Entire spectral sandwich

Testing the normalized weak equation against w_q^+ and against −w_q^- yields

R_p(w_q^σ)=μ_q (∫(w_q^σ)^q)/(∫(w_q^σ)^p), for σ=+,−.

The two nodal parts are nonzero and linearly independent. The Lp-unit sphere in their two-dimensional span is a compact symmetric set of genus two. Because the nodal parts and their gradients are disjoint almost everywhere, its p-Rayleigh quotient is a weighted average of the individual quotients and its maximum equals their maximum. The genus-two characterization at exponent p therefore gives

λ₂≤max_σ R_p(w_q^σ)≤μ_q[1+C(p−q)].

This proves μ_q≥λ₂/[1+C(p−q)]. No q<p equality between least-nodal and LS levels is used.

For the other bound, fix a second p-eigenfunction φ. Its two nodal pieces are nonzero and bounded and satisfy R_p(φ^σ)=λ₂. Proposition 3.1 followed by Proposition 2.3 gives μ_q≤max_σ R_q(φ^σ). The denominator in R_q is (∫|φ^σ|^q)^{p/q}, not simply ∫|φ^σ|^q. It is positive and differentiable near p, with finite derivative by the same logarithmic bound at zero. Thus R_q(φ^σ)=λ₂+O(p−q), proving the upper bound.

Together these estimates give |μ_q−λ₂|≤C(p−q). Positivity of λ₂ then gives |log(λ₂/μ_q)|≤C'(p−q), so the scaling factors a_q=(λ₂/μ_q)^{1/(p−q)} stay bounded above and bounded away from zero. For each sequence q_n→p, a common subsequence has a_q→a>0 and w_q→w in C¹. Consequently u_q=a_qw_q→aw in C¹, and aw is a nonzero nodal second p-eigenfunction. Merely knowing μ_q→λ₂ would not suffice; the report correctly supplies the missing first-order estimate.

## Least-energy correspondence

This portion is also correct. If u is an actual nodal solution of −Δ_pu=λ|u|^{q−2}u, let t=||u||_q and w=u/t. Then w is a normalized nodal eigenfunction with eigenvalue ν=λt^{q−p}, equivalently t=(λ/ν)^{1/(p−q)}. Conversely this scaling constructs an actual nodal solution from every normalized nodal eigenpair.

Testing yields ∫|∇u|^p=λ^{p/(p−q)}ν^{−q/(p−q)}. The energy is (1/p−1/q) times this quantity, with negative coefficient. As ν increases this negative energy increases, so its minimum among actual nodal solutions occurs exactly at the least nodal eigenvalue μ_q. Attainment of μ_q therefore establishes the asserted least-energy correspondence. No claim about minimizing on an unrestricted nodal Nehari constraint is needed or made.

## Additional p=2 check and exact exclusions

For p=2, testing against every ψ in the full λ₂ eigenspace and using self-adjointness gives ∫[u_q−|u_q|^{−ε}u_q]ψ=0. Division by ε is justified by uniform convergence of the scalar difference quotient on bounded intervals to t log|t|. The uniform second-order remainder is controlled by t^{1−δ}|log t|² for δ<1, including at zero. Thus every subsequential limit U obeys ∫U log|U| ψ=0 for all such ψ, and ∫U²log|U|=0. The stated amplitude formula relative to an L²-normalized limiting direction follows.

The audit does not infer a unique limiting direction, a unique general-p amplitude, a derivative of μ_q at p, a general-p entropy equality, or convergence of arbitrary choices without subsequences or an orientation convention. C¹ compactness alone does not justify dividing a nonlinear p-Laplacian defect by p−q. The report appropriately labels its differentiable-branch argument conditional and does not claim that such a branch is necessary for every possible proof. Nor does this audit certify extension to nonsmooth domains or claim that sharper questions are open in the literature.

No theorem edits, source reproduction, publication, or additional research were performed for this persisted audit.
