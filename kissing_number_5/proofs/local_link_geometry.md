# Exact local-link geometry and a contact-free maximal code

This note records universal local consequences of the spherical-code
inequalities, and an exact counterexample to a tempting contact-graph
assumption.  All statements use the non-strict convention
\(\langle x,y\rangle\leq 1/2\).

## 1. Conditional projection lemma

Let \(x_1,\ldots,x_k\in S^{d-1}\) be linearly independent, let
\(H=(\langle x_i,x_j\rangle)\), and fix \(b\in\mathbb R^k\).  Consider code
points \(y\) satisfying
\[
  \langle x_i,y\rangle=b_i\qquad(1\leq i\leq k).
\]
Put
\[
 q=\sum_{i=1}^k (H^{-1}b)_i x_i,\qquad
 Q=b^{\mathsf T}H^{-1}b.
\]
Then every such \(y\) has the unique decomposition \(y=q+r\), where
\(r\perp\operatorname{span}\{x_i\}\), and
\[
 \|q\|^2=Q,\qquad \|r\|^2=1-Q.
\]
Consequently:

* if \(Q>1\), there is no such point;
* if \(Q=1\), there is at most one such point;
* if \(Q<1\), the normalized residuals form a spherical code in dimension
  \(d-k\) with maximum inner product
  \[
    s'=\frac{1/2-Q}{1-Q}.
  \]

Indeed, the displayed formula for \(q\) gives
\(\langle x_j,q\rangle=b_j\), so \(r=y-q\) is orthogonal to every anchor.
For two points \(y=q+r\) and \(z=q+r'\),
\(\langle r,r'\rangle=\langle y,z\rangle-Q\leq 1/2-Q\).
This also proves all boundary cases.

## 2. Links of contact cliques in dimension five

Suppose the anchors form a contact \(k\)-clique, so their Gram matrix is
\[
 H=\frac{I+J}{2},
\]
and a common contact neighbor has \(b=\frac12\mathbf 1\).  Direct inversion
gives
\[
 H^{-1}=2\left(I-\frac{J}{k+1}\right),\qquad
 q=\frac{x_1+\cdots+x_k}{k+1},\qquad
 Q=\frac{k}{2(k+1)}.
\]
The preceding lemma therefore sends the common link to a code in
\(S^{4-k}\) with maximum inner product \(1/(k+2)\).

The following exact bounds result:
\[
\begin{array}{c|c|c}
k&\text{residual code}&\text{number of common contact neighbors}\\ \hline
1&A(4,1/3)&\leq15\\
2&A(3,1/4)&\leq7\\
3&A(2,1/5)&\leq4\\
4&A(1,1/6)&\leq2\\
5&\text{zero-dimensional residual of positive norm}&0.
\end{array}
\]
In particular, if \(\Gamma\) is the contact graph of any five-dimensional
kissing configuration, then
\[
 \deg_\Gamma(v)\leq15,\qquad
 (A_\Gamma^2)_{uv}\leq7\quad(u\ne v),\qquad
 \omega(\Gamma)\leq5.
\]

Here are proofs or precise sources for the small-code bounds.

### The bound \(A(4,1/3)\leq15\)

For \(S^3\), use normalized Gegenbauer polynomials \(P_i(1)=1\).  The
polynomial
\[
 f(t)=(t+1/2)^2(t+1)(t-1/3)
\]
has the exact expansion
\[
 f=\frac3{16}P_0+\frac23P_1+P_2+\frac56P_3+\frac5{16}P_4.
\]
All coefficients are positive, and \(f(t)\leq0\) on \([-1,1/3]\).
The Delsarte argument gives \(A(4,1/3)\leq f(1)/(3/16)=16\).

If equality held for a 16-point code, every off-diagonal inner product would
be a root of \(f\), hence one of \(-1,-1/2,1/3\), and the positive
\(P_1\)-coefficient would force the centroid to be zero.  Fix a code point
and let \(a,b,c\) count its other inner products equal to
\(-1,-1/2,1/3\), respectively.  Then
\[
 a+b+c=15,\qquad 1-a-\frac b2+\frac c3=0,
\]
and hence \(8a+5b=36\).  Since a point has at most one antipode,
\(a\in\{0,1\}\), but neither \(b=36/5\) nor \(b=28/5\) is integral.
Thus equality is impossible and \(A(4,1/3)\leq15\).

For calibration, the certificate checked by
`verifiers/verify_local_links.py` gives 14 exact rational points with
maximum inner product
\[
 \frac{87202900460}{267992911109}<\frac13.
\]
Thus this elementary argument leaves only \(14\) versus \(15\).

### The bound \(A(3,1/4)=7\)

We use the classical exact solution of the eight-point Tammes problem:
every eight points on \(S^2\) contain two with inner product at least
\[
 \frac{2\sqrt2-1}{7}>\frac14.
\]
This is the \(N=8\) case of Schütte and van der Waerden,
*Auf welcher Kugel haben 5, 6, 7, 8 oder 9 Punkte mit Mindestabstand eins
Platz?*, Math. Ann. **123** (1951), 96--124,
<https://doi.org/10.1007/BF02054944>.
Therefore \(A(3,1/4)\leq7\).  The exact rational seven-point certificate
checked by the verifier has maximum inner product
\[
 \frac{1006574101}{4532479101}<\frac14,
\]
so equality holds.

### The one- and two-dimensional bounds

For \(S^1\), among five consecutive angular gaps at least one is at most
\(2\pi/5\), whose cosine is \(>1/5\); hence \(A(2,1/5)\leq4\).
Four equally spaced points show equality.  On \(S^0=\{-1,+1\}\), at most
two points are possible, so \(A(1,1/6)=2\).

## 3. A pair-dependent common-neighbor bound

Let \(x,z\) have inner product \(\rho\), and consider their common contact
neighbors.  For \(\rho>-1/2\), applying the projection lemma to
\[
 H=\begin{pmatrix}1&\rho\\ \rho&1\end{pmatrix},
 \qquad b=(1/2,1/2)^{\mathsf T}
\]
gives
\[
 Q=\frac1{2(1+\rho)},\qquad
 s'=\frac{\rho}{1+2\rho}
\]
in \(S^2\).  If \(\rho=-1/2\), the residual norm is zero and there is at
most one neighbor; if \(\rho<-1/2\), there is none.  For
\(-1/2<\rho\leq0\), \(s'\leq0\), and the orthoplex bound gives at most six
points.  For \(0\leq\rho\leq1/2\), \(s'\leq1/4\), and the preceding
\(A(3,1/4)=7\) result gives at most seven.  Thus every distinct pair has at
most seven common contact neighbors, whether or not the pair itself is an
edge.

For completeness, the orthoplex bound used here has a two-line proof.  If
\(y_1,\ldots,y_m\in S^{d-1}\) have nonpositive mutual inner products and
\(G\) is their Gram matrix, then
\[
 \operatorname{tr}(G^2)\geq\frac{(\operatorname{tr}G)^2}{d}
 =\frac{m^2}{d}.
\]
Since \(g_{ij}^2\leq-g_{ij}\) for \(-1\leq g_{ij}\leq0\),
\[
 \operatorname{tr}(G^2)
 \leq m-\sum_{i\ne j}g_{ij}
 =2m-\left\|\sum_i y_i\right\|^2\leq2m.
\]
Thus \(m\leq2d\).

## 4. Exact counterexample: maximal does not imply contact-rich

Let
\[
 C=\{\pm e_i:1\leq i\leq5\}\ \cup\
 \left\{\frac{\varepsilon}{\sqrt5}:
       \varepsilon\in\{\pm1\}^5,\ \prod_i\varepsilon_i=1\right\}.
\]
This has \(10+16=26\) points.  Its distinct inner products are drawn from
\[
 \{-1,0,\ \pm1/\sqrt5,\ 1/5,-3/5\},
\]
so all are strictly less than \(1/2\).  Its contact graph is empty.

Nevertheless, \(C\) is inclusion-maximal.  If a unit vector \(z\) could be
added, compatibility with every \(\pm e_i\) would imply
\(a_i=|z_i|\leq1/2\).  Thus
\[
 1=\sum_i a_i^2\leq\frac12\sum_i a_i,
 \quad\text{so}\quad S:=\sum_i a_i\geq2.
\]
Choose signs agreeing with \(z\).  If their product is \(+1\), an allowed
even-parity sign vector has dot product \(S\) with \(z\).  If the product
is \(-1\), flip a coordinate of minimum absolute value; zeros may be
assigned either sign.  In every case there is an allowed sign vector
\(\varepsilon\) such that
\[
 \varepsilon\mathbin{\cdot}z
 \geq S-2\min_i a_i
 \geq S-\frac{2S}{5}
 \geq\frac65>\frac{\sqrt5}{2}.
\]
Hence \(\langle \varepsilon/\sqrt5,z\rangle>1/2\), a contradiction.

This disproves, even with a substantial exact code, every unrestricted
premise asserting that an inclusion-maximal spherical code must have a
contact, a positive minimum contact degree, or an infinitesimal-jamming
structure encoded by its contact graph.  It does not concern a
cardinality-maximum code, so it does not by itself rule out a theorem
proved specifically for maximum configurations.
