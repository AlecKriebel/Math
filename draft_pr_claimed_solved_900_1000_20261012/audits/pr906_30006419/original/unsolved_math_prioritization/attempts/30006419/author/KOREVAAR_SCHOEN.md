# The Korevaar–Schoen restriction has a positive stress argument

Authored companion argument, 7 October 2026. AI-assisted and unrefereed; independent audit pending. No novelty or optimal-constant claim.

The counterexample in PROOF.md uses the Reshetnyak energy. This note addresses the different fixed energy

\[
 I_{\rm avg}(s)=\frac1\pi\int_{S^1}s(v)^2\,dv.
\]

**Theorem.** Let (X) be a complete metric space and (u\in W^{1,2}(S^2,X)) be locally minimizing for the Korevaar–Schoen energy, with the neighborhoodwise fixed-trace quantifier of Meier–Vikman–Wenger Definition 6.1. Then (u) is infinitesimally (4+\sqrt{17})-quasiconformal. The constant is deliberately nonsharp. No isoperimetric or topological target hypothesis is needed for this assertion.

It suffices that the metric Sobolev theory has the approximate metric differential and its chain rule under smooth domain diffeomorphisms, as in the source setting. The proof below uses no pointwise differentiability of a target norm.

## 1. Smooth domain variation despite nonsmooth seminorms

For a seminorm (s) on the Euclidean plane and a matrix (A\in GL^+(2)), put

\[
 F_s(A)=\frac{I_{\rm avg}(s\circ A)}{\det A}.
\]

Changing angular variables by (w=Av/|Av|) gives exactly

\[
 F_s(A)=\frac1{\pi(\det A)^2}
 \int_{S^1}\frac{s(w)^2}{|A^{-1}w|^4}\,dw. \tag{1}
\]

Indeed the angular Jacobian is (dw=(\det A)|Av|^{-2}dv), and (|Av|=|A^{-1}w|^{-1}). The integrand on the right is smooth in (A), regardless of smoothness or degeneracy of (s). Uniformly for (A) near the identity, the derivatives through any fixed order are bounded by a constant times (M(s)^2), where (M(s)=\max_{|w|=1}s(w)).

Differentiating (1) at the identity in direction (B) yields

\[
 DF_s(I)[B]=T(s):B,\qquad
 T(s)=\frac1\pi\int_{S^1}s(w)^2(4w\otimes w-2I)\,dw. \tag{2}
\]

The matrix (T(s)) is symmetric and tracefree, and its norm is bounded by a constant times (M(s)^2).

## 2. A holomorphic quadratic differential on the whole sphere

In a conformal domain coordinate (z=x+iy), let (s_z=\operatorname{ap\,md}u_z), computed in the coordinate Euclidean metric. Let (V) be a smooth vector field supported compactly inside a neighborhood on which (u) is minimizing. The domain maps (\phi_\varepsilon=\mathrm{id}+\varepsilon V), for sufficiently small positive and negative (\varepsilon), are diffeomorphisms equal to the identity near the neighborhood boundary.

Use (u\circ\phi_\varepsilon) as a competitor on a smaller smooth domain containing the support. The approximate metric differential chain rule and change of variables give the integrand (F_{s_z}(D\phi_\varepsilon\circ\phi_\varepsilon^{-1})). Its derivative is integrably dominated by (C M(s_z)^2), which is integrable by the Sobolev hypothesis. Thus differentiation under the integral and local minimality imply

\[
 \int T(s_z):DV(z)\,dz=0. \tag{3}
\]

Write (T=\begin{pmatrix}a&b\\b&-a\end{pmatrix}), where (a,b\in L^1_{\rm loc}). Equation (3) is precisely

\[
 a_x+b_y=0,\qquad b_x-a_y=0
\]

in distributions. Therefore (q=a-ib) satisfies (\bar\partial q=0), and the distributional Weyl lemma makes (q) holomorphic on each coordinate neighborhood.

These are a single global quadratic differential, not unrelated local choices: formula (2) assigns a unique stress to every seminorm. For (\lambda>0) and an oriented Euclidean rotation (R), direct substitution gives

\[
 T(\lambda s)=\lambda^2T(s),\qquad
 T(s\circ R)=R^TT(s)R.
\]

Under a holomorphic coordinate change (z=z(w)), the differential seminorm composes with multiplication by (dz/dw). The preceding transformation law gives (q_w=(dz/dw)^2q_z). Hence (q_z\,dz^2) is a globally defined holomorphic quadratic differential on (S^2), including both poles: each pole has its own minimizing coordinate neighborhood, with (L^1) stress and the same weak equation there. No puncture-removal assumption is substituted for this local argument.

Such a differential vanishes. For example, its coefficient in a plane stereographic coordinate is entire, and holomorphy in the coordinate (w=1/z) at infinity gives (q_z=O(|z|^{-4})). Liouville's theorem implies (q_z=0). Thus

\[
 T(s_z)=0\quad\text{almost everywhere}. \tag{4}
\]

## 3. A quantitative seminorm lemma

Suppose (s\ne0), (T(s)=0). Normalize (M(s)=1), and put (m=\min_{|v|=1}s(v)). Choose an orthonormal basis with (s(e_2)=m), and set (L=s(e_1)). The triangle inequality gives

\[
 s(v)\leq L|v_1|+m|v_2|\leq\sqrt{L^2+m^2}\qquad(|v|=1),
\]

so (L^2\geq1-m^2). For the rank-one seminorm (r(v)=L|v_1|), the reverse triangle inequality gives

\[
 |s(v)-r(v)|\leq m|v_2|\leq m.
\]

Both (s) and (r) are at most one on the unit circle, whence (|s(v)^2-r(v)^2|\leq2m). Since the operator norm of (4v\otimes v-2I) is two, (2) implies

\[
 \|T(s)-T(r)\|_{\rm op}\leq8m. \tag{5}
\]

The elementary fourth angular moments give

\[
 T(r)=L^2\operatorname{diag}(1,-1).
\]

Combining (4) and (5),

\[
 1-m^2\leq L^2\leq8m,
 \qquad m\geq\sqrt{17}-4>0.
\]

Undoing normalization yields

\[
 \frac{M(s)}{m(s)}\leq\frac1{\sqrt{17}-4}=4+\sqrt{17}.
\]

At points where (s=0) the quasiconformality inequality holds trivially. This proves the theorem.

A qualitative alternative is compactness: the normalized set (M(s)=1) is compact, stress depends continuously on (s), and every nonzero rank-one seminorm has nonzero stress. Hence the balanced normalized set stays uniformly away from degeneracy. The explicit bound above makes this compactness step unnecessary.

## 4. What the argument does and does not show

For an inner-product seminorm (s(v)^2=v^TGv), (2) gives (T(s)=2G-\operatorname{tr}(G)I), recovering the classical weak conformality conclusion. That smooth-target special case is classical and is not claimed as new.

For general normed tangent planes, (T(s)=0) only means angular balance. A fourfold-rotation-invariant non-Euclidean norm has zero stress without being round. The theorem therefore asserts bounded distortion, not conformality or Reshetnyak infinitesimal isotropy.

This proof cannot be transferred to (I_+(s)=M(s)^2) by comparability of energies. The corresponding domain-variation density is nonsmooth, so no unique stress is obtained from (2). The explicit locally minimizing Reshetnyak example in PROOF.md shows that a transfer claiming the same conclusion would be false.

Source context: D. Meier, N. Vikman, S. Wenger, *Energy minimizing harmonic 2-spheres in metric spaces*, https://arxiv.org/abs/2503.08553, Definitions 2.1, 2.3, 3.1, 6.1. Sobolev metric differentiation and domain chain rules are standard inputs; all stress computations and the quantitative seminorm estimate are provided above. First priority and exhaustive literature coverage are not asserted.
