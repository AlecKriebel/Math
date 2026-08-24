# K2P edge domain, subdivision, and admissible rooting

For an edge with Fourier spectrum \((1,s,g,s)\), inverse Fourier transform
gives transition probabilities

\[
 \frac{1+2s+g}{4},\quad \frac{1-g}{4},\quad
 \frac{1-2s+g}{4},\quad \frac{1-g}{4}.
\]

Thus the strict nonsingular stochastic cone is exactly

\[
1-g>0,\qquad 1+2s+g>0,\qquad 1-2s+g>0,
\qquad sg\ne0.
\]

Its positive-eigenvalue component is

\[
\mathcal D_+=\{0<s<1,\ 0<g<1,\ g>2s-1\}.
\]

Every strict nonsingular edge can be subdivided into two strict nonsingular
edges.  Choose

\[
0<\varepsilon<
\min\{1-g,1+2s+g,1-2s+g,1\}
\]

and set

\[
(s_B,g_B)=(1-\varepsilon,1-\varepsilon),\qquad
(s_A,g_A)=\left(\frac{s}{1-\varepsilon},
                  \frac{g}{1-\varepsilon}\right).
\]

The four displayed bounds are precisely the strict inequalities for the two
factors after multiplication by \(1-\varepsilon>0\), and their coordinatewise
product is \((s,g)\).  This also preserves the positive component whenever
the original edge lies in \(\mathcal D_+\).  Coordinatewise square roots are
not a valid substitute: \((s,g)=(9/10,801/1000)\) is strict stochastic, but
its square-root pair violates the third transition inequality.

The strict continuous-time cone is

\[
0<s<1,\qquad s^2<g<1.
\]

It is closed under power subdivision because
\(g^{1/m}>(s^{1/m})^2\) is equivalent to \(g>s^2\).

Finally, K2P transition matrices are symmetric and have the uniform
stationary distribution.  Moving a root reverses only edges without fixed
reticulation arrowheads, and reversibility leaves their transition kernels
unchanged.  Inserting a root inside an edge is realized by the strict
factorization above; suppressing it composes the two factors by
\((s_1s_2,g_1g_2)\).  Therefore every admissible rooting of a fixed
semi-directed network has the same strict physical image on
\(\mathcal D_+\), and likewise on the continuous-time cone.
