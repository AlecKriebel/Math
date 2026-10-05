# Independent adversarial audit: subcritical reinforcement, problem 30005453

Date: 5 October 2026 (UTC). Rank 798, OWR-12697708-006.

## Verdict and its exact boundary

**Mathematical PASS for the positive-equilibrium theorem actually stated in
Sections 1–9 of the frozen author proof.** I found no analytic gap in the
existence, uniqueness, or almost-sure coordinatewise convergence argument.
This verdict includes bounded strictly positive firing rates with infimum zero.
The argument supplies all steps needed for the countable infinite graph; the
finite diagnostics are supplementary and are not the basis of this verdict.

The verified theorem concerns a countable undirected simple graph of uniformly
bounded degree, vertex rates 0 < p_v <= P, unit initial edge counts, and
0 <= alpha < 1. It gives exactly one equilibrium positive on every edge, and
simultaneous almost-sure coordinatewise convergence N_e(t)/t to that array.
Isolated vertices can be discarded. It does not give uniqueness among
nonnegative equilibria, uniform spatial convergence, or a stochastic rate.

**Literal nonnegative-equilibrium uniqueness is FALSE.** For every 0 < alpha < 1,
the two alternating arrays 2,0,2,0,... on the integer line with unit vertex rates
are distinct fixed points with nonzero denominators at every vertex. The
constant-one array is a third equilibrium. This does not contradict the
positive-equilibrium theorem or its convergence conclusion from unit counts.

**Mandatory source-description correction:** calling the positive formulation
the source's “intended” statement must be marked as an interpretation. It is a
natural corrected formulation, but the report does not explicitly impose this
restriction. The revised wording is supplied separately. A minor equation
reference in the nonunit-initial-count extension also needs correction. Neither
change repairs an analytic gap. Any v2 accompanying this audit is an unaccepted
proposed edit and requires a separate delta review. This audit does not silently
accept its own editorial changes.

No priority, novelty, journal acceptance, or external publication-readiness
claim follows from this review.

## 1. Frozen input and independence

The author ZIP is 19,790 bytes, SHA-256
4e2b7cbf89688b04a80bfae946457582f8970cb90d6af260302aa1dad3a33856.
Its manifest SHA-256 is
1c82aa6a5869110dacd64d0ee64e28b702a59e5224dacb44594fdf9c06910691.
The reviewed PROOF.md is 17,727 bytes, SHA-256
f3a3d0b267c0fde305977fd3c7d3b182825a9674b1e903bf1b354d6e220139c9.

All 11 archive members were independently checked against an exact allowlist,
CRC, size, and manifest hashes. Duplicate members, missing members, a changed
proof byte, an extra PDF, a symlink, and a traversal path were each rejected by
negative controls. The original directory and ZIP are preserved unchanged.

The mathematical review reconstructed the inequalities and limiting argument
directly. The independent finite verifier does not import or invoke the author's
code and uses different deterministic rational inputs. Replaying the author's
code in an isolated extraction is reported separately from this reconstruction.

## 2. Sources, target, and scope

The report's printed pages 653–655 were inspected, including visual inspection
of pages 654–655. Its model has positive bounded vertex rates and bounded
degrees. Its fixed-point definition and Conjecture 1 do not explicitly restrict
equilibria to the strictly positive class. Thus the boundary counterexample
requires an explicit correction of the literal uniqueness formulation, rather
than attribution of an unstated convention to the report. The report's
initial-count discussion also does not itself impose unit counts.
[Primary report](https://doi.org/10.4171/OWR/2023/12).

The cited Couzinié–Hirsch manuscript explicitly uses alpha >= 0 and unit initial
counts. Its equilibrium definition permits nonnegative arrays, whereas its
existence and convergence arguments single out nonvanishing equilibria. Its
Theorem 2.2 covers alpha < 1/2 on general bounded-degree graphs, a larger interval
on regular graphs, and alpha < 1 on the line. This supports the relevance of the
positive formulation but does not make literal nonnegative uniqueness true.
The inspected source is arXiv v2, 25 June 2021; the ECP publication identity is
26 (2021), paper 35, DOI 10.1214/21-ECP404.
[Author manuscript](https://arxiv.org/abs/2010.03347).

The 2018 thesis explicitly states positive-equilibrium uniqueness in its main
general theorem, but restricts that theorem to alpha < 1/2 and starts with rates
uniformly bounded away from zero. This is additional evidence for the corrected
positive formulation; it does not prove the all-subcritical theorem audited
here. Its title, introductory hypotheses, main theorems, and equilibrium section
were inspected.
[Thesis](https://www.theorie.physik.uni-muenchen.de/TMP/theses/couziniethesis.pdf).

## 3. Equilibrium reduction, existence, and uniqueness

Write c=1-alpha and beta=alpha/c, initially with 0<alpha<1. For a strictly positive
edge equilibrium, z_v=p_v/S_v(x) is positive. Dividing the edge equation by x_e^alpha
is legal and gives x_uv^c=z_u+z_v. Substitution yields

    z_v T_v(z)=p_v,  T_v(z)=sum_{w~v}(z_v+z_w)^beta.

The converse is exact, so neither existence nor uniqueness is lost in the change
of variables. Each vertex has a neighbor after isolates are removed. Therefore
T_v(z)>=d(v)z_v^beta and z_v<=(p_v/d(v))^c<=B=P^c. This bound is derived for
every positive equilibrium; it is not an extra boundedness hypothesis.

For a finite vertex set F, use zero boundary values and minimize the displayed
power-sum minus sum p_v log z_v. The edges meeting F are finite. For q=beta+1>1,
the edge terms dominate a positive multiple of sum_{v in F}z_v^q, so the negative
logarithms cannot cause escape to infinity. After bounding the other coordinates,
approaching a coordinate hyperplane forces the objective to infinity. An
interior minimizer exists. The positive diagonal Hessian of the negative-log
part makes it strictly convex, including bipartite graphs where the edge-power
part alone has a kernel. Its first-order conditions are exactly the vertex
equations, with no missing incidence factor.

All minimizers satisfy z_v<=B. At each fixed vertex eventually in F they also
satisfy z_v>=p_v/[d(v)(2B)^beta]>0. The lower bound may vary with v. Countable
product compactness gives a subsequence, and finite degree permits passage to
each equation. This is a valid infinite-volume existence proof; it does not
extrapolate finite-dimensional strict convexity to the infinite problem.

For uniqueness, let M=sup_v|z_v-y_v|>0 and select a vertex with one signed
difference greater than M-epsilon. Every incident pair sum then differs in
that direction by at least -epsilon. Uniform continuity of r^beta on [0,2B]
gives a possible adverse sum error at most D omega(epsilon). At the selected
vertex the larger coordinate is at least M-epsilon, so its T is at least
(M-epsilon)^beta. Subtracting z_v T_v(z)=y_v T_v(y) gives the lower bound

    0 >= (M-epsilon)^(beta+1) - B D omega(epsilon),

which is impossible as epsilon tends to zero. No vertex attaining M is needed.
The estimate also works for 0<beta<1, because only uniform continuity, not a
Lipschitz constant at zero, is used. This rules out unbounded-ratio loopholes
when rates tend to zero: the norm used is the absolute z-coordinate difference.

## 4. Graphical construction and local nonexplosion

Every edge can be incremented only by its two endpoint clocks. Hence its count
has finitely many jumps on compact intervals and is bounded above by its initial
count plus the sum of two ordinary Poisson counts. The global system is not
constructed by ordering all firings in the graph, which would be invalid when
the total firing rate is infinite.

One explicit justification of the usual graphical construction is to explore
the causal predecessors of a fixed local query during [0,T]. A predecessor
walk at the vertex level has at most D+1 choices at each step, including staying
at the current vertex, and its times are strictly decreasing. The expected
number of length-n time-ordered Poisson sequences is bounded by a fixed local
factor times ((D+1)PT)^n/n!. The tail tends to zero. Local finiteness of the
predecessor tree then rules out an infinite ancestry chain and yields a finite
dependency set almost surely. Marks resolve each finite set in chronological
order. Taking countably many queries and integer horizons gives a consistent
process. No positive lower rate or bounded initial-count array is required.

## 5. Exact transform, bracket, and positive growth

For one edge, write q=p_u/S_u(N)+p_v/S_v(N), Q=int q, and lambda=N_e^alpha q.
Since unit initial counts stay at least one, q<=p_u+p_v and lambda<=p_u+p_v.
The exact jump of H(n)=sum_{j=1}^{n-1}j^(-alpha) is n^(-alpha); consequently
the compensator of H(N_e) is exactly Q. Its square-jump compensator is
int N_e^(-alpha)q<=Q. Finite-time square integrability follows from the bounded
clock rates. No diffusion approximation or Taylor expansion is being used.

The normalization M/Q is justified by defining A=1+Q and L=int A^(-1)dM.
Its predictable quadratic variation has expectation at most one because
int (1+Q)^(-2)dQ<=1 pathwise. Thus L is L2-bounded and converges almost surely.
The integration-by-parts identity

    M/A = L - A^(-1) int L dA

then gives M/A->0 on A->infinity by weighted Cesaro convergence. Q is a
continuous adapted finite-variation process, so there is no predictability or
jump correction issue. There is also no invalid assumption that the time change
is independent of the edge process.

The endpoint Poisson upper bound gives limsup N_f(t)/t<=2P for every fixed edge.
Only finitely many f enter the two relevant denominators. Thus for a fixed edge
and epsilon>0, eventually

    q(t) >= [p_u/d(u)+p_v/d(v)](2P+epsilon)^(-alpha)t^(-alpha).

This proves Q grows at least on the t^c scale, before the martingale law is
used. Integral comparison H(n)=n^c/c+O(1) and H(N)=Q+M imply
N_e^c/(cQ)->1 and the stated positive liminf for N_e/t. There is no circular
use of linear growth in the martingale proof. The threshold time may depend on
the edge; countability only intersects probability-one events and does not
produce a uniform spatial threshold.

The same equations and the upper bound give Q=O(t^c) and M/t^c->0. Splitting
Q into its two endpoint integrals gives the exact asymptotic additive vertex
representation X_uv^c=A_u+A_v+o(1). All normalizing factors c are correct.

## 6. Local time-shift compactness and the limiting equation

A_v is nonnegative and locally absolutely continuous for t>0. Its upper limit
is at most (2P)^c because it is bounded by the sum at any incident edge up to an
error tending to zero. Directly integrating the denominator upper bound gives
liminf A_v>=p_v/[d(v)(2P)^alpha]>0. Again this is a fixed-coordinate bound.

With t=exp(s), differentiation gives

    a'_v(s)=c[p_v/S_v(X(exp(s)))-a_v(s)].

The positive growth estimate bounds each fixed denominator away from zero
eventually, and bounds the derivative for that vertex. It is unnecessary to
bound these derivatives uniformly in v. Arzela–Ascoli on each coordinate and
each compact time interval, followed by one countable diagonal subsequence,
produces a trajectory defined for all real times. Limiting upper bounds are
common, although no uniform prelimit spatial bound was claimed; this follows
by taking each coordinate limit separately and then intersecting countably.

An error r_e(t)->0 is uniformly small over a shifted compact logarithmic-time
interval because the smallest physical time in that interval tends to infinity.
Using x_e^alpha=(x_e^c)^beta and finite incident sums gives locally uniform
convergence of the denominators. Positive limiting coordinates justify taking
their reciprocals. Passing through the integral equation gives a classical
solution b'_v=c[p_v/T_v(b)-b_v]. This is a product-topology compactness argument,
not an invocation of a finite-dimensional stochastic-approximation theorem.

## 7. The decisive bounded-complete-trajectory lemma

This is the most consequential infinite-graph step. Its proof is valid.
Let M=sup_{v,s}|b_v(s)-z_v|>0 over all vertices and all real times, and let d=b-z.
Both arrays lie in a common bounded interval. Choose epsilon<M/4 so that
B D omega(epsilon)/(M/2)^beta<M/4.

If d_v>=M-epsilon, every incident pair sum for b is at least the corresponding
sum for z minus epsilon. Also b_v>M/2, so T_v(b)>=(M/2)^beta. Since p_v=z_v T_v(z),

    p_v/T_v(b)-z_v <= B D omega(epsilon)/(M/2)^beta < M/4.

Hence d'_v<=-cM/2 throughout the upper strip. For the lower strip, d_v<=-M+epsilon
implies z_v>M/2 and T_v(b)<=T_v(z)+D omega(epsilon). The potentially delicate
denominator is handled by monotonicity of T_v(z)/T, yielding

    p_v/T_v(b)-z_v >= -z_v D omega(epsilon)/(T_v(z)+D omega(epsilon)) > -M/4.

Thus d'_v>=cM/2 throughout the lower strip. This lower-strip inequality does
not require a lower bound for T_v(b), b_v, or p_v uniform across vertices.

Some fixed coordinate and some time lie strictly inside one of the two strips
by the definition of supremum. For that one coordinate, the strict derivative
sign forbids entry into the strip from its inner boundary in forward time.
Therefore the coordinate must stay in the strip at every earlier time. Integrating
the same nonzero derivative bound backward contradicts the global bound M.
The supremum need never be attained. No derivative of an infinite supremum,
infinite Lyapunov sum, or spatially uniform stochastic noise estimate is used.

Completeness is essential. A bounded solution only on a forward half-line need
not be stationary, even on a single edge. The proof applies the lemma only to
the complete limiting trajectories established in the previous section.

## 8. Completion, endpoints, and attacks on extensions

Every sequence of logarithmic times tending to infinity has a subsequence
whose locally uniform coordinate limits are z. If a fixed coordinate failed
to converge to z_v, a separated sequence would yield a contrary subsequential
limit at time zero. This proves actual coordinatewise convergence, not merely
existence of an equilibrium subsequence. The edge representation then gives
X_uv->(z_u+z_v)^(1/c). Countability makes all edge conclusions simultaneous.

At alpha=0, each marked vertex clock selects uniformly among finitely many
incident edges, so Poisson thinning directly gives the stated deterministic
edge rates. Alpha=1 is correctly excluded: c vanishes and even cycles have
multiple positive alternating equilibria. Negative exponents are outside the
chosen model convention. If there are no edges at all, all edge statements are
vacuous and the empty array is the only equilibrium array.

For arbitrary deterministic positive integer initial counts, each initial
coordinate is finite and its contribution divided by t vanishes. The exact
compensated identity becomes H(N_e(t))-H(N_e(0))=Q_e(t)+M_e(t). Bracket domination
and all local bounds remain valid. The frozen text points to equation (12),
but the required change is equation (9); this is an editorial error, not a
failure of the extension. Fractional initial counts are not required by the
theorem and were not promoted to an independently audited extension here.

No initially zero-edge extension follows: at alpha>0 those edges remain zero.
No unbounded-degree extension follows from the argument, whose uniqueness and
rigidity estimates use D. No uniform-in-edge convergence follows either.
For example, countably many independent disjoint edges with unit vertex
rates have spatially unbounded Poisson fluctuations at each fixed time, even
though every fixed edge satisfies a strong law.

## 9. Computation, provenance, prior work, and limitations

The independent suite rebuilt seven graph families, four beta values, and two
rate families: 56 cases and 2,168 exact rational checks. It additionally ran 300
exact perfect-power jump/bracket controls including alpha<1/2, 32 alpha=1
positive-alternation controls, and a nonunit-initial-offset check. All passed.
The integer-beta suite alone would not cover the difficult continuity-at-zero
regime; that regime is covered by the analytic modulus argument above.

Both complete supplied corpora were rehashed: 68,931,837 and 80,334,822 bytes,
with the hashes in results/provenance.json. The problem occurs uniquely at
index 14237 among 15,458 records. The 6,701-entry research corpus has no matching
key or numeric-ID bytes. The review digest nonetheless reconstructs exactly
using the missing-report empty object and the repository's JSON serialization
rule. It equals the catalog value
23a9b4f35fc3c8b7ae15e35434a656a6b8c9656a95dd6a150feeeb0a4028c0a3.
The complete catalog was rehashed and matched to its freshly observed Git blob.

The public report, manuscript, and thesis were independently downloaded again,
and all three full PDFs match the author's sizes and hashes. Those PDFs,
extractions, screenshots, and raw corpora are deliberately absent from the
safe artifact. Source findings are short original summaries plus metadata.

Independent repository searches found no matching actual prior attempt in
exact-ID PR, commit, or code queries, a subcritical-reinforcement PR query,
the nontruncated 725-entry problems subtree, or the nontruncated 63-entry
attempts subtree at observed main commit
7521b4e8f0e351a2b86edba83e3c7b02cd48f3c0. This does not exclude unindexed history,
deleted branches, or unpublished private work. No remote write was performed.

Fresh title/author/topic searches and primary author-publication pages did not
locate a later source proving this complete all-subcritical heterogeneous-rate
theorem. Older “Infinite WARM graphs I” references identify manuscripts rather
than supply an inspected full solution. The 2025 UCI talk listing gives no
theorem with which to settle this question. These are bounded search outcomes,
not proof of novelty. See SOURCE_CHECK.json for checked links and retrieval
limitations. External specialist review remains appropriate before any claim
of a new published resolution.
