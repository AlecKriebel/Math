# Positivity lane: final accepted result inventory and remaining gap

E-6322, five shared passes, 16 October 2026.

## Final answer to the frozen target

**Unresolved.** The work proves neither a global essential lower determinant bound for every full-class minimizer nor a compliant counterexample. The arbitrary coefficients, arbitrary smooth domains and complete smooth diffeomorphic boundary data, full finite-energy W^{1,6} class, and entire-domain conclusion have not been weakened.

A class-level degenerating map is not a minimizer counterexample. A restricted stationary calculation, a conditional modulus criterion, an inverse moment, or an interior estimate is not the full theorem.

## Unconditional facts established for actual minimizers

1. Safe material compositions yield the distributional stress equation div[pI+Q(Dy)]=0 with p=3dJ^{-2} initially in L^1. Ordinary unrestricted additive Euler stationarity was not assumed.
2. Finite radial and whole-boundary collar comparisons are available, but their right sides retain the initially L^1 positive-degree energy.
3. A boundary-preserving reference truncation is genuinely admissible and gives a bad-set energy estimate. Its safe levels lie below an explicit finite ceiling; the fixed complete trace bounds that ceiling through the prescribed image volume.
4. Fixed-direction and rank-one-connected finite comparisons give quantitative coercivity of gradient, cofactor, determinant, and reciprocal determinant differences.
5. Same-trace rank-one-connected endpoints with merely nonnegative Jacobian force a weighted inverse-cube moment, with the exact residual barrier coefficient 2. The endpoint need not itself have finite barrier energy.
6. The final coupled-endpoint theorem removes the rank-one restriction whenever the two mixed determinants and the endpoint determinant are nonnegative. It forces integral (cof Dy:Dv)J^{-3}<infinity and the explicit variational bound in `COUPLED_ENDPOINT_MOMENT.md`.
7. An inner-stationary deformation that is conformal almost everywhere has constant positive Jacobian. This is a restricted structural consequence, without any assumption that general minimizers are conformal.

The actual weak inverse, its full boundary trace, exact inverse class, and structured inverse comparisons are established in the other lanes and are not re-proved here.

## Whole-boundary conditional positivity tools

- If Dy belongs to L^{6q}, q>1, the pressure estimate gives J^{-2} in L^q globally. This transfers a gradient improvement; it does not create one.
- A Dini-continuous representative of Q(Dy) gives p in L^infinity over the whole domain, without assuming a pressure or Jacobian trace.
- The final continuous-gradient criterion is weaker than Dini continuity of the gradient: omega(r)^2[1+integral_r^R omega(t)dt/t] tending to zero along a sequence suffices. In particular a uniform log-Hölder gradient modulus with exponent greater than 1/3 excludes every interior and boundary Jacobian zero.

None of these extra premises has been proved for an arbitrary minimizer under only the frozen hypotheses.

## Concrete obstacles that were verified, not mistaken for impossibility theorems

- Positive endpoint determinants, smoothness, and small unnormalized excess do not make affine interpolation orientation-preserving.
- A class-wide uniformly positive fixed-direction repair is false, even for a C^1 finite-energy radial homeomorphism. Projection-volume marginals obstruct every fixed target direction in that example. It is explicitly nonminimizing.
- Taking smaller amplitudes does not erase the barrier source in the one-sided estimate.
- The positive minor energy supplies strong quasiconvex lower coercivity but no automatically admissible upper cutoff comparison.
- The exact rank-one ellipticity ratio at tI grows as t^{-12}, with shear stiffness tending to zero. Barrier-normalized affine excess loses uniform unweighted strain coercivity.
- Smooth complete outer trace does not imply smooth or Lipschitz traces on arbitrary interior comparison spheres from class membership alone.
- The regularization and pressure estimates do not silently provide an endpoint q=1 bootstrap or a backward transfer from inverse-Jacobian moments to gradient higher integrability.

## The precise remaining positive bridge

One needs a minimizer-specific construction or estimate that controls arbitrary low-Jacobian regions without already assuming the desired lower bound or its regularity consequences. In the current comparison route, this means an actual compatible, complete-trace coupled repair with sufficiently favorable mixed determinants and controlled positive-energy cost, or a genuine local excess/tail inequality that removes the un-improved barrier/strain source and remains valid next to the entire boundary.

The final coupled theorem does bypass the previous fixed-direction obstruction for the exact radial diagnostic map: its interpolation toward the identity is admissible and has a divergent negative energy derivative. But no construction achieving the necessary coupled hypotheses for an arbitrary minimizer was found. The existence of the original smooth extension alone does not impose those mixed signs relative to Dy.

No sixth mathematical pass is included in this inventory. The accepted conclusion is rigorous partial progress and a precisely identified gap, not a claimed resolution or a negative answer to Ball's wider first-gradient programme.
