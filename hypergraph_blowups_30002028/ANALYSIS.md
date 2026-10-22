# Hypergraph supersaturation blow-ups: six-route audit

Date: 2026-10-21. Queue identifier 30002028, row 1836, OWR11781-001.
Result: NOT SOLVED. No new unconditional improvement of the known balanced bound is claimed. This is an authored mathematical analysis, not a source reproduction.

## Source gate and exact question

For fixed integers ell > r > 2 and fixed c > 0, does every sufficiently large n-vertex r-uniform hypergraph H containing at least c n^ell copies of K_ell^(r) contain its balanced t-blow-up for t >= gamma (log n)^(1/(r-1)), with gamma > 0 depending only on c, ell, r? Copies are non-induced and parts are disjoint. Changing labeled to unlabeled copies only changes c. Statements for impossible densities are vacuous. Logarithm bases change gamma only.

Rödl–Schacht (2012), Problem 2, gives the more general F version and identifies the clique case as sufficient. Boundary cases r=2 and ell=r are known. Catalogue wording with r=1 is not a meaningful counterexample to the intended question.

Primary sources:
- Rödl–Schacht, Complete partite subgraphs in dense hypergraphs, https://www.math.uni-hamburg.de/home/schacht/2012/blowup.pdf (Problem 2, Theorem 1, Theorem 4, Section 4).
- Fox–Wigderson–Zhou, Finding blowups one vertex at a time, arXiv:2605.23301v1, 22 May 2026, https://arxiv.org/html/2605.23301v1 (Introduction, Theorem 1.2, Section 7). This source explicitly retains the hypergraph extension as open. Its graph result is not a hypergraph resolution.

The source gate was checked before these attempts. Publication/peer-review status is separate from whether a manuscript claims a solution; here it explicitly does not.

## Route 1: Auxiliary clique hypergraph (valid known bound)

Define an ell-uniform hypergraph A on V(H) whose edges are precisely the ell-sets spanning K_ell^(r). Then e(A) >= c n^ell. Erdős's dense uniform-hypergraph theorem, applied with uniformity ell, gives a complete ell-partite ell-graph with t >= a (log n)^(1/(ell-1)). For any r distinct parts and any chosen vertices in those parts, complete to a transversal using one vertex of each remaining part. That transversal is an A-edge, so the chosen r-set is an H-edge. Therefore these parts form K_ell^(r)(t).

Adversarial check: A has uniformity ell, NOT r. Its density theorem yields exponent 1/(ell-1). When ell>r this is strictly smaller than 1/(r-1). No renaming of parameters fixes the loss. This is the unconditional baseline, already in Rödl–Schacht, not new progress.

## Route 2: Random construction (sharpness of the requested scale)

Let m=binom(ell,r), fix 0<p<1, and take H~G^(r)(n,p). Let X count unlabeled ell-cliques. Then E X=binom(n,ell)p^m and Var X=O(n^(2ell-r)): distinct clique indicators are independent unless their vertex sets share at least r vertices, and all covariances are bounded by 1. Thus X/n^ell converges in probability to p^m/ell!.

A specified injective labeled copy of K_ell^(r)(t) requires exactly m t^r distinct edges. The union bound gives
P(K_ell^(r)(t) is present) <= n^(ell t) p^(m t^r)
= exp(ell t log n - m log(1/p)t^r).
For t=ceil(A(log n)^(1/(r-1))) and A^(r-1)>ell/[m log(1/p)], this tends to zero. Hence for every fixed 0<c<1/ell! one may choose p with p^m/ell!>c and obtain arbitrarily large examples satisfying the clique-density hypothesis but containing no such blow-up above a constant multiple of the requested scale.

Adversarial check: this gives an UPPER bound on a universally guaranteed size; it does not provide the missing lower bound or refute the conjecture. Disjointness is indispensable for the edge count. The c=1/ell! endpoint is not covered and is unnecessary for exponent sharpness. Variance and union-bound events hold simultaneously with probability tending to 1.

## Route 3: Joint-link averaging and the sparse residual bottleneck

Work in four disjoint classes A,B,C,D of size N in a 3-graph and assume at least alpha N^4 transversal tetrahedra, where 0<alpha<=1 is fixed. A random partition reduces the original problem to this form with a changed positive constant. For each H-edge e in A x B x C let d(e) be the number of vertices d in D completing a tetrahedron.

Discard e with d(e)<alpha N/2. They account for at most alpha N^4/2 tetrahedra. Since d(e)<=N, the retained family E0 has at least alpha N^3/2 edges, and each has d(e)>=alpha N/2. For an integer 1<=s<=alpha N/4, average over s-subsets T of D:

average_T |{e in E0 : T is contained in the completion set of e}|
= sum_(e in E0) binom(d(e),s)/binom(N,s)
>= |E0|(alpha/4)^s
>= (alpha/2)(alpha/4)^s N^3.

So some T has size s and a residual 3-graph J_T of density at least (alpha/2)(alpha/4)^s. Every residual triple is an H-edge and every pair of that triple extends with EVERY vertex of T to an H-edge. A complete tripartite t-blow-up inside J_T would therefore give K_4^(3) with part sizes (t,t,t,s).

For s proportional to sqrt(log N), this leaves density exp(-O(sqrt(log N))). Applying only an arbitrary sparse-3-graph theorem cannot guarantee a sqrt(log N)-sized tripartite blow-up: for an arbitrary random tripartite 3-graph of edge probability q=exp(-C sqrt(log N)), with fixed C>0,
P(K_(u,u,u)^(3) occurs) <= exp(3u log N - C u^3 sqrt(log N)),
which tends to zero when u=ceil(A(log N)^(1/4)) for any fixed A>sqrt(3/C). Such residuals also have edge density (1+o(1))q by elementary concentration. To meet the exact lower bound obtained above, put rho_N=(alpha/2)(alpha/4)^s and choose instead q_N=2rho_N. For s=ceil(b sqrt(log N)), with fixed b>0, q_N<1 eventually, q_N N^3 tends to infinity, and concentration gives density at least rho_N with probability tending to 1. Moreover log(1/q_N)=Theta(s), so the same union-bound obstruction has scale (log N)^(1/4), with a changed constant. Thus edge-density information alone is quantitatively inadequate.

More generally, for growing s=o(log N), a residual density exp(-Theta(s)) has random obstruction scale sqrt(log N/s). Balancing the desired sizes s and sqrt(log N/s) yields s of order (log N)^(1/3), the generic ell=4 scale, not sqrt(log N). This balancing is an obstruction benchmark for the density-only strategy, not a proof of a matching sparse lower bound.

Adversarial check: no assertion is made that these arbitrary random residuals actually arise from a constant-tetrahedron-density host. Their purpose is to disprove the missing universal residual lemma if it uses ONLY density. The useful retained structure is its support on simultaneous joint links; that is exactly what must be exploited. The averaging statement above is a proved elementary reduction, consistent with the 2012 discussion, not a new resolution.

For K_4^-^(3), the analogous residual consists of triangles of a common-link graph; Rödl–Schacht Problem 3 asks for a triangle blow-up at triangle density exp(-C sqrt(log N)). Fox–Wigderson–Zhou Section 7 explicitly says their result is insufficient for that application. Their graph coefficient is polynomial, roughly sqrt(delta)/log(1/delta)^2, and the size condition requires N>=2^(C_H delta^(-11)). At delta=exp(-C sqrt(log N)), this requirement fails for sufficiently large N; even formal substitution in the coefficient would be too small. Thus the 2026 improvement cannot be silently inserted into the sparse joint-link argument.

## Route 4: Repeated Jensen / homomorphism counting

Take the ell-partite clique relation of density delta in equal parts of size N. Repeated Jensen gives at least delta^(t^ell) N^(ell t) homomorphisms of the complete ell-partite ell-graph with t vertices in each class. This follows by successively cloning each coordinate: conditional on all other chosen coordinates, the product of the edge indicators factors over the repeated coordinate, and convexity of x -> x^t applies. The resulting bound is the standard box-counting inequality for a complete multipartite relation.

At most ell*binom(t,2)*N^(ell t-1) choices have an in-class collision (union bound). Consequently the crude count guarantees an injective grid whenever delta^(t^ell)>ell*binom(t,2)/N. For fixed 0<delta<1, this sufficient condition yields t of order (log N)^(1/ell), even weaker than Route 1. It is not a necessary condition for injective grids to exist; the exceptional case delta=1 is a complete relation and is trivial.

Attempted repair: seek a rank-r-sensitive counting inequality whose exponent is t^r, rather than t^ell, using the fact that the clique relation is an intersection of r-coordinate constraints. No such inequality is established here. Moreover, even that hypothetical inequality combined with this crude collision subtraction would only give exponent 1/r, still below 1/(r-1). One would need more discriminating injective counting, or a construction that keeps a large class unused until the end, not merely a stronger homomorphism lower bound.

Adversarial check: a positive homomorphism count by itself may be supported on repeated vertices within classes. Partite domains prevent collisions across classes but not within them. Treating homomorphisms as injective copies is invalid. These are limitations of this exact calculation, not an impossibility theorem for all analytic methods.

## Route 5: Fixed-parameter regularity / counting / blow-up lemmas

A dense clique count can be used to locate positive-density regular complexes. For each FIXED t, counting lemmas give a fixed blow-up once N is sufficiently large. This recovers qualitative blow-up existence, not the desired rate.

The attempted uniform argument would substitute t(N)=gamma(log N)^(1/(r-1)) into fixed-target embedding results. But K_ell^(r)(t) has maximum degree binom(ell-1,r-1)t^(r-1), which is of order log N at the target scale. Bounded-degree blow-up lemmas do not allow this substitution without tracing all parameter dependencies. Likewise fixed-target counting error parameters depend on the growing number of vertices/edges. No sufficiently strong uniform dependence is proved here.

Adversarial check: regularity is not claimed incapable of solving the question; rather the proposed black-box use has an unproved uniformity step. The 2012 relative-density Theorem 4 provides an important special tool, but its input is a constant-density triangle support and near-total relative density, neither supplied by Route 3 at s=sqrt(log N).

## Route 6: Adapt the 2026 energy method

The 2026 paper's mixed structure consists of a k-partite k-uniform auxiliary relation on A_1,...,A_k together with GRAPH edges from C to each A_i. The tuples extended by c are obtained by restricting that relation to the Cartesian product N_1(c) x ... x N_k(c). Its energy maximization and subbox estimates operate on these vertex-subset restrictions.

In a 3-graph, extending a base triple by c imposes the three PAIR conditions xy in L_c, xz in L_c, yz in L_c. This is not generally a restriction of each A_i separately. Even on two classes the relation {(x,y): x and y have equal binary labels} is not a single Cartesian product: it contains (0,0),(1,1) and excludes the cross pairs. Link relations can be arbitrary bipartite graphs. For higher r the constraints similarly live on (r-1)-tuples, not on individual coordinates.

Thus directly replacing graph neighborhoods in the energy iteration by hypergraph links invalidates the Cartesian restriction identity. A possible continuation is energy on an entire lower-dimensional complex, with control of each face relation and of correlation under successive link intersections. No increment lemma or termination budget adequate for t^(r-1)=Theta(log N) is established. This route remains a research proposal, not a proof.

Adversarial check: the example only refutes the asserted single-box identity; it does not rule out a union-of-boxes argument, a multilevel energy, or another successful adaptation. The source itself describes extension of the technique as prospective rather than proved.

## Known positive cases and their exact scope

1. r=2: Nikiforov gives logarithmic clique blow-ups; the 2026 paper improves density dependence in the constant, not the logarithmic exponent.
2. ell=r: the hypothesis is edge density; Erdős gives exponent 1/(r-1).
3. Any fixed r-partite r-uniform F with at least one edge: many F copies force Omega(n^r) edges. A large complete r-partite r-graph then contains F(t) by splitting its parts into the fixed number of vertex classes required by F. This is the elementary special case recorded in Rödl–Schacht Section 4, not a solution for cliques with ell>r.
4. Rödl–Schacht Proposition 7: S_r on x_1,...,x_(r-1),y_1,...,y_r, with edges {y_1,...,y_r} and {x_1,...,x_(r-1),y_j} for every j, satisfies the desired exponent from positive S_r density. It is non-r-partite but is NOT K_ell^(r) in general.
5. Proposition 9 proves a prescribed-part version for tight 3-uniform paths, again not arbitrary clique blow-ups.

## Outcome and claim inventory

- Known import: baseline exponent 1/(ell-1), graph and single-edge cases, specified special F cases.
- Authored verification: explicit random sharpness proof; exact four-part joint-link averaging calculation; quantitative residual-density obstruction; Jensen collision audit; precise failed hypotheses in two structural approaches.
- New unconditional progress on the open conjecture: none established.
- Numerical evidence: none used or needed; no finite computation is represented as asymptotic proof.
- Recommended mathematical classification: open / analysis exhausted, not solved or disproved.
- Independent adversarial review accepted this analysis within the scope recorded in ACCEPTANCE_AUDIT.md.
