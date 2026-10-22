# A published refutation of the 2014 induced-biclique conjecture

## Result and attribution

The revised conjecture in Noga Alon's problem-session contribution to
*Combinatorics*, Oberwolfach Reports 11 (2014), printed page 80, is false.
Its negation follows from Theorem 1.1 of Noga Alon, Tom Bohman and Hao Huang,
*More on the bipartite decomposition of random graphs*, Journal of Graph Theory
84 (2017), 45–52, DOI [10.1002/jgt.22010](https://doi.org/10.1002/jgt.22010).
The result was already in their [September 2014 preprint](https://arxiv.org/abs/1409.6165).
This is a credited consequence of a published theorem, not a new solution or
a priority claim.

The primary question is in the [OWR report](https://ems.press/journals/owr/articles/12861).
An [author-hosted PDF](https://web.math.princeton.edu/~nalon/PDFS/biclique4.pdf)
of the resolving paper gives the needed theorem on its page 2 and completes
its proof on page 6.

## Definitions and exact target

Let G be a finite simple graph on n vertices. Write bp(G) for the smallest
number of complete bipartite subgraphs whose edge sets form a partition of
E(G). Both sides of each counted biclique are nonempty; stars and single
edges are permitted. The partition bicliques need not be induced: extra
edges within their vertex sets belong to other pieces. Vertices may occur in
multiple pieces. This is neither an edge cover allowing overlaps nor a
partition of the vertex set.

Let beta(G) be the largest a+b for which G has an induced K_(a,b), with
a,b >= 1. In this separate parameter, every edge across the two sides is
present and all within-side edges are absent. For an edgeless graph set
beta(G)=0. Empty-side conventions do not affect the probabilistic argument
below, which also bounds independent induced subgraphs.

Let G_n=G(n,1/2): the vertex set is [n] and each unordered pair is an edge
independently with probability 1/2. “With high probability” means that the
probability tends to one as the integer n tends to infinity, with no
subsequence restriction. The conjecture asks whether

    P(bp(G_n) = n - beta(G_n) + 1) -> 1.

We prove instead

    P(bp(G_n) < n - beta(G_n) + 1) -> 1.

The ordinary deterministic upper bound bp(G) <= n-beta(G)+1 explains the
question: partition the edges inside a largest induced biclique using that
one biclique, and process the vertices outside it in any order, assigning
each remaining edge to its first outside endpoint. At most one star is
needed for each outside vertex. Empty stars are omitted.
The edgeless case is immediate from bp(G)=0 and the stated convention.

## Lemma: an upper bound for induced complete bipartite order

For every fixed epsilon>0,

    P(beta(G_n) < (2+epsilon) log_2 n) -> 1.

Proof. Put L=log_2 n and k=ceil((2+epsilon)L). For sufficiently large n,
2 <= k <= n. A fixed k-element set S, together with a division of S into
two specified sides, specifies the status of all binomial(k,2) edges of
G_n[S]. The probability of exactly this induced complete bipartite graph
is 2^(-binomial(k,2)). There are fewer than 2^k possible divisions, even
if ordered sides or empty sides are allowed. Thus a union bound gives

    P(some k-set induces a complete bipartite graph)
      <= binomial(n,k) 2^k 2^(-k(k-1)/2)
      <= 2^[k(L + 3/2 - k/2)]
      <= 2^[k(3/2 - epsilon L/2)] -> 0.

If beta(G_n)>=k, an induced complete bipartite graph of order at least k
contains an induced complete bipartite graph on exactly k vertices with
both sides nonempty: keep one vertex from each side and choose any k-2
of the remaining vertices. Hence beta(G_n)<k with probability tending to
one. Since beta(G_n) is integral, beta(G_n)<=k-1<(2+epsilon)L. QED.

For a check on the counting convention, the exact expected number of
k-subsets inducing a complete bipartite graph with nonempty sides is

    binomial(n,k) (2^(k-1)-1) 2^(-binomial(k,2)),  k>=2.

The tighter formula is unnecessary for the proof. There is one graph for
each unordered nontrivial bipartition because K_(a,b) is connected and its
bipartition is unique up to reversal.

## Published input and the full negative conclusion

Alon–Bohman–Huang Theorem 1.1 supplies a fixed absolute c>0 such that

    bp(G_n) <= n-(2+2c)log_2 n

with probability tending to one. Their notation in the 2014 arXiv version
is bc; that paper defines it as an edge partition, not an overlapping
cover. The author-hosted later version uses bp.

Apply the lemma with epsilon=c. With probability tending to one, both
inequalities hold, since the probability that either fails tends to zero.
On that intersection,

    (n-beta(G_n)+1) - bp(G_n)
       >= (2+2c)L - beta(G_n) + 1
       > cL + 1 > 0.

This proves the stated strict inequality with high probability. In
particular the conjectured equality has probability tending to zero.
It also shows a logarithmically growing separation from that proposed
value. No sharp estimate of beta, independence-number concentration,
chromatic-number estimate, or independence between the two good events
is required.

## Scope limits

The argument settles the revised equality for the fixed model G(n,1/2).
It does not determine the correct second-order value of bp(G_n), does not
prove bp(G_n)=n-Theta(log n), and does not provide an exact finite-n formula.
It does not transfer to fixed p!=1/2 or to a varying sparse p without new
arguments. For p!=1/2 the probability of a specified induced K_(a,b)
depends on a and b, so the lemma's equiprobable-pattern calculation changes.

Alpha(G), the independence number, motivated older star bounds; beta(G)
here is not alpha(G), the chromatic number, a biclique cover number, or the
largest non-induced biclique. The proof deliberately uses the logarithmic
form of the published theorem to avoid conflating these parameters.

The exact UnsolvedMath web page was not readable during retrieval. Its
public OWR audit record keyed OWR-12861-019 was recovered and gives this
same formulation; the descriptor joins that code and title to ID 30002468.
The audit record is editorial and explicitly says its source was not
checked. We therefore checked the primary PDF independently. The raw
prior AI report remains uninspected. These distinctions are retained in
SOURCE_VERIFICATION.json.
