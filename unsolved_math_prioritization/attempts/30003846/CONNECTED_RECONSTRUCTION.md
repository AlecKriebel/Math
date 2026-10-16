Current reading note: ACCEPTANCE.md governs the combined packet. The connected proof below is retained; its former unproved I0 import is superseded by the independently reviewed supplement, under an explicit convention.

# Fast one-bump groups: reconstruction of the prior connected classification

## Status and attribution

This is an authored verification of Gili Golan's existing argument in arXiv:2607.10961v1, dated 12 July 2026. It is not a new solution or a claim of independent discovery. The conclusion of the verification is that the argument establishes the stated classification, with the imported results listed below. The manuscript was publicly available as a preprint when checked on 8 October 2026; journal acceptance was not established.

The proof-checking argument below spells out hypotheses, allowable transformations, base-path transport, induction invariants, and the final finiteness implication. References are to primary sources. No source PDF or source-text extract is part of this packet.

## 1. Exact mathematical scope

Fix n >= 2. Let B consist of n orientation-preserving homeomorphisms of an interval, each with precisely one nonempty support component. Replace any negative generator by its inverse. This preserves the generated group, the supports, and geometric fastness, using the inverse-bump feet convention in Belk–Stott, Section 2.1.

For a positive generator b with support (a_b,c_b), choose m_b inside that support. Its feet are (a_b,m_b) and [b(m_b),c_b). Geometric fastness means that all 2n feet are pairwise disjoint for some choices of the markers. Record their linear order as L_b,R_b, with L_b preceding R_b. Two vertices b,c of the crossing graph are adjacent exactly when their feet alternate. The main classification concerns a connected crossing graph.

The conclusion is G=<B> isomorphic to the n-ary Thompson group F_n, realized on [0,1] with finitely many breakpoints in Z[1/n] and slopes in n^Z. Consequently G is of type F_infinity. The isomorphism assertion is for each fixed n, not an assertion that F_n and F_m coincide for different n.

The original report, printed page 1610, defines C_n by excluding nontrivial direct sums and wreath products and asks its finiteness and isomorphism questions separately as Questions 71 and 72. Golan's introduction asserts a disconnected-diagram direct-product or permutational-wreath decomposition into groups on fewer bumps. SCOPE_AUDIT.md proves that direction under its explicit finite-support, potentially nonfaithful permutational convention, and INDEPENDENT_REVIEW.md accepts it. Therefore exclusion implies connectedness when the excluded products include that convention. The original passage does not define its indexing action, so the exact original interpretation remains conditional. No classification of all abstract decompositions is asserted. For finitely many factors, direct-sum/product wording makes no distinction.

The assumptions are essential. With two disjoint bumps the group is Z^2; with one fast bump nested in another it is Z wr Z. These are not examples to which the connected-graph conclusion applies. There is no claim here about arbitrary slow generators, multibump generators, infinitely many generators, or an unbounded-n uniform isomorphism type.

## 2. Explicit imported-result boundary

I0. In this earlier reconstruction the disconnected-diagram decomposition observation was an unproved import. The first independent audit withheld acceptance of this step. SCOPE_AUDIT.md now proves it for the expressly defined restricted permutational wreath product with finite base support and potentially nonfaithful top action; INDEPENDENT_REVIEW.md accepts that proof. The original report does not define the wreath indexing convention in its question passage, so unconditional acceptance of its exact class remains withheld. See ACCEPTANCE.md for the current verdict.

I1. Bleak–Brin–Kassabov–Moore–Zaremsky, Theorem 1.1: the ordered dynamical diagram determines the marked group for finite geometrically fast sets. Their Theorem 7.1 supplies a piecewise-linear realization of any diagram. In the no-isolated-bump case its proof gives a realization whose feet cover the support except finitely many endpoints. The relevant statement and construction were checked in the primary preprint, Sections 6–7. These imported results apply because the sets here are finite.

I2. Belk–Stott, Theorem 3.7: for a canonical partition A_1,...,A_N, the fast bump group is the diagram group with base A_1...A_N and, for each bump whose feet have indices i<j, the two indexed rules

A_i -> A_i A_(i+1)...A_(j-1),
A_j -> A_(i+1)...A_(j-1) A_j.

The theorem, its canonical-partition hypothesis, and the positive/negative-generator convention were checked in the primary PDF. The underlying representation theorem is imported, not replaced by a surjectivity assumption.

I3. Guba–Sapir, directed-2-complex Theorem 4.1: adjoining a fresh edge x with a cell x->w for a nonempty path w preserves diagram groups at old bases; its inverse deletes an edge occurring in just that one cell, provided w avoids x. A side of one cell can be rewritten using a different cell. The distinct-cell condition matters. The theorem and its proof were checked in the primary preprint, pages 11–12. We also use standard diagram reduction and conjugation between homotopic bases.

I4. The standard core of F_n has a cycle of n-1 inner edges, two boundary edges, and the relations specified in Section 5 below. Golan–Eytan Sapir, Remark 5.2 gives the exact presentation, and Golan's Theorem 4.2 identifies its diagram group with F_n using the core/closure construction. The exact presentation in the primary May 2026 preprint was checked. The whole 51-page generation/maximal-subgroup paper was not audited. The core/closure theorem and the standard tree-pair model remain explicit imports.

I5. Brown, Theorem 4.17, establishes finite presentation and FP_infinity for the groups F_(n,r); Proposition 4.4 identifies F_(n,1) with the interval PL group used here. The scan was inspected directly at printed pages 55–56 and 65–67. Modern F_n corresponds to Brown's F_(n,1), not merely to any group carrying the unadorned symbol F_n in his paper. The usual implication 'finitely presented plus FP_infinity implies F_infinity' is used. Its standard cellular induction starts from a finite presentation complex and uses finite generation of the higher cellular kernels and Hurewicz to attach finitely many cells at each successive dimension. FP_infinity alone, without finite presentation, would not justify this step.

## 3. The dynamical part: an irreducible diagram can be peeled

Number bumps by increasing position of their right feet. A diagram is peelable when every nontrivial prefix in this order has connected crossing graph. Equivalently, each new bump crosses a preceding one.

At a bump b, write the feet strictly between L_b and R_b as XY. Suppose no other bump owns feet in both blocks. Let M be the owners of feet in Y. Replace each y in M by b^(-1) y b; retain all other generators, including b. Both generating sets generate the same group, since the replacement is reversible using b.

Here is the metric check behind the move. Put q equal to the left endpoint of the first Y-foot and m'=b^(-1)(q). The Y-feet were in [q,b(m)); after applying b^(-1) they lie in [m',m). The X-feet lie in [m,q) and remain there. The two new feet of b are (a,m') and [q,c). Every conjugated foot outside (a,c) is fixed by b; closedness excludes a conjugated foot in X. These four regions prove pairwise disjointness and give the new gap order YX. Thus the move preserves fastness and the actual subgroup, not just its abstract isomorphism type.

To see why these moves suffice, remove the rightmost bump z and examine the crossing components of the remaining diagram. Every component contains a bump crossing z, because the original graph is connected. Such crossing bumps all straddle L_z. Bumps from different components do not cross, so their spans are nested. The nesting propagates through a connected crossing component: if one member lies inside a noncrossing outside bump, all members do. Consequently the components are linearly nested, with one innermost component K.

A bump outside K and z either contains the entire reach of K or is disjoint from that reach. It follows that the K-owned feet in z's gap form an initial block X. The other feet form Y, and XY is a closed cut. Swapping these blocks preserves every old crossing: the only pairs with changed relative order have owners in different old components, so none of those pairs crossed before. After the swap, a crossing bump of K crosses a crossing bump of every other component: their formerly nested right endpoints reverse order while their left endpoints remain fixed. Hence deleting z now leaves a connected graph.

Apply induction to that deleted diagram. Each recursive swap lifts to the full diagram: the only extra foot that can occur in the chosen gap is L_z, and its partner R_z is outside; assign L_z to either side if it falls exactly at the cut. This cannot spoil closedness. Throughout a lifted swap, R_z stays last. If L_z lies in the swap's gap, the bump at which the swap is made still crosses z; otherwise z retains its prior crossing neighbors. Thus z remains attached. The recursively peeled smaller diagram together with z is peelable.

This is the induction behind Golan's Theorem 3.13, with no bounded-n assumption.

## 4. The directed complex and its induction invariants

For the canonical realization of an irreducible diagram, no bump is isolated; hence its partition consists of its 2n feet. For induction, also permit k dummy intervals between feet. Write the full partition A_1...A_N with N=2n+k, and the gap word of a bump as Gamma_b.

Begin with a directed line having vertices v_1,...,v_(N+1) and edges A_i:v_i->v_(i+1). If b owns A_i and A_j, the two cells

A_i -> A_i Gamma_b,   A_j -> Gamma_b A_j

force exactly v_(i+1)=v_j. Identify vertices by these equalities. All cell sides remain nonempty directed paths. Forgetting this vertex structure does not change a diagram group based at an originally readable path: every atomic cell replacement has matching endpoints, so all intermediate paths in a diagram remain readable. This proves the passage from I2 to this directed complex at the stated base.

There are exactly n+k+1 vertices. Impose the identifications in increasing j-order. The vertex v_j has not appeared in an earlier identification, so each relation merges two classes. The first and last vertices remain a unique source and a unique sink. Every other vertex has incoming and outgoing edges.

Irreducibility makes the inner vertices strongly connected. From each index one can always move right. If the reachable indices from an inner vertex started at a minimum mu>2, each bump whose right foot was at least mu would have its left foot at least mu-1, by its forced vertex identification. Bumps before and after that cut would form two nonempty sets with no crossings. This contradicts connectedness.

The allowed GS moves preserve vertices, directed reachability, and source/sink status. For edge addition this follows by substituting its defining path; deletion is the reverse, and rewriting a cell leaves the graph unchanged. Therefore these properties survive the entire reduction.

At each deletion x->w, replace x by w in the base path. The old and substituted bases are homotopic, so the group is unchanged. This explicit transport avoids deleting a generator that still appears in the chosen base without explanation.

## 5. The model core and its group

A model with k dummies has n-1 active inner edges and k dummy edges on a single directed cycle, and boundary edges a:source->u and c:v->sink. Denote one full turn starting at w by C(w). Its cells are

 e -> e C(terminal(e))  for each active inner edge e,
 a -> a C(u),
 c -> C(v) c.

There are no cells with dummy top edges. The induction below produces this form without deleting any original dummy edge or either original boundary edge.

For k=0 this is a shifted standard core of F_n. The standard attachment positions and presentation are exactly I4. Arbitrary attachments can be moved one cycle edge at a time by lawful GS operations. For example, write C(v)=gP, with g:v->v'. Adjoin c':v'->sink with c'=Pc. Rewrite c=gPc to c=gc'; rewrite the new defining cell to c'=Pgc'; then delete c. This shifts the right attachment to v'. No rule for g was needed. The left-end operation is symmetric.

Any two source-to-sink paths in a model core differ by full cycle traversals. Inserting or removing a turn at an active boundary edge and sliding its position along the deterministic cycle shows that the paths are homotopic. Thus changes of attachment and transport of base do not introduce a new unidentified diagram group.

Only the k=0 case is required at the end of the original problem. In particular, the dummy-edge contraction lemma in Golan's Section 4.5 is not needed for the dependency chain used here. Dummies are needed inside the structural induction, but that induction never invokes their diagram-group contraction.

## 6. Complete GS reduction bookkeeping

### Base case

A general partition for two crossing bumps is

 a D_1 b D_2 c D_3 d,

where a,c are one bump's feet, b,d the other pair, and each D_i contains only dummy edges. The four rules are

 a -> a D_1 b D_2,
 c -> D_1 b D_2 c,
 b -> b D_2 c D_3,
 d -> D_2 c D_3 d.

Adjoin s=bD_2c. Use this distinct new cell to rewrite c=D_1s and b=sD_3. Substitute these equalities in every other cell and delete b,c with their defining cells. The remaining rules are

 s -> s D_3 D_2 D_1 s,
 a -> a D_1 s D_3 D_2,
 d -> D_2 D_1 s D_3 d.

The inner graph is still strongly connected. It now has k+1 edges on k+1 vertices. A finite strongly connected directed graph with equally many edges and vertices has one incoming and one outgoing edge at every vertex and is therefore a single cycle. Each displayed cycle word traverses all inner edges once. The resulting complex is precisely the required n=2 model, and no boundary or dummy was deleted.

### Lifting a smaller reduction

A GS sequence can be replayed in a larger complex containing its edges and cells, even when the old vertices are identified and extra edges/cells are present. Replay an addition with the endpoints of its displayed path. Replay a cell rewrite using the same two cells. Before deleting x->w, rewrite all extra occurrences of x to w using that cell; only then delete x. This is the entire lifting mechanism. It also proves that the transported side of every extra cell is obtained by the smaller sequence's edge-substitution map phi.

### Induction from n to n+1

Let l,r be the feet of the last bump. Let c be the preceding rightmost foot. Peelability ensures l occurs before c and prevents the last bump from also being leftmost. The partition ends cDr, where D has ell dummy edges. Delete Dr from the partition and reclassify l as a dummy. This is a valid general partition for n bumps with k-ell+1 dummies.

Reduce the truncated complex by induction and lift the sequence. Its model cycle contains l as a preserved dummy, and c is its preserved right boundary. Put l:z->w and c:v->t. If ell=0, t=w; otherwise D:t->w and t is the old terminal vertex. The extra edge r:w->new sink remains in place.

Write the old cycle from v as X l Y, with X:v->z and Y:w->v. The last bump's original gap is P c D, and after lifting its two rules are

 l -> l phi(P) c D,
 r -> phi(P) c D r.

The image phi(P) is an inner path of the smaller core from w to v: it cannot contain either boundary edge because the old source has no incoming edge and the old sink has no outgoing edge. On the simple directed cycle,

 phi(P)=Y C(v)^s   for some integer s>=0.

Use the distinct cell c=C(v)c repeatedly to absorb these s turns in each extra rule. They become

 l -> l Y c D,
 r -> Y c D r.

Meanwhile c=X l Y c. Adjoin p:z->t with p=lYc. Rewrite the l-cell to l=pD and the c-cell to c=Xp. Substitute l=pD everywhere else and delete l. Then substitute c=Xp everywhere else and delete c. Neither is an original dummy of the full complex: both were original feet. The original outer boundary edges and original dummies survive.

For every old active inner edge e, and also for the left boundary, its cycle word has l replaced by pD. The two other remaining cells are

 p -> p D Y X p,
 r -> Y X p D r.

There are n active inner edges and k original dummies, hence n+k inner edges. The full dynamical complex has n+k inner vertices, and its source, sink and inner strong connectivity survived. The cycle-recognition argument used in the base case therefore applies again.

Each substituted old cycle traverses every new inner edge exactly once; so does DYX p, based at t. The final r-word is its cyclic rotation based at w. Therefore every remaining rule has the model-core form. This proves the structural induction for every n and every general partition.

Empty X, Y or D cause no illegal empty defining path: p=lYc always contains l and c; s=bD_2c always contains b and c; each cell's two sides remain nonempty. The ell=0 vertex identification is allowed by the lifting statement, so it is not silently treated as an injective inclusion.

## 7. Conclusion

Start with the original irreducible fast set. The dynamical swaps yield a peelable set generating the same group. Apply I1 to choose a canonical realization of its diagram. There are no isolated bumps, so this canonical partition has k=0. Apply I2 to identify its group with the diagram group of the directed dynamical complex at the full partition path. Section 6 reduces that complex by allowed moves to a shifted standard core, and Section 4 transports the base to a source-to-sink path. Section 5 and I4 identify the resulting diagram group with F_n. Finally I5 gives F_infinity.

This establishes the connected classification for each fixed n, with the explicitly identified imports. With the independently accepted SCOPE_AUDIT.md decomposition, Questions 71–72 follow conditionally on the stated restricted permutational interpretation. The original undefined terminology remains a scope hold. Credit belongs to Golan's July 2026 preprint; no novelty or journal acceptance is claimed.

## Primary references

- Gili Golan, *Irreducible fast sets of bump homeomorphisms generate copies of Thompson's groups F_n*, arXiv:2607.10961v1. https://arxiv.org/abs/2607.10961v1
- *Cohomological and metric properties of groups of homeomorphisms of R*, Oberwolfach Report 26/2018, especially p.1610, Questions 71–72. https://doi.org/10.4171/owr/2018/26
- C. Bleak, M. Brin, M. Kassabov, J. Moore, M. Zaremsky, *Groups of fast homeomorphisms of the interval and the ping-pong argument*. https://arxiv.org/abs/1701.08321v1
- J. Belk and L. Stott, *Pseudo-F_4 is isomorphic to F_4*. https://arxiv.org/abs/2303.16868v1
- V. Guba and M. Sapir, *Diagram groups and directed 2-complexes: homotopy and homology*. https://arxiv.org/abs/math/0301225v2
- G. Golan and E. Sapir, *On the generation problem in Thompson's groups F_n*, Remark 5.2. https://arxiv.org/abs/2606.00863v1
- K. S. Brown, *Finiteness properties of groups*, J. Pure Appl. Algebra 44 (1987), 45–75. https://doi.org/10.1016/0022-4049(87)90015-6 ; author-hosted scan: https://pi.math.cornell.edu/~kbrown/scan/1987.0044.0045.pdf
