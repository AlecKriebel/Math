# Turn 2: infinite coupled error for the superlinear scheme

Status: negative answer to the source's superlinear mean-square claim for the intended scheme, pending independent review. The separate weak-rate question for bounded smooth observables is not settled. No novelty certification.

Retain D=(0,1), alpha=1/4, any nonzero nonnegative u0∈C_c^infinity(D), tau>0 and the intended substeps from Turn1. All stochastic processes use the same real Brownian motion.

## 1. Every numerical moment above one fails

Fix p>1. Choose eta∈(0,1) so that p²(1-eta)>1+eta, for example eta=(p²-1)/(2(p²+1)). Let K be the compact support of u0 and choose y0∈D. Positivity and uniform continuity of the heat kernel imply that a sufficiently small closed interval J around y0 satisfies

1-eta ≤ K_tau(y,z)/K_tau(y0,z) ≤ 1+eta, for y∈J,z∈K.

Consequently, for every finite first increment Z0, if V=U1 and V0=V(y0)>0, then (1-eta)V0≤V(y)≤(1+eta)V0 throughout J. This ratio bound is uniform in Z0; it is not a sample-dependent choice of J.

For a fixed interior output point x put mu=integral_J K_tau(x,y)dy>0 and let nu(dy)=K_tau(x,y)dy/mu on J. Jensen's inequality in its logarithmic form yields, conditionally on Z0,

U2(x) ≥ mu exp(integral log V dnu + Z1 integral V^alpha dnu - (tau/2) integral V^(2alpha) dnu).

Taking the p-th power and integrating the independent N(0,tau) increment Z1 therefore gives

E[U2(x)^p | Z0] ≥ mu^p ((1-eta)V0)^p exp(D_p V0^(1/2)),

where D_p=(tau/2)[p² sqrt(1-eta)-p sqrt(1+eta)]>0. The inequality defining eta proves the positivity of this constant. Turn1 gives V0≥C exp(bZ0) on Z0≥0. The resulting Gaussian integral diverges by the same double-exponential lower bound. Thus E U2(x)^p=infinity for every p>1.

This also holds at every later grid index m≥2. The finite-first-moment identity in Turn1 implies

E[U_m(x) | F_(2tau)] = (E_((m-2)tau) U2)(x).

Conditional Jensen gives E U_m(x)^p ≥ E[(E_((m-2)tau)U2)(x)^p], in extended nonnegative reals. By semigroup composition the latter random field has the same second-step expression with the outer heat kernel K_((m-1)tau) in place of K_tau. Its weight on J remains positive, so the preceding proof applies verbatim. First moments nevertheless remain finite.

## 2. Exact scalar comparison process and its moments

Let M=||u0||_infinity>0, and solve dY=Y^(5/4)d beta, Y(0)=M. The transformation R=4Y^(-1/4) gives, by Itô's formula,

dR=-d beta + (5/(2R))dt, R(0)=4M^(-1/4).

This is a six-dimensional Bessel process (with Brownian motion -beta). It is positive and finite for all finite times, hence Y=(4/R)^4 is finite and continuous on every compact time interval. These standard Bessel facts are documented in Gregory Lawler's *Notes on the Bessel Process*, introduction and Section2, especially Proposition2.1; the transformation and moment bound here are explicit.

At each fixed t>0, R_t has the distribution of the Euclidean norm of a six-dimensional normal vector with covariance tI and a fixed nonzero starting vector. The Gaussian density is bounded by (2 pi t)^(-3). On the unit ball, the integral of |z|^(-4p) is proportional to integral_0^1 r^(5-4p)dr, finite exactly when p<3/2. Outside that ball the integrand is bounded by1. Therefore E Y_t^p<infinity for every fixed t>0 and 0<p<3/2. No claim about E sup_(s≤T)Y_s^p is used or required.

## 3. Localized SPDE comparison, without a hidden C² assumption

We explain why the canonical nonnegative local mild solution exists globally and is bounded by Y, rather than assuming square integrability of the superlinear equation. Extend g(v)=v_+^(5/4) from nonnegative states. For each level K>M choose a globally Lipschitz C¹ cutoff g_K which agrees with g on [0,K] and satisfies g_K(0)=0. Let u^K be the standard globally Lipschitz Dirichlet SPDE solution with this coefficient, and Y^K the scalar solution with the same coefficient and initial value M, driven by the same beta. Their continuous versions exist in dimension one by the usual globally Lipschitz theory used in the cited source.

Both are nonnegative. For u^K this follows from the negative-part energy inequality; for Y^K it follows from pathwise uniqueness and the absorbing zero solution. Moreover u^K≤Y^K. Here is the relevant comparison calculation, which only needs Lipschitz coefficients. Apply the variational Itô formula (or its smooth positive-part approximation) to

Phi(t)=integral_D [(u^K(t,x)-Y^K(t))_+]² dx.

The positive part has zero boundary trace because u^K has Dirichlet boundary0 and Y^K≥0. Integration by parts gives the nonpositive drift term -2 integral_D |partial_x(u^K-Y^K)_+|² dx. The quadratic variation term is

integral_D 1_{u^K>Y^K}|g_K(u^K)-g_K(Y^K)|² dx ≤ L_K² Phi(t).

The stochastic integral has zero expectation after localization; the globally Lipschitz moment bounds allow removal of that localization. Since Phi(0)=0, Gronwall gives Phi(t)=0 almost surely, and spatial/time continuity yields the pointwise comparison. The same calculation with zero gives positivity. The C² noise hypothesis in the older Cresson positivity theorem is not silently imposed on v_+^(5/4); this energy proof bypasses that mismatch.

Let sigma_K=inf{t:Y_t≥K}. Until sigma_K, the cutoff scalar process agrees with Y; thus 0≤u^K≤Y<K. All larger cutoffs agree with u^K on that interval by local pathwise uniqueness. Since sup_(t≤T)Y_t is finite almost surely for every finite T, sigma_K tends to infinity. Patching gives a unique continuous nonnegative global *local mild solution* u with

0≤u(t,x)≤Y_t.

Here the stochastic convolution is understood locally: its square-integrability on stopped intervals is enough, and no unproved global L² moment is asserted. In particular E u(t,x)^p<infinity for every fixed t>0 and 0<p<3/2.

## 4. Consequence for the actual coupled error

Take p=5/4. For every grid index m≥2 and every interior x, the numerical p-th moment is infinite whereas the exact solution's p-th moment at t=m tau is finite. If U_m(x)-u(m tau,x) had finite p-th moment, the triangle inequality would give a finite p-th moment for U_m(x), a contradiction. Hence

E|U_m(x)-u(m tau,x)|^(5/4)=infinity.

On a probability space L² is contained in L^(5/4), so the mean-square error is also infinite. More generally every error moment of order r>1 is infinite, by choosing p∈(1,min(r,3/2)).

Thus, for any fixed horizon T>0 and every uniform partition with M≥2, the final-time mean-square error is infinite. In particular the claimed unconditional mean-square half-order bound cannot hold for this unmodified scheme and this admissible initial datum. This conclusion compares two coupled random variables and does not subtract infinite moments.

## 5. Weak-convergence scope and remaining work

The unbounded test phi(v)=v^(5/4) has an infinite numerical expectation and finite exact expectation, so it cannot have a finite weak error. That says nothing by itself about bounded smooth tests. It also does not settle the source's distinct weak-SPDE question under globally Lipschitz assumptions. Convergence in probability or bounded-test convergence may coexist with the moment failure. These distinctions must be preserved in any eventual disposition.

`verify_turn2.py` supplies exact algebraic controls for the Jensen coefficient, Bessel transformation and integrability threshold. Finite tests do not prove SPDE comparison; that argument is given above and requires independent review.
