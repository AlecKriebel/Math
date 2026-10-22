# Author turn 2 — compact completion and its verification barrier

2026-10-03 06:30 UTC. Status: partial; no global A3w certificate. Completion estimate for the full target remains 5%.

## An obstruction to the noncompact translational model

For a complete warped product on the whole strip R×R, g=dx²+f(x)²dy² with f>0, global A3w implies Gaussian curvature K=−f''/f>=0. Thus f is positive and concave on all R, forcing f to be constant: any nonzero derivative, propagated by concavity toward one end, would force f to become negative. Consequently this entire translationally invariant positive-warp class supplies only flat global-A3w surfaces. The local example of turn 1 cannot be repaired within that class.

## Explicit positively curved compact completion family

Use latitude x in [−π/2,π/2], longitude y modulo 2π, and

f_a(x)=cos x+a cos³x sin⁴x,
g_a=dx²+f_a(x)²dy².

At each pole, in inward distance r, f_a=sin r+a sin³r cos⁴r is an odd analytic function with derivative 1 at zero. Hence g_a extends smoothly to a complete rotationally symmetric metric on S². It is positive away from the poles for a>=0.

Writing z=sin²x, its Gaussian curvature is

K_a(x)=[1+a(−49z³+55z²−12z)]/[1+a(z²−z³)].

The numerator obeys

1+a(−49z³+55z²−12z)=(1−6a)+a(1−z)(49z²−6z+6).

The quadratic factor is strictly positive, since its discriminant is negative. The denominator lies between 1 and 1+4a/27. Thus K_a>0 for 0<=a<1/6, including at the poles. This is an exact global positive-curvature certificate, not an A3w certificate.

At an equatorial point, f_a=1, f_a'=0, K_a=1, ∇K_a=0, and K_a,xx=−24a. The calculation of turn 1 gives

S(r e2;e1,e1)=(2/45−4a/5)r²+O(r⁴).

Therefore every a in (1/18,1/6) is a complete compact positively curved metric failing full NNCC and satisfying strict A3w on sufficiently small product neighborhoods of the equatorial diagonal. For a=1/10 the negative coefficient is −8/225. This removes the negative-curvature defect of the first example but still does not establish global A3w.

## Bounded numerical attempt to check global weak MTW

The local script probe_mtw.py integrates the geodesic and transverse Jacobi equations and forms centered second differences of the first-variable cost Hessian. It minimizes the resulting biquadratic expression over ordinary orthogonal tangent directions. It uses a=1/10, six source latitudes, eight geodesic lengths, and fifteen initial angles per source/length (720 nominal points). This is diagnostic computation only; it does not certify minimization before the cut locus or bound finite-difference error.

The scan found positive weak-MTW values at the checked equatorial points. It found negative values at some source latitudes and length 3, extremely close to conjugacy. These points cannot yet be accepted as counterexamples to A3w: a positive endpoint Jacobi denominator alone does not prove the geodesic is distance-minimizing, and near-conjugate finite differences can be unreliable. Record them as unvalidated obstructions, not as facts about the original squared-distance tensor.

## Exact remaining gap

Determine the full minimizing cut domain and establish the sign of weak MTW on it for any one a in (1/18,1/6). A numerical positive grid cannot establish the antecedent. A negative value beyond the cut locus does not disqualify a metric for the problem. The full conjecture is not reduced to this one family: failure of this family would only close this route.
