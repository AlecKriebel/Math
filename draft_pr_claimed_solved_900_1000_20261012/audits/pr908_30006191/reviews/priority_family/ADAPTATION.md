# Checkable cutoff adaptation of the earlier phase argument

This is an independent audit deduction, not a theorem stated in the source. The source is Oliver Siebert, *Discontinuity of Continuum Fermion Dynamics*, [arXiv:2609.34402v1](https://arxiv.org/pdf/2609.34402v1), submitted 28 September 2026. Relevant proof locations are Lemmas 3.1-3.4, pp. 8-15, and Section 3.3, pp. 15-16. The manuscript under audit is dated 7 October 2026.

## Exact Hamiltonian binding

Put `q=1_{B(0,4)}` and `L=dGamma(q)`. The candidate's fixed smooth potential equals one on every difference of two points of `B(0,4)`. Thus its effective two-variable kernel is exactly

\[
K(x,y)=q(x)q(y).
\]

For either `sigma=0` or `sigma=1`, write the candidate as

\[
H^{(\sigma)}_n=\sum_{j=1}^n h_{\sigma,j}
  +\sum_{i\ne j}K(x_i,x_j),\qquad
h_\sigma=-\Delta+(1-\sigma)q.
\]

Indeed, the off-diagonal sum is `L_n(L_n-1)` and the added one-body term is `(1-sigma)L_n`. This gives precisely `T_n+L_n(L_n-sigma)`. The kinetic energy continues to act on all of `R^3`; this is not a hard-wall or finite-mode model.

No difference potential `W(x-y)` on all space represents `K`: simultaneous translation preserves `x-y` but can move both particles from inside to outside the cutoff. Nor can a fixed one-body potential absorb the entire quadratic difference between `N(N-1)` and `L(L-1)` in all particle sectors. Consequently the stated Theorem 2.4 and Proposition 2.6 are not literal applications to this Hamiltonian.

## Hypothesis and geometry checks

For `-Delta`, the dispersion hypothesis holds in dimension three with `nu=2`; the smooth-cutoff commutator is first order and bounded by the `H^1` norm. The kernel is symmetric, real, bounded, and nonnegative. It has the stronger uniform multiplier estimate

\[
\sup_y\|K(\cdot,y)v\|_2\leq\|v\|_2.
\]

For the normal-ordered case the external potential is zero. For the ordered case it is `q`. The latter is bounded and nonnegative, so `D(h_0)=H^2` with equivalent graph norm. Define

\[
\Omega= B(0,4)\ \cup\ \{x:|x|>4\}.
\]

If `u` is smooth and compactly supported in `Omega`, multiplication by `q` is locally constant near its support. Hence `u` and `h_0 u` are in `H^2`, so `u` lies in `D(h_0^2)`. Functional calculus gives

\[
\|(e^{-ith_0}-1)u\|_{H^2}
\leq C\|(e^{-ith_0}-1)u\|_{D(h_0)}
\leq C|t|(\|h_0u\|+\|h_0^2u\|).
\]

This verifies the local propagation condition with `m=2>3/2`. It does not require differentiating the indicator at its boundary.

An explicit admissible geometry is a cluster ball `B=B(2e_1,1/4)`, a test ball `A_1=B(0,1/2)`, and an exterior test ball `A_2=B(6e_1,1/4)`. Their closures are pairwise disjoint. Let `B_0=B(2e_1,1/8)`; choose fixed normalized `f_j` smooth and compactly supported in `A_j`. Then

\[
K(x,y)=c_j\quad(x\in A_j,y\in B),\qquad c_1=1,\ c_2=0.
\]

Both test supports stay a positive distance from the cutoff boundary. These are fixed sets; no translation, volume, or potential changes with particle number.

## Every mechanism survives the kernel substitution

1. **Packing.** Subdivide a fixed cube compactly contained in `B_0` and place normalized rescaled smooth orbitals in `n` disjoint subcubes. Their Slater has kinetic energy `O(n^{5/3})`. The bounded kernel contributes at most `n(n-1)` and the external term at most `n`, giving initial total energy `O(n^2)`. This replaces the interaction-energy integral in Lemma 3.1 by an easier bound.

2. **Interacting leakage.** For a smooth localization function vanishing on the initial cluster and equal to one outside a slightly larger ball, both `sum K(x_i,x_j)` and the external potential commute with its local particle count. Only the kinetic commutator enters the derivative. Since `H_n>=T_n`, conservation of the initial `O(n^2)` energy bounds kinetic energy uniformly by `Cn^2`. The differential estimate therefore yields

   \[
   \langle N_{B^c}\rangle_{n,s}\leq Cn^2s^2.
   \]

   Translation invariance is unnecessary: multiplication, the lower bound, and the initial energy suffice. This is the Lemma 3.2 route with no singular-potential truncation.

3. **Antisymmetrization.** The map `J_n=sqrt(n+1)P^-_{n+1}` obeys the local bound `||J_n eta||^2<= <eta,(1+N_A)eta>` when the distinguished coordinate lies in `A`. This is an algebraic particle-count decomposition and is unchanged by the Hamiltonian.

4. **Cross phase.** On a distinguished particle plus the cluster, the added interaction is `2 sum_j K(x,y_j)`. Permutation symmetry gives the same intertwining with `H_{n+1}`. Duhamel comparison with the scalar `2nc_j` uses only: exact constancy on `A_j x B`, the uniform multiplier bound above, leakage, and local propagation of `f_j`. Localized terms have integrand `O(n^2|s|)`; the unlocalized distinguished-particle term has integrand `O(n^{3/2}|s|)`. Thus, for `0<=t<=1/n`,

   \[
   \|e^{-itH_{n+1}}a^*(f_j)\Psi_n
     -e^{-2inc_jt}a^*(e^{-ith_\sigma}f_j)e^{-itH_n}\Psi_n\|
      \leq Cn^2t^2.
   \]

   The source's singular multiplier estimate is replaced by a bounded-kernel estimate. Sharp boundaries of `K` do not enter a derivative. This completes the only modification needed to the phase lemma.

5. **Detection.** For the fixed gauge-invariant observable `A=a^*(f_1)a(f_2)`, evaluate the orbit between `a^*(f_1)Psi_n` and `a^*(f_2)Psi_n`. Both initial vectors are normalized. The preceding comparisons, the CAR, and leakage into the test supports give

   \[
   \|\tau_t(A)-A\|\geq |e^{2int}-1|-C(n^2t^2+|t|).
   \]

   With `t_n=theta/n` and a sufficiently small fixed positive `theta<=1`,

   \[
   \liminf_n\|\tau_{t_n}(A)-A\|
      \geq 2|\sin\theta|-C\theta^2>0.
   \]

   The source's polarization argument then supplies a fixed creation observable and, by adjoint, a fixed annihilation observable with positive liminf along a subsequence. That is enough for the existential pointwise-norm question. A varying vector state applied to `D^*D` converts this into a positive state witness. No fixed normal state is shown discontinuous.

## What this adaptation establishes, and its exact quantitative gap

This proves existential discontinuity for the candidate's actual cutoff Hamiltonian, for both ordering conventions, by a direct adaptation of the pre-candidate argument. It uses the source's high-density cluster, phase, and localized antisymmetrization mechanisms; the only structural generalization is from `W(x-y)` to a bounded symmetric `K(x,y)`.

It does not itself give the candidate's prescribed single orbital, exact times `pi/(2N+1-sigma)`, maximal limit `2`, or state limit `4`. Its `Cn^2t^2` error stays of order `theta^2` at `t=theta/n`, so setting the phase exactly to `-1` does not prove the error vanishes. The candidate closes that quantitative gap using free-Slater number variance and the sharper comparison `O(N^{-1/6}+N^{-1/3})`. Maximal limit `2` for the full-space constant-number reference was already stated in Proposition 2.6; the meaningful extra estimate transfers it to the spatial cutoff.

The audit therefore distinguishes **no literal prior cutoff theorem found in the inspected source** from **an earlier proof that directly yields the existential cutoff conclusion**. The latter prevents treating the cutoff qualifier alone as priority clearance. The novelty of the precise maximal-norm localization sharpening is not certified by this audit.
