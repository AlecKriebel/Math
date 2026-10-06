# Independent first-pass criterion and universal reconstruction

This is a validation of the frozen PR #22 candidate, not another proof attempt.
Target: the literal AIM 2003 Conjecture 1 (printed p. 17), repeated as Problem
30 (printed p. 28), for records 20002011 and 20002052. The first pass used only
the candidate `SOURCE_STATUS.md`, the two exact source records, the complete
30-page AIM source, and the input manifest. It did not read or execute the
original author/reviewer programs, historical review, current sibling reviews,
or parent mathematical outcomes. High-level pass/status assertions appearing
inside those allowed inputs are assertions under examination, not evidence.

## Exact success criterion

The PR must establish a universal natural critical-weight density whose
integral is conformally invariant, and a smooth closed-manifold realization
where its density-valued conformal linearization fails formal self-adjointness.
It must also show that every member of the conjectured decomposition has
self-adjoint conformal linearization under the exact source's definitions.
The historical priority attribution is a separate source check, to be done
after this reconstruction is sealed. A successful obstruction refutes only the
literal statement without the variational hypothesis; it says nothing about a
repaired conjecture assuming formal self-adjointness.

The AIM source expressly passes to density-valued invariants on pp. 16–17.
Its primitive is an identity at every background metric and every smooth
conformal direction, not merely at a single metric. The two-metric cocycle and
the integral of a single natural local invariant are distinguished there.
Conjectures 2 and 3 on p. 18, and Problems 31 and 32 on p. 28, permit an arbitrary
divergence and are different targets. The polynomial filtration on p. 18 uses
`k_derivatives + 2 k_curvatures = n`; the candidate belongs to that class.

## 1. Necessary symmetry, with the measure included

Let `H_g` be an n-form and let `D_g H(psi)` denote its derivative along
`g_t = exp(2t psi) g`. If `d F_g(omega) = integral omega H_g` at every metric,
set `F(s,t)=F(exp(2s phi+2t psi)g)`. Differentiating these identities yields

`F_st(0,0) = integral phi D_g H(psi)` and
`F_ts(0,0) = integral psi D_g H(phi)`.

They agree. Smooth natural local densities give a twice continuously
differentiable two-variable functional on a closed manifold. More generally,
the smooth gradient identity itself makes these partial derivatives continuous.
The derivative is of `H` as a density, so its volume derivative is already
present; one must not instead test only the scalar coefficient's derivative.
If `D_g H(psi) = A_g psi dV_g`, this identity is exactly `A_g=A_g^*` with
adjoint taken using the fixed metric's `dV_g`.

The AIM source on pp. 12–14 explicitly assumes the critical GJMS operator is
formally self-adjoint and gives the critical change law
`Q_(exp(2u)g)=Q_g+P_g u` for densities. Thus `D_g Q=P_g` is self-adjoint.
A pointwise conformal invariant density has derivative zero. Therefore every
`a Q + L + G` in Conjecture 1 has self-adjoint density linearization. Changing
Q by a pointwise invariant does not change this necessary property. A cocycle
with a primitive at every running metric would obey the same mixed-variation
test; the obstruction is stronger than failure of a single local formula.

## 2. Universal variation and adjoint calculation

Use dimension six, `Delta=div grad`, `J=R/10`,
`P=(Ric-Jg)/4`, and `B=|P|_g^2`. Under `g_t=exp(2t psi)g`,

* `dot g^{-1}=-2 psi g^{-1}` and `dot dV=6 psi dV`;
* the finite Schouten formula gives `dot P_ij=-Hess_ij psi`;
* two inverse metrics in the norm give
  `dot B=-4 psi B-2 P^{ij} Hess_ij psi`;
* the scalar Laplacian change law gives
  `dot(Delta b)=-2 psi Delta b + 4 <d psi,d b> + Delta(dot b)`.

For `S=(Delta B)dV`, set `T psi=P^{ij} Hess_ij psi`. Collecting all terms gives

`D_g S(psi)=[-4 div(B grad psi)-2 Delta(T psi)]dV`.

Indeed the uncancelled algebra before expansion is
`4 psi Delta B + 4 <d psi,dB> - 4 Delta(psi B) - 2 Delta(T psi)`;
using the scalar product rule leaves precisely the displayed divergence.
The first operator is symmetric by one integration by parts. Twice integrating
T by parts, without commuting derivatives, gives

`T^* h = nabla_j nabla_i(P^{ij}h)`.

The contracted Bianchi identity is `nabla_i P^{ij}=nabla^j J`, so the same
expression may be written

`T^* h = P^{ij} Hess_ij h + 2 <dJ,dh> + (Delta J)h`.

Thus `A-A^*=-2(Delta T-T^* Delta)`. There is no additional volume derivative
inside this formal-adjoint step: A already is the complete density derivative,
and the pairing uses the background `dV_g` held fixed.

## 3. The cubic jet, including connection terms

On a Euclidean coordinate ball in the flat six-torus choose a smooth cutoff
`f`, equal to `x1 x2 x3` near its center p, and set `g=exp(2f)delta`.
Choose a second globally smooth function psi with this same local cubic.
The conformal Schouten formula is

`P_ij=-f_ij+f_i f_j-(|df|_delta^2/2)delta_ij`.

At p, `f=df=Hess f=0`; consequently `g=delta`, the first derivative of g is
zero, the Christoffel symbols vanish, and `P=0`. Differentiating gives
`nabla_k P_ij=-f_ijk`. Because the first two jets of psi vanish, differentiating
its covariant Hessian produces `nabla_k Hess_ij psi=psi_ijk` at p: both the
Christoffel term and the derivative-of-Christoffel term multiply vanishing
first or second scalar jets. Raising P's indices produces no extra term since
`partial g^{-1}=0` there.

The cubic is harmonic. The exact scalar identity
`J=-exp(-2f)(Delta_0 f+2|df|_delta^2)` shows J vanishes to order at least four,
so `J(p)=dJ(p)=0`. Also `Delta_g psi(p)=0`.

Expanding `Delta(T psi)` covariantly at p, the terms containing P or Hess psi
vanish. The sole remaining term is

`2 sum_ijk (nabla_k P_ij)(nabla_k Hess_ij psi)
 = -2 sum_ijk f_ijk^2 = -12`.

There are six ordered nonzero third derivatives, all equal to one. Meanwhile
`T^*(Delta psi)(p)=0`, since its three terms contain respectively `P(p)`,
`dJ(p)`, or `Delta psi(p)`. Therefore

`[(A-A^*)psi](p)=24`.

Also the symmetric term `-4 div(B grad psi)` is zero at p, since `B=dB=0`.
This confirms separately `A psi(p)=24` and `A^* psi(p)=0`.

All functions and the metric are globally smooth on a closed oriented torus.
The defect is continuous, hence positive on a small neighborhood. A nonnegative
nonzero smooth test function phi supported there gives
`integral phi A psi - integral psi A phi > 0`. This is a global integral
witness, with no boundary terms or restriction on conformal directions.

## 4. Eligibility and ancillary assertions

The scalar `Delta|P|^2` is a parity-even polynomial complete contraction of
curvature and its covariant derivatives. Under constant `g -> c^2 g`,
`|P|^2 -> c^-4 |P|^2` and `Delta -> c^-2 Delta`; its scalar weight is -6.
Its six-dimensional density is unchanged by constant rescaling. Its integral
vanishes for every metric on every closed manifold by the divergence theorem,
which is stronger than the required conformal invariance. A single closed
six-dimensional realization suffices to refute the universal implication.
This does not conflict with a decomposition permitting arbitrary divergences.

From `Ric=4P+Jg` and `tr P=J`,
`|Ric|^2=16|P|^2+14J^2` in dimension six. With the present Laplacian convention,
`dot J=-2 psi J-Delta psi`, whence
`d/dt integral J^3 dV = -3 integral psi Delta(J^2)dV`.
Thus `-(1/3)J^3 dV` is a local primitive for `Delta(J^2)dV`; its density
linearization is symmetric. The Ricci-norm density has adjoint defect
`16*24=384` on the same jet. Flipping the Laplacian convention reverses the
nonzero witness's sign but cannot remove the obstruction.

## First-pass finding and pending work

The universal counterexample and necessary variational criterion are valid on
this independent derivation. No mathematical repair is presently identified.
The candidate's known-source attribution, original unchanged reproducibility,
and new adversarial exact controls still require post-seal checks. Completion
of this assigned audit at first seal: 55%.
