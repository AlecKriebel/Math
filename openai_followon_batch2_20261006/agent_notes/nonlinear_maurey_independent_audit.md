# Independent audit: nonlinear Maurey extension into all L1 targets

Checkpoint 2026-10-06 21:53 America/Los_Angeles. Triage-audit completion estimate 95%; no full source proof verification. Verdict: viable short path; exact constants/structural bridge identified.

## Claim

For every metric space X of Markov type2 and every real L1(μ), every Lipschitz map f:S→L1(μ) from an arbitrary subset extends to X with Lip(F)≤C M2(X) Lip(f), universal C. This includes Lp sources for finite p≥2 with O(sqrt(p)) loss using known Markov-type bounds; do not include p=∞ or arbitrary source spaces without snowflaking. Complex L1 costs at most sqrt2 additional distortion.

## Input and distinctness

Family332 `Metric-Markov-Cotype-Two-of-l1-October-5-2026/build/main.tex`: main theorem N2(ell1)≤12sqrt21; finite-cut reconstruction lemma at lines200–280; extension section593–649 states only Hilbert→ell1 and complex ell1 cotype. No all-L1/all-Markov-type-source corollary appears.

## Direct all-L1 bridge

For finitely many functions x_i∈L1(μ), define v(ω)=min_i x_i(ω), and for each nonempty proper B⊂[n], b_B(ω)=(min_{i∈B}x_i(ω)−max_{i∉B}x_i(ω))_+. These are measurable and integrable since |v|≤Σ|x_i| and b_B≤2Σ|x_i|. Set w_B=||b_B||1 and discard zero weights. T(u)=v+Σ_B u_B b_B reconstructs the x_i from binary cuts and is contractive from finite weighted ell1 into the original L1 space. Pointwise nested cuts give exactly the source lemma's identities after integration. There are ≤2^n−2 cuts, so no measurability, separability, or limiting-choice issue. The rest of source proof only uses this reconstruction and finite-dimensional Hilbert/cut calculations. Thus N2(L1(μ))≤12sqrt21 with no dimension/measure dependence. This is stronger/more transparent than finite approximation plus ultraproduct.

## Extension theorem scope

Primary source Mendel–Naor, https://web.math.princeton.edu/~naor/homepage%20files/cat0-extension.pdf, Theorem1.11 and discussion equation(9), printedpp8–10. Finite extension cost is universal multiple Γ M2(X) N2(Y). Every Banach target is W2-barycentric with Γ=1. Full extensions require a Lipschitz retraction from an ultrapower to Y, supplied in the Banach case by projection through Y** and a retraction Y**→Y. L1 is L-embedded, hence admits a canonical norm1 projection Y**→Y. Therefore no extra unknown constant; full bound universal multiple of M2(X). Cite the bidual projection fact from standard M-ideal/L-embedded references, e.g. Harmand–Werner–Werner ChapterIV https://page.mi.fu-berlin.de/werner99/mbuch/buch4.pdf.

## Adversarial pitfalls checked

- It is false that arbitrary L1(μ) is a dual Banach space. Cor1.13's dual-space clause is insufficient by itself; use equation(9)+L-embedded projection.
- Metric Markov cotype is not inherited by arbitrary subspaces. Kalton's counterexample in the same Mendel–Naor paper explicitly forbids claiming the theorem for every subspace of L1.
- Markov type2 constant M2(X) remains in the bound; it cannot be suppressed to an absolute constant for every Markov-type2 space.
- Avoid claiming noncommutative L1/Schatten1 targets: finite pointwise min/max reconstruction does not extend there.
- The short path is a consequence of the supplied theorem and established extension machinery; do not claim a new extension method.
