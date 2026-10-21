# Independent audit: two-target cumulative-mass reduction

## Outcome

For the proposed one-dimensional, two-target, midpoint discretization, the cumulative-mass scheme gives a rigorous route around the boundary entropy issue. For fixed finite positive eta, it yields convergence of the entire sequence of cumulative trajectories, hence weak convergence of transport plans, and finite-time sorting of the limiting trajectory. A conservative rigorous sorting time is

T = 1/kappa,   kappa = tanh((b-a)/(2 eta)).

This is a restricted theorem, not a theorem for the paper's general multi-target setting. The comparison principle for scalar first-order viscosity Hamilton–Jacobi equations is used below; a publication should cite a standard primary reference or append its doubling-of-variables proof. No assertion of strong convergence of the oscillatory basic-cell fractions is needed or made.

## Exact discrete scheme

Let h=1/n, u_i^k in [0,1] be the fraction of cell i sent to b, and let

V_i^k = h sum_{j=1}^i u_j^k,   V_0^k=0,   V_n^k=m_n.

At a half-sweep, alternate the active interior indices i. The pair (i,i+1) is updated while singleton endpoints are unchanged. With

f(p) = [r-sqrt(r^2-4p(1-p))]/2,   r=coth((b-a)/eta),

the active cumulative node obeys exactly

V_i^k = (V_{i-1}^{k-1}+V_{i+1}^{k-1})/2
        - h f((V_{i+1}^{k-1}-V_{i-1}^{k-1})/(2h)).

Inactive cumulative nodes remain unchanged. Endpoint cumulative values remain fixed, including during singleton updates. Thus the boundary condition is exactly Dirichlet for the primitive, not a guessed numerical boundary flux.

The formula assumes the pair optimizer and entropy normalization in the stated two-target setting. In particular one half-sweep has physical duration h. If another convention counts a full two-partition sweep as one iteration, all stated times must be converted accordingly.

## Convergence of primitives, including the boundary

Assume m_n tends to m and initial primitives converge uniformly to V_0. Weak convergence of initial cell measures implies this uniform primitive convergence here, since all primitive slopes lie in [0,1].

1. At every step 0 <= V_i-V_{i-1} <= h. Therefore the spatial piecewise-linear primitive is nondecreasing and 1-Lipschitz.
2. An updated primitive lies in the same interval
   [max(V_{i-1},V_{i+1}-h), min(V_{i-1}+h,V_{i+1})]
   as its old value. This interval has length at most h. Hence the time-linear interpolation has time Lipschitz constant at most 1.
3. Arzela–Ascoli on each finite time slab gives subsequential uniform convergence to a continuous primitive V, with the exact traces V(t,0)=0, V(t,1)=m, and V(0,x)=V_0(x). No boundary-layer assumption is required.
4. Restrict to the staggered lattice of active nodes. Except for its first level, both neighbors used in the update are active nodes of the immediately preceding level. The numerical update is monotone: its two partial derivatives are (1+f')/2 and (1-f')/2, nonnegative since |f'|<=1. It is invariant under adding a constant.
5. At a strict local maximum of V-phi, choose maximizing active lattice nodes. Monotonicity and constant invariance give
   phi(t,x) <= [phi(t-h,x-h)+phi(t-h,x+h)]/2
               -h f([phi(t-h,x+h)-phi(t-h,x-h)]/(2h)).
   Divide by h and pass to the limit to obtain phi_t+f(phi_x)<=0. At minima the inequality reverses. Thus V is an interior viscosity solution of V_t+f(V_x)=0.
6. Extend f outside [0,1] by its endpoint tangent lines, or any globally Lipschitz continuation. The standard viscosity comparison principle with continuous, pointwise Dirichlet boundary and initial data gives uniqueness. It applies to this strong boundary solution: a positive difference between sub- and supersolutions is excluded on the parabolic boundary, so the doubling-of-variables contradiction occurs in the interior. Consequently every convergent subsequence has the same limit, and the full sequence converges uniformly.

The Lipschitz slope restriction ensures any spatial derivative of a touching smooth test function is in [0,1]. Consequently the arbitrary continuation of f outside that interval does not change the result.

The primitive determines q=partial_x V distributionally. Uniform primitive convergence yields weak convergence of q_n dx, uniformly against a fixed smooth spatial test function on compact time intervals. The midpoint atomic target-b measures and their piecewise-constant reconstructions differ against a Lipschitz test by O(h); thus this also proves weak convergence of the actual transport plans. Basic-cell fractions may retain microscopic oscillations, so uniform primitive convergence alone must not be advertised as strong L1 convergence of those fractions.

## Finite-time sorting for positive eta

Write V_*(x)=max(0,m+x-1). Feasibility always gives V>=V_*, since V>=0 and the mass remaining to the right of x is at most 1-x.

The concavity of f and f(0)=f(1)=0 imply

f(p) >= g(p) := kappa min(p,1-p),   0<=p<=1,
kappa=2f(1/2)=r-sqrt(r^2-1)=tanh((b-a)/(2eta))>0.

Hence V is a viscosity subsolution of V_t+g(V_x)=0. Let W be the solution with the same initial and boundary data for g. Comparison gives V<=W.

Here W can be constructed explicitly. Extend V_0 to the whole real line by V_0(y)=0 for y<0 and V_0(y)=m+y-1 for y>1. Then the concave piecewise-linear Hamiltonian formula is

W(t,x) = sup_{|y-x|<=kappa t}
         { V_0(y) - (kappa t+y-x)/2 }.

This formula follows directly from the max-plus semigroup: the admissible displacement interval adds under composition and the cost is linear in time and displacement. Its small-time generator is -g(p). It therefore gives the viscosity solution, including at nonsmooth points by the standard monotone-semigroup test-function argument.

The extension is nondecreasing and 1-Lipschitz. At x=0, every candidate has value <=0 because V_0(y)<=max(y,0), while y=-kappa t gives 0. Thus W(t,0)=0. At x=1, every candidate has value <=m because V_0(y)<=m for y<=1 and equals m+y-1 for y>=1, and y>=1-kappa*t makes the subtracted cost nonnegative for interior y; while y=1+kappa t gives m. Thus W(t,1)=m. Therefore the full-line formula genuinely supplies the required interval Dirichlet solution.

For kappa t>=1 and x in [0,1], the interval of maximization reaches both exterior regions. Its left exterior maximum is 0, and its right exterior maximum is m+x-1. For interior y, use V_0(y)<=min(y,m), giving

V_0(y)-(kappa t+y-x)/2 <= (m+x-kappa t)/2
                                      <= max(0,m+x-1),

where the last inequality follows by separating m+x<=1 and m+x>=1. Thus W(t,x)=V_*(x) for every t>=1/kappa. The sandwich V_*<=V<=W proves the same equality for V.

Its derivative is q_*(x)=1_{x>1-m}, up to a null set. For squared cost and a<b this is the unique optimal two-target coupling, because the cost difference c(x,b)-c(x,a)=b^2-a^2-2(b-a)x is strictly decreasing. Thus the limiting trajectory reaches the global optimum by T.

Important distinction: positive-eta finite-n iterates need not become exactly sorted, and their entropic equilibrium is not exactly the unregularized optimal coupling. The theorem concerns the n-to-infinity trajectory, with epsilon_n=eta/n, and then its finite macroscopic sorting time.

## Independently verified zero-eta finite-n bound

For eta=0, the actual unregularized pair update is

(u,v) -> (max(0,u+v-1), min(1,u+v)).

Use unnormalized cumulative masses U_i=sum_{j<=i}u_j, total M. An active node becomes max(U_{i-1},U_{i+1}-1). The feasible minimal primitive is U_i*=max(0,M-n+i), which is fixed by each update and is a lower bound for every feasible state.

Expand an active node at step k backwards through the alternating stencil until reaching the initial level or a fixed endpoint. An initial-origin path ending at j has k steps and R=(k+j-i)/2 right steps; its contribution is U_j^0-R. Since U_j^0<=min(j,M), this is at most (M+i-k)/2. A path reaching the left endpoint contributes -R<=0. A path reaching the right endpoint has R>=n-i and contributes M-R<=M-n+i. Thus every boundary-origin term is <=U_i*.

For an interior node, M+i<=2n-1. Therefore an active node is exactly sorted whenever k>=2n-1. After step 2n, nodes of both parities have met this criterion. This proves exact sorting after at most 2n half-sweeps for either starting parity, including odd n and singleton endpoints. For n=1 the state is already optimal.

A local numerical sanity check tested 2,970 random trajectories with n=2,...,100 and verified equality to the sorted vector after 2n steps to 1e-10. This is only a check, not a substitute for the path proof.

The stronger continuum bound above specializes to T=1 when eta=0. The finite-n bound 2n is deliberately conservative and sufficient; no optimality of that discrete bound is claimed.

## Scope and cautions

- Do not call the zero-eta result novel without checking the known odd-even-sorting interpretation cited in the earlier entropic domain-decomposition paper.
- For positive eta, extending the DISCRETE cell fractions by 0 left and 1 right does not reproduce singleton boundary updates. It leaks mass across a boundary-straddling pair. The argument above does not use that false equivalence.
- For eta=0 only, the extension does reproduce singleton updates exactly.
- The proof uses the exact two-target midpoint pair formula. General measures, more targets, nonuniform partitions, or higher dimensions are not covered.
- The result does not identify a unique solution of the paper's unrestricted weak continuity-equation system. It identifies the unique viscosity primitive selected by this particular numerical scheme.

## Editorial audit reconciliation

The right-boundary max-plus explanation above explicitly includes its displacement constraint, as required by POSITIVE_ETA_AUDIT.md. The publication proof instead uses the independently checked three-plane barrier. The conservative 2n bound in this earlier audit is superseded by the complete n-update proof in ZERO_ENTROPY_AUDIT.md.
