# Approach 1: an exact global tangency reduction

**Result:** the full ODE problem is equivalent to two algebraic extrema. This is a reduction, not the missing estimate.

Fix \(n\ge4\). Identify \(\Lambda^2\mathbb R^n\) with \(\mathfrak{so}(n)\), using \(e_i\wedge e_j\), \(i<j\), as an orthonormal basis. Curvature norms and inner products are operator Hilbert–Schmidt norms. For symmetric endomorphisms,
\((A\wedge B)(x\wedge y)=\tfrac12(Ax\wedge By+Bx\wedge Ay)\).
Thus \(I=\mathrm{id}\wedge\mathrm{id}\), \(\|I\|^2=N=\binom n2\), and \(S\wedge S\) has diagonal entries \(s_is_j\) when \(S\) is diagonal.

Write \(R=aI+E(S)+W\), where \(E(S)=2S\wedge\mathrm{id}/(n-2)\), \(\operatorname{tr}S=0\), \(\operatorname{Ric}W=0\). Then \(\operatorname{Ric}R=(n-1)a\mathrm{id}+S\) and \(\operatorname{scal}R=n(n-1)a\).

## Evolution identities

Let \(B(X,Y)=\tfrac12(Q(X+Y)-Q(X)-Q(Y))\). The trilinear form \(\langle B(X,Y),Z\rangle\) is symmetric. Standard curvature-algebra identities give

\[
\operatorname{scal}Q(R)=|\operatorname{Ric}R|^2,\qquad
B(I,W)=0,\qquad Q(W)\in\mathcal W,
\]

where \(\mathcal W\) is the Weyl subspace. Consequently, for any Ricci-type \(T\),
\(\langle B(T,W),W\rangle=\langle T,Q(W)\rangle=0\).

For completeness, diagonalize \(S\). The diagonal entries of \(Q(E(S))\) are

\[
\frac{(n-2)s_is_j-s_i^2-s_j^2+|S|^2}{(n-2)^2}.
\]

The last three terms are Ricci/scalar type, so
\(P_WQ(E(S))=P_W(S\wedge S)/(n-2)\). Orthogonal equivariance extends this to every symmetric \(S\). These identities also follow in the stated normalization from Xu's preprint §2.3 and the Böhm–Wilking identities cited there.

Therefore

\[
a'=(n-1)a^2+\frac{|S|^2}{n(n-1)},\qquad
\langle W,W'\rangle=\langle Q(W),W\rangle+
\frac{\langle S\wedge S,W\rangle}{n-2}.
\]

On a smooth boundary point \(a>0,\|W\|^2=cNa^2\), differentiation yields

\[
\frac12\frac d{dt}(\|W\|^2-cNa^2)=
\langle Q(W),W\rangle-cN(n-1)a^3
+\frac{\langle S\wedge S,W\rangle}{n-2}-\frac{ca}{2}|S|^2.\tag{1}
\]

## Necessity and sufficiency away from the apex

The variables \(S\) and \(W\) can be chosen independently. At \(S=0\), (1) is nonpositive for every boundary \(W\) exactly when

\[
\beta_n\sqrt{cN}\le n-1.\tag{2}
\]

For fixed \(W\), replacing \(S\) by \(tS\) forces the quadratic coefficient to be nonpositive. Maximizing over the direction of \(W\), which can align with \(P_W(S\wedge S)\), this is equivalent to

\[
\sqrt{cN}\mu_n\le\frac{c(n-2)}2.\tag{3}
\]

Conversely, (2) and (3) separately make the two groups of (1) nonpositive. The maxima defining \(\mu_n,\beta_n\) exist by compactness of finite-dimensional unit spheres. Changing \(W\) to \(-W\) makes the maximum cubic ratio also the maximum absolute cubic ratio, and the explicit tensor in Approach 3 proves \(\beta_n>0\).

## The nonsmooth locus cannot be omitted

When \(a=0\), the cone requires \(W=0\), but \(S\) is arbitrary. At \(E(S)\), the tangent cone consists of variations obeying
\(\dot a\ge0\) and \(\|\dot W\|\le\sqrt{cN}\dot a\), with unrestricted Ricci variation. Here

\[
\dot a=\frac{|S|^2}{n(n-1)},\qquad
\dot W=\frac{P_W(S\wedge S)}{n-2}.
\]

The tangent requirement is precisely (3), including \(S=0\). In particular, a zero derivative of the squared defining function at this locus is not a sufficient check.

The cone is closed and convex: it is a second-order cone in \((a,W)\) times the full traceless-Ricci space. The vector field \(Q\) is polynomial and locally Lipschitz. The finite-dimensional tangent-cone invariance theorem now gives preservation throughout the maximal ODE existence interval. This proves the equivalence

\[
C_c\text{ invariant}\quad\Longleftrightarrow\quad
L_n:=\frac{4N\mu_n^2}{(n-2)^2}\le c\le
U_n:=\frac{(n-1)^2}{N\beta_n^2}.
\]

The remaining challenge is a global sharp cubic estimate on all Weyl operators, not merely a check of \(Q\) on candidate extremizers.
