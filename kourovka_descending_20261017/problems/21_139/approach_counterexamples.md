# Counterexample search for Kourovka 21.139

Status: **no counterexample, and no resolution of the full problem**. Independent route started 2026-10-17. The strongest results below are deductions from established theorems plus one exact cover calculation; they are not claimed as novel. Best-guess completion toward the original research goal: **12%** (the candidate families are substantially narrowed; the central general gap remains).

## Exact target and quantifiers

Find a word-hyperbolic virtually compact special group G with

    sup { dim_Q H_2(U;Q) : U <= G, [G:U] < infinity } < infinity,

but no finite-index subgroup that is free or a closed surface group. This is an upper bound over **all** finite-index subgroups. A bound in one normal tower, an arbitrary large finite sample, or vanishing normalized/L2 Betti numbers is insufficient.

All homology below has rational coefficients. Passing to a torsion-free compact-special finite-index subgroup G0 is legitimate for an obstruction: its finite-index subgroups are also finite-index in G, so an unbounded family in G0 is one in G. Conversely, a virtual free/surface conclusion for G0 gives the same virtual conclusion for G. Rational transfer makes restriction to a finite-index subgroup injective in cohomology; equivalently rational Betti numbers cannot decrease in a finite cover. Thus boundedness is commensurability invariant, using U intersect G0 for the reverse direction.

## A reusable obstruction: one infinite-index quasiconvex H with b2(H)>0

**Proposition.** If G is hyperbolic and virtually compact special and has an infinite-index quasiconvex subgroup H with b2(H)>0, then vb2(G)=infinity.

Proof. First intersect with a torsion-free compact-special subgroup and use transfer: H0=H intersect G0 remains infinite-index quasiconvex and b2(H0)>=b2(H)>0. Arzhantseva's Theorem 1 [A01] gives a quasiconvex subgroup Q=<H0,t> of G0 with Q isomorphic to H0*Z. The Haglund–Wise virtual-retraction theorem gives a finite-index U of G0 containing Q and a retraction r:U->Q [HW08; W12]. For each m>=1, put Q_m=ker(Q->Z/m), with H0 mapping to zero and t to 1. The elementary covering of a wedge K(H0,1) vee S1 has m copies of K(H0,1) arranged around one circle, whence

    Q_m = (*_{j=1}^m H0) * Z,
    b2(Q_m)=m b2(H0).

The subgroup U_m=r^{-1}(Q_m) has index m in U and retracts onto Q_m. Inclusion and retraction compose to the identity, so H_2(Q_m)->H_2(U_m) is injective. Therefore b2(U_m)>=m b2(H0), proving unboundedness. This uses arbitrary finite-index subgroups, with a constructed family witnessing failure. It does not assume that a homology class embedded in an arbitrary subgroup survives in an ambient cover. Q need not have infinite index for this argument. Q_m has a finite classifying space because H0 is quasiconvex virtually compact special. ∎

In particular, an **infinite-index quasiconvex closed orientable surface subgroup** rules out a counterexample. The same holds for a virtually closed surface subgroup, after intersecting its orientable finite-index subgroup with G0. An arbitrary distorted surface subgroup is not enough for this proof; quasiconvexity is an essential checked gate.

A useful elementary model is G=pi1(Sigma_2)*Z. The index-m kernel of the map that kills pi1(Sigma_2) and maps the Z generator to 1 mod m has

    b1=4m+1, b2=m, chi=-3m.

It is hyperbolic and virtually compact special, but its second Betti numbers are unbounded. Merely starting with b2(G)=1 does not make a near-counterexample.

## Free-by-cyclic candidates: the entire finite-rank family is excluded

**Lemma.** Every non-elementary hyperbolic virtually compact special group has vb1=infinity.

Proof. Work in a torsion-free compact-special subgroup. An infinite cyclic subgroup is quasiconvex and has infinite index. Arzhantseva [A01] enlarges it to a quasiconvex F2. A finite-index subgroup retracts onto F2 by [HW08; W12]. Pull back the index-m subgroups of F2, whose first Betti number is m+1. Their homology injects in that of the pullbacks. ∎

Let G=F_r semidirect_phi Z with finite r>=2 and suppose G is hyperbolic. Hagen–Wise [HaW15] cubulate G and Agol [Ag13] gives virtual compact specialness. A mapping torus of a rose is a finite two-dimensional K(G,1), with chi(G)=0. Every finite-index U has a finite two-dimensional classifying space and chi(U)=0; hence

    b2(U)=b1(U)-1.

The lemma gives vb2(G)=infinity. This excludes **every atoroidal automorphism of every finite-rank free group**, regardless of its abelianization spectrum, Alexander polynomial, or fixed spaces in any chosen tower. Finite r=0 or r=1 supplies no non-elementary hyperbolic counterexample. The broader phrase 'virtually free-by-cyclic' sometimes permits infinitely generated free kernel; the Euler-characteristic argument here does not exclude that broader class. Free groups themselves, for example, admit epimorphisms to Z with infinitely generated free kernel.

More generally, if G has a finite two-dimensional K(G,1), is non-elementary hyperbolic virtually compact special, and chi(G)>=0, then vb2(G)=infinity. For chi>0, Euler characteristic alone gives b2(U)=chi(U)+b1(U)-1>= [G:U]chi(G)-1. For chi=0 use the lemma. Thus a remaining two-dimensional counterexample must have negative Euler characteristic.

### An explicit, exact cyclic-tower diagnostic

Take F=F(a,b,c) and

    phi(a)=b, phi(b)=c, phi(c)=ab,
    G=F semidirect_phi Z.

The inverse sends (a,b,c) to (ca^{-1},a,b), so this is an automorphism. Bestvina–Feighn [BF95], Example 3.3 and Proposition 3.1, give a stable expanding train-track representative without periodic Nielsen paths. Every nontrivial loop eventually becomes legal and expands, excluding a periodic conjugacy class. Brinkmann [Br00] gives hyperbolicity; [HaW15; Ag13] give virtual compact specialness.

This G is neither virtually free nor virtually a closed surface: chi(G)=0, while every non-elementary free or closed hyperbolic surface group has negative Euler characteristic. The elementary alternatives are excluded by its subgroup F3, and a torus alternative by word hyperbolicity. Hence the failure of this near-counterexample is exactly its unbounded homology over all covers.

On H1(F), with columns the images of a,b,c, the matrix is

    M = [[0,0,1],[1,0,1],[0,1,0]],  char_M(x)=x^3-x-1.

This cubic is irreducible over Q (neither 1 nor -1 is a root) and has a real root between 1 and 2. If an eigenvalue were a root of unity, its irreducible polynomial would have all conjugates on the unit circle, contradicting that real root. Consequently det(M^n-I) != 0 for every n>=1. For the standard cyclic cover G_n=F semidirect_phi^n Z, the Wang sequence yields

    b2(G_n)=dim ker(M^n-I)=0,
    b1(G_n)=1.

Nevertheless, let K=ker(F->(Z/2)^3). The subgroup H2=K semidirect_phi^2 Z has index 16 and **b2(H2)=1**; the subgroup H14=K semidirect_phi^14 Z has index 112 and **b2(H14)=7**. Both values are exact calculations below. Thus even a proof that every cover in this entire standard cyclic tower has b2=0 misses actual positive-b2 covers. The preceding family argument proves the still stronger fact vb2(G)=infinity.

Reproduction: run `python3 counterexample_artifacts/exact_cover_diagnostics.py`. It uses only Python's standard library and exact integer/Fraction arithmetic. All matrices are saved in `counterexample_artifacts/exact_results.json`.

The (Z/2)^3 cover X of the three-petal rose has 8 vertices and 24 edges. Its boundary d has rank 7, so H1(X)=ker(d) has dimension 17. Since K is characteristic in F, every phi^n induces a based homotopy equivalence of X. Its vertex map is v -> M^n v; fixing all vertices is unnecessary. For phi^2 the code lifts the words a->c, b->ab, c->bc starting at M^2 v and forms the edge matrix T2 and vertex matrix P2. It checks dT2=P2 d and obtains

    rank([d ; T2-I])=23,
    b2(H2)=24-23=1.

For the stronger jump, the mod-2 order of M is 7, so phi^7 does fix every vertex. Its positive edge words are

    a -> bccab, b -> cababbc, c -> abbcbccab.

The code forms the 24-by-24 cellular edge matrix T by lifting these paths and checks dT=d. The mapping torus of phi^14 on X is a K(H14,1); because X has no 2-cells, its second homology is exactly the simultaneous kernel of d and T^2-I. Exact rational elimination gives

    rank([d ; T^2-I])=17,
    b2(H14)=24-17=7.

This is an exact finite-cover computation, not an empirical inference about all covers. For comparison, the corresponding index-56 cover with monodromy phi^7 has b2=0. The code also checks the covers with monodromy phi^(7n), n=1,...,12, which alternate between 0 and 7; no all-n pattern is inferred from that finite table.

## Odd-dimensional closed real hyperbolic manifolds

For a closed orientable hyperbolic 3-manifold M, Poincare duality gives b2=b1 in each cover. Virtual compact specialness and the preceding vb1 lemma therefore exclude all such groups. No virtual-fibering assumption is needed for this deduction.

For dimension n=2k+1>=5, chi(M)=0 and Poincare duality only gives b2=b_{n-2}; these facts **do not** express b2 in terms of b1. Thus the 3-manifold argument must not be generalized to all odd dimensions.

The standard arithmetic family nevertheless fails. Over k=Q(sqrt(2)), consider

    q_n= -sqrt(2) x0^2 + x1^2 + ... + xn^2.

It has signature (n,1) at the identity embedding and is positive definite at the other real embedding. Positive definiteness there proves anisotropy over k. Standard arithmetic-lattice theory gives uniform lattices in O(q_n) and hence torsion-free closed real-hyperbolic n-manifold groups after passing to finite index. Such simplest-type lattices are virtually compact special [BHW11; AOS24, Section 8]. The subform on x0,x1,x2 supplies a uniform Fuchsian subgroup. Intersecting with the chosen lattice and passing to orientation gives a closed orientable surface group. Its totally geodesic plane is convex, so its group is quasiconvex. For n>2 it has infinite index (for example cohomological dimensions are 2 and n). The reusable obstruction proves vb2=infinity in **every dimension n>2** for this explicit family. [M14] records the general quadratic-subform construction.

This does not establish an all-cover bound, or its failure, for every conceivable odd-dimensional hyperbolic lattice. A proposed exceptional/nonstandard lattice must independently establish virtual compact specialness and the required bound over all finite-index subgroups. Neither chi=0 nor a vanishing normalized tower is that bound. This route is **blocked as a counterexample route for the standard arithmetic family** and **unsupported for general higher-dimensional lattices**.

## Higher-dimensional cube complexes: all hyperbolic right-angled Coxeter groups are excluded

Here is a restricted-class deduction with explicit exceptions; it does not solve 21.139 for arbitrary special subgroups of right-angled Artin groups.

Let Gamma be a finite simple graph and

    W_Gamma=<v in V(Gamma) | v^2=1, [v,w]=1 for edges {v,w}>.

These groups are virtually compact special [K12; HW10]. The hyperbolicity criterion is that Gamma has no induced 4-cycle (the right-angled case of Moussong's criterion; see [D08], Theorem 12.6.1 and Corollary 12.6.3).

If Gamma is chordal (no induced cycle of length >=4), its simplicial-vertex elimination expresses W_Gamma as a finite graph of finite clique groups, amalgamated over finite clique groups. Therefore W_Gamma is virtually free. This includes empty Gamma, complete Gamma, disconnected chordal Gamma, and finite W_Gamma. The elementary induction uses

    W_Gamma = W_(Gamma-v) *_(W_link(v)) W_star(v)

at a simplicial vertex v: star(v) and link(v) are cliques. The equivalent Coxeter virtual-freeness criterion appears in [D08], Proposition 8.8.5.

Otherwise choose an induced cycle C of length m>=5. The special subgroup W_C is a cocompact right-angled hyperbolic polygon reflection group, so has a finite-index orientable closed surface subgroup S. Inclusion W_C->W_Gamma is isometric in the standard word metrics: killing all outside generators is a retraction that does not increase word length, and the reverse length inequality follows from inclusion. Therefore W_C and S are quasiconvex in the hyperbolic group W_Gamma. This also gives a direct proof of the convexity gate without relying on a surface subgroup's mere existence.

If some vertex v outside C misses a cycle vertex u, the retraction

    W_Gamma -> W_{u,v}=<u,v | u^2=v^2=1> = D_infinity

maps W_C into <u>. The cosets (vu)^j <u>, j>=0, are distinct by the alternating normal form in D_infinity. Their lifts (vu)^j W_C are therefore distinct in W_Gamma/W_C: equality for j>i would force (vu)^(j-i) into <u>, impossible. Hence W_C has infinite index and the reusable obstruction gives vb2(W_Gamma)=infinity.

In the other case every outside vertex is adjacent to every vertex of C. If two outside vertices x,y were nonadjacent, choose two nonadjacent cycle vertices u,w; the induced graph on u,x,w,y would be a 4-cycle, contradicting hyperbolicity. Thus the outside graph is complete, and

    W_Gamma = W_C x (Z/2)^(number of outside vertices).

Then W_Gamma is virtually a closed surface group. This includes Gamma=C and any finite clique joined to C. All cases are exhausted, including disconnected nonchordal graphs (vertices in another component trigger the infinite-index case).

Therefore **the answer to 21.139 is positive for hyperbolic right-angled Coxeter groups and all groups commensurable with one**, by an explicit induced-cycle argument. This is an independently checkable restricted-family deduction, not claimed as new.

For a concrete higher-dimensional diagnostic use the icosahedral graph. Its flag complex has 12 vertices, 30 edges, 20 triangles, Euler characteristic 2, no 4-clique, and no induced 4-cycle. A vertex link is an induced pentagon; the opposite vertex misses every vertex of that pentagon. Thus the group is hyperbolic virtually compact special and has vb2=infinity. The code certifies these graph facts; its Davis complex is three-dimensional (indeed this is the right-angled dodecahedral reflection example). Arbitrarily high cohomological dimension in the Coxeter family cannot evade the induced-polygon obstruction.

## Other tempting constructions and the exact missing gate

- **Z^n, n>=3:** compact special, and every finite-index subgroup has b2=binomial(n,2). It is neither virtually free nor virtually a surface, but it fails word hyperbolicity because it contains Z^2.
- **BS(1,d), d>=2:** every finite-index subgroup is isomorphic to BS(1,d^k) for some k>=1, and b2=0. To see this, write it as Z[1/d] semidirect_d Z; a finite-index subgroup intersects Z[1/d] in a finite-index subgroup rZ[1/d] and projects to kZ. The extension splits over Z and its action is multiplication by d^k. The finite two-dimensional aspherical mapping-torus model has chi=0 and b1=1, giving b2=0. This solvable non-virtually-cyclic group fails word hyperbolicity, so is not a counterexample.
- **Property-(T) hyperbolic lattices/random groups:** finite virtual b1 does not establish bounded virtual b2. Non-elementary virtually compact special groups have vb1=infinity by the lemma, so property (T) is incompatible with the special hypothesis. This family cannot be used by silently transferring the good homology behavior across that hypothesis.
- **Generic two-dimensional, negative-Euler-characteristic special groups:** the Euler formula allows bounded b2 together with linearly growing b1. An infinite-index quasiconvex subgroup being one-ended or non-free does not imply it has nonzero rational H2 in a finite cover. Promoting that implication without proof would simply transfer the central difficulty to an unsupported claim. This is the exact remaining gate for this search.
- **Random/small-cancellation examples with an established quasiconvex closed surface:** immediately excluded by the reusable obstruction. Without such an established subgroup, finite Alexander/Fox computations remain selected-cover diagnostics only.

## Source provenance and limitations

Only primary research articles, author-hosted papers, and the original-author Coxeter monograph are used for mathematical claims. `sources_counterexamples/manifest.json` gives URLs, exact locators where checked, and what each source supports. Search-result dates are not treated as publication dates. No author was contacted, no outreach was prepared, and no claim of general openness or novelty is based on this independent search alone. The main team separately audits current literature and adversarially verifies the reusable obstruction and Coxeter deduction.
