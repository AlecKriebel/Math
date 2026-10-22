# A finite-positive-entropy-scale sufficient condition in one dimension

## Status and scope

This is an authored restricted theorem for the ORIGINAL alternating domain-decomposition algorithm. It concerns the continuum limit before long time. It is not a resolution of the general higher-dimensional OWR question, and no novelty priority is asserted. An independent derivation is in INDEPENDENT_FLUX_AUDIT.md; a further independent audit passed in POSITIVE_ETA_AUDIT.md. The zero-entropy sorting background is already discussed in Bonafini–Schmitzer (2021), Section 5.

## Theorem

Fix a<b, 0<m<1 and 0<eta<infinity. Let X=[0,1], mu=Lebesgue measure, nu=(1-m)delta_a+m delta_b, and c(x,y)=(x-y)^2. For each even n let h=1/n, x_i=(i-1/2)h and mu_n=h sum_i delta_{x_i}. Choose any feasible initial plan pi_n^0 in Pi(mu_n,nu), assuming pi_n^0 converges weakly to pi_0.

Run exact entropy-regularized local transport solves with epsilon_n=eta/n, alternately on pairs (1,2),(3,4),... and on singleton 1, pairs (2,3),(4,5),..., singleton n. One application of either partition is one iteration and has macroscopic duration h. Each local solve preserves the local Y marginal, exactly as in the source algorithm.

Then the actual transport-plan trajectories converge weakly, uniformly against each fixed continuous test function on compact time intervals, to a uniquely determined trajectory pi_t. The limit becomes exactly the globally optimal unregularized plan by the finite time

T = coth((b-a)/(2eta)).

For every t>=T,

pi_t(dx,dy)=1_{x<1-m} dx delta_a(dy)+1_{x>1-m} dx delta_b(dy).

The statement allows arbitrary feasible initializations subject only to weak convergence. It neither assumes the source paper's strong disintegration-convergence hypothesis nor asserts strong convergence of raw microscopic occupancies. It proves a weak-plan continuum trajectory directly. The unique limiting primitive selects the relevant solution, rather than selecting an arbitrary weak solution of the source paper's underdetermined continuity equation.

## 1. Exact pair optimizer

Write pi_n^k({x_i} x {b})=h u_i^k, with 0<=u_i^k<=1. An active pair has total upper-target fraction 2p=u_i+u_{i+1}. Its updated fractions have the form p-f,p+f. The four conditional entries, in left/right source rows and a/b target columns, are

left: 1-p+f, p-f;
right: 1-p-f, p+f.

For epsilon_n>0 and 0<p<1, entropic strict convexity yields an interior optimizer, subject to the feasible interval. The derivative of the cost when f increases is -2h^2(b-a), because the difference of the a/b cost differences at consecutive source points is -2h(b-a). The entropy derivative is h epsilon_n times

log[(p+f)(1-p+f)/((p-f)(1-p-f))].

Thus the ratio equals exp(2h(b-a)/epsilon_n)=exp(2(b-a)/eta). Factors from the reference mu_n tensor nu cancel, since its row and column marginals are fixed throughout this local optimization. Solving the quadratic gives

f(p) = (r-sqrt(r^2-4p(1-p)))/2,
r = coth((b-a)/eta).

The formula extends continuously with f(0)=f(1)=0. Differentiation gives

f'(p)=(1-2p)/sqrt(r^2-4p(1-p)),
f''(p)=-2(r^2-1)/(r^2-4p(1-p))^(3/2).

Therefore f is symmetric and concave, positive on (0,1), with |f'|<=1/r<1. In particular the pair output is monotone in p. This derivation also verifies the midpoint cell normalization: the rescaled source law in the paper is (delta_{-1/2}+delta_{1/2})/2, not atoms at +/-1.

## 2. Exact cumulative scheme and compactness

Define U_i^k=h sum_{j<=i}u_j^k. The endpoints are U_0^k=0 and U_n^k=m. At an active edge i the update is exactly

U_i^k = S_h(U_{i-1}^{k-1},U_{i+1}^{k-1}),
S_h(A,B)=(A+B)/2-h f((B-A)/(2h)).

All inactive cumulative nodes are unchanged. This is a checkerboard staggered scheme; both neighbors used at an active node were updated at the immediately preceding time level, except on the harmless first level. Endpoint values are fixed at all levels. There is no artificial boundary-straddling pair.

At every level, 0<=U_i-U_{i-1}<=h. Both the old and updated U_i lie in

[max(U_{i-1},U_{i+1}-h), min(U_{i-1}+h,U_{i+1})],

an interval of length at most h. Spatial piecewise-linear and time-linear interpolation is therefore 1-Lipschitz in space and time. It has a locally uniformly convergent subsequence, preserves the exact endpoint values, and has the prescribed initial primitive. Weak convergence of initial plans gives uniform convergence of initial primitives because they are equi-Lipschitz.

## 3. The algorithm selects a unique viscosity primitive

Extend f to the whole real line using its endpoint tangent lines. The extension is globally Lipschitz and |f'|<=1. Consequently S_h is globally monotone in each argument, with derivatives (1+f')/2 and (1-f')/2, and S_h(A+C,B+C)=S_h(A,B)+C.

On the staggered active lattice, the standard test-function argument is elementary. At a maximizing node for U^n-phi, monotonicity and constant invariance imply

phi(t,x)<=S_h(phi(t-h,x-h),phi(t-h,x+h)).

Taylor expansion gives phi_t+f(phi_x)<=0 in the limit. At minima the inequality is reversed. The active lattice is dense as h->0, and interpolation differs from its latest active-node values by O(h), so these tests apply to every interior contact of the limiting primitive. The first level does not affect positive-time contacts. Thus each subsequential limit solves

U_t+f(U_x)=0 in (0,infinity) x (0,1),
U(t,0)=0, U(t,1)=m, U(0,x)=U_0(x),

in the viscosity sense, with continuous strong boundary values.

For completeness, the needed comparison is the elementary first-order strong-Dirichlet comparison. If a continuous subsolution exceeds a continuous supersolution with ordered parabolic-boundary values, subtract a small strictly increasing time function from the subsolution and maximize their doubled-variable difference minus |x-y|^2/(2alpha)-|t-s|^2/(2beta). The positive maximum remains in the interior as alpha,beta decrease, by boundary continuity. The test gradients in both viscosity inequalities are identical, while their time derivatives differ by a strictly positive amount. Subtracting the two inequalities gives a contradiction. A small terminal-time blow-up penalty keeps the maximum off the top edge. This uses only continuity of the Hamiltonian and the compact Lipschitz bounds here.

Comparison implies uniqueness. Hence all primitive subsequences have the same limit, so the full sequence converges uniformly on compact time slabs. At any smooth contact with a nondecreasing 1-Lipschitz primitive, the spatial test slope lies in [0,1]. The continuation outside [0,1] therefore has no effect on the conclusion.

The distributional derivative q=U_x determines the upper-target measure. Integration by parts transfers uniform primitive convergence to weak convergence of q_n dx, uniformly in time against each fixed C^1 test function. The atomic and piecewise-constant reconstructed measures differ by O(h) against Lipschitz tests. Approximation then gives the same statement for every continuous test on the compact two-target state space. This proves convergence of the actual plans, not merely formal PDE consistency.

## 4. A three-plane supersolution sorts in finite time

Set kappa=2f(1/2)=r-sqrt(r^2-1)=tanh((b-a)/(2eta)). Define the piecewise-affine function

B(t,x)=max{0, m+x-1, (m+x-kappa t)/2}.

It is a viscosity supersolution of B_t+f(B_x)=0. Each affine branch solves the equation classically, with spatial slopes 0, 1, and 1/2, respectively. At a lower smooth contact with a maximum of affine functions, the spacetime derivative of the test function belongs to the convex hull of the gradients of the active planes. To see this, every directional derivative of the test must be at most the directional derivative of the maximum; the separating-hyperplane characterization then places its gradient in that convex hull. Thus there are nonnegative weights theta_j summing to one with p=sum theta_j p_j and tau=-sum theta_j f(p_j). Concavity of f gives tau+f(p)>=0. This proves the viscosity supersolution inequality at all interfaces as well as smooth points.

Initially, B(0,x)>=(m+x)/2>=min(m,x)>=U_0(x). At the left endpoint B(t,0)>=0, and at the right endpoint B(t,1)>=m. The strong-boundary comparison established above therefore gives U<=B. Feasibility gives U>=U_*, where U_*(x)=max(0,m+x-1).

When kappa t>=1, set z=m+x-1. The third plane is at most z/2, and z/2<=max(0,z). Consequently B(t,x)=U_*(x), and the sandwich proves U(t,x)=U_*(x) for every t>=1/kappa.

This barrier needs neither entropy boundary traces nor a general Hopf–Lax theorem. A separate independently derived max-plus formula gives the same bound in INDEPENDENT_FLUX_AUDIT.md.

## 5. Global optimality and limits

The upper-target occupancy of the limiting plan is q_*=1_{x>1-m}. Since

c(x,b)-c(x,a)=b^2-a^2-2(b-a)x

is strictly decreasing, among 0<=q<=1 with integral q=m its integral against q is uniquely minimized by putting all upper-target mass on the rightmost interval. This follows directly by transferring any upper-target mass from a smaller x to a larger x not yet saturated. Equivalently, the sign of [c(x,b)-c(x,a)] minus its value at x=1-m certifies the minimizer by integration. Hence the limiting plan at all t>=T is the unique global optimal transport plan.

There is no assertion that positive-eta finite-n iterates sort exactly in finitely many steps. Their entropic equilibrium has a nonzero microscopic mixing width. The result is specifically about the unregularized weak limit with epsilon_n=eta/n.

As eta decreases to zero, kappa increases to 1 and T decreases to 1, agreeing with the known odd-even sorting benchmark. As eta increases without bound, T diverges, consistent with the source paper's frozen eta=infinity regime.

## What this does not establish

- General-dimensional convergence, multiple-target positive-eta convergence, irregular partitions, nonuniform source density, or arbitrary costs.
- Strong convergence of raw basic-cell fractions or all hypotheses of published Theorem 3.
- Novelty priority or a complete answer to the general OWR research problem.

## Public context and standard methods

Bonafini–Medina–Schmitzer, Asymptotic analysis of domain decomposition for optimal transport (2023), https://doi.org/10.1007/s00211-023-01347-x . Theorem 3 gives a conditional general continuum description; Remark 8 explains why unrestricted weak PDE solutions are not uniquely selected.

Bonafini–Schmitzer, Domain decomposition for entropy regularized optimal transport (2021), https://doi.org/10.1007/s00211-021-01245-0 , preprint https://arxiv.org/abs/2001.10986 . Section 5 supplies the known unregularized one-dimensional sorting background.

The monotone-scheme argument is a direct first-order version of Barles–Souganidis, Convergence of approximation schemes for fully nonlinear second order equations (1991), DOI https://doi.org/10.3233/ASY-1991-4305 . The proof above supplies the needed special-case consistency and comparison rather than relying on unverified boundary hypotheses of a generic convergence theorem.

For standard viscosity terminology and comparison background, Hung Vinh Tran's public author notes: https://people.math.wisc.edu/~hung/HJ%20equations-viscosity%20solutions%20and%20applications-v1.pdf . The three-plane barrier is proved directly above; no Hopf–Lax theorem is needed.


## Audited corollary: varying entropy scale, including vanishing positive entropy

The same proof extends to eta_n=n epsilon_n tending to any eta in [0,infinity), provided the corresponding exact pair flux f_{eta_n} is used (with f_0(p)=min(p,1-p) when epsilon_n=0). These fluxes converge uniformly on [0,1] to f_eta, have a common Lipschitz bound 1, and admit globally 1-Lipschitz endpoint-tangent extensions. For eta=0 the uniform convergence follows directly from r_n=coth((b-a)/eta_n)->1 and the square-root formula. Thus the compactness, monotonicity and viscosity consistency proof is unchanged, and the same barrier applies to the limiting concave flux. For eta=0 take kappa=1, obtaining exact continuum sorting by time 1 even when every epsilon_n is positive. This is NOT the finite-n exact sorting statement; microscopic entropic mixtures persist at every finite n. This corollary passed the independent audit in POSITIVE_ETA_AUDIT.md.

For eta_n->infinity, f_{eta_n}->0 uniformly, so the same restricted primitive argument gives U_t=0 and freezes the limiting trajectory. This is consistent with, rather than a replacement for, the published general frozen-regime theorem.

## Accepted extension: uniformly decreasing C^1 two-target cost difference



### Theorem and independent verdict: PASS

The following extension is accepted under the following explicit hypotheses. Retain the one-dimensional uniform midpoint source grids, two fixed target atoms, fixed upper-target mass m, exact alternating staggered local solves, the time scale t=k/n, and weak convergence of feasible initial plans. Replace quadratic cost by two traces c(.,a), c(.,b) in C^1([0,1]). Define

D(x)=c(x,b)−c(x,a),  gamma(x)=−D'(x),

and assume gamma(x)≥gamma_min>0 throughout [0,1]. For eta_n=n epsilon_n→eta∈[0,infinity), the actual plans have the same full-sequence weak-trajectory convergence as in the main theorem. The limiting trajectory is globally optimal for every t≥1/kappa_min, where

kappa_min=tanh(gamma_min/(4eta)) if eta>0, and kappa_min=1 if eta=0.

The claim includes eta_n→0 with every epsilon_n>0, but does not assert exact finite-grid sorting for those positive entropy parameters. For eta_n→infinity the weak limiting trajectory instead freezes.

### Exact normalization

For the pair at source midpoints x_i and x_{i+1}, put

gamma_{n,i}=[D(x_i)−D(x_{i+1})]/h=(1/h) integral_{x_i}^{x_{i+1}} gamma(s) ds.

The derivative of the transport contribution with respect to the rightward fraction f is h[D(x_{i+1})−D(x_i)]=−h² gamma_{n,i}. The entropy derivative is h epsilon_n times the same logarithmic cross ratio as before. Therefore, when epsilon_n>0,

log[(p+f)(1−p+f)/((p−f)(1−p−f))]=gamma_{n,i}/eta_n.

Consequently the exact finite-grid flux has r_{n,i}=coth(gamma_{n,i}/(2eta_n)). There is no missing factor of two. In the limit,

f(x,p)=(r(x)−sqrt(r(x)²−4p(1−p)))/2,
r(x)=coth(gamma(x)/(2eta)),
2f(x,1/2)=tanh(gamma(x)/(4eta)).

For quadratic cost gamma=2(b−a), reproducing every constant in the main theorem. For epsilon_n=0 the positive pair-cost gap forces the same exact triangular sorting map as in the zero-entropy audit.

### Uniform consistency for all scale limits

Let Gamma=max gamma and let omega_gamma be its modulus of continuity. Then

gamma_min≤gamma_{n,i}≤Gamma,
|gamma_{n,i}−gamma(ih)|≤omega_gamma(h/2).

For 0<eta<infinity, joint continuity on the resulting compact parameter range gives uniform convergence of the exact edge fluxes to f(ih,p), uniformly over p∈[0,1]. The fluxes all have slope bound 1, vanish at p=0,1, and are concave in p. Their tangent-line extensions remain jointly continuous on bounded gradient ranges, uniformly monotone as numerical updates, and consistent with the same limiting Hamiltonian.

For eta_n→0, the lower bound gamma_min makes r_{n,i}→1 uniformly at every edge with positive eta_n. The estimate in POSITIVE_ETA_AUDIT.md, Section 6 (Independent check of the varying-scale corollary), then gives uniform convergence to min(p,1−p), independently of x. Zero eta_n terms already have exactly that flux. For eta_n→infinity, gamma_{n,i}≤Gamma and the maximum flux equals (1/2)tanh(gamma_{n,i}/(4eta_n))≤(1/2)tanh(Gamma/(4eta_n))→0. Thus the freezing assertion also follows directly.

Spatial and temporal primitive compactness and the endpoint traces are unchanged: they follow from feasibility and singleton handling, not from spatial constancy of the flux. At an active interior node, monotonicity is applied to the fixed local map S_{h,i}; Taylor expansion with the preceding uniform flux convergence gives U_t+f(x,U_x)=0. No gamma derivative, no C^2 regularity, and no source-paper conditional-measure assumption are required.

### Comparison with x dependence: bounded slopes close the gap

Use the doubled-variable argument of Section 3 for two nondecreasing 1-Lipschitz primitives, or for a primitive subsolution and the proposed barrier supersolution. At a positive interior maximum, holding the opposite variables fixed supplies a smooth upper test on the primitive u. Its spatial derivative p=(x−y)/alpha necessarily lies in [0,1]: this follows by considering positive and negative spatial increments in the inequalities 0≤u(t,x+d)−u(t,x)≤d for d>0. The lower test on the other function has exactly the same p.

The viscosity inequalities now imply

delta+beta/(T−t)² ≤ f(y,p)−f(x,p).

As alpha tends to zero, |x−y| tends to zero. Since f is uniformly continuous on [0,1]×[0,1], the right side tends to zero uniformly in p, contradicting the fixed positive delta. This explicitly verifies the x-dependent comparison step. Mere continuity in x on unbounded jets would not suffice in general; here the bounded-gradient fact is essential and established. This comparison proves uniqueness within the compactness class and comparison with the barrier, which is all the theorem needs. No stronger blanket comparison theorem for arbitrary unbounded-slope solutions is claimed.

### Three-plane supersolution

Use B=max{0,m+x−1,(m+x−kappa_min*t)/2}. At each x, f(x,0)=f(x,1)=0, while f(x,1/2)≥kappa_min/2. Thus every affine branch is a supersolution (the middle one need not be an exact solution). At a lower smooth contact, the test gradient is a convex combination of active affine gradients. Concavity of p↦f(x,p), at this same fixed x, gives the supersolution inequality for that combination. Hence B is a viscosity supersolution everywhere in the interior. Its initial and boundary domination are identical to the main proof. Comparison and feasibility yield U_*(x)≤U(t,x)≤B(t,x)=U_*(x) once kappa_min*t≥1.

### Unique target optimum and endpoint cases

The unregularized objective differs from a constant by integral D(x)q(x) dx, with 0≤q≤1 and integral q=m. Put s=1−m and q_*=1_{x>s}. Strict decrease of D implies

[D(x)−D(s)] [q(x)−q_*(x)]≥0

almost everywhere, with equality almost everywhere only when q=q_* almost everywhere. Integration proves unique global optimality. This argument uses only the two cost traces and their strictly decreasing difference; it does not require a globally defined Monge condition for arbitrary targets. The cases m=0,1 are trivial fixed couplings if desired, while the theorem's stated 0<m<1 already avoids them. Boundary source singleton cells remain exactly preserved by the finite algorithm; the argument introduces no exterior source cells.

### Scope and required wording

This accepts only the stated uniformly strictly decreasing two-target difference extension, with the original uniform source and midpoint discretization. It does not authorize replacing gamma_min>0 by mere nonnegativity, nor a claim for arbitrary C^1 costs, nonuniform source densities, multiple targets, or higher dimensions. In the x-dependent comparison paragraph, explicitly retain the bounded slope argument above. For eta=0 distinguish continuum finite-time sorting from finite-grid exact sorting. No publication or external state was changed during this audit.
