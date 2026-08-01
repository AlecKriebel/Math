# Degenerate product-corner cluster and the quartic zero cone

## Status

At the singular equality point

\[
 z_0=|000\rangle,
\]

the top squared singular value of \(D_{z_0}\) is \(1/8\) with
multiplicity eight.  The ordinary four-dimensional Hessian is therefore
not defined.  This note computes the complete degenerate second-order
cluster.

For every tangent direction \(\delta\perp z_0\), the sum of the top four
cluster shifts is nonpositive.  Hence no DTH violation bifurcates from a
product equality point at quadratic order.  The zero cone is nevertheless
strictly larger than the tangent cone to the physical equality union; an
explicit zero-Hessian direction has a strictly negative quartic deficit.

Thus the product corner is reduced to a genuinely quartic boundary lemma.

## 1. Effective eight-dimensional cluster

Let

\[
 z(\epsilon)={z_0+\epsilon\delta
               \over\sqrt{1+\epsilon^2\|\delta\|^2}},
 \qquad E=D_\delta,
\]

and put \(S_0=D_{z_0}^\dagger D_{z_0}\).  If

\[
 K=(e_0^\perp)^{\otimes3},\qquad P_0=P_K,
\]

then

\[
 S_0={1\over8}P_0.
\]

For \(S_1=D_{z_0}^\dagger E+E^\dagger D_{z_0}\), direct epsilon
contraction gives

\[
 P_0S_1P_0=0.
\]

The effective second-order operator on the eightfold cluster is therefore

\[
\boxed{
 H_\delta
 =P_0\left(E^\dagger E-{\|\delta\|^2\over8}I\right)P_0
  +8P_0S_1(I-P_0)S_1P_0.
}
\tag{1}

Writing \(\kappa_4(H)\) for the sum of the four largest eigenvalues,

\[
 \mathcal F(z(\epsilon))
 ={1\over2}+\epsilon^2\kappa_4(H_\delta)+O(\epsilon^3).
\tag{2}

## 2. Hamming-support splitting

Decompose the tangent tensor according to the set of nonzero local indices:

\[
 \delta=\sum_{\varnothing\ne J\subseteq\{1,2,3\}}\delta_J,
\]

where an index lies in \(J\) exactly when it belongs to
\(e_0^\perp\).  The Hodge matrices map different support sets to orthogonal
zero/nonzero occupancy sectors.  Both terms of (1) therefore polarize
orthogonally:

\[
 \boxed{H_\delta=\sum_JH_{\delta_J}.}
\tag{3}

The individual spectra are as follows.  Put \(n_J=\|\delta_J\|^2\).

### Weight one

For \(|J|=1\),

\[
 \boxed{H_{\delta_J}=0.}
\tag{4}

These are the infinitesimal local-product motions.

### Weight two

For \(|J|=2\), identify \(\delta_J\) with a \(2\times2\) matrix \(Z_J\)
on the two nonzero local indices and set \(d_J=|\det Z_J|\).  Then

\[
\boxed{
 \operatorname{spec}H_{\delta_J}
 =\left\{
  -{n_J\over8}^{(4)},
  +{d_J\over4}^{(2)},
  -{d_J\over4}^{(2)}
 \right\}.
}
\tag{5}

Since \(d_J\le n_J/2\),

\[
 \boxed{\kappa_4(H_{\delta_J})=0.}
\tag{6}

To prove (5), use the \(U(2)\times U(2)\) stabilizer of \(z_0\) to put
\(Z_J=\operatorname{diag}(b,c)\).  On the affected two-qubit factor,
the effective matrix is unitarily equivalent to

\[
 \begin{pmatrix}
 0&0&0&bc/4\\
 0&-n_J/8&0&0\\
 0&0&-n_J/8&0\\
 bc/4&0&0&0
 \end{pmatrix},
\]

tensored with the identity on the remaining qubit.  This gives (5).

### Weight three

For \(J=\{1,2,3\}\),

\[
\boxed{
 \operatorname{spec}H_{\delta_J}
 =\{0^{(2)},(-n_J/8)^{(6)}\},
 \qquad
 \kappa_4(H_{\delta_J})=-{n_J\over4}.
}
\tag{7}

Indeed, \(E P_0\) and \(E^\dagger D_{z_0}P_0\) each have rank one.
Their two right vectors have equal norm and are orthogonal by the odd Hodge
alternation.  They repair exactly two of the eight eigenvalues
\(-n_J/8\) in (1).

## 3. Exact quadratic theorem

Ky--Fan subadditivity, (3), and (4)--(7) give

\[
\boxed{
 \kappa_4(H_\delta)
 \le-{1\over4}\|\delta_{\{1,2,3\}}\|^2\le0.
}
\tag{8}

Therefore every tangent direction has a nonpositive second cluster
coefficient, and every direction with a genuine weight-three component is
strictly decreasing already at second order.

This is an exact degenerate local-maximum theorem.  It does not give a
uniform quadratic gap because the weight-two pieces individually saturate
(6), and distinct saturated pieces can sometimes share a maximizing
four-plane.

## 4. A zero-Hessian direction outside the equality tangent cone

Consider the exact direction

\[
\boxed{
 \delta_*=|110\rangle+|220\rangle+|101\rangle+|202\rangle.
}
\tag{9}

It contains maximally entangled weight-two pieces on the pairs \(12\) and
\(13\).  In the lexicographic basis of \(K\), its effective matrix has
spectrum

\[
 \boxed{(-1/2)^{(4)},\quad(1/4)^{(2)},\quad(-1/4)^{(2)}.}
\tag{10}

Hence \(\kappa_4(H_{\delta_*})=0\).

This direction is not in the tangent cone of the physical equality union.
At \(z_0\), an arc in the branch factored at site \(i\) can have a
weight-two first derivative only on the complementary pair
\(\widehat i\).  Direction (9) has nonzero components on two distinct
pairs.  Since the equality set is the finite union of the three factor
branches, no equality arc has derivative (9).

The flatness is only quadratic.  Put

\[
 z_*(t)={z_0+t\delta_*\over\sqrt{1+4t^2}}.
\]

If \(\widehat D=(2\sqrt2)D\), exact block diagonalization gives

\[
\begin{aligned}
\det(\lambda I-\widehat D^\dagger\widehat D)
={}&\lambda^7(\lambda-2t^2)^8(\lambda-1)^4\\
&\times
\left(\lambda^2-(1+6t^2)\lambda+9t^4\right)^2\\
&\times
\left(\lambda^2-(1+2t^2)\lambda+t^4\right)^2.
\end{aligned}
\tag{11}

For sufficiently small nonzero \(t\), the four largest roots are the two
large roots of the last two quadratics, each repeated twice.  Therefore

\[
\boxed{
\mathcal F(z_*(t))
=
{2+8t^2+\sqrt{1+12t^2}+\sqrt{1+4t^2}
 \over8(1+4t^2)}
={1\over2}-{5\over2}t^4+O(t^6).
}
\tag{12}

Thus the first nonzero deficit along this nonintegrable zero-Hessian
direction is strictly quartic.

The dependency-free verifier

```text
python3 verification/verify_dth_product_corner_cluster.py
```

checks the support splitting and spectra over the rationals and verifies
the full bivariate characteristic polynomial (11) exactly.
