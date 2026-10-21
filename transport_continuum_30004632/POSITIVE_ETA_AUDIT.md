# Adversarial audit: positive finite eta, two target atoms

## Verdict

PASS, with the explicit hypotheses and proof details below. The exact discrete algorithm, not merely a formal PDE, selects a unique continuum primitive. For fixed 0<eta<infinity, epsilon_n=eta/n, equal-mass midpoint source grids on [0,1], two fixed atoms a<b, quadratic cost, alternating staggered partitions, and weakly convergent admissible initial plans, the full sequence converges weakly as plans, locally uniformly in time against continuous spatial tests. Its limiting plan is the unique unregularized optimum for every t≥coth((b−a)/(2eta)). No source-paper Assumption 1 on almost-everywhere conditional measures is needed for this separate scalar proof.

The general problem remains unresolved. Positive finite-n iterates are not asserted to sort exactly. The zero-entropy sorting result should be credited against the known sorting interpretation rather than promoted as new without a literature check.

## 1. Exact pair optimization and normalization

Put h=1/n and let u,v be the fractions sent to b from adjacent source atoms. Their mean p=(u+v)/2 is preserved. The objective is the quadratic transport cost plus epsilon_n times KL relative to the product marginals. Differentiating with respect to u while holding u+v fixed gives

logit(v)−logit(u)=2(b−a)h/epsilon_n=2(b−a)/eta.

The factors from the two target weights cancel. Thus u=p−f(p), v=p+f(p), where

f(p)=(r−sqrt(r²−4p(1−p)))/2,   r=coth((b−a)/eta).

Strict entropy convexity gives uniqueness for 0<p<1; p=0,1 are forced. The formula is exact for the stated finite discrete algorithm, not an asymptotic local-cell replacement. Its derivative is (1−2p)/sqrt(r²−4p(1−p)), so |f'|≤1/r<1, and f''=2(1−r²)/(r²−4p(1−p))^(3/2)<0.

For physical cumulative mass U_i=h Σ_{j≤i}u_j, an active edge satisfies

U_i^k=(U_{i−1}^{k−1}+U_{i+1}^{k−1})/2−h f((U_{i+1}^{k−1}−U_{i−1}^{k−1})/(2h)).

Inactive edges remain unchanged, and U_0=0, U_n=m_n. One partition update is time h. This works for either starting phase and either grid parity, with every unmatched boundary source cell a singleton.

## 2. Compactness and consistency without conditional-measure assumptions

At every time, 0≤U_i−U_{i−1}≤h. At an active update both old and new U_i belong to

[max(U_{i−1},U_{i+1}−h), min(U_{i−1}+h,U_{i+1})],

whose length is at most h. Spatially piecewise-linear and temporally piecewise-linear interpolation is therefore 1-Lipschitz in each variable. It is uniformly compact on each bounded time slab, with exact continuous endpoint traces 0,m and initial trace U_0.

Weak convergence of admissible initial plans implies uniform convergence of these initial primitives: the limit upper-target measure is dominated by Lebesgue measure, so its CDF is continuous; equivalently use spatial equi-Lipschitz compactness and uniqueness of the distributional derivative and left endpoint.

On the active staggered lattice, every nonendpoint neighbor was active at the immediately preceding time, apart from the harmless first level. Thus the scheme is a one-step monotone consistent approximation to U_t+f(U_x)=0 with step h, not a two-step scheme with step 2h. Inactive-node interpolation differs from active-time values by at most h and has the same limit.

The update is order-preserving in its two arguments because its derivatives are (1+f')/2 and (1−f')/2. It commutes with adding constants. At maximizing active nodes for U_n−phi, this monotonicity gives the test-function scheme inequality, and Taylor expansion yields phi_t+f(phi_x)≤0. At minimizing nodes it yields the reverse inequality. Strict local extrema can be imposed by the usual small smooth perturbation. All interior touching test gradients lie in [0,1], by the monotone 1-Lipschitz spatial constraint. For applying the scheme to arbitrary test values, extend f by its endpoint tangent lines; this preserves global Lipschitz continuity, concavity, and monotonicity of the numerical update.

These details close the staggered-consistency and boundary gaps: no boundary flux is guessed, and no extension of discrete source fractions beyond the endpoints is used.

## 3. Strong-boundary comparison: a self-contained argument

For completeness, the required comparison is only for continuous sub- and supersolutions with ordered actual traces on the initial and spatial boundaries. Let u be a subsolution and v a supersolution of U_t+H(U_x)=0 for the same continuous Hamiltonian H, and suppose a positive interior difference exists on a finite slab. Subtract a small positive multiple delta*t from u and choose a slightly later terminal time T; a small barrier beta/(T−t) keeps positive maxima away from T. Maximize

u(t,x)−v(s,y)−delta*t−beta/(T−t)−((x−y)²+(t−s)²)/(2 alpha),

Here alpha tends to zero. Uniform continuity and boundary ordering force any positive limiting maximizer away from t=0 and x=0,1; both test points are interior for sufficiently small alpha. Freeze the opposite variables to obtain viscosity tests. Both spatial test derivatives are p=(x−y)/alpha. Their time derivatives are respectively (t−s)/alpha+delta+beta/(T−t)² and (t−s)/alpha. Subtracting the subsolution and supersolution inequalities gives delta+beta/(T−t)²≤0, a contradiction. Let the small parameters vanish. This proves comparison and uniqueness for the strong-boundary solution produced by compactness.

Therefore every subsequence has the same limit and the entire sequence of primitives converges uniformly on compact time slabs. Uniform primitive convergence gives convergence of upper-target measures against C^1 tests by integration by parts. Approximation extends this to continuous tests, uniformly in time. Replacing interval reconstructions by midpoint atomic measures changes Lipschitz tests by O(h). The lower-target component is the known source marginal minus the upper-target component. Thus actual transport plans converge. This does not assert strong L1 convergence of microscopic cell fractions.

## 4. Simpler finite-time supersolution, avoiding max-plus boundary algebra

Let m be the upper-target mass, let kappa=2f(1/2)=tanh((b−a)/(2eta)), and define

B(t,x)=max{0, m+x−1, (m+x−kappa*t)/2}.

This is a viscosity supersolution of U_t+f(U_x)=0. Each affine branch solves the equation: its (time,space) gradient is (0,0), (0,1), or (−kappa/2,1/2). At a corner, the gradient of any differentiable lower test belongs to the convex hull of the active affine gradients. Concavity of f implies a+f(p)≥0 for every such convex combination. This is the correct direction: max of affine solutions works as a supersolution because the Hamiltonian is concave, not by a general rule that maxima of supersolutions are supersolutions.

Initially, U_0(x)≤min(x,m)≤(m+x)/2≤B(0,x). On the endpoints, B(t,0)≥0 and B(t,1)≥m. Comparison therefore gives U≤B. Feasibility independently gives U≥U_*(x)=max(0,m+x−1).

For t≥1/kappa, put z=m+x. The middle plane is at most (z−1)/2≤max(0,z−1), whether z≤1 or z≥1. Hence B(t,x)=U_*(x), and the limiting primitive is exactly U_* for all t≥1/kappa. The associated upper-target density is 1_{x>1−m}; strict monotonicity of the quadratic target cost difference makes this the unique unregularized global optimum.

This supersolution proves the proposed sorting-time bound directly and renders the more delicate full-line triangular-flux representation unnecessary.

## 5. Required presentation corrections / guardrails

1. State the exact positive-eta scaling epsilon_n=eta/n, the equal midpoint masses, fixed two-atom target, weak initial convergence, and the partition/time convention together with the theorem.
2. Include active-lattice consistency and strong boundary comparison, rather than simply naming the formal conservation law or invoking the source paper's limiting PDE.
3. Prefer the three-plane supersolution above; if retaining the full-line formula, prove its boundary assertions carefully. In particular the right-boundary bound must use the displacement constraint y≥1−kappa*t as well as V_0(y)≤m, so the subtracted cost is nonnegative.
4. Say weak convergence of actual plans, not strong convergence of oscillatory cell fractions. No source Assumption 1 is silently imported or proved.
5. The full-sequence result is for this scalar special case only. It does not imply selection or optimality for the unrestricted weak continuity-equation formulation.
6. Positive finite-n exact sorting is false in general; finite-time sorting is a statement about the n→infinity trajectory.
7. The zero-entropy finite-grid bound can be strengthened from the draft's conservative 2n to n; see the separate ZERO_ENTROPY_AUDIT.md. This is optional, not a validity defect.

## Numerical sanity check

check_positive_eta.py independently iterates the exact finite pair map for initially inverted half-mass data, eta in {0.1,0.5,1,2,5}, and n in {64,256,1024}. It records cumulative error at ceil(n*coth(1/(2eta))) updates and total-mass error. Results show the expected positive finite-grid residuals, with no counterexample. For small eta and modest n, temporal rounding can dominate the observed trend, so these computations are not an asymptotic proof. The analytical argument above is decisive.

## 6. Independent check of the varying-scale corollary

The varying-scale corollary in RESEARCH.md also passes. Write eta_n=n epsilon_n. For eta_n→eta in (0,infinity), the corresponding exact fluxes converge uniformly on [0,1] by joint continuity. At eta=0, put r_n=coth((b−a)/eta_n)→1 for positive eta_n, and use

sup_p |f_{r_n}(p)−min(p,1−p)| ≤ ((r_n−1)+sqrt(r_n²−1))/2 →0.

Terms with eta_n=0 use the exact triangular flux already. Each flux has Lipschitz constant at most 1 and monotone tangent-line extensions; these extensions converge uniformly on compact gradient sets. The same compactness and test-function proof therefore selects the viscosity solution for the limiting flux. The three-plane barrier applies with kappa=1 at eta=0, yielding continuum sorting at time 1 even if all finite epsilon_n are positive. This does not assert finite-n exact sorting.

For eta_n→infinity, r_n→infinity and sup_p f_{r_n}(p)=1/[2(r_n+sqrt(r_n²−1))]→0. The same argument gives U_t=0 and hence a frozen limiting primitive. This agrees with the known general frozen-regime result.

Earlier cautions against replacing epsilon_n=0 by n epsilon_n→0 concern the finite-grid exact sorting argument, not this separate, now-checked continuum consistency argument.

## 7. Independent audit of the C^1 two-target cost extension

### Scoped verdict: PASS

The C^1 extension at the end of RESEARCH.md is valid under the following explicit hypotheses. Retain the one-dimensional uniform midpoint source grids, two fixed target atoms, fixed upper-target mass m, exact alternating staggered local solves, the time scale t=k/n, and weak convergence of feasible initial plans. Replace quadratic cost by two traces c(.,a), c(.,b) in C^1([0,1]). Define

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

For eta_n→0, the lower bound gamma_min makes r_{n,i}→1 uniformly at every edge with positive eta_n. The estimate in Section 6 then gives uniform convergence to min(p,1−p), independently of x. Zero eta_n terms already have exactly that flux. For eta_n→infinity, gamma_{n,i}≤Gamma and the maximum flux equals (1/2)tanh(gamma_{n,i}/(4eta_n))≤(1/2)tanh(Gamma/(4eta_n))→0. Thus the freezing assertion also follows directly.

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
