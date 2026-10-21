# Independent adversarial audit: hypergraph clique blow-ups

Audit date: 2026-10-21 UTC. Target: catalogue 30002028, queue row 1836. This is an authored mathematical audit.

## Verdict

ACCEPT the six-route analysis as a verification of known bounds and failed proof strategies, not as a solution, disproof, or new unconditional lower bound. The normalized open target is fixed integers ell > r > 2, fixed c > 0, sufficiently large n, and a balanced non-induced K_ell^(r)(t) with t >= gamma(c,ell,r)(log n)^(1/(r-1)). All parts must be disjoint. Impossible copy densities are vacuous.

Initial inspected ANALYSIS.md SHA-256: 94991644186c1e93a8c02c48aea367cbf20bd87a5b942eaba46ffc43f83abb4c. A final acceptance addendum will identify any revised accepted file.

## Independent calculations

1. Auxiliary clique hypergraph. Its uniformity is ell, its edge count is the count of unlabeled ell-cliques, and the dense complete-partite theorem therefore gives exponent 1/(ell-1). Completing each selected r-tuple to an ell-transversal proves transfer back to H. No exponent 1/(r-1) follows when ell > r.

2. Random dense obstruction. Put m=binom(ell,r), p in (0,1) fixed. Distinct clique indicators are independent if their vertex sets overlap in fewer than r vertices. Summing covariance over overlaps k>=r, together with diagonal terms, gives Var X=O(n^(2ell-r)). Thus X/n^ell tends in probability to p^m/ell!. An injective labeled blow-up requires exactly m t^r different edges, and its possible placements number at most n^(ell t). For t=ceil(A(log n)^(1/(r-1))), the logarithm of the first-moment bound is

[ell A - m log(1/p) A^r + o(1)] (log n)^(r/(r-1)).

It tends to minus infinity whenever A^(r-1)>ell/(m log(1/p)). Choosing p^m>c ell! is possible for every fixed 0<c<1/ell!. The concentration and nonexistence events intersect with probability tending to one. Absence at this t also forbids every larger balanced blow-up by trimming. This establishes exponent sharpness only: it neither proves a matching universal lower bound nor identifies the optimal constant. The endpoint c=1/ell! is not needed and, for finite n and unlabeled copies, exceeds binom(n,ell)/n^ell.

3. Joint links. Explicit domain: fixed 0<alpha<=1, integer N large, integer 1<=s<=alpha N/4. Removing triples with fewer than alpha N/2 extensions discards at most alpha N^4/2 tetrahedra. Hence at least alpha N^3/2 retained triples remain. For each retained triple with d extensions,

binom(d,s)/binom(N,s) = product_{i=0}^{s-1}(d-i)/(N-i) >= (alpha/4)^s.

Consequently some s-set T leaves at least rho_N N^3 residual triples, where rho_N=(alpha/2)(alpha/4)^s. Each residual triple belongs to H and every one of its pairs is adjacent in H to every vertex of T. A complete tripartite residual subhypergraph on (t,t,t) vertices therefore supplies the claimed (t,t,t,s) blow-up.

4. Sparse random obstruction. With q_N=exp(-C sqrt(log N)), fixed C>0, and u=ceil(A(log N)^(1/4)), the canonical tripartite first-moment exponent is

[3A-C A^3+o(1)](log N)^(5/4).

Choose A>sqrt(3/C). The probability of any such complete tripartite subhypergraph tends to zero, whereas q_N N^3 tends to infinity and binomial concentration gives density (1+o(1))q_N with probability tending to one. This is a valid obstruction for arbitrary tripartite hypergraphs described only by their edge density.

For an exact lower bound rho_N rather than an asymptotic density, take q_N=2rho_N (for sufficiently large s) and s=ceil(a sqrt(log N)), with fixed a>0. Then log(1/q_N)=s log(4/alpha)+log(1/alpha)=Theta(s), and concentration implies density at least rho_N with probability tending to one. The obstruction scale is O(sqrt(log N/s)). The same calculation applies for s tending to infinity with s=o(log N), where the expected edge count diverges and this obstruction scale diverges. Balancing s against this obstruction gives order (log N)^(1/3). That balance is an upper benchmark on what this density-only strategy could guarantee; no matching sparse embedding theorem is proved by this computation. Most importantly, these random residuals are NOT proved realizable as the joint links of a host with constant tetrahedron density. They are neither structured-link counterexamples nor counterexamples to the original conjecture.

5. Jensen and collisions. Successive coordinate cloning of the ell-partite indicator relation gives homomorphism count at least delta^(t^ell)N^(ell t). Each cloning applies convexity to an average of a nonnegative conditional product; repeating over ell coordinates raises the original density to t^ell. An in-class collision fixes a pair of positions, so at most ell binom(t,2)N^(ell t-1) assignments collide. Strict inequality delta^(t^ell)>ell binom(t,2)/N suffices for an injective grid. For fixed 0<delta<1 this crude sufficient condition gives t of order (log N)^(1/ell). Delta=1 is exceptional and trivially supplies an entire grid. The condition is sufficient, not necessary for injectivity. Even a hypothetical delta^(O(t^r)) bound with this same subtraction yields only the smaller scale (log N)^(1/r). These statements identify limitations of the stated calculation, not all analytic methods.

6. Uniformity and energy. The degree of K_ell^(r)(t) is exactly binom(ell-1,r-1)t^(r-1), so at the target scale it grows as log N. A fixed-degree or fixed-target embedding theorem cannot simply be substituted with a growing t without parameter control. In the 2026 graph argument, adding a vertex restricts coordinates by individual graph neighborhoods, a Cartesian box. Hypergraph links instead constrain (r-1)-tuples. Equality of binary labels on two classes gives a concrete nonrectangular pair relation and disproves the proposed single-box identity. It does not disprove decompositions into boxes or future multilevel energy methods.

## Source-specific checks

Inspected the recovered Rödl–Schacht manuscript text, especially Problem 2, Problem 3, Theorem 4, and Propositions 7 and 9, and the recovered Fox–Wigderson–Zhou v1 text, particularly the introduction and Section 7.

- Rödl–Schacht Problem 2 has the intended ell>r>2 domain. The auxiliary ell-uniform reduction explains the stronger 1/(ell-1) benchmark, distinct from the weaker OWR wording.
- Problem 3 is about triangle copies at density exp(-C sqrt(log N)), arising in the K_4^-^(3) joint-link route. Arbitrary sparse random 3-graphs do not contradict this graph-triangle question.
- Theorem 4 assumes a graph support with at least c n^3 triangles for fixed c and relative hyperedge density at least 1-beta. Route 3 supplies neither hypothesis uniformly at s of order sqrt(log N).
- The 2026 result is a graph result with coefficient proportional to sqrt(delta)/(log(1/delta))^2. Section 7 states the sufficient threshold N>=2^(C_H delta^(-11)) and explicitly says it is inadequate for the 2012 Problem 3 application. For delta=exp(-C sqrt(log N)), this threshold fails eventually: log N grows more slowly than exp(11C sqrt(log N)). Formal substitution into the coefficient yields only a constant multiple of exp(-C sqrt(log N)/2), tending to zero, after multiplication by log N.
- The stated special r-partite case is valid for nonempty fixed F: a fixed edge of F bounds its embeddings by a constant times e(H)n^(v(F)-r), forcing positive edge density. Splitting each large r-partite class into the finitely many vertex classes of F embeds F(t).
- Proposition 7 concerns the explicitly described S_r, not all cliques. Proposition 9 concerns prescribed-part tight 3-uniform paths, not arbitrary F.
- The May 2026 manuscript explicitly retains the hypergraph extension as open. This bounded recovered literature evidence is not proof that no subsequent result exists.

Public source links: https://www.math.uni-hamburg.de/home/schacht/2012/blowup.pdf and https://arxiv.org/html/2605.23301v1 .

## Accepted claim scope

Accepted: the normalized target; imported baseline exponent; elementary random upper-scale proof; exact joint-link averaging; arbitrary sparse-density obstruction with stated domains; Jensen collision audit; identified missing hypotheses; accurately scoped known positive cases; no new unconditional solution.

Not accepted as established: a new gamma for the conjectured target; an optimal sharp constant; a universal barrier to regularity or energy approaches; realizability of the arbitrary random residuals in the required dense host; a matching sparse lower bound inferred solely from balancing; exhaustive current-literature nonexistence.

All findings concern mathematical reasoning; no third-party source contents are bundled.

## Final acceptance addendum

The author incorporated the requested precision changes. Independently reread the revised Routes 3 and 4 and verified the final file SHA-256:

69dd8e2684cac0f8ff9adc48c7d60b5036062405d1465a12ecc94e63a37cea19

Final verdict: ACCEPTED within the claim scope above. No mathematical blocking defect remains. In particular, the final text explicitly bounds alpha and C, rounds the random-test size, gives A>sqrt(3/C), matches exact residual density with q_N=2rho_N, specifies the asymptotic s-domain, labels balancing as an obstruction benchmark only, and treats the Jensen test as sufficient with delta=1 separately.

## Public-copy provenance

The accepted report digest above identifies the frozen pre-sanitization report. The public ANALYSIS.md differs only in administrative wording, not mathematical content. AUDIT_RESULT.json records the separate public-copy digest. This audit likewise omits administrative permission and publication-status sentences.
