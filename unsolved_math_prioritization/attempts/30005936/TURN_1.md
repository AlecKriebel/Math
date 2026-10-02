# Turn 1: remove differentiability while retaining global Lipschitz control

Substantive author turn **1/5**. This is a scoped extension for the exact space-time-white-noise LT scheme. It does not cover the source's superlinear example g(v)=v_+^(5/4), whose Lipschitz constant is unbounded.

Let u0∈C³([0,1]) be nonnegative with u0(0)=u0(1)=0. Let g:R→R be globally Lipschitz with constant L and g(0)=0, **without any differentiability assumption**. Let u be the Itô mild solution of

 du=∂xx u dt+g(u) dW

with Dirichlet boundary and space-time white noise. Put h=1/N, τ=T/M, A_N=N²D_N, and P_τ=exp(τA_N). On the same Brownian sheet use the independent Brownian increments specified in SOURCE_SCOPE. Define f(v)=g(v)/v for v≠0 and f(0)=0, and

 U_{m+1}=P_τ [U_{m,n} exp(sqrt(N)f(U_{m,n})ΔW_{m,n}
                                      −N f(U_{m,n})²τ/2)]_n.        (1)

Then the numerical and exact solutions are nonnegative. The following bounds from the cited smooth-coefficient theorem extend to this g, with constants depending on L,T,γ,u0 but not M,N:

- Under τ<=γh, max_{m,n} ||U_{m,n}−u_n^N(t_m)||_{L²} <= C sqrt(τ/h).
- Under τ<=γh², that temporal error is <=C τ^(1/4).
- Under τ<=γh², max_{m,n} ||U_{m,n}−u(t_m,x_n)||_{L²} <=C h^(1/2).

Here u^N is the spatially semidiscrete solution. The last bound becomes Cτ^(1/4) only under an additional lower comparison τ>=c h², with c>0. We do not inherit the OWR summary's continuum τ-only display under a one-sided mesh condition.

## 1. Coefficient approximation with uniform constants

For ε>0 set

 g_ε(x)=(1/(2ε))∫_{−ε}^{ε}g(x+y)dy
              −(1/(2ε))∫_{−ε}^{ε}g(y)dy.                         (2)

Then g_ε(0)=0, g_ε is C¹, and

 g_ε'(x)=[g(x+ε)−g(x−ε)]/(2ε),
 Lip(g_ε)<=L,       sup_x|g_ε(x)−g(x)|<=Lε.                        (3)

The derivative is continuous because g is continuous. The error bound follows by integrating L|y| at x and at 0. Thus the published Assumption3 holds for every g_ε with the **same** Lipschitz constant L. Define f_ε(v)=g_ε(v)/v off zero and f_ε(0)=g_ε'(0). Then |f_ε|<=L.

The published paper explicitly says its moment/error constants depend on g through L. We also checked its Proposition5, Lemma8, and Theorem6 proof: the coefficient estimates use only |f|<=L, g(v)=vf(v), and the global Lipschitz inequality for g. No modulus of continuity or higher derivative norm of g_ε enters these constants. The derivative at zero is used to define a continuous f in the original presentation, not to generate an ε-dependent estimate.

## 2. The numerical map remains continuous after multiplication by the old state

For fixed real z write

 H_ε(x,z)=x exp(sqrt(N)f_ε(x)z−Nτ f_ε(x)²/2),
 H(x,z)=x exp(sqrt(N)f(x)z−Nτ f(x)²/2).

If x_ε→x≠0, uniform convergence of g_ε and its common Lipschitz bound give f_ε(x_ε)→g(x)/x, so H_ε(x_ε,z)→H(x,z). If x=0, then

 |H_ε(x_ε,z)| <= |x_ε| exp(sqrt(N)L|z|) ->0.                      (4)

Thus the potentially discontinuous f at zero causes no discontinuity of the actual old-state-multiplied update. The same reasoning proves continuity of H itself. Setting any other finite f(0) leaves the update unchanged at zero, but f(0)=0 keeps the convenient global bound.

For every fixed N,M and almost every realization of its finitely many Brownian increments, induction in (1) yields U_m^ε→U_m at every node and step. Moreover P_τ is nonnegative and has row sums at most1. Hence, simultaneously for all ε,

 max_n |U_m^ε(n)|
  <=||u0||_infinity exp(sqrt(N)L Σ_{j<m} max_n|ΔW_{j,n}|).          (5)

The right side has every finite moment for fixed N,M. Dominated convergence therefore gives convergence in every finite L^p for each fixed discretization. This dominating random variable is **not asserted to be uniform** in N,M; uniform discretization constants are transferred from the published theorem only after taking the coefficient limit at fixed N,M.

## 3. Exact-solution stability in the coefficient

The usual globally Lipschitz Walsh/Picard construction applies to g without differentiability. Its L² contraction and moment estimates use the Dirichlet heat-kernel bound

 sup_x∫_0^1 G(t,x,y)²dy <= C_T t^(−1/2),       0<t<=T.             (6)

For completeness, exponential weighting of the supremum-in-x second-moment norm makes the Picard difference norm a contraction once the weight parameter is sufficiently large: the kernel integral ∫_0^∞ e^(−βr)r^(−1/2)dr is proportional to β^(−1/2). This gives existence and uniqueness. Standard higher-moment heat-kernel increment estimates give its continuous version. The same construction is the one underlying the primary paper's mild solution.

Couple u^ε and u using the same white noise. Let D_ε(t)=sup_x E|u^ε(t,x)−u(t,x)|². Itô's isometry, (3), and (6) give

 D_ε(t) <= C L²ε² + C L²∫_0^t(t−s)^(−1/2)D_ε(s)ds.              (7)

The constant in the first term includes the finite T^(1/2) factor. The weakly singular Gronwall inequality, or iteration of this convolution followed by its convergent Mittag-Leffler series, yields sup_{t<=T}D_ε(t)<=C_{L,T}ε². Similarly the finite-dimensional globally Lipschitz SDE stability estimate gives u^{N,ε}→u^N in L² at all grid times for each fixed N; its preliminary stability constant is allowed to depend on N.

## 4. Pass the published estimates through the limit

For each ε, the precise estimates of Bréhier–Cohen–Ulander Theorem6 and Corollary7 apply with constants common to all ε by §1. For fixed M,N, §2 and §3 give convergence of both terms of each error in L². Passing to the limit proves the three displayed estimates, with the same mesh-independent constants. The second-moment bound of their Proposition5 transfers as well under τ<=γh.

This uses the published smooth result as a credited theorem and verifies the approximation bridge. It is not a new derivation of its discrete heat-kernel estimates. It also does not interchange an ε-limit with an unbounded family of meshes: the bound is proved at each fixed mesh with one common constant and hence holds for all admissible meshes.

## 5. Positivity and an explicit weak-test consequence

The matrix A_N is the generator of a killed nearest-neighbor walk: writing B for the adjacency matrix of the interior path,

 P_τ=e^(−2N²τ) Σ_{j>=0}(N²τ)^j B^j/j!.

It has nonnegative entries and row sums at most1. Every stochastic exponential in (1) is strictly positive and finite. Nonnegative U0 therefore stays nonnegative for every finite M,N, with no CFL restriction. This purely algebraic fact also holds for any everywhere-finite Borel g with g(0)=0 and a finite zero convention, whenever that finite recursion is used; it says nothing by itself about exact-solution well-posedness or moments.

For the exact globally Lipschitz solution, each u^ε is nonnegative by the credited smooth theorem. L² convergence at a countable dense set, a subsequence argument, and the continuous version of u imply nonnegativity at all space-time points almost surely.

If φ:R→R is globally Lipschitz, its expectations are finite by the second-moment bounds, and

 |Eφ(U_{m,n})−Eφ(u(t_m,x_n))|
   <=Lip(φ)||U_{m,n}−u(t_m,x_n)||_{L²} <=C Lip(φ)h^(1/2)          (8)

under τ<=γh². Under balanced refinement this is a τ^(1/4) bound. An analogous temporal estimate holds against u^N. This is an explicit pointwise Lipschitz-test weak bound inherited from strong convergence, not a higher weak order for smooth tests or a theorem for arbitrary unbounded observables/path norms.

An example covered by this extension but excluded by the paper's C¹ hypothesis is g(v)=min(v,1), which has a kink at the positive level1. The power g(v)=v_+^(5/4) is not covered: no approximation of that coefficient with a common finite global Lipschitz constant is possible. The original broader rough/superlinear and weak-rate question remains unresolved1/5.
