# Proposed frozen research target E-6322

AMR-019-0006 · formulation only · mathematical passes: 0

## Complete statement

Let a,b,c,d be arbitrary fixed finite positive real numbers. For F in R^{3x3}, using the Frobenius norm, define

W_{a,b,c,d}(F) = a|F|^6 + b|cof F|^3 + c(det F)^2 + d(det F)^{-2}, if det F>0,

and W_{a,b,c,d}(F)=+infinity if det F<=0.

Let Omega be any nonempty bounded connected open subset of R^3 with C-infinity boundary. Let U be an open neighbourhood of the compact set closure(Omega), and let G:U -> G(U) be a C-infinity diffeomorphism satisfying det DG>0 throughout U. Prescribe g=G|boundary(Omega) on the **entire** boundary. There are no body forces or traction terms. No closeness to an affine map, small strain, radial symmetry, topological-ball restriction, or size restriction on G is imposed.

Define

I(y) = integral_Omega W_{a,b,c,d}(Dy(x)) dx,

A_g = {y in W^{1,1}(Omega;R^3) : I(y)<infinity and Tr(y)=g on boundary(Omega)}.

Equivalently for this density and these boundary data, this is the full class

{y in W^{1,6}(Omega;R^3) : Tr(y)=g, det Dy>0 a.e., (det Dy)^{-2} in L^1(Omega)}.

The cofactor-cubic and determinant-square terms are integrable for W^{1,6} maps. Neither injectivity of y nor any higher regularity is included in A_g. It is not the strong or weak closure of a smooth or diffeomorphic comparison class: every map meeting the displayed conditions is a competitor.

The proposed assertion is:

**For every a,b,c,d, Omega and g as above, every y_* in A_g satisfying I(y_*)<=I(z) for all z in A_g has some epsilon=epsilon(y_*,a,b,c,d,Omega,g)>0 with det Dy_*(x)>=epsilon for almost every x in Omega.**

The conclusion is an essential bound over all of Omega, including arbitrarily thin regions next to its boundary. No trace of Dy_* or pointwise boundary derivative is assumed. Epsilon is not required to be common to all minimizers, domains, data or coefficients. The mathematical target depends on the trace g, not on which admissible extension G was used to certify that g is allowed.

The data class includes affine traces, but the substantive assertion covers **all permitted nonaffine traces** as well. Establishing only the affine subset, or a small neighbourhood of it, does not resolve E-6322.

## Established structural baseline, not the research conclusion

The law is nonnegative, homogeneous in the material variable (independent of x and y), compressible, frame-indifferent and isotropic, and smooth on GL^+(3). It is polyconvex through the convex extended-valued function of the independent variables F, cof F and det F. It satisfies the coercive existence hypotheses in Ball (2002), Theorem 2.1. The smooth extension supplies a finite-energy competitor. Thus the direct-method existence baseline is nonvacuous; E-6322 asks for an additional property of those minimizers.

The numerical exponent choice is intentional and limited: 6,3,2 align the positive-power degrees of F, its second-order minors, and its third-order minor. The barrier exponent is exactly 2. It has not been selected using a proved positivity threshold. Standard existence, determinant positivity a.e., and continuity of y are not the proposed lower-bound theorem. No claimed regularity theorem is imported from strict polyconvexity alone.

The source allows a much wider class. A possible later family-level question can be stated precisely by replacing the fixed tuple with finite p>3, q>=3/2, r>1, s>0 and asking whether **there exists** a tuple for which the corresponding assertion holds for all positive coefficients and all the same data. That is a distinct existential research target, not an automatic fallback or a licence to adjust this frozen statement after seeing a result.

## What each outcome means

- A proof of E-6322 supplies explicit sufficient constitutive and data assumptions within Ball's global first-gradient programme.
- A proof only for a=b=c=d=1 is a genuine narrower sufficient-condition theorem if it covers every permitted datum and full-class minimizer, but is not a proof of the entire coefficient-family benchmark.
- One compliant counterexample falsifies E-6322. It does not falsify the existential exponent-family question or Ball's entire search for adequate growth assumptions.
- A counterexample family for every exponent tuple in the displayed later range would rule out that particular finite-power programme, while still not ruling out every other possible first-gradient constitutive condition.
- A near-affine theorem, a symmetric calculation, an interior estimate, or a conditional theorem assuming minimizer regularity is neither a positive nor a negative resolution of this target.

## Source

J. M. Ball, Some Open Problems in Elasticity (2002), author manuscript: Problem 6, p.11, with equation (2.19), p.10; Sections 2.1-2.4 and Theorem 2.1 distinguish the model, admissible class, existence and positivity questions.

https://people.maths.ox.ac.uk/ball/Articles%20in%20Conference%20Proceedings%20and%20Books/JMB%202002%20re%20Marsden%2060th.pdf
