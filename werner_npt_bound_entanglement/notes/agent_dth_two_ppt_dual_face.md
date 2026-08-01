# Dual geometry for the \(\Gamma_1+\Gamma_5\) five-replica cone

## Strengthened primal and its zero-level dual

Work in Hilbert--Schmidt-normalized invariant coordinates.  Let \(K\) be
the holomorphic Plücker--Omega support, let \(U_1\) be the normalized
crossing for the first-bivector partial transpose, and let \(U_5\) be the
normalized crossing for the final \(z\)-slot partial transpose.  Both local
crossings, and hence their three-site tensor cubes, are orthogonal.

The strengthened relaxation is

\[
 \begin{aligned}
 \inf_X\quad&\langle O,X\rangle\\
 \text{subject to}\quad
 &X\succeq0,\quad \operatorname{ran}X\subseteq K,\quad
   \operatorname{Tr}X=1,\\
 &U_1X\in\mathcal C_1,\qquad U_5X\in\mathcal C_5.
 \end{aligned}
\]

Here \(\mathcal C_1\) is the positive cone on the exact product-DTH face
and \(\mathcal C_5\) is the full positive cone in the final-slot mixed
commutant.  A zero-level dual certificate consists of

\[
 Y_1\in\mathcal C_1^*,\qquad
 Y_5\in\mathcal C_5^*,
\]

such that

\[
 S=P_K\bigl(O-U_1^*Y_1-U_5^*Y_5\bigr)P_K\succeq0.
\tag{1}
\]

Indeed, every primal feasible \(X\) then satisfies

\[
 \langle O,X\rangle
 =\langle S,X\rangle
  +\langle Y_1,U_1X\rangle
  +\langle Y_5,U_5X\rangle\ge0.
\]

The known computational equality triple gives a feasible point of value
zero.  Thus a certificate (1) would determine the strengthened optimum
exactly.

## Exact metric projection needed for a dual search

Put

\[
 H=U_1^*Y_1+U_5^*Y_5.
\]

For one holomorphic support block with orthonormal basis matrix \(B\), set

\[
 C=B^THB,
 \qquad
 C'=O_K-(O_K-C)_+.
\]

Then \(C'\preceq O_K\), and it is the Frobenius projection of \(C\) onto
that order interval.  With

\[
 \Delta=B(C'-C)B^T,
\]

the simultaneous update

\[
 Y_1\longmapsto Y_1+\frac12U_1\Delta,
 \qquad
 Y_5\longmapsto Y_5+\frac12U_5\Delta
\tag{2}
\]

is the exact product-space metric projection onto the affine slack set.
To see this, the map

\[
 A:(D_1,D_5)\longmapsto U_1^*D_1+U_5^*D_5
\]

satisfies \(AA^*=2I\).  Therefore the minimum-norm preimage of \(\Delta\)
is \(A^*(AA^*)^{-1}\Delta=(U_1\Delta,U_5\Delta)/2\).

The other metric projection is blockwise: project the compression of
\(Y_1\) to the exact product-face basis onto the positive cone, and project
every full \(Y_5\) block onto the positive cone.  Douglas--Rachford or ADMM
can therefore search the complete two-PPT dual without forming a dense
superoperator.

## Equality-face reduction

Let \(X_0\) be the twirl of the exact computational equality triple and
put \(Z_i=U_iX_0\).  Every feasible zero-level dual certificate obeys

\[
 \langle S,X_0\rangle
 =\langle Y_1,Z_1\rangle
 =\langle Y_5,Z_5\rangle=0.
\]

The holomorphic slack and the final-slot pair are positive.  If \(F_1\)
is the exact product-face basis, write

\[
 \widehat Y_1=F_1^TY_1F_1\succeq0
 \quad\text{and}\quad
 Z_1=F_1\widehat Z_1F_1^T.
\]

Complementarity consequently gives

\[
 \operatorname{ran}S\subseteq\ker X_0,
 \qquad
 \operatorname{ran}\widehat Y_1\subseteq\ker\widehat Z_1,
 \qquad
 \operatorname{ran}Y_5\subseteq\ker Z_5.
\tag{3}
\]

The components of \(Y_1\) transverse to the product face are unrestricted
affine-support multipliers, so (3) makes no claim about their ranges.
Imposing the three displayed compressed conditions from the outset is
lossless.  Numerically stable range bases for \(X_0,\widehat Z_1,Z_5\)
should expose the smallest dual face before attempting rational
reconstruction.  The required audits are:

1. the three cone minima in (1);
2. the three complementary pairings above;
3. block ranks and kernel dimensions of \(S,Y_1,Y_5\);
4. whether the reduced solution is isolated modulo homogeneous facial rays;
5. the smallest exact representation blocks supporting nonzero certificate
   data.

This note supplies only the dual reduction.  Numerical feasibility is not
an exact DTH certificate.

## Numerical maximum-rank Gamma5 face and homogeneous exposer

An objective-free two-PPT feasibility run produced a point which is full
rank on the 768-dimensional holomorphic support and the 2266-dimensional
exact Gamma1 product face.  Its Gamma5 image has rank 751 in 188 of the 216
blocks.  At the recorded checkpoint the largest eigenvalue assigned to the
kernel is (4.375\times10^{-19}), while the smallest positive eigenvalue is
(1.783\times10^{-8}).  Thus the numerical rank split is exceptionally
clean and leaves an 8510-dimensional Gamma5 kernel.

The corresponding homogeneous facial-normal problem is

\[
 F_1^T Y_1F_1=0,qquad
 Y_5\succeq0,quad \operatorname{ran}Y_5\subseteq\ker Z_5,
 \qquad
 P_K(U_1^TY_1+U_5^TY_5)P_K=0.
\tag{4}
\]

After fixing the invariant trace of (Y_5) to one, exact metric-projection
iterations reached residual (1.28\times10^{-13}).  The separate numerical
audits were

\[
 \|F_1^TY_1F_1\|_2=3.61\times10^{-14},
 \quad
 \|P_K(U_1^TY_1+U_5^TY_5)P_K\|_2=7.12\times10^{-14},
\]

and the leakage of (Y_5) outside the proposed face was
(5.20\times10^{-14}).  More importantly, (Y_5) is positive definite on
the entire 8510-dimensional kernel: its smallest compressed eigenvalue is
(7.60014\times10^{-8}), with all 216 blocks active.  This is strong
numerical evidence that the rank-751 Gamma5 face is genuinely exposed and
is the correct first facial reduction.

The exposer is nearly scalar on that kernel.  In 197 of 216 blocks its
restriction agrees, to discovery precision, with

\[
 \tau\sqrt{d_{\lambda_1}d_{\lambda_2}d_{\lambda_3}},I,
 \qquad \tau=7.60013956385\times10^{-8}.
\]

Only 19 blocks are nonscalar.  In the target ordering
((00,03,11,22,30,41)), they are the site permutations of

\[
 (0,2,0),\ (4,0,2),\ (4,4,2),\ (2,2,2),\ (2,2,0),\ (2,2,4).
\]

In every exceptional block the top eigenvalue still equals the displayed
scalar value; only a small subspace is deflated.  This finite exceptional
list is the current target for exact reconstruction.  None of these
floating-point statements is yet an exact facial theorem.

Discovery utilities are
`discovery/agent_dth_gamma5_feasible_face.py` and
`discovery/agent_dth_gamma5_face_exposer.py`.  The frozen temporary
artifacts have SHA-256 hashes

```
80c4d0b3a5a9b34bdb8b0b7581c208d6bc10d3f49e3a63f1239ef87ea8339930
  dth_gamma5_exposer_iter100_sha80c4.npz
a0020339ce9db4c24b1a7e710dbbb139fbbc42f26f87ad0c5a6bd508d940a9ad
  dth_gamma5_face_rank751_shaa002.npz
```
