# PASS1 geometry and one-dimensional endpoint audit

Authored mathematical audit, 14 October 2026 UTC. This document treats geometry independently of the probability argument except where it explicitly identifies the quadrant-survival input. It follows the source-faithful acceptance contract.

**Public-edition version note.** Section 8 retains a historical cross-check of an earlier boundary-tracing presentation. The accepted survival argument is the parity proof in the final construction and probability reports. The [independent acceptance audit](../pass1_audit/INDEPENDENT_ACCEPTANCE.md) explicitly supersedes that earlier presentation and separately checks the geometry, gadget, endpoint, and optional strengthening results. Original and public identities are recorded in [the identity file](../ORIGINAL_IDENTITIES.json).

## 1. Verdict for the canonical graph

Let A = {(x,y) in Z² : x >= 1 and y >= 1}, B = {(x,y) in Z² : x <= -1 and y <= -1}. A lattice edge is **strong** precisely when both endpoints belong to A or both belong to B. Leave strong edges unchanged. Replace every other lattice edge by a path of length L = 100, using new internal vertices that belong to no other replacement path. Call the resulting graph G.

This graph is infinite, countable, connected, undirected and simple. Its maximum degree is exactly 4. It is quasi-isometric to Z² with the single constant C = 100 in the source's stated convention. It is also planar and one-ended. Thus neither its number of ends nor the absence of parallel edges defeats the proposed construction.

The iid bond reduction is exact: at actual parameter p, strong lattice bonds have effective probability p, weak lattice bonds have effective probability p^100, all effective bonds are mutually independent, and the number of infinite clusters is preserved. The inhomogeneity occurs only after reduction; the process on G uses one common probability p.

## 2. Uniform subdivision lemma with explicit constants

Let H be any connected simple graph of maximum degree Delta, and assign an integer length ell(e) with 1 <= ell(e) <= L to each edge e. Replace each edge by a path of that length. Distinct paths have disjoint internal vertices and share only their original endpoints. Denote the resulting graph by S.

### Graph properties

Every original vertex retains its degree in H. Every new vertex has degree 2. No loop arises because the original endpoints are distinct; no multiple edge arises because H is simple and new vertices are private to their paths. Thus S is simple and has maximum degree max(Delta,2), with equality Delta whenever Delta >= 2. Connectedness and countability are immediate. Infinitude follows because H is infinite.

### Metric map

For an original vertex x, let f(x)=x. On each replacement path, map an internal vertex to its nearer original endpoint; ties can be decided separately for each path.

For adjacent vertices x,y of S, their images either coincide or are endpoints of the same H-edge. Therefore f is 1-Lipschitz:

    d_H(f(x),f(y)) <= d_S(x,y).

For original vertices u,v, expand an H-geodesic to obtain

    d_S(u,v) <= L d_H(u,v).

Every vertex x is at S-distance at most floor(L/2) from f(x). Consequently, for arbitrary x,y,

    d_H(f(x),f(y)) <= d_S(x,y)
      <= L d_H(f(x),f(y)) + 2 floor(L/2)
      <= L d_H(f(x),f(y)) + L.

The map f is surjective. Taking C=L gives exactly the source's required pair of inequalities and coarse-surjectivity condition. For the canonical graph, L=100 and C=100. Using arbitrary rather than nearest endpoints gives a weaker additive constant 2(L-1); nearest endpoints avoid that unnecessary loss.

### Topology and ends

Subdividing edges does not alter the topological realization of a graph. In particular, G remains planar when H=Z².

Here is also a direct end argument, requiring no general quasi-isometry theorem. Given a finite vertex set F in S, only finitely many replacement paths meet F. Put all endpoints of those paths into a finite set T in H. For H=Z^d, d>=2, choose a box containing T. The lattice outside a sufficiently large box is connected, and all replacements of edges wholly outside that box avoid F. They therefore form one infinite connected component of S\F. Every other infinite component would need infinitely many original vertices, and hence original vertices outside the box, so would meet that same exterior component. Thus S has one end.

The one-ended conclusion does not assert uniqueness of open clusters: finite percolation clusters of closed edges need not form a deterministic finite separator.

## 3. Exact independent-bond and cluster transfer

At bond parameter p on S, declare an H-edge e effectively open exactly when every edge of its replacement path is open. This has probability p^ell(e). Replacement paths have pairwise disjoint edge sets, so these indicators are mutually independent, even though adjacent gadgets share original vertices.

Two original vertices are connected in the open subgraph of S if and only if they are connected by effectively open edges in H. In one direction expand an effective path. Conversely, an open simple path between original vertices can pass through the interior of a replacement path only by continuing to the other endpoint; its compression is an effective-edge path.

Every infinite open cluster of S contains infinitely many original vertices. Indeed, a cluster with no original vertex lies within one finite replacement path. A cluster meeting a finite set of original vertices is contained in that finite set and the finitely many finite paths incident to it. It is therefore finite. This argument uses local finiteness; bounded replacement lengths are not needed for this particular assertion.

It follows that infinite open clusters in S and in the effective percolation on H correspond bijectively. In particular their counts N_infinity agree for every configuration, not merely almost surely.

## 4. Bridge extraction and opposite-orthant geometry

This section isolates the deterministic ingredients of the probability argument. It applies in every dimension d>=2.

Let

    A_K = {x in Z^d : x_i >= K for every i},
    B_K = {x in Z^d : x_i <= -K for every i},

where K>=1. Call an edge strong if it is internal to A_K or internal to B_K, and weak otherwise.

### Bridge extraction

If an effective open path joins A_K to B_K, truncate it at its first visit to B_K, then start it at its last visit to A_K before that time. The resulting finite path has its first vertex in A_K, last vertex in B_K, and every intermediate vertex outside A_K union B_K. Every edge of that subpath is weak. Loop erasure makes it self-avoiding without introducing an edge or changing its endpoints.

Thus absence of an all-weak open bridge from A_K to B_K forbids every open connection between these regions, regardless of how many strong excursions an originally proposed path makes. It is unnecessary to control the number of strong excursions.

### Exact distance formula

For u=K(1,...,1)+a in A_K, where a_i>=0,

    dist_Zd(u,B_K) = 2dK + |a|_1.

The lower bound follows coordinate by coordinate, since reaching B_K requires decreasing coordinate i by at least 2K+a_i. Equality is achieved by monotone moves to (-K,...,-K).

If every weak effective edge has probability q and r=(2d-1)q<1, the number of self-avoiding lattice paths of length n starting at a fixed u is at most 2d(2d-1)^(n-1). Union bounding over every vertex of A_K, not just its boundary, gives the convenient bound

    P(exists an all-weak open bridge A_K -> B_K)
      <= [2d/(2d-1)] r^(2dK) / (1-r)^(d+1).

To see the final denominator, sum r^n over n>=2dK+|a|_1 and then use

    sum_{a in N_0^d} r^|a|_1 = (1-r)^(-d).

Counting all self-avoiding paths, even ones containing strong edges, is legitimate here: each counted event is restricted to a path whose every edge is weak. Only such paths receive probability q^n. One must not use q^n for arbitrary mixed paths.

When K=1 and r<=1/4, the displayed bound is at most 1/81 for every d>=2, because

    [2d/(2d-1)] r^(2d)/(1-r)^(d+1)
      <= (16/9) (1/12)^d <= 1/81.

The bound may be sharpened by summing only exit-boundary vertices, but that is optional.

### Independence relevant to the nonuniqueness event

The event that A_K contains an infinite cluster using only its internal strong edges depends solely on those strong-edge gadget bonds. The analogous B_K event uses a disjoint set of bonds. The no-weak-bridge event depends solely on weak-edge gadget bonds. Hence all three events are independent. Positive survival probabilities in the two regions and a weak-bridge bound strictly below 1 therefore imply a strictly positive probability of at least two infinite clusters.

No transitive cluster-count theorem is used here. The argument proves N_infinity >= 2 with positive probability, not a deterministic value of N_infinity.

## 5. Additive-only realization is also possible

The canonical construction only needs the source's quasi-isometry convention. Nevertheless, the stronger additive-only convention does not rescue the proposed uniqueness statement.

Retain every edge of H=Z^d. For each selected strong edge {u,v}, add M paths u--w_{e,j}--v of length two, j=1,...,M. All the new vertices are distinct. Add no such vertices on weak edges. Call this graph P.

### Graph and metric properties

P is simple: no two added paths have the same internal vertex, and all new edges have one new endpoint. There is only one original direct edge {u,v}; the additional paths are not parallel edges in the graph-theoretic sense. Its maximum degree is at most 2d(M+1), and all new vertices have degree 2. The original lattice is a spanning skeleton on the original vertices, so P is connected and countable.

Map each new vertex to either original endpoint of its length-two path and fix every original vertex. This map is edge-1-Lipschitz, and every new vertex is adjacent to its image. Original lattice vertices are isometric in P: their original lattice paths still exist, while the 1-Lipschitz projection forbids a shortcut. Hence for all x,y in P,

    d_Zd(f(x),f(y)) <= d_P(x,y) <= d_Zd(f(x),f(y)) + 2.

This is a surjective additive-only rough isometry with error 2. The same finite-gadget argument proves one-endedness for d>=2. In d=2 one can embed the finitely many two-edge paths in a narrow strip around each lattice edge, preserving planarity; this observation is not needed for acceptance.

### Exact iid transfer

A weak effective edge is open with probability p. A strong effective edge is open if the original direct bond is open or at least one of the M two-edge paths is completely open. Thus

    q_strong(p) = 1 - (1-p)(1-p²)^M.

Different gadgets have disjoint bond sets, so the effective indicators are independent. The infinite-cluster correspondence from Section 3 applies verbatim.

### Explicit constants for all d>=2

Take strong regions A_1 and B_1 from Section 4, and choose

    p = 1/(8d),      p0 = 1/(16d),      M = 1024d².

Then

    q_strong(p0)
      = 1 - (1-p0)(1-p0²)^M
      >= 1 - exp(-M p0²)
      = 1 - exp(-4)
      > 15/16 > 9/10.

The inequality exp(4)>16 follows already from exp(1)>2. At p0 each strong orthant contains a coordinate copy of the quarter-plane with independent edge probability above 9/10. Once the elementary quarter-plane survival lemma is established, this gives p_c(P)<=p0<p.

At p, the weak-edge parameter is p itself and r=(2d-1)/(8d)<1/4, so the bridge probability is at most 1/81. The two strong-region survival events and the no-bridge event are independent. Consequently this additive-only graph also has positive-probability nonuniqueness at a strictly supercritical p. Its degree bound is 2d(1024d²+1).

This is an optional strengthened realization. It is supplementary; the canonical acceptance claim uses the low-degree subdivision graph. Its quarter-plane survival input is proved in the companion `pass1_probability/PROBABILITY_AUDIT.md`, independently checked as recorded in Section 8 below.

## 6. Complete d=1 endpoint: p_c=1 without transitivity

### Theorem

If G is a connected bounded-degree graph quasi-isometric to Z, then every Bernoulli-p bond cluster is finite almost surely for every fixed p<1. Consequently p_c(G)=1, and the all-parameter at-most-one statement holds: there are no infinite clusters for p<1 and exactly one at p=1. The strict supercritical range p_c<p<=1 is empty for such G.

### Proof

Choose a source-convention quasi-isometry f:V(G)->Z with constant C>0:

    C^(-1)|f(x)-f(y)| - C <= d_G(x,y)
      <= C|f(x)-f(y)| + C.

Increasing C if necessary, assume C>=1. Let

    D = ceil(C(C+1)).

If x and y are adjacent, the lower inequality implies |f(x)-f(y)|<=D.

Every finite coordinate band f^(-1)([a,b]) is finite. If nonempty, choose x in it. The upper quasi-isometry inequality puts the whole band inside the G-ball centered at x of radius ceil(C(b-a)+C), which is finite by bounded degree.

For an integer t define the edge cut

    E_t = {{x,y} in E(G): f(x)<=t<f(y) or f(y)<=t<f(x)}.

Every endpoint of an edge in E_t lies in f^(-1)([t-D,t+D]). The upper quasi-isometry inequality bounds the diameter of this band by 2CD+C, independent of t. Since the maximum degree Delta is finite, there is a finite constant B bounding the size of every such band. For example, a ball-size upper bound at radius R=ceil(2CD+C) gives

    B <= 1 + Delta sum_{j=0}^{R-1}(Delta-1)^j

when Delta>=2. Therefore |E_t|<=M_*:=Delta B uniformly in t.

Take levels t_k=k(D+1), k in Z. The edge sets E_{t_k} are pairwise disjoint: an edge whose endpoints differ by at most D cannot cross two thresholds separated by D+1. Under Bernoulli-p bond percolation the events

    F_k = {every edge of E_{t_k} is closed}

are independent, and

    P(F_k) = (1-p)^|E_{t_k}| >= (1-p)^M_* > 0

for p<1. An empty cut, if one occurs, has F_k certain and causes no difficulty. By independence, there are almost surely infinitely many k>0 with F_k and infinitely many k<0 with F_k. This conclusion can be obtained directly from the product bound (1-(1-p)^M_*)^n -> 0, or from the independent Borel-Cantelli lemma.

On this probability-one event, fix any vertex v. Choose closed cuts with thresholds t_a<f(v)<=t_b, one on each side. An open path from v cannot cross either cut. Thus its entire open cluster lies in

    f^(-1)({t_a+1,...,t_b}),

a finite coordinate band. This holds simultaneously for all vertices on the same event. Hence no infinite cluster exists at p<1. At p=1, every edge is open and G is infinite and connected, so it is the unique infinite cluster. This proves the theorem.

No invariance, transitivity, stationarity, mass-transport argument, or uniqueness-monotonicity theorem is used.

## 7. Failure modes checked

1. **Unbounded subdivision lengths:** these can destroy the uniform metric estimate. The canonical construction uses one fixed length 100; the optional additive construction has length two and fixed finite M.
2. **Graph-theoretic parallel edges:** not allowed by the source. Private length-two paths give a simple graph; literal multiple edges do not.
3. **Effective inhomogeneity:** it must arise from iid bonds on actual finite gadgets. It is not itself the source model until the exact transfer has been stated.
4. **Independent high and low events:** needed if multiplying probabilities. Their bond supports are disjoint in these constructions.
5. **Strong excursions in a crossing path:** last-A/first-B extraction gives an entirely weak bridge and resolves this issue.
6. **Uniform-width barrier:** infinitely many independent crossings can destroy separation. Opposite orthants have distance growing with every coordinate of the starting point, giving a summable crossing bound.
7. **Extraneous coordinates:** taking a two-dimensional construction times Z^(d-2) without modifying the barrier gives infinitely many extra crossing opportunities. Use full d-dimensional opposite orthants instead.
8. **Finite-cluster branches inside gadgets:** they do not create additional infinite clusters; the exact correspondence handles them.
9. **One-endedness or planarity:** neither supplies a uniqueness theorem without its other hypotheses. Both survive the canonical graph.
10. **Strict supercriticality:** existence at the target p alone only gives p_c<=p. Establish survival separately at p0<p.
11. **Claiming exactly two clusters:** unnecessary and not supplied by the bridge argument. Positive probability of at least two is sufficient.
12. **Dimension one:** the theorem above settles the endpoint; it must not be silently omitted when stating the all-dimensional conclusion.

## 8. Cross-audit of probability and final status

The companion `pass1_probability/PROBABILITY_AUDIT.md` was independently inspected after the geometric lemmas above were completed. Its deterministic quarter-plane dual-cut argument is valid: the outer boundary of the finite union of vertex-centered squares supplies a walk from the left line to the bottom line; last-left/first-bottom extraction removes all exterior-line portions, and loop erasure gives a simple dual arc. Repeated boundary vertices and corner contacts do not invalidate this extraction. Every retained edge crosses a closed primal cluster-boundary bond. The deliberately loose count of at most 4n*3^(n-1) candidate length-n paths is sufficient and yields survival at least 143/245 when p=9/10.

The companion's last-A/first-B extraction, weak-path count, and independence of the three infinite-event sigma-fields also pass this audit. Its claimed positive lower bound for nonuniqueness needs no deterministic cluster-count theorem. Together these establish the canonical counterexample, conditional only on the problem's stated graph/model scope, rather than on an additional percolation theorem.

An optional subdivision-only extension to every d>=2 uses full opposite orthants and length L_d=80d for weak edges. Since (19/20)^20<1/2, q=(19/20)^(80d)<2^(-4d). Thus r=(2d-1)q<1/4 (using 2^(4d)>8d), and Section 4 bounds bridge probability by 1/81. Each orthant contains a strong coordinate quadrant, so p_c<=9/10<19/20; maximum degree is 2d and the metric constant is 80d. This extension is not needed to refute the universal target, but confirms there is no restriction to dimension two.

The canonical geometry, iid transfer, and companion probability argument have no remaining gap identified in this audit. The d=1 theorem is complete. The additive-only realization has explicit parameters and is also complete upon inserting the independently audited quarter-plane lemma. This document makes no literature novelty claim and copies no third-party source text.
