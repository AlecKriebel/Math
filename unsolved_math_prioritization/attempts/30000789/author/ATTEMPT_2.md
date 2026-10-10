# Approach 2: solve the Ricci-side obstruction

**Result:** the Ricci constraint is completely sharp in even dimensions; in odd dimensions it has a strict margin at the proposed central constant. This does not control the Weyl cubic.

Let \(S\) be symmetric, trace free, with eigenvalues \(s_i\), and put \(u=\sum s_i^2\), \(v=\sum s_i^4\). For \(T=S\wedge S\),

\[
\|T\|^2=\tfrac12(u^2-v),\quad
\operatorname{Ric}T=-S^2,\quad\operatorname{scal}T=-u.
\]

The scalar and traceless-Ricci pieces have norms
\(u^2/[2n(n-1)]\) and \((v-u^2/n)/(n-2)\). Orthogonality gives the exact identity

\[
\|P_W(S\wedge S)\|^2=
\frac{n^2-3n+3}{2(n-1)(n-2)}u^2-\frac{n}{2(n-2)}v.\tag{4}
\]

Cauchy–Schwarz says \(v\ge u^2/n\), with equality exactly when all \(s_i^2\) agree. Hence

\[
\mu_n^2\le\frac{n-2}{2(n-1)},\qquad L_n\le\frac n{n-2}.\tag{5}
\]

If \(n\) is even, take half the \(s_i\) equal to \(+1\) and half to \(-1\). Equality holds, proving
\(L_n=n/(n-2)\).

If \(n\) is odd and \(u=1\), equality cannot hold: equally sized nonzero magnitudes with an odd number of signs cannot sum to zero. The unit trace-free sphere is compact, so the maximum is strictly smaller. Therefore
\(L_n<n/(n-2)\). This argument proves strictness but does not evaluate the exact odd maximum.

## A quantitative necessary lower bound in odd dimensions

For \(n=p+q\), take \(p\) eigenvalues \(q\) and \(q\) eigenvalues \(-p\). For odd \(n\), choose \(p=(n-1)/2\), \(q=(n+1)/2\). Then

\[
\frac v{u^2}=\frac{n^2+3}{n(n^2-1)},\qquad
\frac{\|P_W(S\wedge S)\|^2}{u^2}
=\frac{n^2(n-3)}{2(n-2)(n-1)(n+1)}.
\]

Thus

\[
\ell_n:=\frac{n^3(n-3)}{(n-2)^3(n+1)}\le L_n<\frac n{n-2},\qquad
\frac n{n-2}-\ell_n=\frac{4n}{(n-2)^3(n+1)}.\tag{6}
\]

No claim that \(\ell_n=L_n\) in odd dimensions is needed or made. In particular, (6) rigorously yields \(L_{11}\ge2662/2187\), which is enough for the dimension-11 obstruction in Approach 3.

An estimate with an absolute value, rather than the signed inner product, is harmless here because the Weyl sphere permits both signs. Restricting to positive curvature operators would destroy the independence of \(S\) and \(W\) used in this argument and would be a different problem.
