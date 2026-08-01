# Exact Morse--Bott Hessian of the factor DTH equality variety

## Status

The direct physical search and the deficient-support equality
classification isolate the equality variety

\[
 \mathcal E=
 \{a\otimes\xi:\|a\|=\|\xi\|=1,
                  \operatorname{SchmidtRank}(\xi)\le2\},
\tag{1}
\]

including physical-site permutations.  This note computes the complete
Ky--Fan Hessian at every smooth point of (1).

Let

\[
 \Phi(z)={1\over2}\sum_{j=1}^4s_j(D_z)^2
         =\lambda_1(D_z^\dagger D_z)
          +\lambda_2(D_z^\dagger D_z),
\tag{2}
\]

where the second expression uses the paired skew singular values.  At a
generic equality point, the Hessian is negative semidefinite, its kernel is
exactly the tangent space of \(\mathcal E\), and every normal direction has
an explicit strictly negative coefficient.

Consequently there is no full-support stationary branch bifurcating from a
generic factor equality point at quadratic order.  Any full-support
equality or violation must either be separated from this generic boundary
or approach its lower-rank singular strata.

This is a local stability theorem, not a global proof of DTH.

## 1. Canonical point and spectral gap

By local Hodge covariance, take

\[
 z_0=e_0\otimes\xi,
 \qquad
 \xi=s|00\rangle+t|11\rangle,
 \qquad s,t>0,\quad s^2+t^2=1.
\tag{3}
\]

The top four squared singular values of (D_{z_0}) are all (1/8).
The fifth is at most

\[
 {\max(s^2,t^2)\over8}<{1\over8}.
\]

Thus the four-dimensional top spectral projector is isolated and
\(\Phi\) is real analytic near (z_0).

Write a complex tangent vector to the unit projective sphere as

\[
 \delta=e_0\otimes Y_0+e_1\otimes Y_1+e_2\otimes Y_2,
 \qquad \langle\xi,Y_0\rangle=0.
\tag{4}
\]

Use the normalized curve

\[
 z(\epsilon)={z_0+\epsilon\delta
              \over\sqrt{1+\epsilon^2\|\delta\|^2}}.
\tag{5}
\]

## 2. Complete exact Hessian

### Theorem

The first derivative of \(\Phi(z(\epsilon))\) at zero vanishes, and

\[
 \Phi(z(\epsilon))={1\over4}+\epsilon^2q_{s,t}(\delta)
                    +O(\epsilon^3),
\tag{6}
\]

where

\[
\boxed{
\begin{aligned}
q_{s,t}(\delta)={}&
-{s^2t^2\over2}|(Y_0)_{22}|^2\\
&-\sum_{a=1}^2\Bigg[
 {1\over8}|t(Y_a)_{00}-s(Y_a)_{11}|^2\\
&\qquad+{1\over8}
 \left(|(Y_a)_{01}|^2+|(Y_a)_{10}|^2+|(Y_a)_{22}|^2\right)\\
&\qquad+{3+t^2-s^2\over16}
 \left(|(Y_a)_{02}|^2+|(Y_a)_{20}|^2\right)\\
&\qquad+{3+s^2-t^2\over16}
 \left(|(Y_a)_{12}|^2+|(Y_a)_{21}|^2\right)
 \Bigg].
\end{aligned}}
\tag{7}
\]

On the complex projective tangent space, the eigenvalues and
multiplicities are

\[
\begin{array}{c|c}
0&9\\
-s^2t^2/2&1\\
-1/8&8\\
-(3+s^2-t^2)/16&4\\
-(3+t^2-s^2)/16&4.
\end{array}
\tag{8}
\]

After realification, all multiplicities double.  The global phase supplies
one further real zero direction, so the unit-sphere Hessian has kernel
dimension (19) and negative rank (34).

### Proof

Put (D_0=D_{z_0}), (E=D_\delta), (S_0=D_0^\dagger D_0), and let
\(P\) be the top four-dimensional spectral projector.  On
\(P^\perp\), define the reduced resolvent

\[
 R=P^\perp\left({1\over8}I-S_0\right)^{-1}P^\perp.
\tag{9}
\]

The standard isolated-cluster expansion, applied to the sum of the top
four eigenvalues and divided by two as in (2), gives

\[
\boxed{
q_{s,t}(\delta)
={1\over2}\operatorname{Tr}(PE^\dagger E)
-{1\over4}\|\delta\|^2
 +
{1\over2}\operatorname{Tr}
\left[P S_1R S_1\right],
}
\tag{10}
\]

where

\[
 S_1=D_0^\dagger E+E^\dagger D_0.
\]

The linear cluster trace \(\operatorname{Tr}(PS_1)\) vanishes.

For (3), the range of (P) is

\[
 e_0^\perp\otimes
 \operatorname{span}\{|22\rangle,
                       t|00\rangle+s|11\rangle\}.
\tag{11}
\]

Substitute the explicit epsilon matrices into (9)--(10).  The matrix-unit
blocks do not mix, except for the two-dimensional
\(\operatorname{span}\{|00\rangle,|11\rangle\}\) block.  That block
splits into the zero vector (s|00\rangle+t|11\rangle\) and the coefficient
\(-1/8\) on (t|00\rangle-s|11\rangle\).  The remaining blocks give,
respectively,

\[
 -{s^2t^2\over2},\quad -{1\over8},\quad
 -{3+t^2-s^2\over16},\quad
 -{3+s^2-t^2\over16}.
\]

This is exactly (7), and counting its matrix units gives (8).

For a completely independent exact audit, set (s=3/5,t=4/5).  The
dependency-free rational verifier reconstructs (P,R,S_1) from the Hodge
matrices and checks every entry of (10).  It obtains the complex spectrum

\[
 0^{(9)},\quad
 \left(-{72\over625}\right)^{(1)},\quad
 \left(-{1\over8}\right)^{(8)},\quad
 \left(-{41\over200}\right)^{(4)},\quad
 \left(-{17\over100}\right)^{(4)}.
\]

Run

```text
python3 verification/verify_dth_factor_equality_hessian.py
```

to replay it. \(\square\)

## 3. Kernel equals the equality tangent

Equation (7) vanishes precisely when

\[
 (Y_0)_{22}=0,
 \qquad
 Y_1,Y_2\in\mathbb C\xi.
\tag{12}
\]

The first condition is the tangent equation to the rank-at-most-two
determinantal variety at the rank-two matrix \(\xi\).  The other two are
exactly the infinitesimal variations of the one-site factor (e_0).
Therefore

\[
 \boxed{\ker q_{s,t}=T_{z_0}\mathcal E}
\quad\text{on the complex projective tangent.}
\tag{13}
\]

The dimension check is independent:

\[
 \dim_{\mathbb C}\mathbb P\{\operatorname{rank}\xi\le2\}=7,
 \qquad \dim_{\mathbb C}\mathbb CP^2=2,
\]

so the projective equality variety has complex dimension (9), exactly
the nullity in (8).

Every nonzero normal vector satisfies the sharp quadratic estimate

\[
 \boxed{
 q_{s,t}(\delta_\perp)
 \le-{s^2t^2\over2}\|\delta_\perp\|^2,
 }
\tag{14}

because all other coefficient magnitudes in (8) are at least (1/8),
while (s^2t^2/2\le1/8).

## 4. Local strict gap and marginal determinant

Fix \(\epsilon>0\) and restrict to the compact smooth equality stratum

\[
 s,t\ge\epsilon.
\]

Analyticity, (13), and the uniform normal curvature in (14) give a
neighborhood \(\mathcal N_\epsilon\) and a constant (c_\epsilon>0)
such that

\[
 \boxed{
 {1\over4}-\Phi(z)
 \ge c_\epsilon\operatorname{dist}(z,\mathcal E)^2
 \qquad(z\in\mathcal N_\epsilon).
 }
\tag{15}

This is the Morse--Bott lemma with a compact uniformity argument; no
numerical sign enters.

At the factored site of the nearest equality point, the two small
eigenvalues of the one-site marginal are quadratic in the distance from
the factor locus.  Hence

\[
 \det\rho_i^z
 \le C_\epsilon\operatorname{dist}(z,\mathcal E)^4
\tag{16}

after reducing the neighborhood if necessary.  Combining (15)--(16) gives

\[
 \boxed{
 {1\over4}-\Phi(z)
 \ge c'_\epsilon
 \sqrt{\min_i\det\rho_i^z}
 \qquad(z\in\mathcal N_\epsilon).
 }
\tag{17}

For points that remain locally deficient, the right side is zero and the
global deficient-support theorem supplies nonnegativity.  For full-support
points, (17) is a genuine strict gap.

## 5. What remains

The exact Hessian closes every infinitesimal escape from the smooth
rank-two factor stratum.  The only remaining possibilities for a physical
counterexample are:

1. a full-local-rank stationary point separated from the equality variety;
2. a sequence approaching the singular product stratum (st=0), where the
   curvature (s^2t^2/2) vanishes and higher-order analysis is required.

Thus a global proof can now focus on a compact interior stationary
classification plus the lower-rank factor corners.  The present theorem
does not assert that no distant full-support critical point exists.
