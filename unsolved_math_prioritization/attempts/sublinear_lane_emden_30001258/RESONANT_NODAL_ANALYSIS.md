# Resonant nodal asymptotics from below: five approaches and audited partial closure

Date: 2026-10-21. Problem 30001258, ordered row 1877. Authored mathematical analysis only; no publication or queue changes.

## Scope and result

Let Ω be a bounded connected C^{1,1} domain, p>1, and λ₂ its second Dirichlet p-Laplacian eigenvalue. Put ε=p−q>0. Let μ_q be the least nodal eigenvalue of the homogeneous normalized q-problem and choose any associated w_q with ||w_q||_q=1:

−Δ_p w_q = μ_q |w_q|^{q−2}w_q.

Then, using the results and inequalities of Tanaka (2025) specified below,

|μ_q−λ₂| ≤ C(p−q)

for q sufficiently close to p. Consequently the fixed-parameter resonant least-energy nodal solutions

u_q = (λ₂/μ_q)^{1/(p−q)} w_q

form a relatively compact family in C¹(Ω-bar), bounded away from zero. Every sequence q_n↑p admits a subsequence converging in C¹ to a nonzero second p-eigenfunction.

This closes the finite, nonzero **subsequential unnormalized resonant-limit** gap in SOURCE_GATE.md for this smooth domain class. It does not prove a uniquely selected eigenfunction, an exact general-p entropy amplitude formula, or a scalar first derivative of μ_q. It is a deduction from existing literature, not a claim of publication-level novelty or a solution on arbitrary bounded domains. Positive solutions and nonresonant normalized/nodal conclusions were already covered in the source gate and are not reclaimed here.

## Literature inputs, inspected

Mieko Tanaka, Remarks on the non-local eigenvalue problems for the p-Laplacian, Boundary Value Problems (2025), DOI https://doi.org/10.1186/s13661-025-02016-8.

- Theorem 1.6: μ_q exists and is attained for 1<q≤p.
- Proposition 1.7: μ_q→λ₂ as q↑p.
- Lemma 2.1: Lq-normalized eigenfunctions have strong subsequential compactness, in C¹ on the stated regular domains.
- Proposition 2.3 and Proposition 3.1: μ_q≤λ₂^{LS}(q)≤max{R_q(f⁺),R_q(f⁻)} for every sign-changing f, where R_q(f)=∫|∇f|^p/(∫|f|^q)^{p/q}.
- At q=p, the standard second eigenvalue is the genus-two variational eigenvalue. Only the inequalities above are used; equality of the q<p least nodal and LS levels is not assumed.

Original research direction: Grumiau–Parini contribution in Oberwolfach Report 26/2009, pp.1457–1459, DOI https://doi.org/10.4171/OWR/2009/26. The source states convergence language without an explicit choice convention; arbitrary choices always admit sign oscillation, so a literal full-family uniqueness assertion must not be smuggled into the conclusion.

## Approach 1: first-order spectral sandwich (successful)

### 1A. Uniform normalized bounds and nodal masses

There exist M,c>0 and q₀<p such that every normalized least-nodal eigenfunction with q₀<q<p satisfies

||w_q||∞≤M,   ∫(w_q⁺)^p≥c,   ∫(w_q⁻)^p≥c.

To prove uniformity, take a sequence violating a bound. Proposition 1.7 and Lemma 2.1 give a C¹-convergent subsequence to w, with ||w||_p=1 and −Δ_p w=λ₂|w|^{p−2}w. On a connected domain this eigenfunction is sign-changing: a nonnegative nonzero p-eigenfunction belongs to the first eigenvalue, not λ₂. Therefore both limiting nodal masses are positive. This contradicts either vanishing mass, and compactness also excludes unbounded sup norms.

Choose δ>0 with p−δ>1. On 0≤t≤M and p−δ≤r≤p the function t^r|log t|, extended by zero at t=0, is bounded. The mean value theorem and finite measure of Ω give, uniformly in w_q,

|∫(w_q^σ)^q−∫(w_q^σ)^p|≤Cε,  σ∈{+,−}.

Dividing by the uniform positive masses gives the corresponding ratios equal to 1+O(ε).

### 1B. Lower bound for μ_q

Testing the equation by the positive and negative parts gives

R_p(w_q^σ)=μ_q [∫(w_q^σ)^q/∫(w_q^σ)^p].

The Lp-unit circle in span{w_q⁺,w_q⁻} is compact, symmetric and has genus two. Disjoint supports make the maximal p-Rayleigh quotient on that circle exactly max_σ R_p(w_q^σ). Hence

λ₂≤max_σ R_p(w_q^σ)≤μ_q(1+Cε),

and μ_q≥λ₂/(1+Cε).

### 1C. Upper bound for μ_q

Fix any second p-eigenfunction φ. Tanaka's two inequalities give

μ_q≤max_σ R_q(φ^σ).

Both fixed nodal pieces are nonzero and bounded, and their R_q quotients are differentiable with respect to q near p. Since R_p(φ^σ)=λ₂,

μ_q≤λ₂+Cε.

Combining bounds yields |μ_q−λ₂|≤Cε. Since λ₂>0, |log(λ₂/μ_q)|≤C'ε and therefore

0<c₁≤a_q:=(λ₂/μ_q)^{1/ε}≤c₂<∞.

For any sequence q_n↑p, extract a common subsequence with a_q→a>0 and w_q→w in C¹. Homogeneity now gives u_q→aw, a nonzero second eigenfunction. This is a genuine first-order estimate, not an illicit inference from continuity alone.

### 1D. Least-energy correspondence

For any fixed λ>0, every actual nonzero nodal solution corresponds to a normalized nodal eigenpair ν,w, with u=(λ/ν)^{1/ε}w. Its gradient norm satisfies ∫|∇u|^p=λ^{p/ε}ν^{−q/ε}. Its energy is (1/p−1/q) times that positive quantity. Because this coefficient is negative, minimizing energy among actual nodal solutions is equivalent to minimizing ν. Thus the least-nodal μ_q selects precisely the actual least-energy nodal solutions. No minimization over a spurious nodal Nehari set is used.

## Approach 2: entropy inequalities and finite-dimensional spectral projection

### General-p inequalities (rigorous, not an equality)

Suppose w_q→w along a subsequence, normalized by ||w||_p=1. Write

A_σ=∫(w^σ)^p, B_σ=∫(w^σ)^p log w^σ, h_σ=B_σ/A_σ.

Uniform Taylor expansion, including at the nodal zero set, improves the ratio calculation to

[∫(w_q^σ)^q]/[∫(w_q^σ)^p]=1−εh_σ+o(ε).

Therefore

liminf [log(μ_q/λ₂)/ε] ≥ min_σ h_σ.

For any fixed second eigenfunction φ define a_σ=∫(φ^σ)^p, b_σ=∫(φ^σ)^p log φ^σ and k_σ=b_σ/a_σ−(log a_σ)/p. Expanding its Rayleigh quotient gives

log[R_{p−ε}(φ^σ)/λ₂]=εk_σ+o(ε),

and consequently

limsup [log(μ_q/λ₂)/ε] ≤ max_σ k_σ.

The upper estimate holds for every fixed φ. These bounds are finite but generally different; they do not manufacture a unique entropy derivative.

### p=2: exact entropy condition (successful special case)

Let U be any unnormalized resonant subsequential limit, and let E₂ be the full λ₂ eigenspace. For every ψ∈E₂, self-adjointness and the equations yield

∫ [u_q−|u_q|^{−ε}u_q] ψ =0.

After division by ε the scalar integrand converges uniformly on bounded intervals to t log|t|. The Taylor error is bounded using sup_{0≤t≤M} t^{1−δ}|log t|² with δ<1; thus zeros cause no gap. Passing to the limit gives

∫ U log|U| ψ=0 for every ψ∈E₂.

Taking ψ=U gives ∫U²log|U|=0. If U=aw with ||w||₂=1, then

a=exp(−∫w²log|w|).

Moreover, projection onto every ψ orthogonal to w shows that w is a critical point of the entropy ∫w²log|w| on the unit sphere in E₂. This does not prove which critical direction least nodal solutions select. If E₂ is one-dimensional, the positive amplitude is uniquely fixed; an orientation convention still must remove ± ambiguity.

## Approach 3: differentiable-branch/Fredholm calculation (conditional)

A general-p branch calculation predicts the same entropy formula but needs extra hypotheses. Assume, rather than infer, a differentiable normalized solution branch at ε=0, sufficient differentiability of the p-Laplacian along it, and that all differentiations and pairings below are legitimate. Write w_ε=w+εz+o(ε) and μ_ε=λ₂+εm+o(ε), with ||w||_p=1. Differentiating

−Δ_p w_ε=μ_ε|w_ε|^{p−2−ε}w_ε

gives

L_w z=m|w|^{p−2}w + λ₂(p−1)|w|^{p−2}z −λ₂|w|^{p−2}w log|w|.

Pair with w. Homogeneity and symmetry of the valid linearization give ⟨L_w z,w⟩=(p−1)λ₂∫|w|^{p−2}wz, cancelling the z terms. Thus m=λ₂∫|w|^p log|w| and log a=−m/λ₂.

Obstacle: normalized C¹ compactness does not establish a differentiable branch, control the nonlinear defect to o(ε), or justify an invertible linearization near the critical set of ∇w. For 1<p<2 singular coefficients create an additional issue. Consequently this is an explicitly conditional derivation, not part of the unconditional general-p theorem. Other methods might establish the formula without a differentiable branch; necessity is not asserted.

## Approach 4: nodal partition/variational selection (precise obstruction)

The genus-two trial set generated by φ⁺ and φ⁻ has constant p-Rayleigh quotient at q=p. For q<p, its maximal q-Rayleigh quotient occurs at a pure nodal component, and its first-order correction is max{k_+,k_-}, not automatically the whole-function entropy. The least nodal level is only bounded above by the LS level in the inspected source. Replacing that inequality by an equality or replacing the maximum of component entropies by the whole entropy would be an unproved step.

A possible stronger route would optimize partitions and track first-order motion of the nodal interface, enforcing the p-flux matching that turns independently positive pieces into a global weak solution. The existing compactness theorem supplies neither a smooth moving interface nor its shape derivative. The spectral sandwich bypasses these missing ingredients for compactness, but this approach does not currently select an exact general-p entropy amplitude.

## Approach 5: one-dimensional first integral (successful exact check)

On Ω=(0,L), the k-half-wave solution has common absolute maximum M_q on all nodal intervals. The conserved first integral is

[(p−1)/p]|u'|^p + (λ/q)|u|^q = (λ/q) M_q^q.

Let I_q=∫₀¹(1−s^q)^{−1/p}ds. Integrating from a zero to an adjacent maximum gives

L/(2k)=[(p−1)q/(pλ)]^{1/p} M_q^{1−q/p} I_q.

Thus

M_q^{p−q}=[L/(2k I_q)]^p pλ/[(p−1)q].

At λ=λ_k=(p−1)(2kI_p/L)^p this becomes

log M_q = [p(log I_p−log I_q)+log(p/q)]/(p−q),

so

M_q→exp(p I'_p/I_p+1/p).

Differentiability of I_q follows either from its beta-integral expression I_q=(1/q)B(1/q,1−1/p) or direct dominated differentiation near q=p. For p=2 this limit is 2/√e, consistent with the entropy of the sup-normalized sine. For the least nodal branch k=2, this verifies finite resonant amplitude and full convergence after choosing orientation. The first integral forces equal lobe lengths and amplitudes on the interval; its rigidity does not extend to arbitrary multidimensional nodal geometry. This is a consistency/special-case derivation, not a novelty claim.

## Independent adversarial review

An independent mathematical reviewer inspected Tanaka's propositions and checked the entire spectral sandwich. Verdict: passed on bounded connected C^{1,1} domains. The review explicitly checked uniformity over arbitrary choices of least-nodal normalized eigenfunctions, nonvanishing of both nodal masses, the exponent derivative at zeros, genus-two normalization, the inequality-only upper bound (no unproved equality of critical levels), and p=2 full-eigenspace projection. It confirmed that the result closes only the nonzero finite unnormalized subsequential gap and does not establish uniqueness or an exact general-p derivative.

## Honest terminal assessment

- Established here from inspected literature: O(p−q) least-nodal spectral control and nonzero finite C¹ subsequential unnormalized resonant limits, for bounded connected C^{1,1} domains.
- Established special checks: exact p=2 entropy selection condition; exact interval amplitude for every p>1.
- Not established: a unique general-p limiting direction or amplitude, a general-p entropy identity, full-family convergence without selection conventions, or extension to arbitrary bounded nonsmooth domains.
- No assertion that the remaining sharper questions are open in the literature. Targeted web searches did not supply a directly applicable additional theorem; such negative searches are not proof of novelty.
- No source PDFs/text, dataset material, private coordination, queue changes, commits, or publication were performed.
