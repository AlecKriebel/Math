# Independent determinant and torsor Euler check

Checkpoint: 2026-10-07 05:39:20 UTC. Assigned-check completion estimate: 100%.

Scope: independently attempt to falsify the determinant numerical extraction and torsor Euler lemma in the pinned companion source. Only `AGENTS.md`, `build/sections/06-descent.tex`, and (for the free-action implication) `build/sections/05-curves.tex` were read. No existing research notes, reviews, or audits were read. No publication, external communication, or tracker changes were made.

Source SHA-256:

- `06-descent.tex`: `0f63e6a6cc362f49f582c1794291d97f1d2e1599b05ed4bb181655c0032e91dd`.
- `05-curves.tex`: `5cfe4627325738e6b311be9521afe2d8ab5fc3f2b9557bdecf162baad70a8774`.

## Strongest verified result

No defect was found in the assigned determinant or Euler claims. Conditional on the preceding construction of the twisted module, the determinant line in 06-descent.tex:202–209 cancels its scalar weight, has a unimodular mixed first Chern class, and extracts the rank with coefficient ±1. The torsor Euler identity in 06-descent.tex:353–385 holds for an arbitrary projective scheme, including a singular or nonreduced one. These checks do not independently verify the preceding generic module construction or the later index comparison.

## 1. Determinant first Chern class: no missing factor of two

For one curve pair let

\[
D=\lambda(A\otimes V)^{-1}\otimes\lambda(A)\otimes\lambda(V),
\qquad \lambda(W)=\det Rq_*W.
\]

GRR gives the degree-two class of the virtual pushforward by integrating the degree-four part of

\[
\bigl(-e^{a+v}+e^a+e^v\bigr)\operatorname{td}(C),
\quad a=c_1(A),\;v=c_1(V).
\]

The constant term is 1, the degree-two term is exactly 0, and the degree-four term is

\[
-\frac{(a+v)^2}{2}+\frac{a^2}{2}+\frac{v^2}{2}=-av.
\]

The relative Todd class is supported in degrees zero and two on the curve, so neither the constant nor the vanished degree-two term changes this result. Consequently

\[
c_1(D)=-q_*(av).
\]

This independently verifies 06-descent.tex:299–308. The coefficient is one: the factor 2 in the square of the sum cancels the denominator 2.

## 2. Normalization and the integral mixed lattice

Normalization at the fixed curve point implies that the H²-of-parameter component of each universal first Chern class vanishes: restrict the universal line to that point, where it is trivial. Degree zero implies that `a` also has no pure H²(C) component. The degree-one pure curve component of `v` contributes nothing to `av`, since it would require H³(C). Thus `c1(D)` is purely in H¹(Pic⁰(C)) tensor H¹(Pic¹(C)); see 06-descent.tex:310–315.

Choosing the same curve point identifies Pic¹(C) with Pic⁰(C) by tensoring with O_C(−c₀). Under that identification the mixed component of `V` is the same Poincaré mixed component as that of `A`. A different choice introduces a translation, which acts trivially on H¹. The Abel pullback of a normalized universal line is the diagonal line with its two pure components removed. Hence its mixed component induces an integral isomorphism of first-cohomology lattices, rather than merely a rational isomorphism. This verifies the normalization and lattice mechanism in 06-descent.tex:316–325.

Explicitly choose an integral curve basis `(η_i)` and parameter bases `(t_i)` and `(s_i)` in which the universal mixed classes are

\[
a=\sum_i t_i\wedge\eta_i,\qquad
v_{\rm mixed}=\sum_j s_j\wedge\eta_j.
\]

Writing `J_ij=∫_C η_i∧η_j`, moving the curve one-form past the second parameter one-form yields

\[
q_*(av)=-\sum_{i,j}J_{ij}t_i\wedge s_j,
\qquad c_1(D)=\sum_{i,j}J_{ij}t_i\wedge s_j.
\]

`J` is the integral unimodular intersection matrix. There is no passage to an isogeny lattice and no multiplying factor. For genus one a symplectic choice gives `θ=t₁∧s₂−t₂∧s₁` and `θ²/2=−t₁∧t₂∧s₁∧s₂`, so the integral is −1, not −4 or a multiple of two.

For real Picard dimension `d=2g_C`, the exterior algebra identity gives

\[
\int\frac{\theta^d}{d!}=\pm\det J=\pm1.
\]

The product pairs form separate blocks. Since every mixed factor has one degree on each side, attaining top degree on the auxiliary Picard factors already attains top degree on B. All positive-degree terms of `ch(γ)` therefore vanish from the integral. Picard torsors have trivial tangent bundles, so `td(Z)=1`. This proves the stated rank-extraction implication in 06-descent.tex:330–343, with a sign independent of `γ`.

## 3. Scalar weights and cocycle cancellation

For genus `g_C`, Riemann–Roch gives `χ(A)=1−g_C` and `χ(A⊗V)=χ(V)=2−g_C`. A scalar on a line induces its χ-th power on the determinant of its cohomology. Thus D has weights

\[
(-\chi(A\otimes V)+\chi(A),\;-\chi(A\otimes V)+\chi(V))=(-1,0).
\]

The first cancels the stipulated weight +1 of the Morita module; the second eliminates dependence on the degree-one universal-line identification. This checks 06-descent.tex:233–247. The same calculation works for a line pulled back from a parameter base by determinant projection formula, so it handles nontrivial Hom lines as well as scalar trivializations. Determinant functoriality makes composed line identifications compose before cancellation, and the aggregate weight on every scalar is zero. Thus there is no extra scalar character or cocycle introduced by this correction; see 06-descent.tex:248–259. This is conditional on the compatible twisted transport from 06-descent.tex:169–177, which is outside this numerical subcheck.

## 4. Torsor Euler identity on singular quotients

Let `δ:T′→Q` be the stated torsor of degree `a`, and put

\[
d=[\delta_*\mathcal O_{T'}]-a\in K^0(Q).
\]

On an integral closed support a vector bundle of rank `a` is generically isomorphic to the trivial rank-a bundle. Localization in coherent K-theory therefore puts `d` times its structure-sheaf class in smaller support dimension. Integral-support classes generate the support-filtration quotients, so `d` lowers that filtration on all G₀(Q). If `n=dim Q`, its operator satisfies `d^(n+1)=0`. This needs neither regularity nor smoothness and verifies 06-descent.tex:362–371.

Torsor base change gives `δ*δ_*O=O^(⊕a)`; hence `δ*d=0` in K⁰(T′). The projection formula, applied to arbitrary coherent classes, gives the operator identity

\[
(a+d)d=0,\quad\text{equivalently}\quad d^2=-ad.
\]

Together with nilpotence this even yields the integral annihilation identity `a^n d=0` on G₀(Q), because `d^(n+1)=(-a)^n d`. Therefore every `dα` is torsion, and the integer-valued Euler characteristic kills it. Finite pushforward and projection formula then imply

\[
\chi(T',\delta^*\alpha)
=\chi(Q,(a+d)\alpha)
=a\chi(Q,\alpha).
\]

This independently verifies 06-descent.tex:373–384. In particular there is no tacit smooth-Riemann–Roch assumption at the singular quotient.

## 5. Free Pic¹ action and arithmetic use

The supporting free-action proof in 05-curves.tex:357–366 is valid: if an order-r automorphism fixes a degree-one line, rescale its identification by an r-th root to obtain a cyclic linearization. Descent along the free cyclic action then makes the degree divisible by r, contradicting degree one. A nonidentity element of the product group acts nontrivially on at least one Pic¹ factor, giving the free product action used in 06-descent.tex:389–391.

For descended coherent sheaves with a commuting right Δ₀ action, each cohomology vector space is a finite module over the division algebra, and its k-dimension is a multiple of dim_k Δ₀=e₀². The torsor identity multiplies the Euler characteristic by e₁. Hence the numerical divisibility deduction in 06-descent.tex:400–409 is valid, conditional on the sheaf descent already stated there.

## Remaining gap for this subcheck

None in the assigned determinant/Euler mechanisms. Broader theorem validation still requires independent checks of the generic algebra/module descent, construction of the coherent class, and the later index comparison. No statement here promotes the full division theorem as verified.
