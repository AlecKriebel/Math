# Hard capacity fare zone assignment with bounded congestion

## Result and scope

For the hard-capacity optimization problem stated by Britta Peis in Oberwolfach Report 50/2024, printed page 2992, the following baseline results hold under the explicit input assumptions below:

1. If each edge occurs in at most k commodity paths, decreasing-profit greedy returns a feasible solution of value at least OPT/k for k >= 1.
2. If congestion is at most two, an exact polynomial-time reduction to maximum-weight, unit-edge-capacitated b-matching is available.
3. The later paper *Fare Zone Assignment on Trees*, arXiv:2512.19493v3, defines a different, dropout-permitting optimization problem. Even its linear-pricing special case is not the hard-capacity problem. A two-edge path separates their optimum values, 3 and 4.

The first result is an application of the general k-extendible-system greedy guarantee introduced by Mestre [M]. The second uses classical general-graph weighted matching machinery [G]. Neither result is claimed to be new. This is a partial answer and a correction to an attempted transfer between models. It does not determine the best approximation ratio, prove a new hardness threshold, or resolve the original open-ended question.

## 1. The original model and computational assumptions

Let T=(V,E) be a finite tree, and let the commodities be indexed by I={1,...,q}. Each commodity has a specified edge path P_i, a weight w_i, and a capacity u_i. The printed problem [P] has binary edge variables y_e, objective sum_e c_e y_e, where c_e=sum_{i:e in P_i} w_i, and hard constraints sum_{e in P_i} y_e <= u_i for every i. Consequently, for F={e:y_e=1}, its objective is

    c(F) = sum_{e in F} c_e = sum_i w_i |F intersect P_i|,

subject to |F intersect P_i| <= u_i for all i. Each incidence has coefficient one; there are no edge-dependent resource demands.

For the algorithmic claims here assume:

- The finite tree and all commodities are explicitly listed. Paths are either explicit lists of edges or specified by their endpoints in the explicit tree, from which their unique paths can be recovered in polynomial time.
- The weights w_i are nonnegative rationals encoded in binary. The capacities u_i are nonnegative rationals encoded in binary, including nonnegative integers as a special case.
- Rational additions, comparisons, and floors are exact. A polynomial-time claim refers to this finite binary input model, not to unspecified access to arbitrary real numbers.

Set b_i=min(floor(u_i),|P_i|). This preserves feasibility because path-cut counts are integers between zero and |P_i|. In particular b_i is a nonnegative integer whose magnitude is at most |E|, even if u_i was given in binary and is numerically very large. For arbitrary real capacities the mathematical flooring observation remains valid, but a computational claim additionally requires a representation that permits the needed exact comparisons or floors.

The OWR paragraph does not explicitly give number domains, signs, or bit encodings. The preceding conventions are assumptions of this partial theorem and must not be presented as text expressly supplied in that paragraph. Nonnegative w_i imply nonnegative c_e. This nonnegativity is used in the stated greedy argument. Zero-weight commodities retain their hard constraints and must not be discarded just because their own revenue contribution is zero.

Define congestion by

    k = max_{e in E} |{i in I : e in P_i}|,

with k=0 if E is empty. Count the listed commodities, including distinct commodities with identical paths. Edges in no commodity path have c_e=0 and may be omitted without changing the optimum. If k=0 the optimum is zero and the empty set is optimal. Empty commodity paths and zero capacities cause no exception. A negative capacity, outside the theorem's assumptions, would make even the empty set infeasible.

Let L=sum_i |P_i|. Constructing the incidence lists and all c_e takes O(L) additions after the paths are available. Sorting requires O(|E| log |E|) exact comparisons, and capacity-counter feasibility tests and updates take O(L) further elementary operations. The quantities being added have polynomial bit length in the total rational input length, so these are polynomial-time operations in the stated model.

## 2. Exchange structure

Write FAM={F subset E : |F intersect P_i| <= b_i for every i}. It is nonempty and downward closed. We show directly that it is k-extendible for k >= 1.

Take A subset B in FAM and an edge e outside B with A union {e} in FAM. Only constraints whose paths contain e can be violated by adding e to B. For any such violated constraint i, integrality gives |B intersect P_i|=b_i. Since |A intersect P_i| <= b_i-1, choose f_i in (B intersect P_i) minus A. Let Z be the union of these chosen edges, with repeated choices counted once. At most k constraints contain e, hence |Z| <= k. For every violated constraint at least one edge was removed, and no nonviolated constraint becomes violated when edges are removed. Thus

    (B minus Z) union {e} is feasible, Z subset B minus A, and |Z| <= k.

This is exactly the exchange property used in the k-extendible framework [M]. The proof works for arbitrary explicitly listed subsets P_i; the tree-path assumption is not used.

## 3. Greedy approximation proof

Fix a total order of the edges in nonincreasing c_e order, resolving ties arbitrarily but consistently. Start with the empty set and scan every edge once, accepting it if all b_i constraints remain satisfied. Let G be the resulting feasible set. Let e_1,...,e_t be the accepted edges in their acceptance order and G_j={e_1,...,e_j}.

Start from an optimum feasible set O_0. Inductively maintain a feasible O_j containing G_j. If e_j belongs to O_{j-1}, set O_j=O_{j-1}. Otherwise apply the exchange statement with A=G_{j-1}, B=O_{j-1}, and e=e_j. This supplies Z_j subset O_{j-1} minus G_{j-1}, with |Z_j| <= k, for which

    O_j = (O_{j-1} minus Z_j) union {e_j}

is feasible and contains G_j.

Every f in Z_j was feasible to insert into G_{j-1}, because both f and G_{j-1} lie in the feasible set O_{j-1}. It cannot have been scanned earlier and rejected: the accepted set at any earlier scan was a subset of G_{j-1}, so downward closure would have made f feasible at that earlier scan as well. It also cannot have been accepted earlier, since Z_j is disjoint from G_{j-1}. Thus f occurs later than e_j in the scan and c_f <= c_{e_j}. Therefore, when an exchange occurs,

    c(O_{j-1}) - c(O_j)
      = c(Z_j) - c_{e_j}
      <= (|Z_j|-1)c_{e_j}
      <= (k-1)c_{e_j}.

When no exchange occurs the loss is zero, which also satisfies the last bound because k >= 1 and c_{e_j} >= 0.

At termination O_t=G. Indeed, an edge f in O_t minus G would have been rejected when scanned even though the accepted prefix together with f was a subset of feasible O_t. This is impossible. Telescoping the inequalities gives

    OPT - c(G) <= (k-1) sum_{j=1}^t c_{e_j} = (k-1)c(G),

and hence c(G) >= OPT/k. The argument includes zero profits, OPT=0, t=0, and arbitrary tie breaking. It does not use a division by OPT. For k=1 it gives exact optimality. For k=0 use the separate zero-optimum observation above.

## 4. Exact optimization when congestion is at most two

Construct a loopless undirected multigraph H. There is a vertex v_i of capacity b_i for every commodity i. For every original edge e with positive incidence:

- If it belongs to exactly two commodity paths i and j, add a distinct graph edge h_e between v_i and v_j.
- If it belongs to exactly one path i, create a new private vertex a_e of capacity one and add h_e between v_i and a_e.

Give h_e weight c_e and edge upper capacity one. Preserve parallel edges: two different original edges remain different selectable graph edges. Zero-incidence original edges may be omitted since they have zero weight and affect no constraint.

A b-matching here means a subset of these distinct graph edges, with degree at each vertex at most its capacity. For every retained original edge set F, select exactly {h_e:e in F}. At commodity vertex v_i its degree is |F intersect P_i|, and every private vertex has degree at most one automatically. Thus this map is a feasibility- and objective-preserving bijection between retained original choices and b-matchings of H. Omitting zero-incidence edges preserves the optimum, though it intentionally identifies otherwise different zero-revenue original choices.

This is the unit-edge-capacitated version: an uncapacitated b-matching convention that permits several copies of one h_e is not interchangeable with it. The graph H need not be bipartite. For example, the three two-leaf paths on a three-leaf star have congestion two and produce a triangle on the three commodity vertices. A general-graph matching method is required.

### An explicit polynomial reduction to ordinary weighted matching

For completeness, the following standard style of gadget removes any reliance on differing b-matching conventions. Clip each vertex capacity of H to its degree. Suppose H has s edges. Replace each vertex v by b(v) distinct slot vertices. For each edge h=uv of weight c_h, create two new vertices x_h,y_h; add the internal edge x_h y_h of weight 2+c_h, edges from x_h to every slot of u of weight 1+c_h, and edges from y_h to every slot of v of weight 1+c_h.

In a maximum-weight ordinary matching, every gadget is either matched internally or uses two slot edges. If neither gadget vertex is matched, adding its internal edge improves the objective. If just one is matched to a slot, replacing that edge by the internal edge improves the objective by exactly one and frees the slot. These alternatives exhaust all noncanonical possibilities.

Interpret a two-slot gadget as selection of h. Distinct matching edges cannot reuse a slot, so selected edges obey all b(v) bounds. Conversely, every feasible b-matching can assign distinct slots to its selected incident edges and can match all other gadgets internally. The resulting ordinary matching has value

    sum_{h in E(H)} (2+c_h) + sum_{h selected} c_h.

Consequently maximizing ordinary matching weight maximizes the required b-matching weight exactly. The graph has at most 4s vertices: at most 2s slot vertices and 2s gadget vertices. It has at most s+sum_v degree(v)b(v) <= s+4s^2 edges. All generated rational weights have polynomial encoding length. Classical polynomial-time maximum-weight matching on general graphs therefore finishes the reduction. Gabow [G], Section 1, pages 1-2, explicitly discusses ordinary weighted matching, its polynomial-time history, and generalizations; only that established algorithmic result is imported here. No claim is made to reproduce its blossom-algorithm proof.

In particular, neither huge binary capacities nor parallel original choices produce a pseudopolynomial blow-up. The clipping and separate edge gadgets are essential to these statements.

## 5. The later dropout model is different

Hoefer, Kauther, Pabst, Peis, and Tran [F], arXiv v3 dated 24 April 2026, define their FZA model in Definition 1 on PDF page 2. A commodity has a nonnegative integer cut budget and a positive integer weight; the pricing function is nonnegative, nondecreasing, and subadditive. They optimize over every edge subset, assigning the commodity weight times the pricing function of its cut count when its budget is respected, and zero contribution otherwise. The accompanying text explicitly describes dropping out. Page 3 additionally permits a positive base fare. Their letter k counts commodities; the congestion parameter is separately denoted cong on page 4. Here q counts commodities and k denotes congestion.

For f(t)=t, the two objective functions agree on hard-feasible F. However, the later model also admits hard-infeasible F, with a different objective formula on those choices. Thus OPT_dropout >= OPT_hard, but a dropout approximation does not by itself return a hard-feasible solution. Any transfer requires an additional feasibility-preserving argument with its own revenue guarantee. This observation does not establish that such a transfer is impossible and does not criticize the correctness of [F] for its own model. The approximation statements in its body, including Theorem 3 on PDF page 7, refer to its defined FZA model.

### Complete two-edge witness

Take a path with two edges e_1,e_2 and three commodities:

- P_0={e_1,e_2}, w_0=1, u_0=1;
- P_1={e_1}, w_1=2, u_1=1;
- P_2={e_2}, w_2=2, u_2=1.

Each edge is in two paths, so congestion is two. All input numbers are positive integers, and f(t)=t meets the later paper's pricing assumptions. The only hard-feasible sets are the empty set and the two singleton sets. Their values are respectively 0,3,3. The two-edge set violates the first capacity, so OPT_hard=3.

In the dropout model the same four sets have values respectively 0,3,3,4. For the two-edge choice the first commodity contributes zero and each singleton-path commodity contributes two. Hence OPT_dropout=4. This enumerates every choice and proves both claimed optima. The linear hard objective would have assigned value 6 to the two-edge set, but that set is infeasible in the hard model; 6 is not a hard feasible optimum or the dropout revenue.

## 6. Acceptance boundaries

The frozen candidate's exchange proof, reduction, and witness are mathematically correct under its stated nonnegativity and integral-capacity assumptions. This expanded account adds finite input encodings, capacity clipping, treatment of zero-incidence edges, and a general weighted matching gadget. It makes explicit which assumptions are added rather than supplied by the original short statement.

Accept the result as a bounded-congestion baseline and a verified model distinction. Do not mark the original problem fully solved or claim a sharp ratio or new algorithm. No audit here establishes or refutes other results in either primary source, or verifies the complete proofs of the later FZA paper. A broad novelty search and a classification for all k are outside this result.

## Public references

[P] Britta Peis, *Open Problem: Fare Zone Assignment*, in *Combinatorial Optimization*, Oberwolfach Report 50/2024, printed p. 2992 (PDF page 44). Public PDF: https://oa.tib.eu/renate/bitstreams/706cca58-da6b-4d8c-a979-ebf6e92658f0/download . The relevant original paragraph and displayed program were inspected in extracted text and in a rendered page.

[M] Julián Mestre, *Greedy in Approximation Algorithms*, Algorithms - ESA 2006, LNCS 4168, pp. 528-539. DOI: https://doi.org/10.1007/11841036_48 . Publisher page: https://link.springer.com/chapter/10.1007/11841036_48 . Official two-page preview: https://page-one.springer.com/pdf/preview/10.1007/11841036_48 . The inspected preview, printed pp. 528-529, states the general k-extendible greedy guarantee and discusses earlier independence-system guarantees. The complete chapter was not retrieved. The application and proof in Sections 2-3 above are supplied directly.

[G] Harold N. Gabow, *Data Structures for Weighted Matching and Extensions to b-matching and f-factors*, arXiv:1611.07541v1, 22 November 2016. https://arxiv.org/abs/1611.07541v1 ; PDF: https://arxiv.org/pdf/1611.07541v1 . Section 1, PDF pp. 1-2, was inspected for ordinary weighted matching and the differing definitions of generalized matchings. This is a primary algorithmic source, not a claim that its uncapacitated perfect b-matching definition can be used unchanged here.

[F] Martin Hoefer, Lennart Kauther, Philipp Pabst, Britta Peis, and Khai Van Tran, *Fare Zone Assignment on Trees*, arXiv:2512.19493v3, 24 April 2026. https://arxiv.org/abs/2512.19493v3 ; PDF: https://arxiv.org/pdf/2512.19493v3 . Definition 1 and its surrounding text on pp. 2-3 were inspected; pp. 1,4,7 were read for version, terminology, and theorem scope. This citation pins the inspected arXiv manuscript and makes no claim of journal acceptance or peer review.
