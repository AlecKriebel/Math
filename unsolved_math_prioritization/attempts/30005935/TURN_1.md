# Turn 1: positivity with two-step second-moment failure

Status: proved scheme properties and a moment obstruction. A claim about the coupled error requires an additional exact-solution argument and is not inferred merely from two infinite moments. The separate bounded-test weak question remains unresolved.

## 1. Intended scheme and pathwise finiteness

Use the substep-defined scheme in SOURCE_SCOPE.md. Put alpha=1/4, Z_m=beta((m+1)tau)-beta(m tau), and

H_tau(v,z)=v exp(v^alpha z - tau v^(2alpha)/2), v≥0.

Then U_(m+1)=E_tau H_tau(U_m,Z_m). For every finite z and tau>0, H_tau is nonnegative, continuous at zero, and bounded on [0,infinity). Indeed writing a=v^(1/4) gives a^4 exp(az-tau a²/2), which tends to zero as a tends to infinity. Its unique positive maximum occurs at a=(z+sqrt(z²+16tau))/(2tau), by differentiating its logarithm. Thus each numerical iterate is almost surely finite, continuous and nonnegative for bounded continuous nonnegative initial data; the Dirichlet heat semigroup preserves these properties. A nonzero initial profile gives strict positivity in the interior at positive grid times. No uniform moment conclusion follows from this pathwise bound.

For the moment obstruction it suffices to take d=1, D=(0,1), and any nonzero u0∈C_c^infinity(D) with u0≥0. All these initial data satisfy the source's regularity and boundary conditions.

## 2. First moments are finite

Condition on the first m Brownian increments. At each spatial point, U_m and its frozen coefficient are finite. The Gaussian exponential has conditional expectation1. By conditional Tonelli and heat-semigroup composition,

E[U_(m+1)(x) | F_(m tau)] = (E_tau U_m)(x),

and therefore E U_m(x)=(E_(m tau)u0)(x)<infinity. Moreover U_1 has finite moments of every finite positive order: if M=||u0||_infinity, then U_1(x)≤M exp(M^(1/4)|Z_0|), and Gaussian absolute exponential moments are finite.

## 3. Exact conditional second-moment identity

Write K_tau for the strictly positive Dirichlet heat kernel, V(y)=U_1(y), and a(y)=V(y)^(1/4). The same Brownian increment Z_1 is used at every point. Expanding the square, using Tonelli and E exp(cZ_1)=exp(tau c²/2), gives the equality in the extended nonnegative reals

E[U_2(x)^2 | Z_0]
= integral integral K_tau(x,y)K_tau(x,z)V(y)V(z) exp(tau a(y)a(z)) dy dz.

The cross term is crucial; independent pointwise noises would be a different source problem. For every fixed finite Z_0 the conditional integral is finite, since V is bounded. It need not have a finite expectation over Z_0.

## 4. Uniform interior lower bound and divergence

Choose compact intervals I,J inside D with positive lengths and u0≥c>0 on I. Strict positivity and continuity give min_{y∈J,z∈I}K_tau(y,z)=kappa>0. For Z_0≥0 and M=||u0||_infinity,

V(y)≥kappa |I| c exp(c^(1/4)Z_0 - tau M^(1/2)/2)=C exp(b Z_0), y∈J,

where C,b>0. Put mu=integral_J K_tau(x,y)dy>0 for any fixed interior x. The identity above yields

E[U_2(x)^2 | Z_0] ≥ mu² C² exp(2b Z_0) exp(tau C^(1/2) exp(b Z_0/2))

on Z_0≥0. Multiplying by the N(0,tau) density, the logarithm of the lower integrand differs by a constant from

2bz + tau C^(1/2) exp(bz/2) - z²/(2tau).

It tends to positive infinity as z tends to infinity, so its integral over the positive half-line diverges. Consequently

E[U_2(x)^2]=infinity

for every tau>0 and every interior x, despite almost-sure finite positive iterates and finite first moments. This is an analytic tail proof, not a Monte Carlo inference.

## 5. Consequences and exact remaining gap

An unconditional numerical second-moment bound of the globally Lipschitz form cannot hold for this superlinear scheme. If a coupled reference random variable belongs to L², then its difference from U_2(x) cannot belong to L², by the triangle inequality. However this turn has not proved that the exact superlinear SPDE lies in L², so it does not yet assert an infinite coupled error. A lower integrable moment of the exact solution together with a corresponding higher-moment failure of the scheme would be another valid route; that requires further work.

Finite-sample simulations can miss the rare events causing the divergence. This does not by itself rule out convergence in probability or convergence of bounded observables. The original source's separate weak-rate question must be kept distinct.

## 6. Checks

`verify_turn1.py` checks the Gaussian cross-exponent cancellation with exact fractions, positivity of the coefficients in finite positive-kernel controls, the maximum's stationarity identity algebraically, and the elementary exponential-versus-quadratic tail mechanism using exact rational lower bounds. The proof, not the bounded checker, establishes the infinite moment for the continuum heat kernel.
