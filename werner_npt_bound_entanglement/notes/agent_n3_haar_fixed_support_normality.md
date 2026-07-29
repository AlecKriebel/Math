# Fixed-support normality at a three-copy Haar equality

## Status

This note strengthens the exact block-Gram collapse in
`agent_n3_haar_block_gram_collapse.md`.  It does **not** prove that the
Haar-equality system is inconsistent at rank two.

Let \(C\) have rank two and suppose that, at a physical site \(i\),
\[
 Q_3(A^{(i)}C,B^{(i)}C)=\gamma Q_1(A,B)
 \qquad(A,B\in M_3).
 \tag{1}
\]
Put
\[
 E_i={\cal L}^{\otimes\{1,2,3\}\setminus\{i\}}(C).
 \tag{2}
\]
For every rank-two local projection
\[
 P_z=I-|z\rangle\langle z|,
 \tag{3}
\]
define the compressed endpoint gradient
\[
 N_i(z)=P_z^{(i)}{\cal L}^{(i)}(P_z^{(i)}E_i).
 \tag{4}
\]
The new conclusion is that \(N_i(z)\) lies in the determinantal normal
space of \(C\), not merely that its scalar pairing with \(C\) vanishes:
\[
 \boxed{\qquad
 C^\dagger N_i(z)=0,\qquad N_i(z)C^\dagger=0
 \quad\text{for every }z.
 \qquad}
 \tag{5}
\]
If
\[
 C=XSY^\dagger,\qquad X^\dagger X=Y^\dagger Y=I_2,\qquad S>0,
 \tag{6}
\]
then (5) is equivalently
\[
 \boxed{\qquad
 X^\dagger N_i(z)=0,\qquad N_i(z)Y=0.
 \qquad}
 \tag{7}
\]

After clearing the denominator in \(P_z\), (7) is a bidegree-\((2,2)\)
polynomial identity in \(z,\overline z\).  It therefore consists of only
\(36\) matrix coefficients at each site.  Its Haar-constant coefficient
already gives the exact rank-two normality identities
\[
 \boxed{\qquad
 X^\dagger{\cal Q}^{(i)}E_i=0,\qquad
 ({\cal Q}^{(i)}E_i)Y=0,
 \qquad}
 \tag{8}
\]
where
\[
 {\cal Q}(A)=A-\frac{\operatorname{Tr}A}{3}I_3.
 \]

Equations (7), together with the rank-one block Gram
\[
 {\cal B}_2(C_{ab},C_{cd})=\gamma\delta_{ab}\delta_{cd},
 \tag{9}
\]
and the six maximally mixed one-site marginals, form a finite exact
realizability system.  The nonconstant \(35\) harmonics in (7) are
information not present in (9) or in any sector-mass inequality.

The dependency-free checker is
`verification/verify_n3_haar_fixed_support_normality.py`.

## 1. Every local two-plane is an exact boundary zero

Equation (1) and
\[
 Q_1(P_z)=\|P_z\|_2^2-\frac12|\operatorname{Tr}P_z|^2
 =2-\frac12(2)^2=0
 \tag{10}
\]
give
\[
 Q_3(P_z^{(i)}C)=0.
 \tag{11}
\]
Every rank-at-most-two matrix whose left range is supported in
\(P_z\mathbb C^3\) is nonnegative by the established deficient-local-
support theorem.  Thus (11) is a global minimum on the fixed-support
rank-two determinantal variety.

For all \(z\) outside a proper algebraic subset,
\[
 D_z=P_z^{(i)}C
 \tag{12}
\]
still has rank two.  Indeed, rank loss means that the two-plane
\(\operatorname{ran}C\) contains a nonzero vector in
\(|z\rangle\otimes(\mathbb C^3)^{\otimes2}\).  This cannot occur for
every \(z\): applying it to three orthogonal basis vectors would put
three nonzero vectors in mutually orthogonal local summands inside the
two-dimensional space \(\operatorname{ran}C\).  Thus at least one
rank-two projection preserves the rank.  A nonzero \(2\times2\) minor
then shows that rank preservation holds off a proper algebraic subset.

Let \(U_z=\operatorname{ran}D_z\) and
\(V=\operatorname{ran}D_z^\dagger=\operatorname{ran}C^\dagger\).
The tangent space to rank-two matrices supported on the left in
\(P_z\mathbb C^3\) consists of
\[
 U_zK^\dagger+HV^\dagger,
 \tag{13}
\]
with arbitrary compatible \(H,K\) whose left outputs remain in the
fixed support.  Its Hilbert--Schmidt normal space consists exactly of
the matrices \(M\) satisfying
\[
 U_z^\dagger M=0,\qquad MV=0.
 \tag{14}
\]

The gradient of (11), compressed to the fixed left support, is (4).
Stationarity on (13) therefore gives (14) with \(M=N_i(z)\).  Since
\[
 \operatorname{ran}D_z^\dagger=V,\qquad
 \operatorname{ran}D_z=U_z,
 \]
this is equivalent to
\[
 D_z^\dagger N_i(z)=0,\qquad N_i(z)D_z^\dagger=0.
 \tag{15}
\]
The first equation in (15) is \(C^\dagger N_i(z)=0\), because
\(N_i(z)=P_z^{(i)}N_i(z)\).  The second says directly that \(N_i(z)\)
annihilates \(V=\operatorname{ran}C^\dagger\), and hence
\(N_i(z)C^\dagger=0\).  This proves (5) for generic \(z\).
Both sides are continuous, so (5) holds for every \(z\).

Factoring \(C\) as in (6), and using that \(S\) is invertible, turns
(5) into (7).

## 2. The finite bihomogeneous identity

Allow \(z\ne0\) to be unnormalized and put
\[
 r=z^\dagger z,\qquad R=|z\rangle\langle z|,
 \qquad P_z=I-\frac Rr.
 \tag{16}
\]
Write
\[
 T=\operatorname{Tr}_iE_i,\qquad
 T_R=\operatorname{Tr}_i(R^{(i)}E_i).
 \tag{17}
\]
A direct expansion of \(r^2N_i(z)\) gives
\[
\boxed{
\begin{aligned}
 {\mathfrak N}_i(z):=r^2N_i(z)
 ={}&r^2E_i-rR^{(i)}E_i
 -\frac12r^2 I^{(i)}\otimes T\\
 &+\frac12r I^{(i)}\otimes T_R
 +\frac12r R^{(i)}\otimes T
 -\frac12R^{(i)}\otimes T_R .
\end{aligned}}
\tag{18}
\]
Every term in (18) has bidegree \((2,2)\) in
\((z,\overline z)\).  Hence
\[
 X^\dagger{\mathfrak N}_i(z)=0,\qquad
 {\mathfrak N}_i(z)Y=0\quad(z\in\mathbb C^3)
\tag{19}
\]
is equivalent to the vanishing of the
\[
 \dim\operatorname{Sym}^2(\mathbb C^3)^2=6^2=36
\tag{20}
\]
coefficient matrices.  This replaces the continuum of local
two-planes by a finite polynomial system without choosing a frame.

## 3. The constant harmonic

For a Haar unit vector \(z\),
\[
 {\mathbb E}R=\frac13I.
\tag{21}
\]
In local block notation \(E_i=(E_{ab})\), the second moment gives
\[
 {\mathbb E}\left[
 R\otimes\operatorname{Tr}_i(RE_i)
 \right]
 =
 \frac1{12}\left(
 E_i+I\otimes\operatorname{Tr}_iE_i
 \right).
\tag{22}
\]
Substituting (21)--(22) in (18), with \(r=1\), yields
\[
\begin{aligned}
 {\mathbb E}N_i(z)
 &=
 \left(\frac23-\frac1{24}\right)E_i
 +\left(-\frac13+\frac16-\frac1{24}\right)
 I\otimes\operatorname{Tr}_iE_i\\
 &=\frac58\left(
 E_i-\frac13I\otimes\operatorname{Tr}_iE_i
 \right)\\
 &=\frac58{\cal Q}^{(i)}E_i.
\end{aligned}
\tag{23}
\]
Average (7) and use (23) to obtain (8).

Summing (8) over the three sites shows, in operator-valued rather than
scalar form, that
\[
 \left(\frac14\Pi_1-\Pi_2+3\Pi_3\right)C
\tag{24}
\]
lies in the normal space of the rank-two determinantal variety at
\(C\).  Taking only its Hilbert--Schmidt pairing with \(C\) recovers
the grouped Haar equality.  Thus (8) strictly retains information
discarded by sector arithmetic.

## 4. Why the rank cutoff remains essential

The polynomial equations themselves are consistent at high rank.
For example, take \(C=I_{27}\).  Then
\[
 E_i={\cal L}(I_3)\otimes{\cal L}(I_3)\otimes I_3
 =\frac14I_{27},
\tag{25}
\]
up to the placement of the unfiltered site.  Since
\[
 {\cal L}(P_z)=P_z-\frac12\operatorname{Tr}(P_z)I=-|z\rangle\langle z|,
\tag{26}
\]
one has
\[
 P_z{\cal L}(P_z)=0
\tag{27}
\]
and therefore \(N_i(z)=0\) identically at all three sites.

After Hilbert--Schmidt normalization, \(I_{27}\) also has maximally
mixed left and right one-site marginals and satisfies (1) with
\(\gamma=1/12\), but it has rank \(27\).  Any contradiction must
therefore use the two-dimensional common factorization in (6), not
only the polynomial identities (18).

## 5. Remaining exact lemma

For a negative Haar-equality critical point, the complete finite system
now consists of:

1. the thin rank-two factorization \(C=XSY^\dagger\);
2. the six marginal identities
   \(\rho_i^L=\rho_i^R=I_3/3\);
3. the three block-Gram identities (9);
4. the \(3\times36\) left and right normality coefficients (19).

The missing assertion is:

> This finite system has no solution with \(S>0\) and \(\gamma>0\).

Proving it would exclude every stationary negative Haar equality.
Conversely, an exact solution would give the smallest currently known
algebraic candidate for a three-copy negative witness.  No such
solution is proved or asserted here.
