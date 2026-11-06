# Independent mathematical audit: exact particle pinning obstruction

## Verdict and exact scope

**ACCEPTED as an exact nonconvergence example outside the sufficient quantization/regularization scaling, and as an obstruction to an unconditional energy-only compactness argument.** Every proximal minimizer has the same stationary projected velocity. The construction is not dependent on a special selection of nonunique Lagrangian maps. It is not a counterexample when δ_N²/ε→0, and does not refute the accepted theorems in Approaches 2–4.

The complete frozen file audited was `APPROACH_05_COMPACTNESS_AND_PINNING.md`, 6,710 bytes, SHA-256:

`db18e2ed0ff17f6119fd1e5c0d6bf867fd2d9bdcca9a8d4ae89989fa524378f5`

The author confirmed this freeze. The audit snapshot is `FROZEN_APPROACH_05.md`. No author file was edited. The subdensity/map equivalence used below is the elementary proximal-existence argument independently checked in the A2 audit; the pinning construction does not require its convergence theorem.

## 1. The covariance identity has the correct sign

At a configuration X∈H_N with a currently chosen proximal map Y, the continuously updated particle velocity is V=(Π_NY−X)/ε. Since ∇φ(X) is cellwise constant,

d/dt∫φ dμ_N=ε^(−1)〈Y−X,∇φ(X)〉.

Split ∇φ(X)=∇φ(Y)+[∇φ(X)−∇φ(Y)]. The proximal first variation for v=∇φ, supported strictly inside Ω, changes the first term to ∫rᵐΔφ. The fundamental theorem of calculus on the segment from Y to X changes the second to

−ε^(−1)∫(X−Y)^T[∫₀¹D²φ(Y+s(X−Y))ds](X−Y)dρ₀.

This is exactly candidate (1.1), including the minus sign. Bounded regularized energy only bounds ||X−Y||²/ε; it does not force this covariance term to zero. On an actual frozen interval there is also a displacement-from-node term. In the stationary example below that displacement vanishes identically, so no time-freezing issue remains.

The general compactness preamble can be read with a fixed bounded set containing the particle locations, rather than necessarily Ω itself: starting from barycenters in conv(Ω), the frozen ODE is a convex combination of its old locations and proximal barycenters in conv(Ω). The action bound gives W₂ equicontinuity on this common bounded hull. This observation does not identify the limiting nonlinear flux.

## 2. Normalization and scales of the explicit bumps

Let α=1/(m−1) and I=∫_{|z|<a}(a²−|z|²)^α dz. For every d≥1, m>1, 0<a<1/2, this number is finite and strictly positive. The candidate chooses

c=(m−1)I^{m−1}/(2m),

so [(m−1)/(2mc)]^α=I^(−1). Therefore f(z)=I^(−1)(a²−|z|²)_+^α has exactly unit mass. No factor of h or number of particles is missing.

For h=1/n, ε=ch², and cube centers x_i, each r_i(y)=f((y−x_i)/h) has mass hᵈ. Its support ball has radius ah<h/2, is contained in its initial cube, and lies strictly inside Ω=(−1,2)ᵈ. Distinct balls are disjoint. The initial projection error is the sum of d independent uniform-cell variances, δ_N²=dh²/12.

## 3. Exact global minimality

Put c_i(y)=|x_i−y|²/(2ε), ℓ=a²/(2c), and r=Σr_i. On B_{ah}(x_i),

U'(r)=m r^{m−1}/(m−1)=(a²−|(y−x_i)/h|²)/(2c)=ℓ−c_i.

On B_{ah}(x_j), i≠j, the triangle inequality and a<1/2 give |y−x_i|≥h−|y−x_j|>|y−x_j|, so c_i>c_j and c_i+U'(r)>ℓ. Off all balls, r=0 and each c_i≥ℓ. Thus g_i=c_i+U'(r)−ℓ is nonnegative everywhere and vanishes on the support of r_i.

For any admissible competitor tuple (s_i), write s=Σs_i. The objective difference has the exact decomposition

J(s_i)−J(r_i)
=∫[U(s)−U(r)−U'(r)(s−r)] + Σ_i∫g_i s_i.

The mass constraints remove Σ_iℓ∫(s_i−r_i), and g_i r_i=0 removes the remaining reference terms. Both terms in this decomposition are nonnegative: U is convex and each g_i,s_i≥0. Hence the proposed tuple is a global minimizer over all nonnegative subdensities with the prescribed masses. The proof is not restricted to a local perturbation, a tessellation ansatz, or radially symmetric competitors.

## 4. Every minimizing allocation, and every minimizing map, has the same barycenters

This is a crucial quantifier and it is valid.

For any other minimizing tuple, equality holds in the preceding nonnegative decomposition. Strict convexity of U on [0,∞) forces s=r almost everywhere from the vanishing convexity remainder. For i≠j, g_i>0 at almost every point of B_{ah}(x_j), so vanishing of Σ∫g_i s_i forces s_i=0 there. Thus on the jth ball, s_j=r=r_j. Outside all balls s=r=0 forces every s_i=0. Sphere boundaries have zero Lebesgue measure. Consequently s_i=r_i almost everywhere for every i: the entire optimal allocation tuple is unique, even though individual source-to-target maps need not be.

Every finite-energy Lagrangian minimizer Y induces an admissible tuple Y#(ρ₀1_{P_i}), with exactly the same objective. The map/subdensity equivalence proved in A2 says that the tuple minimum and map minimum agree. Hence the induced tuple of every minimizing Y must be the unique tuple just identified. Therefore

w_i(Π_NY)|_{P_i}=∫_{P_i}Y dρ₀=∫y r_i(y)dy=w_i x_i

by radial symmetry of f. This proves Π_NY=X for every proximal minimizer, without selecting a particular transport map.

## 5. Exact stationarity for the original frozen scheme

For any selected minimizer at the initial configuration, the projected ODE is dot X_N=(X_N(t₀)−X_N(t))/ε, whose initial value is X_N(t₀); its unique solution is constant. At the next node the identical configuration produces the identical optimal allocation and projected proximal barycenters. Induction gives a constant particle curve on every time mesh and at all times. Equivalently the exponential frozen solution is the same point throughout each interval.

This is exact time-discrete and continuous-time stationarity. It persists if τ/ε→0 and is not a truncation error, a solver error, or an adverse selection among minimizers.

## 6. The stationary continuum limit fails the PDE

The cell coupling bounds W₂²(μ_N,ρ₀dx)≤δ_N²→0. Since the particle curves are constant, their entire time-dependent limit is ρ(t,x)=1_{(0,1)ᵈ}(x).

A smooth compactly supported φ in Ω can equal x₁²/2 on a neighborhood of [0,1]ᵈ because that cube has positive clearance from ∂Ω. Therefore ∫ρ₀ᵐΔφ=1, whereas the derivative of ∫φρ is zero. To state the distributional contradiction explicitly, multiply by any smooth time test η compactly supported inside the evolution interval with nonzero integral. The time-derivative side is −(∫φρ₀)∫η'=0; the Laplacian side is ∫η≠0. Thus the limiting curve is not a porous-medium weak solution, independently of which no-flux formulation is used at the distant wall.

## 7. Compactness bounds really hold while the defect survives

Changing variables in the disjoint bumps and using nᵈhᵈ=1 gives exactly

F_ε(X_N)=(2c)^(−1)∫|z|²f(z)dz+(m−1)^(−1)∫f(z)ᵐdz,

independent of n. These integrals are finite. The nearest-center assignment is optimal for transport from r to the empirical measure: each ball lies entirely in its center's strict Voronoi region, and supplies exactly that center's mass. Hence its squared W₂ distance is h²∫|z|²f=O(h²)=O(ε). The action dissipation is zero.

For the quadratic test above, every segment between x_i and its bump lies in the region where D²φ=e₁⊗e₁. Its covariance term is exactly c^(−1)∫z₁²f>0, independent of n. The diffusion term is ∫fᵐ. They are equal: differentiating U'(f)=(a²−|z|²)/(2c) gives ∂₁fᵐ=−z₁f/c, and integrating ∂₁(z₁fᵐ) over the ball, whose boundary contribution vanishes, yields

∫fᵐ=c^(−1)∫z₁²f.

This proves the claimed exact cancellation. It is a continuum identity for all d,m in scope, not a finite numerical observation.

Finally δ_N²/ε=d/(12c)>0 for all n. Thus the construction violates δ_N²/ε→0. It shows that arbitrary joint limits N→∞, ε→0 with merely bounded initial regularized energy are insufficient. It does not prove that the sufficient scale condition is necessary for every initial density or every particle arrangement, and does not answer whether all irregular solutions converge under that condition.

## 8. Contextual source and patch disposition

The cited [April 2025 conference timetable](https://indico.math.cnrs.fr/event/13361/timetable/?view=standard) was checked directly. Quentin Mérigot's abstract for “Particle discretization of Wasserstein gradient flows” identifies spurious stationary points of the particle ODEs as an obstacle to convergence analysis. That primary abstract corroborates the general obstruction only; it is not a source for the explicit proof above or a certification of its originality.

No mathematical patch is needed. The exact decomposition in §3 and its equality case in §4 expand the candidate's brief uniqueness sentence and verify its strongest “every minimizer” assertion. The overall unresolved status must remain partial: identification of the nonlinear flux for arbitrary irregular data under the sufficient vanishing quantization scale is not supplied.

The author's A5 diagnostic script was read and independently rerun: 50,030 finite/symbolic checks passed, including the exact one-dimensional m=2 identity; all three supplied mutation controls failed at their intended assertions. These diagnostics are supplementary and are not the proof of the general construction.
