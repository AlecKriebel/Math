# Independent ROOT scalar-kernel and analytic audit

2026-10-07. This records verification of the submitted candidate, not a new central proof attempt. Initial mathematical assessment: no defect found; the final mathematical gate also requires the independent reviewers' final verdicts. Priority is a separate gate.

The original report was read in full for the target paragraph and visually checked at printed p.1452 (PDF zero-based71). It asks for the joint distribution for random or equidistant starts, without specifying a density or named law. All three freshly obtained primary PDFs match the submission's source hashes. The Mörters--Peres theorem and proof were actually read at printed pp.43--44/PDF one-based53--54; an earlier extraction at the wrong page offset remains explicitly a preliminary candidate, and supplied no theorem verification.

## An independent route to the scalar exit flux

Write the killed interval heat kernel by reflected Gaussian images:

    H(t;alpha,beta) = (2*pi*t)^(-1/2) sum_n
        [exp(-(beta-alpha+2*n*ell)^2/(2*t))
         - exp(-(beta+alpha+2*n*ell)^2/(2*t))].

Differentiation at beta=0 and division by two give the left outward exit density

    f0(t;alpha,ell) = (2*pi)^(-1/2) t^(-3/2) sum_n
        (alpha+2*n*ell) exp(-(alpha+2*n*ell)^2/(2*t)).

The right density follows by replacing alpha with ell-alpha. These formulas independently fix the sign and the factor of two in the submitted spectral flux. For s>0, the Laplace transform of an individual signed image is sign(d)*exp(-abs(d)*sqrt(2*s)), where d=alpha+2*n*ell. Summing the two geometric series gives

    [exp(-alpha*r)-exp(-(2*ell-alpha)*r)]/[1-exp(-2*ell*r)]
        = sinh((ell-alpha)*r)/sinh(ell*r),   r=sqrt(2*s).

The complementary right transform is sinh(alpha*r)/sinh(ell*r). Their sum is cosh((alpha-ell/2)*r)/cosh(ell*r/2), confirming that a singleton circle target requires both interval endpoints. Limits at s=0 give the two harmonic exit masses, summing to one; differentiation at zero gives total mean exit time alpha*(ell-alpha).

Positivity and mass are established analytically through the killed-kernel exit interpretation and bounded optional stopping. No claim relies on termwise integration of the signed spectral series near t=0. Later deterministic integrals use the already summed nonnegative kernels. For each positive t the spectral expansion and required derivatives converge absolutely and locally uniformly; this does not license absolute termwise improper time integration.

The supplied checker independently compares formal sinh coefficients with an ODE recursion. My distinct diagnostic compares the image representation with the spectral representation in 180 left/right cases at 105 decimal digits, including starts close to either endpoint and short/long times. Maximum density error after multiplication by ell^2 was approximately 2.34e-101; the maximum relative discrepancy where that scaled density exceeded 1e-50 was approximately 5.45e-73. Another 120 checks compare image-geometric Laplace normalization and the singleton cosh identity. These are finite high-precision diagnostics, not certified quadrature or a uniform numerical error theorem.

## Finite-target and complete-law audit

Successive stopping times hit the remaining finite targets, remove only the just-hit query from the auxiliary target set, and restart the same physical walker at that circle position. The original physical walker is never stopped or coalesced. The interval kernel absorbs only unvisited query targets. The Markov state needs the remaining set and current circle position; winding history does not add a hidden state. Finite interval exits and distinct finite query configurations make all these stopping times finite and strictly successive. The strong Markov property supplies a product of joint increment/endpoint densities; impossible orders have a zero factor.

Each queried first-hitting time is the sum of the increments up to that target in that walker's order. Comparisons across distinct walker rows define proper linear hyperplanes for ties. The product increment density assigns these hyperplanes zero mass, and the strict owner cones partition the positive orthant outside those null boundaries. No independence between one walker's distinct target times is imposed.

Joint measurability follows because a continuous path's range up to a fixed time is compact, and the distance of a query point from that range is a countable infimum of continuous distance functions. For any fixed query outside the seeds, hitting times are finite and atomless; independence across walkers rules out ties there. Fubini gives almost-sure zero spatial measure of tied queries, rather than claiming ties never occur anywhere on the circle. Query repetitions and query/seed coincidences are spatial null sets, and coincident IID seeds are a start-law null set.

For nonnegative theta, the random variable Z=sum(theta_i*L_i) lies in [0,max(theta)]. Tonelli gives the tensor-moment coefficient from finite-query ownership. The absolute exponential series is bounded by exp(max(theta)), so averaging term by term is justified. Taylor's remainder for exp(-z), z>=0, uses derivatives of absolute value at most one: no extra exponential factor is required in theta_max^(M+1)/(M+1)!. The coefficient and remainder bounds are uniform in the seeds, justifying averaging over the IID-uniform starting law.

All mixed moments are recoverable from the homogeneous polynomials E[(theta dot L)^m]. Bounded simplex support justifies differentiation and polynomial approximation. Stone--Weierstrass and uniqueness against continuous test functions identify the whole Borel probability measure. Thus the displayed deterministic transform is more than a path-expectation definition: every coefficient is reduced to explicitly specified scalar functions, finite permutations and finite-dimensional integration. It meets the literal requested distribution format, subject to the remaining priority gate. A compact density, named family, certified quadrature and efficient algorithm are separate refinements not supplied here.

Equidistant starts have dihedral symmetry, not unrestricted permutation symmetry for k>=4. IID-uniform labeled starts give exchangeability; sorting labels would define a different seed law and must not be silently substituted. For circumference c, multiply normalized lengths by c (or replace theta by c*theta); a common time/diffusivity rescaling leaves ownership unchanged.

## Reproducibility caution

The submitted author's `ck` uses Python `assert`; optimization removes its actual guard while leaving reported counters. Its archived historical 8,520-check receipt is accepted only for the normal run. This is a supporting-code robustness issue, not a defect in the Brownian proof. A publication verifier should use an explicit failing guard, then demonstrate that it rejects false checks normally and with optimization. Historical submitted and replay files must remain unchanged in the original archive; any repair belongs in a separately identified working/portable verifier.
