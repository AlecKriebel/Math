# Independent audit: problem 30002637

Date: 2026-10-03 (UTC)

## Verdict

**PASS for the frozen packet's actual partial mathematical claims. The original universal problem is NOT solved.**

No blocking sign, coefficient, projection, analytic, or topological error was found in the five written attempts. In particular, Turn 5's conditional scalar-gap obstruction to linear ν-stability is valid. This verdict does not certify novelty, a universal strict gap decrease, a stable counterexample, or a resolution of the original question.

Required mathematical repairs: **none**. Optional exposition improvements appear below. They are not prerequisites for the partial-result verdict.

## 1. Integrity, independence, and audit boundary

The audited directory was `ricci_soliton_30002637_frozen`. Its manifest SHA-256 is:

`316936e91c184fbc7a6c9b605cfee994a095183b00f75b3e1ca5df3356245f11`

All eleven listed file sizes and SHA-256 values matched the manifest. Every written attempt, the README, final status, research log, turn ledger, supplied algebra program, and supplied receipt were read. The supplied program was rerun: all nine identities passed.

The audit separately reconstructed the integration-by-parts arguments, gauge decomposition, min–max implication, conformal and multiplier formulas, and finite-quotient argument. Eight additional formal identities were checked in a separate audit script, including arbitrary-shrinker-coefficient gauge cancellation and agreement of Turn 3's conformal diagonal with Turn 2's resolvent formula. These checks support the hand audit; they cannot prove existence of a soliton or the missing universal sign.

The frozen directory was not modified. No external write, new author proof attempt, or novelty search was performed. The primary-source inspection below verifies cited inputs and source scope, not a comprehensive literature-status claim as of this audit date.

## 2. Source question and credited inputs

The [original Oberwolfach report](https://ems.press/content/serial-article-files/46526), printed pp. 2017–2019, defines nontrivial to mean non-Einstein, expressly discusses compact solitons, and puts the entropy on metrics modulo diffeomorphisms and rescaling. Its last paragraph on p. 2019 asks whether the positive-Hessian-eigenvalue phenomenon of the known nontrivial examples holds generally. The packet retains that stronger linear target and does not silently substitute dynamical instability. The report also states that compact steady and expanding solitons are Einstein. The reduction to compact gradient shrinkers therefore does not discard the intended nontrivial compact case; compact gradient reduction is standard prior input. No Kähler, dimension-four, or simply-connected restriction belongs in the universal target.

The directly inspected [Cao–Zhu v4 paper](https://arxiv.org/html/2304.01453v4) supports the packet's second-variation formula, weighted adjoints and commutators, invariant orthogonal splitting, and identification of the quotient operator. Theorem 2.1, Lemmas 2.1–2.3, Theorems 1.1–1.2, and Proposition 3.3 are the relevant locations. Their coefficient 1/2 is correctly rescaled to coefficient 1. Their Conjecture 2 is stated on printed p. 13 with the qualification “at least in dimension four.” The packet correctly retains prior credit. [Hall–Murphy](https://arxiv.org/abs/1008.1023) supplies the cited Kähler special case, not an unrestricted theorem.

The source text contains a discussion of dynamical instability despite a nonpositive Hessian. That is a reason to preserve, rather than weaken, the packet's explicit positive-spectrum target.

## 3. Exact accepted theorem scope

Let `(M,g,f)` be a smooth, connected, closed, non-Einstein gradient shrinking Ricci soliton with

\[
\operatorname{Ric}+\nabla^2f=g.
\]

Set `T=Ric`, `r=|T|`, `dμ=e^{-f}dV`, and `dρ=r²dμ`. Let `λ_f` be the first positive eigenvalue of `−Δ_f`, and let `λ_Ric` be the first positive scalar eigenvalue for `dρ`, equivalently of `−Δ_{f−2log r}`. Then:

1. `R>0`, so `r>0` and the second weighted operator is smooth and elliptic.
2. `1<λ_f≤2`.
3. If the ν-Hessian is nonpositive after diffeomorphisms and scaling are removed, then
   \[
   \lambda_{\rm Ric}\geq\lambda_f.
   \]
4. If `λ_Ric<λ_f`, the quotient operator `N` has a positive eigenvalue at least `1−λ_Ric/2` in this normalization.
5. If the first `k` positive `dρ`-eigenvalues are below `λ_f`, there are at least `k` quotient eigenvalues above `1−λ_f/2`.

The displayed numeric lower bound concerns the packet's operator `N`. The full ν-Hessian differs by a positive conventional prefactor, so its sign agrees; an absolute numeric Hessian-eigenvalue bound must retain that prefactor.

The comparison also holds trivially for Einstein metrics because `r` is constant and the two scalar gaps are equal. However, the Turn 5 gauge-threshold proof uses the non-Einstein bound `λ_f≤2`; this hypothesis must remain visible when that proof is reused.

No argument in the packet proves the strict inequality `λ_Ric<λ_f` for every non-Einstein compact shrinker. Nor is that inequality asserted to be necessary for instability.

## 4. Normalization, gauge, and the full Turn 5 min–max argument

### 4.1 Weighted conventions

The signs are consistent with `Δ_f` having nonpositive spectrum and `div_f*ω=−(1/2)L_{ω♯}g`. The normalized operator is

\[
Nh=Lh+\operatorname{div}_f^*\operatorname{div}_fh
 +\tfrac12\nabla^2v_h
 -T\frac{\langle T,h\rangle_f}{m},\qquad
(\Delta_f+1)v_h=\operatorname{div}_f\operatorname{div}_fh,
\]

where `m=∫|T|²dμ=∫R dμ`. Thus the Ricci-line penalty is precisely `−〈T,h〉²/m` at coefficient 1. At general shrinker coefficient `λ`, its denominator is `E[R]`, whereas the orthogonal projection coefficient onto Ricci has denominator `E|Ric|²=λE[R]`. Turn 2 correctly distinguishes these quantities.

The mean-zero resolvent has the correct sign: `v_h=−(−Δ_f−1)^{-1}div_f div_f h`. Its quadratic contribution is nonpositive.

### 4.2 No hidden nongradient gap

For a weighted one-form decomposition `ω=du+η` with `div_f η=0`, the tensors `Hess u` and `div_f*η` are orthogonal. This follows directly from

\[
\operatorname{div}_f\nabla^2u=d(\Delta_fu+u).
\]

The two summands are invariant under `L`. The Hessian of a scalar eigenfunction of eigenvalue `μ` has `L`-eigenvalue `1−μ/2`, so the gradient summand is bounded above by `κ=1−λ_f/2`.

For `h=div_f*η`, the auxiliary function is zero and the Ricci overlap vanishes. The exact equation `Nh=0` gives

\[
\langle Lh,h\rangle_f=-\|\operatorname{div}_fh\|_f^2\leq0.
\]

This handles all coclosed, nongradient, and harmonic one-form contributions without assuming vanishing first cohomology. Since `κ≥0` in the non-Einstein case, the entire gauge space obeys `L≤κ`. The bound is attained by Hessians of first scalar eigenfunctions. This is the crucial point that prevents a spurious instability from an unremoved positive gauge direction.

### 4.3 Ground-state identity and projection

Independent product differentiation and weighted integration give

\[
\langle L(\phi T),\phi T\rangle_f
=\int\phi^2r^2d\mu-\frac12\int|d\phi|^2r^2d\mu.
\]

The terms involving `d(r²)` cancel; no curvature sign is needed. A `dρ`-mean-zero multiplier makes `φT` orthogonal to `T`. Decomposing it into gauge and quotient parts, stability gives

\[
Q_L(\phi T)\leq\kappa\|h_G\|^2\leq\kappa\|\phi T\|^2,
\]

which is exactly the `dρ` Poincaré inequality with constant `λ_f`.

For `a=1−λ_Ric/2>κ`, the independently checked inequality is

\[
Q_L(h_V)\geq a\|h_V\|^2+(a-\kappa)\|h_G\|^2.
\]

It forces a nonzero quotient part and its Rayleigh quotient is at least `a>0`. Compact elliptic spectral theory on the invariant quotient subspace yields an actual eigenvalue. The same separation gives the stated multiplicity result. There is no inference from positivity on the full tensor space alone.

## 5. Exact multiplier and conformal calculations

### Turn 1: potential times Ricci — PASS

`div_f(uRic)=dR/2` and the proposed Hessian correction solves exactly that divergence. Its Ricci pairing vanishes by weighted integration by parts; subtracting `E(u|Ric|²)Ric/m` removes the remaining Ricci line. The leading numerator

\[
\mathbb E[(u^2-S/2)|\operatorname{Ric}|^2]
\]

agrees with the general ground-state identity. For the curvature coefficient `R_j` at scalar eigenvalue `μ_j`, the combined divergence/auxiliary coefficient is

\[
\frac{\mu_j(\mu_j-2)}{8(\mu_j-1)}R_j^2.
\]

The final `−c²/m` is required and correct. In particular, the scalar correction changes sign at 2; it has not been mistaken for a universally favorable term.

### Turn 2: general conformal form — PASS

At general coefficient `λ`, the computed forcing

\[
q_u=-Au-\langle dF,du\rangle+2\lambda Fu
\]

is correct and mean-zero. The sum of the rough-Laplacian, curvature, and divergence-norm terms is

\[
n\lambda\mathbb E[u^2]-\tfrac{n-2}{2}\mathbb E|du|^2.
\]

The complete formula (2.2), including the negative resolvent and scaling penalties, follows. Its polarization with constants vanishes, so the scaling check is stronger than just testing `u=1`. The Einstein specialization factors correctly and has the correct conformal gauge and neutral endpoints.

For `Fg`, the `4λm₂` part of the resolvent exactly cancels the apparent positive quadratic term. Equations (3.5) and (3.6), their strict-sign condition, and upper bound (3.8) are correct. The identities `E(FS)=λm₃`, `E(F²S)=2λm₄/3`, and `E(F|Hess f|²)=0` are valid weighted integrations. Neither the upper bound nor the forced scalar eigenvalue supplies a positive lower bound.

The scalar-eigenfunction expression retains the multiplication coefficients of `Fu`, which cannot be discarded in the non-Einstein situation. The possible constant component of `Fu` contributes zero to the forcing: either its mean vanishes by orthogonality to `F`, or its coefficient `2λ−μ` vanishes.

For the exponential tensor, `div_f(e^F g)=0`, its projection coefficient `nM(1)/E[R]` is correct, and its nonvanishing argument is valid in the non-Einstein range. Integrating `div_f(e^{2F}∇F)` gives the required `E(e^{2F}S)=λM′(2)`. The scalar-curvature forcing, variance penalty, and covariance rewriting in Section 6 are also correct. All these are conditional tests, not universal signs.

### Turn 3: coupled matrix — PASS

Both divergences are exact gradients. The stated scalar correction coefficient

\[
k(\mu)=\frac{\mu(\mu-2)}{2(\mu-1)}
\]

and its polarization are correct. Self-adjointness gives the displayed mixed leading entry. Independently, the scalar evolution equation implies

`E(u²|Ric|²)=3E(u²R)−E(SR)`,

which verifies its alternate expression. The Ricci overlaps satisfy `E(u|Ric|²)=2E(uR)`, producing exactly the rank-one penalty `−c²(2p+q)²/m`.

An independent cross-attempt calculation reduces the conformal diagonal via `k(A)` and the potential moments to Turn 2's formula (3.6). The gradient-square representative and its displayed divergence are correct. The unknown sign of the resulting matrix remains genuinely unknown.

### Turn 5: exact corrections and bundle transform — PASS

For `h=φT`, `b=T(∇φ,·)` and `D=div_f b=T:Hess φ` are correct. Formula (4.3) includes all four effects: ground-state energy, Ricci projection, divergence norm, and negative resolvent. Decomposing `b=du+β` gives exactly formula (4.4). Its negative scalar coefficients occur only for eigenvalues in `(1,2)`. The local sufficient test (4.5), and the reverse necessary inequality under stability, follow with the claimed inequality direction.

The scalar positivity argument ensures `r>0`, so no logarithm or weighted ellipticity degeneracy is hidden. Equations (5.1)–(5.3) are correct, including the positive `|∇U|²/2` zeroth-order term. For `k=φU` it cancels exactly; for transverse tensors the curvature term has no controlled sign. The Bochner identities and gauge zero mode in Section 6 do not supply an additional rigidity equation. The packet correctly refuses the invalid tensor positive-ground-state and scalar-gap-comparison shortcuts.

## 6. Finite quotients — PASS for precisely the two stated surfaces

On a connected compact shrinker, an isometry changes the normalized potential by zero. Thus it preserves the weighted operator and quotient conditions. Quotient instability is equivalent to a nonzero invariant vector in the positive spectral subspace upstairs; averaging an arbitrary unstable tensor can indeed annihilate it.

For the two indicated surfaces, the geometric/topological exclusion is valid:

- Their simply-connected compact topology allows the de Rham argument. A reducible Kähler shrinker here would have compact shrinking surface factors and therefore the `S²×S²` topology, contrary to the two blowups. Irreducibility and non-Ricci-flatness then make the parallel complex structure unique up to sign.
- An isometry is consequently holomorphic or antiholomorphic. A freely acting finite holomorphic subgroup is impossible because the holomorphic Euler characteristic is 1 and multiplies by the degree of a finite étale cover. The sign homomorphism therefore injects any free isometry group into a group of order two.
- The two-point blowup has Euler characteristic 5, excluding a free involution.
- For `F₁`, an antiholomorphic involution preserves the unique exceptional curve and descends to `CP²`. Writing its lift as `A(z)=B\bar z`, one has `A²=cI` with `c` real and `c³=|det B|²>0`. It can therefore be normalized to an antilinear involution, whose fixed projective locus is a copy of `RP²`. Fixed points away from the blowdown center lift, so the involution is not free.

These arguments rule out this quotient construction on Koiso–Cao and Wang–Zhu only. They give no classification of all compact shrinkers, no exclusion of higher-dimensional quotients, and no result for orbifold quotients. Those scope limits in the packet are necessary and correctly stated.

## 7. Required repairs and optional improvements

### Required repairs

None for the partial results and their conditional scope. The universal problem must continue to be labeled unresolved by these five attempts. It cannot be promoted to solved on the basis of this audit.

### Optional exposition improvements

1. State “smooth, connected, closed” once in the shared conventions for Turns 1–3. Turn 5 already does so. This makes explicit the ordinary connected-manifold convention behind a scalar mean-zero spectral basis and positivity of `A−λ` on that space.
2. At Turn 4, line 17, add that the two blowups are simply connected before the global product/holonomy argument. The proof is valid as written for these surfaces; this extra sentence prevents its accidental reuse on a nonsimply-connected manifold without passing to a cover.
3. In any extracted theorem, say “linearly ν-stable” and retain the non-Einstein hypothesis when invoking `κ≥0`. The underlying comparison for Einstein metrics is separately trivial.
4. Describe this as an audited conditional criterion, without a novelty claim. A source dated 2024 establishing that a problem was then open does not by itself establish exhaustive literature status in 2026.
5. If publishing the packet rather than preserving the frozen record, update “unreviewed/pending” status only in a new revision or an external audit record. Do not rewrite the frozen evidence in place.

## 8. Final disposition

- Frozen integrity: PASS.
- Source scope and attribution: PASS, subject to the literature-status boundary above.
- Analytic formulas, signs, normalization, and quotient removal: PASS.
- Turn 5 conditional theorem and multiplicity statement: PASS.
- Finite-quotient exclusion for the two named surfaces: PASS.
- Supplied algebra replay: 9/9 PASS.
- Independent formal audit checks: 8/8 PASS.
- Required mathematical repairs: none.
- Universal strict gap comparison: NOT PROVED.
- Original all-dimensional compact nontrivial-soliton instability problem: NOT SOLVED BY THIS PACKET.

The appropriate endpoint is an independently checked partial-result packet with an exhausted five-attempt ledger, not a universal theorem or counterexample.
