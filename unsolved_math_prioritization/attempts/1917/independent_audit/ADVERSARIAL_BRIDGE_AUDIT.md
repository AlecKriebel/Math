# Adversarial audit of the bounded exceptional set and exact rigidity bridge

Date: 2026-10-06 UTC

## Conclusion

**Lemma 5.1 and Proposition 5.4 are validated.** I read their complete proofs afresh, together with Lemmas 2.3, 4.2, 4.3, 5.2, and 5.3 where their hypotheses matter. I found no quantifier, matching, capacity, or asymptotic-to-exact gap. This is a focused validation of those two bridges, not an independent certification of every result in the manuscript.

The source is Okechukwu arXiv:2609.20871v1, PDF pages 12-19, with the structural obstruction on page 5. PDF SHA-256: `9654af66b347f47df1bc2dd807f1c1950a3afce4f4fe0ece8973fdb4d7d5fa53`. The notation and displayed formulas on page 18 were checked against a rendered PDF page.

## Lemma 5.1

### The first matching really is bounded

After discarding the deficient core columns, each remaining core vertex misses at most rho*n/4 exterior vertices. Each row in Y_0 has exterior degree at least rho*n. Therefore a missing pair between these two sets has at least 3rho*n/4 common exterior neighbors, and the weaker rho*n/2 bound used in the proof is safe.

For ell = ceil(4(s+1)/rho) disjoint missing pairs, summing their witness incidences gives at least 2(s+1)n. If M witnesses see at least s+1 pairs, the incidence sum is at most s*n+ell*M. Consequently M >= (s+2)n/ell, which is stronger than the stated n/ell. One fixed choice of s+1 pairs has at least n/[ell*binom(ell,s+1)] common neighbors. This is a positive linear fraction for fixed s. Its induced chromatic number is at most omega(G[R_0])+s=o(n), so its independence number tends to infinity and eventually exceeds s+1. The forbidden configuration in Lemma 2.3 results.

No endpoint-disjointness is lost: the pairs belong to a matching, and a common neighbor cannot equal a row endpoint because that would require a loop. The core endpoints are outside R_0.

The use of a maximal matching afterward is sufficient. Its endpoints cover every nonedge of the bipartite nonedge graph; otherwise another edge could be added. Since every matching already has fewer than ell edges, this maximal matching also has fewer than ell edges. Deleting its row endpoints and moving its core endpoints therefore makes every retained Y_0 row complete to the retained core. A maximum matching is unnecessary.

### Promotion and the second matching

Moving fewer than ell old core vertices changes exterior degrees by O_s(1) and exterior edge count by O_s(n). Thus an originally low-degree row still has degree below rho*n+O_s(1). This is much smaller than the threshold |R_1|-lambda*n = (2/3-lambda)n+o(n). Every promoted row in U is consequently complete to A_1. Sparsity gives |U|=o(n).

Each A_1 vertex misses at most rho*n/4 <= lambda*n vertices of R_1. Each U vertex misses fewer than lambda*n, with its own vertex counted as a miss. A hypothetical matching of s+1 nonedges in A_1 union U has at least

|R_1|-(2s+2)lambda*n = (2/3-1/50)n+o(n)

common row neighbors. The same chromatic argument again gives the forbidden independent witnesses. Thus a maximal complement matching has at most s edges, and its at most 2s endpoints cover all remaining nonedges. Removing those endpoints leaves an actual clique.

The resulting C, R, T are disjoint and exhaustive. In particular, endpoints removed from the promoted core go to T, not back into R, so no high-degree exceptional row is inadvertently reintroduced. The explicit uniform bound is

|T| <= ceil(4(s+1)/rho)-1+2s = 40000(s+1)^2-1+2s.

The bound depends only on s. The index from which the construction works may depend on the sequence's error rates, as the lemma permits.

### Final degree and deficiency bounds

A retained low-degree row has at most rho*n+O_s(1) neighbors outside A_1 union T_1. Minimum degree n/3-o(n), together with |A_1|=n/3+o(n), therefore bounds its missing core neighbors by rho*n+o(n). All other retained rows are complete to A_1. Adding o(n) promoted core vertices gives sigma <= 2rho*n eventually. Every retained core column already misses at most lambda*n rows, giving tau <= lambda*n. Finally, a row outside U has degree at most |R_1|-lambda*n; deleting |U|=o(n) rows implies Delta(G[R]) <= |R|-lambda*n/2. These are genuine eventual inequalities, and all three have sufficient fixed slack.

## Proposition 5.4

### Capacity for the initial exceptional-vertex estimate

The bounded size of T permits passage to a constant t and convergence of every exceptional profile. The ordinary row graph has the asserted coloring because its degeneracy is at most omega+s-1; the chosen palette Delta+omega+s has an extra spare color.

For the first application of Lemma 4.3, the normalized gap between the upper capacity 2(c-2(sigma+t)) and k is at least lambda/2-8rho-o(1), which is positive. The other capacity has normalized slack at least 1/6-4lambda-o(1), also positive. The facts that t is bounded, m=o(n^2), and k >= c = n/3+o(n) imply ceil(m/k)=o(n), so the ceiling term is harmless.

The matching construction in Lemma 4.3 supports this use. Maximizing total matching size makes each individual matching maximum after other matchings' cross edges are removed. A rectangle of unmatched vertices contains no available edge; deleted edges in that rectangle number at most t*L_x, giving L_x^2-t*L_x <= D. Each vertex loses at most t cross edges. The numerical error is bounded by 4t^2, which vanishes after division by n. This argument does not require compatibility with the later, fresh construction.

The difference Q_s(n)-M_(n-t) is (s+t)n/3+O_s,t(1), so comparison with (4.8) gives precisely the profile lower bound sum |y_i-x_i| >= s+t.

### The exceptional incidence bound has the correct quantifiers

For an index with x_i<1, the number of missing core neighbors is a fixed positive linear fraction along the chosen convergent subsequence. Because the index set I is finite, one positive lower coefficient works for all its members eventually.

The displayed choice is eta_n=sqrt(D/n^2)+n^(-1/2). It tends to zero and is positive, while

D/(eta_n*n) <= sqrt(D/n^2)*n = o(n).

Removing that many deficient rows leaves maximum row deficiency o(n), and its row clique number remains o(n). Lemma 5.2 therefore applies to X=I for sufficiently large indices. Its rooted-order proof counts every X-row edge at the earlier endpoint: a deleted row has at most s later X-neighbors, and a deleted exceptional vertex has at most s+w later row-neighbors. Restoring the removed rows costs at most |I|o(n)=o(n), not o(n^2), because |I| is bounded. Hence the normalization by n/3 legitimately gives sum_{i in I} y_i <= 2s.

Lemma 5.3 then forces equality in each finite optimization step: exactly s profiles are (0,2), and all others are (1,0) or (1,2). It yields uniform o(n) errors over these bounded sets.

### The enlarged clique is exact

A nonedge in C union Z would be disjoint from X. For each of the s vertices of X, its o(n) core neighborhood leaves n/3-o(n) choices of a missed vertex in C. Avoiding the first two endpoints and the boundedly many prior choices produces s more disjoint nonedges.

Their endpoints have at least b-(s+2)lambda*n-o(n) common neighbors in R, a positive linear number since (s+2)lambda <= 1/50. At most s+2 endpoints are old core vertices; all other endpoints have o(n) missing row neighbors by their profiles. The induced chromatic bound again supplies s+2 independent witnesses. This contradiction proves that C union Z is a clique for every sufficiently large index. It also covers s=0 directly.

### The final construction starts with the original graph

The new cut is C'=C union Z union X and R'=R union P. No cross edges removed in the preliminary proof of (4.8) are removed here. Lemma 4.2 explicitly allows a noncomplete core, so applying it to C' is legitimate.

Old rows have core deficiency at most 2rho*n+O_s(1); added P rows have deficiency o(n). Old core columns miss at most lambda*n+O_s(1) new rows, while X and Z miss o(n). Thus the new sigma' and tau' bounds follow. Old row degrees increase by only |P|, whereas new P rows have o(n) row degree. This gives the claimed Delta bound with lambda*n/3 of slack. Also m'=o(n^2) and omega(G[R']) <= omega(G[R])+|P|=o(n).

For the final palette, the first capacity has normalized gap at least lambda/3-8rho-o(1)>0. The second again has gap at least 1/6-4lambda-o(1)>0. Therefore both exact finite hypotheses of Lemma 4.2 hold eventually, and theta=2(c'-2sigma')/k'-1 is strictly positive.

### No asymptotic loss survives in (5.11)

At this stage the only use of limiting profiles was to guarantee exact clique structure and strict finite capacity conditions. Lemma 4.2 now supplies an exact partition inequality. The actual clique C' minus X has order c'-s, so the actual core edge count is at least binom(c'-s,2), with no error term. Consequently

cp(G) <= c'(n-c')-binom(c'-s,2)-D'-theta*m' <= Q_s(n)-D'-theta*m'.

The last inequality is the exact integer maximum of the quadratic, not an asymptotic approximation. The assumption cp(G) >= Q_s(n), together with D',m' >= 0 and theta>0, forces D'=m'=0. Equality in the core-edge estimate leaves exactly the edges of C' minus X, so X is isolated inside the core. Equality in the quadratic forces precisely the specified nearest-integer core sizes. This proves the required extremal form on the extracted subsequence and contradicts its choice.

There is no illegitimate interchange of quantifiers. If infinitely many members failed the proposition, bounded t and compactness would produce the particular convergent subsequence just audited. Each needed eventual inequality holds on that subsequence, yielding the contradiction. No convergence rate uniform over all original sequences is assumed.
