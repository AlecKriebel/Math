# Approach 5: an energy-compactness attempt and an exact pinning obstruction

**Problem:** 30004633. **Author continuation:** approach 5. **Outcome:** rigorous obstruction to an unconditional energy-only convergence argument; the general irregular-solution problem remains open here. The counterexample violates the sufficient condition δ_N²/ε→0 and is therefore **not** a counterexample to Approaches 2–4 or to convergence under that scaling.

## 1. Why try compactness?

For arbitrary finite-energy initial density, the original frozen scheme gives

\[
\mathcal F_\varepsilon(X_N(t_n))\le\mathcal F_\varepsilon(X_N(t_0)),
\qquad \int\|\dot X_N\|_{L^2(\rho_0)}^2\le\mathcal F_\varepsilon(X_N(t_0)).
\]

If the initial discrete energy is bounded, the proximal reconstructions are bounded in Lᵐ, the particle measures are equicontinuous in W₂ on a bounded domain, and the proximal-particle W₂ distance is O(√ε). This suggests weak compactness without a regular reference solution.

The missing step is identification of the nonlinear diffusion flux. Even in the continuous-time version, at a configuration X and its proximal map Y, a smooth interior-supported test φ gives the exact formal consistency identity

\[
{d\over dt}\int\phi\,d\mu_N
 =\int r^m\Delta\phi
 -{1\over\varepsilon}\int (X-Y)^T
 \left[\int_0^1D^2\phi(Y+s(X-Y))\,ds\right](X-Y)\,d\rho_0.
\tag{1.1}
\]

Indeed the particle velocity is (Π_NY−X)/ε, and the proximal variation with v=∇φ replaces (Y−X)·∇φ(Y)/ε by ∫rᵐΔφ. The remaining difference is exactly the Taylor remainder shown. For the frozen scheme an additional time-freezing defect appears; it does not fix the spatial obstruction below.

Energy boundedness controls the second term only by a constant times ||X−Y||²/ε=O(1), rather than o(1). The following example shows this is a real obstruction, not just a loose estimate.

## 2. Exact stationary construction in every dimension and exponent

Let d≥1, m>1, Ω=(−1,2)ᵈ, and take

\[
\rho_0=\mathbf1_{(0,1)^d}.
\]

This has mass one and finite internal energy. Divide (0,1)ᵈ into nᵈ cubes of side h=1/n, let x_i be their centers, and use their barycentric initialization. Every particle has mass w=hᵈ and

\[
\delta_N^2={d h^2\over12}.
\tag{2.1}
\]

Fix 0<a<1/2 and set

\[
I=\int_{|z|<a}(a^2-|z|^2)^{1/(m-1)}\,dz,
\qquad c={m-1\over2m}I^{m-1}>0,
\qquad\varepsilon=c h^2.
\tag{2.2}
\]

Define a unit-mass scaled bump

\[
f(z)=\left({m-1\over2mc}(a^2-|z|^2)_+\right)^{1/(m-1)},
\quad \int f=1,
\]

and candidate proximal subdensities

\[
r_i(y)=f((y-x_i)/h),\qquad r=\sum_i r_i.
\tag{2.3}
\]

Each r_i has mass hᵈ and is supported on B_{ah}(x_i). These balls are pairwise disjoint and are wholly contained in their initial cubes. Put

\[
\ell={a^2\over2c},\qquad c_i(y)={|x_i-y|^2\over2\varepsilon},
\qquad U(s)={s^m\over m-1}.
\]

The pointwise optimality inequalities are

\[
c_i(y)+U'(r(y))\ge\ell\quad\text{for every }i\text{ and a.e. }y\in\Omega,
\tag{2.4}
\]

with equality on the support of r_i. To verify this:

- On B_{ah}(x_i), the definition gives U'(r_i)=ℓ−c_i.
- On B_{ah}(x_j), j≠i, x_j is strictly closer than x_i, because |x_i−x_j|≥h and |y−x_j|<ah<h/2. Hence c_i+U'(r)=ℓ+c_i−c_j>ℓ.
- Outside all balls r=0 and |y−x_i|≥ah, hence c_i≥ℓ.

For any competing nonnegative subdensities s_i with the same individual masses, convexity gives

\[
\sum_i\int c_i(s_i-r_i)+\int[U(\sum_i s_i)-U(r)]
\ge\sum_i\int(c_i+U'(r))(s_i-r_i)\ge0.
\tag{2.5}
\]

Thus (2.3) is a global minimizer of the exact semidiscrete proximal problem, not just a critical point. Strict convexity makes its total density unique. The strict inequalities in the other balls ensure that a minimizing subdensity for particle i is its own bump r_i up to null sets. Consequently **every** minimizing transport allocation has barycenter x_i, by radial symmetry.

It follows that Π_NY=X_N at this configuration. The original frozen ODE is exactly

\[
\dot X_N=0.
\tag{2.6}
\]

After every step the same configuration and proximal problem recur. The particle measure is therefore stationary for all time and for every time mesh. This is not caused by a time-integration error or by a malicious choice among nonunique proximal maps.

## 3. The stationary limit is not a porous-medium solution

The empirical initial measures converge in W₂ to ρ0 dx by the cell coupling, with error squared δ_N²→0. Since every particle stays fixed, the entire particle curve converges to the time-independent measure ρ0 dx.

Choose φ∈C_c^∞(Ω) equal to x_1²/2 on a neighborhood of [0,1]ᵈ. Then

\[
\int_\Omega\rho_0^m\Delta\phi\,dx=\int_{(0,1)^d}1\,dx=1.
\]

The time-independent density has zero distributional time derivative, and so cannot solve ∂_tρ=Δρᵐ even with tests supported strictly inside Ω. Thus there is genuine nonconvergence to porous-medium evolution.

Nevertheless all the basic compactness bounds hold. A change of variables in each bump gives

\[
\mathcal F_\varepsilon(X_N)
 ={1\over2c}\int|z|^2f(z)\,dz+{1\over m-1}\int f(z)^m\,dz,
\tag{3.1}
\]

independent of n. The proximal-particle W₂ distance is O(h)=O(√ε), the particle dissipation is zero, and the scaled covariance term in (1.1) is positive and independent of n. With a quadratic test, that covariance term cancels the reconstructed diffusion term exactly, consistently with stationarity.

Finally

\[
{\delta_N^2\over\varepsilon}={d\over12c}>0.
\tag{3.2}
\]

The example fails δ_N²/ε→0. It shows that merely letting N→∞ and ε→0, while keeping initial discrete energy bounded, is insufficient. It does not establish failure when the quantization error is smaller than √ε.

## 4. Consequence for the broad unresolved target

A compactness proof for arbitrary irregular data must supply an additional argument that removes the covariance defect and identifies r_nᵐ. Energy dissipation alone does neither. Potential routes include a genuine smallness estimate for the within-particle covariance under δ_N²/ε→0, a slope lower-bound argument compatible with the particle projection, or a reference-pressure approximation with constants controlled uniformly near singular interfaces. None is proved by this approach.

A 2025 primary conference abstract by Quentin Mérigot independently identifies spurious stationary points as an obstacle for these Moreau–Yosida particle systems: [EYAWKADANAJKOS, April 2025](https://indico.math.cnrs.fr/event/13361/timetable/?view=standard). That abstract is contextual corroboration only. The explicit minimizer, scaling, stationarity, and non-PDE limit above are derived here and do not depend on an unverified theorem from that abstract.
