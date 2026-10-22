# Root mathematical audit of PR764

2026-10-14 UTC. Reviewed immutable head
`88acf20cdd5b4fe8605dab7eb27733b7deda1c47`; upstream ID 30005453,
OWR-12697708-006. This is independent verification of a complete candidate
recorded at four of five substantive proof turns, not a new search for an
unfinished theorem.

## Target and falsifiable success criteria

The complete selected source record and its empty prior-report join were read.
Their current statement and review hashes match the native catalog. The official
OWR report was freshly retrieved; printed pages 654–655 were rendered and
visually inspected. The cited 2021 arXiv v2 was freshly retrieved and its model,
equilibrium definition, Conjecture 2.1 and Theorem 2.2 read. These bytes match the
historical retrieval pins. Source bodies are excluded from public outputs.

The literal report defines equilibrium by every edge's fixed-point equation,
without requiring strictly positive coordinates. Its uniqueness claim is false:
on the integer line, with unit vertex rates and any 0<alpha<1, alternate edge
weights 2 and 0. Every denominator is 2^alpha. Each positive edge has rate 2;
each zero edge has rate 0. Both phases, and the constant-one array, satisfy the
equations. This exact infinite construction refutes nonnegative uniqueness.

The substantive positive theorem in author_v2/PROOF.md is separately stated:
on any countable undirected simple graph of uniformly bounded degree, with
0<p_v<=P and 0<=alpha<1, there is exactly one equilibrium positive on every edge.
From unit initial counts, or deterministic finite positive integer initial
counts at every edge, N_e(t)/t converges almost surely coordinatewise to that
equilibrium. The infimum of the rates and initial-count uniform bound are not
assumed. The corrected positive formulation is an interpretation of the
homogenization question, not a positivity restriction attributed to the OWR
definition. The report gives initial counts without imposing unit initialization;
the cited 2021 model expressly uses unit counts and alpha>=0. Fractional initial
weights are not part of the frozen candidate's promoted theorem.

Success requires a valid infinite-volume existence argument, uniqueness over
all positive equilibria without an assumed bound, stochastic construction and
martingale control, a noncircular positive growth bound, extraction of complete
limiting trajectories, their rigidity, and actual simultaneous coordinatewise
convergence. Finite diagnostics alone cannot discharge any infinite or
probabilistic step. Boundary uniqueness, spatially uniform convergence, alpha=1,
negative exponents and unbounded-degree graphs are excluded.

## Deterministic reconstruction

Put c=1-alpha and beta=alpha/c for 0<alpha<1. Positive edge equilibria correspond
bijectively to vertex solutions z_v T_v(z)=p_v, where
T_v(z)=sum_{w~v}(z_v+z_w)^beta and x_uv=(z_u+z_v)^(1/c).
Every such z satisfies z_v<=(p_v/d(v))^c<=B=P^c, because
T_v(z)>=d(v)z_v^beta. Boundedness is a deduction, not a hidden extra hypothesis.

On each finite vertex set, the edge-power potential with zero exterior values
and the negative logarithmic barriers is coercive and strictly convex. Its
minimum is interior and solves exactly the vertex equations. Every fixed
coordinate's minimizers have the positive bound p_v/[d(v)(2B)^beta]. Countable
diagonal extraction and finite neighborhoods therefore produce a positive
infinite-volume solution.

For two solutions, approximate a signed supremum M>0 of their absolute
difference. Every adjacent pair sum loses at most epsilon. Uniform continuity
of r^beta on [0,2B] yields
0>=(M-epsilon)^(beta+1)-BD*omega(epsilon), impossible as epsilon tends to zero.
This uses neither an attained maximum nor a lower bound on all rates.

For a positive bounded complete trajectory b of
b_v'=c[p_v/T_v(b)-b_v], compare with z using
M=sup_{v,s}|b_v(s)-z_v|. Near its upper strip, b_v>M/2 protects T_v(b) and gives
d_v'<=-cM/2. Near its lower strip, z_v>M/2 protects T_v(z); monotonicity of the
reciprocal gives d_v'>=cM/2 even when T_v(b) is very small. The common modulus
on a bounded interval suffices for beta<1 as well as beta>1. Choose one fixed
coordinate strictly inside a strip. Its connected strip interval cannot have
a finite left endpoint, since the forward derivative points inward toward the
interior of the allowed range. Integrating backward on the interval contradicts
the bound M. Thus every such complete trajectory is stationary. This does not
differentiate an infinite supremum or sum an infinite Lyapunov function.

## Stochastic reconstruction

Bounded degrees and rates give a graphical construction using finite causal
ancestry: time-ordered Poisson dependency paths have an exponential factor in
their length divided by a factorial. A countable intersection of local queries
and finite horizons defines a consistent process. Each edge is incremented only
by its two endpoint clocks, so it has finitely many jumps on compact intervals
and limsup N_e(t)/t<=p_u+p_v<=2P.

The integer transform H(n)=sum_{j=1}^{n-1}j^(-alpha) has exact jump n^(-alpha)
and asymptotic n^c/c+O(1). For one edge, its compensator is exactly
Q=int[p_u/S_u(N)+p_v/S_v(N)], while the compensated martingale has bracket
int N_e^(-alpha)dQ<=Q. Finite-horizon square integrability follows from bounded
endpoint clocks and N_e>=1. Integrating the martingale against (1+Q)^(-1)
gives an L2 bounded martingale with bracket at most one. Integration by parts
and weighted Cesaro convergence prove M/Q->0 on Q->infinity.

The endpoint-clock upper bounds on the finite incident neighborhood give
q_e(t)>=k_e t^(-alpha) eventually, with k_e>0 for every fixed edge. This proves
Q grows on the t^c scale before using the normalized martingale law. It then
implies positive linear lower growth of each edge. The upper clock bound,
H(N)/Q->1 and M/Q->0 also give M/t^c->0 without any spatial martingale maximum.
Splitting Q into endpoint integrals yields
X_uv^c=A_u+A_v+r_uv with r_uv(t)->0.

Every vertex A_v has a common limiting upper bound and its own positive lower
bound. Its logarithmic-time derivative is locally bounded at large times for
that coordinate. Arzela–Ascoli and a countable diagonal subsequence over vertices
and compact time intervals give a positive, bounded complete limiting trajectory.
The edge errors tend uniformly to zero on each shifted compact time interval.
Finite neighborhoods and positive limiting denominators justify passage through
the integral equation. Rigidity makes every subsequential trajectory z; a
separated sequence at one coordinate would contradict this. Actual edgewise
convergence follows, on one probability-one event by countability. No common
random threshold or sup-norm compactness was used.

For positive integer initial counts replace H(N(t)) by
H(N(t))-H(N(0)); each finite initial constant disappears after scaling. At alpha=0,
Poisson thinning proves the stated limits directly. Edgeless graphs are vacuous;
disconnected graphs need no additional assumption. Alpha=1 genuinely lies
outside the transform and rigidity argument, and has positive boundary-of-scope
examples. No analytic repair to author_v2 was found necessary.

## Evidence status

Root mathematical reconstruction: PASS for the exact corrected theorem and
literal counterexample above. Normal and optimized diagnostic reproduction and
integrity checks are recorded separately, including environmental failures.
Frozen author code contains assertions, so an optimized replay is not evidence
that those assertions ran. The normal assertion replay and new independent
family controls are required. Mathematical acceptance depends on the derivations,
not these finite controls.

Two fresh independent approach families are finishing their closed reports.
A preliminary source search located arXiv:2610.11780 (Shuo Qin, submitted
8 October 2026), whose abstract claims the same positive homogenization theorem.
No detailed priority verdict has yet been made. The full theorem, proof, public
chronology and earlier literature must be compared after the math gate before
any submission package or publication is prepared. No first-priority,
publication-readiness or external human peer-review claim follows from this log.

Current PR process completion estimate: 35%; shard estimate: 28%.
