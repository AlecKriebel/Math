# Independent audit of signed fractional localization and packing conversion

Date: 2026-10-06 UTC

## Result and scope

**Section 3 is validated**, conditional on the established fixed-graph fractional-packing approximation stated in Yuster's Theorem 1.1 (also a special case of his Theorem 1.2). The signed estimates, localization parameter choices, weighted packing conversion, and passage to Theorem 1.3 all close. The disconnected template in Lemma 3.4 is permitted by the imported theorem. No correction patch, counterexample, or unresolved mathematical gap was found in this section.

This conclusion follows from the independent derivations below, rather than from a numerical spot check or the absence of an apparent defect. It covers Lemmas 3.1, 3.2, and 3.4, Theorem 3.3, and the proof of Theorem 1.3, together with the elimination-order facts they use. It does not certify the later exact integral theorem or equality classification.

## Sources actually inspected

- Obinna Okechukwu, *Clique partitions and bounded simplicial defect*, arXiv:2609.20871v1. Sections 1-3, PDF pages 1-11; equation layout on pages 8-11 was additionally checked from rendered pages. Local PDF SHA-256: `9654af66b347f47df1bc2dd807f1c1950a3afce4f4fe0ece8973fdb4d7d5fa53`.
- Raphael Yuster, *Integer and fractional packing of families of graphs*, arXiv:math/0305350v4. The definitions and Theorems 1.1-1.2 on PDF pages 1-2, the explicit quantification at the start of Section 3 on page 3, and the subgraph construction and concluding packing argument on pages 3-7 were inspected. Local PDF SHA-256: `dbe20fa983b79cae91ecc7c1cab7ec57c5d3aa017d92c1c3508623ea3ace6fbe`.

The supplied local primary documents were sufficient for this audit. The Haxell-Rodl article was not separately inspected; Yuster directly supplies the necessary statement and an independent proof. The regularity and hypergraph-matching results inside that established theorem are accepted imports, not re-proved here.

## Elimination and linear programming prerequisites

The rooted condition gives an s-defective order ending in any prescribed clique by repeatedly deleting a permitted exterior vertex. The condition is induced-hereditary, so the same operation is available in any induced remainder. If vertices are removed from a forward neighborhood, its order and clique number each drop by at most the number removed, and its order-minus-clique-number cannot increase. These observations justify every elimination-order use in Section 3. In particular, the argument never assumes closure of the graph class under arbitrary edge deletion.

For the finite clique-partition LP, edge-only variables supply a feasible primal with finite objective. Equality constraints in the primal correctly produce unrestricted signed dual variables. The K2 constraints give z_e <= 1. Dual attainment also follows directly from finite LP duality. The manuscript's alternate compactness argument is sound: let B = binom(L,2) and replace every z_e below 2-B by 2-B. If a clique constraint is affected, it contains an updated coordinate of value 2-B and at most B-1 other coordinates, each at most 1. Its new sum is therefore at most 1, even when several coordinates are updated simultaneously. Unaffected constraints stay feasible, and the objective does not decrease.

## Lemma 3.1

### Positive clique-star selection and exterior counting

Maximize the signed spoke sum over all pairs consisting of a vertex and a clique in its neighborhood, allowing the empty clique. The maximum alpha is nonnegative. Deleting zero-weight members preserves it; a negative member could not belong to a maximizing pair because deleting that member would improve the sum. Hence a maximizing clique C can have only positive chosen spokes, with 0 <= alpha <= c = |C|.

In an s-defective order ending in C, each exterior vertex has a forward clique and at most s further forward neighbors. Its positive-weight neighbors inside that clique form another clique-star and contribute at most alpha. Its positive exceptional spokes contribute at most s because every dual coordinate is at most 1. Each edge outside E(C) has exactly one earlier exterior endpoint. Thus the positive mass on those edges is at most (n-c)(alpha+s). Since positive mass equals signed mass plus negative mass, this proves the exterior estimate (3.3), including all signs.

### Triangle summation and the small-core case

Summing the triangle constraints with the selected vertex counts each edge inside C once and each chosen spoke c-1 times. Consequently

Z(E(C)) <= binom(c,2) - (c-1) alpha.

Writing d = c-alpha >= 0, combination with exterior counting gives exactly

W + N_out <= B_n(c) - (n-2c+1)d + s(n-c),

where B_n(c) = c(n-c)-binom(c,2). The identity

M_n - B_n(c) = (3/2)(c-(2n+1)/6)^2

then gives (3.4). When c <= (n+1)/2, all four terms retained on its right-hand side are nonnegative: the square, (n-2c+1)d, sc, and N_out. The empty clique causes no exception; its alpha and internal edge sum are zero.

### Large-core exclusion

For c >= (n+1)/2 and n >= 8 there are at least four vertices in C. Averaging K4 constraints bounds Z(E(C)) by binom(c,2)/6, with no assumption that its edge weights are nonnegative. The two available upper bounds after removing s(n-c) are

f(alpha) = (n-2c+1)alpha + binom(c,2),

g(alpha) = (n-c)alpha + binom(c,2)/6.

The first is nonincreasing, the second nondecreasing. Their intersection is at alpha = 5c/12, which lies in [0,c]. Therefore their minimum never exceeds the intersection value

c(5n-4c-1)/12 <= (5n-1)^2/192 <= 25n^2/192.

This proves (3.5). Its leading constant is below 1/6, while M_n >= n^2/6, so it also implies W <= M_n+sn. In the small-core case the same conclusion follows from the nonnegative right side of (3.4). Lemma 3.1 is valid.

## Lemma 3.2

This is a cover argument on the original graph H. At every vertex, exceptional forward edges are covered singly. If its forward clique has size below ceil(xi*n)+1, that clique's forward spokes require at most ceil(xi*n) single-edge parts. Otherwise divide a uniformly random ordering of that clique into groups of size at most L-1 and adjoin the current vertex.

Every edge occurs once in the part or singleton designated by its earlier endpoint. Additional occurrences can only come from vertices earlier than both endpoints. All parts are actual cliques of orders at most L, even though they overlap.

The total number of parts is bounded by

s*n + n*ceil(xi*n) + e(H)/(L-1) + n.

Using ceil(xi*n) <= xi*n+1 and e(H) <= n(n-1)/2 gives the claimed bound with (s+3)n; indeed (s+2)n is already sufficient after a coarser simplification. Thus there is slack in the manuscript's linear term.

For a fixed pair in a forward clique of size u, after the first endpoint's random position is fixed there are at most L-2 permissible positions for the other endpoint among u-1 positions. The probability of sharing a group is at most (L-2)/(u-1). In the large-clique case, u-1 >= ceil(xi*n) >= xi*n. Summing over at most n possible earlier vertices bounds the expected extra multiplicity of any edge by (L-2)/xi.

Finally, if the multiplicity is ell_e >= 1, clique feasibility yields sum_e ell_e*z_e <= number of parts. Hence

sum_e z_e <= number of parts + sum_e (ell_e-1)*(-z_e)_+.

Taking expectations proves (3.7). This is precisely the correction needed for signed weights; replacing the cover by a partition or simply discarding its overlaps would be unjustified, but the manuscript does neither. Lemma 3.2 is valid.

## Theorem 3.3

### Gap and localization radius

The large-core alternative is impossible when delta_0+eta_0 < 7/192, because 1/6-25/192 = 7/192. For the remaining alternative define rho = M_n+sn-W. Its upper bound is

rho <= (delta_0+eta_0)n^2 + n/6 + 1/24.

Once rho <= gamma*n^2 with gamma < 10^-3 and n >= 8, the square term in (3.4) gives

|c-(2n+1)/6| <= sqrt(2rho/3).

These constants imply n/4 <= c <= 5n/12. For example, sqrt(2gamma/3) < 0.026, so the upper bound is below (1/3+0.026)n+1/6 < 5n/12 for n >= 8, while the lower bound exceeds n/4. It follows that n-2c+1 >= n/6 and thus

c-alpha <= 6rho/n; also N_out <= rho.

This checks all statements in (3.8), including the denominators used later.

### Spoke deficiency and the row-edge estimate

Define the deficiency for each potential spoke xu as 1 if missing and 1-z_xu if present. These quantities are nonnegative. Their row sums are the b_x in the manuscript, and their total is B. Missing spokes therefore contribute at most B, so D_C <= B.

The exact cross-edge contribution is c(n-c)-B. Combining it with the triangle bound inside C gives

W <= B_n(c)-B+(c-1)(c-alpha)+Z(E(R)).

Since W = M_n+sn-rho and B_n(c) <= M_n,

B <= rho-sn+(c-1)(c-alpha)+Z(E(R)) <= 7rho+Z(E(R)).

The last step uses c-1 <= n and c-alpha <= 6rho/n. Applying Lemma 3.2 to the induced graph on R is legitimate. Its negative mass is bounded by N_out, hence by rho. With A_0=(L-2)/xi, this proves

B/n^2 <= xi+1/(2(L-1))+delta_0+3/n+(7+A_0)gamma.

At most 8B/c <= 32B/n rows have b_x >= c/8. Edges incident with those rows number at most 32B. For an adjacent pair of remaining rows, the sum of their spoke deficiencies is below c/4. Some core vertex therefore has paired deficiency below 1/4. Both associated spokes must exist, and their weights sum to more than 7/4. The triangle constraint forces the row-edge weight below -3/4. There are at most (4/3)rho such edges, hence certainly at most 2rho. Adding D_C <= B proves

D_C+e(R) <= 33B+2rho.

No positivity of row-edge weights is assumed, and a negative row edge is charged to the correct outside negative-mass budget.

### Order of parameter choices

There is no circular choice. First choose xi and then the fixed integer L so that 33(xi+1/(2(L-1))) < epsilon/4. This fixes A_0. Next choose gamma so that sqrt(2gamma/3) < epsilon/4, [33(7+A_0)+2]gamma < epsilon/4, and gamma < 10^-3. Then choose positive delta_0 and eta_0 with delta_0+eta_0 < min(gamma/2,7/192) and 33delta_0 < epsilon/8. Finally increase n_0 to cover n >= 8 and all three stated finite-size conditions.

The normalized bound for D_C+e(R) is then strictly below

epsilon/4 + epsilon/8 + epsilon/8 + epsilon/4 = 3epsilon/4.

The normalized error in core size is below epsilon/4 + epsilon/4 = epsilon/2. The stated conclusions follow with room to spare. Theorem 3.3 is valid.

## Imported approximation and disconnected graphs

Yuster works with finite simple graphs without isolated vertices. His Theorem 1.1 supplies, for a fixed graph J, an additive o(n^2) difference between fractional and integral edge-packing numbers. The start of his Section 3 makes the relevant uniform quantifier explicit: for fixed family and positive error there is one order threshold applying to every host graph of that order. His theorem does not require connectedness. Theorem 1.2 also allows a fixed family, but the manuscript's bundling proof only needs the singleton-family case.

Copies are non-induced. This is supported both by the subgraph definition on page 3 and by the construction on page 5, which retains only edge pairs belonging to the target graph. Thus a union of clique components in a host with extra edges between components is an allowed copy of J.

Each nonempty J used by Lemma 3.4 is a disjoint union of complete graphs of order at least three. It is finite, simple, nonempty, and has no isolated vertices, so it meets all target-graph hypotheses.

To remove the host's no-isolated-vertices convention, let m be its number of nonisolated vertices. Integral and fractional J-packings are unchanged on passing to those vertices. If m is above the imported error threshold, the error is at most epsilon*m^2 <= epsilon*n^2. If m is below that fixed threshold, its edge count is bounded by a constant, so its entire fractional packing number is O(1), which is at most epsilon*n^2 for all sufficiently large n. This establishes the manuscript's uniform (3.12) for arbitrary hosts.

## Lemma 3.4

### Weighted packing identity and quantization

Start with an optimal exact fractional clique partition. Its variables on cliques of orders at least three form a fractional edge-packing. Conversely, every such packing can be completed by giving each edge its unused capacity. If t_j is the total mass on j-cliques and w_j=binom(j,2)-1, the partition objective equals

e(G) - S, where S = sum_{j=3}^L w_j*t_j.

This identity accounts for the weights; an unweighted family-packing approximation alone would not suffice. Edge capacity gives binom(j,2)t_j <= e(G), and hence t_j <= n^2/6.

Fix alpha > 0 with alpha*sum_j w_j < zeta/4 and put a_j=floor(t_j/(alpha*n^2)). Then 0 <= a_j <= floor(1/(6alpha)), so the set of possible templates is finite, independently of the host and its order. Quantization loses

0 <= S-alpha*n^2*w_J < zeta*n^2/4,

where w_J=sum_j a_j*w_j. If every a_j vanishes, the edge-only partition already has the required error.

### Bundle extraction invariant

For any residual packing, the total mass of all its cliques containing a fixed vertex v is at most deg(v)/2 <= (n-1)/2. Each such clique consumes at least two incident edge capacities, and summing those capacities proves the assertion even when cliques have different sizes. Consequently, cliques meeting any set of at most h=|J| vertices have total mass below h*n.

After bundle mass u has been extracted, the residual mass in size j is exactly t_j-a_j*u. For each required size, a_j >= 1, and when u < alpha*n^2-h*n,

t_j-a_j*u >= a_j(alpha*n^2-u) > a_j*h*n >= h*n.

During the next bundle, at most h vertices are forbidden by components already selected. The incident-mass bound therefore ensures a positive-weight clique of each required size disjoint from all selected components. This validates the greedy component selection. There is no need to require that host edges between the components be absent.

Subtracting the minimum selected residual variable from every chosen component transfers exactly that mass to a fractional J-copy without increasing any edge load. The per-size mass invariant is preserved. Every nonfinal transfer exhausts an original clique variable, and there are finitely many such variables. Capping the final transfer at the remaining target mass therefore constructs a fractional J-packing of mass alpha*n^2-h*n. The target is positive once n > h/alpha.

### Rounding loss and uniformity

Apply the imported theorem for this fixed J with additive error zeta*n^2/(4w_J). Expanding the resulting integral J-copies into their clique components yields edge-disjoint cliques whose total saving is at least

w_J*alpha*n^2 - w_J*h*n - zeta*n^2/4.

For n >= 2w_J*h/zeta, the middle loss is at most zeta*n^2/2. Together with quantization, the overall saving loss is less than zeta*n^2. Filling unused edges singly gives q_L(G) <= q_L^*(G)+zeta*n^2.

Take the maximum over the finitely many nonempty templates of their imported theorem thresholds, their h/alpha thresholds, and their 2w_J*h/zeta thresholds. This produces a single host-independent order threshold. Although the selected J can vary between input graphs, it varies only inside that fixed finite collection. No varying-pattern approximation theorem is being assumed. Lemma 3.4 is valid.

## Passage to Theorem 1.3

For each desired structural accuracy epsilon, Theorem 3.3 first fixes L, delta_0, and eta_0. Lemma 3.4 is then applied with this L and error eta_0/2. Since cp(G) <= q_L(G),

q_L^*(G) >= cp(G) - (eta_0/2)n^2.

The sequence hypothesis cp(G_j) >= n_j^2/6-o(n_j^2) eventually supplies the other eta_0/2 of error, and rsd(G_j)=o(n_j) eventually supplies the defect threshold. This establishes the hypotheses of Theorem 3.3 without ever sending L to infinity inside the rounding theorem.

For every graph, minimize over its finitely many cliques the maximum of the normalized core-size and structural errors. For every fixed epsilon these minima are eventually at most epsilon, so the minima converge to zero. Choosing an attaining clique in each graph yields exactly the sequence required in Theorem 1.3.

For the all-graph bound (1.5), one can make the unspecified uniform function explicit as

epsilon(n) = max_{|G|=n} [q_4(G)-q_4^*(G)]/n^2.

This finite maximum is nonnegative and tends to zero by Lemma 3.4. Lemma 3.1 and cp <= q_4 then give (1.5) for every n >= 8, including the finitely many small orders outside any chosen asymptotic threshold.

## Final disposition

All inequalities and all parameter transitions in Section 3 have been checked. The potentially delicate issues are resolved by arguments present in the manuscript: repeated negative cover weights are charged; weighted savings are bundled before rounding; disconnected non-induced templates meet the imported theorem; isolated host vertices are harmless; and the family of templates is fixed and finite before its thresholds are maximized. The signed fractional localization and the fractional-to-integral bridge can be accepted as inputs to the audit of Sections 4-6.
