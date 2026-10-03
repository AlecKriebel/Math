# Independent adversarial audit: AMR-067-0014 / 6800014

Date: 2026-10-03 UTC.

## Verdict

**PASS: the frozen Attempt 2 proves the stated counterexample.** No mathematical repair is required. For every fixed `0 < u₀ < 1/2`, the displayed five-dimensional metric is a non-strict local maximum of `Scal²/|Ric|²` on **all** left-invariant metrics on its fixed simply connected solvable group, has value `1/3`, fails the algebraic solvsoliton equation, and has a same-group comparison metric with value `9/17`.

The conclusion concerns the original source's universal local-maximum assertion. It is not a novelty certificate, a claim that no prior proof exists, or verification of the inaccessible live aggregator page. This audit makes no remote changes and does not add an author research attempt.

One source-credit refinement is recommended: the **exact** family `J ⊕ tE₁₂` already appears as `D_t` in Lauret–Will I, §6.4, printed p. 20. Credit that appearance explicitly; do not describe the family itself as new. The frozen packet already disclaims novelty, so this is an attribution improvement, not a mathematical blocker.

## 1. Frozen inputs and audit scope

The supplied manifest hash is correct:

`f5446c816081c5322e4279bcd9a61dca5bfb63cfacf69d105d1587ed9d93b7fb`.

The main proof hash is correct:

`3009eff237f0c11059a2bed1241e04ac2dc5779f1c285c7138d4dc1ca1405472`.

All six publication-allowed files match their frozen SHA-256 digests and byte counts. They were read without alteration. The two author verification scripts both pass. More importantly, this audit separately derives the generic curvature formula and the block-slice expansion; its check script imports neither author script.

The mathematical proof, target scope, and relevant primary-source statements were audited. The packet's historical corpus hashes, queue state, prior-chat/repository search coverage, and exact accounting of author work before the freeze were not independently reconstructed. Those are provenance claims, not premises in the proof below.

## 2. Source statement and local-versus-global distinction

The original Morgan–Pansu source is accessible: [Question 14, §11, printed p. 12](https://www.imo.universite-paris-saclay.fr/~pierre.pansu/problems_MTDG.pdf). It concerns local maxima among left-invariant metrics on a solvable group and defines solvsoliton by `Ric = cI + D`, with `D` a derivation of that group's Lie algebra. It does not restrict to completely solvable groups, to metrics with an a priori orthogonal invariant splitting, or to global maxima.

[Lauret–Will I](https://arxiv.org/pdf/1808.01380), Theorem 1.5, distinguishes Ricci-soliton local maxima from solvsoliton global maxima. Proposition 6.11 isolates the exceptional commuting `N+C` family; the discussion following Lemma 6.12 leaves small-coefficient local maximality unresolved. Section 6.4 already gives the exact candidate family as `D_t`, including its value `1/3`. Thus the candidate is an established family whose local behavior is what the supplied argument proves.

[Lauret–Will II](https://arxiv.org/pdf/1907.08014), Theorems 1.1–1.2, concerns global maxima and imposes additional hypotheses in the abelian-nilradical result. It does not prove the universal local assertion being tested.

[Lauret's 23 July 2018 slides](https://www.ime.usp.br/~mtg/slides/j_lauret.pdf), slide 13/17, PDF pp. 71–73, announce nonglobal Ricci-soliton local maxima that are not solvsolitons. The later paper leaves their existence open. Both statements were independently located. Their discrepancy should remain disclosed; neither priority nor the reason for the discrepancy is established here.

The live `unsolvedmath.com/problems/6800014` request did not yield mathematical content in this audit. Its live wording is therefore not certified. The accessible original source is enough to determine the mathematical target actually disproved by this construction.

## 3. Lie algebra and curvature, independently from Koszul

The bracket `[e₀,X]=AX`, `[V,V]=0` satisfies Jacobi for every linear map `A:V→V`: every potentially nonzero Jacobi expression has at least two entries in the abelian ideal. Its derived algebra is contained in `V` and is abelian, so the Lie algebra is solvable. Lie's integration theorem gives the simply connected solvable group used in the claim.

Put `S=(A+Aᵀ)/2` and `K=(A−Aᵀ)/2`. The Koszul formula directly gives, for constant left-invariant `X,Y∈V`,

\[
\nabla_{e_0}e_0=0,\quad
\nabla_{e_0}X=KX,\quad
\nabla_Xe_0=-SX,\quad
\nabla_XY=\langle SX,Y\rangle e_0.
\]

With `R(U,V)=∇_U∇_V−∇_V∇_U−∇_[U,V]`, this yields

\[
R(e_0,X)e_0=(S^2+[S,K])X,
\]
\[
R(X,Y)Z=-\langle SY,Z\rangle SX+\langle SX,Z\rangle SY.
\]

Taking the Ricci trace, including the `e₀` contribution, gives

\[
\operatorname{Ric}_{00}=-\operatorname{tr}S^2,\qquad
\operatorname{Ric}_{0V}=0,\qquad
\operatorname{Ric}_{VV}=[K,S]-(\operatorname{tr}A)S
=\tfrac12[A,A^T]-(\operatorname{tr}A)S.
\]

The independent script also constructs the full connection and curvature matrices from the structure constants of a **generic** symbolic `4×4` matrix and checks this identity, including the nonzero-trace term. Thus it verifies the formula for the perturbed slice, not merely for the candidate.

For the trace-zero matrices here, `s=||S||²>0`, `q=||[A,Aᵀ]||²`, and

\[
F=\frac{s^2}{s^2+q/4},\qquad F\le\tfrac13\iff q-8s^2\ge0.
\]

At `A_u`, `s=u²/2`, `q=2u⁴`; the metric is nonflat and `F=1/3`. No division by zero occurs in a neighborhood: in the eventual slice, `s≥v²/2>0`.

## 4. Every nearby metric reduces to a nearby scaled conjugate

This step passes, including metrics whose cross terms between `e₀` and `V` are nonzero. An explicit construction makes the coverage transparent.

Write the Gram matrix of any nearby inner product as

\[
G=\begin{pmatrix}\alpha&\beta^T\\\beta&G_V\end{pmatrix},
\quad T=G_V^{-1/2},\quad
c=(\alpha-\beta^TG_V^{-1}\beta)^{-1/2}.
\]

The columns of `T` give an orthonormal basis of the **fixed** ideal `V`, and

\[
f_0=c(e_0-G_V^{-1}\beta)
\]

is the orthogonal unit complement. Since `V` is abelian, its extra component has zero adjoint action on `V`. The matrix in this orthonormal basis is exactly `c T⁻¹ A_{u₀} T`. As the metric tends to the original one, `c→1` and `T→I` continuously, indeed smoothly. No assumption about a fixed orthogonal decomposition has been imposed on the metrics.

Scalar multiplication of `A` multiplies `s` by the square and `q` by the fourth power, so it preserves `F`. Orthogonal conjugation also preserves `F`. Consequently a neighborhood result on the ordinary conjugacy class proves the required neighborhood result on the entire positive-definite metric cone. Unique parametrization is unnecessary.

## 5. The spectral projection and orthogonal slice cover all conjugates

Every conjugate satisfies `A⁴+A²=0`. Hence

\[
E(A)=I+A^2,\quad E(A)^2=E(A),\quad
\operatorname{im}E(A)=\ker A^2=W.
\]

The image has dimension two. Although `E(A)` generally is **not an orthogonal projection**, it is a smooth rank-two projection. This causes no gap: local frames of its image can be orthonormalized.

For complete local choices, take `p=E(A)e₄` and

\[
f_3=\frac{Ap}{\|Ap\|},\qquad
f_4=\frac{p-\langle p,f_3\rangle f_3}
{\|p-\langle p,f_3\rangle f_3\|}.
\]

At the base point the denominators are `u₀` and `1`, so these formulas are smooth nearby. They give `Af₃=0` and `Af₄=vf₃` with `v>0`, `v→u₀`. Orthogonally projecting `e₁,e₂` onto `W⊥` and applying Gram–Schmidt gives a smooth nearby frame there.

Since `W` is invariant, the upper-right block vanishes. The induced quotient map has characteristic polynomial `λ²+1`, so its real `2×2` matrix has trace zero and determinant one. Writing it as

\[
C=\begin{pmatrix}a&b-k\\b+k&-a\end{pmatrix}
\]

gives `k²=1+a²+b²`; closeness to `J` selects the positive root. The entire lower-left matrix `L=[[x,y],[z,w]]` survives. Thus the author's seven-variable slice, with six transverse variables and one flat parameter `v`, covers every nearby conjugate. It does not assume both summands are invariant or discard their nonorthogonal coupling.

## 6. Independent block derivation of the decisive polynomial

Let

\[
M=\begin{pmatrix}C&0\\L&N\end{pmatrix},\quad
N=\begin{pmatrix}0&v\\0&0\end{pmatrix}.
\]

Direct block multiplication, before any expansion or Taylor approximation, gives

\[
[M,M^T]=
\begin{pmatrix}
[C,C^T]-L^TL & CL^T-L^TN\\
LC^T-N^TL & LL^T+[N,N^T]
\end{pmatrix}.
\]

Therefore

\[
q=\|[C,C^T]-L^TL\|^2
+2\|LC^T-N^TL\|^2
+\|LL^T+[N,N^T]\|^2,
\]
\[
s=2(a^2+b^2)+\tfrac12(x^2+y^2+z^2+w^2+v^2).
\]

These are an independent route to the full expansion. Put `h²=a²+b²`, `r²=x²+y²+z²+w²`, and `d=wx−yz`. Substitution of `k²=1+h²` yields precisely

\[
P=Q_v+R,
\]
\[
Q_v=16(2-v^2)h^2
+2\{x^2+y^2+(1-3v^2)(z^2+w^2)+2vd\},
\]
\[
\begin{aligned}
R={}&-12h^2r^2-24ak(wz+xy)
+12bk(x^2+z^2-y^2-w^2)\\
&+4v\{a(wy-xz)-b(wx+yz)\}
+4v(k-1)d-4d^2.
\end{aligned}
\]

In particular, the absence of a pure `h⁴` term is correct: it cancels between `q` and `8s²`. The negative quartic term `−4d²` is retained, not overlooked. Every coefficient and sign in the frozen equations (3)–(5) agrees with this calculation.

## 7. Positivity, flat directions, and a quantitative uniform remainder

The author's completion of squares is exact:

\[
Q_v=16(2-v^2)h^2+2(x+vw)^2+2(y-vz)^2
+2(1-4v^2)(z^2+w^2).
\]

Hence it is positive definite for `0<v<1/2`. Each mixed two-variable block has underlying matrix `[[1,±v],[±v,1−3v²]]`, determinant `1−4v²`, and trace `2−3v²`.

The compact-interval argument in the proof is already sufficient. As an additional audit check, choose `0<v₋<u₀<v₊<1/2` and put `c₀=1−4v₊²`. The determinant/trace bound on the smallest eigenvalue gives the explicit uniform inequality

\[
Q_v(\xi)\ge c_0\|\xi\|^2\quad (v\in[v_-,v_+]).
\]

For `ρ=||ξ||≤1`, we have `k≤√2`, `k−1≤h²/2`, and `|d|≤r²/2`. Estimating the six displayed remainder terms separately gives

\[
|R|\le (13.5+25\sqrt2)\rho^3<50\rho^3.
\]

Thus `ρ≤min(1,c₀/100)` implies

\[
P\ge \tfrac12c_0\rho^2\ge0.
\]

This explicitly validates uniformity while `v` changes along the flat family. At `ξ=0`, `P` vanishes identically for all such `v`; when `ξ≠0` is sufficiently small, `P>0`. There is no inference from a semidefinite Hessian alone, and no uncontrolled higher-order drift along a kernel direction.

The resulting maximum is non-strict, as expected from the constant family and scale/isometry invariances. The original question does not require strictness. Neither endpoint `u₀=0` nor `u₀=1/2` is included or proved; no endpoint claim is needed.

## 8. Solvsoliton obstruction and nonglobal comparison

Direct curvature gives

\[
\operatorname{Ric}=
\operatorname{diag}(-u_0^2/2,0,0,u_0^2/2,-u_0^2/2).
\]

If `D=Ric−cI` is a derivation, it is this specific diagonal map, not an arbitrary derivation that might have off-diagonal entries. The nonzero rotation bracket forces `d₀=0`, hence `c=−u₀²/2`. Then `d₃=u₀²` and `d₄=0`; the bracket `[e₀,e₄]=u₀e₃` would require `d₃=d₀+d₄=0`. Since `u₀≠0`, this is a contradiction. The proof therefore excludes precisely the source's algebraic equation on the fixed Lie algebra. Being a Ricci soliton, or being isometric to a solvsoliton realized on another group, does not negate this obstruction.

For the matrix `B` in the frozen proof, both conjugations check exactly. With the given `T` and `H`, `B=(TH)A_{u₀}(TH)⁻¹`. Thus it is realized by a left-invariant metric on the same simply connected group. Independent Koszul curvature at `B` gives `F(B)=9/17`; equivalently `s(B)=3/2`, `q(B)=8`. The strict inequality `9/17>1/3` is correct. Global theorems are not being used to infer this comparison.

## 9. Required repairs and recommended publication edits

### Required mathematical repairs

**None.** The frozen main argument is complete at the level of an ordinary finite-dimensional differential-geometric proof.

### Recommended precise attribution edit

Add to `SOURCE_AUDIT.md`, under Lauret–Will I:

> Section 6.4, printed p. 20, already displays the exact family `D_t=J⊕tE₁₂` and computes `F(D_t)=1/3`. The construction here uses that known family; the local-slice argument establishes the required small-parameter local maximality directly.

An analogous one-sentence acknowledgment at the start of Attempt 1 would be appropriate. Preserve the existing no-novelty claim and the 2018/later-paper discrepancy disclosure. Do not label the live problem page verified.

### Optional exposition improvements

- Include the four Koszul connection identities to make the curvature formula self-contained for the whole slice.
- Give the explicit positive-definite Gram-matrix reduction or the explicit `f₃,f₄` formulas if a reader wants more detail about smooth local coverage.
- State explicitly that `E(A)` is not necessarily orthogonal and that ordinary orthonormalization supplies the needed orthogonal frame.
- State `s≥v²/2>0` and that the maximum is non-strict.

These are clarifications rather than repairs. The proof already contains their essential content.

## 10. Reproducible independent check

The companion `independent_checks.py` verifies:

1. The complete generic Koszul Ricci formula for every real `4×4` matrix.
2. The block commutator identity, full remainder, and quadratic extraction.
3. The positive mixed-block determinant and trace.
4. The candidate value, polynomial spectral projection, and derivation obstruction.
5. The conjugacy and `9/17` comparison by direct curvature.
6. The continued integrity of all six frozen author files.

All six checks passed with exact symbolic arithmetic. The coverage and uniform-neighborhood claims are established textually above, not delegated to numerical testing.
