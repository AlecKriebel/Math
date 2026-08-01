# Exact site-symmetric reduction of the complete level-two target

## Result

Let (V) be the complete constrained five-replica highest-weight target
space, written as the direct sum over the 125 ordered triples of local
(S_5) shapes.  A real-symmetric invariant moment on this space has 4,139
coordinates.

Let (S_3) permute the three physical qutrit sites.  The exact invariant
coordinate count is

\[
\boxed{\dim \operatorname{Sym}(V)^{S_3}=761.}
\]

Thus exact physical-site symmetrization reduces the full fixed-extension
target by a factor greater than five before any semidefinite calculation.

## Why the reduction is lossless for a symmetrized obstruction

Let (\mathcal L:C\to V) be the degree-three-to-degree-two marginal map,
where (C) is the product of the post-Omega positive semidefinite source
cones.  Both (C) and (\mathcal L) are (S_3)-equivariant.  If (P) denotes
group averaging and (r\in V^{S_3}), then

\[
r\in\mathcal L(C)
\quad\Longleftrightarrow\quad
r\in P\mathcal L(C).
\]

The forward implication is immediate.  Conversely, if
(P\mathcal L(x)=r), then the averaged source

\[
\bar x=\frac16\sum_{\pi\in S_3}\pi x
\]

is still positive semidefinite and satisfies
(\mathcal L(\bar x)=r).

The recorded exact five-replica pseudomoment may itself be averaged over
physical-site permutations.  Positivity, the Pluecker constraint, the lifted
support and Omega equations, and every grouped PPT constraint are preserved.
The minimal-DTH witness is site invariant, so its exact negative expectation
is unchanged.  Hence a failure of the 761-equation symmetric extension test
would still be an exact constrained pseudomoment obstruction.

## Exact block arithmetic

There are 35 unordered triples of the five local (S_5) shapes.

- If all three shapes are distinct, the stabilizer is trivial and a
  representative (k)-dimensional block contributes (k(k+1)/2) coordinates.
- If exactly two shapes agree, the stabilizer transposition has eigenspace
  dimensions (p,q), and the block contributes
  (p(p+1)/2+q(q+1)/2).
- If all shapes agree, write the code space as
  (a[3]\oplus b[1,1,1]\oplus c[2,1]) under site (S_3).  The real-symmetric
  commutant contributes
  (a(a+1)/2+b(b+1)/2+c(c+1)/2).

All characters and multiplicities were computed over the rationals in the
existing exact physical (K)-charts.  Two useful high-negative sectors are

\[
K_{444}=2[3]\oplus4[2,1],
\qquad \dim\operatorname{Sym}(K_{444})^{S_3}=13,
\]

and

\[
K_{333}=2[3]\oplus2[1,1,1]\oplus6[2,1],
\qquad \dim\operatorname{Sym}(K_{333})^{S_3}=27.
\]

For the orbit of (433), the stabilizer transposition has eigenspace
dimensions (9,6), giving 66 coordinates.  These three contributions explain
the 106-variable reduced joint test used in
`discovery/agent_dth_level2_joint_symmetry.py`.

## Numerical companion result

On the exactly site-averaged recorded moment, the joint
(444+333+433)-orbit extension test is strictly feasible numerically.  The
reduced (106\times106) operator (\mathcal L\mathcal L^*) has spectrum in

\[
[154.8121841694696,\ 483.18357792943607].
\]

A shifted Douglas--Rachford solve found a common source-block floor

\[
X_b\succeq10^{-12}I
\]

with invariant marginal residual (9.74\times10^{-21}) and no numerical PSD
defect.  This is discovery evidence, not an exact extension certificate.  It
shows that these five highest-negative target blocks do not furnish a facial
obstruction, even jointly.

The same reduction was then applied to all 17 ordered blocks in the six
site orbits (444), (333), (433), (141), (331), and (321).  Their 1,199 raw
equations reduce to 222 invariant equations.  The unaveraged enlarged problem
also admitted a numerical common source floor (10^{-13}), with marginal
residual (1.23\times10^{-20}) and zero PSD defect.  Thus every target orbit
with the largest recorded negative witness contribution is jointly interior
at this discovery precision.  Any degree-three obstruction must couple in at
least one of the remaining 26 nonzero site-shape orbits.

## Complete PSD fixed-marginal discovery test

The complete post-Omega map contains 118 nonzero ordered target blocks and
487 ordered source blocks.  Its raw source rank is 14,511 and its raw source
cones contain 519,434 real-symmetric variables.  On the 761-dimensional
site-invariant target, the reduced operator \(\mathcal L\mathcal L^*\) is
positive definite, with numerical spectrum

\[
[49.328371469943804,\ 490.01506230813277].
\]

The minimum-norm affine preimage is not positive semidefinite: its marginal
residual is \(3.10\times10^{-17}\), its aggregate negative-eigenvalue norm
is \(2.87\times10^{-7}\), and its least eigenvalue is
\(-4.05\times10^{-8}\).  A full blockwise Douglas--Rachford correction,
however, reduced these quantities to

\[
\begin{aligned}
\text{invariant marginal residual}&=1.6326912387466753\times10^{-20},\\
\text{PSD defect}&=3.1092050679560775\times10^{-14},\\
\lambda_{\min}&=-6.1533713273820615\times10^{-15}.
\end{aligned}
\]

The retained discovery cache is
`discovery/dth_level2_full_symmetric_floor0.pkl`, with SHA-256 digest

```
5240025205d277a5270154a71d1ada3b9901af7e0a77056b80771aa14f3daa6c
```

This is strong numerical evidence that the **PSD-only**, post-Omega,
fixed-marginal relaxation is feasible on a boundary face.  It is not an
exact extension certificate.  In particular, it does not yet impose the
prolonged support equation on the partially transposed source or either of
the remaining grouped PPT constraints.  It therefore does not decide the
complete degree-three DTH lift.

## Verification

`verification/verify_dth_site_symmetric_target_census.py` reconstructs all
35 exact stabilizer representations, pins every multiplicity and invariant
dimension, and checks both totals (4,139) and (761) without floating-point
arithmetic.  The smaller independent verifier
`verification/verify_dth_site_symmetric_census_arithmetic.py` rechecks the
pinned character arithmetic and both totals using only the Python standard
library.
