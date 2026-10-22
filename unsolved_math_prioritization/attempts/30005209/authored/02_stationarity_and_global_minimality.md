# Approach 2: a complete planar analytic criterion

## Theorem

Let (P\subset\mathbb R^2\) be an open bounded convex polygon, with nonzero side lengths and no redundant collinear sides, containing the origin and satisfying |P|=1. Let \(\psi=h_P\), and fix (0<\alpha<2\). The following are equivalent:

1. (P\) minimizes (P_\psi+\gamma V_\alpha\), among all unit-area finite-perimeter sets, for at least one \(\gamma>0\).
2. The side averages
   \[
   A_i(P)=\frac1{\ell_i}\int_{L_i}v_P\,d\mathcal H^1
   \]
   are independent of (i\).
3. For all sufficiently small \(\gamma>0\), (P\) is the unique global minimizer modulo translations.

Implication 2→3 is the point requiring proof beyond merely writing the stationarity equations. The theorem does **not** explicitly classify the solutions of those equations.

## 1. Support-number coordinates and smooth transport

Write (P=P(h)=\bigcap_i\{x:x\cdot\nu_i<h_i\}\), with cyclically ordered normals. For small (s\in\mathbb R^n\), put (P_s=P(h+s)\). All sides remain present. Each vertex is the intersection of two successive supporting lines, and hence is an affine function of (s\).

Triangulate \(\overline P\) by joining 0 to its successive vertices. On each reference triangle define (F_s\) to be the affine map fixing 0 and taking its two boundary vertices to the corresponding vertices of (P_s\). The definitions agree on shared edges. Thus (F_s:\overline P\to\overline{P_s}\) is a continuous piecewise-affine bijection. For sufficiently small (s\), the triangles remain nondegenerate and form the fan triangulation of (P_s\).

Moreover
\[
F_s(x)=x+U_s(x),\qquad
\|U_s\|_{\operatorname{Lip}(P)}\le C|s|.
\]
The global Lipschitz estimate follows by integrating the bounded piecewise gradient along the segment joining any two points of the convex set (P\). In particular
\[
(1-C|s|)|x-y|\le |F_s(x)-F_s(y)|\le(1+C|s|)|x-y|.
\]
The Jacobian (J_s\) is, on each fixed triangle, a positive polynomial of degree at most two in (s\), with bounded derivatives of every required order.

Pulling back the interaction gives
\[
V_\alpha(P_s)=\int_P\int_P
 |F_s(x)-F_s(y)|^{-\alpha}J_s(x)J_s(y)\,dx\,dy.
\]
For a parameter derivative, each differentiated difference (\partial_{s_j}(F_s(x)-F_s(y))\) is bounded by (C|x-y|\). Differentiating the kernel once or twice therefore produces an integrand bounded by (C|x-y|^{-\alpha}\), including the Jacobian terms. For example the potentially worst second derivative is bounded by
\[
C|F_s(x)-F_s(y)|^{-\alpha-2}|x-y|^2
\le C'|x-y|^{-\alpha}.
\]
This is integrable on (P\times P\) precisely in the relevant range \(\alpha<2\). Dominated differentiation proves that (s\mapsto V_\alpha(P_s)\) is (C^2\), with bounded Hessian on a small parameter neighborhood. The same proof works for smoothly varying vertices, and gives arbitrarily many parameter derivatives on a fixed nondegenerate triangulation.

This argument avoids the misleading isolated boundary-to-boundary integral \(\iint_{L_i\times L_i}|x-y|^{-\alpha}\), which diverges when \(\alpha\ge1\). The cancellation comes from differences of a **single global Lipschitz transport field**.

## 2. First variation for all (0<\alpha<2\)

The potential (v_P\) is continuous. One direct proof splits the convolution into a ball of radius (r\), whose contribution is at most (Cr^{2-\alpha}\), and its complement, where the kernel is uniformly continuous under a small translation.

For (D_s=\chi_{P_s}-\chi_P\), the exact identity is
\[
V_\alpha(P_s)-V_\alpha(P)
=2\int D_s v_P+ \iint D_s(x)D_s(y)|x-y|^{-\alpha}\,dx\,dy.
\]
If \(\delta=|P_s\triangle P|\), the absolute value of the second term is at most
\[
C\delta^{2-\alpha/2}=o(\delta).
\]
Indeed, for a set (D\) of measure \(\delta\), splitting the potential integral at radius \(\sqrt\delta\) gives \(\|v_D\|_\infty\le C\delta^{1-\alpha/2}\). Since \(\delta=O(|s|)\), the remainder is (o(|s|)\).

The first term consists of signed thin strips of widths (s_i\) along the sides, plus (O(|s|^2)\)-area corner pieces. Continuity of (v_P\) yields
\[
DV_\alpha(P)[s]=2\sum_i s_iB_i,
\qquad B_i=\int_{L_i}v_P\,d\mathcal H^1.
\]
Likewise
\[
D|P_s|_{s=0}[s]=\sum_i\ell_i s_i.
\]
The area gradient is nonzero. Thus the unit-area parameter surface is smooth, and its tangent space is \(\ell^\perp\).

## 3. Necessity

On this fixed-normal class, (P_\psi(P_s)=\sum_i\psi(\nu_i)\ell_i(s)\) is smooth. Since (P\) minimizes its own anisotropic perimeter under area constraint, its derivative vanishes on \(\ell^\perp\).

If (P\) minimizes the total energy for any \(\gamma>0\), every sufficiently small two-sided constrained variation has zero first derivative. Hence \(\sum_i B_i s_i=0\) for every \(s\in\ell^\perp\). Linear algebra gives (B=A\ell\), which is condition 2.

Conversely, if two side averages differ, there is a tangent vector with nonzero first derivative of (V_\alpha\). The implicit function theorem realizes it by an exact area-preserving support path. Reversing its sign gives a strict energy descent for every fixed \(\gamma>0\), since the perimeter derivative vanishes. This excludes minimality for any positive γ.

## 4. Stationarity supplies a quadratic interaction bound

By the (C^2\) result,
\[
V_\alpha(P_s)-V_\alpha(P)=2A\sum_i\ell_i s_i+O(|s|^2)
\]
under condition 2. Area is a smooth function, so \(|P_s|=|P|\) gives \(\sum_i\ell_i s_i=O(|s|^2)\). Therefore
\[
|V_\alpha(P_s)-V_\alpha(P)|\le C|s|^2.
\]
For fixed (P\) and sufficiently small (s\),
\[
|s|\le C_P|P_s\triangle P|.
\]
For completeness, take a closed middle subsegment of each side, of positive length, away from the vertices. The other supporting inequalities have uniformly positive slack there. For all small (s\), the strip between the old and new supporting lines above this subsegment lies in the symmetric difference. Choose disjoint fixed neighborhoods of these subsegments. Their strip areas give a lower bound (c\sum_i|s_i|\), proving the estimate.

We have proved the two-sided bound
\[
|V_\alpha(Q)-V_\alpha(P)|\le C|Q\triangle P|^2
\tag{Q}
\]
for all sufficiently close equal-area polygons with the same normals. Translation invariance permits using a best aligned translate.

## 5. Global minimality, not merely constrained local minimality

We use the following established ingredients, as in the proof of BCT (2021), Theorem 2.5:

- Existence of a unit-area minimizer for small γ (Choksi–Neumayer–Topaloglu, *Anisotropic liquid drop models*, Theorem 3.1).
- Quantitative Wulff stability:
  \[
  P_\psi(E)-P_\psi(P)\ge c_P\delta(E)^2,
  \quad \delta(E)=\min_a|E\triangle(P+a)|.
  \]
- Planar crystalline rigidity of small perimeter quasiminimizers (Figalli–Maggi; Theorem 3.7 in the retrieved author manuscript, cited as Theorem 7 in BCT).

The elementary potential bound above implies, for unit-area sets,
\[
|V_\alpha(E)-V_\alpha(F)|\le L_\alpha|E\triangle F|.
\]
Let (E_\gamma\) be a minimizer. Comparison with (P\) gives
\[
c_P\delta(E_\gamma)^2
\le\gamma\bigl(V_\alpha(P)-V_\alpha(E_\gamma)\bigr)
\le\gamma L_\alpha\delta(E_\gamma).
\]
Hence \(\delta(E_\gamma)\le\gamma L_\alpha/c_P\), unless it is zero already. Also minimality against an arbitrary equal-area (F\) gives
\[
P_\psi(E_\gamma)\le P_\psi(F)+\gamma L_\alpha|E_\gamma\triangle F|.
\]
Thus (E_\gamma\) is an (O(\gamma)\) perimeter quasiminimizer. The rigidity theorem and its uniform proximity conclusion make (E_\gamma\), after translation, a close convex polygon with the normals of (P\). For small enough γ all of (P\)'s facets remain represented, so (Q) applies.

Combining (Q) with quantitative Wulff stability now yields
\[
0\ge \mathcal E_\gamma(E_\gamma)-\mathcal E_\gamma(P)
\ge(c_P-\gamma C)\delta(E_\gamma)^2.
\]
Choose γ smaller than the existence/rigidity/proximity thresholds and (c_P/C\). Then \(\delta(E_\gamma)=0\). Every minimizer is a translate of (P\), proving condition 3. Condition 3 trivially implies 1.

## Exact remaining gap

The theorem gives a finite-dimensional integral test but does not solve it geometrically. There are (n-3\) nontranslation constrained directions, and the zero set of their interaction derivatives remains to be classified for general (n\). Nor does this argument automatically cover nonsimple higher-dimensional polytopes, where arbitrary support shifts can change combinatorics and a single smooth vertex parametrization need not exist.
