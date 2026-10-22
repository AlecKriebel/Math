# Approach 4: a reflecting-wall free-boundary theorem

**Problem:** 30004633. **Author continuation:** approach 4. **Status:** candidate conditional theorem, awaiting independent review. This approach treats a compact physical domain where the exact density really reaches the wall. It uses an admissible tangential flow variation, rather than assuming reconstructed pressure vanishes on that wall.

## 1. Reflecting Barenblatt geometry

Fix d≥1, m>1, 0<t0<T, an integer 1≤k≤d, and L>0. Let

\[
\Omega=(-L,L)^{d-k}\times(0,L)^k.
\tag{1.1}
\]

Set β=(d(m−1)+2)^{-1} and λ=dβ(m−1). Choose A>0 so that the restriction to the orthant of

\[
\rho(t,x)=\left[{m-1\over m}\left(A t^{-\lambda}-{\beta\over2t}|x|^2\right)_+\right]^{1/(m-1)}
\tag{1.2}
\]

has total mass one. The corresponding full-space profile has mass 2ᵏ. Assume its support radius R(T)<L.

The density is positive up to each reflecting face x_j=0 within its ball. Its free boundary is the spherical part |x|=R(t), meeting the reflecting faces orthogonally. On those faces the physical pressure has zero normal derivative, because its gradient is radial and its jth component is −βx_j/t. On all the other faces the solution vanishes in a neighborhood. Consequently (1.2), restricted to Ω, is a unit-mass no-flux porous-medium solution.

Its exact flow on the mass-carrying labels is X(t,a)=(t/t0)^β a. The force has a nonzero interior trace on the spherical moving free boundary. Unlike Approach 2, the support has **zero clearance from the physical wall**.

This example describes permanent orthogonal reflecting contact. It does not describe a freely expanding off-center ball striking a wall for the first time; that generic collision is not settled here.

## 2. Tangential-flow proximal variation

The original constrained energy and frozen particle scheme are exactly as in Approach 2. A proximal minimizer Y_n is constrained only through (Y_n)#ρ0 being supported in closure(Ω).

Let v be a smooth globally Lipschitz vector field whose flow Φ_s preserves Ω for small positive and negative s. The curve Φ_s∘Y_n is then an admissible variation. Differentiating the quadratic cost and the internal energy at s=0 gives

\[
{1\over\varepsilon}\langle Y_n-X_N(t_n),v(Y_n)\rangle
 =\int_\Omega r_n^m\operatorname{div}v\,dx.
\tag{2.1}
\]

The proof is the same change-of-variables computation as for an interior-supported variation. No integration-by-parts boundary trace of r_n is required. In particular (2.1) remains valid when reconstructed pressure on a reflecting face is nonzero.

For the box (1.1), a sufficient concrete condition is that v be tangent to each coordinate-zero face and vanish near every other face, with each coordinate-zero hyperplane invariant under its full-space ODE. This is satisfied by every smooth radial vector field v(x)=f(|x|²)x which vanishes for |x|≥R2<L: coordinates obey x_j'=f(|x|²)x_j, so their signs are preserved, and the remaining physical faces are fixed in an open neighborhood. Existence and uniqueness of the full-space ODE, applied in both time directions, gives Φ_s(Ω)=Ω.

## 3. A signed cutoff respecting the reflecting walls

Choose R(T)<R1<R2<L and a radial χ∈C_c^∞(B_{R2}), equal to one on B_{R1}. Set

\[
q_0(t,x)=A t^{-\lambda}-{\beta\over2t}|x|^2,
\qquad q=\chi q_0-(1-\chi)\kappa,
\qquad u=-\nabla q
\tag{3.1}
\]

for a fixed κ>0. These are smooth full-space functions. The field u is radial, hence of the form f(t,|x|²)x, and vanishes for |x|≥R2. Therefore u(t,·) is an admissible field for (2.1) at every fixed t.

As in Approach 2, the residual

\[
\mathcal R=q_t-|u|^2+(m-1)q\operatorname{div}u
\]

vanishes where |x|≤R1 and where |x|≥R2. The annulus between them is strict vacuum with q bounded above by a uniform negative number. Thus

\[
|\mathcal R|\le C_R(-q)\mathbf1_{\{q<0\}}
\tag{3.2}
\]

holds throughout Ω and, in fact, throughout Rᵈ. This construction does not force u to vanish at the reflecting wall, but it does force its normal component to vanish there.

Put P(t)=∫Ωρᵐ. Scaling in the orthant gives P(t)∝t^{-λ}, so

\[
P'=\int_\Omega\rho q_t=-(m-1)\int_\Omega\rho^m\operatorname{div}u.
\tag{3.3}
\]

The restriction changes only the normalization and the value of the integral, not these identities.

## 4. Quantitative original-scheme theorem

Partition the initial support into positive-mass measurable cells, initialize X_N(t0)=Π_NId, and define δ_N²=||Π_NId−Id||²_{L²(ρ0)}. For any choice of exact proximal minimizers and the exact frozen integration, and 0<ε≤1, τ≤ε,

\[
\sup_{t_0\le t\le T}\|X_N(t)-X(t)\|_{L^2(\rho_0)}^2
 +\int_{t_0}^T\|\dot X_N(t)-\dot X(t)\|_{L^2(\rho_0)}^2dt
 \le C\left({\delta_N^2\over\varepsilon}+\varepsilon+{\tau\over\varepsilon}\right).
\tag{4.1}
\]

The reconstructed densities converge in W₂, uniformly for the piecewise-frozen time interpolation, under the same vanishing scale conditions. Constants depend on d,m,k,t0,T,A,L and the outer-face clearance R2<L.

### Proof

Define e=U(r)−qr+ρᵐ, the frozen modulated energy Z, and the nonnegative shift W exactly as in Approach 2. Nonnegativity and the vacuum control e≥(−q)r require no boundary assumption. In the differential calculation, use the tangential-flow identity (2.1) with v=u(t,·), in place of the compactly supported variation in Approach 2. Equations (3.2)–(3.3) yield the identical cancellation

\[
-\int_\Omega r_n^m\operatorname{div}u
 +\int_\Omega r_n(|u|^2-q_t)+P'
 =-(m-1)\int_\Omega e\operatorname{div}u-\int_\Omega r_n\mathcal R.
\]

The spatial commutator, frozen-step defect, exact frozen-energy dissipation, and downward energy resets are unchanged. Consequently the same shifted-energy differential inequality and initialization bound hold. Grönwall and the Lipschitz flow comparison give (4.1).

Every physical-boundary issue in this argument is accounted for by an admissible two-sided flow on the constrained domain. In particular there is no assumption that the proximal density has zero boundary pressure, and no accidental use of a whole-space proximal problem.

## 5. Remaining wall-contact gap

Reflection works because the solution and pressure extension have the exact symmetry needed for a tangential auxiliary velocity. A Barenblatt profile centered away from a wall generally ceases to solve the reflecting-boundary PDE once its free boundary reaches the wall. The theorem above therefore cannot be obtained by just continuing that profile after its first impact. General wall-contact evolution requires a different exact reference pressure and compatible extension estimates near the contact set. No such general extension is proved here.
