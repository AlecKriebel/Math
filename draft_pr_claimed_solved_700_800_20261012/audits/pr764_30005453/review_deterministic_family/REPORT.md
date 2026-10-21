# Independent adversarial review: deterministic family, PR764

## Verdict and exact claim

**PASS for Sections 2, 6 and 7 of the frozen author_v2 proof. No mathematical repair is required in this family.** The independent derivation was written before reading either historical audit. The proof hash and exact PR head are bound in INPUT_BINDING.json.

For a countable undirected simple graph with degree bounded by D, positive rates bounded above by P (their infimum may be zero), and 0<alpha<1, the vertex equilibrium equations have exactly one positive solution. Every positive classical solution of the vertex ODE that is complete in both time directions and bounded above by one common finite constant is that equilibrium. The stochastic coordinate bounds, vanishing-error representation and local derivative bounds stated before Section 6 imply precisely such complete subsequential trajectories. Section 6 does not need spatially uniform prelimit estimates. Together with the separately checked stochastic steps, this deterministic family supplies the actual final convergence mechanism.

**The literal nonnegative equilibrium uniqueness claim is false.** On the integer line with unit rates, the two alternating edge arrays (2,0,2,0,...) and (0,2,0,2,...) satisfy x=f(x) for every 0<alpha<1; every vertex denominator is 2^alpha, so none is undefined. The constant-one array is a third equilibrium. This is a complete disproof of unrestricted uniqueness, not a counterexample to uniqueness in the positive class. The positive-equilibrium theorem is a corrected formulation and should be presented separately from that disproof.

This report is a fresh mathematical family review, not a priority audit, human peer review, formal proof certificate, or whole-publication-package acceptance. No new recent-paper proof was read before closing this verdict.

## Exact source scope

I independently downloaded the official 2023 report and arXiv2010.03347v2, matching the original source hashes, and visually inspected the report's full printed pages654-655. Its model assumes positive rates bounded above and bounded degrees; its equilibrium definition x=f(x) adds no strict-positivity restriction. Conjecture1 asserts uniqueness and edgewise almost-sure convergence. The report allows general given initial counts, while the cited countable-network manuscript uses unit initial counts and nonnegative reinforcement exponents. Thus the author's positive restriction is a transparent correction, not a verified quotation of an intended source convention. The candidate proves the natural unit model and states the deterministic positive-integer extension; zero initial edges are excluded for a reason, since their reinforcement probabilities remain zero when alpha>0.

Sources: [original workshop report](https://ems.press/content/serial-article-files/47008?nt=1), [dated Couzinie-Hirsch manuscript](https://arxiv.org/pdf/2010.03347v2). Retrieval hashes and limitations are in SOURCE_RETRIEVAL.json. This review did not fetch the problem website, final journal PDF or thesis, and makes no fresh claim about them. Primary source bodies and rendered pages are removed from the safe review artifact after inspection.

## Infinite-volume variational existence

Let c=1-alpha and beta=alpha/c. The positive equilibrium reduction is bijective: x_uv^c=z_u+z_v, z_v=p_v/S_v(x), and z_v T_v(z)=p_v with T_v(z)=sum_{w~v}(z_v+z_w)^beta. Each solution automatically satisfies z_v <= (p_v/degree(v))^c <= B=P^c. An edge equilibrium is not assumed bounded first.

For each finite set F with zero exterior data, the energy consists of finitely many positive power terms and negative logarithms. Every retained vertex has an incident edge. For q=beta+1>1, the edge energy dominates (1/[2q])sum z_v^q, which dominates the finite negative logarithmic terms at infinity. Once coordinates are bounded above, approaching a zero coordinate costs infinity because its rate is strictly positive. Therefore an interior minimizer exists. The negative-log Hessian is strictly positive definite, even on bipartite graphs where the edge-power Hessian has a kernel. Its gradient is T_v(z)-p_v/z_v, with the correct incidence factor.

The universal upper estimate and local lower estimate p_v/[degree(v)(2B)^beta] hold for every finite minimizer after v is included. The lower bound can tend to zero with v. Countability gives a diagonal convergent subsequence; every vertex equation is a finite sum, so it passes to the limit. The local lower bounds keep the limit positive. This is genuine infinite-volume existence and does not assume a finite infinite-graph energy, monotone minimizers, summable rates or compactness in sup norm.

## Approximate maximum uniqueness

For two positive solutions define M=sup_v|z_v-y_v|. If M>0, fix the orientation whose signed supremum is M and choose a coordinate greater than M-epsilon. Every incident pair sum in that orientation decreases by at most epsilon. Uniform continuity of r^beta on [0,2B] gives the adverse T error at most D omega(epsilon). At the selected coordinate, the larger coordinate and its T are bounded below by M-epsilon and (M-epsilon)^beta. Subtracting the two equilibrium equations in the displayed order gives

    0 >= (M-epsilon)^(beta+1)-BD omega(epsilon),

which is impossible for small epsilon. No supremum attainment or ratio bound is needed. For 0<beta<=1, epsilon^beta is a valid modulus, including the nondifferentiability at zero; for beta>=1 use beta(2B)^(beta-1)epsilon. There is no rate-infimum hypothesis hidden in this step.

## Complete limiting trajectories

For each coordinate, eventual upper and positive lower bounds and an eventual local Lipschitz bound hold on shifted compact logarithmic-time intervals. A diagonal over vertices and intervals[-j,j] produces coordinatewise locally uniform limits defined for every real time. A coordinatewise limsup upper bound yields the same common upper bound for every limiting coordinate, without asserting a spatially uniform random threshold before the limit.

The vanishing edge error is uniformly small on each shifted compact interval because its minimum physical time tends to infinity. Local finiteness and positive limiting sums justify passing through the finite denominators and reciprocals in the integral equation. The limit is a classical positive solution of b'_v=c[p_v/T_v(b)-b_v]. No infinite-dimensional stochastic approximation theorem or uniform spatial noise estimate is being smuggled in.

## Rigidity and adversarial attacks

Take M=sup_{v,s}|b_v(s)-z_v|, bounded because b is globally bounded above and z<=B. If M>0, choose epsilon<M/4 with delta=BD omega(epsilon)/(M/2)^beta<M/4. In the upper strip d_v=b_v-z_v>=M-epsilon, all pair sums differ from equilibrium by at least -epsilon and b_v>M/2. Hence R_v(b)-z_v<=delta, so d'_v<=-cM/2.

In the lower strip d_v<=-M+epsilon, all pair sums differ by at most epsilon and z_v>M/2. Although T_v(b) might be extremely small, monotonicity of its reciprocal gives

    R_v(b)-z_v >= -z_v D omega(epsilon)/(T_v(z)+D omega(epsilon)) >= -delta,

and d'_v>=cM/2. A small current denominator makes this lower drift more positive; it creates no Lipschitz estimate or missing lower-bound hypothesis.

One coordinate at one time lies strictly in an extreme strip by the definition of supremum. The connected component of its strip-time set cannot have a finite left endpoint: integrating the strict inward forward derivative from that endpoint would contradict entry into the strip. Thus it stays in the strip for all preceding times. Backward integration then violates its global absolute bound M. This proves M=0 without differentiating a spatial supremum or taking an attained maximum.

The most substantial attempted falsifications were nonattained space-time suprema, arbitrary rate decay, reciprocal denominators tending to zero, beta<1, beta>1, disconnected graphs, time translations defined only eventually, and forward-only nonstationary trajectories. Each is controlled by a specific inequality or hypothesis above. On countably many one-edge components with p_n tending to zero, symmetric solutions satisfy b^(beta+1)=p_n/2^beta+C exp(-s); C<0 loses positivity backward and C>0 loses boundedness backward. Completeness is essential and is supplied by Section6, not assumed for the original noisy process.

## Controls, reproducibility and exact remaining gaps

The standalone standard-library script independently checks24 finite-volume path problems for beta in {1/4,1/2,1,2,4,9}, with rate2^(-abs(v)) and radius2,4,8,16. It solves each coordinate by bisection, not with author code, checks residuals and local upper/lower bounds, and treats center stabilization only as a diagnostic. It checks400 exact Fraction strip cases for beta1,2 and800 floating strip cases for beta1/4,1/2,4,9, with opposing neighbors and small coordinates. It also checks10 alternating-path boundary cases, four critical positive-cycle controls and20 vanishing-rate one-edge components. Normal and optimized Python pass with explicit exception guards; no assertions disappear under -O. The initial harness incorrectly generated one nonpositive fixture and stopped before testing the theorem; the fixture generator was corrected transparently in RESEARCH_LOG.md.

Replay without modifying the closed result:

    python3 independent_controls.py
    python3 -O independent_controls.py
    python3 verify_review.py --replay

These computations are arithmetic and finite diagnostics. Infinite existence and rigidity are supported by the preceding derivations, not by extrapolation from simulations.

After the independent derivation and controls, I read the two historical reviews. Their deterministic verdicts agree, and no additional gap emerged; their prior-work conclusions are not independently renewed here. No source or frozen proof was repaired or changed. There is no remaining deterministic mathematical issue in the assigned family. Final stochastic audit, detailed priority/current literature audit, paper/package preparation and fresh publication-package adversarial review remain outside this family verdict. The original-source disproof and corrected positive theorem must remain visibly distinct in all promoted artifacts. Alpha0 is handled by thinning, alpha1 is genuinely excluded, arbitrary zero rates or zero initial edges are excluded, unbounded degree/rates are outside the claim, and no spatially uniform convergence or quantitative stochastic rate follows.
