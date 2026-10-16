# Finite inverse-square energy, regularity thresholds, and the boundary gap

AMR-019-0006 / E-6322. Shared mathematical pass 1, 2026-10-16.

## 1. Scope and result status

The entire frozen target and its baseline literature screen were read. The law is

W(F) = a|F|^6 + b|cof F|^3 + c(det F)^2 + d(det F)^{-2}

on det F > 0, with all four coefficients positive. The admissible class is the full finite-energy W^{1,6} class with the specified entire-boundary trace. The required lower bound extends to arbitrarily thin boundary collars.

This report proves auxiliary facts about finite-energy maps. It does **not** establish any extra regularity for arbitrary global minimizers. Consequently it neither proves nor refutes E-6322. Its constructions are not stationary solutions or global minimizers, and are never offered as counterexamples to the frozen benchmark. The companion `PRESSURE_REDUCTION.md` subsequently obtains a stronger conditional result for minimizers by using stationarity: global C^{1,beta} regularity, with any beta>0, suffices for whole-domain positivity.

Write J = det Dy. Finite energy immediately gives

|{x in Omega: J(x) < delta}| <= delta^2 I(y)/d.

That distribution estimate is consistent with essential infimum zero. Continuity of y, or even boundedness of Dy, does not change this by itself.

## 2. An elementary scalar positivity theorem

### Theorem 2.1: whole-domain positivity with a C^{1,1} Jacobian

Let Omega be a bounded C^2 domain in R^3. Suppose f belongs to C^{1,1}(closure Omega), f > 0 almost everywhere in Omega, and f^{-2} belongs to L^1(Omega). Then

min_{closure Omega} f > 0.

Here C^{1,1} on the closure can be interpreted chartwise; a global extension is not needed in the proof.

Proof. Continuity and positivity almost everywhere imply f >= 0 on the closure. Any negative value would give a relatively open set of negative values with positive volume.

If f(x0)=0 at an interior point, its derivative vanishes there. The Lipschitz continuity of Df yields f(x) <= C|x-x0|^2 nearby. Thus f(x)^{-2} >= C^{-2}|x-x0|^{-4}, whose integral in three dimensions diverges.

Now suppose f(x0)=0 on the boundary. Use smooth boundary coordinates (z,t), with z in R^2, t >= 0 inward, and x0 corresponding to (0,0). The coordinate Jacobian is bounded above and below. Put F(z,t)=f(Phi(z,t)). Since the nonnegative boundary function F(z,0) has a minimum at z=0, D_z F(0,0)=0. The C^{1,1} assumption gives F(z,0) <= C|z|^2, and the bounded normal derivative gives

0 <= F(z,t) <= C(|z|^2+t).

For rho=|z| small, integrate over 0<t<rho^2. On this region F <= 2C rho^2. Hence the inverse-square integral is bounded below by a constant times

integral_0^epsilon rho d rho integral_0^{rho^2} rho^{-4} dt
= integral_0^epsilon d rho/rho = infinity.

This contradicts integrability and excludes boundary zeros. Compactness of the closure now gives a strictly positive minimum. QED.

### Corollary 2.2 for the frozen energy

Every finite-energy y in C^{2,1}(closure Omega;R^3) has det Dy bounded below by a positive constant throughout the closure. The reason is that det Dy is then C^{1,1} and its inverse square is integrable.

This uses no minimality. It is a conditional sufficient criterion, not a permitted additional assumption in E-6322. In particular, the statement must not be weakened by accidentally replacing C^{2,1} regularity of y with C^{1,1} regularity of y.

## 3. Interior and boundary thresholds are different

Let f >= 0 be C^{1,alpha}, 0<alpha<=1, with an interior zero. Taylor expansion at that minimum gives

f(x) <= C|x-x0|^{1+alpha}.

In dimension n, finiteness of f^{-s} excludes such a zero whenever

s(1+alpha) >= n.

Equality also excludes it: the radial integral diverges logarithmically. For n=3 and s=2, the interior criterion is alpha >= 1/2. Thus a finite-energy deformation in C^{2,1/2} cannot have an interior Jacobian zero.

At a boundary zero, the same argument gives only

f(Phi(z,t)) <= C(|z|^{1+alpha}+t).

For s>1, integrating first in the normal variable shows that divergence occurs when

(1+alpha)(s-1) >= n-1.

For the frozen n=3, s=2 this is alpha >= 1. Therefore the corresponding energy-only boundary condition is C^{1,1} for the Jacobian. Proving C^{2,alpha} regularity of y for some alpha<1, even uniformly up to the boundary, would not alone complete an energy-integrability argument.

These are sufficient thresholds for this specific scalar Taylor argument. They are not assertions that a minimizer must attain these regularity classes before positivity can be proved; a genuinely variational or PDE argument could rule out zeros using weaker regularity.

### A slightly weaker, borderline sufficient condition

Full C^{1,1} regularity is more than the contradiction requires. At a hypothetical boundary zero it is enough to establish, in boundary coordinates,

f(Phi(z,t)) <= C[t + |z|^2(log(e/|z|))^beta]

with beta <= 1, for sufficiently small |z| and t. Normal integration then bounds the inverse-square integral below by a constant times

integral_0^epsilon d rho / [rho(log(e/rho))^beta],

which diverges for beta<=1. This singles out an exact local vanishing-rate target rather than imposing a stronger global regularity theorem.

## 4. A sharp interior obstruction below the interior threshold

On the unit ball B in R^3, choose 1<gamma<3/2 and set

y_gamma(x1,x2,x3) = (x1,x2,x3 |x|^gamma).

At the origin define the map continuously. Its nontrivial component is homogeneous of degree 1+gamma, smooth away from zero, and belongs to C^{2,gamma-1}(closure B). The other two components are linear. It has exactly the identity trace on the sphere.

Because its derivative is triangular in the first two rows,

J_gamma(x) = |x|^gamma [1 + gamma x3^2/|x|^2]

away from zero. Thus |x|^gamma <= J_gamma <= (1+gamma)|x|^gamma. The Jacobian is positive everywhere except at the origin, and

integral_B J_gamma^{-2} < infinity  iff  2gamma < 3.

Dy is bounded, so all positive-power terms in the frozen energy are integrable. Hence this is an admissible finite-energy map for every positive coefficient quadruple, with a zero Jacobian at one interior point and essential infimum zero.

It is even a homeomorphism of the closed ball onto itself: for each fixed pair (x1,x2), the third component is a strictly increasing function of x3 on the corresponding vertical interval and fixes both endpoints. This observation is not needed for admissibility.

This construction establishes sharpness of the preceding energy-only interior threshold within this simple family: it supplies every alpha=gamma-1 in (0,1/2). It is not a minimizer.

An additional caution concerns the ordinary Piola stress. For this map (cof Dy)_{33}=1. The barrier derivative contributes

-2d J_gamma^{-3}

to its (3,3) component. Its integral diverges for gamma>=1, while all positive-power stress terms remain bounded. Thus finite energy, smooth trace, homeomorphism, and even C^{2,alpha} regularity for alpha<1/2 do not guarantee locally integrable ordinary Piola stress. The separate variations lane treats the safe alternatives to ordinary additive variations.

## 5. Boundary obstruction for every C^{2,alpha}, alpha<1

### 5.1 Domain and local formula

Choose a bounded connected C-infinity domain having a flat boundary patch around the origin, with inward coordinate t=x3>0 and tangential coordinates z=(x1,x2). Such domains are obtained, for example, by smoothly flattening one small patch of a ball. Choose a sufficiently small cylindrical collar contained in this patch's coordinate neighbourhood; no other part of the boundary meets the collar.

Fix 0<alpha<1, put gamma=1+alpha, rho=|z| and r=(rho^2+t^2)^{1/2}, and define

h(z,t) = t^2/2 + t r^gamma.

The triangular map (z,t) -> (z,h(z,t)) has Jacobian

q(z,t) = partial_t h
       = t + r^gamma + gamma t^2 r^{gamma-2}.

For small r and t>=0,

c(t+rho^gamma) <= q(z,t) <= C(t+rho^gamma).

Indeed, the lower bound follows from r>=rho and the nonnegative terms. For the upper bound, t^2 r^{gamma-2} <= r^gamma, and r^gamma <= C(rho^gamma+t^gamma) <= C'(rho^gamma+t) for t<1.

The map belongs to C^{2,alpha} up to the flat boundary: t r^gamma is homogeneous of degree 2+alpha with a smooth angular part. It agrees with the identity trace (z,0) on the boundary, although its normal derivative is zero at the origin.

### 5.2 Gluing without losing orientation

Choose smooth cutoffs eta(z) and zeta(t), valued in [0,1], equal to one near zero and supported in the chosen small collar. Take zeta nonincreasing, and set chi=eta zeta. Shrink the collar until h<=t there; this is possible since h/t=t/2+r^gamma<1 for small positive t.

Set

H(z,t) = t + chi(z,t)[h(z,t)-t],

and define y(z,t)=(z,H(z,t)) in the collar and y(x)=x outside the cutoff support. Then

partial_t H = (1-chi) + chi q + (partial_t chi)(h-t).

All three displayed summands are nonnegative. For any interior point, the first two have strictly positive sum, since q>0 for t>0. Therefore det Dy>0 throughout Omega. Smooth vanishing of the cutoff near its support boundary makes the global map C^{2,alpha} on the closure.

On the flat boundary t=0, H=0. Outside this patch the map is the identity. Thus the entire boundary trace is exactly the identity, certified by the global smooth orientation-preserving diffeomorphism G(x)=x. The full trace requirement is genuinely satisfied.

At the distinguished boundary point det Dy=0; at every other point of the closure the determinant is positive. By continuity the essential infimum over the open domain is zero.

### 5.3 Finite energy

Near the origin chi=1, so J=q is comparable to t+rho^gamma. Therefore

integral_0^epsilon rho d rho integral_0^epsilon dt/(t+rho^gamma)^2
<= integral_0^epsilon rho^{1-gamma} d rho < infinity

precisely for gamma<2. Away from the origin J is continuous and positive on the relevant compact sets. Consequently J^{-2} is integrable over the whole domain. Dy is bounded, so every positive-power term is integrable as well.

We have proved that, for every alpha<1, even C^{2,alpha} regularity of a finite-energy deformation on the whole closure with smooth diffeomorphic boundary data is insufficient by itself to produce a uniform determinant lower bound.

## 6. One boundary example in all sub-Lipschitz C^{2,alpha} classes

A logarithmic variant sharpens the preceding point. For sufficiently small r, set L(r)=log(e/r), fix p>1, and replace h by

h(z,t) = t^2/2 + t r^2 L(r)^p.

Define the last term to be zero at r=0. Its second derivatives are O(r L(r)^p), and its third derivatives away from zero are O(L(r)^p). Standard integration along segments, splitting at distance comparable to the separation from the origin when needed, shows that the second derivatives are Hölder continuous of every exponent alpha<1. Thus h belongs to C^{2,alpha} for every alpha<1, simultaneously.

Its determinant is

q = t + r^2 L(r)^p + t^2[2L(r)^p-pL(r)^{p-1}].

Restrict to a collar where L(r)>p, so the final bracket is positive and r -> r^2 L(r)^p is increasing. The same estimates as before give

q comparable to t+rho^2 L(rho)^p.

One detail for the upper bound is that r<=sqrt(2)max(rho,t); monotonicity and bounded fixed-ratio changes give r^2L(r)^p <= C[rho^2L(rho)^p+t^2L(t)^p], while t^2L(t)^p<=Ct near zero. The lower bound follows from monotonicity.

The same decreasing-normal-cutoff gluing preserves positive interior determinant and identity boundary trace. The inverse-square integral converges because

integral_0^epsilon rho d rho/[rho^2L(rho)^p]
= integral_0^epsilon d rho/[rho L(rho)^p] < infinity

for p>1. Thus one admissible map belongs to every C^{2,alpha}, alpha<1, yet has a boundary-only Jacobian zero and essential infimum zero. This is consistent with the divergence for beta<=1 in Section 3.

## 7. Why none of these maps is a benchmark counterexample

For identity boundary data, the identity is the unique full-class minimizer of this law. Here is the relevant direct argument, included to make the negative status of the examples unambiguous.

For W^{1,6} competitors with identity trace, the integrals of F=Dy, cof F, and det F agree with those of the identity map. The first follows by integration by parts; the latter two are the standard null-Lagrangian identities, justified by smooth approximation at this Sobolev exponent. Apply Jensen's inequality separately to the convex functions

a|F|^6, b|K|^3, cJ^2+dJ^{-2} (J>0).

The resulting lower bound is |Omega|W(I), achieved by the identity. Strict convexity of |F|^6 forces Dy=I almost everywhere in any equality case, and the boundary trace fixes the additive constant. Every displayed nonidentity map therefore has strictly larger energy than the identity.

These examples show that a proof must use minimization or its justified consequences in an essential way; no conclusion follows merely by combining the prescribed data, finite energy, and the stated subcritical regularity.

## 8. Attempted analytic routes and exact missing steps

### 8.1 Safe stationarity is useful, but it is not regularity

For this law both material and spatial stress-growth bounds hold. Consequently minimizers satisfy Ball's inner energy-momentum and outer target-composition identities. The separate variations lane proves the relevant formulas and admissibility. These are available without first proving J>=epsilon.

However, the resulting tensors are controlled only in L^1 by the energy. Taking a divergence again, or applying a formal inverse Laplacian to isolate a scalar pressure, merely produces a distributional equation with tensor-valued L^1 data. It does not produce a scalar second-order elliptic inequality with controlled coefficients, so no determinant maximum principle has been obtained in this way.

Even if one independently improved the tensor data to L^q for a fixed finite q>1, that pressure information would not automatically give an L-infinity lower bound for J. The companion `PRESSURE_REDUCTION.md` makes the stronger global negative-norm estimate precise and combines it with independently assumed Hölder regularity to obtain a conditional entire-domain positivity theorem. The unconditional starting regularity is still missing.

### 8.2 Ordinary Euler-Lagrange bootstrapping can be circular

The determinant barrier contributes -2d J^{-3} cof Dy to DW(Dy). Finite integral of J^{-2} alone does not establish integrability of this term. Section 4 gives a concrete smooth-trace finite-energy map where this defect occurs locally. Likewise, an arbitrary additive perturbation y+tau phi need not remain orientation preserving when J has no lower bound. One cannot first write the ordinary weak equilibrium system for every Sobolev minimizer and then use it to prove the assumptions that justified writing it.

This does not prove ordinary equilibrium fails for minimizers; it identifies the gap in that attempted proof.

### 8.3 Polyconvexity does not supply the needed global derivative estimates here

The direct-method coercivity yields y in W^{1,6}, hence continuity of y. It supplies no derivative of J or cof Dy. The density is strongly rank-one convex on GL^+(3), but that statement does not amount to a proved whole-domain C^{1,alpha}, C^{2,alpha}, or Lipschitz-gradient theorem for arbitrary large-data vectorial minimizers with the singular barrier.

The usual cut-off or harmonic-replacement route needs admissible comparison maps. A convex interpolation between an admissible map and the given diffeomorphic extension need not have positive determinant. Therefore an ordinary unconstrained Caccioppoli/Gehring argument cannot simply be imported without verifying the determinant constraint in its comparison step.

### 8.4 A conditional smoothness theorem does not fill its own premise

The Bauman–Owen–Phillips publisher synopsis starts from a C^{1,beta} stationary state and states an interior C^{2,beta} / determinant-positivity consequence under its structure assumptions. Ball's discussion likewise presents this as a conditional regularity mechanism. The full 1991 theorem's structural and boundary assumptions were not independently audited in this lane, so no exact application to this law is asserted.

In any case, invoking it cannot establish the missing initial C^{1,beta} regularity for arbitrary Sobolev minimizers. An interior conclusion also does not by itself exclude determinant collapse along the boundary, as the explicit examples above emphasize.

### 8.5 A precise next proof target

A successful regularity-based approach could proceed by proving, without a prior determinant lower bound, global C^{1,beta} regularity for some beta>0: the companion pressure argument then finishes positivity on the entire closure. The energy-only route in this report instead needs the stronger local vanishing-rate control in Section 3. Alternatively a direct variational comparison could exclude a vanishing-Jacobian collar before such regularity is known.

Neither route was completed here. In particular, no admissible large-data comparison with a quantified gain on arbitrary low-Jacobian sets was constructed. This is the unresolved analytic step rather than an integrability arithmetic issue.

## 9. Source use and verification

- J. M. Ball, *Some Open Problems in Elasticity* (2002), Section 2.4, Problem 6 and Theorem 2.3. The recovered full text was consulted for the distinction between ordinary and composed variations and for the conditional regularity discussion. Public author source: https://people.maths.ox.ac.uk/ball/Articles%20in%20Conference%20Proceedings%20and%20Books/JMB%202002%20re%20Marsden%2060th.pdf
- P. Bauman, D. Phillips and N. C. Owen, *Maximal smoothness of solutions to certain Euler–Lagrange equations from nonlinear elasticity*, Proceedings of the Royal Society of Edinburgh A 119 (1991), 241–263. The publisher synopsis was inspected on 2026-10-16; it is not a full-paper theorem audit. https://doi.org/10.1017/S0308210500014815
- The frozen target and existing baseline screen were read completely. No claim of exhaustive literature coverage or novelty certification is made.

The scalar positivity proofs and explicit constructions above are derived in this pass rather than attributed to an unseen theorem. Elementary determinant differentiation and threshold arithmetic are checked separately in `check_formulas.py`; those symbolic checks supplement, but do not replace, the proofs.
