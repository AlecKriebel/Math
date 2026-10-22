# Independent audit of the integral proof and exact rigidity

## Conclusion and scope

The main proof in Sections 1–5 of Obinna Okechukwu, *Clique partitions and bounded simplicial defect*, [arXiv:2609.20871v1](https://arxiv.org/abs/2609.20871v1), validates Theorem 1.1 and Corollary 1.2 under the ordinary use of established mathematical theorems. This assessment is based on the derivations below and the separate signed-fractional audit, including the actual construction that removes the approximation error. It is not an inference from the abstract or from a successful finite program.

All graphs below are finite, simple, and undirected. A clique partition partitions edges exactly once; cliques need not be maximal. Isolated vertices add no parts. Let F(n)=floor(n(n+1)/6), Q_s(n)=F(n+s)-binom(s+1,2), and M(n)=(2n+1)^2/24. The defect parameter s is fixed in Section 5. The manuscript's exact all-order conjecture in Section 7 is outside the accepted theorem.

## Section 2 and the structural prerequisites

### Rooted elimination and the chordal bridge

The hereditary rooted condition permits successive deletion outside a chosen clique. Every remainder is induced, so the condition remains available until only that clique remains. Conversely, the first exterior vertex of an order ending in the root has the required deficiency. If all s-simplicial vertices of a noncomplete induced graph formed a clique, that proper clique would violate the rooted condition. Thus there are two nonadjacent such vertices. Conversely a clique cannot contain both members of a nonadjacent pair. A complete induced graph presents no problem because every vertex is simplicial. The empty root is permitted; the empty graph has no proper root to check.

For any induced H, one of its vertices has degree at most omega(H)+s-1; repeating this proves degeneracy and chi(H)<=omega(H)+s. Restricting an elimination order to an induced vertex set is safe: deleting r neighbors reduces neighborhood order by r and clique number by at most r, so deficiency cannot increase. None of these arguments asserts preservation under edge deletion.

Here is an independent proof of the exact classical fact needed to identify s=0, so the identification does not hinge on access to Dirac's original paywalled article. Every noncomplete chordal graph has two nonadjacent simplicial vertices. Prove this by induction on its order. If disconnected, choose a simplicial vertex in each of two components, using induction or the completeness of a component. If connected and not complete, choose nonadjacent a,b and an inclusion-minimal a-b vertex separator S. Let A and B be the components of a and b in G-S. Each member of S has a neighbor in both A and B: deleting that member from the separator must allow an a-b path. If x,y in S were nonadjacent, shortest x-y paths with interiors in A and B would combine to an induced cycle of length at least four. No cross-component edges exist and shortestness rules out the other chords. Therefore S is a clique. Apply induction to G[A union S] and G[B union S], both strictly smaller chordal graphs. In either graph, if complete choose a vertex outside S; otherwise the nonadjacent simplicial pair has a member outside the clique S. That vertex is simplicial in all of G, since it has no neighbors in other components of G-S. The two chosen vertices are nonadjacent. This completes induction.

In every chordal induced graph, a proper clique root leaves such a simplicial vertex outside it. Thus chordal graphs have rooted defect zero. In the other direction an induced cycle of length at least four has no simplicial vertex, violating the empty-root condition. The equivalence includes disconnected graphs and isolates and requires no connectedness assumption.

### Join and obstruction lemmas

For Lemma 2.2, a maximum clique of H leaves at most |H|-omega(H) exceptional vertices in every neighborhood. Clique deficiency cannot increase on taking induced subgraphs. For a join with a complete graph, the original H is induced, giving one inequality for the defect. For the other, retain all complete-side vertices while following an H-order ending at the H-part of the root. Each retained complete-side neighbor adds equally to neighborhood order and clique number. Finish within the remaining complete graph.

In Lemma 2.3, a clique on the 2s+2 endpoints of s+1 disjoint nonedges misses at least one endpoint of each pair. An independent common-neighbor set P of size s+2 therefore gives deficiency at least s+1 at every vertex of P. With a maximum endpoint clique retained as root, each endpoint outside the root sees all P. Its neighborhood clique number increases by only one upon adjoining P, whereas its neighborhood size increases by s+2. It also has deficiency at least s+1. No allowed first deletion remains. The configuration really needs vertex-disjoint nonedges and an independent common-neighbor set; both hypotheses are later supplied explicitly.

### Edge coloring and the extremal examples

Restoring the edges of a vertex of degree at most d in a d-degenerate simple graph forbids at most (Delta-1)+(d-1) colors at each restoration. The claimed Delta+d palette is therefore sufficient. Alternating components of two edge colors are paths or even cycles. If their total sizes differ by at least two, a path with one additional edge of the larger color exists; reversing it lowers the sum of squared class sizes. This proves balanced color classes, allowing unused colors.

For the attaining graph, its core consists of a clique of size k-s and s internally isolated vertices; its b pages are independent and every core-page edge is present. Delete non-root pages first. At most one page can be in the root. The graph then remaining is chordal, so the rooted elimination can finish. The reverse defect inequality follows by retaining the forced core clique: all pages have deficiency s and each exceptional core vertex has deficiency b-1>=s. For s=0 the lower bound is automatic.

A part with one page and j core vertices has j spokes and consumes binom(j,2) core edges. Since j<=1+binom(j,2), summing over page-containing parts gives cp>=kb-binom(k-s,2), whether or not the partition also has core-only parts. To attain this bound, label the forced core by residues modulo k-s, color ij by i+j, assign its colors to distinct pages, and extend each core edge to a triangle. Colors of incident edges differ; there are enough pages. Complete with single edges. The case k-s=1 has no core edges.

The square completion is an identity:

c(n-c)-binom(c-s,2) = M(n+s)-binom(s+1,2) -(3/2)(c-(2(n+s)+1)/6)^2.

The integer maximum is Q_s(n). When n+s is 0 or 2 modulo 3 the loss from the real maximum is 1/24; when it is 1 modulo 3 the loss is 3/8. The maximizing integers are precisely those nearest (2(n+s)+1)/6. For fixed s they eventually lie between s+1 and n/2, so the attaining construction has b>=k and a nonempty forced core. There is no unstated divisibility restriction.

## Section 4 and compatible edge-disjoint constructions

### Lemma 4.1

Put a=ceil(c/2), and split the core into parts of sizes floor(c/2) and a. Every potential core pair has at least all but 2tau of the exterior vertices as possible triangle apices. Use disjoint palettes of sizes a+2tau and 2a-3+2tau. The first palette leaves at least a allowed colors on each crossing pair. The crossing graph is a complete bipartite graph with maximum degree a and a proper a-edge-coloring, given directly by the sum of endpoint labels modulo a. Galvin's original Theorem 4.1 on printed page 156 says that the line graph of an n-edge-colorable bipartite multigraph is n-choosable. Its hypotheses therefore hold exactly. The original paper and theorem number were inspected, rather than inferred from a secondary description.

For pairs within either half, there are at most 2a-4 adjacent pairs. At least 2a-3 colors remain in the second palette, so greedy coloring works. The two halves can reuse colors because they have disjoint vertices; the two palettes cannot collide. Keeping only actual core edges then extends each to one triangle. A repeated cross edge would require two incident core edges to have the same color, which properness forbids. The palette sum is exactly 3a-3+4tau. This argument works for an incomplete core because coloring was performed on the complete abstract pair set first.

### Lemma 4.2

Balance a k-edge-coloring of the exterior so that each class has size at most ceil(m/k). Inject the c core vertices into its k colors. For an exterior edge xy, at least c-2sigma core vertices are adjacent to both endpoints. Each of these has probability 1/k of receiving the edge's color; these events are disjoint because the assignment is injective. The expected number of retained exterior edges is at least m(c-2sigma)/k. Therefore some assignment attains that count.

Extend each retained exterior edge through its assigned core vertex. Edges of one color form a matching, so the resulting triangles are mutually edge-disjoint. Each core vertex spends at most 2ceil(m/k) cross edges. Thus in the residual graph its missing-exterior count is at most tau+2ceil(m/k). All core edges remain. Lemma 4.1 applies because (4.5) is exactly its requirement with this enlarged deficiency. The second triangle family cannot reuse edges of the first because it is built in the residual graph.

For t retained exterior edges the resulting partition has

e(G)-2(h+t)=cb-D-h+m-2t

parts. Substituting the lower bound on t gives (4.6). The upper capacity bound k<=2(c-2sigma) makes the omitted exterior saving nonnegative. Strictness later makes that saving coefficient positive. No property of an edge-deleted graph other than the displayed cut parameters is imported.

### Lemma 4.3

A family of exceptional-vertex matchings maximizing total cardinality exists in the finite graph. For a fixed exceptional x, its matching is maximum after deleting the cross edges used by all other matchings, since an improvement would improve the family. Write q_x for its size and L_x=min(u_x,v_x)-q_x. There are at least L_x unmatched vertices on each side. Choose exactly L_x on each side. An available edge between two unmatched vertices would enlarge the matching, so the chosen rectangle has no available edge.

Each other matching uses at most one edge at any fixed vertex. Consequently the original graph has at most t L_x edges inside the rectangle; its L_x^2 pairs contain at least L_x^2-t L_x missing pairs. Thus L_x^2-t L_x<=D, and L_x<=sqrt(D)+t. The matchings yield edge-disjoint triangles through the exceptional vertices. Removing their cross edges increases each row and column deficiency by at most t, with core and exterior internal graphs unchanged. Apply Lemma 4.2 to that residual graph.

When the exceptional triangles and unused exceptional incidences are restored, the count is

cb-binom(c,2)-D + sum_x |v_x-u_x| + 2 sum_x L_x + e(T).

The term -D+2t sqrt(D) is at most t^2, and e(T)<=binom(t,2). Together with the remaining 2t^2 the error is at most 4t^2. This derives (4.8); it does not hide a linear-in-n error. Later t is bounded by a constant depending on s, not merely sublinear.

## Section 5 and removal of all asymptotic losses

### Fixed constants and the bounded exceptional set

The constants are lambda=1/[100(s+1)] and rho=lambda/100. The needed margins are

lambda/3-8rho > 0, 1/6-4lambda > 0, and (2s+2)lambda=1/50.

All are strictly valid for every integer s>=0. They are fixed before passing along a sequence.

Starting with a near-extremal clique A, discard its columns missing more than rho n/4 exterior vertices. There are o(n) such columns because their aggregate deficiency is o(n^2). Moving them creates only o(n^2) exterior edges; hence omega(R_0)=o(n). A retained core column still misses at most rho n/4 exterior vertices because moved clique vertices are adjacent to it.

Set ell=ceil(4(s+1)/rho). Suppose ell disjoint missing pairs join retained core columns to rows with exterior degree at least rho n. Each pair has at least rho n/2 common exterior neighbors. Summing pair incidences gives at least 2(s+1)n. If M exterior vertices see at least s+1 pairs, the sum is at most sn+ell M, giving M>=n/ell. One fixed (s+1)-subset of pairs is therefore seen by at least n/[ell binom(ell,s+1)] vertices. This is a positive constant times n. The induced exterior has chromatic number at most omega(R_0)+s=o(n), so the common-neighbor set has an independent set of size s+2 for all sufficiently large n. Lemma 2.3 gives a contradiction.

A maximal matching of missing pairs has fewer than ell edges. Put its row endpoints into T_1 and move its core endpoints into the exterior. Every remaining high-degree row is complete to the surviving core A_1; otherwise an additional edge could enlarge that maximal matching. The moved core vertices are also complete to A_1. Other rows have exterior degree below rho n+O_s(1).

Promote U, the rows with degree above |R_1|-lambda n. They are complete to A_1, and |U|=o(n) by exterior sparsity. Each member of A_1 union U misses at most lambda n vertices in R_1, including itself when appropriate. A matching of s+1 nonedges within A_1 union U would have at least |R_1|-(2s+2)lambda n=Omega(n) common neighbors in R_1. The same coloring argument would give s+2 independent common neighbors, contradicting Lemma 2.3. Remove all endpoints Z_0 of a maximal such matching, at most 2s vertices. The remaining promoted core is a clique. Put Z_0 into T, not back among ordinary rows.

Thus |T|<=ell-1+2s, a bound independent of all error rates. Changes to A involve o(n) vertices, retaining the sparse-error conclusions. A remaining low-degree row has only rho n+O_s(1) neighbors outside A_1 and the bounded exceptional set; minimum degree n/3-o(n) therefore forces all but rho n+o(n) core adjacencies. Other rows were already complete to A_1. Adding U of size o(n) gives sigma<=2rho n. Columns miss at most lambda n rows. An unpromoted row has degree at most |R_1|-lambda n, so after removing U its degree is at most |R|-lambda n/2 for sufficiently large n. This establishes every conclusion of Lemma 5.1 with uniform T_0(s).

### The incidence inequality and finite optimization

In Lemma 5.2 use an elimination order ending in C. At a row deletion, retained core neighbors provide a clique of order at least |C|-a. Any forward-neighborhood clique meeting X has order at most |N_C(x)|+w+h<|C|-a for some x in that clique. Therefore a largest forward clique avoids X, and at most s later X-neighbors remain. At an exceptional deletion, its largest forward clique has order at most |N_C(x)|+w+d_X^+(x). Subtracting this from forward degree shows d_R^+(x)<=s+w. Counting X-R edges at the earlier endpoint yields s|R|+h(s+w). This is an inequality on an induced graph, not an altered-edge graph.

For Lemma 5.3, outside I={i:y_i>x_i and x_i<1}, each absolute difference is at most one. Inside it, the sum is at most both 2h and sum_I y_i<=2s. Thus the total is at most t-h+min(2h,2s)=t+s-|h-s|. Achieving at least t+s forces h=s, x_i=0,y_i=2 inside I, and (x_i,y_i)=(1,0) or (1,2) outside I. All equality requirements are necessary; no points with intermediate coordinates remain.

### Proposition 5.4 before taking limits

Theorem 1.3 applies because Q_s(n)=n^2/6+O_s(n). Apply Lemma 5.1. Its bounded T permits a subsequence with fixed size t and convergent normalized exceptional profiles (3u_i/n,3v_i/n) in [0,1] times [0,2]. No compactness of an unbounded exceptional family is assumed.

Exterior degeneracy and Lemma 2.4 give k=max(c,Delta(R)+omega(R)+s) colors. Its normalized upper bound is 2/3-lambda/2+o(1), while 2(c-2(sigma+t))/n>=2/3-8rho-o(1). The capacity inequality is eventually strict. The other normalized palette slack is at least 1/6-4lambda-o(1)>0, since k>=c and m=o(n^2) imply ceil(m/k)=o(n). Thus Lemma 4.3 actually applies to all sufficiently large graphs in the subsequence.

Its base cb-binom(c,2) is at most M(n-t), while Q_s(n)-M(n-t)=(s+t)n/3+O_{s,t}(1). The 4t^2 error disappears after division by n/3. Therefore sum_i |y_i-x_i|>=s+t in the limit.

For I as above, every selected exceptional vertex misses a positive linear number of core vertices; there are only boundedly many such vertices. Define eta_n=sqrt(D/n^2)+n^(-1/2), and remove rows missing more than eta_n n core vertices. At most D/(eta_n n)=o(n) are removed. The remaining maximum row deficiency and clique number are both o(n), so Lemma 5.2's strict hypothesis holds. Restoring o(n) rows costs only o(n) incidences with bounded X. Dividing the incidence bound by n/3 gives sum_I y_i<=2s. Lemma 5.3 therefore yields exactly s exceptional vertices X of type (0,2), and sets P,Z of types (1,0),(1,2).

### Exact rigidity after the limits

The limits alone do not give exact adjacency. The manuscript obtains that next. If C union Z contained a nonedge, choose for each of the s vertices of X a different missed vertex of C, also avoiding the initial endpoints. Each X-vertex has linearly many choices. Together these are s+1 disjoint nonedges. Their endpoints have at least b-(s+2)lambda n-o(n)=Omega(n) common neighbors in R: old core columns miss at most lambda n, whereas X and Z miss only o(n). Exterior chromatic number o(n) again supplies s+2 independent common neighbors, violating Lemma 2.3. This also works at s=0 with just the initial nonedge. Hence C union Z is an exact clique.

Now discard the preliminary matchings and use a fresh cut of the original graph: C'=C union Z union X and R'=R union P. This is crucial for avoiding reused edges. The core contains the clique C' minus X of order c'-s. Moving a bounded set and using the established profiles gives

c'=n/3+o(n), b'=2n/3+o(n), sigma'<=2rho n+o(n), tau'<=lambda n+o(n), m'=o(n^2), omega(R')=o(n).

Old rows gain only boundedly many neighbors and added P-rows have o(n) row neighbors, so Delta(R')<=b'-lambda n/3 eventually. With k'=max(c',Delta(R')+omega(R')+s), the first normalized capacity margin is at least lambda/3-8rho-o(1)>0. The second is at least 1/6-4lambda-o(1)>0. Thus Lemma 4.2 gives a finite bound with theta=2(c'-2sigma')/k'-1 strictly positive:

cp(G) <= c'b'-e(C')-D'-theta m'
      <= c'(n-c')-binom(c'-s,2)-D'-theta m'
      <= Q_s(n).

The hypothesis cp(G)>=Q_s(n) forces equality. Since D',m'>=0 and theta>0, both vanish. The known clique C' minus X already accounts for binom(c'-s,2) edges, so equality forces every X-vertex to be isolated inside the core. All cross edges exist; the exterior is independent. Equality in the integer quadratic fixes exactly the nearest-integer choices for c'. This proves the eventual graph classification, not only an asymptotic approximation to it.

### Theorem 1.1 and Corollary 1.2

Suppose cp(G)-Q_s(|G|) were unbounded for fixed s. For each integer K tending to infinity choose a smallest-order graph violating cp<=Q_s+K. Its order tends to infinity because there are finitely many graphs of bounded order. Every one-vertex deletion satisfies the same K-bound. Adding its incident edges as singleton parts and using integrality yields

d(v)>=Q_s(n)-Q_s(n-1)+1=floor((n+s+1)/3)+1>n/3.

This sequence meets Proposition 5.4 and must have cp=Q_s eventually, a contradiction. Thus a uniform nonnegative integer K_s exists. Only after this is established, a graph with cp>=Q_s has d(v)>=Q_s(n)-Q_s(n-1)-K_s>=n/3-K_s-1. Any unbounded sequence of such graphs therefore meets Proposition 5.4. This proves one uniform eventual threshold N_s and the exact extremal classification above it. Lemma 2.5 supplies an attaining graph at every sufficiently large order.

There is no circular use of the desired constant in its proof. Theorem 1.3 depends only on the fractional localization and packing conversion; Proposition 5.4 depends on that stability theorem and the exact construction; the constant-error theorem is proved last. Substituting s=0 using the independently established chordal equivalence gives the claimed uniform bound floor(n(n+1)/6)+K_0 and eventual exactness.

## Limits of the acceptance

This is a mathematical proof audit, not machine-checked formalization or journal peer review. Finite computations corroborate arithmetic and small examples only. The established fixed-pattern packing approximation is a cited theorem, not a theorem re-proved from regularity and hypergraph matching here. The exact role and hypotheses of that import are verified in FRACTIONAL_AUDIT.md. No new conjectural assumption enters the accepted result. Auxiliary Section 6 is not part of this acceptance, and no explicit usable values of K_s or N_s are supplied. No correction of the manuscript is required by this audit.
