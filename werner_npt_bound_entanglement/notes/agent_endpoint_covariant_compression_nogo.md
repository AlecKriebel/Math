# A no-go theorem for covariant dimension compression at the endpoint

## Status

This note does **not** prove or disprove unrestricted three-copy
positivity.  It settles one natural version of the dimension-reduction
question exactly.

One might hope to compress every local \(d\)-dimensional coefficient
matrix to \(k\) dimensions, average over a common Haar-random local
basis, and recover a positive multiple of the endpoint form
\[
 L_d(X)=X-\frac12\operatorname{Tr}(X)I_d.
\]
That is impossible whenever \(2\leq k<d\), even if the row and column
compression subspaces are allowed to differ and even if one mixes
arbitrarily many such compression orbits.  More strongly, correlating
the choices of compression orbit at different physical sites does not
repair the obstruction: no positive correlated mixture of tensor-product
compression orbits can reproduce a positive multiple of
\(L_d^{\otimes n}\).

The obstruction is local, so it rules out this averaging strategy for
three copies and for every other copy number.  It does not rule out a
non-covariant, state-dependent, or nonlinear dimension reduction.

The independent exact checker is
`verification/verify_endpoint_covariant_compression_nogo.py`.

## 1. Two-sided compression

Fix isometries
\[
 A,B:\mathbb C^k\longrightarrow\mathbb C^d,
 \qquad A^\dagger A=B^\dagger B=I_k.
\]
For \(U\in U(d)\), compress a coefficient matrix on its two sides by
\[
 {\cal C}_U(X)=A^\dagger U^\dagger XUB\in M_k.
\tag{1}
\]
Two-sided compression preserves matrix rank.  Pulling the \(k\)-dimensional
endpoint form back to \(M_d\), and averaging over normalized Haar measure,
defines a superoperator \({\cal A}_{A,B}\) by
\[
 \left\langle X,{\cal A}_{A,B}(Y)\right\rangle_{\rm HS}
 =
 \int_{U(d)}
 \left\langle{\cal C}_U(X),
 L_k({\cal C}_U(Y))\right\rangle_{\rm HS}\,dU .
\tag{2}
\]

Put
\[
 P_A=AA^\dagger,\qquad P_B=BB^\dagger,\qquad K=BA^\dagger,
\tag{3}
\]
and define
\[
 t=\operatorname{Tr}(P_AP_B)=\|A^\dagger B\|_2^2,\qquad
 s=\operatorname{Tr}(A^\dagger B).
\tag{4}
\]
Before Haar averaging, the pulled-back superoperator is
\[
 Y\longmapsto
 P_A YP_B-\frac12K^\dagger\operatorname{Tr}(KY).
\tag{5}
\]
Indeed, the first term is the pullback of the Hilbert--Schmidt norm,
while
\[
 \operatorname{Tr}{\cal C}_U(X)
 =\operatorname{Tr}(UKU^\dagger X)
\]
gives the second term.

## 2. The two invariant scalars

Haar covariance implies
\[
 {\cal A}_{A,B}(Y)=cY+e\operatorname{Tr}(Y)I_d
\tag{6}
\]
for two real scalars \(c,e\).  They are fixed by the superoperator trace
and the image of the identity.

The superoperator trace of (5) is
\[
 \tau=k^2-\frac k2=k\left(k-\frac12\right).
\tag{7}
\]
The first summand contributes
\(\operatorname{Tr}P_A\operatorname{Tr}P_B=k^2\), and the rank-one
superoperator in the second summand has trace
\(\|K\|_2^2=k\).

Also, Haar twirling (5) on the identity gives
\[
 {\cal A}_{A,B}(I_d)=\frac{h}{d}I_d,\qquad
 h=t-\frac12|s|^2.
\tag{8}
\]
Consequently
\[
 c d^2+ed=\tau,\qquad c+ed=\frac hd.
\tag{9}
\]

For (6) to be a positive scalar multiple of \(L_d\), it is necessary
and sufficient that
\[
 e=-\frac c2.
\tag{10}
\]
Equations (9)--(10) then force the exact ratio
\[
 \boxed{\qquad
 \frac h\tau=-\frac{d-2}{2d-1}.
 \qquad}
\tag{11}
\]

## 3. The obstruction

Cauchy--Schwarz applied to the \(k\times k\) matrix \(A^\dagger B\)
gives
\[
 |s|^2\leq k t.
\tag{12}
\]
Since \(0\leq t\leq k\),
\[
 h=t-\frac12|s|^2
 \geq-\frac{k-2}{2}\,t
 \geq-\frac{k(k-2)}2.
\tag{13}
\]
Dividing by (7) yields
\[
 \boxed{\qquad
 \frac h\tau\geq-\frac{k-2}{2k-1}.
 \qquad}
\tag{14}
\]
The function
\[
 x\longmapsto\frac{x-2}{2x-1}
\]
is strictly increasing for \(x>1/2\).  Hence, when \(k<d\),
\[
 -\frac{k-2}{2k-1}>
 -\frac{d-2}{2d-1},
\tag{15}
\]
contradicting the required ratio (11).

This proves:

### Theorem

Let \(2\leq k<d\).  No Haar-covariant average of two-sided
rank-preserving \(k\)-dimensional isometric compressions has pulled-back
endpoint form equal to a positive scalar multiple of \(L_d\).

The same conclusion holds for an arbitrary positive mixture of fixed
pairs \((A,B)\): equation (7) is the same on every orbit, and the linear
bound (14) is preserved by positive averaging.

When \(k=d\), equality in (12)--(14) and (11) requires
\[
 t=k,\qquad |s|^2=k^2.
\]
Thus \(A^\dagger B\) is a scalar unitary, and the construction is only
the trivial full-dimensional change of basis.

## 4. Correlations between sites do not help

The preceding one-site obstruction has a tensor consequence which is
slightly stronger than independent averaging.  On the traceless
operator space, (6) has eigenvalue \(c\).  On the identity direction
its eigenvalue is
\[
 \lambda_0=c+ed=\frac hd.
\tag{16}
\]
Solving (9) without imposing the endpoint relation gives
\[
 c=\frac{\tau-h/d}{d^2-1}>0.
\tag{17}
\]
If \(x=h/\tau\), the identity-to-traceless eigenvalue ratio is therefore
\[
 r_d(x)=\frac{\lambda_0}{c}
 =\frac{x(d^2-1)}{d-x}.
\tag{18}
\]
This function is strictly increasing for \(x<d\).  The endpoint value
\[
 x_d=-\frac{d-2}{2d-1}
\]
satisfies
\[
 r_d(x_d)=1-\frac d2,
\tag{19}
\]
which is exactly the identity-to-traceless eigenvalue ratio of \(L_d\).
For every proper \(k\)-dimensional compression, (14)--(15) instead give
\[
 x\geq-\frac{k-2}{2k-1}>x_d,
\qquad
 r_d(x)>1-\frac d2.
\tag{20}
\]

Now allow an arbitrary positive mixture of products of local compression
orbits at \(n\) sites; the choices at different sites may be correlated.
For a term \(q\) in the mixture, write its local traceless eigenvalues
as \(c_{q,j}>0\) and its ratios as \(r_{q,j}\).  The coefficient of the
all-traceless sector is
\[
 \sum_q w_q\prod_{j=1}^n c_{q,j}>0.
\tag{21}
\]
The ratio of the coefficient of the sector which is identity at site
\(1\) and traceless at every other site to (21) is
\[
 \frac{\sum_q w_q r_{q,1}\prod_jc_{q,j}}
      {\sum_q w_q\prod_jc_{q,j}}.
\tag{22}
\]
It is a convex combination of the \(r_{q,1}\), all of which are
strictly larger than \(1-d/2\) by (20).  But the same sector ratio for
\(L_d^{\otimes n}\) is exactly \(1-d/2\).  Hence:

### Tensor-correlated no-go theorem

For \(n\geq1\), no positive mixture of tensor products of Haar-covariant,
two-sided, rank-preserving proper compression orbits is a positive
multiple of \(L_d^{\otimes n}\), even when the orbit choices are
arbitrarily correlated between the \(n\) sites.

The argument also allows the proper output dimension \(k\) and the two
compression subspaces to vary from term to term and site to site.

## 5. Consequence for the Werner program

If the pulled-back local form had been exactly \(cL_d\), independent
compression at three sites would have given
\[
 \mathbb E\,Q_3({\cal C}_{U_1,U_2,U_3}(C))
 =c^3Q_3(C).
\]
Since two-sided compression preserves rank, a negative
\(d\)-dimensional witness would then have produced a negative
\(k\)-dimensional compressed witness.  The theorem shows that this
simple route to a qutrit dimension reduction cannot work.  Section 4
shows that correlated choices of local compression do not evade the
obstruction.

The failure has a definite sign.  Same-subspace compression produces
an additional depolarizing component rather than the more negative
identity direction needed to match \(L_d\).  A valid dimension
reduction, if one exists, must use nonlinear common-code geometry or
some state-dependent selection; ordinary covariant compression and
averaging discard precisely that information.
