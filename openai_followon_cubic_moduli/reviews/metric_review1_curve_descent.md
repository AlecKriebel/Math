The equality is valid without either variety being \(\mathbb Q\)-factorial, provided the degree is defined by intersecting the determinant **Weil-divisor cycle** with the Cartier polarization.

Write \(n=\dim X\), \(d=\deg f\), and \(r=\operatorname{rk}F>0\). Choose a big open \(U\subset X\) on which \(X\) is smooth, \(f\) is étale, and \(F,T_X/F\) are locally free. This is possible because \(X\) is normal and \(F\) is saturated. On \(V=f^{-1}U\),
\[
T_Y|_V\simeq f^*(T_X|_U),\qquad
G|_V\simeq f^*(F|_U).
\]
The latter inclusion has locally free quotient. Consequently, saturation introduces **no codimension-one correction**.

Choose a rational section of \(\det F=(\bigwedge^rF)^{**}\), and let \(D\) be its Weil divisor. Its pulled-back section has divisor \(D_Y\), representing \(\det G\). At every prime divisor \(E\subset Y\) over a prime divisor \(P\subset X\), étaleness gives
\[
\operatorname{coeff}_E(D_Y)=\operatorname{coeff}_P(D).
\]
Moreover,
\[
\sum_{E\mapsto P}[k(E):k(P)]=d:
\]
the finite algebra over the DVR \(\mathcal O_{X,P}\) is finite étale of rank \(d\). Thus, as Weil cycles,
\[
f_*D_Y=dD.
\]
Applying the Cartier intersection projection formula repeatedly gives
\[
\deg_{f^*H}G
=\deg\!\left(c_1(f^*\mathcal O_X(H))^{n-1}\cap[D_Y]\right)
=d\,\deg_HF.
\]
Rank is preserved, hence
\[
\boxed{\mu_{f^*H}(G)=d\,\mu_H(F).}
\]
The needed projection formula applies to arbitrary cycles and invertible sheaves; it does not require the cycle \(D\) to be Cartier. See [Stacks, Lemma 42.26.4](https://stacks.math.columbia.edu/tag/02SU).

The proposed curve proof also works. For sufficiently large \(m\), take a general complete-intersection curve
\[
C=D_1\cap\cdots\cap D_{n-1}\subset U,\qquad D_i\in|mH|.
\]
Bertini and dimension counting allow \(C\) to be smooth and to avoid the entire codimension-two bad locus. Let \(C'=f^{-1}C\). Then
\[
m^{n-1}\deg_HF=\deg(F|_C),\qquad
m^{n-1}\deg_{f^*H}G=\deg(G|_{C'}).
\]
If \(C'=\coprod C_j'\) is disconnected, with covering degrees \(d_j\), degree is additive:
\[
\deg(G|_{C'})=\sum_j d_j\deg(F|_C)
=d\deg(F|_C).
\]
The curve pullback-degree formula is [Stacks, Lemma 33.44.11](https://stacks.math.columbia.edu/tag/0AYQ).

The only wording issue is that \(c_1(F)\) need not lie in the Cartier numerical space \(N^1(X)\). Define its degree through the determinant Weil cycle, and the argument is complete. Stability of \(T_Y\) is unnecessary for this equality; applying it afterward yields stability of \(T_X\).
